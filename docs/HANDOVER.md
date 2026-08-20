# P2 Handover, 17 August 2026 (sprint day 5 of 19)

**Update, 20 August 2026 (Cowork session, Gate D day).** The first OPEN item
below is fixed and validated; struck through in place rather than deleted, so
this doc still reads as the record of what handover looked like. See
`docs/DAILY.md` D8 entry, `docs/RESEARCH_LOG.md` 2026-08-20, and
`docs/DERIVATIONS.md` Part V for the full account. The second OPEN item and the
BLOCKED section are unchanged: still blocked on BFSI pipeline access, now
overdue since 17 August, four days as of this update.

Repo: github.com/designer-coderajay/p2-agentic-attribution (PRIVATE)
Local: ~/Desktop/"Evidential Validity of AI Explanations"/p2-agentic-attribution
One command to check health: `./verify.sh` -> must print ALL GREEN (7 suites).

## Read in this order
1. docs/POSITIONING.md   why the paper changed shape. The brief is stale.
2. preregistration/PREREG.md   what is LOCKED and what is a RULE.
3. docs/DERIVATIONS.md   every closed form, in four parts.
4. docs/DAILY.md, docs/TODO.md   state and open items.

## What the paper is now
The original brief claimed the technical literature had not answered agentic
causal attribution. That is FALSE as of June 2026. Four of eight contributions
are occupied by others. Four survive:
  1. DE/ME decomposition via common random numbers (CAR leaves it as future work)
  2. observability rank comparison with a bias decomposition (nobody)
  3. live side-effecting tools in a regulated decision (CAR and CausalFlow
     both declare this out of scope)
  4. the Annex IV record-keeping conversion (nobody)

## Built and validated (all against closed forms, both machines bit-identical)
  scm.py         synthetic SCMs, CRN keyed by (seed, step, replicate)
  effects.py     TE_marg, TE_crn, DE (Pearl natural direct), ME. 16/16 within
                 4 MC sigma of hand derivations
  coupling.py    quantile and maximal coupling, both matching closed form
  mediation.py   4 purity classes; EFFECTFUL_UNSAFE never executes (20 checks)
  observability.py  3 attributors, all provenance VERIFIED; tau_b with ties
  analysis.py    CR1 cluster-robust sandwich; coverage 0.95 vs naive 0.35
  ranking.py     Plackett-Luce by Newton, joint Wald, H3, H4, separation guard,
                 normalised-beta reporting (2026-08-20)
  dry_run.py     end-to-end chain on synthetic data

## Bugs the validation caught before any of them reached a result
  marginal arm re-rolled the prefix before k          60 sigma
  claimed shared-u coupling attains 1 - TV            215 sigma
  coverage generator had no decision-level variance   test tested nothing
  Wilson lower bound at k=0 was 2.17e-19 not 0        every zero H3 cell wrong
  prereg locked an unimplemented primary contrast     uncomputable
  |z| > 40 separation rule                            fired on healthy fits
  dry run generator was degenerate                    +172, p = 1e-98
  ratio-to-causal convention, div-by-near-zero         -2.29 / -26.7, unbounded

## OPEN, blocking Gate D (20 August)
  - ~~PREREG s2 ratio convention anchors on the causal coefficient, which the
    hypotheses predict is near zero. Anchor must change.~~ FIXED 2026-08-20:
    report beta / ||beta||_2 with a decision-level bootstrap CI. Validated
    (invariance to the PL scale ambiguity, exact; bounded as beta_causal -> 0,
    demonstrated on this repo's own dry-run numbers where the old convention
    produced -26.7). `verify.sh` ALL GREEN with the fix. Primary contrast
    (the joint Wald test) unaffected, confirmed algebraically invariant.
  - Power rule needs sigma_resid from Stage 0. RULE is locked, number is not.
    STILL OPEN, needs Stage 0, see BLOCKED below.

## BLOCKED on pipeline access, overdue since 17 August
  Gates B (cost), C (replay floor), E (harness working). All three need the
  BFSI pipeline with its five MCP servers. PREREG s7 fallback: if Stage 0
  cannot run, the paper reports synthetic and sampler-level results only and
  states the absent live arm in the abstract. Weaker paper, still a real one.

## Working rules that were earned, not assumed
  - Hand derivation BEFORE code. Every bug above was caught this way.
  - Nothing is committed until ./verify.sh prints ALL GREEN.
  - Patches carry an assert so they fail loudly instead of silently no-oping.
  - No citation enters the bibliography unless VERIFIED in the ledger with a
    checked date. Anything still RECALLED on 30 August is cut, not chased.
  - Synthetic output is labelled NOT RESULTS in console and JSON.
