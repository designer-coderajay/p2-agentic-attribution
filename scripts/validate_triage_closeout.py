"""WS1.12. The four objections the red team raised that were not settled in
WS1.11, each checked against the committed code rather than argued about.

Two are upheld and change the paper. Two are refuted, and the refutation is
computed here so that the next reviewer does not have to take our word for it.

  A  UPHELD in part. CAR's point-of-commitment rule IS implemented and IS
     exercised (scripts/validate_estimators.py prints it), so "never
     implemented" is wrong. But it is printed, never compared. Contribution 1
     claims a separation from that instrument and nothing measured the
     separation. Measured here: the rule's locus and our largest-CRN-effect
     step disagree, in a specific and repeatable direction.

  B  UPHELD, and worse than the objection said. Figure 2's numbers are quoted
     at vocabulary 32 and one source entropy. Held at matched TV = 0.18,
     quantile agreement ranges 0.0044 to 0.6307 across vocabulary size and
     source entropy, a factor of 142, and probability-sorted agreement ranges
     0.0000 to 0.7742. Maximal coupling does not move at all, because it is
     1 - TV by construction, which makes the case for it far stronger at a real
     vocabulary than at 32.

     A SECOND finding, which the objection did not raise and which the paper
     currently states backwards: probability sorting is NOT uniformly worse
     than a fixed index order. In 1 of 12 cells it is better, by 0.774 against
     0.631, and the reversal survives a Monte Carlo run through the sampler.
     The defect in sorting is that the order becomes a function of the branch's
     own distribution, not that it is always worse. The design requirement has
     to be restated.

  C  REFUTED, with a caveat that is worth more than the objection. "g =
     beta/||beta|| is guaranteed near +/-1 exactly when H1 is true." H1 drives
     g_causal toward 0, which says nothing about whether any other component
     reaches 1; with two live covariates the largest |g_j| is 0.707. The pole
     needs ONE component to dominate, which is a different condition.

     The committed dry-run fit does sit at the pole, |g| = 0.9957, but because
     verbosity dominates recency 0.78 to 0.067, not because H1 holds. And there
     the delta-method 95% interval runs to 1.0154, outside the parameter space
     of a unit-vector component. That is the reason PREREG locks the bootstrap,
     demonstrated from results/dry_run.json rather than asserted.

  D  UPHELD, and it generalises WS1.11. A do_resample intervention on a
     DETERMINISTIC step draws the factual action every time, so its estimated
     effect is exactly zero however decisive it is. At q = 1 the executing step
     is deterministic given the retrieval and reports zero effect, zero change
     rate, and is indistinguishable from an inert step.

Nothing is repaired. Where a number does not generalise it is reported as not
generalising.
"""
import os
import platform
import sys
import time
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "src"))
import numpy as np
from p2.scm import CRNStream, SyntheticSCM, W_DIRECT, partial_mediation_scm
from p2.effects import (estimate_effects, point_of_commitment, largest_effect_step)
from p2.coupling import total_variation, overlap, quantile_agreement
from p2.ranking import normalized_beta

TOL = 1e-12
ok = True


def check(label, cond):
    global ok
    ok = ok and bool(cond)
    print(f"  [{'PASS' if cond else 'FAIL'}] {label}")


def softmax(z):
    z = z - z.max()
    e = np.exp(z)
    return e / e.sum()


print(__doc__.split("\n\n", 1)[1].rstrip())
print()
t0 = time.time()

# =============================================================================
# A. CAR's locus rule against our estimand, on the chain whose answer we know.
# =============================================================================
print("A. The comparison contribution 1 claims, actually run")
print("   Planted truth: step 1 is the decisive retrieval, step 3 executes what")
print("   step 1 decided, steps 0 and 2 have no path to the outcome.")
print("   CAR's rule (reproduced verbatim in effects.point_of_commitment) returns")
print("   the LATEST step whose total-effect interval still excludes zero.\n")

scm = partial_mediation_scm()
N_A, ROLL_A = 60, 300
car_locus, crn_top = [], []
for i in range(N_A):
    crn = CRNStream(300_000 + i)
    fact = scm.run(crn, replicate=0)
    at = estimate_effects(scm, crn, fact.actions(), fact.outcome,
                          n_rollouts=ROLL_A, pin_probes=0, seed=300_000 + i)
    car_locus.append(point_of_commitment(at, "te_marg"))
    crn_top.append(largest_effect_step(at, "te_crn"))


def tally(xs):
    return {v: xs.count(v) for v in sorted(set(xs), key=lambda z: (z is None, z))}


