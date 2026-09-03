# analysis

Notebooks that read `results/` and produce figures, per the repository
convention.

As of 2026-09-03 every figure in the paper is produced by a script under
`scripts/` writing to `results/`, with config, seed and environment hash
recorded in the output JSON. No notebook stands between a result and a figure,
which is stricter than the convention requires rather than looser: there is no
hand-run cell whose state is not captured.

Figure generation for the manuscript lands here as `make_figures.py` when the
figures are cut.
