# P2 Pre-Registration Skeleton

NOT YET A PRE-REGISTRATION. This is the list of items that must be filled and committed with a timestamp before Stage 1 results are pooled. Target: 30 September 2026.

## 1. Hypotheses and primary contrast
- [ ] H1 to H4 stated with directional predictions
- [ ] The single primary contrast named. Everything else labelled exploratory.
- [ ] Both abstracts drafted and committed (result-positive and result-negative)

## 2. Corpus
- [ ] N per system, derived from the power simulation, not chosen
- [ ] Stratification rule across outcome classes
- [ ] Inclusion and exclusion criteria for decisions

## 3. Intervention protocol
- [ ] Operator assignment rule by node type
- [ ] K (alternative-generation count) and sampling temperature
- [ ] The four resample-validity checks and their thresholds
- [ ] Counterfactual-environment distribution declared per deterministic tool
- [ ] Off-support check for DE pinning, and its threshold
- [ ] Discard rules. Discard means discard, and the rate is reported per node type.

## 4. Estimators
- [ ] Repeat counts R_0, R_1, R_2 derived from Stage 0
- [ ] Shapley convergence criterion and efficiency check tolerance
- [ ] Null-replay action-match rate below which the study pauses

## 5. Observability attributors
- [ ] All five specified as code, hashed
- [ ] Citation to the real tool or practice backing each one
- [ ] Judge set J, judge prompts frozen, inter-judge agreement statistic named

## 6. Analysis
- [ ] Primary model (rank-ordered, decision-level random effects) fully specified
- [ ] Secondary model (OLS on ranks, SE clustered by decision) fully specified
- [ ] Bootstrap scheme: over repeats and over decisions, both
- [ ] Multiplicity handling
- [ ] Stratification for Stage 2 and Stage 3 subsets, including the random low-rank control sample

## 7. Stopping and deviation
- [ ] What would cause the design to change, and what would be reported if it did
- [ ] Any deviation from this document is logged in RESEARCH_LOG.md with a reason, on the day