print(f"   over {N_A} factual draws, {ROLL_A} rollouts per node")
print(f"   CAR locus on TE_marg           : {tally(car_locus)}")
print(f"   largest |TE_crn| step          : {tally(crn_top)}")
disagree = sum(a != b for a, b in zip(car_locus, crn_top, strict=True))
print(f"   disagreement rate              : {disagree}/{N_A} = {disagree/N_A:.3f}")
car3 = car_locus.count(3)
crn1 = crn_top.count(1)
print(f"   CAR names the EXECUTING step 3 : {car3}/{N_A} = {car3/N_A:.3f}")
print(f"   ours names the RETRIEVAL step 1: {crn1}/{N_A} = {crn1/N_A:.3f}")
print()
print("   READ THIS CAREFULLY. CAR is not wrong. Its rule asks where the outcome")
print("   became committed, and on this chain that is the executing step. Ours")
print("   asks which step's own action carried the effect, and that is the")
print("   retrieval. The paper must report a DISAGREEMENT WITH A DIRECTION, not")
print("   a failure of the incumbent, and contribution 1 must say which question")
print("   each estimand answers.")
check("the two rules disagree on a majority of draws", disagree / N_A > 0.5)
check("CAR's locus is the executing step on a majority of draws", car3 / N_A > 0.5)
check("ours is the retrieval on a majority of draws", crn1 / N_A > 0.5)

# =============================================================================
# B. Does Figure 2's magnitude travel across vocabulary and source entropy?
# =============================================================================
print("\nB. Coupling agreement at MATCHED total variation, across V and entropy")
print("   Construction is the committed one in scripts/validate_coupling.py:")
print("   p = softmax(N(0, s)), q = softmax(base + N(0, shift)), shift bisected")
print("   to hit the target TV. All three agreements are CLOSED FORM, so V = 1e5")
print("   costs nothing and no Monte Carlo error enters the comparison.\n")


def sorted_agreement(p, q):
    """Agreement when each branch walks its OWN probability-sorted CDF.

    Closed form. Token t occupies [lo, hi) in each branch's own interval
    partition; the branches emit the same token when u lands in both of t's
    intervals, so agreement is the total intersection length over tokens. With
    identity orderings this reduces to quantile_agreement, which is asserted.
    """
    op, oq = np.argsort(-p, kind="stable"), np.argsort(-q, kind="stable")
    return _agreement_under(p, q, op, oq)


def _agreement_under(p, q, op, oq):
    n = len(p)
    Pc = np.concatenate([[0.0], np.cumsum(p[op])])
    Qc = np.concatenate([[0.0], np.cumsum(q[oq])])
    lo_p = np.empty(n); hi_p = np.empty(n); lo_q = np.empty(n); hi_q = np.empty(n)
    lo_p[op] = Pc[:-1]; hi_p[op] = Pc[1:]
    lo_q[oq] = Qc[:-1]; hi_q[oq] = Qc[1:]
    return float(np.maximum(0.0, np.minimum(hi_p, hi_q) - np.maximum(lo_p, lo_q)).sum())


# self-check: identity ordering must reproduce the committed closed form
_r = np.random.default_rng(7)
_p, _q = softmax(_r.normal(0, 1.5, 64)), softmax(_r.normal(0, 1.5, 64))
_ident = np.arange(64)
check("the general form reproduces quantile_agreement under identity ordering",
      abs(_agreement_under(_p, _q, _ident, _ident) - quantile_agreement(_p, _q)) < 1e-12)


def pair_at_tv(V, s, target_tv, seed):
    """Bisect the perturbation scale until TV(p, q) hits the target."""
    rng = np.random.default_rng(seed)
    base = rng.normal(0, s, V)
    p = softmax(base)
    noise = rng.normal(0, 1.0, V)
    lo, hi = 0.0, 40.0
    for _ in range(80):
        mid = 0.5 * (lo + hi)
        q = softmax(base + mid * noise)
        if total_variation(p, q) < target_tv:
            lo = mid
        else:
            hi = mid
    q = softmax(base + 0.5 * (lo + hi) * noise)
    return p, q


TARGET_TV = 0.18
print(f"   {'V':>7} {'entropy s':>10} {'TV':>7} {'maximal':>8} {'quantile':>9} {'p-sorted':>9}")
grid = []
for V in (32, 1_000, 32_000, 100_000):
    for s in (0.5, 1.5, 3.0):
        p, q = pair_at_tv(V, s, TARGET_TV, seed=1000 * len(grid) + 11)
        tv = total_variation(p, q)
        mx, qt, sr = overlap(p, q), quantile_agreement(p, q), sorted_agreement(p, q)
        grid.append((V, s, tv, mx, qt, sr))
        print(f"   {V:>7} {s:>10.1f} {tv:>7.4f} {mx:>8.4f} {qt:>9.4f} {sr:>9.4f}")

