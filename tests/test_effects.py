"""effects.mediated_share, the quantity H4 ranks on.

These are the eight boundary cases from WS1.7. The estimators were already
correct; the reporting quantity built on them was not, and no test existed that
entered the suppression regime. That is why this file exists.
"""
import numpy as np
import pytest

from p2.effects import SHARE_TE_FLOOR, mediated_share


def test_share_floor_is_pre_registered_value():
    """PREREG s2 LOCKS this. A silent retune changes which nodes are reported as
    having no defined share, so it is pinned rather than trusted."""
    assert SHARE_TE_FLOOR == 1e-9


@pytest.mark.parametrize(
    "name,te,de,want_share,want_suppressed",
    [
        ("ordinary partial mediation", 1.0, 0.4, 0.6, False),
        ("pure mediator, DE = 0", 0.5, 0.0, 1.0, False),
        ("pure direct, DE == TE", 0.5, 0.5, 0.0, False),
        ("suppression, opposite signs", 0.30, -0.10, None, True),
        ("suppression, |DE| > |TE|", 0.2, 0.5, None, True),
        ("negative TE, ordinary", -1.0, -0.4, 0.6, False),
        ("inert node, TE = 0", 0.0, 0.0, None, False),
        ("boundary, |DE| == |TE|", 0.5, 0.5, 0.0, False),
    ],
)
def test_share_boundaries(name, te, de, want_share, want_suppressed):
    share, suppressed = mediated_share([te], [de])
    if want_share is None:
        assert np.isnan(share[0]), f"{name}: expected NaN, got {share[0]}"
    else:
        assert share[0] == pytest.approx(want_share, abs=1e-12), name
    assert bool(suppressed[0]) is want_suppressed, name


def test_inert_node_is_not_counted_as_suppression():
    """An inert node has no share, but it is not a sign violation. Counting it as
    suppression would inflate the rate the paper reports."""
    share, suppressed = mediated_share([0.0], [0.0])
    assert np.isnan(share[0])
    assert not suppressed[0]


def test_suppressed_share_would_have_exceeded_one():
    """The defect, stated as a test: the raw ratio on the WS1.7 SCM is 4/3, which
    outranks a pure mediator's 1.0 and inverts H4's ordering."""
    te, de = 0.30, -0.10
    raw = abs(te - de) / abs(te)
    assert raw == pytest.approx(4.0 / 3.0, rel=1e-12)
    assert raw > 1.0
    share, suppressed = mediated_share([te], [de])
    assert np.isnan(share[0]) and suppressed[0]


def test_vectorised_matches_elementwise():
    te = [1.0, 0.5, 0.30, 0.0, -1.0]
    de = [0.4, 0.0, -0.10, 0.0, -0.4]
    s_vec, sup_vec = mediated_share(te, de)
    for i in range(len(te)):
        s_one, sup_one = mediated_share([te[i]], [de[i]])
        assert np.isnan(s_vec[i]) == np.isnan(s_one[0])
        if not np.isnan(s_vec[i]):
            assert s_vec[i] == pytest.approx(s_one[0], abs=1e-15)
        assert bool(sup_vec[i]) == bool(sup_one[0])


def test_decomposition_identity_holds_exactly():
    """ME = TE_crn - DE is an identity, not an approximation."""
    rng = np.random.default_rng(20260903)
    te = rng.normal(size=500)
    de = rng.normal(size=500)
    me = te - de
    assert np.abs(me - (te - de)).max() == 0.0
