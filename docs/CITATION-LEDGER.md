# P2 Citation Ledger

Append-only. Nothing enters a manuscript until it appears here as VERIFIED with a checked date.
Status values: VERIFIED (fetched/searched, URL recorded), RECALLED (training only), FALSE (checked, does not exist as stated).

**Verification sweep 2026-08-21.** Eight of the load-bearing RECALLED entries were
checked against primary sources this session. One citation was **WRONG in two
fields** and would have entered the bibliography uncorrected (2509.08682, see
below). Three entries gained material qualifications that change how they must be
cited. Details in the corrections section at the foot of this file.

| arXiv / ref | Title | Authors / venue | Status | Checked | Note |
|---|---|---|---|---|---|
| 2605.09168 | CIVeX: Causal Intervention Verification for Language Agents | Fabio Rovai, The Tesseract Academy. Submitted 9 May 2026 | VERIFIED | 2026-08-13 | Ex ante action verifier. Cleared as kill-gate threat. |
| 2607.25364 | Explanation-Bound Tool Execution for AI Agents | Genliang Zhu, Chu Wang (Accentrust / Georgia Tech / UIUC). v1 28 Jul 2026, v2 29 Jul 2026 | VERIFIED | 2026-08-13 | Ex ante mediation layer. Cleared. |
| 2606.08275 | Causal Agent Replay: Counterfactual Attribution for LLM-Agent Failures | Jaineet Shah, jaineets@andrew.cmu.edu. v1, 06 Jun 2026, cs.LG. No venue listed. | VERIFIED, FULL TEXT READ | 2026-08-13 | Gate A PASSED. No DE arm (sec 7 names it future work). No observability comparison. Mocked tools only, real side effects out of scope. Repo: github.com/jaineet17/causal-agent-replay |
| 2605.25338 | CausalFlow: Causal Attribution and Counterfactual Repair for LLM Agent Failures | Akash Bonagiri, Devang Borkar, Gerard Janno Anderias, Setareh Rafatirad, Houman Homayoun. v1 25 May 2026, cs.LG/cs.AI | VERIFIED, authors confirmed on arXiv listing | 2026-08-14 | Cleared. Oracle substitution not same-policy resample; CRS is a binary indicator; purpose is repair and training supervision. |
| 2607.20827 | Auditing Provenance Sensitivity in LLM Agent Action Selection | Junchi Liao. v1 23 Jul 2026, cs.AI | VERIFIED, FULL TEXT READ | 2026-08-14 | Cleared but takes the "correct action need not be grounded in permitted evidence" framing. Static context-factor ablation, no trajectory re-execution, no DE/ME, no observability comparison. MUST be cited in P2 paragraph one. |
| 2607.24054 | Success Is Not Self-Explanatory: Auditing Success Provenance in Agent Evaluation | Jingkun Luo, Da-Tian Peng. v1 27 Jul 2026, cs.AI, 17pp | VERIFIED (abstract + listing) | 2026-08-14 | AcquaBench, CLEAN/GOLD/SHAM. Benchmark-contamination object, not step attribution. Owns "a correct answer can conceal why an agent succeeded". |
| 2607.12747 | Tracing Agentic Failure from the Flow of Success (OAT) | not recorded | VERIFIED (abstract) | 2026-08-14 | Unsupervised failure attribution, one-class learning with neural CDEs. Learned not causal. Cite. |
| 2603.03116 | Beyond Task Completion: Revealing Corrupt Success in LLM Agents through Procedure-Aware Evaluation | Hongliu Cao, Ilias Driouich, Eoin Thomas. 3 Mar 2026 | VERIFIED (abstract) | 2026-08-14 | Reports 27-78% of benchmark successes as corrupt. Adjacent. |
| 2606.04990 | From Agent Traces to Trust: A Survey of Evidence Tracing and Execution Provenance in LLM Agents | Yiqi Wang (Griffith), Jiaqi Zhang, Zhangkai Wu, Taotao Cai, Zirui Liu, Qingqiang Sun, Zequn Sun, Manqing Dong, Mingkai Zheng, Xuefei Yin, Yanming Zhu. v4, 28 Jun 2026, cs.CR | VERIFIED, FULL TEXT READ | 2026-08-15 | CLEARS P2. Sec 6.3 Table 5 grades execution-provenance metrics as "Proposed": no agreed definitions, no adopted protocols. LOAD-BEARING for paragraph one. Sec 7.1 and 6.4 give the schema basis for WS6. Repo: github.com/xiaoqi-7/Agent-Tracing-Survey |
| **2509.08682** | **Automatic Failure Attribution and Critical Step Prediction Method for Multi-Agent Systems Based on Causal Inference** | **Guoqing Ma, Jia Zhu, Hanghui Guo, Weijie Shi, Jiawei Shen, Jingjiang Liu, Yidan Liang.** v1 10 Sep 2025, cs.AI, CC BY 4.0 | **VERIFIED, FULL TEXT READ** | **2026-08-21** | **TITLE AND FIRST AUTHOR WERE BOTH WRONG in the previous entry. See correction C1.** NOT a threat: static logs, no re-execution for attribution, no observability-vs-causal comparison, no DE/ME arm, Shapley over AGENTS not steps, zero regulatory content. |
| **2505.00212** | **Which Agent Causes Task Failures and When? On Automated Failure Attribution of LLM Multi-Agent Systems** | **Shaokun Zhang, Ming Yin, Jieyu Zhang, Jiale Liu, Zhiguang Han, Jingyang Zhang, Beibin Li, Chi Wang, Huazheng Wang, Yiran Chen, Qingyun Wu.** v1 30 Apr 2025, v3 2 Jun 2025, cs.MA/cs.CL. **ICML 2025, PMLR v267, pp. 76583-76599** | **VERIFIED, FULL TEXT READ** | **2026-08-21** | Who&When benchmark. Venue confirmed against PMLR directly. The 14.2% figure is real but is a four-cell average printed only in the abstract. **See correction C2 before citing the number.** |
| **2509.03312** | **AgenTracer: Who Is Inducing Failure in the LLM Agentic Systems?** | **Guibin Zhang, Junhao Wang, Junjie Chen, Wangchunshu Zhou, Kun Wang, Shuicheng Yan.** v1 3 Sep 2025, v2 4 Sep 2025, cs.CL/cs.MA. No venue listed, treat as preprint | **VERIFIED, FULL TEXT READ** | **2026-08-21** | Oracle substitution CONFIRMED for the failed-trajectory branch, but that is only half the method: successful trajectories get programmed fault injection instead. Oracle is approximated by a DeepSeek-R1 analyzer conditioned on the ground-truth solution, not a stored known-good output. Project page: bingreeky.github.io/atracer/ |
| **2606.09692** | **Observability for Delegated Execution in Agentic AI Systems** | **Abhinav Mishra, Kumar Sharad (Splunk / Cisco).** v1 8 Jun 2026, cs.CR/cs.AI, CC BY 4.0 | **VERIFIED, FULL TEXT READ** | **2026-08-21** | Title exactly correct. **The non-identifiability claim is weaker than previously recorded. See correction C3.** Gives R1-R4 semantic requirements and a CIM schema, directly usable for WS6. **No EU AI Act content anywhere: the regulatory bridge is ours to build.** Vendor paper. |
| **2603.10749** | **AttriGuard: Defeating Indirect Prompt Injection in LLM Agents via Causal Attribution of Tool Invocations** | **Yu He, Haozhe Zhu, Yiming Li, Shuo Shao, Hongwei Yao, Zhihao Liu, Zhan Qin.** v1 11 Mar 2026, **v2 10 Jun 2026**, cs.CR | **VERIFIED, FULL TEXT READ** | **2026-08-21** | Title and authors exactly as believed. CLEARED: ex ante runtime guardrail, gates upcoming tool calls via teacher-forced shadow replay of the in-progress prefix. No observability-vs-causal comparison. **Pin v2.** |
| **2602.07918** | **CausalArmor: Efficient Indirect Prompt Injection Guardrails via Causal Attribution** | **Minbeom Kim, Mihir Parmar, Phillip Wallis, Lesly Miculicich, Kyomin Jung, Krishnamurthy Dj Dvijotham, Long T. Le, Tomas Pfister.** v1 8 Feb 2026, cs.CR/cs.LG/stat.ME | **VERIFIED, FULL TEXT READ** | **2026-08-21** | Title and authors exactly as believed. CLEARED: ex ante guardrail, leave-one-out ablation on log-probabilities in a single batched forward pass, no agent re-execution. Check the "Krishnamurthy Dj Dvijotham" string against the PDF byline before setting a BibTeX author field. |
| 2602.10133 | AgentTrace: a structured logging framework for agent system observability | AlSayyad, Huang, Pal 2026 | RECALLED via survey bibliography | 2026-08-15 | Candidate source for a real observability attributor (WS3.3). Verify. |
| 2604.23374 | Ghost in the Agent: redefining information flow tracking for LLM agents | Cai, Tang, Wen, Qin 2026 | RECALLED via survey bibliography | 2026-08-15 | Semantic taint. Verify. |
| 2510.21236 | Securing AI Agent Execution | Bühler, Biagiola, Di Grazia, Salvaneschi 2025 | RECALLED via survey bibliography | 2026-08-15 | Execution boundaries. Relevant to WS2.6 side-effect containment. |
| - | Why do multi-agent LLM systems fail? (MAST) | Cemri, Pan, Yang, Agrawal, Chopra, Tiwari, Keutzer, Parameswaran, Klein, Ramchandran et al. NeurIPS 38 | RECALLED via survey bibliography | 2026-08-15 | Verify. "NeurIPS 38" is a suspicious volume string, check it. |
| 2504.19413 | Mem0: building production-ready AI agents with scalable long-term memory | Chhikara, Khant, Aryan, Singh, Yadav 2025 | RECALLED via survey bibliography | 2026-08-15 | Memory node type context. |
| - | W3C PROV-DM; OpenTelemetry; PROV-AGENT; Agent-Sentry; FIDES; NeuroTaint; CaMeL; AgentSpec; AgentBound; TRAIL; LADYBUG; Aegis; AgentOps | various | RECALLED via survey bibliography | 2026-08-15 | Bulk related-work set. Several load-bearing for WS6 Annex IV schema. Verify individually before any enters the bibliography. |
| 2011.09464 | Counterfactual Credit Assignment in Model-Free RL | T. Mesnard et al., ICML 2021 | RECALLED, seen in TWO independent bibliographies | 2026-08-14 | Via CAR ref [4]. The RL ancestor of the single-action counterfactual. Still verify directly. |
| - | Counterfactual Multi-Agent Policy Gradients (COMA) | J. Foerster et al., AAAI 2018 | RECALLED | 2026-08-13 | Via CAR ref [5]. |
| **Castro et al. 2009** | **Polynomial calculation of the Shapley value based on sampling** | **Javier Castro, Daniel Gómez, Juan Tejada.** *Computers & Operations Research* **36(5):1726-1730**, 2009. **DOI 10.1016/j.cor.2008.04.004** | **VERIFIED (Crossref + dblp)** | **2026-08-21** | All fields confirmed. **Surname carries an accent: Gómez.** Use this rather than Lundberg & Lee for the permutation-sampling estimator, if a Shapley arm returns. |
| 2102.01685 | Agent Incentives: A Causal Perspective | Everitt, Carey, Langlois, Ortega, Legg, AAAI 2021 | RECALLED | 2026-08-13 | Via CAR ref [7]. Causal influence diagrams. |
| 2208.08345 | Discovering Agents | Kenton, Kumar, Farquhar, Richens, MacDermott, Everitt, *Artificial Intelligence* 322, 2023 | RECALLED | 2026-08-13 | Via CAR ref [8]. |
| - | Engineering Record and Replay for Deployability | O'Callahan, Jones, Froyd, Huey, Noll, Partush, USENIX ATC 2017 | RECALLED | 2026-08-13 | Via CAR ref [10]. The record-replay discipline the harness is built on. |
| **He & TML 2025** | **Defeating Nondeterminism in LLM Inference** | **Horace He and Thinking Machines Lab.** *Thinking Machines Lab: Connectionism*, 10 Sep 2025. **DOI 10.64434/tml.20250910** | **VERIFIED, FULL TEXT READ** | **2026-08-21** | Author-supplied BibTeX taken from the page. **Materially changes the replay-floor design. See correction C4.** |
| **Pearl 2001** | **Direct and Indirect Effects** | **J. Pearl.** *Proc. 17th Conf. on Uncertainty in Artificial Intelligence (UAI 2001)*, Morgan Kaufmann, pp. 411-420 | **VERIFIED (dblp)** | **2026-08-21** | **This, not Causality 2009, is the standard primary citation for the natural direct effect.** See correction C5. |
| **Pearl 2009** | **Causality: Models, Reasoning, and Inference**, Cambridge University Press, **2nd edition**, 2009 | **J. Pearl.** ISBN 9780521895606, DOI 10.1017/CBO9780511803161, xix+464pp | **VERIFIED (Stanford library record + CUP catalogue)** | **2026-08-21** | Upgraded from VERIFIED-SECONDARY. Natural direct effects are **section 4.5.4**, mediation formula **4.5.5**, chapter 4. Section 4.5 is 2nd-edition material: citing the 1st edition (2000) would be wrong. |
| **Robins & Greenland 1992** | **Identifiability and exchangeability for direct and indirect effects** | *Epidemiology* **3(2):143-155**, 1992. DOI 10.1097/00001648-199203000-00013, PMID 1576220 | **VERIFIED (PubMed)** | **2026-08-21** | Priority for the natural/pure direct effect concept, predating Pearl's counterfactual formalisation. Cite if the paper makes any priority claim about the estimand. |
| 2407.08734 | Transformer Circuit Faithfulness Metrics Are Not Robust | COLM 2024 | VERIFIED in P1 | (P1) | Cross-cite for the resample-over-remove argument. |
| Shapley 1953; Lundberg & Lee | Shapley value; SHAP | - | RECALLED | - | Verify before citing. Castro et al. 2009 is the better estimator citation and is now verified. |
| Reg (EU) 2024/1689 | Arts. 11, 12, 13, 86; Annex III, Annex IV | Primary text | - | - | Read the regulation, not summaries. Article 86 (right to explanation) added: it is the hook for attributing correct decisions, not only failures. **Now the only load-bearing unverified item for WS6.** |

