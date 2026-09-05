"""WS1.11. When does an exact zero under common random numbers mean inertness?

Answer: not always, and the paper said otherwise until this script was written.

This validator was written in response to an adversarial review of the
manuscript, which observed that on the planted chain of section 3 the decisive
retrieval's CRN total effect is exactly zero whenever the executing step flips.
The review was right. What follows checks the claim against the COMMITTED SCM
and the COMMITTED estimator, derives the closed form by hand, and reports the
rate with variance across independent seed blocks rather than at one draw.

Three results, in order of how much they cost the paper.

  P1  TE_marg(0) = TE_marg(1) and TE_marg(2) = TE_marg(3) IDENTICALLY, on every
      factual draw. The marginal estimand's failure to separate an inert step
      from a decisive one is an algebraic identity on this chain, not a
      coincidence at the one factual run the paper reported. This STRENGTHENS
      the paper's claim.

  P2  Conditional on u_3 >= q, which has probability 1 - q, TE_crn(1) = 0
      EXACTLY, while DE(1) != 0. The decisive retrieval is then numerically
      indistinguishable from the two inert steps under the very estimand the
      paper proposes as the fix. This WEAKENS the paper's claim and must be
      stated in the abstract, not in section 7.

  P3  P2 requires w = 1 - w. It is a knife-edge at w = 1/2 and the exact-zero
      rate is 0 at every other w tested. So the degeneracy is a worst case, and
      the paper keeps w = 1/2 BECAUSE it is the worst case, not despite it.

Nothing here is repaired. w is not retuned to make the degeneracy go away; that
would be exactly the repair PREREG s4 forbids. It is measured and reported.
"""
import sys, os, json, time, platform, hashlib
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "src"))
import numpy as np
from p2.scm import SyntheticSCM, CRNStream, partial_mediation_scm, Q_FIDELITY, W_DIRECT
from p2.effects import estimate_effects

N_ROLL   = 200          # rollouts per node per factual draw
N_DRAWS  = 60           # factual draws per seed block
N_BLOCKS = 5            # independent seed blocks, for the variance PREREG s5 wants
W_GRID   = (0.2, 0.3, 0.4, 0.5, 0.6, 0.8)
TOL      = 1e-12        # "exactly zero" means exactly zero, not small
ok = True


def _binom_p(k, n, p):
    """Exact two-sided binomial p-value. Written out rather than imported so the
    validator depends on numpy alone, as the pinned environment does."""
    from math import comb
    pmf = [comb(n, i) * p**i * (1-p)**(n-i) for i in range(n+1)]
    return float(min(1.0, sum(x for x in pmf if x <= pmf[k] * (1 + 1e-9))))


def check(label, cond):
    global ok
    ok = ok and bool(cond)
    print(f"  [{'PASS' if cond else 'FAIL'}] {label}")


def build(w, q=Q_FIDELITY):
    """The chain of eq:scm with w free. At w = W_DIRECT this IS the committed SCM;
    that identity is asserted below rather than assumed."""
    def free(prefix, u): return int(u < 0.5)
    def follow(prefix, u): return int(prefix[1]) if u < q else 1 - int(prefix[1])
    return SyntheticSCM(
        name=f"chain4_w{w}", policies=[free, free, free, follow],
        outcome_fn=lambda a, w=w: w * a[1] + (1.0 - w) * a[3],
        kinds=["llm_call", "retrieval", "memory_read", "tool_call"])


def draw(scm, seed, n_roll=N_ROLL):
    crn = CRNStream(seed)
    fact = scm.run(crn, replicate=0)
    attrs = estimate_effects(scm, crn, fact.actions(), fact.outcome,
                             n_rollouts=n_roll, pin_probes=0, seed=seed)
    return crn.uniform(3, 0), fact, attrs


print(__doc__.split("\n\n", 1)[1].rstrip())
print(f"\nq = {Q_FIDELITY}, w = {W_DIRECT}, rollouts/node = {N_ROLL}, "
      f"{N_BLOCKS} blocks x {N_DRAWS} factual draws\n")
t0 = time.time()

# --- the committed SCM and the parameterised one must be the same object ------
print("0. The parameterised chain reproduces the committed SCM at w = W_DIRECT")
ref, par = partial_mediation_scm(), build(W_DIRECT)
same = all(ref.outcome_fn(a) == par.outcome_fn(a)
           for a in [(i, j, k, l) for i in (0, 1) for j in (0, 1)
                     for k in (0, 1) for l in (0, 1)])
