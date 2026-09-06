# arXiv submission metadata

Everything the submission form asks for, so that nothing is typed from memory at
the point of upload. Generated alongside the tarball; regenerate the tarball with
`make -C paper arxiv`.

## Files to upload

`paper/p2-arxiv-submission.tar.gz`, containing exactly:

```
main.tex
main.bbl
figures/fig1_two_total_effects.pdf
figures/fig2_coupling_gap.pdf
```

arXiv does not run bibtex, which is why `main.bbl` is in the package and
`refs.bib` is not. The package is test-compiled by the Makefile with three
`pdflatex` passes and no bibtex, the way arXiv compiles it, and the build fails
if any reference or citation is unresolved. Do **not** upload `main.pdf`: arXiv
compiles the source itself and a submitted PDF alongside TeX source is rejected.

## Title

```
Causal Attribution for Agentic Decisions: Estimators, Coupling, and a Traceability Specification
```

## Authors

```
Ajay Pravin Mahale
```

## Abstract

Paste the block below. It is 1916 characters, inside arXiv's 1920-character
limit, and it is the manuscript's abstract with LaTeX markup removed, not a
separate text. If you edit one, regenerate the other.

```
A provider of a high-risk AI system must keep records that make a decision traceable, and for agentic systems it has not been established what those records must contain for post-hoc causal attribution to be possible. We give the estimator framework and then the conditions under which it fails. We separate the marginal total effect that prior work measures from a common-random-numbers total effect that isolates a step's own contribution, add the natural direct effect under a pinned downstream, and check the estimators against hand derivations. Both estimands then fail, in the same direction. Under the marginal estimand a causally inert step has the identical total effect to the decisive one on every run of our planted chain, an algebraic identity and not a coincidence at one draw. Under common random numbers the decisive step returns exactly zero on the runs where the executing step flips, about one in ten, while its direct effect there is 0.25 and it demonstrably acts; an exact zero does not certify that a step did nothing, and we put that here rather than in the limitations. We derive the coupling that keeps the direct effect estimable once contexts diverge, with a closed form for its degradation, and show that the mediated share on which a natural ranking is built is not a share under suppression: where the direct and mediated paths oppose, it exceeds one and ranks a suppressed component above a pure mediator. We publish the discrepancy experiment's pre-registration rather than a result, because the live pipeline it requires was not available in the study window. We contribute the traceability specification such a filing would need, against a gap the Act's calendar opens: Article 86's right to an explanation has applied since 2 August 2026, while the Article 12 logging and Annex IV documentation that could evidence one were deferred to 2 December 2027 by Regulation (EU) 2026/1744.
```

## Categories

**Recommended primary: `cs.LG`.** The load-bearing contributions are estimator
and statistical: two total-effect estimands and a separation result between them,
a closed form for coupling agreement, a proportion-mediated instability, and a
Plackett-Luce specification. The closest prior work, arXiv:2606.08275, is
`cs.LG`.

**Cross-list: `cs.AI` and `cs.CY`.** `cs.AI` for the agentic-systems framing;
`cs.CY` for the regulatory analysis in Section 8 and Appendix A.

The alternative is `cs.AI` primary, which is where the companion paper
arXiv:2608.13754 sits, and there is a real argument for programme consistency.
Either is defensible. Pick one and keep the cross-lists.

## Comments field

```
23 pages, 2 figures, 2 tables, 3 propositions with proofs. Pre-registered
discrepancy experiment published in full and not run; no empirical result is
claimed. Code, validators, derivations and a traceability specification at
https://github.com/designer-coderajay/p2-agentic-attribution
```

The repository was made public on 6 September 2026 and CI is green on the base
commit, both jobs, so the URL resolves and the badge it carries is not decorative.
Re-check that the link opens before pasting it: a link to a 404 is worse than no
link.

## ACM class / MSC class

Leave both blank. Plausible codes exist (`I.2.11`, `K.4.1`, `62D20`) but we have
not verified their current definitions against the ACM CCS and MSC2020 schemes,
and a wrong classification code is a small avoidable error in a paper whose
argument is about unverified evidence. Blank is honest; guessed is not.

## Licence

`arXiv.org perpetual, non-exclusive license` is sufficient and is the default.
The repository is MIT, which does not constrain the choice. CC BY 4.0 is also
fine if wider reuse is wanted; it cannot be changed after announcement, so decide
before submitting.

## Journal reference / DOI

Leave blank. This is a preprint with no venue.

## After the identifier is assigned

Two follow-ups, each as its own commit:

1. `CITATION.cff`: fill in the commented `preferred-citation` block with the
   arXiv identifier and URL.
2. `README.md`: add the arXiv link beside the paper line at the top.

Do not backdate either into the release commit. The identifier does not exist
until arXiv assigns it, and a commit that claims otherwise is a small lie in a
repository whose whole argument is about provenance.
