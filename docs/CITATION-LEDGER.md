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
| **Reg (EU) 2024/1689** | **Regulation (EU) 2024/1689 (Artificial Intelligence Act)** | **Consolidated text as at 27 July 2026, CELEX 02024R1689-20260727** | **PARTIALLY VERIFIED** | **2026-08-23** | Art. 113, Art. 6(1)-(2), Annex III pt 5, Art. 11(1) 2nd subpara: **VERBATIM, see `docs/REGULATORY-BASIS.md`**. Arts. 11 (full), 12, 13, 18(1), 19, 26, 86 and Annex IV (full): **RETRIEVED VERBATIM 2026-08-25** via the Publications Office repository, see `docs/REGULATORY-BASIS.md`. This row read NOT RETRIEVED until 2026-09-03; the retrieval had happened and the ledger had not been updated. **Still not retrieved:** Arts. 25, 72, 74, 79(1) and the Art. 3 definitions. Consolidated text carries "no legal effect"; quote the OJ text for anything load-bearing. |
| **Reg (EU) 2026/1744** | **Regulation (EU) 2026/1744 of 8 July 2026 amending Regulations (EU) 2024/1689, (EU) 2018/1139 and (EU) 2023/1230 as regards the simplification of the implementation of harmonised rules on artificial intelligence (Digital Omnibus on AI)** | **European Parliament and Council. OJ L series, 2026/1744, 24.7.2026. In force 27 July 2026** | **VERIFIED, PRIMARY TEXT** | **2026-08-23** | **PROGRAMME-ALTERING. Art. 1(40) defers Chapter III Sections 1-3 to 2 Dec 2027 (Annex III) and 2 Aug 2028 (Annex I).** Arts. 11, 12, 13 and Annex IV are therefore NOT in application today. Only four articles exist: cite **Article 1(40)**, never "Article 40". **Recital (40) is separate, non-binding, and is the strongest regulatory hook the programme has.** See correction C7. |

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

### C7. The AI Act obligations this paper is about are not in application

Found 2026-08-23. The largest single correction the ledger has recorded, and it
changes paragraph one.

**Regulation (EU) 2026/1744**, the "Digital Omnibus on AI", adopted 8 July 2026
and in force 27 July 2026, amended Article 113 of the AI Act. Chapter III
Sections 1, 2 and 3 now apply from **2 December 2027** for Annex III high-risk
systems and 2 August 2028 for Annex I. Articles 11, 12 and 13 sit in Chapter III
Section 2, and Annex IV is operative only through Article 11(1), so all of them
are deferred.

**The original brief's claim "the AI Act applies to them now" is FALSE** as of
today for every provision this paper is built on. It survives only in
`paper-2-agentic-attribution.md`; the repo documents never asserted it, which is
the one piece of luck here.

Three things follow.

1. **Do not trust any secondary source on AI Act dates.** Almost all of them
   predate the Omnibus and still say 2 August 2026. This includes law-firm
   briefings published as recently as May 2026, one of which was consulted this
   session and described the change as a *proposal* because at the time it was.
   Only EUR-Lex, and only with the publication date checked.

2. **The framing improves rather than weakens.** A conformity specification
   published in 2026 for an obligation that bites in December 2027 arrives when
   it can still be adopted, and Article 11(1) as amended now requires the
   Commission to produce a simplified technical documentation form for SMEs that
   does not yet exist. The deliverable has a live target.

3. **Recital (40) of 2026/1744 is a gift to the programme thesis** and should be
   in paragraph one of all three papers. The legislature's stated reason for the
   deferral, verbatim: "the delayed availability of standards, common
   specifications, and alternative guidance and the delayed establishment of
   national competent authorities lead to challenges that jeopardise the
   effective entry into application of those obligations". That is the Union
   saying on the record that the apparatus for demonstrating conformity was not
   ready. Cite as a **recital**: explanatory, non-binding, never as operative law.

**A citation trap worth stating explicitly.** Regulation (EU) 2026/1744 has only
four articles. Recital (40) and Article 1 point (40) both exist and concern the
same subject. "Article 40" does not exist. The binding amendment is **Article
1(40)**. A paper about regulatory evidence that miscites a regulation loses the
argument before it starts.

Full verbatim record, with URLs and epistemic markers, in
`docs/REGULATORY-BASIS.md`.

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

---

## Additions from the 2026-09-04 novelty sweep

Searched because the draft made three novelty claims that had not been checked.
One of them was wrong. Recorded per standing rule 3.