check("outcome_fn agrees on all 16 action tuples", same)
check("kinds agree", ref.kinds == par.kinds)

# --- P1. The marginal estimand cannot tell 0 from 1, identically -------------
print("\n1. P1  TE_marg(0) == TE_marg(1) and TE_marg(2) == TE_marg(3), every draw")
print("   Closed form:  TE_marg(0) = TE_marg(1) = 1/2 - y_fact")
print("                 TE_marg(2) = TE_marg(3) = w*a1 + (1-w)(q*a1 + (1-q)(1-a1)) - y_fact")
scm = partial_mediation_scm()
d01 = d23 = 0.0
pred01 = pred23 = 0.0
for s in range(30):
    u3, fact, at = draw(scm, 700_000 + s)
    a1 = fact.actions()[1]; yf = fact.outcome
    m = [a.te_marg.estimate for a in at]
    d01 = max(d01, abs(m[0] - m[1])); d23 = max(d23, abs(m[2] - m[3]))
    q, w = Q_FIDELITY, W_DIRECT
    pred01 = max(pred01, abs(m[0] - (0.5 - yf)))
    pred23 = max(pred23, abs(m[2] - (w*a1 + (1-w)*(q*a1 + (1-q)*(1-a1)) - yf)))
print(f"   max |TE_marg(0) - TE_marg(1)| over 30 draws = {d01:.3e}")
print(f"   max |TE_marg(2) - TE_marg(3)| over 30 draws = {d23:.3e}")
print(f"   max deviation from the closed form, steps 0/1 = {pred01:.3e}")
print(f"   max deviation from the closed form, steps 2/3 = {pred23:.3e}")
check("steps 0 and 1 are marginally identical to within 1e-12", d01 < TOL)
check("steps 2 and 3 are marginally identical to within 1e-12", d23 < TOL)
# The closed form is a finite-sample mean over resampled a'_k, so it is exact only
# in expectation. Tolerance is the Monte Carlo scale, and is stated, not tuned.
# se of a mean of N_ROLL values bounded in [0,1] is at most 0.5/sqrt(N_ROLL).
# The statistic here is a MAX over 60 such means, so the band is 4 se, fixed
# before the run and not adjusted to the observed 8.75e-2.
mc = 4.0 * 0.5 / np.sqrt(N_ROLL)
check(f"closed form matches within 4 standard errors ({mc:.3f})",
      pred01 < mc and pred23 < mc)

# --- P2. The CRN estimand returns an exact zero for a step that acts ----------
print("\n2. P2  TE_crn(1) = 0 exactly when u_3 >= q, though DE(1) != 0 there")
rates, de_on_zero = [], []
zero_when_flip, zero_when_no_flip = True, False
for b in range(N_BLOCKS):
    base = 800_000 + b * 10_000
    z = n = 0
    for i in range(N_DRAWS):
        u3, fact, at = draw(scm, base + i)
        te1, de1 = at[1].te_crn.estimate, at[1].de.estimate
        flip = u3 >= Q_FIDELITY
        if flip:
            if abs(te1) >= TOL:
                print(f"   COUNTEREXAMPLE seed {base+i}: u3={u3:.4f} TE_crn(1)={te1:+.3e}")
                zero_when_flip = False
            de_on_zero.append(abs(de1))
            z += 1
        elif abs(te1) < TOL:
            print(f"   UNEXPECTED zero at seed {base+i}, u3={u3:.4f} < q")
            zero_when_no_flip = True
        n += 1
    rates.append(z / n)
r = np.array(rates)
# The estimator pass above visits 300 seeds, which is too few to pin a rate of
# 0.1. The rate itself needs no estimator: it is P(u_3 >= q) under the factual
# noise, so it is measured directly on a large seed set. Both numbers are
# reported. Disagreement between them is a property of the small seed set, and
# is quantified rather than removed by reseeding.
big = np.array([CRNStream(s_).uniform(3, 0) for s_ in range(20_000)])
print(f"   direct rate P(u_3 >= q) over 20000 seeds = {float(np.mean(big >= Q_FIDELITY)):.4f}"
      f"   [nominal {1-Q_FIDELITY:.2f}]")
