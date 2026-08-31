"""WS1.7: does the mediated SHARE survive a non-binary outcome with opposing paths?

THE QUESTION. H4 is a rank correlation on `mediated_share = |ME| / |TE_crn|`, and
`dry_run.py` computes exactly that. But `ME = TE_crn - DE` is an IDENTITY, not a
decomposition into non-negative parts. If `DE` and `TE_crn` carry OPPOSITE signs
then `|ME| = |TE - DE| > |TE|`, and the "share" exceeds 1. A share that exceeds 1
is not a share, and H4 would be a rank correlation computed on a corrupted
variable.

This is not a contrived worry. It is the classic SUPPRESSION case, and it has a
plain reading in an agent pipeline: a retrieval that directly supports approval
while causing a later verification step to raise a flag. Direct path up, mediated
path down. Every existing SCM in scm.py has both paths pushing the SAME way
(`y = w*a1 + (1-w)*a3`, both weights positive), so this case has never been
exercised.

HAND DERIVATION FIRST, per the project rule. Structure:

    a0 ~ Bern(1/2)                       inert
    a1 ~ Bern(1/2)                       retrieval
    a2 ~ Bern(1/2)                       inert
    a3 = a1      if u3 < q               executing tool call
       = 1 - a1  otherwise
    y  = w*a1 - (1-w)*a3                 NOTE THE MINUS

with w = 0.2, q = 0.9. Factual run at seed 20260813, replicate 0 is
a_fact = (0,1,1,1) with u3_fact = 0.7703699... < q, so a3 = a1 = 1.

    y_fact = w - (1-w) = 0.2 - 0.8 = -0.6

TE_crn(1): intervene a1, hold u3 factual so a3 = a1' deterministically.
    y = w*a1' - (1-w)*a1' = (2w-1)*a1' = -0.6*a1'
    E[y] = -0.3        TE_crn(1) = -0.3 - (-0.6) = +0.30

DE(1): intervene a1, pin a3 = 1.
    y = 0.2*a1' - 0.8,  E[y] = 0.1 - 0.8 = -0.7
    DE(1) = -0.7 - (-0.6) = -0.10

ME(1) = TE_crn - DE = 0.30 - (-0.10) = +0.40

    |ME| / |TE_crn| = 0.40 / 0.30 = 1.333...      <-- EXCEEDS 1

TE_crn(3): prefix holds a1 = 1, redraw a3' which follows a1 with probability q.
    y = 0.2 - 0.8*a3',  E[a3'] = q = 0.9,  E[y] = 0.2 - 0.72 = -0.52
    TE_crn(3) = -0.52 - (-0.6) = +0.08 ;  DE(3) = TE_crn(3) ;  ME(3) = 0

Steps 0 and 2 are inert: TE_crn = DE = ME = 0 exactly.

WHAT THIS SCRIPT ESTABLISHES. That the estimators are CORRECT here (they are, the
identity holds by construction), and that the REPORTING quantity built on top of
them is not. The bug is in the share, not in the effects.
"""
import sys, os, json, hashlib, platform
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "src"))
import numpy as np
from p2.scm import SyntheticSCM, CRNStream
from p2.effects import estimate_effects

SEED, N_ROLL, Q, W = 20260813, 4000, 0.9, 0.2
FAILS = []


def check(name, cond, detail=""):
    print(f"   {'ok  ' if cond else 'FAIL'}  {name}" + (f"   {detail}" if detail else ""))
    if not cond:
        FAILS.append(name)


def suppression_scm(q=Q, w=W):
    def free(prefix, u): return int(u < 0.5)
    def follow(prefix, u): return int(prefix[1]) if u < q else 1 - int(prefix[1])
    return SyntheticSCM(
        name="suppression",
        policies=[free, free, free, follow],
        outcome_fn=lambda a: w * a[1] - (1.0 - w) * a[3],
        kinds=["llm_call", "retrieval", "memory_read", "tool_call"],
        notes="Direct path and mediated path carry OPPOSITE signs.",
    )


