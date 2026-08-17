# P2 Research Plan

**Causal Attribution for Agentic Decisions. Revision 2, 13 August 2026.**

Revision 1 was `paper-2-agentic-attribution.md`. This revision supersedes sections 1, 2, 3, 4 (partly), 8, 9, 12, and 13 of that brief. Read `docs/POSITIONING.md` first; it explains why.

Epistemic tags used throughout: **VERIFIED** (searched or fetched this session, URL given), **RECALLED** (training, unverified), **INFERRED** (reasoning). Any number not tagged VERIFIED has not been measured.

---

## 0. Scheduling note, requires a decision from Ajay before work proceeds

Three timing facts, stated because they conflict:

1. The programme operating model says one project owns each day, and names context-switching as the highest-probability failure mode.
2. P1's schedule has the full specification sweep running 10 to 24 August, which is compute-bound and unattended, and P1 ships to arXiv on 10 September.
3. The P3 kill gate was dated 10 August, three days ago. I have no record in this chat of whether it fired. It is not P2's business to resolve, but if it failed, reallocation has already changed what P2's calendar looks like.

P2's original start was 24 September. My position, INFERRED: doing P2's **literature and design** work now is correct and does not violate the operating model, because P1's sweep is unattended compute and P2's current work is reading and writing, not GPU time. Doing P2's **build** now would violate it. The plan below is structured on that split. If Ajay disagrees, the August and September rows change and nothing else does.

---

## 1. Revised research question

Original: does agentic observability tooling identify the components that causally determined a decision?

That question was answered in the negative, at low resolution, by arXiv 2606.08275 (VERIFIED). The revised question:

> **When causal attribution over an agent trajectory is available as ground truth, what is the structure of the error made by the observability record a provider would actually file, and what record-keeping requirement would remove it?**

Three sub-questions, each mapping to a hypothesis:

- Q1: How large is the discrepancy, measured as rank agreement, and does its interval exclude the level an accountability claim would require?
- Q2: What is the discrepancy made of? Specifically, does the observability record track presentational properties (recency, verbosity, terminality) after conditioning on causal effect?
- Q3: Is the failure explained by mediation? Do the nodes observability misses have low direct effect and high mediated effect?

Q2 and Q3 are the paper. Q1 is the setup.

---

## 2. Hypotheses

| ID | Statement | Both-outcomes-publishable check |
|---|---|---|
| H1 | Kendall tau_b between `A_obs` and `A_causal = TE` is low, with a bootstrap CI excluding the accountability threshold | If agreement is high, the finding is that current observability is adequate for Annex IV, which is a positive result a standards body wants and nobody has shown |
| H2 | After conditioning on causal rank, `A_obs` retains systematic dependence on recency and verbosity | If the dependence vanishes, observability error is unstructured noise, which implies a different remedy (more repeats, not different instrumentation) and is equally writeable |
| H3 | A non-trivial fraction of decisions have a causally dominant node that is negligible in the trace | Either direction is a number a regulator can act on |
| H4 | The discrepancy concentrates in nodes with high `ME` and low `DE` | If it does not, the mechanism is something else and identifying what is the contribution |

Both abstracts get drafted in the week the pre-registration is locked, not after Stage 1 results are seen.

**H4 is load-bearing for novelty.** If the full read of CAR shows a direct-effect arm, H4's status changes and Ajay re-scores the paper. See `docs/POSITIONING.md` section 6.

---

## 3. Design

Four stages. Each stage's parameters are set by the previous stage's measurement, never by a guess.

### Stage 0. Null replay and cost measurement

Purpose: establish the noise floor and the price of one rollout.

- Re-execute `N_0` trajectories with no intervention, `R_0` times each.
- Report the **action-match rate**: fraction of null replays producing the same action sequence. This is the noise floor. No effect smaller than it is reportable.
- Measure wall clock and price per suffix rollout, with and without prefix-cache reuse.
- Gate: if the action-match rate on the local primary model is below a pre-registered threshold, the study pauses and the cause is found before Stage 1. A low match rate on a hosted frontier endpoint is expected and is an argument for confining that model to a subset arm.

### Stage 1. Screening

Purpose: rank every node by effect magnitude and variance cheaply, so Stages 2 and 3 can be targeted.

- All decisions, all nodes, **resample operator only**, small `R_1`.
- Output: per-node `TE` point estimate with a Wilson interval, and a variance estimate.
- The stratification rule for Stages 2 and 3 is derived from this and is **pre-registered before Stage 1 results are pooled**.

### Stage 2. Full attribution

Purpose: `TE`, `DE`, `ME` with intervals, on a stratified subset.

- Stratified subset of decisions, top-`k` nodes by Stage 1 screening plus a random sample of low-ranked nodes (so the design does not condition on the outcome it is measuring; this control is not optional).
- Three operators. Resample primary, remove and corrupt as contrasts.
- `DE` arm requires pinning downstream nodes to factual values. Report the off-support rate. See the `agentic-intervention-design` skill, section 3.

