"""
Validate the CRN coupling claim against theory, and measure how it degrades as
contexts diverge. This is WS2.7, the highest technical risk in the paper.

Two claims under test, each against its own closed form.

  1. Shared-u inverse-transform coupling in fixed index order agrees at rate
     quantile_agreement(p,q) = sum_i max(0, min(P_i,Q_i) - max(P_{i-1},Q_{i-1})).
     An earlier draft wrongly claimed this equals 1 - TV(p,q); this script
     rejected that at up to 215 sigma, which is why it exists.
  2. Maximal coupling agrees at rate exactly 1 - TV(p,q), the optimum.

The gap between them is the value of carrying the factual branch's distribution
at draw time, and it decides whether ME is estimable with usable precision once
contexts diverge. Third column measures a further degradation from sorting the
vocabulary by probability, as a naive top-k sampler does.
"""
import sys, os, json, hashlib, platform
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "src"))

import numpy as np
from p2.coupling import (keyed_uniform, inverse_transform, total_variation,
                         overlap, maximal_coupling_sample, measure_coupling)

SEED = 20260813
N_DRAWS = 40000
VOCAB = 32
TOL_SIGMA = 4.0


def softmax(z):
    z = z - z.max()
    e = np.exp(z)
    return e / e.sum()


def coupled_agreement_sorted_by_prob(p, q, run_id, step, n_draws):
    """The WRONG implementation: each branch walks its own probability-sorted CDF."""
    ip, iq = np.argsort(-p), np.argsort(-q)
    ps, qs = p[ip], q[iq]
    agree = 0
    for r in range(n_draws):
        u = keyed_uniform(run_id, step, r)
        agree += ip[inverse_transform(ps, u)] == iq[inverse_transform(qs, u)]
    return agree / n_draws


def main():
    rng = np.random.default_rng(SEED)
    base = rng.normal(0, 1.5, VOCAB)
    p = softmax(base)

    print(f"vocab {VOCAB}   draws/point {N_DRAWS}   tolerance {TOL_SIGMA} MC sigma\n")
    hdr = (f"{'shift':>6} {'TV':>7} | {'quant':>7} {'emp':>7} {'sig':>6} | "
           f"{'max':>7} {'emp':>7} {'sig':>6} | {'gain':>6} {'psort':>7}")
    print(hdr); print("-" * len(hdr))

    rows, failures = [], []
    for shift in [0.0, 0.25, 0.5, 1.0, 2.0, 4.0]:
        q = softmax(base + rng.normal(0, shift, VOCAB))

        rep = measure_coupling(p, q, "validate", 0, n_draws=N_DRAWS)
        qb = rep.quantile_bound
        se_q = np.sqrt(max(qb * (1 - qb), 1e-12) / N_DRAWS)
        sig_q = abs(rep.empirical_agreement - qb) / se_q
        if sig_q > TOL_SIGMA:
            failures.append(("quantile", shift, rep.empirical_agreement, qb, sig_q))

        agree_max = 0
        for r in range(N_DRAWS):
            a, b = maximal_coupling_sample(
                p, q, keyed_uniform("v", 0, r, 0),
                keyed_uniform("v", 0, r, 1), keyed_uniform("v", 0, r, 2))
            agree_max += a == b
        emp_max = agree_max / N_DRAWS
        mb = rep.overlap_bound
        se_m = np.sqrt(max(mb * (1 - mb), 1e-12) / N_DRAWS)
        sig_m = abs(emp_max - mb) / se_m
        if sig_m > TOL_SIGMA:
            failures.append(("maximal", shift, emp_max, mb, sig_m))

        wrong = coupled_agreement_sorted_by_prob(p, q, "validate", 0, N_DRAWS)
        print(f"{shift:>6.2f} {rep.tv:>7.4f} | {qb:>7.4f} {rep.empirical_agreement:>7.4f} "
              f"{sig_q:>6.1f} | {mb:>7.4f} {emp_max:>7.4f} {sig_m:>6.1f} | "
              f"{mb - qb:>6.3f} {wrong:>7.4f}")
        rows.append({"shift": shift, "tv": rep.tv, "quantile_bound": qb,
                     "quantile_emp": rep.empirical_agreement,
                     "maximal_bound": mb, "maximal_emp": emp_max,
                     "gain": mb - qb, "prob_sorted": wrong})

    print("\nidentity check  overlap(p,q) == 1 - TV(p,q):")
    for shift in [0.5, 2.0]:
        q = softmax(base + rng.normal(0, shift, VOCAB))
        resid = abs(overlap(p, q) - (1 - total_variation(p, q)))
        print(f"  shift {shift}: residual {resid:.2e}")
        assert resid < 1e-12, "overlap identity violated"

    print("\norder independence  keyed_uniform is a pure function of its key:")
    a = [keyed_uniform("r", 3, i) for i in range(5)]
    b = [keyed_uniform("r", 3, i) for i in reversed(range(5))][::-1]
    print(f"  forward vs reverse call order identical: {a == b}")
    assert a == b, "keyed draw depends on call order"

    if failures:
        print("\nFAILURES:")
        for f in failures:
            print(f"  {f[0]} shift {f[1]}: empirical {f[2]:.4f} vs closed form {f[3]:.4f} ({f[4]:.1f} sigma)")
        sys.exit(1)
    print("\nBoth couplings match their closed forms at every shift.")
    print("Maximal coupling dominates quantile coupling everywhere; the gain column")
    print("is the agreement bought by a second forward pass per step.")

    env = {"python": platform.python_version(), "numpy": np.__version__,
           "seed": SEED, "n_draws": N_DRAWS, "vocab": VOCAB}
    env["env_hash"] = hashlib.sha256(json.dumps(env, sort_keys=True).encode()).hexdigest()[:16]
    os.makedirs("results", exist_ok=True)
    with open("results/validation_coupling.json", "w") as fh:
        json.dump({"env": env, "rows": rows}, fh, indent=2)
    print(f"env_hash {env['env_hash']} -> results/validation_coupling.json")


if __name__ == "__main__":
    main()