qts = np.array([g[4] for g in grid]); srs = np.array([g[5] for g in grid])
mxs = np.array([g[3] for g in grid])
print()
print(f"   maximal agreement spread   : {mxs.min():.4f} to {mxs.max():.4f}"
      f"   (it is 1 - TV by construction, so it does not move)")
print(f"   quantile agreement spread  : {qts.min():.4f} to {qts.max():.4f}"
      f"   ratio {qts.max()/max(qts.min(),1e-12):.1f}x")
print(f"   p-sorted agreement spread  : {srs.min():.4f} to {srs.max():.4f}"
      f"   ratio {srs.max()/max(srs.min(),1e-12):.1f}x")
print()
print("   UPHELD. At one fixed TV the two order-dependent agreements move by")
print("   more than an order of magnitude with vocabulary size and source")
print("   entropy. Quoting 0.412 and 0.086 without saying 'at V = 32, at this")
print("   entropy' invites a reader to carry them to a real vocabulary, where")
print("   they do not hold.")
check("maximal coupling is invariant at matched TV, as theory says",
      float(mxs.max() - mxs.min()) < 1e-9)
check("quantile agreement moves by more than 2x across the grid",
      qts.max() / max(qts.min(), 1e-12) > 2.0)
check("maximal dominates both order-dependent couplings in every cell",
      all(g[3] >= g[4] - 1e-12 and g[3] >= g[5] - 1e-12 for g in grid))

# The paper currently treats probability sorting as strictly worse than a fixed
# index order. The grid says otherwise, so that is checked rather than assumed.
sorted_worse = [g for g in grid if g[5] < g[4] - 1e-12]
sorted_better = [g for g in grid if g[5] > g[4] + 1e-12]
print()
print(f"   cells where p-sorted is WORSE than fixed order : {len(sorted_worse)}/{len(grid)}")
print(f"   cells where p-sorted is BETTER                 : {len(sorted_better)}/{len(grid)}")
for g in sorted_better:
    print(f"     V={g[0]}, s={g[1]}: sorted {g[5]:.4f} > fixed {g[4]:.4f}")
print()
print("   NEW, AND THE PAPER SAYS THE OPPOSITE. Sorting the vocabulary by")
print("   probability is not uniformly worse than a fixed index order. When both")
print("   branches are peaked they largely agree on WHICH tokens are large, the")
print("   two sorted orders nearly coincide, and sorting aligns the big intervals")
print("   and RAISES agreement. When they are flat the orders diverge and sorting")
print("   destroys it. The defect in sorting is therefore not that it is worse;")
print("   it is that the order becomes a function of the branch's OWN")
print("   distribution, so its cost is set by the divergence rather than by the")
print("   implementer. The requirement that survives is: the order must be shared")
print("   and branch-independent, or else use maximal coupling, which needs no")
print("   order at all.")
check("probability sorting is worse in some cells and better in others, so the "
      "paper's blanket claim is false", len(sorted_worse) > 0 and len(sorted_better) > 0)

# The magnitudes do not even survive a change of PERTURBATION MODEL at the same
# vocabulary and the same TV. The committed validator forms q by adding Gaussian
# logit noise of a stated scale; this script bisects a scale on a fixed noise
# vector to hit a target TV. Both are defensible. They disagree by a large
# factor on exactly the numbers Figure 2 quotes.
SEED_C, VOC_C = 20260813, 32
rngc = np.random.default_rng(SEED_C)
base_c = rngc.normal(0, 1.5, VOC_C)
p_c = softmax(base_c)
for _sh in (0.0, 0.25):                      # consume the same draws in order
    rngc.normal(0, _sh, VOC_C) if _sh else rngc.normal(0, 1e-300, VOC_C)
q_c = softmax(base_c + rngc.normal(0, 0.5, VOC_C))
tv_c, qt_c, sr_c = total_variation(p_c, q_c), quantile_agreement(p_c, q_c), sorted_agreement(p_c, q_c)
mine = [g for g in grid if g[0] == 32 and g[1] == 1.5][0]
print()
print("   Same V = 32, near-identical TV, two perturbation models:")
print(f"     committed validator construction : TV {tv_c:.4f}  quantile {qt_c:.4f}  p-sorted {sr_c:.4f}")
print(f"     this script's construction       : TV {mine[2]:.4f}  quantile {mine[4]:.4f}  p-sorted {mine[5]:.4f}")
if sr_c > 1e-9:
    print(f"     p-sorted differs by a factor of {max(sr_c, mine[5])/min(sr_c, mine[5]):.1f}"
          " at the same vocabulary and the same divergence")
