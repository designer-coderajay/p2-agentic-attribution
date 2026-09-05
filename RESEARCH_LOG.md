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

## 2026-08-21

**Scope.** Two pieces of work. First a provenance repair, then the WS0 citation
verification sweep that had been sitting since 13 August.

**Provenance repair, committed and pushed.** `requirements.txt` said
`numpy>=1.26`, a floor rather than a pin, and three numpy versions had produced
artifacts in `results/`: 1.26.4 on the machine of record, 2.2.6 from a stray
interpreter, 2.4.4 from a cloud session. Standing rule 10 requires a pinned
environment and that was not a true statement about the repo. Pinned to
`numpy==1.26.4`; `validate_mediation.py` now records numpy so the fingerprint is
uniform across all seven artifacts; every artifact regenerated on the machine of
record. Verified field-by-field against HEAD before committing: worst non-env
delta 1.110e-16, everything else bit-identical, so this was pure provenance and
no claim moved. `git fsck` clean, which also retires the iCloud-corruption worry
flagged in PUSH.md. Commits `6b3d2f6` and `c91b3f4` are now on the private
GitHub remote, verified by SHA match after fetch.

**Citation sweep, five parallel verifications against primary sources.** This is
the substantive result of the day.

1. **A wrong citation was caught before it reached the bibliography.** 2509.08682
   was recorded as "Automatic Failure Attribution and Critical Step Prediction via
   Causal Inference" by "Y. Ma et al.". Both title and first author are wrong. The
   actual title is "... Method for Multi-Agent Systems Based on Causal Inference"
   and the first author is **Guoqing Ma**; the only "Y." initial belongs to the
   last author. It sat in the ledger for eight days marked RECALLED. Standing
   rule 1 exists for exactly this and the ledger discipline worked.

2. **On substance 2509.08682 clears P2**, verified from full text: static logs,
   no re-execution for attribution, zero occurrences of mediation or direct
   effect, Shapley over agents rather than steps, no regulatory content. One
   qualification worth pre-empting in related work: it compares trace-reading
   LLM-judge baselines against its causal method, but scores both against human
   annotation rather than against causal ground truth, so it is not a measurement
   of whether observability tracks causation. That gap is still ours.

3. **The Who&When 14.2% figure is real but three obvious ways of citing it are
   wrong.** It appears exactly once in the paper, in the abstract, in no table,
   and is the mean of four Table 1 cells. The best single cell is 25.51%. More
   importantly, **on realistic hand-crafted long logs it is 7.02 and 8.77 against
   a 4.16 random baseline**. If P2's argument is about long-horizon traces the
   honest number is single-digit, which is stronger for the thesis than 14.2%.

4. **The delegation non-identifiability result is narrower than recorded and
   must be cited more carefully.** 2606.09692 proves the *authorization relation*
   is non-identifiable, as a Proposition whose proof defines the observation
   function to discard the quantity. It is a scoping result, not an impossibility
   barrier. Cite as "must be bound at execution time", never as "attribution from
   logs is impossible". It also has zero EU AI Act content, so the regulatory
   bridge in WS6 is entirely ours and must not be attributed to them. Vendor
   paper, no seeds or CIs on its metrics.

5. **The replay floor needs batch invariance, and our stated precondition was
   wrong.** DERIVATIONS section 14 listed "single-stream inference" as a
   precondition. The primary source does not claim that. The forward pass is
   already run-to-run deterministic; nondeterminism comes from lack of batch
   invariance under varying server load; temperature 0 plus a fixed seed is not
   sufficient, and their measurement is 80 unique completions from 1000
   temperature-0 samples, collapsing to 1 with batch-invariant kernels.
   Determinism is also not version-invariant. **This changes what Gate C is
   asking**: not "can we replay" but "can we obtain batch-invariant inference on
   the serving stack we have". Written up as DERIVATIONS section 15.

6. **Pearl attribution improved.** Pearl 2009 is now verified against the Stanford
   library record and CUP catalogue rather than CAR's bibliography, sections 4.5.4
   and 4.5.5 located, and 2nd edition confirmed as necessary. But Pearl (2001)
   UAI is the standard primary citation for the natural direct effect, with Robins
   & Greenland (1992) holding priority. All three now cited in DERIVATIONS s4.

Also cleared: AttriGuard 2603.10749 and CausalArmor 2602.07918, both ex ante
guardrails, both with titles and author lists exactly as believed. AgenTracer
oracle-substitution basis confirmed, with the qualification that it is only the
failed-trajectory half of the method. Castro et al. 2009 fully verified, surname
takes an accent, Gómez.

**Operational finding.** One verification agent had its scratchpad file
overwritten mid-task by a concurrent process. It detected the substitution,
re-fetched in isolation, and re-derived every quote. Parallel verification must
use isolated working directories; silent cross-contamination between two citation
checks would be very hard to catch after the fact.

**What is now the single load-bearing unverified item.** Regulation (EU)
2024/1689 primary text, Articles 11, 12, 13, 86 and Annex IV. The entire WS6
deliverable rests on it and no verified reading exists. Nothing else on the
RECALLED list is close in importance.