---

## Corrections from the 2026-08-21 sweep

### C1. 2509.08682 was wrong in two fields. This is the one that mattered.

Recorded as *"Automatic Failure Attribution and Critical Step Prediction via
Causal Inference"* by *"Y. Ma et al."*. Both wrong.

- Actual title: *Automatic Failure Attribution and Critical Step Prediction
  **Method for Multi-Agent Systems Based on** Causal Inference*
- Actual first author: **Guoqing Ma (G. Ma)**, not Y. Ma. The only "Y." initial in
  the author list belongs to **Yidan Liang**, the *last* author.

This is exactly the failure mode standing rule 1 exists to prevent, and it
survived eight days in the ledger marked RECALLED. It was caught only because
the sweep re-derived the metadata from the arXiv API rather than trusting the
existing row.

On the substance it is **not a threat**. Verified from the full text: attribution
is computed from static logs via learned causal graph plus ACE; the do-expression
is evaluated against the learned model, not by re-running agents; the single
re-execution in the paper is downstream repair validation. `mediat*` = 0,
`direct effect` = 0, `indirect` = 0 occurrences. Shapley is over **agents** as
coalition players, not over steps. `EU AI Act` = 0, `Annex` = 0.

One qualification to carry: it does compare LLM-as-Judge trace-reading baselines
against its causal framework, and characterises them as relying on
"surface-level correlations". But **both arms are scored against human
annotation, not against a causally measured ground truth**, so it is not a
measurement of whether observability tracks causation. There is also one
unquantified qualitative sentence noting baselines "often misattribute the
failure to downstream 'symptoms' (e.g., the final agent that produced an
error)". A reviewer could raise that as anticipating our terminal-action
attributor. It has no experiment behind it. Pre-empt it in related work rather
than waiting to be asked.

