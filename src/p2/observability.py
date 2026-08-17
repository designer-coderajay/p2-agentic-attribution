"""Observability attributors: the objects under test. H1/H2/H3 ask what the trace
a provider would file says was decisive, versus what intervention shows.

Every attributor must be traceable to a real shipping tool before it enters the
paper. WS3.3 audit completed 2026-08-17, see docs/PROVENANCE.md.

RECENCY WAS CUT. No shipping tool was found that ranks trace steps by recency; it
was an inference about how humans read a trace. It survives only as a COVARIATE in
the H2 regression, where it is a bias term rather than an attributor and needs no
tool provenance. H1's tau_b set is therefore three attributors, not four.
"""
from __future__ import annotations
from dataclasses import dataclass, field
import numpy as np


@dataclass
class SpanRecord:
    """Only fields a real OTel/Langfuse trace carries. If an attributor needs
    something not here it is an oracle, not an attributor, and using it would
    flatter the tools under test."""
    index: int
    kind: str
    duration_ms: float
    output_tokens: int
    is_terminal: bool = False


@dataclass
class Attributor:
    name: str
    fn: object
    provenance: str = "UNVERIFIED"
    def score(self, spans): return np.asarray(self.fn(spans), dtype=float)


ATTRIBUTORS = [
    Attributor("span_duration", lambda ss: [s.duration_ms for s in ss],
               "VERIFIED 2026-08-17: Langfuse documents sorting traces by duration to find "
               "slow queries; OTel GenAI defines an operation-duration histogram"),
    Attributor("token_count", lambda ss: [s.output_tokens for s in ss],
               "VERIFIED 2026-08-17: OTel gen_ai.usage.*_tokens; per-span token accounting "
               "documented as how an anomalous step becomes visible"),
    Attributor("terminal_action", lambda ss: [1.0 if s.is_terminal else 0.0 for s in ss],
               "VERIFIED 2026-08-17: OTel defines execute_tool as a first-class span type; "
               "CAR 2606.08275 says the executing step is usually not the deciding "
               "step. This attributor is that error made explicit."),
]


def rank_desc(x):
    """Average ranks, 1 = highest. Ties share a rank: durations and token counts
    tie constantly in real traces and terminal_action is binary, so tau_b's tie
    correction is not optional here."""
    x = np.asarray(x, dtype=float)
    order = np.argsort(-x, kind="mergesort")
    ranks = np.empty(len(x), dtype=float)
    i = 0
    while i < len(x):
        j = i
        while j + 1 < len(x) and x[order[j + 1]] == x[order[i]]:
            j += 1
        ranks[order[i:j + 1]] = (i + j) / 2.0 + 1.0
        i = j + 1
    return ranks


def kendall_tau_b(x, y):
    """tau_b = (C - D) / sqrt((n0 - n1)(n0 - n2)), n0 = n(n-1)/2. Implemented not
    imported so the tie handling is auditable and the repo stays numpy-only."""
    x = np.asarray(x, dtype=float); y = np.asarray(y, dtype=float)
    n = len(x)
    if n < 2: return float("nan")
    C = D = 0
    for i in range(n - 1):
        s = np.sign(x[i + 1:] - x[i]) * np.sign(y[i + 1:] - y[i])
        C += int((s > 0).sum()); D += int((s < 0).sum())
    n0 = n * (n - 1) / 2.0
    def tie(v):
        _, c = np.unique(v, return_counts=True)
        return float((c * (c - 1) / 2.0).sum())
    d = np.sqrt(max(n0 - tie(x), 0.0) * max(n0 - tie(y), 0.0))
    return float((C - D) / d) if d > 0 else float("nan")


@dataclass
class SyntheticTraceGenerator:
    """Decisions with PLANTED relationships between causal effect and
    presentational properties. Validates that the H1/H2 machinery recovers a known
    answer. A test of the statistics, NOT evidence about real systems."""
    n_steps: int = 25
    beta_causal: float = 1.0
    beta_recency: float = 0.0
    beta_verbosity: float = 0.0
    noise_sd: float = 0.5
    decision_sd: float = 0.8
    seed: int = 0
    _rng: object = field(default=None, repr=False)

    def __post_init__(self): self._rng = np.random.default_rng(self.seed)

    def decision(self):
        n, r = self.n_steps, self._rng
        causal = r.normal(0, 1, n)
        recency = np.arange(n) / (n - 1)
        log_tokens = r.normal(4.0, 0.8, n)
        duration = np.exp(r.normal(5.0, 0.9, n))
        spans = [SpanRecord(i, "llm_call", float(duration[i]),
                            int(np.exp(log_tokens[i])), is_terminal=(i == n - 1))
                 for i in range(n)]
        z = lambda v: (v - v.mean()) / v.std()
        zc, zr, zv = z(causal), z(recency), z(log_tokens)
        # Decision-level random intercept. Without it rows within a decision are
        # independent, cluster-robust and naive SEs agree, and a coverage test
        # built on such a generator silently fails to test what clustering is for.
        alpha_d = r.normal(0, self.decision_sd)
        latent = (self.beta_causal * zc + self.beta_recency * zr
                  + self.beta_verbosity * zv + alpha_d
                  + r.normal(0, self.noise_sd, n))
        return {"causal": causal, "latent_obs": latent, "spans": spans,
                "z_causal": zc, "z_recency": zr, "z_verbosity": zv}
