# P2 Pre-Registration

**Status: DRAFT. Becomes binding at the Gate D commit, target 20 August 2026.**
Nothing pooled, inspected or analysed before that commit exists.

Two kinds of entry below.
**LOCKED** is a fixed choice, final at the Gate D commit.
**RULE** is a decision procedure whose output is determined mechanically by a
Stage 0 measurement that does not yet exist. A rule removes the researcher degree
of freedom without pretending to a number we have not measured. Any rule still
unresolved when Stage 0 completes is resolved by the rule, not by judgment.

---

## 1. Hypotheses and directional predictions

| ID | Statement | Direction |
|---|---|---|
| H1 | Kendall tau_b between each observability attributor's ranking and the causal ranking (TE_crn) is low | tau_b bootstrap CI over decisions excludes 0.5 from below |
| H2 | After conditioning on causal rank, attributor rankings retain systematic dependence on recency and verbosity | joint Wald test of (beta_recency, beta_verbosity) = (0,0) rejects |
| H3 | A non-trivial fraction of decisions have a causally dominant node the trace ranks negligible | H3 > 0 with Wilson CI excluding 0 at the pre-registered (delta, tau) |
| H4 | The discrepancy concentrates in nodes with high ME and low DE | rank correlation between per-node mediated share and obs-causal rank gap is positive |

**PRIMARY CONTRAST, LOCKED, one only:** the H2 joint 2-degree-of-freedom Wald
test of `(beta_recency, beta_verbosity) = (0, 0)` in the Plackett-Luce model,
conditioning on causal rank, pooled across the three attributors with the
decision as the clustering unit.

A joint test rather than two marginal tests, so H2 carries no multiplicity
correction. H1, H3, H4 and all per-attributor breakdowns are **exploratory** and
labelled as such in every table.

## 2. Estimators, all validated before this document

| estimator | validation | env_hash |
|---|---|---|
| TE_marg, TE_crn, DE, ME | 16/16 within 4 MC sigma of hand derivations; identity residual 0.0; mediated share 0.500 vs analytic 1-w | 9c043b73 (linux) / 24f3e9e5 (macos) |
| quantile and maximal coupling | both match closed form within 1.9 sigma at every divergence level | 6e1224b9 / 1a987180 |
| tau_b, CR1 cluster-robust OLS | exact tau_b cases; planted betas covered; cluster coverage 0.943-0.953 vs naive 0.347 on intercept; null FP 0.048/0.052 | f9cba1c8 / 2a4494eb |
| Plackett-Luce, H3 | PL recovers its generative model, se/sd calibration 1.011/1.083/1.030 on disjoint seeds; H3 matches E[H3]=p(1-tau) at six planted cells | badc7184 / 61f8bcfd |

**LOCKED:** `ME` is reported with per-step TV and coupling efficiency attached.
**LOCKED:** `DE` uses maximal coupling, not quantile coupling. Fixed vocabulary
order in the sampler. `keyed_uniform` remains a pure function of its key.
**LOCKED:** PL coefficients are reported as **ratios**, never as levels.
Misspecification absorbs a common scale factor (measured at 1.039 under Gaussian
latents), so levels are not identified.

## 3. Corpus

- **LOCKED:** stratified across outcome classes of the BFSI underwriting decision.
- **LOCKED:** outcome function `Y` is rule-based and frozen with a hash. No LLM
  in `Y`. CAR section 7 is explicit that judge outcomes inject their own noise.
- **RULE, N:** `n_decisions` is the smallest value satisfying
  `2.802 * sigma_resid / sqrt(n_steps * n_decisions) <= MDE_target`, with
  `MDE_target = 0.10` on the standardised scale and `sigma_resid` the
  within-decision residual sd measured in Stage 0. Design analysis shows H2 is
  over-powered at plausible `sigma_resid`, so **N is expected to bind on tau_b
  precision and H3's tail, not on H2 power**; whichever binds, the rule above is
  the floor and the binding criterion is reported.
- **RULE, exclusion:** decisions whose Stage 0 null-replay action-match rate falls
  below the replay floor (section 6) are excluded and the exclusion rate reported.

## 4. Intervention protocol

- **LOCKED:** operators are CAR's five (`do_resample`, `do_action`,
  `do_observation`, `do_context`, `do_policy`). `do_resample` is primary.