### C2. The 14.2% Who&When figure is real, and three ways of citing it are wrong

Verified: the sentence *"The best method achieves 53.5% accuracy in identifying
failure-responsible agents but only 14.2% in pinpointing failure steps, with some
methods performing below random"* appears verbatim in the abstract. The string
"14.2" appears **exactly once in the whole paper, in the abstract**, in no table.

It is the mean of four Table 1 cells (Step-by-Step, GPT-4o, step-level accuracy):
25.51, 7.02, 15.31, 8.77, mean 14.15. This is licensed by the paper's own stated
convention that results are averaged across the with/without-ground-truth
scenarios. The companion 53.5% checks out the same way.

Do not write any of these:
1. *"14.2% is the best step-level accuracy reported"* - false, the best single
   cell is **25.51%**.
2. *"~14%"* attached to a table cell - there is no 14.2 cell. Nearest lookalikes
   are 14.66 (Table 2, tolerance ±1, hand-crafted) and 15.31 (Table 1). Do not
   conflate.
3. 14.2% as the figure for realistic traces - **on hand-crafted long logs it is
   7.02 and 8.77**, against a random baseline of 4.16, and the best hybrid in
   Table 3 reaches only 12.28%.

Point 3 is worth taking seriously rather than treating as a caveat: if P2's
argument concerns realistic long-horizon traces, the honest number is
**single-digit**, which is *stronger* for the thesis than 14.2%. Cite it
precisely and the argument improves.

