# Attributor provenance audit (WS3.3)

17 August 2026. Rule: every attributor is traced to a documented shipping tool or
practice, or it is cut. A reviewer will call these strawmen and a citation is the
only answer. VERIFIED means searched this session with a URL.

| attributor | status | evidence |
|---|---|---|
| span_duration | VERIFIED | Langfuse documents sorting traces by duration to find slow queries (encore.dev/blog/langfuse-tutorial). OTel GenAI defines an operation-duration histogram. Tool spans documented as where latency outliers surface (zylos.ai, 2026-02-28). |
| token_count | VERIFIED | OTel GenAI standardises gen_ai.usage.input_tokens / output_tokens; Datadog maps them natively (datadoghq.com, 2025-12-01). Per-span token accounting documented as the way an anomalous step becomes visible: 50k tokens where 3k is normal signals misbehaviour (zylos.ai). |
| terminal_action | VERIFIED | OTel GenAI defines execute_tool as a first-class span type (opentelemetry.io/blog/2026/genai-observability). CAR 2606.08275 states the executing step is usually not the deciding step. |
| recency | **NOT SOURCED. CUT.** | No shipping tool found that ranks trace steps by recency. It is an inference about how humans read a trace, not a documented feature. Keeping it would be the strawman the audit exists to prevent. |

## Consequence

H1's tau_b attributor set is THREE, not four.

Recency is retained ONLY as a covariate in the H2 regression, where it is a bias
term rather than an attributor and needs no tool provenance. H2 is unaffected.

## For WS6, the Annex IV deliverable

The OTel GenAI conventions are pre-1.0 and mid-flight: the June 2026 repository
split moved the human-readable conventions out of the main semconv docs, and
attribute stability markers were replaced by a pointer. Frameworks emit both
attribute generations simultaneously during the transition.

A conformity specification cannot be written against a moving standard without
saying so. This goes in the deliverable's opening paragraph, with a pinned
version recorded.

Useful for the same deliverable: OTel already defines span shapes for model
inference, embeddings, retrieval, memory operations, tool execution, agent
invocation, workflow invocation and planning. That maps closely onto P2's node
types, so the Annex IV spec extends an existing schema rather than inventing one.