| ref | Title | Authors / venue | Status | Checked | Note |
|---|---|---|---|---|---|
| **MacKinnon, Warsi & Dwyer 1995** | **A Simulation Study of Mediated Effect Measures** | **D. P. MacKinnon, G. Warsi, J. H. Dwyer.** *Multivariate Behavioral Research* **30(1):41-62**, 1995. **DOI 10.1207/s15327906mbr3001_3**, PMID 20157641 | **VERIFIED** | **2026-09-04** | Volume, issue and pages agree across Taylor & Francis, PubMed, ERIC and the Google Scholar record. **PRIOR ART for the section 6 proposition.** The instability of the proportion mediated when the total effect is small is theirs, not ours. |
| **MacKinnon, Krull & Lockwood 2000** | **Equivalence of the Mediation, Confounding and Suppression Effect** | **D. P. MacKinnon, J. L. Krull, C. M. Lockwood.** *Prevention Science* **1:173-181**, 2000. **DOI 10.1023/A:1026595011371** | **VERIFIED** | **2026-09-04** | Confirmed against Springer, the ASU research record and Semantic Scholar. **Issue number NOT confirmed: do not state one.** Establishes suppression and mediation as the same algebra. |
| **Kenny (mediation resource)** | **Mediation** (davidakenny.net/cm/mediate.htm) | **D. A. Kenny.** Web resource, not peer reviewed | **VERIFIED (fetched)** | **2026-09-04** | Source of the verbatim "inconsistent mediation" naming and "this measure can be greater than one or even negative". **Cite as a secondary/tertiary source only; the primary attribution is MacKinnon et al.** |
| **Levin, Peres & Wilmer** | **Markov Chains and Mixing Times** | **D. A. Levin, Y. Peres, E. L. Wilmer.** American Mathematical Society. 1st ed. 2009, ISBN 9780821847398; **2nd ed. 2017, ISBN 9781470429621** | **VERIFIED (AMS + publisher records)** | **2026-09-04** | For the maximal coupling bound `1 - TV`. **NO chapter, section or proposition number has been verified. Do not add one without checking the text.** |
| **Law & Kelton** | **Simulation Modeling and Analysis** | **A. M. Law, W. D. Kelton.** McGraw-Hill. 3rd ed. 2000 recorded by multiple citation records; earlier ed. ISBN 9780070366985 | **VERIFIED (edition ambiguous)** | **2026-09-04** | For common random numbers as a variance-reduction technique. **Pick one edition and check its CRN chapter before the bibliography is frozen.** |
| 2605.04732 | Using Common Random Numbers for Simulation-based Planning with Rollouts | Sandarbh Yadav, Frederic J Maliakkal, Harshad Khadilkar, Shivaram Kalyanakrishnan. v1 6 May 2026 | **VERIFIED, abstract read** | **2026-09-04** | **CLEARED.** CRN for variance reduction in rollout-based planning. No coupling agreement probability, no quantile-versus-maximal comparison, no attribution, direct effects or mediation. Cite as adjacent work on CRN in rollouts. |

### What the sweep changed

**Section 6 was claiming a known result.** The proposition that `|ME|/|TE| > 1`
under opposing signs is the proportion-mediated instability of MacKinnon et al.
(1995), and the configuration is standardly called inconsistent mediation. The
section is demoted to a restatement with attribution.

**Sections 3 and 5 were at risk of the same error.** Common random numbers and
maximal coupling are both classical. Neither is claimed as novel; both are cited.

**What remains genuinely ours, and is now stated with "to our knowledge":** the
closed form for shared-`u` quantile-coupling agreement in fixed index order and
the measured gap against the maximal bound. A search for it returned nothing
directly on point, but it is an elementary computation and the honest phrasing is
that we have not found it stated for this purpose, not that it does not exist.

---

## Full pre-arXiv verification sweep, 5 September 2026

Run under the `citation-verify` standard: **VERIFIED means fetched this session
and every field confirmed against the fetched record.** A prior verified row does
not carry over. Thirteen arXiv identifiers in `paper/refs.bib` were re-fetched;
`2608.13754` was fetched earlier the same session.

**Result: 12 confirmed, 4 discrepancies found and corrected, 2 not re-verifiable.**