def main():
    print(__doc__.split("HAND DERIVATION")[0].strip()[:400], "...\n")
    scm = suppression_scm()
    crn = CRNStream(SEED)
    fact = scm.run(crn, replicate=0)
    print(f"1. Factual run: actions={fact.actions()}  y_fact={fact.outcome:+.4f}")
    check("y_fact matches the derivation (-0.6)", abs(fact.outcome - (-0.6)) < 1e-12,
          f"{fact.outcome:+.6f}")

    attrs = estimate_effects(scm, crn, fact.actions(), fact.outcome,
                             n_rollouts=N_ROLL, pin_probes=16, seed=SEED)
    te = np.array([a.te_crn.estimate for a in attrs])
    de = np.array([a.de.estimate for a in attrs])
    me = np.array([a.me.estimate for a in attrs])

    print("\n2. Estimates against the hand derivation")
    ANALYTIC = {0: (0.0, 0.0, 0.0), 1: (0.30, -0.10, 0.40),
                2: (0.0, 0.0, 0.0), 3: (0.08, 0.08, 0.0)}
    print(f"   {'step':>4} {'TE_crn':>18} {'DE':>18} {'ME':>18}")
    for k in range(4):
        aT, aD, aM = ANALYTIC[k]
        print(f"   {k:>4} {te[k]:>+9.4f}/{aT:>+7.2f} {de[k]:>+9.4f}/{aD:>+7.2f} "
              f"{me[k]:>+9.4f}/{aM:>+7.2f}")
    for k in range(4):
        aT, aD, aM = ANALYTIC[k]
        tol = 0.05 if k in (1, 3) else 1e-9
        check(f"step {k} TE_crn", abs(te[k] - aT) < tol, f"{te[k]:+.4f} vs {aT:+.2f}")
        check(f"step {k} DE    ", abs(de[k] - aD) < tol, f"{de[k]:+.4f} vs {aD:+.2f}")

    print("\n3. The decomposition identity still holds exactly")
    resid = np.abs(me - (te - de)).max()
    check("ME == TE_crn - DE to machine precision", resid < 1e-12, f"max residual {resid:.2e}")
    print("   The estimators are NOT wrong. The identity is arithmetic and it holds.")

    print("\n4. THE DEFECT: the mediated SHARE exceeds 1")
    share = np.where(np.abs(te) > 1e-9, np.abs(me) / np.maximum(np.abs(te), 1e-9), 0.0)
    print(f"   {'step':>4} {'|ME|/|TE|':>12} {'sign(TE)':>9} {'sign(DE)':>9}  reading")
    for k in range(4):
        sT = int(np.sign(te[k])); sD = int(np.sign(de[k]))
        opposed = (sT * sD) < 0
        tag = "SUPPRESSION, share meaningless" if opposed else ("inert" if abs(te[k]) < 1e-9
                                                               else "ordinary")
        print(f"   {k:>4} {share[k]:>12.4f} {sT:>9} {sD:>9}  {tag}")
    check("step 1 share EXCEEDS 1, as derived", share[1] > 1.0, f"{share[1]:.4f} (analytic 1.333)")
    check("step 1 share matches the analytic 4/3", abs(share[1] - 4.0/3.0) < 0.08,
          f"{share[1]:.4f}")
    check("TE and DE carry opposite signs at step 1", te[1] * de[1] < 0,
          f"TE {te[1]:+.3f}, DE {de[1]:+.3f}")

    print("\n5. Why this matters for H4, which is a rank correlation on the share")
    print("   H4 predicts: the more of a node's influence travels through what it")
    print("   caused later steps to do, the more the trace under-ranks it. Under")
    print("   suppression the share is not a proportion at all: it is unbounded")
    print("   above, and it grows as |DE| grows in the OPPOSITE direction. Two")
    print("   nodes can get the same share for opposite mechanisms, so ranking on")
    print("   it mixes them. On this SCM step 1 would enter H4 with share 1.33,")
    print("   ranking it as MORE mediated than a pure mediator, whose share is")
    print("   exactly 1.0. That inverts the intended ordering.")
    pure_share = 1.0
    check("a suppressed node outranks a PURE mediator on the current statistic",
          share[1] > pure_share, f"{share[1]:.3f} > {pure_share:.1f}")

    print("\n6. The proposed fix, stated but NOT yet applied to dry_run.py")
    print("   Report the share ONLY when sign(DE) == sign(TE) and |DE| <= |TE|,")
    print("   which is the regime where the decomposition is a genuine split of a")
    print("   common-signed effect. Otherwise flag SUPPRESSION and report signed")
    print("   ME and DE without forming a ratio. H4 is then computed on the")
    print("   non-suppressed subset with the suppression rate reported alongside,")
    print("   exactly as PREREG s4 already requires discard rates to be reported")
    print("   rather than repaired.")
    n_supp = int(np.sum((te * de) < 0))
    print(f"   suppression rate on this SCM: {n_supp}/4 nodes")

    print()
    if FAILS:
        print("FAILURES:", FAILS); sys.exit(1)
    print("All suppression checks passed. The estimators are correct;")
    print("the mediated-share reporting statistic is not, and is now demonstrated.")
    env = {"python": platform.python_version(), "numpy": np.__version__,
           "seed": SEED, "n_rollouts": N_ROLL, "q": Q, "w": W}
    env["env_hash"] = hashlib.sha256(json.dumps(env, sort_keys=True).encode()).hexdigest()[:16]
    os.makedirs("results", exist_ok=True)
    json.dump({"env": env, "te": te.tolist(), "de": de.tolist(), "me": me.tolist(),
               "share": share.tolist(), "suppressed_nodes": n_supp},
              open("results/validation_suppression.json", "w"), indent=2)
    print(f"env_hash {env['env_hash']} -> results/validation_suppression.json")


if __name__ == "__main__":
    main()
