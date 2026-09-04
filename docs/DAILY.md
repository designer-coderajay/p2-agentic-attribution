# P2 Daily Log

Append-only. One entry per day of the August sprint. Written at end of day, never reconstructed later.
Sprint: 13 to 31 August 2026, 19 days, 15 hours per day, arXiv 31 August.

---

## D1, Thursday 13 August 2026

**Hours.** Partial day. Sprint declared mid-day.

**Shipped (build).**
- `src/p2/scm.py`: synthetic agent SCMs with analytically known structure, CRN stream keyed by (seed, step, replicate).
- `src/p2/effects.py`: four estimators. `TE_marg` (CAR's estimand), `TE_crn` (unit-level counterfactual under common random numbers), `DE` (Pearl natural direct effect via downstream pinning), `ME = TE_crn - DE`. Plus CAR's point-of-commitment rule reproduced for the head-to-head, and a pin-plausibility diagnostic.
- `docs/DERIVATIONS.md`: every effect derived by hand BEFORE the estimators ran.
- `scripts/validate_estimators.py`: checks estimates against the derivations, fails outside 4 MC sigma.
- `docs/TODO.md`: eight workstreams, every item with an acceptance check.

**Result.** 16/16 estimates within 4 MC sigma of analytic. Decomposition identity residual exactly 0. Mediated share 0.500 against analytic 1-w = 0.500. `env_hash 9c043b7372c27cfc`.

**The finding, on synthetic ground truth only.** On the planted partial-mediation SCM, step 0 has no causal path to the outcome whatsoever, yet the marginal run-forward estimator returns TE = -0.501 for it, numerically indistinguishable from the genuinely decisive step 1 at -0.501. Under common random numbers both inert steps return exactly 0.000 and the planted structure is recovered without any heuristic. CAR names this confound in section 4 and resolves it with the point-of-commitment locus rule; CRN removes it by construction. This is an estimator result on a known structure and must not be written as a claim about any real system.

**Bug caught by the derivations, first run.** The marginal arm initially re-rolled the steps BEFORE k, which is not CAR's estimand. It failed at 60 and 54 sigma on steps 2 and 3 while the CRN, DE and ME arms passed. Fixed by pinning the factual prefix. The derivations existing first is the only reason this was caught rather than shipped.

**Shipped (planning).**
- Kill-gate verification. 2605.09168 (CIVeX) and 2607.25364 (EBTE) both VERIFIED to exist and both cleared: ex ante action gatekeepers, not post hoc attribution.
- Found the actual threat: arXiv 2606.08275, Causal Agent Replay, VERIFIED, absent from the original brief. Overlaps section 4 of the brief nearly line for line.
- Also found: 2605.25338 (CausalFlow), 2606.09692 (delegation-scope non-identifiability).
- Repo skeleton, positioning memo, research plan revision 2, citation ledger, memory doc, pre-registration skeleton.
- Two skills created: `p2-research-protocol`, `agentic-intervention-design`.
- August sprint plan with cut list, five gates, and pre-decided fallbacks.

**Slipped.** Nothing yet. Sprint starts from a standing start on D1 rather than a running one.

**Gate status.**
- **Gate A (positioning): PASSED on D1, a day early.** Full text of 2606.08275 read. Sec 7 states the direct effect is left as a refinement; no observability comparison beyond the cited Who&When figure; real tools with side effects declared out of scope, demonstrations use mocked tools. All four surviving contributions confirmed open, and the real-system differentiator is conceded in print. P2 proceeds to full build.
- Gates B, C, E (17 Aug): not yet reachable.
- Gate D (prereg lock, 20 Aug): not yet reachable.

**Deviations from pre-registration.** None. No pre-registration exists yet; Gate D is 20 August.

**Decisions taken.** Logged in full at the foot of `docs/POSITIONING.md`. In short: adopt CAR's five-operator intervention algebra instead of P2's three; add a head-to-head against their point-of-commitment rule as a named contribution; rule-based outcome function only; real-tool side effects promoted to a headline differentiator and stated in the abstract; DE pinning uses common random numbers where contexts have not diverged and gets the largest build block; P1 slips to 1 to 5 September analysis, arXiv around 12 September. All reversible.

**Tomorrow, D2, Friday 14 August.** Gate A cleared early, so D2 gains half a day. Reallocated to starting the harness.
1. Full read 2605.25338 (CausalFlow) and 2509.08682 (Ma et al., Shapley over static logs, newly surfaced from CAR's bibliography). Verify 2505.00212 and 2509.03312 directly.
2. Full read 2606.09692, scope the Annex IV spec against its non-identifiability result.
3. Pull ahead from D3: harness architecture. Clone CAR's repo, assess how much of the record-replay layer transfers to a LangGraph pipeline with live MCP servers.

---

## D2, Friday 14 August 2026

**Shipped.** Four papers checked from source, two of them previously unknown to this project. Positioning addendum 2 and nine ledger entries written.

**Gate A: still PASSED, but the basis has narrowed and the score should change.**

- 2605.25338 CausalFlow VERIFIED with author list confirmed on the arXiv listing rather than taken from CAR's bibliography. Cleared: oracle substitution not same-policy resample, binary CRS with no intervals, purpose is repair not measurement.
- 2607.20827 Liao VERIFIED, full text read. Cleared on two independent axes: its intervention unit is a context factor in a static prompt with no environment transition simulated, so no re-execution, no DE, no ME; and it runs no observability comparison. But it publishes P2's contribution-1 framing, that a correct action need not be grounded only in permitted evidence, on 23 July 2026. That framing is no longer available as novel.
- Four further papers surfaced and logged: AcquaBench 2607.24054, OAT 2607.12747, PAE 2603.03116, and a SURVEY of evidence tracing and execution provenance, 2606.04990, at v4 by late June.
- Two more RECALLED via Liao's bibliography and unverified: AttriGuard 2603.10749, CausalArmor 2602.07918.

**What this costs.** Four of the eight elements P2 was standing on are now occupied: interventional attribution over steps, Shapley over components, attributing correct rather than failed decisions, and trajectory re-execution. Four remain unoccupied after four days of searching: the CRN direct and mediated effect decomposition, the observability rank comparison with bias decomposition, live side-effecting tools in a regulated decision, and the Annex IV conversion. The full table is in `docs/POSITIONING.md` addendum 2.

**Deviations from pre-registration.** None. No pre-registration exists; Gate D is 20 August.

**Tomorrow, D3.**
1. Read the survey 2606.04990 in full. It is the single highest-value remaining read because it maps the whole space and any residual novelty claim has to survive it.
2. Verify AttriGuard and CausalArmor directly.
3. Begin harness architecture, WS2.1 and 2.2.

**Standing note for Ajay.** Gate A was scheduled for today and its formal action is your re-score. My assessment, INFERRED: P2 remains a real paper and the D1 CRN result remains unoccupied, but this is a narrower methods-plus-measurement contribution with a strong regulatory deliverable, not the flagship the brief described. The re-score should be against the eight-row table in addendum 2.

---

## D3, Saturday 15 August 2026

**Shipped.** Full read of arXiv 2606.04990v4, the survey of evidence tracing and execution provenance. Positioning addendum 3.

**Result: the survey clears P2 and strengthens it.**

Three findings, each checked against the four remaining rows of the addendum-2 table:

1. The survey states P2's premise as an open design tension (a log records what happened without showing whether memory influenced a tool call) and nowhere reports a measurement of it.
2. **Section 6.3 Table 5 grades execution-provenance metrics as "Proposed", defined by the survey as desiderata without agreed definitions or broadly adopted evaluation protocols**, while evidence attribution and safety metrics are graded Established. This is a third-party survey-level statement that P2's measured quantity has no agreed protocol. It goes in paragraph one.
3. No mediation, no direct effect, no common random numbers, no counterfactual estimand, no observability-versus-causal comparison, and no EU AI Act or Annex IV anywhere in the document.

**Bonus for WS6.** The survey's section 7.1 and 6.4 specify what a full-stack provenance schema must record. The Annex IV deliverable should be built on that rather than invented: the field has converged on what to record, and P2 adds what must additionally be recorded for post-hoc causal attribution to be possible. Cheaper and more citable.

**Cost.** The survey's framing that a correct answer reveals nothing about how an output was produced is the third independent occurrence of P2's contribution-1 motivation, after Liao and AcquaBench. It is common ground. Cite and move on.

**Deviations from pre-registration.** None. Gate D is 20 August.

**Carried forward, unverified.** AttriGuard 2603.10749, CausalArmor 2602.07918, plus fifteen related-work references surfaced from the survey bibliography. None threatens the four remaining rows on its face; several are load-bearing for WS6.

**Tomorrow, D4.** Literature phase closes. WS2 begins: harness architecture, trajectory capture into the schema, node-level checkpoint and restore. Gates B, C and E are on 17 August and all three depend on it.

---

## D4, Sunday 16 August 2026

**Shipped.** `src/p2/mediation.py` (WS2.6, side-effect containment), `src/p2/coupling.py` (WS2.7, CRN across divergent contexts), `scripts/validate_coupling.py`, DERIVATIONS Part II. Literature phase closed.

**WS2.6, tool mediation.** Four purity classes drive four mediation strategies: PURE, READ_ONLY_VOLATILE, EFFECTFUL_IDEMPOTENT, EFFECTFUL_UNSAFE. Identical requests always serve the recorded factual response, which is exact, free and safe for every class. Diverged requests re-call only if PURE, sandbox only if idempotent and sandboxing is enabled, and otherwise draw from a declared counterfactual environment. EFFECTFUL_UNSAFE never executes, and the refusal is recorded rather than silent. `ToolSpec` refuses to construct a non-PURE tool without a declared counterfactual environment, so guessing is impossible by design.

Falls out of this: the first concrete Annex IV requirement the project has produced. A provider who does not record tool requests keyed by content cannot support post-hoc causal attribution, because a counterfactual request cannot be told apart from the factual one.

**WS2.7, and a false claim caught before it reached a manuscript.** The first draft of `coupling.py` asserted that shared-uniform inverse-transform sampling attains the maximal-coupling bound `1 - TV(p,q)`. **The closed-form check rejected it at up to 215 sigma.** It is false: an early perturbation shifts every later CDF boundary, so quantile coupling decouples the whole tail.

Corrected, both couplings now implemented with their own closed forms and both validated within 1.9 MC sigma at every divergence level:
- quantile coupling: `sum_i max(0, min(P_i,Q_i) - max(P_{i-1},Q_{i-1}))`
- maximal coupling: exactly `1 - TV(p,q)`, optimal, costs one extra forward pass

At `TV = 0.179` the numbers are 0.412 versus 0.821. A naive probability-sorted sampler delivers 0.086 against an achievable 0.821, a factor of nine.

**What that converts.** CAR's "hard across divergent LLM contexts, left as a refinement" is now a quantity with a closed form, an optimal construction, a measured cost and three binding implementation requirements. That is WS2.7 discharged in theory. It is not discharged in practice: this is a result about samplers on synthetic categorical distributions and has never touched a language model.

**Deviations from pre-registration.** None. Gate D is 20 August.

**Tomorrow, D5. Gates B, C and E.** Trajectory capture from Langfuse/OTel into the schema, node-level checkpoint and restore, and Stage 0 null replay measuring action-match rate and per-rollout cost. All three gates depend on access to the BFSI pipeline, which I do not have. **This is the point at which the sprint needs Ajay's system, not more of my code.**

---

## D5 to D8, 17 to 20 August 2026 (retroactive summary, reconstructed from git log)

**This entry was not written same-day and is flagged as such.** The chat that
did this work did not keep DAILY.md current; the record below is reconstructed
from commit messages and file contents on 20 August, not written live. Treat
timestamps within this entry as approximate and the content as a summary, not
a same-day account.

**Shipped, per commit history.** WS1.6 pin-plausibility and H1/H2 machinery
(cluster coverage 0.95 vs naive 0.35 on intercept); Plackett-Luce rank-ordered
estimator and the H3 statistic; WS3.3 provenance audit (`docs/PROVENANCE.md`,
recency cut, three attributors survive); `preregistration/PREREG.md` first
draft; the pre-registered primary contrast implemented and validated, plus H4;
`verify.sh`; the mediation safety test; the separation guard for the primary
contrast, then the `|z| > 40` rule removed after it was shown to be a
false-positive generator (DERIVATIONS Part IV); the separation rule
pre-registered; an end-to-end dry run, first generator collinear rather than
correlated (verbosity coefficient +172, p = 1e-98, quasi-complete separation,
caught before any manuscript claim), fixed; `docs/HANDOVER.md` written for a
Cowork transfer.

**Gates B, C, E: still not reached.** Confirmed still blocked on BFSI pipeline
access as of this entry. No Stage 0 measurement exists. `sigma_resid` for the
power RULE in PREREG s3 remains unmeasured; the rule itself does not need to
change, only the number, and the number needs the live system.

**Deviations from pre-registration.** None recorded in this window beyond what
is logged under D8 below.

---

## D8 (cont.), 20 August 2026, Cowork session

**Scope.** Gate D day. Handed off via `docs/HANDOVER.md` from the prior
session with two OPEN items blocking the gate. Reviewed the full repo,
`verify.sh` ALL GREEN on the incoming state, then worked the first blocking
item, which is a pure math and statistics problem solvable without pipeline
access.

**DEVIATION FROM PRE-REGISTRATION, logged same day per s7.** PREREG s2's
ratio-to-causal convention for reporting PL coefficients is replaced with
`beta / ||beta||_2` (normalised direction), CI by decision-level bootstrap
instead of the causal-anchored ratio. Reason: the causal-anchored ratio is
provably unbounded as `beta_causal -> 0`, and both H1 and H2 predict
`beta_causal` is small, so the convention meant to make the result readable
was guaranteed to malfunction exactly when the paper's headline finding holds.
Demonstrated on the project's own dry-run fit (`beta_causal = -0.029` ->
"ratio to causal" of -26.7 for verbosity, unstable under a perturbation smaller
than its own se). Full derivation in `docs/DERIVATIONS.md` Part V. Implemented
as `ranking.normalized_beta` (point estimate + delta-method se, both validated
exactly invariant to the PL scale ambiguity) and `ranking.bootstrap_normalized_beta`
(the interval actually reported, because the delta method is shown to
under-cover near the unit-sphere pole at 30.7% relative difference against
Monte Carlo). `scripts/validate_primary.py` s6, six sub-checks, all passing.
`scripts/dry_run.py` updated to print and save the corrected convention.
`verify.sh` ALL GREEN after the change. This does not touch the primary
contrast itself: the joint Wald test is algebraically invariant to
`beta -> c*beta, V -> c^2*V` and was never affected by the bug, verified as
part of the same check.

**Not resolved, and not resolvable from here.** The second OPEN item at
handover, `sigma_resid` for the power rule, requires a Stage 0 measurement
against the live BFSI pipeline. Gates B, C, E remain blocked on the same
access, now overdue since 17 August, four days. Nothing in this session's
scope can substitute for that measurement without inventing a number, which
the standing rules forbid.

**Status for Gate D.** The one defect identified as blocking the gate at
handover is fixed and validated. Whether that satisfies Gate D, or the corpus
RULE items (unmeasured until Stage 0 runs) mean the gate is better described as
"pre-registration mechanically complete, awaiting Stage 0 to instantiate two
RULE-determined numbers," is Ajay's call. Recommendation, INFERRED: lock the
document now, since every entry is either LOCKED outright or a RULE whose
procedure (not outcome) is fixed, which is what the RULE/LOCKED distinction in
PREREG s0 exists to allow. Stage 0 then resolves the RULE entries mechanically
without reopening the document.

**Tomorrow.** Blocked on Ajay for Gates B, C, E (BFSI pipeline access) and the
Gate D sign-off decision above. If access does not arrive, the fallback
already pre-registered in PREREG s7 applies: report synthetic and
sampler-level results only, state the absent live arm in the abstract. Work
continues in parallel on items that do not need pipeline access: WS0 remaining
literature verification (Pearl 2009 library record, Shapley citations, AttriGuard,
CausalArmor), WS6 Annex IV drafting against the primary EU AI Act text, WS1.7
non-binary outcome estimators, WS1.9 pytest/CI.

## Gap, 21 August to 2 September 2026

**No entries. Thirteen days.** AUGUST-SPRINT s7 made this log binding at one
entry per day and it was not kept. Recorded as a gap rather than backfilled from
git, because a reconstructed entry is the thing the protocol exists to prevent
and this log already contains one of those.

What happened in the gap is in `RESEARCH_LOG.md` under 21, 23 and 25 August: the
citation sweep, the regulatory retrieval, WS5.3 and WS1.7. What did not happen is
any step of the sprint plan from D9 onward, all of which needed pipeline access.

## D-restart, Thursday 3 September 2026

1. **Hours.** Cowork session.
2. **Shipped.** Programme audit against all four plan documents. Fallback
   invoked and recorded with a date. Abstract rewritten for the delivered scope.
   Two stale status docs corrected. Three convention directories created. Paper
   outline written.
3. **Slipped.** The sprint's arXiv date of 31 August, by three days at the point
   it was noticed. No fallback was triggered because none was pre-decided for
   the ship date itself, which is a defect in the sprint plan worth naming.
4. **Gates.** A passed. D ready to lock, Ajay's call, unchanged. B, C and E are
   now **CUT by the fallback**, not blocked: they gate a live arm this paper does
   not have. That is a status change, and it means no gate is now waiting on
   anything outside the repository.
5. **Deviation from pre-registration.** None. The fallback is clause two of s7
   and is invoked as written.
6. **Tomorrow's blocks.** WS1.9 pytest and CI. Remaining reachable workstream
   items. Manuscript sections 3 to 6, which are written from `DERIVATIONS.md`.
7. **Needing a decision from Ajay.** Gate D sign-off, still open. P1 and P3
   state, which this chat cannot see and which the 10 September and 19 September
   dates make urgent.

## D-restart+1, Friday 4 September 2026

1. **Hours.** Cowork session.
2. **Shipped.** WS1.9: 85 tests, `tests/test_contracts.py` for specification
   compliance, `pytest.ini`, pinned `requirements-dev.txt`, GitHub Actions
   workflow, pytest wired into `verify.sh`. Two defects found and fixed while
   writing it (bare `pytest` interpreter resolution; `validate_mediation.py`
   omitting `seed` against its own stated principle).
3. **Slipped.** Nothing today.
4. **Gates.** Unchanged. A passed, D awaiting sign-off, B/C/E cut by the fallback.
5. **Deviation from pre-registration.** None. One `env_hash` moved by design and
   is gated; no scientific number moved.
6. **Tomorrow's blocks.** Manuscript sections 3, 4, 5 and 6 from `DERIVATIONS.md`.
   Then section 8 from `REGULATORY-BASIS.md`.
7. **Needing a decision from Ajay.** Gate D sign-off, still open. P1 and P3 state,
   still unknown to this chat, and the 10 and 19 September dates have not moved.
