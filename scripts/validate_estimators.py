"""
Validate the TE / DE / ME estimators against the hand derivations in
docs/DERIVATIONS.md. Fails loudly if any estimate misses its analytic value by
more than `tol_sigma` Monte Carlo standard errors.

Run:  python3 scripts/validate_estimators.py
"""
import sys, os, json, hashlib, platform
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "src"))

import numpy as np
from p2.scm import REGISTRY, CRNStream, Q_FIDELITY, W_DIRECT
from p2.effects import estimate_effects, point_of_commitment, largest_effect_step

SEED = 20260813
N_ROLLOUTS = 4000
TOL_SIGMA = 4.0


def analytic(a_fact, y_fact, q, w, u3_fact):
    """Closed forms from docs/DERIVATIONS.md, recomputed here from parameters."""
    assert u3_fact < q, "derivation assumes the factual executing step followed the retrieval"
    a1f = a_fact[1]
    # CRN: a3 tracks a1 exactly, so y = w*a1 + (1-w)*a1 = a1
    te_crn = {0: 0.0, 1: 0.5 - y_fact, 2: 0.0, 3: (w * a1f + (1 - w) * q) - y_fact}
    de = {0: 0.0, 1: (w * 0.5 + (1 - w) * a_fact[3]) - y_fact, 2: 0.0, 3: te_crn[3]}
    me = {k: te_crn[k] - de[k] for k in te_crn}
    # marginal: fresh downstream noise. P(a3=1) = 1/2 when a1 is re-rolled.
    te_marg = {0: 0.5 - y_fact, 1: 0.5 - y_fact,
               2: (w * a1f + (1 - w) * q) - y_fact, 3: te_crn[3]}
    return te_marg, te_crn, de, me


def main():
    scm = REGISTRY["partial_mediation"]()
    crn = CRNStream(SEED)
    fact = scm.run(crn, replicate=0)
    a_fact, y_fact = fact.actions(), fact.outcome
    u3_fact = crn.uniform(3, 0)

    te_marg_a, te_crn_a, de_a, me_a = analytic(a_fact, y_fact, Q_FIDELITY, W_DIRECT, u3_fact)

    attrs = estimate_effects(scm, crn, a_fact, y_fact,
                             n_rollouts=N_ROLLOUTS, seed=SEED)

    print(f"SCM            : {scm.name}   q={Q_FIDELITY}  w={W_DIRECT}")
    print(f"factual        : a={a_fact}  y={y_fact}  u3={u3_fact:.4f}")
    print(f"rollouts/step  : {N_ROLLOUTS}   tolerance: {TOL_SIGMA} MC sigma\n")

    hdr = f"{'k':>2} {'kind':>12} {'TE_marg':>18} {'TE_crn':>18} {'DE':>18} {'ME':>18} {'pin':>6} {'chg':>5}"
    print(hdr); print("-" * len(hdr))

    failures = []
    for a in attrs:
        cells = []
        for arm, truth in (("te_marg", te_marg_a), ("te_crn", te_crn_a),
                           ("de", de_a), ("me", me_a)):
            e = getattr(a, arm)
            t = truth[a.step]
            dev = abs(e.estimate - t)
            sig = dev / e.se if e.se and e.se > 1e-12 else (0.0 if dev < 1e-12 else np.inf)
            ok = sig <= TOL_SIGMA
            if not ok:
                failures.append((a.step, arm, e.estimate, t, sig))
            cells.append(f"{e.estimate:+.3f}/{t:+.3f}{'' if ok else ' X'}")
        print(f"{a.step:>2} {a.kind:>12} " + " ".join(f"{c:>18}" for c in cells)
              + f" {a.pin_plausibility:>6.2f} {a.change_rate:>5.2f}")

    print("\nidentity check  ME = TE_crn - DE, per step:")
    for a in attrs:
        resid = abs(a.me.estimate - (a.te_crn.estimate - a.de.estimate))
        print(f"  step {a.step}: residual {resid:.2e}")
        assert resid < 1e-9, "decomposition identity violated"

    ms = attrs[1].mediated_share
    print(f"\nmediated share of step 1 : {ms:.3f}   analytic 1-w = {1-W_DIRECT:.3f}")

    print(f"\nCAR point-of-commitment locus (marginal arm) : step {point_of_commitment(attrs,'te_marg')}")
    print(f"largest |TE_crn| step                        : step {largest_effect_step(attrs,'te_crn')}")
    print("inert steps under marginal arm               : "
          f"step 0 = {attrs[0].te_marg.estimate:+.3f}, step 2 = {attrs[2].te_marg.estimate:+.3f}")
    print("inert steps under CRN arm                    : "
          f"step 0 = {attrs[0].te_crn.estimate:+.3f}, step 2 = {attrs[2].te_crn.estimate:+.3f}")

    if failures:
        print("\nFAILURES:")
        for f in failures:
            print(f"  step {f[0]} {f[1]}: est {f[2]:+.4f} vs analytic {f[3]:+.4f}  ({f[4]:.1f} sigma)")
        sys.exit(1)
    print("\nAll estimates within tolerance of the analytic values.")

    env = {"python": platform.python_version(), "numpy": np.__version__,
           "seed": SEED, "n_rollouts": N_ROLLOUTS, "q": Q_FIDELITY, "w": W_DIRECT}
    env["env_hash"] = hashlib.sha256(json.dumps(env, sort_keys=True).encode()).hexdigest()[:16]
    os.makedirs("results", exist_ok=True)
    with open("results/validation_partial_mediation.json", "w") as fh:
        json.dump({"env": env, "factual": {"actions": list(a_fact), "y": y_fact},
                   "steps": [{"step": a.step, "kind": a.kind,
                              "te_marg": a.te_marg.estimate, "te_crn": a.te_crn.estimate,
                              "de": a.de.estimate, "me": a.me.estimate,
                              "pin_plausibility": a.pin_plausibility,
                              "change_rate": a.change_rate} for a in attrs]}, fh, indent=2)
    print(f"env_hash {env['env_hash']} -> results/validation_partial_mediation.json")


if __name__ == "__main__":
    main()
