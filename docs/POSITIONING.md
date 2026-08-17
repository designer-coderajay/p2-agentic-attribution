# P2 Positioning and Kill-Gate Report

**Date: 13 August 2026. Supersedes section 9 of `paper-2-agentic-attribution.md`.**

Epistemic tags: VERIFIED means fetched or searched this session with a URL. RECALLED means from training, unverified. INFERRED means reasoning.

---

## 1. Result of the kill-gate check

The brief named two papers that could kill P2 and scheduled the read for 24 September. Both were checked today. **Neither is the threat.** A third paper, absent from the brief, is much closer.

### 1.1 arXiv 2605.09168, CIVeX. VERIFIED, cleared.

Fabio Rovai, The Tesseract Academy, submitted 9 May 2026. `https://arxiv.org/abs/2605.09168`

CIVeX is an **ex ante** verifier. It maps a *proposed* action to a structural causal query over a committed action-state graph, checks identifiability, and returns EXECUTE, REJECT, EXPERIMENT, or ABSTAIN before execution. Evaluated on Causal-ToolBench, IHDP, and ZOZO Open Bandit.

P2 is **post hoc** attribution over an executed trajectory. Different direction in time, different object, different comparison target. CIVeX asks whether an action *will* have an identifiable effect. P2 asks which node *did* determine the outcome, and whether the trace reports it.

**Verdict: does not kill P2. Cite as related work on causal machinery for agents, differentiate in one sentence.**

### 1.2 arXiv 2607.25364, EBTE. VERIFIED, cleared.

Genliang Zhu and Chu Wang (Accentrust, Georgia Tech, UIUC), v1 28 July 2026, v2 29 July 2026. `https://arxiv.org/abs/2607.25364`

A claim-carrying mediation layer that converts rationale content into typed action claims and checks them against server-held facts. Also ex ante, also a gatekeeper. Its contribution is that rationales are neither authorization nor reliable introspection, which is thematically aligned with the programme thesis but methodologically unrelated.

**Verdict: does not kill P2. Cite as support for the premise that self-reported rationale is not evidence.**

### 1.3 arXiv 2606.08275, Causal Agent Replay (CAR). VERIFIED. This is the real threat.

Jaineet Shah, CMU affiliation on the PDF, June 2026. `https://arxiv.org/abs/2606.08275`. Open source at `https://github.com/jaineet17/causal-agent-replay`.

From the abstract and introduction, VERIFIED, CAR contains:

- an agent run modelled as a structural causal model
- a `do()` operation on a step with **re-execution forward under the same stochastic policy**, which is exactly P2's resample operator and total effect
- an explicit **intervention algebra over agent steps**
- a single-step contrastive estimator with a point-of-commitment rule that resolves the run-forward confound
- a **budget-bounded Monte Carlo Shapley estimator** splitting credit across interacting steps
- confidence intervals on every effect
- validation against synthetic SCMs with planted ground truth
- an explicit action-match rate for replay rather than a reproducibility assertion
- the framing that observability answers what happened and evaluation answers whether it passed, but neither answers which step caused it
- the observation that the step executing the harmful action is usually not the step that decided on it

That list overlaps P2 section 4 almost line for line, and it pre-empts the introduction as written.

**A second close paper: arXiv 2605.25338, CausalFlow, VERIFIED**, causal attribution plus counterfactual repair for LLM agent failures, reporting that agent failures are often localized to one or a few steps whose intervention flips the outcome.

**A third, adjacent: arXiv 2606.09692, Observability for Delegated Execution in Agentic AI Systems, VERIFIED.** It proves a non-identifiability result: audit logs and causal tracing alone cannot in general recover delegation-scoped execution. This partially occupies the territory of the planned Annex IV traceability deliverable and must be read before that document is drafted.

