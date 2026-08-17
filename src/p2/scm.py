"""
Synthetic agent SCMs with analytically known causal structure.

Every quantity these SCMs induce is derived by hand in docs/DERIVATIONS.md and the
estimators are checked against those derivations, not against each other. An
attribution method validated only against its own output is not validated.

Trajectory schema mirrors the real one:  tau = [s_0, (a_1,o_1), ..., (a_n,o_n), y].

Randomness discipline. Every stochastic draw is a pure function of
(seed, step index, replicate). Nothing depends on call order. This is what makes
common random numbers possible, and CRN is what makes the direct effect estimable.
arXiv 2606.08275 section 7 names exactly this as the reason it leaves the direct
effect as a refinement.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Callable, Sequence

import numpy as np


@dataclass(frozen=True)
class Step:
    index: int
    kind: str
    action: int


@dataclass
class Trajectory:
    steps: list[Step]
    outcome: float

    def actions(self) -> tuple[int, ...]:
        return tuple(s.action for s in self.steps)


class CRNStream:
    """Uniform draws keyed by (seed, step, replicate). Order independent by construction."""

    def __init__(self, seed: int):
        self._seed = int(seed)

    def uniform(self, step_index: int, replicate: int) -> float:
        ss = np.random.SeedSequence([self._seed, int(step_index), int(replicate)])
        return float(np.random.default_rng(ss).random())


Policy = Callable[[Sequence[int], float], int]


@dataclass
class SyntheticSCM:
    name: str
    policies: list[Policy]
    outcome_fn: Callable[[Sequence[int]], float]
    kinds: list[str] = field(default_factory=list)
    notes: str = ""

    def __post_init__(self):
        if not self.kinds:
            self.kinds = ["llm_call"] * len(self.policies)
        assert len(self.kinds) == len(self.policies)

    @property
    def n_steps(self) -> int:
        return len(self.policies)

    def run(self, crn, replicate, forced=None, pinned=None) -> Trajectory:
        """
        forced: step -> action. Overrides the policy. This is do_action, and
                do_resample is expressed by forcing a value drawn from the same policy.
        pinned: step -> action. Held at factual value regardless of upstream. The DE arm.
        replicate: which noise stream the NON forced, NON pinned steps draw from.
                   Passing the factual replicate here is the CRN condition.
        """
        forced = forced or {}
        pinned = pinned or {}
        actions: list[int] = []
        steps: list[Step] = []
        for k in range(self.n_steps):
            if k in forced:
                a = int(forced[k])
            elif k in pinned:
                a = int(pinned[k])
            else:
                a = int(self.policies[k](tuple(actions), crn.uniform(k, replicate)))
            actions.append(a)
            steps.append(Step(k, self.kinds[k], a))
        return Trajectory(steps, float(self.outcome_fn(tuple(actions))))

    def sample_action(self, k, prefix, crn, replicate) -> int:
        return int(self.policies[k](tuple(prefix), crn.uniform(k, replicate)))


# -----------------------------------------------------------------------------
# Planted structures. Parameters are module constants so the derivations and the
# code cannot drift apart.
# -----------------------------------------------------------------------------

Q_FIDELITY = 0.9   # P(executing step follows the retrieval)
W_DIRECT = 0.5     # weight of the retrieval's own direct path into the outcome


def partial_mediation_scm() -> SyntheticSCM:
    """
    Four steps. The structure the paper is about.

        a0 ~ Bern(1/2)                      inert chatter, no path to y
        a1 ~ Bern(1/2)                      retrieval: pulls the risk flag
        a2 ~ Bern(1/2)                      inert chatter, no path to y
        a3 = a1        if u3 < q            executing tool call
             1 - a1    otherwise
        y  = w*a1 + (1-w)*a3

    Step 1 reaches y by two paths: directly (weight w) and through step 3
    (weight 1-w). So its direct effect is nonzero and strictly smaller than its
    total effect, which is the case that makes ME informative rather than trivially
    equal to TE.

    Steps 0 and 2 have no path to y at all. Their true effect is exactly zero under
    every definition. They are the negative control, and under naive run forward
    they will not look like zero.
    """
    q, w = Q_FIDELITY, W_DIRECT

    def p0(prefix, u): return int(u < 0.5)
    def p1(prefix, u): return int(u < 0.5)
    def p2(prefix, u): return int(u < 0.5)
    def p3(prefix, u): return int(prefix[1]) if u < q else 1 - int(prefix[1])

    return SyntheticSCM(
        name="partial_mediation",
        policies=[p0, p1, p2, p3],
        outcome_fn=lambda a: w * a[1] + (1.0 - w) * a[3],
        kinds=["llm_call", "retrieval", "memory_read", "tool_call"],
        notes="Step 1 acts both directly and through step 3. Steps 0 and 2 are inert.",
    )


def pure_mediation_scm() -> SyntheticSCM:
    """Same, with w = 0: step 1 reaches y only through step 3. DE(1) is exactly 0."""
    q = Q_FIDELITY

    def p0(prefix, u): return int(u < 0.5)
    def p1(prefix, u): return int(u < 0.5)
    def p2(prefix, u): return int(u < 0.5)
    def p3(prefix, u): return int(prefix[1]) if u < q else 1 - int(prefix[1])

    return SyntheticSCM(
        name="pure_mediation",
        policies=[p0, p1, p2, p3],
        outcome_fn=lambda a: float(a[3]),
        kinds=["llm_call", "retrieval", "memory_read", "tool_call"],
        notes="w = 0. Step 1 is a pure mediator: DE(1) = 0 exactly.",
    )


REGISTRY = {
    "partial_mediation": partial_mediation_scm,
    "pure_mediation": pure_mediation_scm,
}