**Still blocked on Ajay, now five days overdue.** BFSI pipeline access for Stage
0, which gates B, C, E and the `sigma_resid` number for the corpus-size rule.
Unchanged since 17 August and not substitutable by any work I can do.

## 2026-08-23

**Scope.** Status check after a two-day gap, then repair of two integrity
defects found by that check. A parallel session had committed `4e8de3c` on 23
August touching `src/p2/ranking.py` and the ledger.

**What the other session did, and it was right to.** It lifted `CAUTION_K = 2.0`
out of an inline literal in `normalized_beta` into a named constant, on the
correct reasoning that a threshold deciding whether a reader is told to distrust
the reported direction is an analysis choice, not an implementation detail. It
also caught a citation failure of mine (below).

**DEFECT 1, in the incoming commit: a pre-registration claim that was not true.**
`ranking.py` carried the comment "Pre-registered constant, PREREG s2" while
`preregistration/PREREG.md` contained **zero** occurrences of `CAUTION_K`, and
that commit did not touch PREREG. Committed code asserting a pre-registration
that does not exist is precisely the failure this programme's thesis is about,
and a reviewer checking the claim would find it immediately.

Resolved by making the claim true rather than deleting it, since the underlying
instinct was correct: `CAUTION_K = 2.0` is now LOCKED in PREREG s2 with its
rationale and with the provenance of the discrepancy recorded openly. This is
legitimate rather than retrospective **only** because Gate D is unsigned and no
pooled result has been inspected, which is the condition PREREG s9 sets. Had
either been false, the honest action would have been to strike "pre-registered"
from the code instead. Stated in the PREREG entry itself so the reasoning is
auditable.

**DEFECT 2, mine: a citation reached committed source without reaching the
ledger.** The `normalized_beta` docstring I committed on 20 August cites
"(Fieller 1954)" as the authority for the ratio-of-normals argument that
justifies the paper's headline reporting convention. I never added it to the
ledger. It sat in committed source, in a RECALLED state, inside the
justification for a pre-registered analysis choice, and would have travelled
into the manuscript's methods section unchecked. The other session caught it by
eye and logged it RECALLED.

Verified today: E. C. Fieller, "Some Problems in Interval Estimation", *JRSS
Series B (Methodological)* 16(2):175-185, July 1954, DOI
10.1111/j.2517-6161.1954.tb00159.x, confirmed against the Oxford Academic
record and corroborated by the Wiley DOI page and the JSTOR volume listing.
Upgraded to VERIFIED.

**The lesson is about scope and it is now enforced mechanically.** The ledger
rule was practised as "nothing enters a MANUSCRIPT until VERIFIED", treating
docstrings as outside the boundary. In this project the docstrings are where the
methodological arguments are actually written, so that boundary was wrong.
`scripts/check_citations.py` now extracts every arXiv ID and author-year
citation from `src/` and `scripts/` and fails if any is absent from the ledger,
and it is wired into `verify.sh`. Tested in both directions: passes on the
current tree, and catches a planted unledgered reference. Recorded as ledger
correction C6.

**Also added to `verify.sh`'s import-surface check.** `CAUTION_K == 2.0` is
pinned so a silent retune cannot change what a reader is told, and
`normalized_beta` is asserted exactly scale-invariant under
`beta -> c*beta, V -> c^2*V`. Both are one-line assertions on properties the
paper depends on and neither existed before.

**Attempted and not completed.** The EU AI Act primary-text retrieval
(Articles 11, 12, 13, 19, 26, 86, Annex III point 5, Annex IV, and the Article
113 application dates). One agent hit an API session limit mid-task and the
other failed to start. **Nothing from that attempt is recorded anywhere**, and
no partial legal text was retained, deliberately: a half-retrieved regulation is
worse than none. Reg (EU) 2024/1689 therefore remains the highest-risk
unverified item, unchanged from 21 August. The application-date question in
particular must be settled before the paper claims the Act applies to agentic
credit underwriting now.

**Unchanged and now seven days overdue.** BFSI pipeline access for Stage 0.

## 2026-08-23, second entry

**The AI Act obligations this paper is about are not in application, and will not
be until 2 December 2027.** Verified from EUR-Lex primary text. This is the
largest single finding since Gate A and it changes paragraph one.

**What happened.** Regulation (EU) 2026/1744, the "Digital Omnibus on AI",
adopted 8 July 2026, published in the OJ on 24 July 2026, in force 27 July 2026,
amended Article 113 of the AI Act. Its Article 1(40) replaces Article 113 third
paragraph point (c) so that Chapter III Sections 1, 2 and 3 apply from **2
December 2027** for Annex III high-risk systems and 2 August 2028 for Annex I.

Articles 11 (technical documentation), 12 (record-keeping) and 13 (transparency)
sit inside Chapter III Section 2, and Annex IV is operative only through Article
11(1). All of them are therefore deferred for a credit underwriting system.
Annex III point 5(b), creditworthiness, is itself unchanged and still captures
the BFSI pipeline.

**The brief is wrong and must be corrected.** `paper-2-agentic-attribution.md`
says "Agentic systems are the 2026 deployment story, the AI Act applies to them
now". False as of today for every provision this paper rests on. The repo
documents never made that claim, which is luck rather than discipline.

