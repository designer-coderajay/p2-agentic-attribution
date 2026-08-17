# P2 Memory

State that must survive a chat that does not remember across weeks. Update at the end of every session.

## Current framing (as of 2026-08-13, revision 2)
Causal attribution over agent trajectories is now solvable (2606.08275). P2 measures the discrepancy between the observability record a provider files and the causal ground truth, characterises its bias structure, and converts the result into an Annex IV record-keeping requirement.

**Do not draft any text presenting intervention-based agent attribution as new.**

## Sprint
**13 to 31 August 2026. 19 days, 15 hours per day. arXiv 31 August.** See `docs/AUGUST-SPRINT.md`.
Daily entry in `docs/DAILY.md`, end of day, never reconstructed.

## Live gates (all moved forward for the sprint)
- Gate A, **14 Aug**: full read of 2606.08275 confirms no DE arm and no observability bias decomposition. If it fails, P2 stops and does not build.
- Gate B, **17 Aug**: cost. Stage 0 measured per-rollout cost fits the nested budget within 3x.
- Gate C, **17 Aug**: replay floor. Null-replay action-match rate above the pre-registered threshold.
- Gate D, **20 Aug**: pre-registration committed with a timestamp. Nothing pooled before this exists.
- Gate E, **17 Aug**: harness working end to end on one BFSI trajectory.

## Cut for the sprint
- Stage 3 Shapley: dropped, cite 2606.08275. It is prior art.
- Third-party framework arm: dropped, limitation in the abstract.
- Second system: reduced to Stage 0 and 1, plus Stage 2 if days 15 to 17 hold.
- N: set by the power simulation on 20 Aug, not by the N >= 300 figure.

Kept and non-negotiable: the DE arm and ME (H4), the five observability attributors, the bias decomposition (H2), the pre-registration, the Annex IV spec.

## Decided
- Resample is the primary intervention operator. Remove is a contrast only.
- The observability attributor set is the novel object and gets P1-claim-map levels of care: deterministic code, pre-registered, each justified by a real tool.
- Nested four-stage design. No naive full sweep.
- Power by simulation, not formula.

## Undecided (Ajay owns all of these)
1. P2 literature work now vs fully dormant until 24 Sept
2. Flagship status after Gate A
3. Third-party framework arm vs larger corpus
4. Venue (FAccT favoured under the revised framing)
5. Annex IV spec ships with the paper or earlier and separately

## Known-unmeasured
Every cost, runtime, node count, and corpus size in the plan. Stage 0 measures them. Nothing is quoted in the paper until it is.