Prior chain, RECALLED from citations inside those papers and **not yet directly verified**: Zhang et al., *Which Agent Causes Task Failures and When?*, arXiv 2505.00212, ICML 2025, source of the Who&When benchmark and the roughly 14 percent step-level attribution accuracy figure; and *AgenTracer*, arXiv 2509.03312. Verify both directly before citing.

---

## 2. What this kills

The claim that intervention-based causal attribution over agent trajectories is a gap the technical literature has not answered. That claim is **false as of June 2026**. Section 1 of the brief, the flagship rationale, does not survive in its current form.

Also dead as written:

- Presenting the intervention algebra as a contribution.
- Presenting Monte Carlo Shapley over steps as a contribution.
- The sentence "nobody can say which component caused a contested decision."
- The 8.5/10 rating and the "flagship" designation, pending Ajay's re-scoring.

## 3. What survives, and why it is still a paper

Four things. INFERRED from the abstracts and introductions read today; **each needs confirming against the full texts before being asserted in print.**

**3.1 The measured object is different.** CAR and CausalFlow attribute **failures** in order to debug them. P2 attributes **regulated decisions**, including correct ones, in order to test whether a filed explanation is evidence. A credit denial that is correct still needs an attributable cause under Article 86 and Annex IV. Debugging tooling has no reason to attribute a success; conformity assessment has no option not to.

**3.2 The comparison is different, and this is the strongest surviving card.** CAR's comparison target is LLM-judge accuracy on a benchmark, reported as a scalar (approximately 14 percent). P2's target is the **rank correlation between deployed observability heuristics and causal effect, plus a decomposition of the residual onto recency and verbosity.** CAR asserts the heuristics are wrong. P2 measures *how* they are wrong and *in which direction they fail*. Hypothesis H2 is a bias-structure result, and I found no evidence it has been run. That is now the headline, not the method.

**3.3 The mediated effect decomposition.** `ME = TE - DE` requires pinning downstream nodes to factual values. From the abstract, CAR runs forward and adapts, which is total effect only; its point-of-commitment rule addresses the run-forward confound but is not the same object as a natural direct and indirect effect decomposition. If the full text confirms CAR has no `DE` arm, `ME` is P2's technical core and H4 (the discrepancy concentrates in high-`ME`, low-`DE` nodes) is the mechanistic explanation nobody else has. **This is the single highest-value thing to confirm in the full read.**

**3.4 The regulatory conversion.** Neither CAR, CausalFlow, nor EBTE produces an Annex IV traceability requirement. 2606.09692 is closest and must be read first, but its object is delegation scope, not causal attributability. The specification of what a provider must log for post-hoc causal attribution to be *possible at all* remains unoccupied, and it is the deliverable that reaches TÜV AI.Lab, notified bodies, and CEN-CENELEC JTC 21.

Ajay's differentiator was never the causal machinery. It was the combination of a real regulated production system, five live MCP servers, and the regulatory reading. That combination is intact.

## 4. Revised one-sentence framing

> Causal attribution over agent trajectories is now solvable. This paper shows that the observability record a provider actually files does not recover it, characterises the bias that makes it fail, and specifies the record-keeping that would make an Annex IV filing checkable.

The paper moves from method to **measurement plus regulation**. INFERRED: this is a better fit for FAccT than the original framing, and a worse fit for a systems venue.

## 5. Actions

| Action | Owner | Deadline | Status |
|---|---|---|---|
| Full read of 2606.08275, confirm absence of a DE/ME arm | Claude | 15 Aug | open |
| Full read of 2605.25338 CausalFlow | Claude | 17 Aug | open |
| Full read of 2606.09692, scope the Annex IV deliverable against it | Claude | 20 Aug | open |
| Verify 2505.00212 and 2509.03312 directly | Claude | 15 Aug | open |
| Run CAR's open-source repo against one BFSI trajectory to see what it does and does not produce | Ajay + Claude | 24 Aug | open |
| Re-score P2 and decide flagship status | **Ajay** | after full reads | open |

