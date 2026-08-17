# P2 August Sprint

**13 to 31 August 2026. 19 days, 15 hours per day, 285 hours. arXiv 31 August.**

Supersedes section 9 of `P2-RESEARCH-PLAN.md` (revision 2). Everything else in that plan stands.

Epistemic tags: **VERIFIED** searched or fetched with a URL. **RECALLED** training, unverified. **INFERRED** reasoning. No number below is measured.

---

## 1. What had to be cut, and why these and not others

285 hours cannot deliver the revision-2 design. The cuts are chosen so that everything novel survives and everything that is prior art goes first.

| Cut | Was | Now | Reason |
|---|---|---|---|
| **Stage 3, Shapley** | Full arm, 30 decisions, 1,000 coalition evaluations per system | **Dropped. Cite 2606.08275 for it.** | It is prior art. CAR ships a budget-bounded Monte Carlo Shapley estimator. Spending 30,000 rollouts to reproduce someone else's contribution is the worst trade available. |
| **Third-party framework arm** | If reachable | **Dropped.** Limitation stated in the abstract. | No time. It was always the first thing to go. |
| **Second system** | Full parallel arm, N >= 300 | **Reduced replication arm.** Stage 0 and Stage 1 only, smaller N, plus Stage 2 on the top nodes if days 15 to 17 hold. | Two systems is the minimum against "artifact of one architecture". Reducing it is survivable; cutting it is not. |
| **Corpus size** | N >= 300 per system | Set by the power simulation on day 8. **INFERRED, likely 100 to 150 primary.** | N >= 300 was never derived from anything. |
| **Frontier API upper anchor** | Decision subset | Kept, small, run in parallel on API so it costs money not wall clock. | Cheap in the currency that is scarce. |

**Kept, non-negotiable, because they are the paper:** the `DE` arm and `ME = TE - DE` (H4), the five observability attributors, the bias decomposition (H2), the pre-registration, and the Annex IV traceability specification.

Dropping Shapley removes the interaction result. Say so in the limitations, in the abstract, and point at CAR.

---

## 2. Gates, all moved forward

| Gate | Was | Now | Condition | Consequence if it fails |
|---|---|---|---|---|
| **A. Positioning** | 24 Aug | **14 Aug, end of day** | Full read of 2606.08275 confirms no direct-effect arm and no observability bias decomposition | If CAR has a `DE` arm, P2 is an application paper. Stop, do not build, reallocate to P1 the same day. |
| **B. Cost** | 24 Sept | **17 Aug, end of day** | Stage 0 measures effective per-rollout cost inside the nested budget | Shrink N and repeat counts the same day. The design changes, the standard of evidence does not. |
| **C. Replay floor** | new | **17 Aug, with B** | Null-replay action-match rate above the pre-registered threshold on the local primary model | If replay is loose, effects are unreadable. More repeats, or a tighter model, decided that day. |
| **D. Pre-registration lock** | 30 Sept | **20 Aug, end of day** | Analysis plan committed with a timestamp, both abstracts drafted | Nothing pooled before this commit exists. Hard stop. |
| **E. Harness working** | new | **17 Aug** | Checkpoint, resample, suffix re-execute, score, end to end on one BFSI trajectory | This is the real engineering risk, not compute. If it slips past 19 Aug the ship date goes. |

Gate A is 36 hours away and it is the one that decides whether the other 250 hours happen.

---

## 3. Day by day

Three blocks per day. Block 1 and 2 are deep work, block 3 is build, analysis, or writing depending on the phase. Compute runs overnight where marked.

