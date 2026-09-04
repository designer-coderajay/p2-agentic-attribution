# P2 Work Breakdown

> **SCOPE CHANGE 2026-09-03.** The pre-registered fallback is invoked (PREREG
> header). Every item requiring live BFSI access is **CUT from this paper** and
> carried to a follow-on study, not left open: WS2.2 to WS2.5, WS2.8, WS4.1 to
> WS4.4, and the `N` and replay-floor RULE entries. They are not failures and
> not abandoned; they are the pre-registered experiment the paper publishes and
> does not run. Items reachable without access remain live and are the week's
> work.

Eight workstreams. Every item carries an **acceptance check**: the thing that must
be true for the item to be closed. An item without a check is not a task, it is a
wish. Status as of 13 August 2026, end of D1, with corrections dated 2026-08-25 and 2026-09-03.

Epistemic discipline applies to every line: VERIFIED means searched or fetched with
a URL, RECALLED means training only, INFERRED means reasoning. Nothing enters the
manuscript from the second or third category.

---

## WS0. Literature and citation integrity

| # | Item | Acceptance check | Status |
|---|---|---|---|
| 0.1 | Full read 2606.08275 (CAR) | DE arm present or absent, established from the text | **DONE.** Absent, sec 7. Gate A passed |
| 0.2 | Full read 2605.25338 (CausalFlow) | Confirm no DE arm, no observability rank comparison | **DONE 2026-08-14.** Cleared |
| 0.3 | Full read 2509.08682 (Ma et al., Shapley over static logs) | Confirm static-log basis, no interventional arm | **DONE 2026-08-21.** Static-log basis confirmed, cleared. **Citation was WRONG in title and first author, corrected, see ledger C1** |
| 0.4 | Verify 2505.00212 (Who&When) directly | Authors, venue, and the ~14% figure read from the source, not from CAR | **DONE 2026-08-21.** ICML 2025 PMLR v267 pp.76583-76599 confirmed. 14.2% verified as a four-cell abstract-only average; realistic-log value is single-digit. See ledger C2 |
| 0.5 | Verify 2509.03312 (AgenTracer) directly | Oracle-substitution basis confirmed from the source | **DONE 2026-08-21.** Confirmed for the failed-trajectory branch only; fault injection is the other half |
| 0.6 | Full read 2606.09692 (delegated-execution observability) | Its non-identifiability result stated precisely; scope WS6 against it | **DONE 2026-08-21.** Result is narrower than assumed (authorization relation, a Proposition true by construction). Zero EU AI Act content. See ledger C3 |
| 0.7 | Pearl 2009 against a library record | Edition, publisher, year confirmed outside CAR's bibliography | **DONE 2026-08-21.** Stanford + CUP. Sections 4.5.4/4.5.5 located. Pearl 2001 UAI added as the primary citation, Robins & Greenland 1992 for priority |
| 0.8 | Fetch Thinking Machines nondeterminism post | Load-bearing for the replay-floor gate; must be read not cited blind | **DONE 2026-08-21.** Changes what Gate C asks: batch invariance, not single-stream. DERIVATIONS s15. See ledger C4 |
| 0.10 | Verify AttriGuard 2603.10749 and CausalArmor 2602.07918 | Ex ante or post hoc established from the text | **DONE 2026-08-21.** Both ex ante guardrails, both cleared, titles and authors exact. Pin AttriGuard v2 |
| 0.11 | **Read Reg (EU) 2024/1689 Arts. 11, 12, 13, 86 and Annex IV in the primary text** | Provisions quoted from the Official Journal text, not from summaries | **DONE 2026-08-25, this row was stale until 2026-09-03.** Articles 6(1), 6(2), 11, 12, 13, 18(1), 19, 26, 86, 113, Annex III pt 5 and Annex IV complete, all VERBATIM from the Publications Office repository, in `docs/REGULATORY-BASIS.md`. **Still open:** Arts 25, 72, 74, 79(1) and the Art 3 definitions |
| 0.9 | Final ledger pass | Every bibliography entry VERIFIED with a checked date. RECALLED entries cut, not chased | D18. Remaining RECALLED set ranked by risk at the foot of the ledger |

## WS1. Estimator core