## 6. The honest downside

If the full read of CAR reveals a direct-effect arm and any observability comparison beyond the single Who&When number, P2 as designed reduces to an application paper: same method, new domain, regulatory wrapper. That is publishable at a workshop, not at FAccT, and it is not a flagship. Ajay should know that outcome is live before October compute is spent.

---

# ADDENDUM: Gate A resolved, 13 August 2026

Full text of arXiv 2606.08275v1 fetched and read. `https://arxiv.org/html/2606.08275v1`. Single author, Jaineet Shah, CMU email, 06 June 2026, cs.LG, eight sections, no venue listed.

## Gate A: PASSED. P2 proceeds to full build.

### 1. CAR has no direct-effect arm, and says so

Section 7, Limitations, VERIFIED: the contrastive effect is a total effect through a stochastic continuation, and isolating a step's direct effect calls for common random numbers across branches, which is hard across divergent LLM contexts and **is left as a refinement**.

`DE`, `ME`, and H4 are open. This is exactly the thing that had to be true and it is stated by the authors as future work, which is the strongest possible version of the answer. P2's positioning line becomes: CAR resolves the run-forward confound with a heuristic locus rule; we resolve it with the mediation decomposition, and we compare the two.

### 2. CAR has no observability comparison at all

VERIFIED: the only comparison to non-causal attribution in the whole paper is the cited Who&When figure of approximately 14 percent step-level LLM-judge accuracy. There is no rank correlation, no attributor set, no bias decomposition, nothing on recency or verbosity. H1, H2, H3 are untouched.

### 3. CAR does not run on a real system

VERIFIED, section 7: **real tools with side effects are out of scope; the demonstrations use mocked, reproducible tools.** Validation is against synthetic SCMs with planted ground truth, plus one illustrative mocked support agent.

This was the differentiator I expected to have to argue for. It is now conceded in print. A BFSI credit underwriting pipeline with five live MCP servers is the case CAR explicitly excludes.

### 4. CAR disclaims novelty on the parts P2 was going to have to concede anyway

VERIFIED, section 6: CAR states it is deliberately not claiming novelty on counterfactual replay or Shapley for agent blame. Its claimed contribution is the combination of executed same-policy interventions, distributional outcomes with intervals, the point-of-commitment rule, Shapley credit splitting, and ground-truth validation.

Counterfactual replay over agent steps is field commons, not CAR's property. Cite and move on.

## Decisions taken, all reversible, no action needed from Ajay

1. **Adopt CAR's intervention algebra rather than inventing a competing one.** CAR implements five operations, VERIFIED: `do_resample` (re-draw the action from the same policy, the null intervention), `do_action` (force an action), `do_observation` (replace a tool result), `do_context` (edit history at k), `do_policy` (swap the model from k onward). This is strictly better than P2's remove/resample/corrupt triple: `do_observation` is precisely the tool-output intervention P2 needed and had no clean name for, and using their vocabulary removes a reviewer's easiest complaint. P2's *remove* has no counterpart and is dropped rather than defended.

2. **Add a head-to-head against the point-of-commitment rule.** CAR's locus rule is the latest step whose effect interval still excludes zero. `ME`/`DE` is an alternative resolution of the same confound with a principled basis in natural direct and indirect effects. Both run off the same rollouts, so the comparison is nearly free, and it converts P2 from "adjacent work" into "the method paper that answers their open problem." This is now a named contribution.

3. **Rule-based outcome function only for `Y`.** CAR's limitation, VERIFIED: judge-based outcome functions inject their own noise and rule-based outcomes are preferred for anything to be trusted. BFSI credit decisions are natively rule-based. The LLM judge stays in the design only as an observability *attributor*, which is a measured object, not as the outcome function.

4. **Real-tool side effects become a headline differentiator, stated in the abstract**, with the sandboxing and idempotency protocol as a methods contribution. CAR conceded this scope; taking it is free.