### C3. The delegation non-identifiability result is narrower than recorded

Recorded as "proves a non-identifiability result about audit logs and delegation
scope". Directionally right, imprecise in a way a reviewer would catch.

What is proven non-identifiable is the **authorization relation
`R_auth ⊆ D × E`**, the assignment of each observed event to the delegation under
which it executed. Not "delegation scope" as a semantic object. It is a
**Proposition (2.1), not a Theorem**, and the proof works by defining an
observation function `F` that discards `R_auth` and then noting `F` is not
injective in that argument.

So it is a **scoping result, not a deep impossibility barrier**: it establishes
that the standard observable set is insufficient, given a formalisation in which
the standard observable set was defined to exclude the quantity. It does not
prove that no enrichment of logs short of a gateway could recover `R_auth`, and
says nothing about approximate or statistical recovery.

**Cite it as:** "the target quantity is latent in standard telemetry and must be
bound at execution time". **Do not cite it as:** "causal attribution from logs is
impossible". The second would be overclaiming on our side and is easy to refute.

Two further flags. The paper has **zero** occurrences of "AI Act", "Annex",
"regulat\*", "conformity", or "record-keeping" - the regulatory bridge is
entirely ours to build and must not be attributed to them. And both authors are
Splunk/Cisco, advocating a CIM adjacent to a commercial observability product
line; disclose that if their empirical numbers are cited as neutral evidence.
Their reconstruction metrics report percentiles but no seeds and no CIs, so
programme rule 5 applies to anything built on them.