| # | Item | Acceptance check | Status |
|---|---|---|---|
| 1.1 | Trajectory schema and CRN stream | Draws are a pure function of (seed, step, replicate), order independent | **DONE** |
| 1.2 | `TE_marg`, `TE_crn`, `DE`, `ME` estimators | All four match hand derivations within 4 MC sigma on a planted SCM | **DONE.** 16/16 pass, `env_hash 9c043b73` |
| 1.3 | Decomposition identity | `ME = TE_crn - DE` residual < 1e-9 per step | **DONE.** Residual 0.0 |
| 1.4 | Mediated share closed form | Recovers `1 - w` on the partial-mediation SCM | **DONE.** 0.500 vs 0.500 |
| 1.5 | CAR point-of-commitment rule, reproduced verbatim in intent | Locus matches CAR's stated semantics on the planted SCM | **DONE.** Returns step 3 |
| 1.6 | Pin-plausibility diagnostic | Analytic value 0.5 at step 3 under DE(1) recovered | partial. Estimated 0.54; needs a tightened probe and its own derivation |
| 1.10 | Maximal-coupling sampler wired into the estimators | `DE` arm uses maximal coupling; per-step TV and coupling efficiency reported alongside ME | open |
| 1.7 | Non-binary and continuous outcome functions | Estimators correct where `Y` is not in {0,1} | **DONE 2026-08-25.** Estimators confirmed correct on a continuous `Y` with OPPOSING direct and mediated paths (`y = w*a1 - (1-w)*a3`), all four steps within MC error of a hand derivation, identity residual 5.6e-17. **Found a real defect in the reporting layer, not the estimators:** `|ME|/|TE|` exceeds 1 under suppression and would rank a suppressed node above a pure mediator, inverting H4. Fixed by `effects.mediated_share`, LOCKED in PREREG s2, derived in DERIVATIONS Part VI, guarded by `scripts/validate_suppression.py` in `verify.sh`. Changed the dry-run H4 from +0.698 to +0.855 |
| 1.8 | Replay-nondeterminism arm | Factual side resampled too; effect intervals widen correctly | open |
| 1.9 | Unit tests, pinned seeds, CI | `pytest` green from a clean checkout | **DONE 2026-09-04.** 85 tests, green from a clean tree and from a subdirectory. `tests/test_contracts.py` checks that LOCKED reports are actually reached by `dry_run.py`, that every validator is wired into `verify.sh`, and that the provenance guards hold. Wired into `verify.sh` and into GitHub Actions |

## WS2. Replay harness for the live system

| # | Item | Acceptance check | Status |
|---|---|---|---|
| 2.1 | Assess CAR's public repo for transferable record-replay layer | Written assessment of what transfers to LangGraph plus live MCP | open, D2 |
| 2.2 | Trajectory capture from Langfuse/OTel into the schema | Round-trip a real BFSI decision without loss | open, D3 |
| 2.3 | Node-level checkpoint and restore | State `s_k` reconstructed byte-identically for arbitrary `k` | open, D4 |
| 2.4 | Suffix-only re-execution | Re-run from `k` produces the factual trajectory when nothing is forced | open, D4 |
| 2.5 | The five CAR operators against the live pipeline | `do_resample`, `do_action`, `do_observation`, `do_context`, `do_policy` all exercised | open, D5 |
| 2.6 | **Side-effect containment for live tools** | No counterfactual rollout mutates external state; unsafe calls refused and logged | **DONE in principle.** `src/p2/mediation.py`: four purity classes, four strategies, refusal recorded. Needs the real MCP tool inventory classified. |
| 2.7 | CRN across divergent LLM contexts | Closed form for the coupling, optimal construction, measured degradation | **DONE in theory**, `env_hash 6e1224b9f63551b9`. Both couplings match closed form within 1.9 sigma. NOT yet run against a language model. |
| 2.8 | Stage 0 null replay | Action-match rate, wall clock, price, prefix-cache saving, all measured | D5. **Gates B, C, E** |

## WS3. Observability attributors

| # | Item | Acceptance check | Status |
|---|---|---|---|
| 3.1 | `span_duration`, `token_count`, `recency`, `terminal_action` | Deterministic code, hashed, each with a citation to a shipping tool | open, D7 |
| 3.2 | `llm_judge` attributor, `J >= 3` judges | Prompts frozen; inter-judge agreement reported | open, D7 |
| 3.3 | Attributor provenance audit | Every attributor traced to a real tool or practice, else cut | open, D7. Answers "your heuristics are strawmen" |

## WS4. Corpus and protocol

