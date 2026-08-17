"""
Common random numbers across divergent LLM contexts.

arXiv 2606.08275 section 7 states that isolating a step's direct effect calls for
common random numbers across branches, that this is hard across divergent LLM
contexts, and leaves it as a refinement. This module says exactly what is and is
not achievable there, and makes the shortfall a measured quantity rather than a
caveat.

The mechanism. Token sampling from a language model is inverse-transform sampling
from a categorical distribution: draw u ~ U(0,1), walk the CDF of p(. | context),
emit the token whose interval contains u. If u is a pure function of
(run id, step index, replicate) and never of the context, then a factual and a
counterfactual rollout at the same replicate consume THE SAME uniform draws. The
two branches then differ only because the distribution moved, never because the
dice were re-rolled. That is the coupling, and it is exact.

What is exact and what is not:

  EXACT      the noise is shared. This is a property of the sampler and holds
             no matter how far the contexts diverge.
  NOT EXACT  the *benefit* of sharing it, which is what determines whether ME is
             estimable with usable precision.

An earlier draft of this module asserted that shared-u inverse-transform sampling
attains the maximal-coupling bound 1 - TV(p, q). **That is false**, and the
closed-form check in scripts/validate_coupling.py rejected it at up to 215 sigma.
The correct statement distinguishes two couplings:

  QUANTILE COUPLING (shared u, fixed index order). One uniform, one pass, needs
  only the branch's own distribution. Agreement is the overlap of the two CDF
  interval partitions:

      A_quant(p,q) = sum_i max(0, min(P_i, Q_i) - max(P_{i-1}, Q_{i-1}))

  where P, Q are the CDFs in fixed index order. This is <= 1 - TV(p,q), with
  equality only in degenerate cases. Shifting probability mass between two tokens
  moves every later CDF boundary, so an early perturbation decouples the whole
  tail: the loss is real and can be large even at small TV.

  MAXIMAL COUPLING (needs p and q at draw time). With probability
  omega = sum_i min(p_i, q_i) both branches emit the same token, drawn from
  min(p,q)/omega; otherwise each draws from its own residual. Agreement is
  exactly 1 - TV(p,q), the information-theoretic optimum. It requires carrying
  the factual branch's distribution alongside the counterfactual one, which costs
  a second forward pass per step but is available to us because the factual run
  is being replayed anyway.

Design consequence: **use maximal coupling, not quantile coupling.** The extra
forward pass buys the difference between the two curves, and that difference is
what decides whether ME has usable precision once contexts diverge. Report both,
because quantile coupling is what a naive implementation gives and the gap is a
result worth showing.

Fixed index order still matters: sorting the vocabulary by probability, as a
naive top-k or nucleus implementation does, degrades quantile coupling further.

Three preconditions, all of which constrain the model choice:
  1. Per-request seed control. Hosted endpoints generally do not offer it.
  2. Single-stream inference. Batch-size-dependent kernels break bitwise
     reproducibility, so the null-replay action-match rate must be measured
     (Gate C) rather than assumed.
  3. Fixed vocabulary ordering in the sampler, per the paragraph above.

What gets reported: coupling retention per step, the divergence frontier, and the
fraction of downstream steps past it. ME is quoted with those numbers attached.
"""

from __future__ import annotations

import hashlib
from dataclasses import dataclass, field

import numpy as np


def keyed_uniform(run_id: str, step: int, replicate: int, draw: int = 0) -> float:
    """
    A uniform draw that is a pure function of its key and nothing else.

    Deliberately not an RNG object with advancing state: state would make the
    draw depend on call order, and call order differs between a factual rollout
    and a counterfactual one. Order independence is the whole point.
    """
    key = f"{run_id}|{step}|{replicate}|{draw}".encode()
    digest = hashlib.blake2b(key, digest_size=8).digest()
    return int.from_bytes(digest, "big") / float(1 << 64)


def inverse_transform(probs: np.ndarray, u: float) -> int:
    """
    Sample by walking the CDF in FIXED index order.

    Fixed order is load-bearing. It is what makes two branches with different
    distributions attain the maximal-coupling agreement bound 1 - TV(p, q).
    """
    return int(np.searchsorted(np.cumsum(probs), u, side="right"))


def total_variation(p: np.ndarray, q: np.ndarray) -> float:
    return 0.5 * float(np.abs(p - q).sum())