**This is a better position, not a worse one.** A conformity specification
published in 2026 for an obligation that bites in December 2027 arrives while it
can still be adopted, which is the entire point of the WS6 deliverable. And
Article 11(1) as amended now obliges the Commission to produce a simplified
Annex IV form for SMEs and SMCs which **does not yet exist**, so the deliverable
has a live target rather than a hypothetical one.

**Recital (40) is the strongest regulatory hook the programme has found, and it
belongs in all three papers.** The legislature's own stated reason for the
deferral, verbatim: "the delayed availability of standards, common
specifications, and alternative guidance and the delayed establishment of
national competent authorities lead to challenges that jeopardise the effective
entry into application of those obligations". The Union is saying on the record
that it could not bring the high-risk regime into application because the
apparatus for demonstrating conformity was not ready. P1 argues interpretability
evidence cannot support a conformity claim; P2 argues observability evidence does
not track causation; recital (40) is the regulator conceding the general point.
Cite as a recital: explanatory, non-binding, never as operative law.

**A trap now recorded in the ledger.** Regulation (EU) 2026/1744 has only four
articles. Recital (40) and Article 1 point (40) both exist and concern the same
subject. There is no "Article 40". The binding amendment is Article 1(40).

**Methodological note that cost nothing and would have cost a lot.** The first
search surfaced a law-firm briefing describing the deferral as a *proposal* with
formal adoption "expected in the coming weeks". It was published 27 May 2026 and
was accurate then. Had it been trusted rather than used only to locate the
instrument, the paper would have recorded a proposed change as unadopted, or the
old dates as current. Every secondary source on AI Act dates is now suspect
unless its publication date is checked against 24 July 2026.

**Written.** `docs/REGULATORY-BASIS.md`, the verbatim primary-text foundation for
WS6, with epistemic markers throughout and an explicit list of what is still not
retrieved. Ledger correction C7. Ledger rows added for 2024/1689 (PARTIALLY
VERIFIED) and 2026/1744 (VERIFIED).

**One load-bearing link needs a second pair of eyes.** That Articles 11, 12 and
13 sit inside Chapter III Section 2 was established by inspecting where the
Section headings fall in the consolidated text, not by direct quotation. The
whole framing depends on it. Flagged in REGULATORY-BASIS section 7 as a
two-minute check to do before the claim enters the manuscript.

**Still not retrieved, all load-bearing for WS6.** Article 12 in full, which is
the single most important provision for the deliverable, plus Articles 11, 13,
19, 26, 86 and Annex IV in full. EUR-Lex HTML truncates on retrieval, so these
need fetching in sections or from the PDF. Next block.

## 2026-08-23, third entry

**WS6 now has its full legal foundation.** Articles 11, 12, 13, 18(1), 19, 26, 86
and Annex IV retrieved complete and verbatim, plus recitals 71 and 171. Written
into `docs/REGULATORY-BASIS.md` sections 8 to 14. Article 12 was verified
character for character against the OJ original.

**Retrieval note worth keeping.** EUR-Lex is behind an AWS WAF challenge that
returns HTTP 202 and zero bytes of legal text to programmatic fetches, which is
why the earlier attempts truncated. The working route is the **Publications
Office Cellar repository**, EUR-Lex's official backing store, which serves the
identical consolidated document at
`https://publications.europa.eu/resource/celex/02024R1689-20260727`. Recorded so
the next session does not rediscover it.

**Four findings, and they are stronger than the original framing.**

1. **Article 12 is system-level and says so.** The unit of obligation is "the
   system", and the three purposes in 12(2) are risk identification, post-market
   monitoring and deployer monitoring. None is attribution of an output to an
   internal cause.

2. **For credit scoring there is no minimum log content at all.** Article 12(3),
   the only enumerated minimum, binds solely Annex III **point 1(a)**, remote
   biometric identification. Creditworthiness is point 5(b) and falls outside it.
   So for the BFSI pipeline the Regulation prescribes no minimum log content
   whatsoever, only that capability exist. Stronger than what the paper claimed.

3. **The Act has no vocabulary for agentic systems.** Across the six units that
   constitute the entire high-risk documentation and record-keeping package,
   "agent", "agentic", "multi-agent", "orchestration" and "reasoning" appear
   **zero times**. "tool" appears once, plural, meaning third-party development
   artefacts. "step" appears once, meaning a step in the **development process**.
   The only internal-component reference is Annex IV 2(c).

4. **The retention asymmetry is a factor of twenty.** Technical documentation is
   kept 10 years (Art. 18(1)); logs are kept 6 months (Arts. 19(1) and 26(6)).
   The static architecture description outlives the dynamic execution record
   twentyfold. If attribution needs the runtime record, the mandated evidence
   expires before litigation or market surveillance would reach it. Both
   retention duties are also limited to logs "to the extent such logs are under
   their control", which writes accountability diffusion into the duty itself.

**The sharpest single point found so far.** Article 86 gives an affected person
the right to "clear and meaningful explanations of the role of the AI system in
the decision-making procedure and the main elements of the decision taken". Two
limbs, and neither covers how the system produced its output. The duty-holder is
the **deployer**, whose evidentiary base is Article 13 instructions plus Article
12 logs, both system-level. **The right terminates at exactly the layer where
causal attribution would have to begin.** That is the paper's thesis stated in
the structure of the Regulation.