- **LOCKED:** tool purity classes (PURE / READ_ONLY_VOLATILE /
  EFFECTFUL_IDEMPOTENT / EFFECTFUL_UNSAFE) declared per MCP tool BEFORE any
  rollout. EFFECTFUL_UNSAFE never executes; refusals are logged and the refusal
  rate reported.
- **LOCKED:** every non-PURE tool carries a declared counterfactual environment,
  stated in the paper as an assumption with sensitivity analysis.
- **LOCKED:** resample-validity checks are schema validity, support membership,
  semantic type preservation and non-degeneracy. Failures are **discarded, not
  repaired**, and the discard rate is reported per node type.
- **RULE, off-support threshold:** the primary DE analysis uses the subset with
  pin plausibility above the 25th percentile of the Stage 0 distribution; the
  full set is a robustness arm. Both reported.
- **RULE, repeat counts:** `R_1`, `R_2` set so the per-node effect interval half
  width is below 0.05 on the outcome scale, computed from Stage 0 variance.

## 5. Observability attributors

**LOCKED: three.** `span_duration`, `token_count`, `terminal_action`. Each sourced
to documented shipping behaviour in `docs/PROVENANCE.md`. Code hashed at the Gate
D commit.

**`recency` was cut** as an attributor (no shipping tool ranks by recency) and is
retained only as a covariate in the H2 regression, where it is a bias term
requiring no tool provenance.

**LLM-judge attributor: RULE.** Included only if `J >= 3` judges are run with
frozen prompts and inter-judge agreement is reported. If the judge arm cannot be
afforded, it is dropped entirely rather than run at `J = 1`.

## 6. Analysis

- **LOCKED, primary:** Plackett-Luce, decision as the unit, cluster-robust
  sandwich. Calibration ratio (mean se over empirical sd) reported alongside.
- **LOCKED, secondary:** CR1 cluster-robust OLS on the attributor score.
  Reported for comparability. If primary and secondary disagree, that is stated
  in the abstract.
- **LOCKED:** VIFs reported. Coverage was verified to hold to VIF 6.11.
- **LOCKED:** bootstrap over decisions, never over rows.
- **LOCKED:** H3 reported across the full `(delta, tau)` grid,
  `delta in {1.0, 0.9, 0.8}` x `tau in {0.25, 0.5, 0.75}`. A single cell is a
  tuned number.
- **RULE, replay floor:** the null-replay action-match rate measured in Stage 0
  is the noise floor. No effect smaller than it is reported as an effect.

## 7. Stopping and deviation

- Any deviation from this document is logged in `docs/DAILY.md` **on the day**,
  with a reason, and appears in the paper.
- If Stage 0 cannot be run, the paper reports the synthetic and sampler-level
  results only, states the absence of a live arm in the abstract, and no live
  claim is made.
- If the LLM-judge arm is dropped, H1 and H2 are reported over three attributors
  and the omission is stated in the abstract.

## 8. Both abstracts, drafted before any result is seen

**If the discrepancy is found (H1-H4 supported):**

> Causal attribution over agent trajectories is now possible in principle, but
> only as a total effect on mocked tools. We run it on a live regulated credit
> underwriting system with five external services, add the direct-effect
> decomposition prior work leaves open, and find that the observability record a
> provider would file recovers neither: its ranking agrees with causal effect at
> tau_b = [X], and after conditioning on causal rank it retains systematic
> dependence on presentational properties. The discrepancy concentrates in nodes
> whose influence is mediated rather than direct. We specify the record-keeping an
> Annex IV filing would need to be checkable.

**If no discrepancy is found (H1-H4 not supported):**

> Causal attribution over agent trajectories is now possible in principle, but
> only as a total effect on mocked tools. We run it on a live regulated credit
> underwriting system with five external services, add the direct-effect
> decomposition prior work leaves open, and find that the observability record a
> provider would file **does** track causal effect (tau_b = [X]), with no residual
> dependence on presentational properties after conditioning. Deployed
> observability is therefore adequate as Annex IV evidence for this system class,
> a claim the field currently asserts without measurement and which a survey of
> execution provenance grades as having no agreed evaluation protocol. We specify
> the conditions under which the result should be expected to hold.

Both are writeable. Neither is a null result.

## 9. Signature

Gate D is met when this file is committed with a timestamp and no pooled result
has been inspected. The commit hash is the pre-registration.
