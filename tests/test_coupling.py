"""coupling.py: the construction that keeps the direct effect estimable once
contexts diverge. Maximal coupling was LOCKED over quantile coupling on a
measured factor-of-nine gap, so both bounds are tested, not assumed."""
import numpy as np
import pytest

from p2.coupling import (
    inverse_transform,
    keyed_uniform,
    maximal_coupling_sample,
    overlap,
    quantile_agreement,
    total_variation,
)


def _probs(rng, k=6):
    p = rng.random(k) + 0.05
    return p / p.sum()


class TestKeyedUniform:
    def test_is_a_pure_function_of_its_key(self):
        a = keyed_uniform("run-a", 3, 7, 0)
        b = keyed_uniform("run-a", 3, 7, 0)
        assert a == b

    def test_is_order_independent(self):
        """The whole point: a factual rollout and a counterfactual one call these
        in different orders, and an advancing RNG would make the draw depend on
        that order."""
        forward = [keyed_uniform("r", s, 1) for s in range(10)]
        backward = [keyed_uniform("r", s, 1) for s in reversed(range(10))][::-1]
        assert forward == backward

    def test_distinct_keys_give_distinct_draws(self):
        vals = {keyed_uniform("r", s, rep) for s in range(20) for rep in range(20)}
        assert len(vals) == 400

    def test_draws_lie_in_the_unit_interval(self):
        vals = [keyed_uniform("r", s, 1) for s in range(500)]
        assert all(0.0 <= v < 1.0 for v in vals)


class TestCouplingBounds:
    def test_overlap_is_one_minus_total_variation(self):
        rng = np.random.default_rng(20260903)
        for _ in range(50):
            p, q = _probs(rng), _probs(rng)
            assert overlap(p, q) == pytest.approx(1.0 - total_variation(p, q), abs=1e-12)

    def test_quantile_agreement_never_beats_maximal(self):
        """The locked choice rests on this inequality holding always, not on
        average."""
        rng = np.random.default_rng(11)
        for _ in range(200):
            p, q = _probs(rng), _probs(rng)
            assert quantile_agreement(p, q) <= overlap(p, q) + 1e-12

    def test_identical_distributions_couple_perfectly(self):
        rng = np.random.default_rng(5)
        p = _probs(rng)
        assert overlap(p, p) == pytest.approx(1.0, abs=1e-12)
        assert total_variation(p, p) == pytest.approx(0.0, abs=1e-12)

    def test_disjoint_supports_never_agree(self):
        p = np.array([1.0, 0.0, 0.0])
        q = np.array([0.0, 0.0, 1.0])
        assert overlap(p, q) == pytest.approx(0.0)
        assert total_variation(p, q) == pytest.approx(1.0)


class TestMaximalCoupling:
    def test_agreement_rate_attains_the_bound(self):
        """Monte Carlo against the closed form. Seed pinned."""
        rng = np.random.default_rng(20260903)
        p, q = _probs(rng), _probs(rng)
        omega = overlap(p, q)
        n = 40000
        u = rng.random((n, 3))
        agree = sum(1 for i in range(n)
                    if (lambda ab: ab[0] == ab[1])(maximal_coupling_sample(p, q, *u[i])))
        assert agree / n == pytest.approx(omega, abs=0.01)

    def test_marginals_are_preserved(self):
        rng = np.random.default_rng(7)
        p, q = _probs(rng, 4), _probs(rng, 4)
        n = 40000
        u = rng.random((n, 3))
        draws = [maximal_coupling_sample(p, q, *u[i]) for i in range(n)]
        pa = np.bincount([d[0] for d in draws], minlength=4) / n
        qb = np.bincount([d[1] for d in draws], minlength=4) / n
        assert np.allclose(pa, p, atol=0.012)
        assert np.allclose(qb, q, atol=0.012)


class TestInverseTransform:
    def test_walks_the_cdf_in_fixed_index_order(self):
        p = np.array([0.2, 0.3, 0.5])
        assert inverse_transform(p, 0.0) == 0
        assert inverse_transform(p, 0.19) == 0
        assert inverse_transform(p, 0.21) == 1
        assert inverse_transform(p, 0.51) == 2
        assert inverse_transform(p, 0.999) == 2
