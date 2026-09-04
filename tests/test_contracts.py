"""Specification-compliance tests.

WHY THIS FILE EXISTS. This project has now caught the same failure four times,
and not one instance would have been caught by a test of correctness:

  1. CAUTION_K claimed a pre-registration that did not exist.
  2. PREREG s6 LOCKED two reports (VIFs, the CR1 secondary) that lived in
     `analysis.py`, were validated in `validate_analysis.py`, and were never
     called by `dry_run.py`. The specification was satisfied in the library and
     unsatisfied in the analysis.
  3. WS1.7 had a pre-registered statistic whose definition broke outside the
     regime every existing test happened to occupy.
  4. `docs/TODO.md` and the citation ledger said provisions were unretrieved that
     had been retrieved verbatim nine days earlier.

In all four the code was correct and the specification was not met. Unit tests do
not catch that class, because there is nothing wrong with the code. These tests
check the OTHER direction: that what is LOCKED is actually reached by the
analysis, that every validator is actually wired, and that guards that make
numbers honest are actually present.
"""
import ast
import glob
import json
import os

import pytest


def _read(path):
    """Read a file and close it. `pytest.ini` sets filterwarnings=error, so a
    leaked handle is a test failure here, which is the correct setting for a repo
    whose central claim is that its artifacts are reproducible."""
    with open(path, encoding="utf-8") as fh:
        return fh.read()


def _read_json(path):
    with open(path, encoding="utf-8") as fh:
        return json.load(fh)


def _calls_in(path):
    """Every function name called anywhere in a module, via AST rather than grep
    so that a name inside a comment or a docstring does not count as a call."""
    tree = ast.parse(_read(path))
    names = set()
    for node in ast.walk(tree):
        if isinstance(node, ast.Call):
            f = node.func
            if isinstance(f, ast.Name):
                names.add(f.id)
            elif isinstance(f, ast.Attribute):
                names.add(f.attr)
    return names


@pytest.fixture(scope="module")
def dry_run_calls(repo_root):
    return _calls_in(os.path.join(repo_root, "scripts", "dry_run.py"))


class TestLockedReportsAreActuallyProduced:
    """PREREG s6 LOCKS these. Locking a report that the chain never runs is the
    failure this class exists to prevent."""

    @pytest.mark.parametrize("fn,clause", [
        ("vif", "PREREG s6: VIFs reported"),
        ("ols_cluster", "PREREG s6: CR1 cluster-robust OLS secondary"),
        ("joint_wald", "PREREG s6: joint 2-df Wald primary contrast"),
        ("normalized_beta", "PREREG s2: direction on the unit sphere"),
        ("mediated_share", "PREREG s2: share formed only where it is a share"),
        ("h4_statistic", "PREREG s1: H4"),
        ("bootstrap_over_decisions", "PREREG s6: bootstrap over decisions"),
    ])
    def test_analysis_calls_the_locked_estimator(self, dry_run_calls, fn, clause):
        assert fn in dry_run_calls, (
            f"{clause}: `{fn}` is LOCKED in the pre-registration but "
            f"scripts/dry_run.py never calls it. The specification would be "
            f"satisfied in the library and unsatisfied in the analysis."
        )

    def test_analysis_imports_them_from_the_library(self, repo_root):
        src = _read(os.path.join(repo_root, "scripts", "dry_run.py"))
        for fn in ["vif", "ols_cluster", "mediated_share"]:
            assert fn in src


class TestPreconditionsTheAnalysisMustSatisfy:
    def test_covariates_are_standardised_before_vif(self, repo_root):
        """`vif` is a standard variance inflation factor only on mean-centred
        columns (see test_analysis.py). The analysis z-scores within decision.
        If that standardisation is ever removed the reported VIFs silently stop
        being VIFs."""
        src = _read(os.path.join(repo_root, "scripts", "dry_run.py"))
        assert "v.mean()" in src and "v.std()" in src, (
            "the z-score helper feeding the design matrix is gone; reported VIFs "
            "are no longer variance inflation factors"
        )