**Also relevant to BFSI specifically.** Articles 19(2) and 26(6) second
subparagraph fold a financial institution's AI Act log duty into its existing
financial-services record-keeping, whose granularity was never designed for
causal attribution over an agent trajectory.

**Three reviewer objections identified and answers drafted** in REGULATORY-BASIS
section 13, including one that needs more work: a reviewer may say Article 25
(AI value chain) is where the Act handles multi-component systems. Article 25 and
the Article 3 definitions are **not yet retrieved** and should be before the
manuscript. The answer is that allocating responsibility between actors is not
the same as producing evidence of which component caused an output, but it must
be met explicitly.

**Discipline note.** Two formulations are supported by the text and two are not.
Supported: the obligation is specified at system level, and neither Article 12
nor Annex IV requires records sufficient to attribute an output to a specific
component. Not supported and must not be written: that the Act "prohibits" or
"excludes" component-level logging, or that it "defines traceability as
system-level". The word "traceability" appears once in the entire Article and is
never defined in the Act.

**Still not retrieved:** Articles 25, 72, 74, 79(1) and the Article 3
definitions.

## 2026-08-25

**Blocked on two tool limits, so the day went to unblocked code.** Subagents hit
a weekly limit resetting 29 August, which stopped the Article 25 retrieval before
it produced anything usable. Nothing partial was kept. A direct fetch of the
Cellar URL also failed: it needs specific Accept headers the fetch tool cannot
send. Articles 25, 72, 74, 79(1) and the Article 3 definitions therefore remain
outstanding, and reviewer objection 3 in REGULATORY-BASIS section 13 stays
unanswered until then.

**WS5.3 closed, and it was a pre-registration compliance gap of the same class
as the CAUTION_K one.** PREREG s6 LOCKS two reports: the CR1 cluster-robust OLS
secondary specification, and VIFs. Both estimators existed in `analysis.py` and
were validated in `validate_analysis.py`. **Neither was ever called in
`dry_run.py`.** The locked specification was satisfied in the library and
unsatisfied in the analysis, which is exactly the failure this project already
caught once when the prereg locked a primary contrast that had never been
computed. Now wired into the H2 block: per-covariate VIFs flagged against the
6.11 level coverage was verified to, the CR1 OLS secondary with cluster and naive
standard errors side by side, and an explicit primary-versus-secondary agreement
line implementing the "if they disagree, state it in the abstract" clause.

**Two dishonest output lines caught in my own draft before shipping.** The first
version printed "this is why clustering by decision is not optional here"
directly underneath a measured `se_cluster / se_naive` ratio of **0.99**, a
number that flatly contradicts the sentence. The second printed a |z| of 0.29 for
an intercept that is structurally zero, because `y` is standardised within
decision, making it a ratio of two numerical zeros.

Both are now fixed to report what the numbers say. The clustering block reports
the ratio, states plainly that on this synthetic generator clustering barely
changes anything, and explains why that is a property of the generator rather
than evidence against clustering: this chain draws node covariates independently
and puts no decision-level random intercept into the attributor score, whereas
`validate_analysis.py`, whose generator does carry one, measures cluster coverage
0.95 against naive 0.35. Real traces resemble the second case. That is precisely
why PREREG locks clustering in advance instead of deciding it from a measured
ratio, and the block now says so. The intercept is reported as not identified.

Worth recording as a pattern: both defects were narration asserting a conclusion
the adjacent number did not support. Neither would have been caught by a test,
because the code was correct. They were caught by reading the output.

**Verified on the machine of record**, in an isolated temp directory so
`results/` was untouched: compiles, runs to exit 0, VIFs 1.04/1.07/1.05 all well
under 6.11, secondary rejects on verbosity at |z| = 16.68, primary and secondary
agree. Six new keys added to the `h2` block of `results/dry_run.json`.

**Tooling note.** The cloud sandbox's shell was unavailable for most of this
session (safety-classifier timeouts), so the candidate was tested through the
device bridge instead, in a scratch copy rather than the repo. The bridge cannot
delete files, so the scratch script was moved to `_to_delete/`, now gitignored
along with `_scratch_*`.

**Unchanged and now nine days overdue.** BFSI pipeline access.

## 2026-08-25, second entry

**WS1.7 closed, and it found a real defect in a pre-registered statistic.**

The task was "estimators correct where Y is not in {0,1}". The estimators are
correct. What is not correct is the quantity H4 ranks on.

**The defect.** `ME = TE_crn - DE` is an identity, not a split into non-negative
parts. H4 is a rank correlation on `mediated_share = |ME| / |TE_crn|`, and that
is a share only where `DE` and `TE_crn` point the same way. Where they oppose,
`|ME| = |TE - DE| > |TE|` and the ratio exceeds 1. Every SCM in the repo before
today had both paths pushing the same way, so the case had never been exercised.

It is not exotic. It is suppression, and it has a plain reading in an agent
pipeline: a retrieval that directly supports approval while causing a later
verification step to raise a flag.

