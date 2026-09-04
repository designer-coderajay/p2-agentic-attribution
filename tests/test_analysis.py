"""analysis.py: the secondary specification and the diagnostics PREREG s6 LOCKS
as reportable. These existed and were validated for three weeks while the
analysis never called them, which is the failure test_contracts.py guards."""
import numpy as np
import pytest

from p2.analysis import bootstrap_over_decisions, ols_cluster, vif


class TestOlsCluster:
    def test_recovers_coefficients_on_a_noiseless_design(self):
        rng = np.random.default_rng(20260903)
        X = np.column_stack([np.ones(200), rng.normal(size=200), rng.normal(size=200)])
        truth = np.array([0.5, -1.25, 2.0])
        y = X @ truth
        beta, se_cl, se_naive = ols_cluster(X, y, np.arange(200) // 10)
        assert np.allclose(beta, truth, atol=1e-10)

    def test_clustering_matters_when_a_decision_level_intercept_exists(self):
        """With a decision-level random intercept the naive standard error is too
        small. That is the whole reason clustering is pre-registered rather than
        chosen from a measured ratio."""
        rng = np.random.default_rng(4)
        G, per = 40, 10
        clusters = np.repeat(np.arange(G), per)
        shock = rng.normal(scale=2.0, size=G)[clusters]
        x = rng.normal(size=G * per)
        X = np.column_stack([np.ones(G * per), x])
        y = 0.3 * x + shock + rng.normal(scale=0.1, size=G * per)
        _, se_cl, se_naive = ols_cluster(X, y, clusters)
        assert se_cl[0] > se_naive[0]

    def test_returns_three_arrays_of_matching_width(self):
        rng = np.random.default_rng(1)
        X = rng.normal(size=(60, 3))
        y = rng.normal(size=60)
        beta, se_cl, se_naive = ols_cluster(X, y, np.arange(60) // 6)
        assert beta.shape == se_cl.shape == se_naive.shape == (3,)


class TestVif:
    def test_orthogonal_centred_columns_have_vif_one(self):
        rng = np.random.default_rng(20260903)
        A = np.linalg.qr(rng.normal(size=(400, 3)))[0]      # orthonormal columns
        X = A - A.mean(axis=0)                               # and mean-centred
        out = np.asarray(vif(X), float)
        assert np.allclose(out, 1.0, atol=1e-3)

    def test_input_must_be_mean_centred_for_the_value_to_be_a_vif(self):
        """PRECONDITION, pinned rather than assumed. `vif` regresses column j on
        the others WITHOUT an intercept but scales by a mean-centred total sum of
        squares, so the ratio is a standard VIF only when the columns are already
        centred. The analysis satisfies this by z-scoring within decision
        (`scripts/dry_run.py`), and `test_contracts.py` asserts it still does.

        On uncentred orthogonal indicators the same call returns 0.75, which is
        not a variance inflation factor and would read as reassuring. This test
        exists so that the precondition is visible rather than latent."""
        uncentred = np.column_stack([[1, 0, 0, 0], [0, 1, 0, 0], [0, 0, 1, 0]]).astype(float)
        out = np.asarray(vif(uncentred), float)
        assert np.allclose(out, 0.75, atol=1e-9)
        assert (out < 1.0).all()

        centred = uncentred - uncentred.mean(axis=0)
        out_c = np.asarray(vif(centred), float)
        assert (out_c >= 1.0 - 1e-9).all()

    def test_collinear_columns_inflate(self):
        rng = np.random.default_rng(9)
        a = rng.normal(size=300)
        b = a + rng.normal(scale=0.01, size=300)
        X = np.column_stack([a, b, rng.normal(size=300)])
        out = np.asarray(vif(X), float)
        assert out[0] > 100 and out[1] > 100
        assert out[2] < 2

    def test_single_column_is_one(self):
        out = np.asarray(vif(np.random.default_rng(0).normal(size=(50, 1))), float)
        assert out[0] == pytest.approx(1.0)


class TestBootstrapOverDecisions:
    def test_is_deterministic_under_a_pinned_seed(self):
        v = np.linspace(0, 1, 40)
        a = bootstrap_over_decisions(v, n_boot=500, seed=20260903)
        b = bootstrap_over_decisions(v, n_boot=500, seed=20260903)
        assert a == b

    def test_different_seeds_move_the_interval_but_not_the_point(self):
        v = np.linspace(0, 1, 40)
        m1, lo1, hi1 = bootstrap_over_decisions(v, n_boot=500, seed=1)
        m2, lo2, hi2 = bootstrap_over_decisions(v, n_boot=500, seed=2)
        assert m1 == pytest.approx(m2)
        assert (lo1, hi1) != (lo2, hi2)

    def test_interval_brackets_the_mean(self):
        rng = np.random.default_rng(3)
        v = rng.normal(loc=0.4, scale=0.2, size=120)
        m, lo, hi = bootstrap_over_decisions(v, n_boot=2000, seed=0)
        assert lo < m < hi
