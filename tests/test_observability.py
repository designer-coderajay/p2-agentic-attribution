"""observability.py: the attributor set and the tie-corrected rank correlation.

The attributor set is a provenance claim, not a design choice. `recency` was CUT
in the WS3.3 audit because no shipping tool ranks trace steps by it, and keeping
it would have been the strawman the audit existed to prevent."""
import numpy as np
import pytest

from p2.observability import ATTRIBUTORS, kendall_tau_b, rank_desc


class TestAttributorProvenance:
    def test_there_are_exactly_three(self):
        assert len(ATTRIBUTORS) == 3, [a.name for a in ATTRIBUTORS]

    def test_every_attributor_traces_to_a_shipping_tool(self):
        for a in ATTRIBUTORS:
            assert a.provenance.startswith("VERIFIED"), a.name

    def test_recency_was_cut_and_stays_cut(self):
        """It survives only as a covariate in the H2 regression. If it reappears
        as an attributor the provenance audit has been undone."""
        assert "recency" not in {a.name for a in ATTRIBUTORS}


class TestRankDesc:
    def test_highest_value_gets_rank_one(self):
        assert rank_desc([3.0, 1.0, 2.0]).tolist() == [1.0, 3.0, 2.0]

    def test_ties_share_an_average_rank(self):
        """Durations and token counts tie constantly in real traces and
        terminal_action is binary, so tie handling is load-bearing."""
        assert rank_desc([1.0, 1.0, 0.0]).tolist() == [1.5, 1.5, 3.0]

    def test_all_tied_gives_one_shared_rank(self):
        assert rank_desc([2.0, 2.0, 2.0]).tolist() == [2.0, 2.0, 2.0]


class TestKendallTauB:
    def test_perfect_concordance(self):
        assert kendall_tau_b([1, 2, 3, 4], [10, 20, 30, 40]) == pytest.approx(1.0)

    def test_perfect_discordance(self):
        assert kendall_tau_b([1, 2, 3, 4], [40, 30, 20, 10]) == pytest.approx(-1.0)

    def test_tie_correction_is_applied(self):
        """Without the tie correction this returns something other than 1.0."""
        assert kendall_tau_b([1, 1, 2, 2], [5, 5, 9, 9]) == pytest.approx(1.0)

    def test_fewer_than_two_points_is_nan(self):
        assert np.isnan(kendall_tau_b([1.0], [1.0]))

    def test_constant_vector_is_nan_not_zero(self):
        """A constant vector has no ranking. Returning 0 would read as 'measured
        no association' when nothing was measurable."""
        assert np.isnan(kendall_tau_b([1, 1, 1, 1], [1, 2, 3, 4]))

    def test_is_symmetric(self):
        rng = np.random.default_rng(20260903)
        x, y = rng.normal(size=30), rng.normal(size=30)
        assert kendall_tau_b(x, y) == pytest.approx(kendall_tau_b(y, x))