**Derived by hand first, then measured.** On `y = w*a1 - (1-w)*a3` with w = 0.2,
q = 0.9: `TE_crn(1) = +0.30`, `DE(1) = -0.10`, `ME(1) = +0.40`, share = 4/3
exactly. Measured: `+0.3003`, `-0.1001`, `+0.4004`, share `1.3333`. All four
steps within Monte Carlo error, decomposition identity residual `5.55e-17`. The
estimators are right; the ratio on top of them is not.

**Why it matters for H4 specifically.** A pure mediator has `DE = 0` and scores
exactly 1.0, the maximum the quantity is meant to reach. A suppressed node scores
1.33 and outranks it. The raw ratio is unbounded above and grows as `|DE|` grows
in the opposing direction, so ranking on it puts suppression above pure mediation
and mixes two opposite mechanisms into one score.

**The fix, and why not a clamp.** `effects.mediated_share` forms a share only
where `sign(DE) == sign(TE_crn)` and `|DE| <= |TE_crn|`, returning NaN and a
suppressed flag otherwise. `ranking.h4_statistic` now returns
`(taus, n_dropped, n_total)` so H4 cannot be reported without its exclusion rate.
Clamping 1.33 to 1.0 would be the repair PREREG s4 forbids, and it would silently
merge suppression into pure mediation, which is the confusion the rule exists to
prevent. LOCKED in PREREG s2, derived in DERIVATIONS Part VI.

**A previously reported number was wrong, and this is the part worth flagging.**
The fix moved dry-run H4 from `tau_b = +0.698` to `+0.855`, with 80/240 nodes
(33.3%) now excluded, all inert, none suppressed. The old code assigned inert
nodes a share of **0.0**, which asserts their influence is entirely direct when
they have no influence at all. **A third of the nodes entering the previously
reported H4 carried a fabricated share.** Synthetic, so no live claim moves, but
the statistic would have met real traces in that state, where inert nodes and
opposing paths are both expected rather than exotic.

**Caught a call-site break before it shipped.** Changing `h4_statistic`'s return
to a tuple would have silently broken `validate_primary.py:122`, which unpacked a
bare array. Fixed, and given an assertion that the planted H4 design has zero
exclusions, so a future change to the generator or to `mediated_share` fails
loudly instead of quietly altering H4's population.

**Verified.** Eight edge cases on `mediated_share` (ordinary, pure mediator, pure
direct, both suppression forms, inert, the `|DE| == |TE|` boundary, vectorised),
`scripts/validate_suppression.py` added to `verify.sh`, full suite ALL GREEN with
eight validators.

**Pattern worth naming, third instance.** CAUTION_K claimed a pre-registration
that did not exist. WS5.3 had two LOCKED reports the chain never produced. This
one had a pre-registered statistic whose definition broke outside the regime
every existing test happened to sit in. In all three the code was correct and the
specification was not met. Tests do not catch this class; only reading the
specification against the analysis does.

**Unchanged and now eleven days overdue.** BFSI pipeline access.

## 2026-09-03

**Programme audit, requested by Ajay, and it found drift that neither of us had
named.** Today is 3 September. The August sprint's own arXiv date was 31 August
and passed three days ago with no manuscript in existence: the repository had no
`paper/`, no `configs/` and no `analysis/` directory. Two sessions ran past that
date without raising it.

**The shape of the drift.** Sprint days D1 to D4 and D8 executed close to plan.
From D5, 17 August, every remaining day required BFSI pipeline access that never
arrived. Work continued, and the work was real: estimator core, coupling theory,
mediation layer, statistics, pre-registration, citation sweep, verified EU AI Act
foundation, `verify.sh` green across eight validators. But all of it was the
unblocked residue rather than the critical path. For fourteen days the work
optimised what was reachable instead of confronting what was blocking. The brief
had anticipated exactly this and said the fallback must be invoked on a date and
not arrived at by drift. It was arrived at by drift.

**Two protocols we agreed and dropped.** `docs/DAILY.md` was made binding by
AUGUST-SPRINT s7, one entry per day; its last entry was D8 on 20 August, and the
D5 to D8 entry is itself marked "reconstructed from git log", which is the
failure the protocol existed to prevent. `RESEARCH_LOG.md` went nine days
unlogged. Both are mine and I raised neither.

**FALLBACK INVOKED, by Ajay, today.** Recorded in `preregistration/PREREG.md`
under a dated heading. PREREG s7 clause two is in force.

**The consequence is scope, not wording, and it is the part worth recording.**
H1 to H4 are hypotheses about a real observability record against real causal
effect. They are not testable without the live arm. Both abstracts drafted in
PREREG s8 open "We run it on a live regulated credit underwriting system" and
neither survives. So this is not a weaker version of the same paper; it is a
different paper, methods and theory and specification, publishing a
pre-registered experiment it does not run.

**The dry run was not promoted to a result, and the temptation to do it was
real.** `results/dry_run.json` carries `SYNTHETIC_NOT_RESULTS: true` and every
generator behind it is planted, so `tau_b = +0.855` is known by construction.
Reporting it as a finding would be circular and a reviewer would say so in one
line. A gate in this session's script asserts the guard flag is still present.