5. **`DE` pinning uses common random numbers where the contexts have not diverged**, which is CAR's own diagnosis of why the problem is hard. This is the technical crux of the paper and gets the largest single block of build time.

6. **P1 slips**: analysis 1 to 5 September, writing 5 to 12, arXiv around 12 September. Its sweep is unattended compute and the results do not spoil.

## Revised abstract-level framing

> Causal attribution over agent trajectories is now possible in principle, but only as a total effect on mocked tools. This paper runs it on a live regulated credit-underwriting system with five external services, adds the direct-effect decomposition its authors left open, and shows that the observability record a provider would actually file recovers neither: it tracks recency and verbosity rather than causation, and is blind precisely where mediation is largest. We specify the record-keeping an Annex IV filing would need to be checkable.

## Residual risk

Low but non-zero. CausalFlow (2605.25338) and Ma et al. (2509.08682, Shapley with causal discovery over static logs) are still unread. Neither is likely to carry a direct-effect arm or an observability bias decomposition, but they are on the D2 calendar and the framing above is provisional until they are read.

---

# ADDENDUM 2: D2 landscape sweep, 14 August 2026

Four papers checked from source today, two of them not previously known to this project. The cross-check was run twice: once against P2's four surviving contributions, once against the estimator design in `src/p2/effects.py`.

## 1. arXiv 2605.25338, CausalFlow. VERIFIED from source. Cleared.

Akash Bonagiri, Devang Borkar, Gerard Janno Anderias, Setareh Rafatirad, Houman Homayoun. v1, 25 May 2026, cs.LG and cs.AI. Author list confirmed against the arXiv listing page, not taken from another paper's bibliography.

What it is: a repair pipeline. It computes a Causal Responsibility Score, `CRS(s_i) = I[V(tau') = 1]`, a **binary indicator**, by replacing a step with an **oracle-guided alternative** and re-executing downstream. Validated repairs become contrastive training pairs.

Three reasons it is not a threat:
1. Oracle substitution, not same-policy resample. It asks what a *better* step would have done, not what the step's own distribution would have done. Different estimand.
2. `CRS` is binary. No outcome distribution, no confidence intervals, no direct or mediated effect.
3. Purpose is repair and preference-optimisation supervision, not attribution measurement. Domains are maths, code, QA and medical, not regulated decisions.

Notable, and useful: a secondary source summarising the paper states that the technique requires sandboxed reasoning and that production tool-use agents mutating external state need a snapshotting layer first. **That is the second independent confirmation that live side-effecting tools are unoccupied territory.** RECALLED from a secondary source; confirm against the paper's own limitations section before citing it that way.

## 2. arXiv 2607.20827, Auditing Provenance Sensitivity in LLM Agent Action Selection. VERIFIED, full text read. Cleared, but it takes territory.

Junchi Liao, v1, 23 July 2026, cs.AI. This is a strong, careful paper: 450 tasks, 1,350 audited targets, 10,800 target-factor labels, three external PhD annotators, Fleiss kappa 0.608 on four labels and 0.626 on invalid-versus-rest, cluster-bootstrap intervals throughout, an explicit label-count-matched null over 500 permutations.

Why it does not kill P2, established on two independent axes:

- **Its unit of intervention is a context factor inside a prompt, not a trajectory step.** It states that no environment transition is simulated during scoring. There is no re-execution, no suffix rollout, no downstream adaptation. Consequently there is no total effect through a stochastic continuation, and therefore no direct effect and no mediation. The whole `TE_crn` / `DE` / `ME` decomposition is outside its design.
- **It runs no comparison against observability tooling.** No span duration, token count, recency, terminality or LLM-judge attributor. H1, H2 and H3 remain untouched by it.

Why it nonetheless costs P2 something real, and this is the part that matters:

Its opening move is that evidence can be relevant without being authorized to determine a decision, so a correct action need not be grounded only in permitted evidence, and that outcome benchmarks cannot distinguish a well-grounded decision from a brittle one that happens to be correct. **That is contribution 1's motivation, already in print since 23 July 2026.** P2 cannot present "we attribute correct regulated decisions, not only failures" as a new framing. It must cite Liao, adopt the framing as established, and differentiate on the mechanism.

It also runs Harsanyi and Shapley interactions over context subsets, which further reduces the value of any Shapley arm. The Stage 3 cut made for the sprint now looks correct for reasons beyond time.

## 3. Newly surfaced, unread, on the D3 list

From Liao's related work and the CausalFlow search:

- **arXiv 2603.10749, AttriGuard**, He et al. 2026: defeating indirect prompt injection via causal attribution of tool invocations. RECALLED via citation.
- **arXiv 2602.07918, CausalArmor**, Kim et al. 2026: indirect prompt injection guardrails via causal attribution. RECALLED via citation.
- **arXiv 2606.04990**, a survey of evidence tracing and execution provenance in LLM agents, at v4 by late June 2026. RECALLED. **A survey existing in this space is itself information: the area is mature enough to be surveyed, and any "nobody has done this" sentence in P2 must be checked against it.**
- **arXiv 2607.24054, AcquaBench**, Luo and Peng: audits whether success depended on an acquired target via CLEAN/GOLD/SHAM substitution. Different object (benchmark contamination), but it owns the phrase that a correct answer can conceal why an agent succeeded.
- **arXiv 2607.12747, OAT**: unsupervised failure attribution by one-class learning on successful trajectories. Learned, not causal. Cite, not a threat.
- **arXiv 2603.03116**, procedure-aware evaluation, reporting 27 to 78 percent of benchmark-reported successes as corrupt successes concealing violations. Adjacent.

## 4. Honest revised position

The claim in the original brief that the technical literature has not answered this is **false**, and now demonstrably so on several axes at once. What survives is a conjunction, not a gap:

| Element | Occupied by | P2's remaining edge |
|---|---|---|
| Interventional attribution over agent steps | CAR, CausalFlow | none, cite them |
| Shapley over agent components | CAR, Liao | none, arm already cut |
| Attributing correct, not only failed, decisions | Liao, AcquaBench, PAE | none as framing, cite them |
| Trajectory re-execution with downstream adaptation | CAR only | shared |
| **Direct and mediated effect via common random numbers** | **nobody** | **the technical core** |
| **Rank comparison against deployed observability attributors, with bias decomposition** | **nobody** | **the headline** |
| **Live side-effecting tools in a regulated decision** | **excluded by CAR and CausalFlow** | **the setting** |
| **Annex IV record-keeping conversion** | **nobody** | **the deliverable** |

Four rows are gone. Four remain, and they are the four the D1 build already implements or targets.

**INFERRED, and stated as my assessment rather than a fact:** this is still a paper, and the CRN result validated yesterday is still, as far as four days of searching can establish, unoccupied. But it is no longer an 8.5-out-of-10 flagship whose gap was named as unsolved by policy people. It is a narrower methods-plus-measurement paper with a strong regulatory deliverable. Gate A is tomorrow. Ajay should re-score against this table, not against the original brief.

---

# ADDENDUM 3: the survey, 15 August 2026

**arXiv 2606.04990v4, *From Agent Traces to Trust: A Survey of Evidence Tracing and Execution Provenance in LLM Agents*.** VERIFIED, full text read. Yiqi Wang (Griffith), Jiaqi Zhang, Zhangkai Wu, Taotao Cai, Zirui Liu, Qingqiang Sun, Zequn Sun, Manqing Dong, Mingkai Zheng, Xuefei Yin, Yanming Zhu. v4, 28 June 2026, cs.CR. Live repository at github.com/xiaoqi-7/Agent-Tracing-Survey.

