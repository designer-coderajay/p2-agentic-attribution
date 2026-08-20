# P2 Research Log

Append-only. Dated. What was run and what was learned.

## 2026-08-13

**Scope.** Literature and design session. No compute. P1's specification sweep is the owning project this week; this session is reading and writing only, which does not contend for GPU.

**Ran.** Four web searches verifying the P2 kill-gate papers and scanning for prior art on intervention-based agent attribution.

**Learned, and it changes the paper.**

1. arXiv 2605.09168 (CIVeX) and 2607.25364 (EBTE), the two papers the brief named as kill-gate threats, both VERIFIED to exist and both **cleared**. Both are ex ante gatekeepers deciding whether a proposed action should execute. P2 is post hoc attribution over an executed trajectory. Different object.

2. **arXiv 2606.08275, Causal Agent Replay, is the real threat and was absent from the brief.** VERIFIED. It contains an SCM over agent runs, a do-operation with run-forward under the same stochastic policy, an intervention algebra over steps, a Monte Carlo Shapley estimator, confidence intervals throughout, an action-match rate for replay, and the framing that observability answers what happened but not what caused it. That overlaps section 4 of the brief nearly line for line.

3. Also found: 2605.25338 (CausalFlow), 2606.09692 (Observability for Delegated Execution, proves a non-identifiability result about audit logs and delegation scope), and a prior chain via 2505.00212 (Who&When) and 2509.03312 (AgenTracer).

**Consequence.** The flagship rationale in section 1 of the brief does not survive. The intervention algebra and Shapley estimator are prior art. What survives: the measured object is regulated decisions rather than failures, the comparison is a rank-agreement plus bias decomposition rather than a scalar accuracy, the ME/DE decomposition (pending confirmation that CAR has no DE arm), and the Annex IV conversion.

**Written.** `docs/POSITIONING.md`, `docs/P2-RESEARCH-PLAN.md` (revision 2), `docs/CITATION-LEDGER.md`, this log. Two skills created: `p2-research-protocol`, `agentic-intervention-design`.

**Also flagged, not P2's to resolve.** The P3 kill gate was dated 10 August. Its outcome is not recorded in this chat. If it failed, reallocation has already changed P2's calendar.

**Next.** Full read of 2606.08275, priority one, deadline 15 August. The specific question: does it have a direct-effect arm and any observability comparison beyond the single Who&When number. Gate A on 24 August, Ajay re-scores.

**Open for Ajay.** Five decisions listed in `docs/P2-RESEARCH-PLAN.md` section 11.

## 2026-08-13, second entry

**Sprint declared.** Ajay compressed P2 to 13 to 31 August, 15 hours per day, arXiv 31 August. Plan written to `docs/AUGUST-SPRINT.md`. Daily log opened at `docs/DAILY.md`.

Cuts: Stage 3 Shapley dropped (prior art, CAR ships it), third-party framework arm dropped, second system reduced, N set by power simulation rather than the undelivered N >= 300 figure. Kept: DE/ME decomposition, the five attributors, the bias decomposition, pre-registration, Annex IV spec.

Five gates, all moved forward. Gate A is 14 August and it decides whether the remaining 250 hours happen at all.

Flagged to Ajay: P1's 24 to 31 August analysis window collides with this sprint; recommended P1 slips to 1 to 5 September. Also flagged that P2 will now appear on arXiv before P1, inverting the intended reading order.

## 2026-08-13, third entry

**GATE A PASSED, a day early.** Full text of arXiv 2606.08275v1 fetched and read.

Four things confirmed, all VERIFIED from the full text:
1. Sec 7: isolating a step direct effect "is left as a refinement". No DE arm. H4 and the ME decomposition are open, and named by the authors as future work.
2. No observability comparison anywhere in the paper beyond the cited Who&When 14 percent figure. H1, H2, H3 untouched.
3. Sec 7: real tools with side effects are out of scope; demonstrations use mocked, reproducible tools; validation is against synthetic SCMs. The live-BFSI differentiator is conceded in print.
4. Sec 6: CAR explicitly disclaims novelty on counterfactual replay and Shapley for agent blame. Field commons, not their property.

Six decisions taken and logged at the foot of docs/POSITIONING.md. Most consequential: adopt CAR five-operator algebra (do_resample, do_action, do_observation, do_context, do_policy) rather than the remove/resample/corrupt triple, and add a head-to-head of ME/DE against their point-of-commitment locus rule as a named contribution.

Citation ledger gained nine references harvested from CAR bibliography, including the Pearl reference that was load-bearing and unverified: Causality: Models, Reasoning, and Inference, CUP, 2nd ed, 2009. Marked VERIFIED-SECONDARY pending a library record.

Residual risk: 2605.25338 and 2509.08682 unread. On the D2 calendar.

## 2026-08-20

**Scope.** Gate D day, handed to a Cowork session via `docs/HANDOVER.md`. Full
repo review top to bottom against the incoming state (`verify.sh` ALL GREEN,
git log to `10f7cbd`), then work on the two OPEN items HANDOVER listed as
blocking the gate.

**Resolved.** PREREG s2's ratio-to-causal convention for reporting Plackett-Luce
coefficients was identification-broken: it divides by `beta_causal`, and both
H1 and H2 predict `beta_causal` is small, so the convention was guaranteed to
misbehave exactly in the regime the paper is built to detect. Confirmed on the
project's own dry-run numbers (`beta_causal = -0.029` producing a "ratio to
causal" of -26.7 for verbosity, unbounded under an arbitrarily small
perturbation of `beta_causal`). Fixed by reporting `beta / ||beta||_2`
(coefficient direction on the unit sphere, exactly invariant to the same PL
scale ambiguity, well-defined whenever any coefficient carries signal) with a
decision-level bootstrap confidence interval, matching the bootstrap-over-
decisions convention already locked for every other interval in the paper.
Six new validation checks in `scripts/validate_primary.py`, all passing,
including confirmation that the primary contrast's Wald test itself was never
affected (it is algebraically invariant to the scale ambiguity that broke the
ratio). Full derivation: `docs/DERIVATIONS.md` Part V. Deviation logged in
`docs/DAILY.md` the same day per PREREG s7.

**Not resolved.** The second OPEN item, `sigma_resid` for the corpus-size power
rule, needs a Stage 0 measurement against the live BFSI pipeline. Gates B, C, E
remain blocked on pipeline access, overdue since 17 August. This is not
resolvable without either the live system or fabricating a number, and the
standing rules forbid the second option. **This is the single item blocking
further empirical progress on P2 and it needs Ajay's action, not more
analysis.**

**Backfilled.** DAILY.md had no entries between D4 (16 Aug) and today, despite
five days of committed work (WS1.6, H1/H2 machinery, Plackett-Luce, WS3.3
provenance audit, the pre-registration draft, the primary contrast, H4, the
separation guard and its correction, the mediation safety test, the first
end-to-end dry run). Reconstructed retroactively from git log and flagged as
such rather than presented as a same-day record.

**Next.** Blocked on Ajay: (1) BFSI pipeline access for Stage 0 / Gates B, C, E,
(2) a decision on whether today's fix satisfies Gate D or the gate stays open
pending a second read. Not blocked, and available to continue in parallel:
WS0 remaining citation verification, WS6 Annex IV drafting, WS1.7/1.9.
