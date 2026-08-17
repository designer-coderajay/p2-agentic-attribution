# Analytic ground truth for the synthetic SCMs

Derived by hand before the estimators were run. The validation script checks the
estimators against these numbers, not against each other. Any disagreement outside
Monte Carlo error is an estimator bug, and the derivation is the referee.

## 1. The SCM

`partial_mediation`, four steps, parameters `q = 0.9` (fidelity of the executing
step to the retrieval) and `w = 0.5` (weight of the retrieval's own direct path):

```
a0 ~ Bern(1/2)                         inert, no path to y
a1 ~ Bern(1/2)                         retrieval, pulls the risk flag
a2 ~ Bern(1/2)                         inert, no path to y
a3 = a1        if u3 < q               executing tool call
   = 1 - a1    otherwise
y  = w*a1 + (1-w)*a3
```

Realised factual run under seed 20260813, replicate 0:

```
a_fact = (0, 1, 1, 1),  u3_fact = 0.7703699...,  y_fact = 1
```

Since `u3_fact < q`, the factual executing step followed the retrieval. All effects
below are conditional on this factual run, as they must be: an effect is a
contrast against something that happened.

## 2. Two total effects, not one

The distinction is the technical crux and it is not cosmetic.

**Marginal total effect (run-forward, as in arXiv 2606.08275).** Intervene at `k`,
then let every downstream step re-decide under *fresh* randomness:

    TE_marg(k) = E_{a'_k, u_{>k}} [ Y | do(a_k := a'_k) ] - y_fact

**CRN total effect (this work).** Intervene at `k`, then let every downstream step
re-decide under the *factual* randomness `u_{>k} = u_fact`:

    TE_crn(k) = E_{a'_k} [ Y | do(a_k := a'_k), U_{>k} = u_fact ] - y_fact

The second is a counterfactual in Pearl's sense: same unit, same exogenous noise,
one variable changed. The first marginalises the noise away and therefore also
re-rolls every downstream decision, which is the confound CAR identifies in
section 4 and resolves with its point-of-commitment rule. We resolve it by
construction. The derivations below show why that matters.

## 3. CRN arm

Under CRN, `u3` is held at `u3_fact = 0.770 < q`, so `a3 = a1` deterministically
along every counterfactual branch. Write `a'_1 ~ Bern(1/2)`.

**Step 0 (inert).** No path to `y`; steps 1, 2, 3 replay at factual noise.

    y = y_fact  for every draw    =>    TE_crn(0) = 0    exactly.

**Step 1 (retrieval).** `a3 = a'_1`, so `y = w a'_1 + (1-w) a'_1 = a'_1`.

    E[y] = 1/2                    =>    TE_crn(1) = 1/2 - 1 = -0.5

**Step 2 (inert).** As step 0.                TE_crn(2) = 0    exactly.

**Step 3 (executing).** Prefix holds `a1 = 1`; the redraw gives `a'_3 = 1` with
probability `q`. So `y = w + (1-w) a'_3`.

    E[y] = 0.5 + 0.5 q = 0.95     =>    TE_crn(3) = -0.05

## 4. Direct effect

Intervene at `k`, pin every `j > k` to its factual action. This is Pearl's natural
direct effect: mediators held at the values they took under the factual run
(Pearl, *Causality*, CUP 2nd ed. 2009).

**Step 0.** Pins `a1 = 1, a2 = 1, a3 = 1`, so `y = 1`.        DE(0) = 0
**Step 1.** Pins `a3 = 1`, so `y = w a'_1 + (1-w)`.
            `E[y] = 0.5(0.5) + 0.5 = 0.75`.                   DE(1) = -0.25
**Step 2.** Pins `a3 = 1`, so `y = 1`.                        DE(2) = 0
**Step 3.** Nothing downstream to pin.                        DE(3) = TE_crn(3) = -0.05

## 5. Mediated effect, ME = TE_crn - DE

    ME(0) = 0        ME(1) = -0.25        ME(2) = 0        ME(3) = 0

