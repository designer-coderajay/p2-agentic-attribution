# configs

One file per experimental specification, no hardcoded parameters, per the
repository convention in `PROJECT-SETUP.md`.

**Empty by design as of 2026-09-03, and the reason is recorded rather than
hidden.** Every configuration this directory was to hold parameterises a run
against the live BFSI pipeline: Stage 0 null replay, Stage 1 screening, Stage 2
sweep. The pre-registered fallback was invoked on 3 September 2026 and those
stages are not run in this paper. The specifications that would populate this
directory are fully determined by `preregistration/PREREG.md` sections 3, 4, 5
and 6, which is the point of a pre-registration: the configs are derivable from
the locked document by anyone continuing the work.

The synthetic generators used for estimator validation take their parameters
inline in `scripts/validate_*.py` with the seed and environment hash written into
`results/`, which is sufficient for reproduction and is verified by `verify.sh`.
