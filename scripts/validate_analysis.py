"""Validate the H1/H2 machinery against planted coefficients and known answers.
  1. tau_b against hand-computable cases.
  2. Coefficient recovery: plant betas, confirm the 95% CI covers them.
  3. Coverage: cluster-robust CIs must hit nominal 95%.
  4. Null control: with beta_recency = beta_verbosity = 0 the false positive rate
     must sit at alpha. If the machinery manufactures H2 out of noise, H2 is
     unpublishable and better to know now.
Validates STATISTICS on synthetic data. Not evidence about any real system."""
import sys, os, json, hashlib, platform
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "src"))
import numpy as np
from p2.observability import SyntheticTraceGenerator, kendall_tau_b, rank_desc
from p2.analysis import ols_cluster, bootstrap_over_decisions, vif

SEED, N_DECISIONS, N_STEPS, N_SIMS = 20260813, 200, 25, 400
Z = 1.959963985


def build(bc, br, bv, seed, n_dec=N_DECISIONS):
    gen = SyntheticTraceGenerator(n_steps=N_STEPS, beta_causal=bc,
                                  beta_recency=br, beta_verbosity=bv, seed=seed)
    rows, taus = [], []
    for d in range(n_dec):
        dec = gen.decision()
        taus.append(kendall_tau_b(rank_desc(dec["latent_obs"]), rank_desc(dec["causal"])))
        for i in range(N_STEPS):
            rows.append((d, dec["latent_obs"][i], dec["z_causal"][i],
                         dec["z_recency"][i], dec["z_verbosity"][i]))
    a = np.array(rows, float)
    X = np.column_stack([np.ones(len(a)), a[:, 2], a[:, 3], a[:, 4]])
    return X, a[:, 1], a[:, 0].astype(int), np.array(taus)


def main():
    print("1. Kendall tau_b against exact answers")
    for nm, x, y_, want in [("identity",[1,2,3,4,5],[1,2,3,4,5],1.0),
                            ("reversal",[1,2,3,4,5],[5,4,3,2,1],-1.0),
                            ("all tied",[1,2,3,4,5],[2,2,2,2,2],float("nan")),
                            ("one swap",[1,2,3,4],[1,2,4,3],4/6)]:
        g = kendall_tau_b(x, y_)
        ok = (np.isnan(g) and np.isnan(want)) or abs(g-want) < 1e-12
        print(f"  {nm:<10} got {g:>8.4f}  want {want:>8.4f}  {'ok' if ok else 'FAIL'}")
        assert ok, nm

    print("\n2. Coefficient recovery with planted betas")
    TRUE = np.array([0.0, 1.0, 0.6, -0.4])
    X, y, cl, taus = build(TRUE[1], TRUE[2], TRUE[3], SEED)
    beta, se_cl, se_nv = ols_cluster(X, y, cl)
    names = ["intercept","causal","recency","verbosity"]
    print(f"  {'term':>10} {'true':>7} {'est':>7} {'se_cl':>7} {'se_naive':>9} {'ratio':>6} {'cov':>5}")
    for j, nm in enumerate(names):
        cov = abs(beta[j]-TRUE[j]) <= Z*se_cl[j]
        print(f"  {nm:>10} {TRUE[j]:>7.3f} {beta[j]:>7.3f} {se_cl[j]:>7.4f} "
              f"{se_nv[j]:>9.4f} {se_cl[j]/se_nv[j]:>6.2f} {'yes' if cov else 'NO':>5}")
        assert cov, nm
    print(f"  VIFs: {np.round(vif(X[:,1:]),3)}")
    m, lo, hi = bootstrap_over_decisions(taus, seed=SEED)
    print(f"  mean tau_b = {m:.3f}  95% CI [{lo:.3f}, {hi:.3f}]")

    print(f"\n3. CI coverage over {N_SIMS} sims (nominal 95%)")
    hc, hn = np.zeros(4), np.zeros(4)
    for s in range(N_SIMS):
        Xs, ys, cls, _ = build(TRUE[1], TRUE[2], TRUE[3], SEED+1000+s, n_dec=60)
        b, sc, sn = ols_cluster(Xs, ys, cls)
        hc += (np.abs(b-TRUE) <= Z*sc); hn += (np.abs(b-TRUE) <= Z*sn)
    print(f"  {'term':>10} {'cluster':>9} {'naive':>9}")
    for j, nm in enumerate(names):
        print(f"  {nm:>10} {hc[j]/N_SIMS:>9.3f} {hn[j]/N_SIMS:>9.3f}")
    assert (hc[1:]/N_SIMS).min() >= 0.90, "cluster-robust CIs under-cover"

    print(f"\n4. Null control: beta_recency = beta_verbosity = 0, {N_SIMS} sims")
    fr = fv = 0
    for s in range(N_SIMS):
        Xs, ys, cls, _ = build(1.0, 0.0, 0.0, SEED+5000+s, n_dec=60)
        b, sc, _ = ols_cluster(Xs, ys, cls)
        fr += abs(b[2]) > Z*sc[2]; fv += abs(b[3]) > Z*sc[3]
    print(f"  false positive, recency   : {fr/N_SIMS:.3f}  (nominal 0.050)")
    print(f"  false positive, verbosity : {fv/N_SIMS:.3f}  (nominal 0.050)")
    assert fr/N_SIMS < 0.10 and fv/N_SIMS < 0.10, "H2 test manufactures effects from noise"

    print("\nAll four checks passed.")
    env = {"python": platform.python_version(), "numpy": np.__version__, "seed": SEED,
           "n_decisions": N_DECISIONS, "n_steps": N_STEPS, "n_sims": N_SIMS}
    env["env_hash"] = hashlib.sha256(json.dumps(env, sort_keys=True).encode()).hexdigest()[:16]
    os.makedirs("results", exist_ok=True)
    json.dump({"env": env, "true_betas": TRUE.tolist(), "beta": beta.tolist(),
               "se_cluster": se_cl.tolist(), "se_naive": se_nv.tolist(),
               "coverage_cluster": (hc/N_SIMS).tolist(),
               "coverage_naive": (hn/N_SIMS).tolist(),
               "fp_recency": fr/N_SIMS, "fp_verbosity": fv/N_SIMS,
               "mean_tau_b": m}, open("results/validation_analysis.json","w"), indent=2)
    print(f"env_hash {env['env_hash']} -> results/validation_analysis.json")


if __name__ == "__main__":
    main()
