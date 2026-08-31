"""Validate the PRE-REGISTERED PRIMARY CONTRAST, the separation guard, and H4.

PREREG.md locks the primary contrast as a joint 2-df Wald test of
(beta_recency, beta_verbosity) = (0,0) under Plackett-Luce. A pre-registered test
statistic that has never been checked is the same error as a pre-registered
estimator that has never been checked. Until now these numbers existed only in
commit messages. This makes them runnable.

  1. chi2 survival at df=2 against its closed form exp(-x/2).
  2. Wald SIZE under the null: rejection rate must sit at alpha.
  3. Wald POWER under a planted alternative.
  4. SEPARATION REGRESSION TEST. The |z| > 40 rule was a false-positive
     generator and was removed; this pins that it cannot come back.
  5. H4 against a planted mechanism, with a null control.
"""
import sys, os, json, hashlib, platform, time
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "src"))
import numpy as np
from p2.ranking import (fit_plackett_luce, joint_wald, chi2_sf_df2,
                        separation_diagnostic, h4_statistic, normalized_beta,
                        bootstrap_normalized_beta)
from p2.observability import rank_desc

SEED, N_STEPS, Z = 20260813, 12, 1.959963985
FAILS = []


def check(name, cond, detail=""):
    print(f"   {'ok  ' if cond else 'FAIL'}  {name}" + (f"   {detail}" if detail else ""))
    if not cond:
        FAILS.append(name)


def make(n_dec, beta, seed, n_steps=N_STEPS):
    r = np.random.default_rng(seed); out = []
    for _ in range(n_dec):
        X = r.normal(0, 1, (n_steps, 3))
        e = -np.log(-np.log(r.random(n_steps)))
        out.append((X, list(np.argsort(-(X @ beta + e)))))
    return out