check("the two constructions agree on TV to within 0.01", abs(tv_c - mine[2]) < 0.01)
check("and still disagree on p-sorted agreement by more than 2x",
      max(sr_c, mine[5]) / max(min(sr_c, mine[5]), 1e-12) > 2.0)

# Monte Carlo cross-check of the surprising cell, using the sampler path rather
# than the closed form, so the reversal cannot be an artifact of the algebra.
from p2.coupling import keyed_uniform, inverse_transform
gb = sorted_better[0]
pc, qc = pair_at_tv(gb[0], gb[1], TARGET_TV, seed=1000 * grid.index(gb) + 11)
ip, iq = np.argsort(-pc), np.argsort(-qc)
ps, qs = pc[ip], qc[iq]
NMC = 40000
agree_sorted = sum(ip[inverse_transform(ps, keyed_uniform("x", 0, r))] ==
                   iq[inverse_transform(qs, keyed_uniform("x", 0, r))] for r in range(NMC))
agree_fixed = sum(inverse_transform(pc, keyed_uniform("x", 0, r)) ==
                  inverse_transform(qc, keyed_uniform("x", 0, r)) for r in range(NMC))
es, ef = agree_sorted / NMC, agree_fixed / NMC
se = np.sqrt(0.25 / NMC)
print(f"\n   Monte Carlo at V={gb[0]}, s={gb[1]}, {NMC} draws through the sampler:")
print(f"     p-sorted   empirical {es:.4f}  closed form {gb[5]:.4f}  "
      f"({abs(es-gb[5])/se:.1f} sigma)")
print(f"     fixed order empirical {ef:.4f}  closed form {gb[4]:.4f}  "
      f"({abs(ef-gb[4])/se:.1f} sigma)")
check("the reversal survives a Monte Carlo run through the actual sampler",
      es > ef)
check("both empirical rates match their closed forms within 4 sigma",
      abs(es - gb[5]) / se < 4 and abs(ef - gb[4]) / se < 4)

# =============================================================================
# C. Is g = beta/||beta|| forced to +/-1 by H1?
# =============================================================================
print("\nC. The claim that H1 forces the normalised direction to a pole")
print("   Covariates are (causal rank, recency, verbosity), so K = 3.")
print("   H1 says the causal coefficient is small. H2 says recency and verbosity")
print("   are jointly nonzero AFTER conditioning on it. Neither says one of them")
print("   dominates the other, and only that would drive |g| to 1.\n")
V3 = np.eye(3) * 0.01
print(f"   {'beta':>28} {'|g|_max':>9}  regime")
cases = [
    (np.array([0.00, 0.70, 0.70]), "H1 and H2 both hold, the two compete"),
    (np.array([0.00, 0.90, 0.30]), "H1 and H2 hold, recency leads"),
    (np.array([0.00, 1.00, 0.00]), "one covariate alone: THIS is the pole"),
    (np.array([0.80, 0.10, 0.10]), "H1 FAILS, causal dominates"),
]
gmax = []
for b, label in cases:
    g, se, note = normalized_beta(b, V3)
    gmax.append(float(np.abs(g).max()))
    print(f"   {np.array2string(b, precision=2):>28} {np.abs(g).max():>9.3f}  {label}")
print()
print("   REFUTED as stated. Under H1 with two live covariates the largest")
print(f"   |g_j| is {gmax[0]:.3f}, not 1. The pole is reached only when a single")
print("   covariate carries the whole vector, which is neither H1 nor H2.")
check("H1 with two competing covariates does not reach the pole", gmax[0] < 0.75)
check("the single-covariate case does reach the pole", gmax[2] > 0.999)

# The committed fit, READ FROM THE ARTIFACT rather than typed from memory. An
# earlier version of this script typed an approximation of it and labelled the
# approximation "the actual dry-run fit". It was not: the second component was
# invented. The rule that a number enters a paper only from its source applies
# to the scripts that check the paper too.
print("\n   The actual fit, read from results/dry_run.json:")
import json, os
_dr = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "results", "dry_run.json")
D = json.load(open(_dr))["h2"]
beta_obs = np.array(D["beta"], float)
g_obs, se_obs, _ = normalized_beta(beta_obs, np.diag(np.array(D["se"], float) ** 2))
j = int(np.argmax(np.abs(g_obs)))
print(f"     beta        = {np.array2string(beta_obs, precision=4)}")
print(f"     g recomputed= {np.array2string(g_obs, precision=4)}")
print(f"     g as stored = {np.array2string(np.array(D['g_normalized']), precision=4)}")
check("normalized_beta reproduces the stored g to 1e-12",
      float(np.abs(g_obs - np.array(D["g_normalized"])).max()) < 1e-12)

