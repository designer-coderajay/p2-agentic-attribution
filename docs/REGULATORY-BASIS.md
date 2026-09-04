# Regulatory basis for WS6

Primary-text foundation for the Annex IV traceability specification. Every legal
quotation below was retrieved from EUR-Lex on **2026-08-23** and is marked
verbatim. Nothing here comes from a law-firm summary, a tracker site, or
recollection. Where a claim is structural inference rather than quotation it
says so.

**Read the epistemic markers.** `VERBATIM` means the exact words were retrieved
this session with a URL. `STRUCTURAL` means it follows from the document's own
organisation, which was inspected, but is a reading rather than a quotation.
`INFERRED` means it is my reasoning about consequences.

---

## 0. The headline finding, and it changes paragraph one

**The obligations this paper is about are not in application, and will not be
until 2 December 2027.**

Regulation (EU) 2024/1689 was amended by **Regulation (EU) 2026/1744** of 8 July
2026, the "Digital Omnibus on AI", published in the Official Journal on
24 July 2026 and in force from 27 July 2026. It moved the date of application of
Chapter III Sections 1, 2 and 3 from 2 August 2026 to:

| Class | Applies from |
|---|---|
| Annex III high-risk (Article 6(2)), which includes credit scoring | **2 December 2027** |
| Annex I high-risk (Article 6(1)) | **2 August 2028** |

Articles 11 (technical documentation), 12 (record-keeping) and 13 (transparency)
sit inside Chapter III Section 2, and Annex IV is operative only through Article
11(1). All of them are therefore deferred to **2 December 2027** for a credit
underwriting system.

**What this kills.** The original brief states: "Agentic systems are the 2026
deployment story, the AI Act applies to them now". As of 23 August 2026 that is
**false** for the provisions this paper is built on. It must not survive into the
manuscript, and it must be corrected in
`paper-2-agentic-attribution.md`. Any secondary source still saying 2 August 2026
for high-risk obligations predates the Omnibus and is now wrong, which is most of
them.

**What this does not kill.** The Regulation is enacted law, in force since 1
August 2024, with a deferred application date. Systems being built now are being
built against it. A specification published in 2026 for an obligation that bites
in December 2027 is not late, it is early, and early is when a conformity
specification is actually adoptable. This is a better position than the one the
brief claimed, not a worse one, and it is defensible without hedging.

---

## 1. The operative amendment

`VERBATIM`, Regulation (EU) 2026/1744, **Article 1, point (40)**. Source:
https://eur-lex.europa.eu/legal-content/EN/TXT/PDF/?uri=OJ%3AL_202601744

> (40) in Article 113, the third paragraph is amended as follows:
> (a) point (a) is replaced by the following:
> '(a) Chapters I and II shall apply from 2 February 2025, with the exception of Article 5(1), first subparagraph, points (ba) and (bb), and Article 5(1a) and (1b) which shall apply from 2 December 2026;';
> (b) point (c) is replaced by the following:
> '(c) Chapter III, Sections 1, 2, and 3, with the exception of Article 6(5), shall apply from:
> (i) 2 December 2027 as regards AI systems classified as high-risk pursuant to Article 6(2) and Annex III; and
> (ii) 2 August 2028 as regards AI systems classified as high-risk pursuant to Article 6(1) and Annex I;';
> (c) the following point is added:
> '(d) Articles 102 to 110 shall apply from 27 July 2026.';

**Citation discipline, and a trap.** Regulation (EU) 2026/1744 has only four
articles. There is **no "Article 40"**. Recital (40) and Article 1 point (40)
both exist, both concern the same subject, and they are different things: the
recital is explanatory and non-binding, Article 1(40) is the binding amendment.
Cite **Article 1(40)**. Getting this wrong in a paper about regulatory evidence
would be an unusually bad look.

---

## 2. Article 113 as it now stands

`VERBATIM`, consolidated Regulation (EU) 2024/1689 as at 27 July 2026. Source:
https://eur-lex.europa.eu/legal-content/EN/TXT/HTML/?uri=CELEX:02024R1689-20260727

`M1` marks text inserted by Regulation (EU) 2026/1744; `B` marks original 2024 text.

> Article 113
> Entry into force and application
> This Regulation shall enter into force on the twentieth day following that of its publication in the Official Journal of the European Union.
> It shall apply from 2 August 2026.
> However:
> [M1] (a) Chapters I and II shall apply from 2 February 2025, with the exception of Article 5(1), first subparagraph, points (ba) and (bb), and Article 5(1a) and (1b) which shall apply from 2 December 2026;
> [B] (b) Chapter III Section 4, Chapter V, Chapter VII and Chapter XII and Article 78 shall apply from 2 August 2025, with the exception of Article 101;
> [M1] (c) Chapter III, Sections 1, 2, and 3, with the exception of Article 6(5), shall apply from:
> (i) 2 December 2027 as regards AI systems classified as high-risk pursuant to Article 6(2) and Annex III; and
> (ii) 2 August 2028 as regards AI systems classified as high-risk pursuant to Article 6(1) and Annex I;
> [M1] (d) Articles 102 to 110 shall apply from 27 July 2026.
> [B] This Regulation shall be binding in its entirety and directly applicable in all Member States.

