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
                        separation_diagnostic, h4_statistic)
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
        taus = h4_statistic(ms_l, obs_l, cau_l)
        bs = np.array([taus[rr.integers(0, taus.size, taus.size)].mean() for _ in range(2000)])
        lo, hi = np.quantile(bs, [0.025, 0.975]); res[frac] = (taus.mean(), lo, hi)
        print(f"   frac ranked by DE = {frac:.1f}   tau = {taus.mean():+.4f}  "
              f"[{lo:+.4f}, {hi:+.4f}]")
    check("no false positive when the mechanism is absent",
          res[0.0][1] <= 0 <= res[0.0][2])
    check("detects the mechanism when fully present", res[1.0][1] > 0)
    check("monotone in how often the trace ranks by DE",
          res[0.0][0] < res[0.5][0] < res[1.0][0])

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