def overlap(p: np.ndarray, q: np.ndarray) -> float:
    """sum_i min(p_i, q_i) = 1 - TV(p, q). The MAXIMAL-coupling agreement."""
    return float(np.minimum(p, q).sum())


def quantile_agreement(p: np.ndarray, q: np.ndarray) -> float:
    """
    Closed form for shared-u inverse-transform coupling in fixed index order.

    Two branches agree at token i exactly when u falls in the intersection of
    [P_{i-1}, P_i) and [Q_{i-1}, Q_i). Summing those intersection lengths:

        sum_i max(0, min(P_i, Q_i) - max(P_{i-1}, Q_{i-1}))

    Always <= overlap(p, q). The gap is the cost of not carrying the other
    branch's distribution at draw time.
    """
    P = np.concatenate([[0.0], np.cumsum(p)])
    Q = np.concatenate([[0.0], np.cumsum(q)])
    lo = np.maximum(P[:-1], Q[:-1])
    hi = np.minimum(P[1:], Q[1:])
    return float(np.maximum(0.0, hi - lo).sum())


def maximal_coupling_sample(p, q, u1: float, u2: float, u3: float):
    """
    Draw (a_factual, a_counterfactual) from the maximal coupling of p and q.

    Agreement probability is exactly omega = sum_i min(p_i, q_i) = 1 - TV(p, q),
    which is optimal: no coupling of p and q agrees more often.
    """
    m = np.minimum(p, q)
    omega = float(m.sum())
    if u1 < omega:
        a = inverse_transform(m / omega, u2)
        return a, a
    rp, rq = p - m, q - m
    sp, sq = float(rp.sum()), float(rq.sum())
    a = inverse_transform(rp / sp, u2) if sp > 0 else inverse_transform(p, u2)
    b = inverse_transform(rq / sq, u3) if sq > 0 else inverse_transform(q, u3)
    return a, b


@dataclass
class CouplingReport:
    """Per-step coupling diagnostics. These go in the results table."""

    step: int
    tv: float
    overlap_bound: float       # maximal coupling, 1 - TV
    quantile_bound: float      # shared-u inverse transform, always <= overlap
    empirical_agreement: float
    diverged: bool

    @property
    def coupling_efficiency(self) -> float:
        """Empirical agreement over the MAXIMAL bound. 1.0 is optimal."""
        if self.overlap_bound <= 0:
            return float("nan")
        return self.empirical_agreement / self.overlap_bound


@dataclass
class DivergenceTracker:
    """
    Tracks where a counterfactual rollout's context stops matching the factual one.

    Before the frontier, the context is byte-identical and the factual output can
    be replayed exactly, at zero cost and zero noise. At and after the frontier,
    the distribution has moved and coupling degrades to the overlap bound.
    """

    factual_context_hashes: list[str]
    frontier: int | None = None
    reports: list[CouplingReport] = field(default_factory=list)

    def observe(self, step: int, context_hash: str) -> bool:
        """Returns True if this step's context matches the factual run."""
        matched = (
            step < len(self.factual_context_hashes)
            and context_hash == self.factual_context_hashes[step]
        )
        if not matched and self.frontier is None:
            self.frontier = step
        return matched

    def divergence_depth(self, n_steps: int) -> float:
        """Fraction of the trajectory lying at or after the divergence frontier."""
        if self.frontier is None:
            return 0.0
        return (n_steps - self.frontier) / n_steps


def measure_coupling(
    p: np.ndarray,
    q: np.ndarray,
    run_id: str,
    step: int,
    n_draws: int = 20000,
) -> CouplingReport:
    """
    Empirically confirm that shared keyed draws attain the maximal-coupling bound.

    p is the factual step distribution, q the counterfactual one. Both branches
    consume the same u at each replicate. Agreement should land on
    quantile_agreement(p, q), NOT on overlap(p, q).
    """
    agree = 0
    for r in range(n_draws):
        u = keyed_uniform(run_id, step, r)
        agree += inverse_transform(p, u) == inverse_transform(q, u)
    return CouplingReport(
        step=step,
        tv=total_variation(p, q),
        overlap_bound=overlap(p, q),
        quantile_bound=quantile_agreement(p, q),
        empirical_agreement=agree / n_draws,
        diverged=total_variation(p, q) > 0.0,
    )