This was the highest-risk remaining read: a survey of exactly P2's space, meaning any residual novelty claim had to survive a document whose job is to enumerate everything. **It survives, and the survey improves P2's position rather than weakening it.**

## 1. The survey states P2's premise as an open tension, not as a measured result

Section 2.2, design tension one, paraphrased: chronological logging and semantic provenance are not the same thing, because a log can record what happened without showing whether evidence supported a claim or whether memory influenced a tool call.

That is P2's premise, from a third party, in a survey. It is stated as a **tension the field has identified**, not as something anyone has quantified. The survey nowhere reports a measurement of how far observability output diverges from causal effect.

## 2. The survey classifies execution-provenance metrics as "Proposed"

Section 6.3, Table 5. The survey grades each metric family by maturity: *Established* means operationalised in existing benchmarks, *Partly established* means it exists for some sub-tasks, and *Proposed* means a desideratum without agreed definitions or broadly adopted evaluation protocols.

- Evidence attribution: **Established**
- Safety and robustness: **Established**
- Debugging and recovery: **Partly established**
- **Execution provenance (trace completeness, provenance accuracy, dependency coverage, temporal consistency): Proposed**

**This is the single most useful sentence found in six days of searching.** It is a third-party, survey-level statement that the exact quantity P2 measures has no agreed definition and no adopted protocol. It belongs in P2's paragraph one, and it is far stronger than any claim P2 could make on its own authority.

## 3. What the survey does not contain

Checked twice, once by reading the taxonomy and metric tables and once by scanning the seven research threads and the open-problems section:

- **No mediation, no direct effect, no natural direct or indirect effect, no common random numbers, no counterfactual estimand.** The closest is AgenTracer, described as using counterfactual replay and fault injection, which CAR independently characterises as oracle substitution rather than same-policy resampling.
- **No comparison of observability output against causal ground truth.** Observability is one of the seven reviewed threads (AgentOps, AgentTrace, TRAIL, LADYBUG), and every system in it is described as recording or localising. None is described as validated.
- **No EU AI Act, no Annex IV, no conformity assessment.** Section 7.5 discusses governance, but as privacy, retention, minimisation and access control, not as regulatory conformity evidence.

All four remaining rows of the addendum-2 table survive a document written to enumerate this field.

## 4. What the survey gives WS6 for free

Section 7.1 and Appendix D.1 set out trace-schema requirements, and section 6.4 specifies what a full-stack provenance benchmark must record: user requests, retrieved evidence, tool calls and outputs, memory reads and writes, inter-agent messages, intermediate claims, final responses, external state changes, and policy or permission context, plus typed relations Support, Contradict, Depend-on, Update, Invalidate, Trigger.

**The Annex IV traceability specification should be built on top of this rather than invented.** The argument becomes: the field has converged on what a provenance schema should record; here is what must additionally be recorded for post-hoc *causal* attribution to be possible, and here is how that maps onto Articles 11, 12 and Annex IV. That is a stronger and more citable deliverable than a specification written from nothing, and it costs less time.

## 5. Cost

The survey's own framing sentence, that a correct answer reveals nothing about how an output was produced, is now the third independent occurrence of P2's contribution-1 motivation, after Liao and AcquaBench. It is field common ground. P2 cites it and moves on.

## 6. Still unverified, carried to D4

AttriGuard 2603.10749 and CausalArmor 2602.07918, both RECALLED via Liao's bibliography, both presumed ex ante guardrails. Also newly surfaced from the survey's bibliography and unverified: AgentTrace 2602.10133, Ghost in the Agent 2604.23374 (information-flow tracking), Securing AI Agent Execution 2510.21236, MAST (Cemri et al., NeurIPS 38), Agent-Sentry, FIDES, NeuroTaint, CaMeL, AgentSpec, AgentBound, TRAIL, LADYBUG, Aegis, PROV-AGENT, and W3C PROV-DM. None is a threat to the four remaining rows on its face; all are related-work citations and several are load-bearing for WS6.