**What ships instead**, all built and validated already: the `TE_marg` versus
`TE_crn` distinction, the direct effect and decomposition identity, the coupling
construction and its measured degradation, the suppression result, the verified
regulatory basis including the deferral, and the Annex IV specification. A third
abstract was drafted and committed before any further writing, per rule 6.

**Two stale status documents corrected.** `docs/TODO.md` 0.11 and 6.1, and the
ledger row for Reg (EU) 2024/1689, all still read "not retrieved" for provisions
that were retrieved verbatim on 25 August. Same failure class as a locked
specification the analysis never satisfies, pointing the other way.

**Three missing convention directories created**, with the reason `configs/` is
empty written down rather than left to look like an omission.

**Next.** WS1.9 pytest and CI, then the remaining reachable workstream items,
then the manuscript. Target: P2 complete this week.

## 2026-09-04

**WS1.9 closed. `pytest` green from a clean checkout, 85 tests, wired into
`verify.sh` and into CI.** This was the last unblocked code item in the
repository.

**The part that is not coverage.** `tests/test_contracts.py` tests the direction
a unit test cannot. Four times this project has caught a defect in which the code
was correct and the specification was not met: CAUTION_K claiming a
pre-registration that did not exist; PREREG s6 locking two reports that lived in
`analysis.py`, were validated, and were never called by `dry_run.py`; a
pre-registered statistic that broke outside the regime its tests occupied; and
status documents asserting provisions were unretrieved nine days after they were
retrieved. No numeric validator catches that class, because nothing is wrong with
the numbers. The contract tests parse `dry_run.py` with `ast` and assert that
every LOCKED estimator is actually called, that every `validate_*.py` on disk is
wired into `verify.sh`, that the citation gate is present, that every results
file carries an env block, and that the fallback invocation is in the
pre-registration with its date.

**Two real defects the suite found while it was being written.**

First, `verify.sh` would have called bare `pytest`. A bare console script
resolves to whichever interpreter installed it, which need not be the `python3`
running the validators. It produced "No module named numpy" from a suite that
passes under `python3 -m pytest`. Now pinned to the same interpreter as
everything else in the file.

Second, and this is the better one: `validate_mediation.py` contains a comment
arguing that env fields must be recorded uniformly, because a fingerprint that
omits a field on some files cannot answer "same environment?", since an audit
reads an absent field as a third environment rather than as "not applicable".
The file then omits `seed`. It argued the principle and did not apply it to
itself. Now records `seed: None`, which is the true statement for a module that
draws no randomness. This moves that file's `env_hash` and no scientific number;
a gate in this session asserts exactly that, checking that `unsafe_executions`
is still 0 and that no other results file moved.

**One precondition pinned rather than left latent.** `analysis.vif` regresses
column j on the others without an intercept while scaling by a mean-centred total
sum of squares, so the ratio is a standard VIF only when the input columns are
already centred. `dry_run.py` satisfies this by z-scoring within decision. On
uncentred orthogonal indicators the same call returns 0.75, which is not a
variance inflation factor and would read as reassuring. The function is unchanged,
because on the data it is actually given it is correct and changing it would move
a committed number for no gain. The precondition is now a test, and a second test
asserts the analysis still standardises.

**Verified green three ways:** in place, from a clean `git archive` tree, and
from a subdirectory. `verify.sh` now prints ten lines.

**Next.** The manuscript. Sections 3 to 6 are written from `DERIVATIONS.md` and
are the parts that already exist in full.

**A defect in the shipping script, recorded because it is the same class.** The first
run of `ws19_session.sh` aborted, and its gates were wrong while the tests were
right. GATE 4 ran `pytest` immediately after patching `validate_mediation.py`
but BEFORE re-running it, so `results/validation_mediation.json` still held the
pre-patch env block with no `seed` key. The contract test reported that a
results file lacked a seed, which was true. GATE 6 then ran `verify.sh`, which
re-ran the validator, regenerated the artifact, and passed 85/85 in the same
transcript: `env_hash f0e8cb10e8d82826` at GATE 4, `f407d037b90aefde` at GATE 6.

The correct order is patch, then regenerate the artifacts the patch affects,
then test. The script tested first. A second flaw was found while fixing it: the
clean-checkout gate built its tree from `git archive HEAD`, which is the old
commit plus the new files, so it would have failed on the stale artifact even
after a correct regeneration. A clean-checkout check has to be built from what
is about to be committed, and it now archives the staged tree.

Worth naming because it is the third defect this week from the gap between where
something was tested and where it runs, after the zsh `#` comment producing five
junk files and `git log | grep -q` returning 141 under `pipefail` on the machine
of record while passing in the sandbox. The tests were not at fault in any of
the three. The harness around them was.

## 2026-09-04, second entry

**Manuscript started, and a novelty sweep found that its sharpest section was
claiming a known result.**

Sections 3 to 6 were written from `docs/DERIVATIONS.md`. Then the sweep that
should have run first ran, and section 6 did not survive it intact.

