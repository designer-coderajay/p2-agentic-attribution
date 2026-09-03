# P2 manuscript outline

**Scope set by the fallback invocation of 2026-09-03.** This is a methods,
theory and specification paper. It publishes a pre-registered experiment and
does not run it. It reports no H1 to H4 result and promotes no dry-run number to
a finding.

Target: arXiv. Venue after posting: FAccT 2027 or a systems venue, per brief s11.
**Not ICLR.**

## Abstract

As drafted in `preregistration/PREREG.md` s8, entry three. The absent live arm
appears in the abstract, not in a limitations section, per standing rule 8.

## 1. Introduction

Opens on the deferral. Recital (40) of Reg (EU) 2026/1744, verbatim and cited as
a recital, explanatory and non-binding: the Union's own record that the apparatus
for demonstrating conformity was not ready. Then the gap: no agreed protocol for
execution provenance (survey 2606.04990 sec 6.3 Table 5, graded "Proposed").
Then the contribution list.

Differentiation from CAR (2606.08275) in paragraph one, not in related work.
CAR concedes in print that the direct effect is left as a refinement and that
real tools with side effects are out of scope. That concession is the opening.

## 2. Setting and estimands

Trajectory, node types, decision `Y`. The five-operator intervention algebra
adopted verbatim from CAR, with the explicit statement that it is adopted rather
than improved because modifying an instrument under test is a free rejection.

## 3. Two total effects, and why the distinction is the crux

`TE_marg` versus `TE_crn`. The planted partial-mediation SCM on which `TE_marg`
cannot separate an inert step from the decisive one while `TE_crn` returns
exactly zero for inert steps. `DERIVATIONS.md` parts I and II.

## 4. The direct effect and the decomposition

Natural direct effect under a pinned downstream. Pearl (2001) primary, Pearl
(2009) 2nd ed. sec 4.5.4 and 4.5.5 as the textbook treatment, Robins and
Greenland (1992) for priority. `ME = TE_crn - DE`, identity residual to machine
precision.

## 5. Coupling

Maximal versus quantile coupling, the factor-of-nine gap, the closed form for
degradation as contexts diverge, and batch invariance as the real replay
precondition (He and Thinking Machines Lab 2025). This is where Gate C actually
bites, and it is a serving-stack constraint, not a seed-control one.

## 6. The mediated share is not a share

The suppression result. Hand derivation on `y = w*a1 - (1-w)*a3`, measured
agreement, and the demonstration that the raw ratio is unbounded above and ranks
a suppressed node above a pure mediator. Why the fix is exclusion and not a
clamp: clamping is the repair the pre-registration forbids and merges two
opposite mechanisms into one score.

**This is the paper's sharpest single result and it should be a numbered
proposition, not a subsection.**

## 7. The pre-registered experiment

H1 to H4, the primary contrast, the estimators, the corpus rule, the exclusion
rules. Published in full. State plainly that it is not run here and why.

## 8. Annex IV traceability specification

The standalone deliverable. Grounded in the verbatim provisions in
`REGULATORY-BASIS.md`. Targets the Commission's forthcoming simplified Annex IV
form for SMEs and SMCs, which does not yet exist.

## 9. Limitations

Short, because the principal one is in the abstract. Remaining: single planted
generator family for validation, no live arm, no Shapley interaction arm
(prior art, cite CAR), coupling measured but not against a language model.

## 10. Related work

CAR, CausalFlow, AgenTracer, Liao, the survey, AttriGuard, CausalArmor,
2606.09692. All VERIFIED in the ledger. Nothing RECALLED enters the bibliography.

---

## Writing order, 3 to 10 September

Sections 3, 4, 5 and 6 first: they are written from `DERIVATIONS.md` and are the
parts that already exist in full. Then 8 from `REGULATORY-BASIS.md`. Then 7 from
`PREREG.md`. Then 1, 2, 9, 10. Abstract is already written and does not get
rewritten at the end to match a result, because there is no result to match.
