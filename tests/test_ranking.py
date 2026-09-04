"""ranking.py: the primary contrast, the reporting convention, and H4's guard."""
import numpy as np
import pytest

from p2.ranking import (
    CAUTION_K,
    chi2_sf_df2,
    h4_statistic,
    joint_wald,
    normalized_beta,
    wilson,
)


def test_caution_k_is_pre_registered_value():
    """PREREG s2 LOCKS 2.0. Pinned so a retune cannot silently change what a
    reader is told about how far to trust the reported direction."""
    assert CAUTION_K == 2.0


class TestChiSquare:
    def test_exact_at_zero(self):
        assert chi2_sf_df2(0.0) == pytest.approx(1.0)

    def test_textbook_critical_value(self):
        assert chi2_sf_df2(5.991464547) == pytest.approx(0.05, abs=1e-6)

    def test_is_exponential_not_approximation(self):
        for x in [0.5, 2.0, 7.3, 20.0]:
            assert chi2_sf_df2(x) == pytest.approx(float(np.exp(-x / 2)), rel=1e-15)

    def test_monotone_decreasing(self):
        xs = np.linspace(0, 30, 200)
        vals = [chi2_sf_df2(x) for x in xs]
        assert all(b <= a for a, b in zip(vals, vals[1:]))


class TestJointWald:
    def test_exact_on_diagonal(self):
        W, q, p = joint_wald(np.array([0.0, 1.0, 1.0]), np.diag([1.0, 0.25, 0.25]), (1, 2))
        assert q == 2
        assert W == pytest.approx(8.0, abs=1e-12)
        assert p == pytest.approx(chi2_sf_df2(8.0), rel=1e-15)

    def test_zero_coefficients_give_zero_statistic(self):
        W, q, p = joint_wald(np.zeros(3), np.eye(3), (1, 2))
        assert W == pytest.approx(0.0, abs=1e-15)
        assert p == pytest.approx(1.0)

    def test_is_joint_not_two_marginals(self):
        """A 2-df test carries no multiplicity correction. Correlated coefficients
        must not be treated as two independent z-tests, so the statistic has to
        use the off-diagonal covariance."""
        beta = np.array([0.0, 1.0, 1.0])
        V_indep = np.diag([1.0, 1.0, 1.0])
        V_corr = np.array([[1.0, 0, 0], [0, 1.0, 0.9], [0, 0.9, 1.0]])
        W_i, _, _ = joint_wald(beta, V_indep, (1, 2))
        W_c, _, _ = joint_wald(beta, V_corr, (1, 2))
        assert W_i != pytest.approx(W_c)


class TestNormalizedBeta:
    b = np.array([-0.029, 0.067, 0.780])
    V = np.diag([0.0055, 0.0092, 0.0098])

    def test_returns_unit_vector(self):
        g, se, note = normalized_beta(self.b, self.V)
        assert np.linalg.norm(g) == pytest.approx(1.0, abs=1e-12)

    def test_scale_invariance_is_exact(self):
        """The Plackett-Luce noise scale is unidentified: the fit recovers c*beta
        for unknown c > 0. The reported direction must not move with c."""
        g1, _, _ = normalized_beta(self.b, self.V)
        g2, _, _ = normalized_beta(7.5 * self.b, 56.25 * self.V)
        assert np.allclose(g1, g2, atol=1e-14)

    def test_standard_errors_are_scale_invariant_too(self):
        _, se1, _ = normalized_beta(self.b, self.V)
        _, se2, _ = normalized_beta(7.5 * self.b, 56.25 * self.V)
        assert np.allclose(se1, se2, atol=1e-12)

    def test_zero_vector_is_reported_not_smoothed(self):
        g, se, note = normalized_beta(np.zeros(3), np.eye(3))
        assert np.isnan(g).all() and np.isnan(se).all()
        assert "zero vector" in note

    def test_caution_note_fires_when_direction_is_poorly_determined(self):
        small = np.array([1e-4, 1e-4, 1e-4])
        _, _, note = normalized_beta(small, np.eye(3))
        assert note != "" and "caution" in note

    def test_no_caution_note_on_a_healthy_fit(self):
        _, _, note = normalized_beta(self.b, self.V)
        assert note == ""

    def test_does_not_divide_by_the_causal_coefficient(self):
        """The regression this replaces. beta_causal = -0.029 gave a 'ratio to
        causal' of -26.7 for verbosity. The direction convention must stay bounded
        when that coefficient is near zero, which is exactly what H1 and H2
        predict."""
        g, _, _ = normalized_beta(self.b, self.V)
        assert np.abs(g).max() <= 1.0 + 1e-12
        assert g[2] == pytest.approx(0.9957, abs=5e-4)


class TestH4Contract:
    def test_returns_three_tuple(self):
        """A bare array here silently broke validate_primary.py once. The
        exclusion rate must be impossible to drop on the floor."""
        out = h4_statistic([[1.0, 0.5, 0.2]], [[1, 2, 3]], [[3, 2, 1]])
        assert isinstance(out, tuple) and len(out) == 3
        taus, n_dropped, n_total = out
        assert isinstance(taus, np.ndarray)
        assert n_dropped == 0 and n_total == 3

    def test_nan_shares_are_excluded_and_counted(self):
        shares = [[1.0, np.nan, 0.2, np.nan]]
        taus, n_dropped, n_total = h4_statistic(shares, [[1, 2, 3, 4]], [[4, 3, 2, 1]])
        assert n_total == 4
        assert n_dropped == 2

    def test_a_decision_with_fewer_than_two_usable_nodes_yields_no_tau(self):
        taus, n_dropped, n_total = h4_statistic([[1.0, np.nan, np.nan]],
                                                [[1, 2, 3]], [[3, 2, 1]])
        assert taus.size == 0
        assert n_dropped == 2 and n_total == 3


class TestWilson:
    def test_zero_cell_lower_bound_is_exactly_zero(self):
        """Floating-point cancellation left ~2e-19 here, putting a correct
        estimate of a zero rate outside its own interval. Every zero cell in the
        H3 grid would have been wrong."""
        lo, hi = wilson(0, 100)
        assert lo == 0.0
        assert 0.0 < hi < 1.0

    def test_full_cell_upper_bound_is_exactly_one(self):
        lo, hi = wilson(100, 100)
        assert hi == 1.0
        assert 0.0 < lo < 1.0

    def test_interval_contains_the_point_estimate(self):
        for k in range(0, 51):
            lo, hi = wilson(k, 50)
            assert lo <= k / 50 <= hi, f"k={k}"

    def test_empty_sample_is_nan_not_an_exception(self):
        lo, hi = wilson(0, 0)
        assert np.isnan(lo) and np.isnan(hi)