The consolidated text carries its own disclaimer, `VERBATIM`: "This text is meant
purely as a documentation tool and has no legal effect." For anything load-bearing
in the manuscript, quote the OJ text of 2024/1689 and of 2026/1744 separately
rather than the consolidation.

---

## 3. Why the deferral happened, in the legislature's own words

This is the most useful paragraph in the whole instrument for this programme, and
it is worth quoting at length. `VERBATIM`, Regulation (EU) 2026/1744,
**recital (40)**, which is **explanatory and NOT binding**:

> (40) Article 113 of Regulation (EU) 2024/1689 establishes the dates of entry into force and application of that Regulation, in particular that the general date of application is 2 August 2026. For the obligations related to high-risk AI systems laid down in Sections 1, 2 and 3 of Chapter III of Regulation (EU) 2024/1689, the delayed availability of standards, common specifications, and alternative guidance and the delayed establishment of national competent authorities lead to challenges that jeopardise the effective entry into application of those obligations and that risk a significant increase in implementation costs in a way that does not justify maintaining their initial date of application, namely 2 August 2026.

`INFERRED`, and it is the strongest regulatory hook the programme has found:
**the Union legislature has stated on the record that it postponed the high-risk
regime because the apparatus for demonstrating conformity was not ready.**
"The delayed availability of standards, common specifications, and alternative
guidance" is an official acknowledgement that the evidence base for a conformity
claim does not yet exist.

That is the programme thesis, stated by the regulator, in the Official Journal.
P1 argues interpretability evidence is not stable enough to support a conformity
claim; P2 argues observability evidence does not track causation; recital (40)
says the Union could not bring the regime into application because the
specifications were missing. Use it in paragraph one of all three papers.

**Cite it correctly or not at all**: recital, non-binding, explanatory. A recital
states reasons; it does not impose obligations. Presenting it as operative law
would be the same category of error this programme is about.

---

## 4. The system class is unchanged

`VERBATIM`, consolidated Annex III. Regulation (EU) 2026/1744 does **not** amend
Annex III: its annex-amending points are (41) Annex I, (42) Annex VIII, (43) a
new Annex XIV, and the consolidated Annex III carries no `M1` marker.

> ANNEX III
> High-risk AI systems referred to in Article 6(2)
> High-risk AI systems pursuant to Article 6(2) are the AI systems listed in any of the following areas:
> [...]
> 5. Access to and enjoyment of essential private services and essential public services and benefits:
> (a) AI systems intended to be used by public authorities or on behalf of public authorities to evaluate the eligibility of natural persons for essential public assistance benefits and services, including healthcare services, as well as to grant, reduce, revoke, or reclaim such benefits and services;
> (b) AI systems intended to be used to evaluate the creditworthiness of natural persons or establish their credit score, with the exception of AI systems used for the purpose of detecting financial fraud;
> (c) AI systems intended to be used for risk assessment and pricing in relation to natural persons in the case of life and health insurance;
> (d) AI systems intended to evaluate and classify emergency calls by natural persons or to be used to dispatch, or to establish priority in the dispatching of, emergency first response services, including by police, firefighters and medical aid, as well as of emergency healthcare patient triage systems.

`VERBATIM`, Article 6(2), unamended:

> 2. In addition to the high-risk AI systems referred to in paragraph 1, AI systems referred to in Annex III shall be considered to be high-risk.

**Consequence for the BFSI system.** A credit underwriting pipeline evaluating the
creditworthiness of natural persons is squarely within Annex III point 5(b), and
therefore Article 6(2) high-risk, and therefore on the 2 December 2027 clock. Note
the carve-out: systems "used for the purpose of detecting financial fraud" are
excluded. If any part of the pipeline is characterised as fraud detection, that
part falls outside. Worth stating explicitly in the paper's system description,
because a reviewer or a notified body will ask.

---

## 5. Article 11(1) was itself amended, and it matters for the deliverable

`VERBATIM`, consolidated Article 11(1), second subparagraph, marked `M1`:

> It shall contain, at a minimum, the elements set out in Annex IV. SMEs, including start-ups, and SMCs, may provide the elements of the technical documentation specified in Annex IV in a simplified manner. To that end, the Commission shall establish a simplified technical documentation form targeted at the needs of SMEs, including start-ups, and SMCs.

`INFERRED`. The Annex IV traceability specification now has a two-tier audience: a
full form, and a Commission-issued simplified form for SMEs and SMCs that does not
yet exist. A specification that addresses only the full form is incomplete, and a
specification published before the Commission's simplified form is an opportunity
to influence it. That is an argument for shipping the deliverable sooner rather
than later, and for saying explicitly which requirements are irreducible even
under simplification.

---

## 6. What is in application on 23 August 2026

`STRUCTURAL`, derived by applying the quoted Article 113 to the Act's chapter
structure. The dates are quoted; the mapping of subject matter to chapter is a
reading of the consolidated headings.