| # | Item | Acceptance check | Status |
|---|---|---|---|
| 4.1 | Rule-based outcome function `Y`, frozen and hashed | No LLM in `Y`. CAR sec 7 is explicit that judge outcomes inject noise | open, D4 |
| 4.2 | Counterfactual environment declared per deterministic tool | Stated as an assumption, with sensitivity design | open, D6 |
| 4.3 | Decision corpus, stratified across outcome classes | Inclusion criteria written before selection | open, D7 |
| 4.4 | Second system, reduced arm | Stage 0 and 1 at minimum | open, D11 |

## WS5. Statistics and pre-registration

**Note, 2026-08-20: this table was last updated D1 and had drifted from the
repo's actual state. Corrected below against `preregistration/PREREG.md`,
`docs/DERIVATIONS.md`, and `verify.sh` (ALL GREEN) rather than left stale.**

| # | Item | Acceptance check | Status |
|---|---|---|---|
| 5.1 | Simulation-based power analysis | `N` derived from Stage 0 variance, not chosen | **RULE locked** (PREREG s3). Number needs Stage 0, **blocked on BFSI pipeline access** |
| 5.2 | Kendall tau_b with bootstrap over decisions | Distribution reported, not the mean alone | **DONE.** `analysis.bootstrap_over_decisions`, used in `dry_run.py` H1/H4 |
| 5.3 | H2 model: rank-ordered primary, OLS-on-ranks secondary | Both pre-specified; VIFs reported | **DONE 2026-08-25.** Both LOCKED reports were implemented and validated in `analysis.py` but never called in `dry_run.py`, so the specification was satisfied in the library and unsatisfied in the analysis. Now wired: VIFs per covariate with a flag above the 6.11 level coverage was verified to, CR1 OLS secondary with cluster and naive se side by side, and an explicit primary-vs-secondary agreement line implementing the "state it in the abstract" clause |
| 5.4 | **Pre-registration committed with a timestamp** | Commit exists before any pooled result is viewed | **Drafted, one known defect fixed 2026-08-20** (ratio-to-causal convention, `docs/DERIVATIONS.md` Part V). Gate D sign-off is Ajay's call |
| 5.5 | Both abstracts drafted | Result-positive and result-negative, both committed | **DONE.** PREREG s8 |
| 5.6 | Normalised-beta reporting convention | Point estimate, delta-method se, bootstrap CI, all validated against invariance and coverage | **DONE, 2026-08-20.** `ranking.normalized_beta`, `ranking.bootstrap_normalized_beta`, `validate_primary.py` s6 |

## WS6. Annex IV traceability specification

| # | Item | Acceptance check | Status |
|---|---|---|---|
| 6.1 | Read Reg (EU) 2024/1689 Arts. 11, 12, 13, 86 and Annex IV in the primary text | Not summaries | **DONE 2026-08-25.** See 0.11. Four load-bearing findings established in `REGULATORY-BASIS.md` s9 |
| 6.2 | Scope against 2606.09692's non-identifiability result | Stated precisely, with what it forecloses | **PARTIAL 2026-09-04.** Chapter III Section 2 placement now VERBATIM, Article 25 and the Art 3 definitions retrieved and reviewer objection 3 answered from their own text. **Arts 72, 74 and 79 now retrieved too**, see s19 to s22 |
| 6.3 | Draft the specification | What a provider must log for post-hoc causal attribution to be possible at all | D12 to D15 |

## WS7. Paper and reproducibility

| # | Item | Acceptance check | Status |
|---|---|---|---|
| 7.1 | Positioning paragraph one, against CAR | Differentiation in the abstract, not in related work | open |
| 7.2 | Limitations in the abstract | Single organisation's systems, no Shapley arm, CRN degradation | open |
| 7.3 | Red-team session, fresh context | An independent attempt to make the result an artifact, and the response | D16 |
| 7.4 | Every figure traceable | Config, seed, environment hash per figure | continuous |
| 7.5 | Public repo, pinned environment | Clean-checkout reproduction of every number | D18 |

---

## Blocking dependencies, in order

```
0.1 DONE ──> 2.1 ──> 2.2 ──> 2.3 ──> 2.4 ──> 2.7 ──> 2.8 (Gates B,C,E) ──> 5.1 ──> 5.4 (Gate D) ──> Stage 1
                                              │
                                              └── 2.6 side-effect containment BLOCKS every live rollout
```

**2.7 (CRN across divergent LLM contexts) is the highest technical risk in the
paper.** It is the condition CAR names as the reason it left the direct effect
alone. If CRN cannot be maintained once contexts diverge, `DE` degrades and H4
weakens, and the honest fallback is to report `DE` only on the low-divergence
subset with the divergence rate stated. That fallback is decided now, not in
October.