def main():
    t0 = time.time()
    print("1. chi2 survival at df=2 against exp(-x/2)")
    print("   df=2 chi-square is an exponential with mean 2, so the survival")
    print("   function is exact. No scipy, no approximation.")
    r = np.random.default_rng(SEED)
    d = r.normal(0, 1, 400000)**2 + r.normal(0, 1, 400000)**2
    for x in [0.5, 2.0, 5.991, 9.21]:
        emp = float((d > x).mean()); cf = chi2_sf_df2(x)
        se = np.sqrt(cf*(1-cf)/400000)
        check(f"x={x:<6.3f} closed {cf:.5f} vs simulated {emp:.5f}",
              abs(emp-cf)/se < 4.0, f"{abs(emp-cf)/se:.1f} sigma")
    check("critical value at alpha=.05 is 5.9915",
          abs(-2*np.log(0.05) - 5.9915) < 1e-3)

    print("\n2. Wald SIZE under the null, 120 sims of 80 decisions")
    NS = 120
    rej5 = rej1 = 0
    for s in range(NS):
        b, _, V, _ = fit_plackett_luce(make(80, np.array([1.,0.,0.]), SEED+200000+s), 3)
        p = joint_wald(b, V, (1, 2))[2]
        rej5 += p < 0.05; rej1 += p < 0.01
    for a, rj in [(0.05, rej5), (0.01, rej1)]:
        emp = rj/NS; se = np.sqrt(a*(1-a)/NS)
        check(f"alpha={a:.2f}  rejection {emp:.4f}", abs(emp-a)/se < 4.0,
              f"{(emp-a)/se:+.1f} sigma")

    print("\n3. Wald POWER under a planted alternative, 80 sims each")
    for mag in [0.0, 0.2, 0.4]:
        rej = 0
        for s in range(80):
            b, _, V, _ = fit_plackett_luce(
                make(80, np.array([1.0, mag, -mag*0.7]), SEED+400000+s), 3)
            rej += joint_wald(b, V, (1, 2))[2] < 0.05
        print(f"   (beta_r, beta_v) = ({mag:>5.2f}, {-mag*0.7:>5.2f})   power {rej/80:.3f}")

    print("\n4. SEPARATION REGRESSION TEST")
    print("   z = |beta|/se grows like sqrt(N), so a fixed z cut fires on strong")
    print("   well-identified effects. Pinned here so the rule cannot return.")
    TRUE = np.array([1.0, 0.6, -0.4])
    for n in [100, 400, 1600]:
        b, se, _, _ = fit_plackett_luce(make(n, TRUE, 7), 3)
        z = abs(b[0])/se[0]
        sep, why = separation_diagnostic(b, se)
        check(f"n={n:<5} |z|={z:>5.1f}  not flagged", not sep, why)
    rr = np.random.default_rng(1); dec = []
    for _ in range(60):
        X = rr.normal(0, 1, (10, 3)); X[:, 2] = np.arange(10)[::-1]
        dec.append((X, list(range(10))))
    b, se, V, _ = fit_plackett_luce(dec, 3)
    sep, why = separation_diagnostic(b, se)
    check("truly separated design IS flagged", sep, why)
    check("unpenalised p would read as overwhelming",
          joint_wald(b, V, (1, 2))[2] < 1e-6, f"p={joint_wald(b,V,(1,2))[2]:.3g}")
    b2, se2, V2, _ = fit_plackett_luce(dec, 3, ridge=1.0)
    check(f"ridge=1.0 bounds beta from {abs(b).max():.1f} to {abs(b2).max():.2f}",
          abs(b2).max() < 10.0)
    check("penalised p is STILL not trustworthy, hence INDETERMINATE",
          joint_wald(b2, V2, (1, 2))[2] < 1e-6, f"p={joint_wald(b2,V2,(1,2))[2]:.3g}")
    b3, _, _, _ = fit_plackett_luce(make(400, TRUE, 7), 3)
    b4, _, _, _ = fit_plackett_luce(make(400, TRUE, 7), 3, ridge=1.0)
    check("ridge costs nothing on a well-behaved fit",
          np.abs(b4-b3).max() < 0.01, f"max shift {np.abs(b4-b3).max():.4f}")

    print("\n5. H4 against a planted mechanism")
    print("   Plant: the trace ranks by DIRECT effect while causation ranks by")
    print("   TOTAL. Mediated nodes are then under-ranked, so tau must be > 0.")
    rr = np.random.default_rng(SEED + 11)
    res = {}
    for frac in [0.0, 0.5, 1.0]:
        ms_l, obs_l, cau_l = [], [], []
        for _ in range(400):
            te = rr.normal(0, 1, N_STEPS)
            share = rr.random(N_STEPS)
            de = te * (1 - share)
            basis = de if rr.random() < frac else te
            ms_l.append(share)
            obs_l.append(rank_desc(np.abs(basis) + 0.05*rr.normal(0, 1, N_STEPS)))
            cau_l.append(rank_desc(np.abs(te)))
        # h4_statistic returns (taus, n_dropped, n_total) since WS1.7, so that a
        # caller cannot report H4 without also being handed its exclusion rate.
        taus, n_drop, n_tot = h4_statistic(ms_l, obs_l, cau_l)
        assert n_drop == 0, (
            f"planted H4 design should have no excluded nodes, got {n_drop}/{n_tot}. "
            "Shares here are drawn in [0,1) by construction, so any exclusion means "
            "the generator or mediated_share has changed.")
        bs = np.array([taus[rr.integers(0, taus.size, taus.size)].mean() for _ in range(2000)])
        lo, hi = np.quantile(bs, [0.025, 0.975]); res[frac] = (taus.mean(), lo, hi)
        print(f"   frac ranked by DE = {frac:.1f}   tau = {taus.mean():+.4f}  "
              f"[{lo:+.4f}, {hi:+.4f}]")
    check("no false positive when the mechanism is absent",
          res[0.0][1] <= 0 <= res[0.0][2])
    check("detects the mechanism when fully present", res[1.0][1] > 0)
    check("monotone in how often the trace ranks by DE",
          res[0.0][0] < res[0.5][0] < res[1.0][0])

    print("\n6. NORMALISED-BETA REPORTING CONVENTION (replaces ratio-to-causal)")
    print("   Gate D deviation, 2026-08-20: ratio-to-beta_causal blows up exactly")
    print("   when H1/H2 hold, because both predict beta_causal is small. Fix:")
    print("   report beta / ||beta||_2, invariant to the same scale ambiguity,")
    print("   well-defined whenever any coefficient carries signal.")

    print("\n   6a. Exact invariance under beta -> c*beta, V -> c^2*V")
    rng6 = np.random.default_rng(2026)
    A = rng6.normal(0, 1, (3, 3)); V0 = A @ A.T + 0.1 * np.eye(3)
    b0 = np.array([-0.029, 0.067, 0.780])  # the actual dry-run fit
    g0, se0, _ = normalized_beta(b0, V0)
    for c in [0.3, 1.0, 5.0, 50.0]:
        gc, sec, _ = normalized_beta(c * b0, c * c * V0)
        check(f"c={c:<6.1f} g invariant", np.allclose(gc, g0, atol=1e-9),
              f"max|dg|={np.abs(gc-g0).max():.2e}")
        check(f"c={c:<6.1f} se invariant", np.allclose(sec, se0, atol=1e-9),
              f"max|dse|={np.abs(sec-se0).max():.2e}")

    print("\n   6b. Old convention blows up as beta_causal -> 0; new one does not")
    print(f"   {'beta_causal':>12} {'old: verb/causal':>18} {'new: g_verbosity':>18}")
    b_rec, b_ver = 0.067, 0.780
    prev_old = None
    diverges = False
    for bc in [0.5, 0.1, 0.01, 0.001, -0.029, -0.001]:
        b = np.array([bc, b_rec, b_ver])
        old_ratio = b_ver / bc
        g, se, _ = normalized_beta(b, V0)
        print(f"   {bc:>12.4f} {old_ratio:>18.2f} {g[2]:>18.4f}")
        if prev_old is not None and abs(old_ratio) > 5 * abs(prev_old):
            diverges = True
        prev_old = old_ratio
    check("old ratio-to-causal is unbounded as beta_causal -> 0", diverges)
    check("new normalised beta stays within [-1, 1] by construction",
          all(-1 - 1e-9 <= normalized_beta(np.array([bc, b_rec, b_ver]), V0)[0][2]
              <= 1 + 1e-9 for bc in [0.5, 0.1, 0.01, 0.001, -0.029, -0.001, 0.0]))

    print("\n   6c. Delta-method SE against Monte Carlo, at a realistic N=300-scale V")
    print("      (se should be small relative to beta, as it will be with the")
    print("      pre-registered corpus size; V0 above is deliberately adversarial)")
    V_real = V0 * (0.06 ** 2) / np.mean(np.diag(V0))  # se ~ 0.06-0.15, realistic for N>=300
    g_hat, se_delta, note_real = normalized_beta(b0, V_real)
    draws = rng6.multivariate_normal(b0, V_real, size=200000)
    norms = np.linalg.norm(draws, axis=1)
    keep = norms > 1e-6
    g_mc = draws[keep] / norms[keep, None]
    se_mc = g_mc.std(axis=0)
    print("      Known limitation, not a bug: near |g_j| = 1 the map beta_j ->")
    print("      beta_j/||beta|| is locally flat (d g_j/d beta_j scales like")
    print("      1 - g_j^2), so the first-order delta method under-states se")
    print("      there. This is why the PAPER'S reported CI for normalised beta")
    print("      is a decision-level bootstrap refit, not the delta se; the delta")
    print("      se is a fast diagnostic only. Tolerance below reflects that.")
    for j in range(3):
        rel = abs(se_delta[j] - se_mc[j]) / se_mc[j]
        near_pole = abs(g_hat[j]) > 0.95
        tol = 0.40 if near_pole else 0.15
        check(f"component {j}: delta se {se_delta[j]:.4f} vs MC se {se_mc[j]:.4f}"
              + ("  (near pole, wider tolerance)" if near_pole else ""),
              rel < tol, f"{rel:.1%} relative difference")
    check("no caution flag at realistic SE scale", note_real == "")

    print("\n   6d. Caution flag fires, and is right to, when se is large relative to")
    print("      ||beta|| (V0 above: se ~ 1-2 against ||beta|| = 0.78)")
    _, se_adversarial, note_adversarial = normalized_beta(b0, V0)
    check("delta method is NOT trusted blindly: caution note fires",
          note_adversarial != "", note_adversarial)

    print("\n   6e. Decision-level bootstrap CI (the interval reported in the paper,")
    print("       correct at the pole where the delta method is not) recovers a")
    print("       planted direction dominated by verbosity, the H2-true regime.")
    TRUE6 = np.array([0.05, 0.15, 1.2])
    g_true6 = TRUE6 / np.linalg.norm(TRUE6)
    dec6 = make(80, TRUE6, 909, n_steps=8)
    g_hat6, lo6, hi6 = bootstrap_normalized_beta(dec6, 3, n_boot=80, seed=909)
    covered = (lo6 <= g_true6) & (g_true6 <= hi6)
    for j, nm in enumerate(["causal", "recency", "verbosity"]):
        print(f"       {nm:>10}  g_hat={g_hat6[j]:>+.3f}  "
              f"[{lo6[j]:>+.3f}, {hi6[j]:>+.3f}]  true={g_true6[j]:>+.3f}  "
              f"{'covered' if covered[j] else 'MISSED'}")
    check("bootstrap CI covers the planted direction on all 3 components",
          bool(covered.all()))
    check("bootstrap CI is finite everywhere", bool(np.all(np.isfinite(lo6))
                                                     and np.all(np.isfinite(hi6))))

    print()
    if FAILS:
        print("FAILURES:", FAILS); sys.exit(1)
    print(f"All primary-contrast checks passed in {time.time()-t0:.0f}s.")
    env = {"python": platform.python_version(), "numpy": np.__version__, "seed": SEED}
    env["env_hash"] = hashlib.sha256(json.dumps(env, sort_keys=True).encode()).hexdigest()[:16]
    os.makedirs("results", exist_ok=True)
    json.dump({"env": env, "h4": {str(k): list(v) for k, v in res.items()}},
              open("results/validation_primary.json", "w"), indent=2)
    print(f"env_hash {env['env_hash']} -> results/validation_primary.json")


if __name__ == "__main__":
    main()
