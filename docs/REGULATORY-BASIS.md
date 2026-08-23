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

## 8. Still outstanding for WS6

Retrieved this session: Article 113, Article 6(1) and 6(2), Annex III point 5,
Article 11(1) second subparagraph, recital (40) of 2026/1744, Article 1(40) and
Article 4 of 2026/1744.

**Not yet retrieved, and all of it load-bearing:**

- **Article 12 (record-keeping) in full.** This is the single most important
  provision for the deliverable. The whole argument is that Article 12 mandates
  logging that is insufficient for causal attribution, and that argument cannot be
  made without its exact words.
- **Article 11 in full**, beyond the amended second subparagraph.
- **Annex IV in full**, all enumerated points. The deliverable is a specification
  against this list.
- **Article 13** (transparency to deployers) in full.
- **Article 19** (automatically generated logs) in full.
- **Article 26** (deployer obligations), especially any log-retention period.
- **Article 86** (right to explanation of individual decision-making) in full,
  including its conditions and limits. Load-bearing for the "attribute correct
  decisions, not only failures" framing.

EUR-Lex HTML truncates on retrieval, so these need fetching in sections or from
the PDF. Do not fill any of it from a summary site.