**The finding.** Section 6 presented as a result that `|ME|/|TE|` exceeds 1 when
the direct and mediated paths oppose. In mediation analysis that ratio is the
proportion mediated, the configuration is called **inconsistent mediation**, and
its instability is established in MacKinnon, Warsi and Dwyer (1995),
*Multivariate Behavioral Research* 30(1):41-62. Kenny's mediation resource states
verbatim that the measure "can be greater than one or even negative". A reviewer
who knows this literature rejects the claim in a line.

Both primary references were verified against four independent records each
before being written into the bibliography.

**What survives, and it is a better paper for the correction.** The inequality is
attributed. What stays ours is that a **pre-registered statistic in this project
ranked on a quantity the literature says not to compute when the denominator is
small**; that inconsistent mediation has a concrete reading in an agent pipeline,
namely a retrieval that supports approval while causing a later verification step
to flag; and that the response is exclusion with a mandatory reported rate rather
than a clamp. The framing is now that agent-attribution work has been built
without reference to fifty years of mediation methodology, and importing it
correctly is the contribution.

**Two further claims caught before they were written.** Common random numbers is
standard variance reduction (Law and Kelton) and the maximal-coupling bound
`1 - TV` is classical (Levin, Peres and Wilmer). Neither is claimed now; both are
cited. arXiv 2605.04732 uses CRN for rollout-based planning and was checked and
**cleared**: no coupling agreement probability, no quantile-versus-maximal
comparison, no attribution or mediation. It is cited as adjacent work.

The one thing left as ours in section 5 is the closed form for shared-`u`
quantile-coupling agreement and the measured gap, and it is stated with "we have
not found it stated for this purpose" rather than as a novelty claim, because a
search returning nothing is not proof of absence.

**Process failure worth recording.** The rule is "before any novelty claim,
search". The draft existed for a day before the search ran. Search before
drafting, not before submitting.

**IASEAI'27 policy, verified from the '26 documents and NOT yet from the '27
call:** double-anonymous review; preprints allowed before or during review but
"must not be linked or mentioned in the submission", so an arXiv post does not
conflict; 10 pages main text excluding references; mandatory template; archival
track requires at least 50% new technical content. **The '27 dates could not be
retrieved: the page is JavaScript-rendered and returns none.**

**Next.** Section 8 as an appendix from `REGULATORY-BASIS.md`, section 7 from the
pre-registration, then 1, 2, 9, 10, figures, and a red team.

## 2026-09-04, third entry

**The load-bearing legal link is no longer a reading.** `REGULATORY-BASIS.md` s7
step 2, the claim that Articles 11 to 13 sit inside Chapter III Section 2, was
marked STRUCTURAL and the whole deferral framing rested on it. Read off the
primary text today: Section 1 is classification and covers Articles 6 and 7,
**Section 2 is "Requirements for high-risk AI systems" and covers Articles 8 to
15**, Section 3 is obligations of providers and deployers and covers 16 to 26.
Articles 11, 12 and 13 are in Section 2. One weak inference remains and is marked
as such: that the OJ original carries the same Section structure as the
consolidated text, which follows from the scope of the amending act.

**Article 25 retrieved, and it strengthens the paper rather than threatening
it.** Reviewer objection 3 was that Article 25 is where the Act handles
multi-component systems, so Article 12 is the wrong provision to build on. With
the text in hand the objection answers itself. Article 25 allocates the legal
role of provider between actors and imposes duties of cooperation, documentation
"sufficient to assess compliance with the requirements laid down in Article 16",
information about "known limitations and failure modes", and targeted technical
access. Every obligation is about who is answerable and about enabling
compliance. None is about evidence of which component caused an output. The two
provisions do different work and the paper needs both.

**Article 3 definitions retrieved**, and (1) "AI system" is singular and
system-level throughout, so a pipeline of five tool-backed services and a model
is one AI system with one provider and one deployer. The Act has no vocabulary
for the internal components this paper measures, and that is now supported by
the definition itself rather than by its absence elsewhere.

**Still not retrieved: Articles 72, 74(1) and 79(1).** Every route tried today is
recorded in the new s18 with its outcome, so the next attempt starts from the
failures. The only route that returns article text truncates mid Article 26,
which is why 25 came back and 72 did not. Until they are read, section 8 must not
characterise what Article 12(2)'s cross-references require.

**IASEAI'27 dates, provided by Ajay from the official programme page.** Main
conference **9 to 10 February 2027**, workshop days 11 to 12 February, UNESCO
House, Paris. Submission portal **opens 18 September 2026**; **paper, workshop and
model-policy proposals close 2 October 2026**; reviews shared 2 November; optional
author responses 4 November; decisions 6 November. Talk proposals and statements
of interest remain open on a rolling basis to 9 and 15 January 2027.

**That is 28 days, not seven.** The arXiv date next week is Ajay's own choice and
stands, but the conference deadline is 2 October, which leaves roughly three weeks
after the preprint for the anonymised, template-formatted, 10-page version. The
plan should stop treating the two as one deadline.

**A gate defect fixed rather than carried.** In the previous session GATE 5 ran
pytest, printed nothing at all, and passed. A gate that reports success without
producing evidence is worse than no gate. It now requires a summary line matching
a test count and fails closed if there is none.

## 2026-09-04, fourth entry