| Day | Date | Block 1 | Block 2 | Block 3 | Overnight |
|---|---|---|---|---|---|
| D1 | Thu 13 Aug | Full read 2606.08275 (CAR), targeted at the `DE` question | CAR read continued, extract exactly what it measures against observability | Clone and run CAR's repo, assess adaptability to a LangGraph pipeline | - |
| D2 | Fri 14 Aug | Full read 2605.25338 (CausalFlow) | Full read 2606.09692, scope the Annex IV spec against its non-identifiability result | **GATE A.** Verify 2505.00212 and 2509.03312 directly. Update positioning. | - |
| D3 | Sat 15 Aug | Harness architecture: trajectory capture, node-level checkpoint and restore against the BFSI LangGraph | Model selection. Verify current open-weight availability on Hugging Face. Replay-tightness as a selection criterion. | Begin harness build | - |
| D4 | Sun 16 Aug | Harness core: checkpoint, restore, suffix re-execution | Outcome scoring function `Y`, frozen and hashed | Harness end-to-end on one trajectory | - |
| D5 | Mon 17 Aug | Stage 0: null replay, `N_0` trajectories, `R_0` repeats | Measure action-match rate, wall clock, price, prefix-cache saving | **GATES B, C, E.** Re-cost the sprint from measured numbers. | Stage 0 completion runs |
| D6 | Tue 18 Aug | Resample operator, plus the four validity checks | Counterfactual-environment declaration per deterministic tool (penny-drop, bureau) with sensitivity design | Remove and corrupt operators as contrasts | - |
| D7 | Wed 19 Aug | Five observability attributors as deterministic code, each with its tool citation | Judge harness, `J >= 3`, prompts frozen | Corpus assembly and stratification | - |
| D8 | Thu 20 Aug | Power simulation from Stage 0 and pilot variance. Fix `N`. | Write the pre-registration in full | **GATE D. Timestamped commit.** Both abstracts drafted. | - |
| D9 | Fri 21 Aug | Launch Stage 1 screening, primary system | Related work section, written against CAR and CausalFlow | `DE` pinning implementation, off-support check | **Stage 1 runs** |
| D10 | Sat 22 Aug | Stage 1 results, derive the Stage 2 stratification per the locked rule | Method section | Stage 2 configuration and dry run | - |
| D11 | Sun 23 Aug | Launch Stage 2, primary system | Introduction, positioning paragraph one against CAR | Second system Stage 0 | **Stage 2 runs** |
| D12 | Mon 24 Aug | Stage 2 monitoring, partial results | Second system Stage 1 launch | Annex IV traceability spec, first draft | **Both run** |
| D13 | Tue 25 Aug | Stage 2 primary completes. Sanity checks against the noise floor. | Analysis: Kendall tau_b, bootstrap over repeats and over decisions | Second system Stage 2 launch if D12 held | **Stage 2 second system** |
| D14 | Wed 26 Aug | H2 model: rank-ordered primary, OLS-on-ranks secondary, VIFs | H4: `ME` and `DE` decomposition, off-support rate | **Figure 1.** All figures generated from committed configs. | - |
| D15 | Thu 27 Aug | Results section | Annex IV spec finalised | Reproducibility pass: config, seed, environment hash per figure | - |
| D16 | Fri 28 Aug | **Red team.** Fresh chat, no context, asked to argue the result is an artifact. | Address whatever it finds | Discussion section | - |
| D17 | Sat 29 Aug | Limitations into the abstract, not section 7 | Full paper assembly, LaTeX | Repo cleanup, pinned environment | - |
| D18 | Sun 30 Aug | Full read-through, every number traced to a committed config | Citation ledger final pass. Nothing unVERIFIED enters the bibliography. | Buffer | - |
| D19 | Mon 31 Aug | Final pass | arXiv submission | Log, handover to P1 | - |

---

## 4. Slack: there is none, and that is the plan's main defect

D18 block 3 is the only buffer in 19 days. INFERRED, and I am confident in this one: something will slip, and the most likely candidate is the replay harness on D3 to D5, because instrumenting a LangGraph pipeline for node-level checkpoint and suffix re-execution is the kind of work that reveals its difficulty on day two.

Three pre-decided fallbacks, so the decision is made now and not at 2am on D6:

1. **Harness slips past 19 Aug.** Drop the second system entirely. Recover four days. State the single-architecture limitation in the abstract.
2. **Cost gate B fails by more than 3x.** Cut `N` to whatever the power simulation says is the floor, and cut `R_2` before cutting `N`. Repeats buy precision, `N` buys generalisation, and generalisation is the thing reviewers attack.
3. **Replay floor gate C fails.** Move the primary to a tighter single-stream local model even at a capability cost, and report task success rate before any attribution number so the capability trade is visible.

---

## 5. Collisions outside P2

Two, both requiring a call from Ajay, neither mine to make.

**P1.** Its schedule has pre-registration and analysis on 24 to 31 August and writing 1 to 10 September, arXiv 10 September. A 15-hour P2 sprint through 31 August takes that window. Options: P1 analysis slips to 1 to 5 September with writing 5 to 12 and arXiv around 12 September, or P1's sweep results sit untouched until 1 September. The second is cheaper and I would take it, INFERRED, since the sweep is unattended compute and the results do not spoil.

**Order of appearance.** P2 on arXiv 31 August and P1 on 10 to 12 September means P2 lands first. The P1 cross-citation for the ablation-operator argument still works, and P2 gains an "extended in forthcoming work" line. No problem, but it inverts the programme's intended reading order, so it is worth being deliberate about.

---

## 6. The risk I am obliged to name once

19 consecutive 15-hour days raises the error rate, and the two errors that matter here are irreversible: an unverified citation entering the manuscript, and an unlogged deviation from the pre-registration. Both are career damage and neither is recoverable after submission.

Two mitigations, both cheap, both binding:

- **No citation enters the bibliography unless it is VERIFIED in `docs/CITATION-LEDGER.md` with a checked date.** D18 block 2 is a full ledger pass, and anything still RECALLED gets cut, not chased.
- **Every deviation from the pre-registration is logged in `docs/DAILY.md` on the day, with a reason.** Not reconstructed later.

That is the whole of what I have to say about it. Your call on the hours.

---

## 7. Daily update protocol

`docs/DAILY.md` is append-only. One entry per day, written at end of day, containing:

1. Hours worked, blocks completed
2. What shipped
3. What slipped, and which fallback was triggered if any
4. Gate status, and any gate now unreachable
5. Any deviation from the pre-registration, with reason
6. Tomorrow's three blocks, restated
7. Anything needing a decision from Ajay, listed

Say "daily update" at the end of any session and I will write the entry and re-cut the remaining days against actual progress rather than against this plan.