| ID | State | Verified on | Notes |
|---|---|---|---|
| 2606.08275 | **VERIFIED** | 2026-09-05 | Title, sole author Jaineet Shah, 6 Jun 2026, v1, cs.LG all match |
| 2605.25338 | **VERIFIED** | 2026-09-05 | All five authors and order match; 25 May 2026, v1, cs.LG |
| 2606.04990 | **VERIFIED, CORRECTED** | 2026-09-05 | **AUTHOR ORDER WAS WRONG.** See D1 |
| 2505.00212 | **VERIFIED (record), DISPUTED (venue)** | 2026-09-05 | Title and all 11 authors match. **Venue unconfirmed.** See D2 |
| 2509.03312 | **VERIFIED** | 2026-09-05 | Six authors and order match; v2 4 Sep 2025, cs.CL |
| 2509.08682 | **VERIFIED** | 2026-09-05 | Seven authors and order match; 10 Sep 2025, v1, cs.AI |
| 2607.20827 | **VERIFIED** | 2026-09-05 | Sole author Junchi Liao; 23 Jul 2026, v1, cs.AI |
| 2603.10749 | **VERIFIED, ENRICHED** | 2026-09-05 | **Venue found that we never had.** See D3 |
| 2602.07918 | **VERIFIED** | 2026-09-05 | All eight authors match, including the "Krishnamurthy Dj Dvijotham" spelling the August row flagged for checking. Now checked |
| 2607.25364 | **VERIFIED** | 2026-09-05 | Both authors; v2 29 Jul 2026; Comments "25 pages, 1 figure, 15 tables" |
| 2605.04732 | **VERIFIED, ENRICHED** | 2026-09-05 | **Journal reference found.** See D4 |
| 2608.13754 | **VERIFIED** | 2026-09-05 | P1. Ajay Pravin Mahale (Hochschule Trier), 13 Aug 2026, v1, cs.AI |
| **2606.09692** | **NOT RE-VERIFIED** | attempted 2026-09-05 | See N1 |
| **2605.09168** | **NOT RE-VERIFIED** | attempted 2026-09-05 | See N1 |

### D1. 2606.04990, author order was wrong in the bibliography and in this ledger

Recorded here on 2026-08-15 and written into `refs.bib` as: Yiqi Wang, Jiaqi
Zhang, **Zhangkai Wu**, Taotao Cai, Zirui Liu, Qingqiang Sun, Zequn Sun, ...

The arXiv listing gives: Yiqi Wang, Jiaqi Zhang, Taotao Cai, Zirui Liu,
Qingqiang Sun, Zequn Sun, **Zhangkai Wu**, Manqing Dong, Mingkai Zheng, Xuefei
Yin, Yanming Zhu.

**Zhangkai Wu was in position 3 and belongs in position 7.** Corrected in
`refs.bib` on 2026-09-05. Order is not cosmetic: it determines et-al truncation
and it misstates a co-author's contribution. Submission date also corrected: the
paper was submitted 3 June 2026, with v4 on 28 June; the ledger recorded only the
v4 date.

### D2. 2505.00212, the venue claim could not be re-confirmed

The August row states "ICML 2025, PMLR v267, pp. 76583-76599", said to have been
confirmed against PMLR directly.

Today: PMLR volume 267 **is** confirmed to be ICML 2025, the 42nd International
Conference on Machine Learning, Vancouver, 13-19 July 2025. But the paper could
not be located in the volume index in the retrieved portion, and the arXiv
Comments field reads only "camera-ready" with no venue named.

**State: DISPUTED on the venue, VERIFIED on the record.** The page range is now
marked in `refs.bib` as pending re-confirmation. Per the skill's rule on numbers
that cannot be located, confirm the page range directly or fall back to the
arXiv form before submission anywhere.

### D3. 2603.10749, a venue we did not have

The arXiv Comments field reads **"Accepted by USENIX Security 2026"**. Neither
this ledger nor the bibliography recorded it, and the paper was being cited as a
bare preprint. Added.

### D4. 2605.04732, a journal reference we did not have

The arXiv listing carries the journal reference **"Reinforcement Learning
Journal 2026"**. Not previously recorded. Added, along with the primaryClass
field, which was missing from the entry entirely.

### N1. Two entries could not be re-verified, and are named rather than assumed

`2606.09692` (Observability for Delegated Execution in Agentic AI Systems) and
`2605.09168` (CIVeX) both return no machine-readable text to the fetch tool; each
was attempted twice. This is a tool limitation, not evidence of a problem: both
carry VERIFIED, FULL TEXT READ rows from 2026-08-13 and 2026-08-21 with URLs.

Per the skill's failure rule, a blocked fetch is **not** routed around and the
state is **not** upgraded. Both are cited in the manuscript.

