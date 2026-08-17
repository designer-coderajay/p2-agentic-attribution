"""Validate the Plackett-Luce estimator and the H3 statistic against known answers.

  1. PL correctly specified (Gumbel latents). Must recover planted beta. If it
     cannot recover its own generative model the estimator is broken.
  2. Coverage over repeated fits.
  3. PL misspecified (Gaussian latents, which is what our trace generator uses).
     Bias measured, not assumed away.
  4. H3 against a closed form: if the trace ranking is independent of causation in
     a fraction p of decisions, the top causal node lands in the bottom (1 - tau)
     of the ranking with probability (1 - tau), so E[H3] = p * (1 - tau).
"""
import sys, os, json, hashlib, platform
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "src"))
import numpy as np
from p2.ranking import fit_plackett_luce, h3_statistic
from p2.observability import rank_desc

SEED, N_STEPS, Z = 20260813, 12, 1.959963985
TRUE = np.array([1.0, 0.6, -0.4])


def make(n_dec, noise, seed, n_steps=N_STEPS):
    r = np.random.default_rng(seed)
    out = []
    for _ in range(n_dec):
        X = r.normal(0, 1, (n_steps, 3))
        eta = X @ TRUE
        e = (-np.log(-np.log(r.random(n_steps))) if noise == "gumbel"
             else r.normal(0, 1, n_steps))
        out.append((X, list(np.argsort(-(eta + e)))))
    return out


def main():
    print("1. Plackett-Luce, correctly specified (Gumbel)")
    d = make(400, "gumbel", SEED)
    b, se, it = fit_plackett_luce(d, 3)
    print(f"   converged in {it} Newton steps")
    for j, nm in enumerate(["causal", "recency", "verbosity"]):
        cov = abs(b[j] - TRUE[j]) <= Z * se[j]
        print(f"   {nm:>10} true {TRUE[j]:>6.3f}  est {b[j]:>6.3f}  se {se[j]:.4f}  "
              f"{'covered' if cov else 'NOT COVERED'}")
        assert cov, nm

    print("\n2. Coverage over 300 sims, 120 decisions each (nominal 0.950)")
    hits = np.zeros(3)
    for s in range(300):
        bb, ss, _ = fit_plackett_luce(make(120, "gumbel", SEED + 3000 + s), 3)
        hits += (np.abs(bb - TRUE) <= Z * ss)
    print(f"   {np.round(hits/300, 3)}")
    assert (hits / 300).min() >= 0.90, "PL cluster-robust CIs under-cover"

    print("\n3. Misspecified (Gaussian latents, as our trace generator uses)")
    bg, seg, _ = fit_plackett_luce(make(400, "gauss", SEED + 7), 3)
    scale = bg[0] / TRUE[0]
    print(f"   {'term':>10} {'true':>7} {'est':>7} {'est/scale':>10}")
    for j, nm in enumerate(["causal", "recency", "verbosity"]):
        print(f"   {nm:>10} {TRUE[j]:>7.3f} {bg[j]:>7.3f} {bg[j]/scale:>10.3f}")
    print(f"   common scale factor {scale:.3f}: Gaussian noise has sd 1 against")
    print("   Gumbel's pi/sqrt(6) = 1.283, so PL rescales. RATIOS survive, levels")
    print("   do not. H2 must therefore be read as relative, not absolute.")
    rt, re = TRUE[1:] / TRUE[0], bg[1:] / bg[0]
    print(f"   ratio recovery: true {np.round(rt,3)} est {np.round(re,3)}")
    assert np.abs(re - rt).max() < 0.10, "ratios not preserved"

    print("\n4. H3 against closed form  E[H3] = p * (1 - tau)")
    r = np.random.default_rng(SEED)
    print(f"   {'p':>5} {'tau':>5} {'expected':>9} {'observed':>9} {'95% CI':>18}")
    for p in [0.0, 0.3, 0.6]:
        for tau in [0.5, 0.75]:
            cl, ol = [], []
            for _ in range(1500):
                causal = r.normal(0, 1, N_STEPS)
                obs = (r.normal(0, 1, N_STEPS) if r.random() < p
                       else causal + 0.01 * r.normal(0, 1, N_STEPS))
                cl.append(causal); ol.append(rank_desc(np.abs(obs)))
            est, lo, hi, k, n = h3_statistic(cl, ol, delta=1.0, tau=tau)
            exp = p * (1 - tau)
            inside = lo <= exp <= hi
            print(f"   {p:>5.2f} {tau:>5.2f} {exp:>9.3f} {est:>9.3f} "
                  f"[{lo:.3f}, {hi:.3f}] {'ok' if inside else 'FAIL'}")
            assert inside, f"H3 off closed form at p={p}, tau={tau}"

    print("\nAll checks passed.")
    env = {"python": platform.python_version(), "numpy": np.__version__,
           "seed": SEED, "n_steps": N_STEPS}
    env["env_hash"] = hashlib.sha256(json.dumps(env, sort_keys=True).encode()).hexdigest()[:16]
    os.makedirs("results", exist_ok=True)
    json.dump({"env": env, "pl_true": TRUE.tolist(), "pl_gumbel": b.tolist(),
               "pl_se": se.tolist(), "coverage": (hits/300).tolist(),
               "pl_gauss": bg.tolist(), "scale": float(scale)},
              open("results/validation_ranking.json", "w"), indent=2)
    print(f"env_hash {env['env_hash']} -> results/validation_ranking.json")


if __name__ == "__main__":
    main()