### Stage 3. Shapley

Purpose: interaction, and the divergence from single-node estimates.

- Smaller stratified subset, Monte Carlo permutation sampling.
- Convergence diagnostic and efficiency check both reported. Stop on the convergence criterion, not on budget.

### The observability arm, run in parallel with all stages

`A_obs` is computed from the traces the systems already emit through Langfuse and OpenTelemetry. Five attributors, each justified by a real tool or practice, each implemented as deterministic code except the last:

1. `span_duration` rank
2. `token_count` rank (verbosity)
3. `recency` rank
4. `terminal_action` (the node that executed the decision)
5. `llm_judge`, `J >= 3` judges, inter-judge agreement reported

Attributor 5 is the only place an LLM generates a measured object, and it is permitted only because judge variance is measured as part of the design. **Every attributor must carry a citation to the tool or practice that ships it.** A reviewer will call these strawmen; the citation is the answer, and it is the same defence structure P1 uses for the claim map.

---

## 4. Statistics

- **Rank agreement.** Kendall tau_b per decision, aggregated with a bootstrap over decisions. Report the distribution, not the mean alone.
- **H2 model.** Ranks within a decision are a permutation, so within-decision observations are not independent and the naive OLS-on-ranks with clustered standard errors is defensible but not ideal. Primary specification: a rank-ordered (Plackett-Luce family) model with decision-level random effects. Secondary: OLS on ranks with standard errors clustered by decision, reported for comparability with how such results are usually presented. Pre-register both, report both, and if they disagree say so in the abstract.
- **Collinearity.** Recency, verbosity, and causal rank are correlated by construction. Report variance inflation factors and partial effects. A significant `beta_2` with a VIF of 12 is not a finding.
- **Intervals everywhere.** Proportions get Wilson intervals. Effect shifts get bootstrap intervals computed **twice**: over repeats within a node (sampling noise) and over decisions (population noise). Reporting the ratio of the two is a headline number, mirroring P1's seed-variance-versus-analytic-variance ratio.
- **Power.** No formula. Kendall tau_b under clustered, permutation-constrained data has no clean closed form here, and quoting a textbook `n` would be a fabricated number. Run a **simulation-based power analysis** using Stage 0 and pilot Stage 1 variance, before the corpus size is fixed.
- **Multiplicity.** Four hypotheses, five attributors, two systems, several node types. Pre-register the primary contrast; everything else is exploratory and labelled as such in the tables.

---

## 5. Cost model

The naive design in the original brief is not affordable and the "Medium" severity rating in its threats table was wrong. Illustrative arithmetic, **INFERRED, with no measured per-rollout cost**:

Naive, assuming 25 nodes per trajectory, `N = 300` per system, 3 operators, 30 repeats:

```
300 x 25 x 3 x 30 = 675,000 suffix rollouts per system
1,350,000 across two systems
```

That is not happening in an October window on any budget Ajay has.

Nested, same assumptions:

```
Stage 0    20 decisions  x 30 null replays                        =     600
Stage 1   300 decisions  x 25 nodes x 1 op   x  5 repeats         =  37,500
Stage 2   100 decisions  x  6 nodes x 2 ops  x 25 repeats x 2 arms=  60,000
Stage 3    30 decisions  x 1,000 coalition evaluations            =  30,000
                                                    per system    = 128,100
                                                    two systems   = 256,200
```

Two savings, both mandatory, both measured in Stage 0 rather than assumed:

- **Suffix-only re-execution.** Intervening at node `t` requires re-running from `t`, not from the start. For uniformly distributed `t` the expected saving is close to a factor of two.
- **Prefix cache reuse.** The prefix up to `t` is identical across all repeats at that node. On a local model this should be a large saving. Measure it.

INFERRED: with an effective 4 seconds per rollout, 256,000 rollouts is approximately 285 single-stream hours, roughly 12 days continuous, which is feasible with parallelism inside the October window and not feasible without it. **If Stage 0 measures anything above roughly 10 seconds effective, the design changes before the standard of evidence does.** That is a stated kill condition, not a hope.

Frontier API model: subset arm only, costed separately, and its low expected action-match rate is a reason to keep it small.

---

## 6. Systems and corpus

- **Primary:** the BFSI credit underwriting pipeline, five MCP servers (credit bureau, GST, bank transaction, penny-drop verification, RBI compliance), instrumented with Langfuse and OpenTelemetry. Already built, already a high-risk decision type under Annex III, already emitting the traces `A_obs` is computed from.
- **Second:** the enterprise agentic platform, three MCP servers.
- **Third if reachable:** a third-party framework. This is the answer to "both systems are his", and it is worth more than a larger `N` on the first two. Prioritise it over corpus size if a trade is forced.
- **Corpus:** stratified across outcome classes. Final `N` set by the Stage 0 and pilot power simulation, not by the `N >= 300` figure in the brief, which was not derived from anything.