**Therefore this bibliography must not be described as fully checked.** It is 12
of 14 re-verified today, with 2 resting on an August verification that could not
be refreshed. Resolving it takes two minutes in a browser: open both abstract
pages and confirm title and author list against `refs.bib`.

### Process note

Two of the four discrepancies were things we did not have rather than things we
had wrong, and both make the citations stronger. The author-order error is the
one that mattered: it had survived three weeks and two prior sweeps, because
every earlier check confirmed that the paper existed rather than that our
transcription of it was right.

---

## 2026-09-05, second pass. The ledger closes, and one entry was wrong

The 4 September sweep ended with the sentence "**this bibliography must not be
described as fully checked**", because two entries rested on an August check
that could not be refreshed. Both have now been read against their arXiv
records. The check took four minutes, not the two it was estimated at, and it
found something.

| ID | Field checked | Record says | Entry said | State |
|---|---|---|---|---|
| 2606.09692 | title | Observability for Delegated Execution in Agentic AI Systems | same | `VERIFIED` |
| 2606.09692 | authors | Abhinav Mishra, Kumar Sharad | same, same order | `VERIFIED` |
| 2606.09692 | primary class | cs.CR (also cs.AI) | cs.CR | `VERIFIED` |
| 2606.09692 | version | v1 only, submitted 8 Jun 2026 | not recorded | **added** |
| 2605.09168 | title | CIVeX: Causal Intervention Verification for Language Agents | same | `VERIFIED` |
| 2605.09168 | authors | Fabio Rovai, sole author | same | `VERIFIED` |
| 2605.09168 | primary class | cs.AI (also cs.LG) | **absent** | **added** |
| 2605.09168 | version | v1 only, submitted 9 May 2026 | not recorded | **added** |
| 2605.09168 | note | Comments: 16 pages, 3 figures | **"The Tesseract Academy"** | **CORRECTED** |

**The correction that matters.** The `civex2026` note asserted the affiliation
"The Tesseract Academy". That string appears nowhere on the arXiv record: not in
the author line, not in Comments, not in the journal reference. It may well be
true, but it was an unsourced field sitting in a bibliography whose entire
discipline is that fields come from the source. It is replaced by the Comments
field, which is on the record. Where it came from is not recoverable from the
ledger, which is itself the lesson: a field added without a row here cannot be
audited later.

**Every entry in `paper/refs.bib` is now `VERIFIED` against a primary record.**
The header sentence in that file which said otherwise has been replaced rather
than deleted.

### Regulatory sources, upgraded from VERIFIED-SECONDARY to primary

Part IV of `docs/REGULATORY-BASIS.md` recorded Articles 86 and 73(6) as
`VERIFIED-SECONDARY`, because the EUR-Lex consolidated HTML truncates inside
Article 26 and the OJ PDF truncates inside the recitals, so neither could be
read through to them.

Both were retrieved on 5 September from
`https://eur-lex.europa.eu/legal-content/EN/TXT/HTML/?uri=CELEX:32024R1689`, the
**original Official Journal text**, by restricting the extraction to the
document's own `art_86`, `art_73`, `cpt_IX.sct_2` and `cpt_IX.sct_4` elements
instead of requesting the whole 800-page document and being truncated. The
element identifiers are themselves the proof of placement: Article 86 is inside
`cpt_IX.sct_4`, headed "SECTION 4 / Remedies", between Articles 85 and 87;
Article 73 is inside `cpt_IX.sct_2`, headed "SECTION 2 / Sharing of information
on serious incidents".

| Source | Was | Now | Discrepancy against the secondary read |
|---|---|---|---|
| Article 86(1)-(3) | `VERIFIED-SECONDARY` | `VERIFIED` primary | none, character for character |
| Article 73(6), both subparagraphs | `VERIFIED-SECONDARY` | `VERIFIED` primary | none, character for character |
| Article 86 in Chapter IX Section 4 | inferred | `VERIFIED` primary | none |
| Article 73 in Chapter IX Section 2 | inferred | `VERIFIED` primary | none |

Nothing had to be corrected. That is worth recording too: two independent
secondary reads agreed with the primary text, which is evidence about the
sources as well as about the quotations.

**Note for anyone repeating this.** The reason three earlier attempts failed is
that the fetchers truncate a large document from the beginning, and the AI Act's
recitals alone exhaust the budget. Requesting the specific element by its
identifier returns the article and nothing else. That technique is the finding;
it should be the first thing tried on any EUR-Lex article, not the fourth.