Mediated share of step 1: `|ME| / |TE_crn| = 0.25 / 0.5 = 0.5`, which equals
`1 - w` as it must, since the mediated path carries exactly weight `1 - w`. That
identity is the closed-form check on the whole decomposition.

## 6. Marginal arm, and the confound

Downstream noise is refreshed, so the redrawn `a3` is `a'_1`-following only with
probability `q`, and marginally `P(a3 = 1) = q/2 + (1-q)/2 = 1/2`.

**Step 0 (inert).** Forcing `a0` re-rolls steps 1, 2 and 3.

    E[y] = w E[a1] + (1-w) E[a3] = 0.25 + 0.25 = 0.5
    TE_marg(0) = -0.5

**Step 1.**  `E[y] = 0.5` likewise.                            TE_marg(1) = -0.5
**Step 2 (inert).** Re-rolls step 3 only; prefix keeps `a1 = 1`, so `E[a3] = q`.

    E[y] = 0.5 + 0.5(0.9) = 0.95                               TE_marg(2) = -0.05

**Step 3.** No downstream steps, so identical to CRN.          TE_marg(3) = -0.05

## 7. The result this establishes

| step | truth | TE_marg | TE_crn | DE | ME |
|---|---|---|---|---|---|
| 0 | inert, no path to y | **-0.50** | **0** | 0 | 0 |
| 1 | decisive retrieval | -0.50 | -0.50 | -0.25 | -0.25 |
| 2 | inert, no path to y | **-0.05** | **0** | 0 | 0 |
| 3 | executing step | -0.05 | -0.05 | -0.05 | 0 |

Under marginal run-forward the causally inert step 0 is **numerically
indistinguishable** from the decisive step 1, and the inert step 2 is
indistinguishable from the executing step 3. Magnitude cannot separate them, which
is precisely what CAR states and why it needs a locus rule. Under CRN both inert
steps are exactly zero and the planted structure is recovered without a heuristic.

This is a statement about estimators on a known structure. It is not yet a
statement about any real system, and must not be written as one.

## 8. Pin plausibility

The DE arm at step 1 pins `a3 = 1` while `a1` has been resampled. When `a'_1 = 1`
the pin agrees with the policy with probability `q = 0.9`; when `a'_1 = 0` it agrees
with probability `1 - q = 0.1`. Averaging over `a'_1 ~ Bern(1/2)`:

    E[pin plausibility at step 3 under DE(1)] = (0.9 + 0.1)/2 = 0.5

Reported, not assumed away. Where this number is small the DE estimate rests on a
pin the policy would rarely have produced, and ME must be read as bounded rather
than as a point estimate.

---

# Part II: coupling across divergent contexts

Added 16 August 2026 (D4). Validated in `scripts/validate_coupling.py`,
`env_hash 6e1224b9f63551b9`.

## 9. The estimand problem restated

`DE` requires re-running a step under a changed upstream while holding the noise
fixed. arXiv 2606.08275 section 7 states this needs common random numbers across
branches, calls it hard across divergent LLM contexts, and leaves it as a
refinement. The question is what "hard" means precisely, and the answer is a
closed form rather than a vibe.

Token sampling is inverse-transform sampling from a categorical distribution. If
the uniform draw `u` is a pure function of `(run id, step, replicate)` and never
of the context, then factual and counterfactual branches consume identical draws.
The noise is shared exactly. What is not shared exactly is the *benefit*.

## 10. A false claim, and its correction

The first draft of `src/p2/coupling.py` asserted that shared-`u`
inverse-transform sampling in fixed index order attains the maximal-coupling
bound `1 - TV(p, q)`. **This is false.** The validation script rejected it at up
to 215 Monte Carlo sigma before any of it reached a manuscript.

The correct closed form for shared-`u` inverse-transform (quantile) coupling: two
branches agree at token `i` exactly when `u` lands in the intersection of the CDF
intervals `[P_{i-1}, P_i)` and `[Q_{i-1}, Q_i)`. Summing the intersections,

    A_quant(p, q) = sum_i max(0, min(P_i, Q_i) - max(P_{i-1}, Q_{i-1}))