### C4. The replay floor needs batch invariance, not single-stream inference

`docs/DERIVATIONS.md` section 14 previously listed the preconditions for CRN
replay as "per-request seed control, single-stream inference, fixed vocabulary
order". The middle item was our inference and the source does not support it.

Verified from the primary source: the forward pass is *already* run-to-run
deterministic; the concurrency-plus-floating-point explanation is explicitly
rejected; the real cause is **lack of batch invariance under nondeterministically
varying server load**. Temperature 0 plus a fixed seed is **not sufficient** -
their own measurement gives 80 unique completions from 1000 temperature-0 samples
of one prompt, identical for 102 tokens then diverging, collapsing to 1 unique
completion once batch-invariant kernels are used.

The stated remedy is batch-invariant kernels. Single-stream inference removes the
symptom by holding batch size constant but is never claimed as a requirement, and
citing the post for it would be putting words in the source. Determinism is also
explicitly **not** hardware or software version invariant.

Consequence, now written into DERIVATIONS section 15: Gate C is not "can we
replay", it is "can we obtain batch-invariant inference on the serving stack we
have". If not, `ME` carries a noise floor that belongs to the infrastructure
rather than to the system under study.

### C5. Pearl 2009 alone is not the strongest attribution for the natural direct effect

Pearl 2009 is now fully VERIFIED against a library record (Stanford) and the CUP
catalogue rather than against CAR's bibliography, and the relevant sections are
located: **4.5.4** natural direct effects, **4.5.5** indirect effects and the
mediation formula. Section 4.5 is 2nd-edition material, so the edition matters.

But the standard primary citation for the definition is **Pearl (2001), "Direct
and Indirect Effects", UAI 2001, pp. 411-420**, with **Robins & Greenland (1992)**
holding priority on the underlying concept. `docs/DERIVATIONS.md` section 4 now
cites all three in that order. Citing Pearl 2009 alone was defensible; citing the
1st edition would have been wrong.

---

### C6. A citation entered committed code without entering this ledger

Found 2026-08-23, and worth recording as a process failure rather than quietly
fixing, because it is the exact failure this ledger exists to prevent and it was
committed by the same session that wrote the sweep above.