### The pre-submission list is now empty

All four items carried since 4 September are closed. Nothing in the manuscript
or the regulatory analysis now rests on a source that was not read from its
primary record this week.

## Retrievals of 2026-09-06, pre-arXiv

| ID | Exact title as fetched | Authors | Venue | Date | State | Verified on | Source URL | Notes |
|---|---|---|---|---|---|---|---|---|
| C(2025) 3871 final | COMMISSION IMPLEMENTING DECISION on a standardisation request to the European Committee for Standardisation and the European Committee for Electrotechnical Standardisation as regards high-risk AI-systems in support of Regulation (EU) 2024/1689 of the European Parliament and of the Council and repealing Implementing Decision C(2023)3215 | European Commission | Register of Commission Documents; standardisation request M/613 | 23 June 2025 | VERIFIED | 2026-09-06 | ec.europa.eu/transparency/documents-register, files C(2025)3871_0 and C(2025)3871_1 | Body (7pp) and ANNEXES 1 to 2 (8pp) both read. Annex II point 2.3 quoted verbatim in the paper. |
| C(2023) 3215 final | ANNEXES to the COMMISSION IMPLEMENTING DECISION on a standardisation request ... in support of Union policy on artificial intelligence | European Commission | standardisation request M/593 | 22 May 2023 | **SUPERSEDED** | 2026-09-06 | ec.europa.eu/growth/tools-databases/enorm/mandate/593_en | **Repealed** by Article 4 of C(2025) 3871. A draft of Section 8 quoted it as operative. Withdrawn from the manuscript. Retained here so the correction is on the record, not erased. |
| Art. 40, Reg. (EU) 2024/1689 | Harmonised standards and standardisation deliverables | European Parliament and Council | OJ L, 2024/1689, 12.7.2024 | 13 June 2024 | VERIFIED primary | 2026-09-06 | eur-lex CELEX:32024R1689, element `art_40` | Art. 40(1) quoted in docs/REGULATORY-BASIS.md Part VI. |
| Art. 41, Reg. (EU) 2024/1689 | Common specifications | European Parliament and Council | OJ L, 2024/1689, 12.7.2024 | 13 June 2024 | VERIFIED primary | 2026-09-06 | eur-lex CELEX:32024R1689, element `art_41` | Read whole. Not quoted in the paper; summarised in Part VI. |
| prEN 18229-1 status | AI Trustworthiness Framework - Part 1: Logging, in public hearing (Enquiry) until 20 August 2026 | CEN-CENELEC JTC 21 secretariat | jtc21.eu notice of 9 July 2026 | 9 July 2026 | VERIFIED | 2026-09-06 | jtc21.eu/significant-milestone-for-european-ai-standardization/ | Status only. The draft's **content** is NOT RETRIEVED and cannot be: CEN drafts at enquiry are not public. |
| arXiv 2608.13754 | Explanation Multiplicity: Circuit-Level Interpretability Evidence Does Not Survive Defensible Analytic Variation | Ajay Pravin Mahale | arXiv, cs.AI | v1, 13 August 2026 | VERIFIED (re-check) | 2026-09-06 | arxiv.org/abs/2608.13754 | Title, author, date, class all match refs.bib. The 73.2% figure the paper attributes to it appears on the abstract page. |
| arXiv 2606.08275 | Causal Agent Replay: Counterfactual Attribution for LLM-Agent Failures | Jaineet Shah | arXiv, cs.LG | v1, 6 June 2026 | VERIFIED (re-check) | 2026-09-06 | arxiv.org/abs/2606.08275 | Matches refs.bib field for field. |
| arXiv 2606.04990 | From Agent Traces to Trust: A Survey of Evidence Tracing and Execution Provenance in LLM Agents | Yiqi Wang et al., 11 authors | arXiv, cs.CR | submitted 3 June 2026, v4 28 June 2026 | VERIFIED (re-check) | 2026-09-06 | arxiv.org/abs/2606.04990 | Author list and both dates match refs.bib. |

**Correction recorded, not erased.** A draft paragraph in Section 8 quoted a
repealed standardisation request and drew a word-count comparison across its ten
deliverables, including a "median of 115" that was in fact the sixth value of a
ten-element sorted list. Both the instrument and the statistic are gone from the
manuscript. `scripts/validate_standardisation_request.py` now pins the quotation
to the committed primary text and fails if the paper names the repealed
instrument without saying it was repealed.