check("the direct rate is within 0.005 of 1 - q",
      abs(float(np.mean(big >= Q_FIDELITY)) - (1 - Q_FIDELITY)) < 0.005)
print(f"   exact-zero rate per block: {[f'{x:.3f}' for x in rates]}")
print(f"   mean {r.mean():.3f}, sd {r.std(ddof=1):.3f}, nominal 1 - q = {1-Q_FIDELITY:.2f}")
print(f"   on those draws, mean |DE(1)| = {np.mean(de_on_zero):.4f} "
      f"(sd {np.std(de_on_zero, ddof=1):.4f}), so the step demonstrably acts")
check("every u_3 >= q draw gave TE_crn(1) exactly zero", zero_when_flip)
check("no u_3 < q draw gave a zero", not zero_when_no_flip)
nflip = int(round(r.mean() * N_BLOCKS * N_DRAWS))
print(f"   over the {N_BLOCKS*N_DRAWS} estimator seeds: {nflip} flips, "
      f"binomial two-sided p against 1 - q = "
      f"{_binom_p(nflip, N_BLOCKS*N_DRAWS, 1-Q_FIDELITY):.3f}")
check("the estimator seed set is not significantly off 1 - q at the 1% level",
      _binom_p(nflip, N_BLOCKS*N_DRAWS, 1-Q_FIDELITY) > 0.01)
check("DE(1) is nonzero on every such draw", min(de_on_zero) > 1e-6)

# --- P3. The degeneracy is a knife-edge at w = 1/2 ---------------------------
print("\n3. P3  The cancellation needs w = 1 - w. Zero-rate against w")
print(f"   {'w':>6} {'P(TE_crn(1)==0)':>17} {'mean TE_crn(1)':>15} {'sd':>8}")
zr = {}
for w in W_GRID:
    m = build(w); v = []
    for i in range(N_DRAWS):
        _, fact, at = draw(m, 900_000 + i, n_roll=N_ROLL)
        v.append(at[1].te_crn.estimate)
    v = np.array(v); zr[w] = float(np.mean(np.abs(v) < TOL))
    print(f"   {w:>6.1f} {zr[w]:>17.3f} {v.mean():>+15.4f} {v.std(ddof=1):>8.4f}")
check("zero-rate is nonzero at w = 1/2", zr[0.5] > 0)
check("zero-rate is exactly 0 at every other w tested",
      all(zr[w] == 0.0 for w in W_GRID if w != 0.5))

# --- P4. Pin plausibility as currently reported is uninformative -------------
print("\n4. P4  The pooled pin-plausibility number is 1/2 for every q, by construction")
print("   Averaged over a'_1 ~ Bern(1/2): q if the intervention did not change the")
print("   action, 1-q if it did, mean (q + (1-q))/2 = 1/2 regardless of q.")
print(f"   {'q':>6} {'pooled':>8} {'unchanged arm':>14} {'changed arm':>12}")
for q in (0.6, 0.75, 0.9, 0.99):
    m = build(W_DIRECT, q=q)
    crn = CRNStream(950_000); fact = m.run(crn, replicate=0)
    a1f, a3f = fact.actions()[1], fact.actions()[3]
    hits = {0: [], 1: []}
    for r in range(1, 601):
        alt = m.sample_action(1, (fact.actions()[0],), crn, replicate=r)
        cf = m.run(crn, replicate=0, forced={1: alt}).actions()
        h = sum(m.sample_action(3, tuple(cf[:3]), crn, replicate=10_000 + r*131 + mm) == a3f
                for mm in range(32)) / 32.0
        hits[int(alt != a1f)].append(h)
    pooled = np.mean(hits[0] + hits[1])
    print(f"   {q:>6.2f} {pooled:>8.3f} {np.mean(hits[0]):>14.3f} {np.mean(hits[1]):>12.3f}")
    check(f"pooled is 1/2 to within Monte Carlo error at q={q}", abs(pooled - 0.5) < 0.05)
    check(f"the two arms separate at q={q}", abs(np.mean(hits[0]) - np.mean(hits[1])) > 0.1)

print(f"\nelapsed {time.time()-t0:.1f}s   python {platform.python_version()}   "
      f"numpy {np.__version__}")
print("\nRESULT:", "ALL CHECKS PASS" if ok else "FAILURES ABOVE")
sys.exit(0 if ok else 1)