class TestEveryValidatorIsWired:
    def test_verify_sh_runs_every_validator_that_exists(self, repo_root):
        """A validator that exists but is not in verify.sh is a validator nobody
        runs. verify.sh printing ALL GREEN must mean all of them."""
        verify = _read(os.path.join(repo_root, "verify.sh"))
        found = sorted(
            os.path.basename(p)[:-3]
            for p in glob.glob(os.path.join(repo_root, "scripts", "validate_*.py"))
        )
        assert found, "no validators found at all"
        missing = [v for v in found if v not in verify]
        assert not missing, f"validators not wired into verify.sh: {missing}"

    def test_the_citation_gate_is_wired(self, repo_root):
        verify = _read(os.path.join(repo_root, "verify.sh"))
        assert "check_citations" in verify, (
            "the mechanical citation gate is not in verify.sh; a reference can "
            "reach committed source without entering the ledger, which is how "
            "(Fieller 1954) sat unledgered for three days"
        )


class TestGuardsThatKeepNumbersHonest:
    def test_dry_run_output_is_marked_as_not_results(self, repo_root):
        """Under the invoked fallback the temptation to promote these numbers to
        findings is real. Every generator behind them is planted, so the values
        are known by construction and reporting them would be circular."""
        p = os.path.join(repo_root, "results", "dry_run.json")
        d = _read_json(p)
        assert d.get("SYNTHETIC_NOT_RESULTS") is True

    def test_every_result_file_records_its_environment(self, repo_root):
        """Standing rule 10: config, seed and environment hash for every reported
        figure."""
        for p in glob.glob(os.path.join(repo_root, "results", "*.json")):
            d = _read_json(p)
            env = d.get("env", {})
            name = os.path.basename(p)
            assert "env_hash" in env, f"{name} has no env_hash"
            assert "numpy" in env, f"{name} has no numpy version"
            assert "seed" in env, (
                f"{name} omits `seed`. validate_mediation.py already argues the "
                f"principle in its own comment: a fingerprint that omits a field "
                f"on some files cannot answer 'same environment?', because an "
                f"audit reads an absent field as a third environment rather than "
                f"as 'not applicable'. A deterministic module records seed=None."
            )

    def test_results_were_produced_under_one_pinned_environment(self, repo_root):
        """`results/` once held files from three different environments because
        requirements.txt carried a floor rather than a pin."""
        versions = set()
        for p in glob.glob(os.path.join(repo_root, "results", "*.json")):
            env = _read_json(p).get("env", {})
            if "numpy" in env:
                versions.add(env["numpy"])
        assert len(versions) <= 1, f"results/ mixes numpy versions: {sorted(versions)}"

    def test_numpy_is_pinned_exactly_not_floored(self, repo_root):
        """Comments in requirements.txt narrate the old `numpy>=1.26` floor and
        why it was wrong, so only the requirement lines are read."""
        lines = [ln.split("#", 1)[0].strip()
                 for ln in _read(os.path.join(repo_root, "requirements.txt")).splitlines()]
        reqs = [ln for ln in lines if ln]
        numpy_reqs = [ln for ln in reqs if ln.lower().startswith("numpy")]
        assert numpy_reqs, "numpy is not pinned at all"
        for ln in numpy_reqs:
            assert "==" in ln, f"a floor is not a pin: {ln!r}"
            assert ">=" not in ln, f"a floor is not a pin: {ln!r}"


class TestPreRegistrationIntegrity:
    def test_the_fallback_invocation_is_recorded_with_a_date(self, repo_root):
        """Invoked 2026-09-03. The date is the point: the brief required it be
        invoked deliberately rather than arrived at by drift."""
        prereg = _read(os.path.join(repo_root, "preregistration", "PREREG.md"))
        assert "FALLBACK INVOKED, 2026-09-03" in prereg

    def test_the_delivered_abstract_does_not_claim_a_live_run(self, repo_root):
        """Both original abstracts open 'We run it on a live regulated credit
        underwriting system'. Under the fallback that claim is false."""
        prereg = _read(os.path.join(repo_root, "preregistration", "PREREG.md"))
        marker = "ADDED 2026-09-03, and this is the one the paper ships with."
        assert marker in prereg
        delivered = prereg.split(marker, 1)[1]
        assert "was not available in the study window" in delivered
