"""END-TO-END DRY RUN on synthetic data.

=============================================================================
THESE ARE NOT RESULTS. Every number below comes from a synthetic SCM with a
planted structure. Nothing here is evidence about any real system. The purpose
is to exercise the entire chain once, in the exact shape Stage 1 will use, so
that interface and reporting problems surface now and not on the day the live
pipeline comes online.
=============================================================================

Chain: SCM -> real TE_crn/DE/ME estimators -> observability attributors ->
separation pre-check -> H1 (tau_b) -> H2 (PL joint Wald) -> H3 grid -> H4.

The first version of this script produced a verbosity coefficient of +172 with
p = 1e-98, because span duration and token count were both generated from the
same salience variable, making verbosity near-deterministic in the ranked score.
That is quasi-complete separation and it is now guarded in ranking.py. The
generator below gives duration and tokens a SHARED component plus INDEPENDENT
noise, which is the realistic case: correlated, not collinear.

Planted mechanism: trace salience tracks a node's DIRECT effect, not its total
effect. Mediating nodes are therefore quiet in the trace while carrying large
total effect. If the chain works, H1 should be poor, H2 should reject, H3 should
be non-zero and H4 positive.
"""
import sys, os, json, hashlib, platform, time
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "src"))
import numpy as np
from p2.scm import SyntheticSCM, CRNStream
from p2.effects import estimate_effects
from p2.observability import SpanRecord, ATTRIBUTORS, rank_desc, kendall_tau_b
from p2.analysis import bootstrap_over_decisions
from p2.ranking import (fit_plackett_luce, joint_wald, h3_statistic,
                        h4_statistic, separation_diagnostic)

SEED, N_DEC, N_ROLL, Q, RIDGE = 20260813, 40, 300, 0.9, 1.0


def chain_scm(q=Q):
    """Six nodes. 1 and 3 are retrievals driving executing steps 2 and 4; 0 and 5
    are inert. y depends on the executing steps only, so 1 and 3 act purely
    through mediation and have zero direct effect by construction."""
    def free(prefix, u): return int(u < 0.5)
    def follow(src):
        return lambda prefix, u: (int(prefix[src]) if u < q else 1 - int(prefix[src]))
    return SyntheticSCM(
        name="chain6",
        policies=[free, free, follow(1), free, follow(3), free],
        outcome_fn=lambda a: 0.5 * a[2] + 0.5 * a[4],
        kinds=["llm_call", "retrieval", "tool_call", "retrieval", "tool_call", "llm_call"],
    )