**The draft is complete.** Sections 1, 2, 7, 8, 9 and 10 written, plus Appendix A,
the traceability specification. Zero stubs. 17 pages: 11 main text, 2 references,
4 appendix. Every citation resolves in both directions and every arXiv id in the
bibliography is ledger-backed.

**The appendix is derived, not proposed, and that is the design decision worth
recording.** Twelve requirements, each of which is a precondition for one of this
paper's own estimands to be computable from a filed record. Nothing is in it
because it sounded prudent. Four conformance levels, and the one that matters is
L1 to L2: L1, a reconstructable trajectory, is what observability stacks already
deliver; L2, counterfactual replayability, is what causal attribution requires,
and no provision of the Regulation asks for it. R5, the keyed-randomness
requirement, is singled out as free at design time and impossible to add
afterwards.

**Section 8 makes the argument the retrievals earned.** Description versus record
and general versus per-instance; the logging duty bounded above by two
system-level purposes now that Articles 72 and 79(1) have been read; no minimum
log content at all for Annex III point 5; the factor-of-twenty retention
asymmetry with neither actor obliged to hold the whole trace; Article 74's
escalation ladder reaching source code without ever reaching an execution trace;
and Article 79(6)(b) offering one whole system against one whole Section as the
finest granularity available. Then the two Commission instruments that do not yet
exist, one of which has a deadline of 2 September 2027.

**The introduction positions against CAR in paragraph one**, as the brief
required, and uses the concessions in that work's own text: a marginal total
effect, the direct effect left as a refinement, and mocked tools.

**Page budget, stated now rather than discovered later.** Main text is 11 pages
against IASEAI's 10-page limit. arXiv has no limit, so this binds only the
conference version, and the trim is a bounded named task.

**Still to do before arXiv:** figures, of which the paper currently has none; a
red team in a fresh session per standing rule 7; the final ledger pass; and the
anonymised, template-formatted variant for 2 October.

## 2026-09-05

**P1 is on arXiv and has been since 13 August.** Verified against the listing:
arXiv 2608.13754, *Explanation Multiplicity*, Ajay Pravin Mahale, Hochschule
Trier, v1, cs.AI. It shipped 28 days ahead of its own 10 September target. The
audit of 3 September recorded P1 as unknown and the decisions of 4 September
slipped it to 20 September. Both were wrong, and wrong because this chat asked a
question instead of opening a folder that sat one level above one already
connected. Recorded because it is the same failure this project has been
cataloguing all week, committed by me.

**P2 now cites P1 twice**, which is the cross-citation the brief said makes these
a programme rather than two unrelated papers: at the ablation-operator argument,
where the circuit-level finding that a filed claim flips across 73.2% of
specification pairs is the same class of analytic choice one level down; and in
the introduction, framing them as one argument at two levels of abstraction, with
the note that the two failures are independent because evidence could be
perfectly stable and still track the wrong thing.

**Full pre-arXiv citation sweep under the citation-verify standard**, which holds
that a prior verified row does not carry over and VERIFIED means fetched this
session with every field confirmed. Fourteen arXiv identifiers, twelve confirmed,
**four discrepancies, two not re-verifiable**.

The one that mattered: **2606.04990's author order was wrong**, in the
bibliography and in this ledger. Zhangkai Wu sat in position 3 and belongs in
position 7, after Zequn Sun. It had survived three weeks and two earlier sweeps,
because every earlier check confirmed that the paper existed rather than that our
transcription of it was right. That is a different question and only the second
one protects a bibliography.

Two discrepancies were things we did not have rather than things we had wrong,
and both strengthen the citations: AttriGuard is **"Accepted by USENIX Security
2026"** and Yadav et al. carries a **Reinforcement Learning Journal** reference.
Both were being cited as bare preprints.

One is now **DISPUTED**: Who&When's "PMLR v267, pp. 76583-76599". PMLR v267 is
confirmed to be ICML 2025, but the paper was not locatable in the index this
session and arXiv's Comments field says only "camera-ready". The page range is
marked pending re-confirmation in `refs.bib`.

**Two entries could not be re-verified and are named rather than assumed.**
2606.09692 and 2605.09168 both return no machine-readable text to the fetch tool,
attempted twice each. Both carry August VERIFIED rows with URLs. Per the rule, a
blocked fetch is not routed around and the state is not upgraded, so **this
bibliography must not be described as fully checked** until someone opens those
two abstract pages in a browser. Two minutes.

**A humanizer pass found nothing, and nothing was invented to look busy.** Zero
hits across AI vocabulary, copula avoidance, superficial participial phrases,
negative parallelism, filler, hedging stacks, em dashes and curly quotes. All
eleven three-item lists are real enumerations: step types, hypothesis labels, a
verbatim quote from Article 74. The prose was written under the standing rules
that already ban em-dashes and hedging, so those patterns were never introduced.

**A Unicode audit found the sources are pure ASCII**, with no invisible or
provenance-marking characters in `main.tex`, `refs.bib` or the `Makefile`.

**A BibTeX lesson worth keeping.** The first attempt at these corrections put
explanatory `%` comments inside the entries. BibTeX has no in-entry comment
syntax and skipped every entry that followed one, silently dropping 46 citations.
Comments belong between entries, where BibTeX ignores them. A gate now fails on
any `%` inside an entry.