with `P`, `Q` the CDFs in fixed index order. Since the intersection of two
intervals is no longer than the shorter, `A_quant <= sum_i min(p_i, q_i) = 1 - TV`,
with equality only in degenerate cases.

The mechanism behind the loss: probability mass moved between two tokens shifts
*every subsequent CDF boundary*. A perturbation early in the index order
decouples the entire tail, so `A_quant` can fall far below `1 - TV` at small
`TV`. The measured table shows exactly this: at `TV = 0.179` the maximal bound is
`0.821` but quantile coupling delivers `0.412`.

## 11. Maximal coupling, and what it costs

Maximal coupling attains `1 - TV(p, q)`, which is optimal: no coupling of `p` and
`q` agrees more often. Construction: with probability `omega = sum_i min(p_i, q_i)`
both branches emit the same token drawn from `min(p, q) / omega`; otherwise each
draws from its own residual `(p - min) / (1 - omega)` and `(q - min) / (1 - omega)`.

It requires `p` and `q` at draw time, so the factual branch's distribution must be
carried alongside the counterfactual one. That is one extra forward pass per step,
and it is available to us because the factual run is being replayed anyway.

## 12. Measured, against closed form

Vocabulary 32, 40,000 draws per point, `q` formed by perturbing the logits of `p`
with Gaussian noise of the stated scale. Every empirical value is within 1.9 MC
sigma of its closed form.

| logit shift | TV(p,q) | quantile bound | quantile emp. | maximal bound | maximal emp. | gain | prob-sorted |
|---|---|---|---|---|---|---|---|
| 0.00 | 0.0000 | 1.0000 | 1.0000 | 1.0000 | 1.0000 | 0.000 | 1.0000 |
| 0.25 | 0.0856 | 0.7851 | 0.7839 | 0.9144 | 0.9142 | 0.129 | 0.5298 |
| 0.50 | 0.1788 | 0.4121 | 0.4087 | 0.8212 | 0.8221 | 0.409 | 0.0858 |
| 1.00 | 0.3969 | 0.2777 | 0.2740 | 0.6031 | 0.6075 | 0.325 | 0.0447 |
| 2.00 | 0.4245 | 0.3057 | 0.3054 | 0.5755 | 0.5801 | 0.270 | 0.0446* |
| 4.00 | 0.9369 | 0.0167 | 0.0177 | 0.0631 | 0.0654 | 0.046 | 0.0252 |

`gain` is `maximal - quantile`: the coupling bought by the second forward pass.
`prob-sorted` is what a naive top-k or nucleus sampler delivers, because sorting
the vocabulary by probability breaks the fixed index order that quantile coupling
depends on. At `TV = 0.179` it collapses to `0.086` against an achievable `0.821`,
a factor of nine.

## 13. Design consequences, all three binding

1. **Use maximal coupling, not quantile coupling.** The gain column is not a
   rounding difference. At moderate divergence it is the difference between a
   usable `ME` estimate and an unusable one.
2. **Fix the vocabulary order in the sampler.** Sorting by probability is the
   default in common sampling implementations and it destroys the coupling.
3. **`keyed_uniform` must stay a pure function of its key.** An RNG object with
   advancing state makes the draw depend on call order, and call order differs
   between branches. Order independence is verified in the script.

## 14. What this converts

CAR's "hard across divergent LLM contexts, left as a refinement" becomes a
quantity with a closed form, an optimal construction, a measured cost, and three
implementation requirements. `ME` is reported with per-step `TV` and coupling
efficiency attached, so a reader can see exactly where the estimate is tight and
where divergence has eroded it.

This is a result about samplers, established on synthetic categorical
distributions. It has not yet been run against a language model, and the
preconditions it assumes (per-request seed control, single-stream inference,
fixed vocabulary order) are model-selection constraints that Gate C must confirm.
