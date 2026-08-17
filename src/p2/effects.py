"""
Causal effect estimators over agent trajectories.

Quantities, per step k, all conditional on one factual run (a_fact, u_fact, y_fact):

  TE_marg(k)  total effect, downstream re-decides under FRESH noise.
              This is the estimand of arXiv 2606.08275.
  TE_crn(k)   total effect, downstream re-decides under FACTUAL noise.
              A unit-level counterfactual. Common random numbers across branches.
  DE(k)       direct effect. Downstream pinned to factual actions. Pearl's natural
              direct effect (Pearl, Causality, CUP 2nd ed. 2009).
  ME(k)       TE_crn(k) - DE(k).

CAR section 7 states that isolating a step's direct effect calls for common random
numbers across branches, which is hard across divergent LLM contexts, and leaves it
as a refinement. This module is that refinement, plus the CRN total effect, which
removes the run-forward confound CAR resolves heuristically with its
point-of-commitment rule.

Nothing here knows what a language model is. It talks to a Runner protocol, so the
synthetic SCM and the live LangGraph pipeline are interchangeable.
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import Protocol, Sequence

import numpy as np


class Runner(Protocol):
    @property
    def n_steps(self) -> int: ...
    def run(self, crn, replicate, forced=None, pinned=None): ...
    def sample_action(self, k, prefix, crn, replicate) -> int: ...


@dataclass
class Effect:
    estimate: float
    lo: float
    hi: float
    n: int
    se: float

    @property
    def excludes_zero(self) -> bool:
        return (self.lo > 0.0) or (self.hi < 0.0)


@dataclass
class StepAttribution:
    step: int
    kind: str
    te_marg: Effect
    te_crn: Effect
    de: Effect
    me: Effect
    pin_plausibility: float
    change_rate: float

    @property
    def mediated_share(self) -> float:
        if abs(self.te_crn.estimate) < 1e-9:
            return float("nan")
        return abs(self.me.estimate) / abs(self.te_crn.estimate)


def _ci(values: np.ndarray, baseline: float, alpha: float, rng) -> Effect:
    """
    Percentile bootstrap on mean(values) - baseline.

    The baseline is the single factual outcome, not a sample, so only the
    interventional arm is resampled. On a real system with replay nondeterminism
    the factual arm is also a sample; that case is handled by passing null
    intervention replicates in as `values` and setting baseline to their mean.
    """
    v = np.asarray(values, dtype=float)
    if v.size == 0:
        return Effect(float("nan"), float("nan"), float("nan"), 0, float("nan"))
    point = float(v.mean() - baseline)
    se = float(v.std(ddof=1) / np.sqrt(v.size)) if v.size > 1 else float("nan")
    idx = rng.integers(0, v.size, size=(2000, v.size))
    draws = v[idx].mean(axis=1) - baseline
    lo, hi = np.quantile(draws, [alpha / 2.0, 1.0 - alpha / 2.0])
    return Effect(point, float(lo), float(hi), int(v.size), se)


def estimate_effects(
    runner: Runner,
    crn,
    factual_actions: Sequence[int],
    factual_outcome: float,
    factual_replicate: int = 0,
    n_rollouts: int = 4000,
    pin_probes: int = 400,
    alpha: float = 0.05,
    seed: int = 0,
) -> list[StepAttribution]:
    rng = np.random.default_rng(seed)
    n = runner.n_steps
    kinds = getattr(runner, "kinds", ["step"] * n)
    out: list[StepAttribution] = []

    for k in range(n):
        prefix = tuple(factual_actions[:k])
        marg, crn_vals, de_vals = [], [], []
        changed = 0
        pin_scores: list[float] = []

        for r in range(1, n_rollouts + 1):
            # do_resample at k: redraw from the unchanged policy at the factual prefix
            alt = runner.sample_action(k, prefix, crn, replicate=r)
            if alt != factual_actions[k]:
                changed += 1

            # marginal total effect: prefix [0,k) HELD at factual actions, step k
            # forced, and only the steps after k re-decide under fresh noise. The
            # prefix pin is not optional: without it the estimator also re-rolls
            # upstream steps and the effect is no longer attributable to k. This is
            # the estimand of arXiv 2606.08275 section 4.
            held_prefix = {j: int(factual_actions[j]) for j in range(k)}
            marg.append(
                runner.run(crn, replicate=r, forced={k: alt}, pinned=held_prefix).outcome
            )

            # CRN total effect: downstream re-decides under the factual noise stream
            crn_traj = runner.run(crn, replicate=factual_replicate, forced={k: alt})
            crn_vals.append(crn_traj.outcome)

            # direct effect: downstream pinned to factual actions
            pinned = {j: int(factual_actions[j]) for j in range(k + 1, n)}
            de_vals.append(
                runner.run(crn, replicate=factual_replicate, forced={k: alt}, pinned=pinned).outcome
            )

            # pin plausibility: would the policy have produced the pinned action
            # given the counterfactual prefix it now finds itself in?
            if pinned and r <= pin_probes:
                cf = list(crn_traj.actions())
                for j in range(k + 1, n):
                    hits = sum(
                        runner.sample_action(j, tuple(cf[:j]), crn, replicate=10_000 + r * 131 + m)
                        == factual_actions[j]
                        for m in range(32)
                    )
                    pin_scores.append(hits / 32.0)

        te_marg = _ci(np.array(marg), factual_outcome, alpha, rng)
        te_crn = _ci(np.array(crn_vals), factual_outcome, alpha, rng)
        de = _ci(np.array(de_vals), factual_outcome, alpha, rng)
        # ME interval is bootstrapped on the PAIRED difference: TE_crn and DE share
        # the same forced draw at k on each replicate and are strongly correlated.
        # Treating them as independent would inflate the interval.
        me = _ci(np.array(crn_vals) - np.array(de_vals), 0.0, alpha, rng)

        out.append(
            StepAttribution(
                step=k,
                kind=kinds[k],
                te_marg=te_marg,
                te_crn=te_crn,
                de=de,
                me=me,
                pin_plausibility=float(np.mean(pin_scores)) if pin_scores else float("nan"),
                change_rate=changed / n_rollouts,
            )
        )
    return out


def point_of_commitment(attrs: Sequence[StepAttribution], arm: str = "te_marg") -> int | None:
    """
    CAR's locus rule: the LATEST step whose total-effect interval still excludes
    zero. Reproduced in intent, not improved. We compare against this instrument,
    and modifying an instrument you compare against hands a reviewer a free
    rejection.
    """
    locus = None
    for a in attrs:
        if getattr(a, arm).excludes_zero:
            locus = a.step
    return locus


def largest_effect_step(attrs: Sequence[StepAttribution], arm: str = "te_crn") -> int | None:
    live = [a for a in attrs if getattr(a, arm).excludes_zero]
    if not live:
        return None
    return max(live, key=lambda a: abs(getattr(a, arm).estimate)).step