**Deterministic tools are a design problem, not a detail.** A penny-drop verification API has no conditional distribution to resample from. This requires an explicitly declared counterfactual environment per tool, stated as an assumption, with sensitivity analysis, and named in the abstract. See `agentic-intervention-design` skill, section 2.

---

## 7. Models

Capability-bound, not patching-bound. Below roughly 20 to 30B, reliable multi-step tool use degrades and attribution failure becomes confounded with incompetence.

All model and benchmark figures carried over from the brief (a 35B-class MoE at 73.4 on SWE-Bench Verified; Gemma 3 27B on a single 4090) are **RECALLED from a comparison site, not verified against primary model cards, and the landscape has moved since**. Re-verify current open-weight availability on Hugging Face before the build starts, and check the official card before any number enters the paper.

One additional selection criterion the brief did not have: **replay tightness**. A single-stream local model with a fixed seed replays far more reliably than a shared hosted endpoint, and the whole design rests on replay. Weight this alongside capability.

---

## 8. Deliverables

1. The paper.
2. Public repo, pinned environment, config and seed and environment hash per figure.
3. Timestamped pre-registration commit.
4. **The Annex IV traceability specification for agentic systems**, shipped standalone. Scope this only after reading arXiv 2606.09692 (VERIFIED), which proves a non-identifiability result about audit logs and delegation scope and partially occupies this territory.
5. The observability attributor implementations, released. INFERRED: like P3's cue-injection benchmark, this is infrastructure, and infrastructure gets cited longer than findings.

---

## 9. Revised schedule

| Dates | Work | Compute |
|---|---|---|
| 13 to 20 Aug | Full reads: 2606.08275, 2605.25338, 2606.09692. Verify 2505.00212, 2509.03312. Update positioning. | None. Runs alongside the P1 sweep. |
| 20 to 24 Aug | Run CAR's public repo against one BFSI trajectory. Establish exactly what it does and does not produce. | Trivial. |
| **24 Aug** | **Gate A. Ajay re-scores P2 and confirms or drops flagship status.** Binding. | |
| 25 Aug to 10 Sept | P1 owns the calendar. P2 dormant. | P1 |
| 10 to 24 Sept | Stage 0 on the BFSI pipeline. Action-match rate and per-rollout cost measured. Attributor implementations written. | Small |
| **24 Sept** | **Gate B. Cost gate. If effective per-rollout cost breaks the nested budget by more than a factor of three, the design shrinks the same day.** | |
| 24 to 30 Sept | Pre-registration written and committed with a timestamp. Both abstracts drafted. Power simulation run. | None |
| 1 to 31 Oct | Stages 1, 2, 3. | The big spend |
| 1 to 20 Nov | Analysis. Annex IV traceability spec drafted. | Small |
| 20 Nov to 5 Dec | Writing. Red-team session in a fresh chat with no context. arXiv 5 Dec. | None |

Two new binding gates, A on 24 August and B on 24 September, replacing the single 24 September gate in the brief.

---

## 10. Red team, written now rather than after the result

The strongest objections a reviewer will raise, and the response each requires:

1. **"CAR did this."** The response is H2 and H4, and it only works if the full read confirms CAR has no direct-effect arm and no bias decomposition. This is why the full read is the first thing on the calendar and not the last.
2. **"Your observability heuristics are strawmen."** Response: every attributor carries a citation to the tool or practice that ships it. If an attributor cannot be sourced to something real, it is cut.
3. **"Resampling a deterministic bureau API is not resampling."** Response: the declared counterfactual environment, the sensitivity analysis, and naming it in the abstract. This objection is correct and the only defence is owning it.
4. **"Pinned downstream nodes are off-support, so ME is meaningless."** Response: the measured off-support rate, `ME` reported as bounded where the rate is high, and the low-off-support subset as the primary analysis.
5. **"Both systems are yours, both LangGraph."** Response: the third-party framework arm. If it does not happen, the limitation goes in the abstract.
6. **"You are measuring a mid-size model's incompetence."** Response: the frontier API subset arm, and the Stage 0 task-success rate reported before any attribution number.
7. **"The effect is smaller than your replay noise."** Response: the action-match rate is reported first and every effect is read against it.

The formal red-team session is scheduled for the writing window: a fresh chat, no context on how much work went in, asked to argue the result is an artifact.

---

## 11. Open decisions, all Ajay's

1. Does P2 do literature work now, or stay fully dormant until 24 September? Section 0.
2. After the full reads, does P2 remain the flagship, or does P1 take that slot? Gate A, 24 August.
3. Third-party framework arm versus larger corpus, if a trade is forced. My recommendation, INFERRED: take the third framework. It removes an objection that no amount of `N` removes.
4. Venue. The revised framing fits FAccT better than a systems venue. Confirm before the writing window shapes the paper.
5. Whether the Annex IV traceability spec ships with the paper or as a separate, earlier artifact aimed at CEN-CENELEC JTC 21. INFERRED: earlier and separate reaches more people, but it burns the paper's novelty budget if it lands first.