def main():
    t0 = time.time()
    print(__doc__.split("=====")[1].strip())
    print(f"\nN decisions {N_DEC}, rollouts/node {N_ROLL}, 6 nodes\n")

    rng = np.random.default_rng(SEED)
    scm = chain_scm()
    causal_l, obs_l, ms_l, spans_l = [], [], [], []

    for d in range(N_DEC):
        crn = CRNStream(SEED + d)
        fact = scm.run(crn, replicate=0)
        attrs = estimate_effects(scm, crn, fact.actions(), fact.outcome,
                                 n_rollouts=N_ROLL, pin_probes=8, seed=SEED + d)
        te = np.array([a.te_crn.estimate for a in attrs])
        de = np.array([a.de.estimate for a in attrs])
        me = np.array([a.me.estimate for a in attrs])
        share = np.where(np.abs(te) > 1e-9, np.abs(me) / np.maximum(np.abs(te), 1e-9), 0.0)

        # Salience tracks the DIRECT effect. Duration and tokens share it but each
        # carries independent noise, so they are correlated without either being a
        # deterministic function of the other. Collinear generators create
        # separation, which is a property of the test data, not of the world.
        s = np.abs(de)
        s = (s - s.mean()) / (s.std() if s.std() > 0 else 1.0)
        log_dur = 4.0 + 1.2 * s + rng.normal(0, 0.8, len(attrs))
        log_tok = 3.0 + 0.9 * s + rng.normal(0, 0.7, len(attrs))
        spans = [SpanRecord(i, attrs[i].kind, float(np.exp(log_dur[i])),
                            int(np.exp(log_tok[i])) + 1, is_terminal=(i == len(attrs) - 1))
                 for i in range(len(attrs))]

        causal_l.append(te); ms_l.append(share); spans_l.append(spans)
        obs_l.append({a.name: a.score(spans) for a in ATTRIBUTORS})

    print("PRE-CHECK  max |corr| between the ranked attributor score and each H2")
    print("           covariate. This is what produces separation, so it is")
    print("           reported before the test, not after.")
    rank_score = np.concatenate([np.log(o["span_duration"]) for o in obs_l])
    rec = np.concatenate([np.arange(len(o["span_duration"]), dtype=float) for o in obs_l])
    ver = np.concatenate([np.log([s.output_tokens for s in sp]) for sp in spans_l])
    for nm, v in [("recency", rec), ("verbosity", ver)]:
        print(f"           corr(log span_duration, {nm:>9}) = {np.corrcoef(rank_score, v)[0,1]:+.3f}")

    print("\nH1  tau_b(attributor, TE_crn), bootstrap over decisions")
    print(f"    {'attributor':>16} {'mean tau_b':>11} {'95% CI':>20}")
    h1 = {}
    for a in ATTRIBUTORS:
        taus = np.array([kendall_tau_b(rank_desc(o[a.name]), rank_desc(np.abs(c)))
                         for o, c in zip(obs_l, causal_l)])
        taus = taus[np.isfinite(taus)]
        m, lo, hi = bootstrap_over_decisions(taus, seed=SEED)
        h1[a.name] = (m, lo, hi)
        note = "  (binary: CI tight by construction)" if a.name == "terminal_action" else ""
        print(f"    {a.name:>16} {m:>11.3f}  [{lo:>+.3f}, {hi:>+.3f}]{note}")

    print("\nH2  PL joint 2-df Wald on (recency, verbosity) | causal rank")
    print("    PRE-REGISTERED PRIMARY CONTRAST")
    dec = []
    for o, c, sp in zip(obs_l, causal_l, spans_l):
        n = len(c)
        z = lambda v: (v - v.mean()) / (v.std() if v.std() > 0 else 1.0)
        X = np.column_stack([z(np.abs(c)), z(np.arange(n, dtype=float)),
                             z(np.log([s.output_tokens for s in sp]))])
        dec.append((X, list(np.argsort(-o["span_duration"]))))
    beta, se, V, it = fit_plackett_luce(dec, 3)
    sep, why = separation_diagnostic(beta, se)
    print(f"    separation check on the UNPENALISED fit: {sep}  ({why})")
    if sep:
        print("    -> PRIMARY CONTRAST REPORTED AS INDETERMINATE per PREREG s6.")
        beta, se, V, it = fit_plackett_luce(dec, 3, ridge=RIDGE)
        print(f"    -> ridge={RIDGE} refit shown as a BOUNDED DESCRIPTIVE estimate,")
        print("       no p-value claimed.")
    for j, nm in enumerate(["causal", "recency", "verbosity"]):
        print(f"    {nm:>16} {beta[j]:>+8.3f}  se {se[j]:.3f}   ratio to causal "
              f"{beta[j]/beta[0]:>+7.3f}")
    W, q, p = joint_wald(beta, V, (1, 2))
    if sep:
        print(f"    W = {W:.3f} (df {q}) NOT REPORTED AS A TEST under separation")
    else:
        print(f"    joint Wald W = {W:.3f}, df = {q}, p = {p:.3g}   "
              f"{'REJECT' if p < 0.05 else 'no rejection'} at alpha=0.05")
    print("    coefficients are RATIOS: PL absorbs a common scale factor")

    print("\nH3  causally dominant but ranked negligible, (delta, tau) grid")
    obs_rank_l = [rank_desc(o["span_duration"]) for o in obs_l]
    print(f"    {'delta':>6} {'tau':>6} {'rate':>7} {'95% CI':>18}")
    for delta in [1.0, 0.9, 0.8]:
        for tau in [0.25, 0.5, 0.75]:
            est, lo, hi, k, n = h3_statistic(causal_l, obs_rank_l, delta, tau)
            print(f"    {delta:>6.1f} {tau:>6.2f} {est:>7.3f}  [{lo:>.3f}, {hi:>.3f}]")

    print("\nH4  does the discrepancy concentrate in MEDIATED nodes")
    cau_rank_l = [rank_desc(np.abs(c)) for c in causal_l]
    taus4 = h4_statistic(ms_l, obs_rank_l, cau_rank_l)
    m4, lo4, hi4 = bootstrap_over_decisions(taus4, seed=SEED)
    print(f"    tau_b(mediated share, obs_rank - causal_rank) = {m4:+.3f}  "
          f"[{lo4:+.3f}, {hi4:+.3f}]")

    print(f"\nchain completed in {time.time()-t0:.0f}s.")
    print("NOT RESULTS: synthetic SCM, planted structure, no real system.")
    env = {"python": platform.python_version(), "numpy": np.__version__,
           "seed": SEED, "n_dec": N_DEC, "n_roll": N_ROLL}
    env["env_hash"] = hashlib.sha256(json.dumps(env, sort_keys=True).encode()).hexdigest()[:16]
    os.makedirs("results", exist_ok=True)
    json.dump({"SYNTHETIC_NOT_RESULTS": True, "env": env,
               "h1": {k: list(v) for k, v in h1.items()},
               "h2": {"beta": beta.tolist(), "se": se.tolist(), "separated": bool(sep)},
               "h4": [m4, lo4, hi4]},
              open("results/dry_run.json", "w"), indent=2)
    print(f"env_hash {env['env_hash']} -> results/dry_run.json")


if __name__ == "__main__":
    main()