| Subject | Locus | Applies from | Today |
|---|---|---|---|
| Prohibited practices, general provisions, definitions | Ch. I, II | 2 Feb 2025 | in application |
| AI literacy (Art. 4, softened 27 Jul 2026) | Ch. I | 2 Feb 2025 | in application |
| New Art. 5 prohibitions (NCII, CSAM) | Art. 5(1)(ba),(bb); 5(1a),(1b) | 2 Dec 2026 | not yet |
| Notified bodies | Ch. III Sec. 4 | 2 Aug 2025 | in application |
| GPAI models | Ch. V | 2 Aug 2025 | in application |
| Governance | Ch. VII | 2 Aug 2025 | in application |
| Penalties, except Art. 101 | Ch. XII | 2 Aug 2025 | in application |
| Amendments to other Union acts | Arts. 102-110 | 27 Jul 2026 | in application |
| Residual, incl. Art. 50 transparency | - | 2 Aug 2026 | in application |
| **High-risk requirements, Annex III** | **Ch. III Sec. 1,2,3** | **2 Dec 2027** | **NOT in application** |
| **High-risk requirements, Annex I** | **Ch. III Sec. 1,2,3** | **2 Aug 2028** | **NOT in application** |

---

## 7. The one structural link that should get a second pair of eyes

The conclusion in section 0 rests on a chain:

1. Article 113(c) defers "Chapter III, Sections 1, 2, and 3" for Annex III systems. `VERBATIM`
2. Articles 11, 12 and 13 sit inside Chapter III Section 2. `STRUCTURAL`
3. Annex IV is operative only through Article 11(1), its heading being "Technical documentation referred to in Article 11(1)". `VERBATIM`
4. Therefore Articles 11, 12, 13 and Annex IV are deferred to 2 December 2027.

Step 2 was established by inspecting where the Section headings fall in the
consolidated text: Section 2 opens before Article 8, Section 3 opens after Article
15, so Articles 11 to 13 are inside Section 2. That is sound but it is a reading
rather than a quotation, and it is the load-bearing link. **Confirm it directly
against the OJ text of 2024/1689 before the claim enters the manuscript.** It is a
two-minute check and the entire framing depends on it.

---

## 8. Article 12, the provision the whole deliverable is about

`VERBATIM`, consolidated text, marker `B`. **Article 12 is NOT amended by
Regulation (EU) 2026/1744**, confirmed both by the absence of an M1 marker and
against the amending act's own list of instructions.

> **Article 12 — Record-keeping**
>
> 1. High-risk AI systems shall technically allow for the automatic recording of events (logs) over the lifetime of the system.
>
> 2. In order to ensure a level of traceability of the functioning of a high-risk AI system that is appropriate to the intended purpose of the system, logging capabilities shall enable the recording of events relevant for:
> (a) identifying situations that may result in the high-risk AI system presenting a risk within the meaning of Article 79(1) or in a substantial modification;
> (b) facilitating the post-market monitoring referred to in Article 72; and
> (c) monitoring the operation of high-risk AI systems referred to in Article 26(5).
>
> 3. For high-risk AI systems referred to in point 1 (a), of Annex III, the logging capabilities shall provide, at a minimum:
> (a) recording of the period of each use of the system (start date and time and end date and time of each use);
> (b) the reference database against which input data has been checked by the system;
> (c) the input data for which the search has led to a match;
> (d) the identification of the natural persons involved in the verification of the results, as referred to in Article 14(5).

