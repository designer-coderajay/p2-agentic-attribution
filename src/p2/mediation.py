"""
Tool mediation for counterfactual rollouts against live external services.

The problem, stated precisely. Attribution requires re-executing a trajectory
many times under intervention. A trajectory that calls a credit bureau, a GST
service, a bank-transaction API and a penny-drop verification cannot simply be
re-run: some of those calls cost money, some mutate external state, and some
return different answers on every call for reasons that have nothing to do with
the intervention. arXiv 2606.08275 declares real tools with side effects out of
scope for exactly this reason and demonstrates on mocked tools. This module is
the layer that removes that exclusion.

The core move is that "can this tool be re-called during a counterfactual" is not
one question but four, and the answer determines a different mediation strategy.

    PURE                    deterministic, no side effects.
                            f(x) is always the same. Re-call or serve from cache,
                            both are correct. Example: a scorecard computation.

    READ_ONLY_VOLATILE      no side effects, but the answer moves.
                            A bureau lookup for the same applicant can differ
                            between Tuesday and Thursday. Re-calling injects
                            variance that is NOT attributable to the intervention,
                            so it must be served from the recorded response
                            whenever the request is identical. Re-calling here is
                            a silent confound and is the most likely way an
                            attribution study on a live system produces garbage.

    EFFECTFUL_IDEMPOTENT    mutates state, but repeating is harmless.
                            Setting a flag to the value it already has. Safe to
                            re-execute in a sandbox, never against production.

    EFFECTFUL_UNSAFE        mutates state and repeating is not harmless.
                            Penny-drop verification moves money. A notification
                            is seen by a human. These MUST NOT execute during any
                            counterfactual rollout, ever, under any operator.

Mediation strategy follows from the class and from whether the request is
identical to the factual one:

    identical request  ->  serve the recorded factual response (exact, free, safe)
    diverged request   ->  PURE                 re-call
                           READ_ONLY_VOLATILE   draw from the declared
                                                counterfactual environment
                           EFFECTFUL_IDEMPOTENT sandbox only
                           EFFECTFUL_UNSAFE     counterfactual environment only,
                                                execution refused

The counterfactual environment is the honest name for the assumption that has to
be made when a deterministic external service is asked a question it was never
asked. It is declared per tool, stated in the paper, and carries a sensitivity
analysis. Sampling silently and calling it "resampling" would be the single most
dishonest move available in this design.
"""

from __future__ import annotations

import hashlib
import json
from dataclasses import dataclass, field
from enum import Enum
from typing import Any, Callable


class Purity(Enum):
    PURE = "pure"
    READ_ONLY_VOLATILE = "read_only_volatile"
    EFFECTFUL_IDEMPOTENT = "effectful_idempotent"
    EFFECTFUL_UNSAFE = "effectful_unsafe"


class MediationError(RuntimeError):
    """Raised when a rollout attempts something the mediation policy forbids."""


def request_hash(tool: str, payload: Any) -> str:
    """Stable hash of a tool request. Cache and divergence keys both use this."""
    blob = json.dumps({"tool": tool, "payload": payload}, sort_keys=True, default=str)
    return hashlib.sha256(blob.encode()).hexdigest()[:32]


@dataclass
class ToolSpec:
    """Declared properties of one external tool. Written once, pre-registered."""

    name: str
    purity: Purity
    # Required for anything not PURE: how to produce a response for a request
    # that was never actually made. Returns a response given the request payload
    # and a uniform draw. This IS the counterfactual environment, and it is an
    # assumption, not a measurement.
    counterfactual_env: Callable[[Any, float], Any] | None = None
    notes: str = ""

    def __post_init__(self):
        if self.purity is not Purity.PURE and self.counterfactual_env is None:
            raise ValueError(
                f"tool {self.name!r} is {self.purity.value} and therefore needs a "
                "declared counterfactual environment. Refusing to guess."
            )


@dataclass
class MediationRecord:
    """One mediated call. Everything the paper needs to report is in here."""

    tool: str
    purity: Purity
    identical_to_factual: bool
    served_from: str  # factual_cache | live_call | sandbox | counterfactual_env
    refused: bool = False


@dataclass
class ToolMediator:
    """
    Sits between the agent and every external service during a rollout.

    `factual_responses` maps request_hash -> recorded response from the factual
    run. That recording is the whole reason a live system can be replayed at all,
    and it is the first concrete Annex IV requirement this project produces: a
    provider who does not record tool requests keyed by content cannot support
    post-hoc causal attribution, because the counterfactual cannot be told apart
    from the factual.
    """

    specs: dict[str, ToolSpec]
    factual_responses: dict[str, Any] = field(default_factory=dict)
    allow_sandbox: bool = False
    log: list[MediationRecord] = field(default_factory=list)

    def record_factual(self, tool: str, payload: Any, response: Any) -> None:
        self.factual_responses[request_hash(tool, payload)] = response

    def call(self, tool: str, payload: Any, uniform: float, live_fn=None) -> Any:
        if tool not in self.specs:
            raise MediationError(f"tool {tool!r} has no declared ToolSpec")
        spec = self.specs[tool]
        h = request_hash(tool, payload)

        # Identical request. Always serve the recorded factual response: exact,
        # free, and safe for every purity class including EFFECTFUL_UNSAFE.
        if h in self.factual_responses:
            self.log.append(MediationRecord(tool, spec.purity, True, "factual_cache"))
            return self.factual_responses[h]

        # Diverged request. Strategy depends on purity.
        if spec.purity is Purity.PURE:
            if live_fn is None:
                raise MediationError(f"pure tool {tool!r} needs live_fn to re-call")
            self.log.append(MediationRecord(tool, spec.purity, False, "live_call"))
            return live_fn(payload)

        if spec.purity is Purity.EFFECTFUL_IDEMPOTENT and self.allow_sandbox:
            if live_fn is None:
                raise MediationError(f"sandbox call to {tool!r} needs live_fn")
            self.log.append(MediationRecord(tool, spec.purity, False, "sandbox"))
            return live_fn(payload)

        if spec.purity is Purity.EFFECTFUL_UNSAFE:
            # Refusal is recorded, not silent. A refused call is a data point:
            # it means this node could not be intervened on against production
            # and its effect estimate rests entirely on the declared environment.
            self.log.append(
                MediationRecord(tool, spec.purity, False, "counterfactual_env", refused=True)
            )
            return spec.counterfactual_env(payload, uniform)

        self.log.append(MediationRecord(tool, spec.purity, False, "counterfactual_env"))
        return spec.counterfactual_env(payload, uniform)

    # -- reporting -----------------------------------------------------------

    def summary(self) -> dict[str, float | int]:
        """Numbers that go in the paper, not in a footnote."""
        n = len(self.log)
        if n == 0:
            return {"calls": 0}
        cached = sum(r.identical_to_factual for r in self.log)
        cf_env = sum(r.served_from == "counterfactual_env" for r in self.log)
        refused = sum(r.refused for r in self.log)
        return {
            "calls": n,
            "factual_cache_rate": cached / n,
            "counterfactual_env_rate": cf_env / n,
            "unsafe_refusal_rate": refused / n,
        }