The `normalized_beta` docstring in `src/p2/ranking.py`, added in commit
`6b3d2f6` (2026-08-20), contains the parenthetical "(Fieller 1954)" as the
authority for the ratio-of-normals argument. **That reference was never added
to this ledger.** It went into committed source, in the justification for the
paper's headline reporting convention, in a RECALLED state, and it would have
travelled from the docstring into the manuscript's methods section without ever
being checked.

It was caught by a different session (commit `4e8de3c`), which logged it as
RECALLED with the correct instruction to verify before use. Verified today
against the JRSS-B record and now upgraded.

**The lesson is about scope, not about Fieller.** The rule as practised was
"nothing enters a *manuscript* until it appears here as VERIFIED". Code
docstrings were treated as outside that boundary. They are not: a docstring that
justifies a pre-registered analysis choice is a load-bearing citation, and in
this project docstrings are where the methodological arguments are actually
written. The rule at the top of this file should be read as covering **any
committed artifact**, source included.

A cheap mechanical check: grep the source tree for author-year patterns and
confirm each appears here. Worth adding to `verify.sh` rather than relying on
noticing.

## Numbers not to reuse without checking

- "73.4 SWE-Bench Verified" for a 35B-class MoE: RECALLED from a comparison site. Not a primary model card. **Still unverified.**
- "Gemma 3 27B runs on one RTX 4090": RECALLED, same source. **Still unverified.**
- "approximately 14 percent step-level attribution accuracy on Who&When": **VERIFIED 2026-08-21 against the primary source.** It is 14.2%, it is a four-cell average, it appears only in the abstract, and it is 7.02/8.77 on realistic long logs. See correction C2 for the three wrong ways to cite it.
- CAR Shapley validation figures (phi_0 = 0.44, phi_1 = 0.45, phi_2 approx 0, efficiency sum 0.909 vs analytic 0.91): VERIFIED from the full text. Synthetic SCM, not a real system.
- 2606.09692 reconstruction metrics (CIM ambiguity 1 by construction; B2 median ambiguity 1543 / 107718 / 1107; B0 delegation recall 0.06 / 1 / 0.04): VERIFIED from the full text, but **percentiles only, no seeds, no CIs**, and it is a vendor paper. Programme rule 5 applies.

## Still RECALLED and load-bearing, ranked by risk

1. **Reg (EU) 2024/1689** primary text, Arts. 11, 12, 13, 86 and Annex IV. The
   entire WS6 deliverable rests on it and no verified reading exists yet. Nothing
   else on this list is close in importance.
2. 2602.10133 AgentTrace and 2604.23374 Ghost in the Agent, both candidate
   sources for observability attributor provenance (WS3.3).
3. The bulk survey-bibliography set (PROV-DM, PROV-AGENT, OpenTelemetry
   semantic conventions, and the rest). Several are load-bearing for the WS6
   schema and each needs an individual check.
4. MAST, whose recorded venue string "NeurIPS 38" looks wrong on its face.
5. 2011.09464 Mesnard et al. and COMA, both seen only through bibliographies.

## Process note, 2026-08-21

One verification agent reported that its working file in a shared scratchpad was
**overwritten mid-task by a concurrent process**, with several files it had not
created appearing alongside. It detected the substitution because the content
stopped matching, re-fetched into an isolated directory, and re-derived every
count and quote from the clean copy. All findings above come from the clean
re-extraction.

Two lessons, both cheap to act on. Parallel verification runs must use isolated
working directories, not a shared scratchpad with generic filenames, because
cross-contamination between two citation checks is silent and would be very hard
to detect after the fact. And the incident is itself an argument for the discipline
already in force here: every claim in this sweep carries a URL and an exact quote,
so a contaminated intermediate could be caught and discarded rather than
propagating into the bibliography.
| **Fieller 1954** | **Some Problems in Interval Estimation** | **E. C. Fieller.** *Journal of the Royal Statistical Society: Series B (Methodological)* **16(2):175-185**, July 1954. **DOI 10.1111/j.2517-6161.1954.tb00159.x** | **VERIFIED** | **2026-08-23** | Upgraded from RECALLED. Confirmed against the Oxford Academic JRSS-B record, corroborated by the Wiley DOI landing page and the JSTOR volume listing for Vol. 16 No. 2 (1954). Cited in the `normalized_beta` docstring as the reason a ratio to a near-zero coefficient has heavy tails and a possibly unbounded interval. **Logged only because another session caught it: it was referenced in committed code without ever entering this ledger.** See correction C6. |