That is the complete Article. The odd punctuation in paragraph 3 ("point 1 (a),
of Annex III") is authentic and identical in the OJ original.

**Retrieval note.** EUR-Lex sits behind an AWS WAF challenge that returns HTTP
202 and zero bytes of legal text to programmatic fetches. All text in sections 8
to 13 was taken from the **Publications Office Cellar repository**, EUR-Lex's
official backing store, which serves the identical consolidated document:
`https://publications.europa.eu/resource/celex/02024R1689-20260727` (851,286
bytes, header `02024R1689 — EN — 27.07.2026 — 001.001`), cross-checked against
`.../32024R1689` (OJ original) and `.../32026R1744` (the amending act). Article
12 was verified character for character against the OJ original.

---

## 9. The four findings that make the argument

### 9.1 The obligation is system-level, and says so

`VERBATIM` the unit of obligation is "the system": *"automatic recording of
events (logs) over the lifetime of the system"*. The purpose clause fixes
granularity by reference to three system-level regulatory functions: risk
identification under Article 79(1), post-market monitoring under Article 72, and
deployer monitoring under Article 26(5). **None of them is attribution of an
output to an internal cause.**

`INFERRED`, and this is the formulation to use because it does not overstate:
the Regulation mandates logging capability sufficient for system-level risk and
monitoring functions, leaves granularity to the provider against the intended
purpose, and **nowhere sets attribution of an output to an internal cause as the
specification**. What must NOT be written: "the Act prohibits component-level
logging", or "the Act defines traceability as system-level". The word
"traceability" appears exactly once, in the 12(2) chapeau, and is never defined
in the Act.

### 9.2 For credit scoring there is no minimum log content at all

Article 12(3) is the only enumerated minimum, and it binds **only** systems under
Annex III **point 1(a)**, remote biometric identification. A creditworthiness
system is Annex III **point 5(b)**. It therefore falls outside 12(3) entirely.

`INFERRED`. For the BFSI pipeline, and for every Annex III category except
biometric identification, the Regulation prescribes **no minimum log content
whatsoever** — only that logging capability exist and that logged events be
"relevant for" the three purposes. This is stronger than the paper's original
framing and it is directly quotable.

Note also the direction of 12(3)(d): the single identification requirement in the
whole Article attributes to a **natural person who verified the result**, not to a
system component.

### 9.3 The Act has no vocabulary for agentic systems

`VERBATIM` word counts across the six units that constitute the entire high-risk
documentation and record-keeping package (Articles 11, 12, 13, 19, 26 and Annex
IV), case-insensitive, whole-word:

| Term | Count | Where |
|---|---|---|
| agent | **0** | nowhere |
| agentic | **0** | nowhere |
| multi-agent | **0** | nowhere |
| orchestration | **0** | no `orchestrat*` stem at all |
| reasoning | **0** | nowhere (2 irrelevant `reason*` hits) |
| tool / tools | 1 | Annex IV 2(a), third-party development artefacts |
| component / components | 2 | Annex IV 1(f) and 2(c) |
| step / steps | 1 | Annex IV 2(a) |
| trace / traceability | 1 | Article 12(2) chapeau |

The only occurrence of "step" means a step in the **development process**:
*"the methods and steps performed for the development of the AI system"*. Not a
step in an execution trace. The only internal-component occurrence is Annex IV
2(c); the other, 1(f), treats the AI system as a component **of a physical
product**, inherited from product-safety law.

### 9.4 The one component-aware provision is static and design-time

`VERBATIM`, Annex IV point 2(c), the most component-aware sentence in the entire
compliance package:

> the description of the system architecture explaining how software components build on or feed into each other and integrate into the overall processing; the computational resources used to develop, train, test and validate the AI system;

`INFERRED`. This is a **design-time documentation** duty discharged before
placing on the market and kept up to date under Article 11(1). It requires a
static description of how components relate **in general**, not a runtime record
of how they related **on any particular occasion**. It yields a diagram of the
pipeline. Article 12 yields events over the system's lifetime. **Neither yields a
per-output execution trace.** That is the gap, and the text supports the claim as
stated.

The distinction doing most of the work in the paper is therefore
**description versus record**, and **general versus per-instance**. Make it
explicit early.

---

## 10. The retention asymmetry, a factor of twenty

`VERBATIM`, Article 19(1), binding the **provider**:

> Providers of high-risk AI systems shall keep the logs referred to in Article 12(1), automatically generated by their high-risk AI systems, to the extent such logs are under their control. Without prejudice to applicable Union or national law, the logs shall be kept for a period appropriate to the intended purpose of the high-risk AI system, of at least six months, unless provided otherwise in the applicable Union or national law, in particular in Union law on the protection of personal data.

`VERBATIM`, Article 26(6) first subparagraph, binding the **deployer**, in
near-identical terms and with the same six-month floor.

`VERBATIM`, Article 18(1), the documentation retention period:

> The provider shall, for a period ending 10 years after the high-risk AI system has been placed on the market or put into service, keep at the disposal of the national competent authorities: (a) the technical documentation referred to in Article 11;

`INFERRED`, and it is one of the sharpest points available to the paper. **The
static architectural description is retained for 10 years. The dynamic execution
record is retained for 6 months. A factor of twenty.** If causal attribution
requires the runtime record, the mandated evidence expires long before most
accountability processes — litigation, regulatory investigation, market
surveillance under Article 74 — would reach it.

**And no single actor need hold the whole trace.** Both Article 19(1) and Article
26(6) are limited to logs *"to the extent such logs are under their control"*.
`INFERRED`: in a multi-actor pipeline with five external MCP services, that
limitation is exactly the accountability-diffusion problem the governance
literature named, written into the retention duty itself.

**Financial-institution carve-out, directly relevant to BFSI.** `VERBATIM`,
Article 19(2): providers that are financial institutions *"shall maintain the
logs automatically generated by their high-risk AI systems as part of the
documentation kept under the relevant financial services law."* Article 26(6)
second subparagraph does the same for deployers. `INFERRED`: for a bank, the AI
Act's log duty is absorbed into existing financial-services record-keeping, whose
granularity was never designed for causal attribution over an agent trajectory.
Worth a paragraph.

---

## 11. Article 86 terminates exactly where attribution would begin

`VERBATIM`, Article 86, unamended:

> **Article 86 — Right to explanation of individual decision-making**
>
> 1. Any affected person subject to a decision which is taken by the deployer on the basis of the output from a high-risk AI system listed in Annex III, with the exception of systems listed under point 2 thereof, and which produces legal effects or similarly significantly affects that person in a way that they consider to have an adverse impact on their health, safety or fundamental rights shall have the right to obtain from the deployer clear and meaningful explanations of the role of the AI system in the decision-making procedure and the main elements of the decision taken.
>
> 2. Paragraph 1 shall not apply to the use of AI systems for which exceptions from, or restrictions to, the obligation under that paragraph follow from Union or national law in compliance with Union law.
>
> 3. This Article shall apply only to the extent that the right referred to in paragraph 1 is not otherwise provided for under Union law.

`INFERRED`. The entitlement has **two** limbs joined by "and": the **role of the
AI system in the decision-making procedure** (a procedural fact: at what point it
was used, whether determinative or advisory), and **the main elements of the
decision taken** (the substance of the human deployer's decision). There is no
third limb covering **how the AI system produced its output**. The explanandum is
the system's *position in the procedure*, not its *processing*.

**The sharpest point in the whole regulatory analysis.** The duty-holder is the
**deployer**, not the provider. The actor best placed to explain the system's
internals has no obligation under this Article; the actor who is obliged holds
only what Article 13 instructions and Article 12 logs give them, and both are
system-level. **The right therefore terminates at exactly the layer where causal
attribution would have to begin.**

Two drafting traps:
- Recital 171 says *"based mainly upon the output"*; Article 86(1) says only
  *"on the basis of the output"*. The enacting text controls. Do not import
  "mainly" into the operative test.
- The adverse-impact element is **subjective**: *"in a way that they consider to
  have an adverse impact"*. Unusually claimant-friendly; worth flagging.

Scope limits: Annex III only, point 2 excluded, Annex I systems entirely outside;
Article 86(3) is a subsidiarity clause deferring to existing Union rights such as
GDPR Article 22.

---

## 12. Article 13, and the two provisions that nearly help but do not

`VERBATIM`, Article 13(3)(b)(iv):

> where applicable, the technical capabilities and characteristics of the high-risk AI system to provide information that is relevant to explain its output;

`VERBATIM`, Article 13(3)(f):

> where relevant, a description of the mechanisms included within the high-risk AI system that allows deployers to properly collect, store and interpret the logs in accordance with Article 12.

`INFERRED`. Both are **disclosure** duties about whatever capability the system
happens to have. "Where applicable" and "where relevant" make each contingent on
the capability existing. Neither creates an obligation to build an explanatory
capability, and neither creates an obligation to record its outputs. They are the
strongest counter-text a reviewer will find, and they do not carry the weight.

---

## 13. The reviewer objections, and how to meet them

`INFERRED` throughout. Three are worth pre-empting in the paper rather than
waiting for.

1. **"Article 12(2) is open-textured, so component-level logging could be
   required."** True and should be conceded. If component-level records were
   genuinely necessary to make risk situations identifiable under 12(2)(a), a
   regulator or harmonised standard could argue they are "events relevant for"
   that purpose. The text does not foreclose component-level logging; it does not
   mandate it, and supplies no criterion by which an assessor could demand it in
   the general case. Concede the first half, hold the second.

2. **"Annex IV points 2(b) and 3 are broad enough to reach component
   behaviour."** Point 2(b) requires "the general logic of the AI system and of
   the algorithms"; point 3 requires "Detailed information about the monitoring,
   functioning and control of the AI system". Both are, on their face,
   requirements to **describe** in general terms, and neither is a **recording**
   requirement attaching to individual outputs. This is why the
   description/record and general/per-instance distinctions must be stated early.

3. **"Article 25 on the AI value chain is where the Act handles multi-component
   systems, not Article 12."** `NOT RETRIEVED` — Article 25 and the Article 3
   definitions of "AI system", "provider" and "deployer" were not fetched and
   should be, before the manuscript. This is a genuine counter-argument and it
   does not defeat the point: **allocating legal responsibility between actors is
   not the same as producing evidence of which component caused an output.** Meet
   it explicitly.

---

## 14. Still outstanding

Retrieved and verbatim: Articles 6(1), 6(2), 11, 12, 13, 18(1), 19, 26, 86, 113;
Annex III point 5; Annex IV complete; recitals 71 and 171; Regulation (EU)
2026/1744 Articles 1(40) and 4 and recital (40).

**Not retrieved:**

- **Article 25** (responsibilities along the AI value chain) and the **Article 3**
  definitions. Needed to meet reviewer objection 3 above.
- **Article 72** (post-market monitoring) and **Article 79(1)**, both referenced
  by Article 12(2) and so load-bearing for what "relevant events" means.
- **Article 74** (market surveillance powers), for the argument that logs expire
  before investigations reach them.

**Citation discipline for the manuscript.** The consolidated text carries the
standard disclaimer that it "is meant purely as a documentation tool and has no
legal effect". For a paper turning on exact wording, cite **OJ L, 2024/1689,
12.7.2024** (ELI `http://data.europa.eu/eli/reg/2024/1689/oj`) for Articles 12,
13, 19, 26, 86 and Annex IV, all unamended and therefore identical in the OJ
original, and **OJ L, 2026/1744, 24.7.2026** for the replaced second subparagraph
of Article 11(1) and for the Article 113 amendment.

---

# Part II: retrievals of 4 September 2026

Added after the 2026-09-04 session. Same discipline: `VERBATIM` means the exact
words were retrieved this session with a URL, `STRUCTURAL` a reading, `INFERRED`
my reasoning.

## 15. Section 7 step 2 is now VERBATIM, not STRUCTURAL

The load-bearing link flagged in section 7 has been checked against the primary
text and holds. Retrieved 2026-09-04 from
`https://eur-lex.europa.eu/legal-content/EN/TXT/HTML/?uri=CELEX:02024R1689-20260727`.

CHAPTER III, "HIGH-RISK AI SYSTEMS", is divided as follows: `VERBATIM`

| Section | Heading | Articles |
|---|---|---|
| SECTION 1 | Classification of AI systems as high-risk | 6, 7 |
| **SECTION 2** | **Requirements for high-risk AI systems** | **8 to 15** |
| SECTION 3 | Obligations of providers and deployers of high-risk AI systems and other parties | 16 to 26 |

**Articles 11, 12 and 13 are inside Section 2.** The chain in section 7 is
therefore complete and every step of it is now a quotation:

1. Article 113(c) defers "Chapter III, Sections 1, 2, and 3" for Annex III systems. `VERBATIM`
2. Articles 11, 12 and 13 sit inside Chapter III Section 2. `VERBATIM as of 2026-09-04`
3. Annex IV is operative only through Article 11(1). `VERBATIM`
4. Therefore Articles 11, 12, 13 and Annex IV are deferred to 2 December 2027.

**Remaining caveat, and it is small.** This was read from the consolidated text,
which carries the standard "no legal effect" disclaimer. The Section headings of
Chapter III were not amended by Regulation (EU) 2026/1744, whose Article 1(40)
amends Article 113 and whose only other relevant change is to the second
subparagraph of Article 11(1), so the OJ original carries the same structure.
That last step is `INFERRED` from the scope of the amending act rather than read
off the OJ original, because the OJ HTML truncates in the recitals before
reaching any article. It is a much weaker dependency than the one it replaces.

## 16. Article 25, and why it does not answer the question this paper asks

Reviewer objection 3 in section 13 was that Article 25 is where the Act handles
multi-component systems, so Article 12 is the wrong provision to build on. The
article has now been retrieved and the objection can be met from its own text.

**Article 25, "Responsibilities along the AI value chain", paragraph 1:** `VERBATIM`

> "Any distributor, importer, deployer or other third-party shall be considered
> to be a provider of a high-risk AI system for the purposes of this Regulation
> and shall be subject to the obligations of the provider under Article 16, in
> any of the following circumstances: (a) they put their name or trademark on a
> high-risk AI system already placed on the market or put into service ...
> (b) they make a substantial modification ... (c) they modify the intended
> purpose of an AI system ... in such a way that the AI system concerned becomes
> a high-risk AI system in accordance with Article 6."

**Paragraph 2, third subparagraph, the cooperation duty:** `VERBATIM`

> "In particular, the obligation laid down in the second subparagraph shall
> include, where relevant for the purposes specified therein, the following:
> (a) making available of technical documentation sufficient to assess
> compliance with the requirements laid down in Article 16; (b) informing the
> new providers about known limitations and failure modes; and (c) providing the
> new providers with targeted technical access, including for testing and
> validation."

**Paragraph 4, the written agreement:** `VERBATIM`

> "The provider of a high-risk AI system and the third party that supplies an AI
> system, AI model, tools, services, components, or processes that are used or
> integrated in a high-risk AI system shall, by written agreement, specify the
> necessary information, capabilities, technical access and other assistance
> based on the generally acknowledged state of the art, in order to enable the
> provider of the high-risk AI system to fully comply with the obligations set
> out in this Regulation."

**The objection is met, and the article helps us.** `INFERRED`, but from
quotations rather than from recollection. Article 25 allocates the legal role of
"provider" between actors and imposes duties of cooperation, documentation and
technical access. Every one of its obligations is about **who is answerable** and
about **enabling compliance**. None of them is about producing evidence of
**which component caused a particular output**. Paragraph 2 requires technical
documentation "sufficient to assess compliance with the requirements laid down
in Article 16", and information about "known limitations and failure modes",
which is a class-level statement about a system, not a decision-level statement
about an instance. Paragraph 4 requires the parties to agree what information is
needed "in order to enable the provider ... to fully comply", which presupposes
that the content of compliance is fixed elsewhere. It is fixed in Section 2,
which is where Article 12 sits.

So the two provisions do different work and the paper needs both: Article 25
determines who must answer, Article 12 determines what the record must contain,
and neither tells a provider how to establish which step of an agentic
trajectory determined a contested decision. That gap is what the specification in
this paper addresses.

## 17. Article 3 definitions, for the scope argument

Retrieved 2026-09-04, same URL. `VERBATIM`

> "(1) 'AI system' means a machine-based system that is designed to operate with
> varying levels of autonomy and that may exhibit adaptiveness after deployment,
> and that, for explicit or implicit objectives, infers, from the input it
> receives, how to generate outputs such as predictions, content,
> recommendations, or decisions that can influence physical or virtual
> environments;"

> "(3) 'provider' means a natural or legal person, public authority, agency or
> other body that develops an AI system or a general-purpose AI model or that
> has an AI system or a general-purpose AI model developed and places it on the
> market or puts the AI system into service under its own name or trademark,
> whether for payment or free of charge;"

> "(4) 'deployer' means a natural or legal person, public authority, agency or
> other body using an AI system under its authority except where the AI system
> is used in the course of a personal non-professional activity;"

**Why these matter to the argument.** `INFERRED`. The definition of "AI system"
is singular and system-level throughout: one machine-based system that infers
how to generate outputs. An agentic pipeline of five tool-backed services and a
model is, on this definition, **one** AI system with one provider and one
deployer. The Act therefore has no vocabulary at all for the internal components
whose relative contribution this paper measures, which is the same finding
recorded in section 9.3 and is now supported by the definition itself rather
than by its absence elsewhere.

## 18. Still outstanding after this session

**Retrieved and verbatim:** Articles 3(1), 3(3), 3(4), 6(1), 6(2), 11, 12, 13,
18(1), 19, **25**, 26, 86, 113; the Chapter III Section structure; Annex III
point 5; Annex IV complete; recitals 71 and 171; Regulation (EU) 2026/1744
Articles 1(40) and 4 and recital (40).

**Still not retrieved: Articles 72, 74(1) and 79(1).** Article 12(2) refers to
Articles 72 and 79(1), so they bound what "relevant events" means, and Article 74
carries the argument that logs expire before a market-surveillance investigation
reaches them.

**Routes tried on 2026-09-04 and their outcomes**, recorded so the next attempt
does not repeat them:

| Route | Outcome |
|---|---|
| `publications.europa.eu/resource/celex/02024R1689-20260727` | HTTP 404 to a plain fetch; needs Accept-header content negotiation the tool cannot send |
| `eur-lex.../TXT/HTML/?uri=CELEX:02024R1689-20260727` | **WORKS**, but truncates mid Article 26. Everything through Article 25 is reachable this way; nothing beyond it is |
| `eur-lex.../TXT/HTML/?uri=CELEX:32024R1689` (OJ original) | Truncates in recital (60), before any article |
| `eur-lex.../TXT/?uri=CELEX:02024R1689-20260727` | Returns metadata only |
| `data.europa.eu/eli/reg/2024/1689/oj/eng/html` | robots.txt disallowed |
| adding a query parameter to bust the fetch cache | robots.txt disallowed |

The three outstanding articles sit in Chapter IX, well past the truncation point
of the only route that returns article text. They must be obtained another way:
from a browser session, or from the OJ PDF, before section 8 makes any claim that
depends on them. Until then section 8 must not characterise Article 12(2)'s
cross-references, and must say so.

---

# Part III: Articles 72, 74 and 79, retrieved 4 September 2026

Provided by Ajay from the consolidated text on EUR-Lex and pasted into the
session, rather than fetched by me: every programmatic route recorded in section
18 truncates before Chapter IX. The text below is therefore `VERBATIM` as to
wording but the retrieval is second-hand, and a final check against the OJ should
be made before any of it is quoted in the manuscript.

**One numbering caveat, recorded rather than glossed.** The pasted block
beginning "Market surveillance and control of AI systems in the Union market"
carried no article number. That title is Article 74 of Regulation (EU) 2024/1689,
and the block's own cross-references to "the procedures referred to in Articles 79
to 83" are consistent with it. The article number is therefore `INFERRED` from
the title, not read. Confirm the number when a browser is next open, before the
appendix cites it.

## 19. Article 72, post-market monitoring

**Article 72(2):** `VERBATIM`

> "The post-market monitoring system shall actively and systematically collect,
> document and analyse relevant data which may be provided by deployers or which
> may be collected through other sources on the performance of high-risk AI
> systems throughout their lifetime, and which allow the provider to evaluate the
> continuous compliance of AI systems with the requirements set out in Chapter
> III, Section 2. Where relevant, post-market monitoring shall include an
> analysis of the interaction with other AI systems."

**The last sentence is the one that matters, and it cuts our way.** `INFERRED`.
The only interaction the Act asks a provider to analyse is the interaction
**with other AI systems**, that is, between systems. It does not ask for analysis
of the interaction between components inside one system, which is the object this
paper measures. Taken with the Article 3(1) definition, under which an agentic
pipeline is one AI system, the Act's monitoring obligation is silent on exactly
the internal structure where an agentic failure is located.

**Article 72(3), as amended (the consolidated text carries an M1 marker at this
paragraph, indicating amendment by Regulation (EU) 2026/1744):** `VERBATIM`

> "The post-market monitoring system shall be based on a post-market monitoring
> plan. The post-market monitoring plan shall be part of the technical
> documentation referred to in Annex IV. The Commission, taking utmost account of
> the opinion of the Board, shall adopt guidance, including a template, on the
> post-market monitoring plan by 2 September 2027."

**A second live target for the deliverable.** `INFERRED`. Section 7 of the brief
already identified the simplified Annex IV form for SMEs as an instrument that
does not yet exist. This is a second one: a post-market monitoring plan template,
due from the Commission by **2 September 2027**, which is part of the Annex IV
technical documentation. A specification for what an agentic post-market
monitoring plan must record in order to make causal attribution possible arrives
before that template does.

**Article 72(4), second subparagraph:** `VERBATIM`

> "The first subparagraph of this paragraph shall also apply to high-risk AI
> systems referred to in point 5 of Annex III placed on the market or put into
> service by financial institutions that are subject to requirements under Union
> financial services law regarding their internal governance, arrangements or
> processes."

Annex III point 5 is creditworthiness. This provision names the exact system
class the paper's intended live arm belongs to.

## 20. Article 74, market surveillance, and an escalation ladder that stops short

**Article 74(12):** `VERBATIM`

> "Without prejudice to the powers provided for under Regulation (EU) 2019/1020,
> and where relevant and limited to what is necessary to fulfil their tasks, the
> market surveillance authorities shall be granted full access by providers to
> the documentation as well as the training, validation and testing data sets
> used for the development of high-risk AI systems, including, where appropriate
> and subject to security safeguards, through application programming interfaces
> (API) or other relevant technical means and tools enabling remote access."

**Article 74(13):** `VERBATIM`

> "Market surveillance authorities shall be granted access to the source code of
> the high-risk AI system upon a reasoned request and only when both of the
> following conditions are fulfilled: (a) access to source code is necessary to
> assess the conformity of a high-risk AI system with the requirements set out in
> Chapter III, Section 2; and (b) testing or auditing procedures and
> verifications based on the data and documentation provided by the provider have
> been exhausted or proved insufficient."

**This is the strongest regulatory finding of the session.** `INFERRED`, from
quotation. Article 74 sets out an escalation ladder for an investigating
authority: first the documentation and the data sets, then, only once those are
"exhausted or proved insufficient", the source code. **Execution traces are on
neither rung.** The ladder is built for a system whose behaviour can be
interrogated from its artefacts and its training data, which is the right model
for a classifier and the wrong one for an agent whose contested decision is a
path through a trajectory that happened once. An authority following Article 74
in order would reach source code without ever obtaining the one record that could
establish which step determined the outcome.

That is not a gap the Act acknowledges, and it is the gap the specification in
this paper fills.

## 21. Article 79, and what an authority is required to say

**Article 79(2), second subparagraph, the correction window:** `VERBATIM`

> "it shall without undue delay require the relevant operator to take all
> appropriate corrective actions to bring the AI system into compliance, to
> withdraw the AI system from the market, or to recall it within a period the
> market surveillance authority may prescribe, and in any event within the
> shorter of 15 working days, or as provided for in the relevant Union
> harmonisation legislation."

**Article 79(6):** `VERBATIM`

> "the market surveillance authorities shall indicate whether the non-compliance
> is due to one or more of the following: (a) non-compliance with the prohibition
> of the AI practices referred to in Article 5; (b) **a failure of a high-risk AI
> system to meet requirements set out in Chapter III, Section 2**; (c)
> shortcomings in the harmonised standards or common specifications referred to
> in Articles 40 and 41 conferring a presumption of conformity; (d)
> non-compliance with Article 50."

**The finest granularity the Act provides for attributing a failure is the whole
system against a whole Section.** `INFERRED`. Article 79(6)(b) is the category
into which every agentic failure of the kind this paper studies would fall, and
it resolves to "this system failed Chapter III Section 2". There is no category,
and no requirement, for saying which component of the system failed, or which
step of a trajectory produced the contested output. An authority can be fully
compliant with Article 79 while being unable to say anything about causation
inside the system.

**Article 79(1)** defines an AI system presenting a risk by reference to Article
3, point 19 of Regulation (EU) 2019/1020, "in so far as they present risks to the
health or safety, or to fundamental rights, of persons". `VERBATIM`

## 22. What Article 12(2)'s cross-references actually require

Section 8 was told not to characterise these until they were read. They have now
been read, so it may. `INFERRED`, from the quotations above.

Article 12(2) obliges logging that enables identifying situations that may
present a risk within the meaning of Article 79(1), or lead to a substantial
modification, and that facilitates post-market monitoring under Article 72. Both
cross-references resolve to system-level obligations. Article 79(1) is about
whether the system presents a risk; Article 72 is about the system's performance
over its lifetime and its interaction with other systems. **Neither
cross-reference imports any component-level or step-level requirement.** The
logging duty in Article 12 is therefore bounded above by two system-level
purposes, and a provider who logs enough to serve both can still be unable to
answer which retrieval, tool call or model step determined a specific contested
decision.

That bound is the precise statement the specification needs, and it could not be
made before these three articles were read.

## 23. Retrieval status after this session

**Retrieved and verbatim:** Articles 3(1), 3(3), 3(4), 6(1), 6(2), 11, 12, 13,
18(1), 19, 25, 26, **72, 74, 79**, 86, 113; the Chapter III Section structure;
Annex III point 5; Annex IV complete; recitals 71 and 171; Regulation (EU)
2026/1744 Articles 1(40) and 4 and recital (40).

**Outstanding checks, none of them blocking:**

- Confirm that the block titled "Market surveillance and control of AI systems in
  the Union market" is numbered Article 74.
- Confirm the M1 amendment marker on Article 72(3) against Regulation (EU)
  2026/1744 itself, since the paper will state that the monitoring-plan template
  deadline of 2 September 2027 is an amended provision.
- Article 73, serious incident reporting, was not retrieved and sits between 72
  and 74. It is not currently load-bearing but should be checked before the
  appendix claims the Act has no incident-level component reporting.