print(f"\n   That fit IS at the pole, |g| = {abs(g_obs[j]):.4f}, and the reason matters.")
print("   beta_causal is -0.0292, so H1 holds. But recency is 0.0667 against")
print("   verbosity 0.7804: ONE covariate carries the vector. It is that, not H1,")
print("   that puts the fit at the pole, which is exactly what the refutation says.")

# And at the pole the delta method returns an interval that cannot be true.
z = 1.959963985
d_lo = D["g_normalized"][j] - z * D["g_delta_se"][j]
d_hi = D["g_normalized"][j] + z * D["g_delta_se"][j]
b_lo, b_hi = D["g_bootstrap_lo"][j], D["g_bootstrap_hi"][j]
print(f"\n   delta-method 95% CI on g_{j}: [{d_lo:.4f}, {d_hi:.4f}]")
print(f"   bootstrap    95% CI on g_{j}: [{b_lo:.4f}, {b_hi:.4f}]")
print("   g is a component of a UNIT vector, so it cannot exceed 1. The delta")
print("   method's upper limit does. That is not a small under-coverage, it is an")
print("   interval outside the parameter space, and it is why PREREG locks the")
print("   bootstrap. Read from the committed artifact, not asserted.")
check("the delta-method interval leaves the parameter space at the pole", d_hi > 1.0)
check("the bootstrap interval stays inside it", b_hi <= 1.0 and b_lo >= -1.0)
check("the bootstrap interval is the wider of the two",
      (b_hi - b_lo) > (d_hi - d_lo))

# =============================================================================
# D. A deterministic step cannot be attributed to by resampling.
# =============================================================================
print("\nD. What do_resample does to a step with no randomness left")
print("   At fidelity q the executing step follows the retrieval with")
print("   probability q. At q = 1 it is a deterministic function of it.\n")


def chain_at_q(q):
    def free(prefix, u): return int(u < 0.5)
    def follow(prefix, u): return int(prefix[1]) if u < q else 1 - int(prefix[1])
    return SyntheticSCM(name=f"q{q}", policies=[free, free, free, follow],
                        outcome_fn=lambda a: W_DIRECT * a[1] + (1.0 - W_DIRECT) * a[3],
                        kinds=["llm_call", "retrieval", "memory_read", "tool_call"])


print(f"   {'q':>6} {'step':>5} {'change rate':>12} {'TE_marg':>9} {'TE_crn':>9} {'DE':>9}")
det_zero = None
for q in (0.9, 0.99, 1.0):
    m = chain_at_q(q)
    crn = CRNStream(400_000)
    fact = m.run(crn, replicate=0)
    at = estimate_effects(m, crn, fact.actions(), fact.outcome,
                          n_rollouts=400, pin_probes=0, seed=400_000)
    for k in (1, 3):
        a = at[k]
        print(f"   {q:>6.2f} {k:>5} {a.change_rate:>12.4f} {a.te_marg.estimate:>+9.4f} "
              f"{a.te_crn.estimate:>+9.4f} {a.de.estimate:>+9.4f}")
        if q == 1.0 and k == 3:
            det_zero = (a.change_rate, a.te_marg.estimate, a.te_crn.estimate, a.de.estimate)
print()
print("   UPHELD, and it is the same failure as Proposition 2 seen from the other")
print("   side. A do_resample intervention redraws from the UNCHANGED policy. If")
print("   the policy is a point mass, the redraw is the factual action every time,")
print("   the change rate is 0, and every effect is exactly 0 no matter how")
print("   decisive the step is. Attribution by resampling is defined only where")
print("   the policy still has entropy left at that step, and the change rate is")
print("   the quantity that says whether it does. The paper reports change rate")
print("   already; it does not say that a zero there voids the effect estimate.")
check("at q = 1 the executing step has change rate exactly 0", det_zero[0] == 0.0)
check("at q = 1 every effect at that step is exactly 0",
      all(abs(v) < TOL for v in det_zero[1:]))

print(f"\nelapsed {time.time()-t0:.1f}s   python {platform.python_version()}   "
      f"numpy {np.__version__}")
print("\nRESULT:", "ALL CHECKS PASS" if ok else "FAILURES ABOVE")
sys.exit(0 if ok else 1)
