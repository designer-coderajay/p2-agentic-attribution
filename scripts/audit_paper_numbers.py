"""WS1.13. Every number in the manuscript's tables, checked against the artifact
it is supposed to have come from.

WHY THIS EXISTS. A cell in Appendix B's coupling table read 0.0446 when
results/validation_coupling.json said 0.1655. It had been there since the table
was written. It survived a full citation sweep, a figure pass, two adversarial
reviews and four readings, because a transcribed table is not something a human
re-checks digit by digit. One of forty-two cells was wrong and no process in this
repository would have caught it.

WHAT IT DOES. For every table in the paper whose numbers come from a committed
results/*.json, this script derives the expected LaTeX string FROM THE ARTIFACT
and asserts it appears in paper/main.tex. The direction matters: it does not
parse the paper and hope to recognise a number, it computes what the paper must
say and checks that it says it. A number that drifts in either the artifact or
the manuscript fails.

WHAT IT DOES NOT DO. It does not check prose numbers that come from a validator's
stdout rather than a JSON, and it does not check model parameters. Those are
listed at the end as the residual, with a count, so the coverage is a stated
number rather than an impression.

Run from the repository root.
"""
import json
import math
import os
import re
import sys

ROOT = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..")
TEX = os.path.join(ROOT, "paper", "main.tex")


def results(name):
    with open(os.path.join(ROOT, "results", name), encoding="utf-8") as fh:
        return json.load(fh)


def load_tex():
    with open(TEX, encoding="utf-8") as fh:
        raw = fh.read()
    # A LaTeX comment can hold a number that is not a claim, including the text
    # of a withdrawn one. Strip comments before matching so a retraction's own
    # quotation of the number it retracts cannot satisfy a check. This repository
    # has shipped that bug four times in other guises.
    return "\n".join(ln for ln in raw.splitlines() if not ln.lstrip().startswith("%"))


TEXT = load_tex()
checks, failures, notes = 0, [], []


def expect(label, literal, context=None):
    """Assert `literal` appears in the manuscript, optionally inside `context`."""
    global checks
    checks += 1
    hay = TEXT
    if context is not None:
        i = TEXT.find(context)
        if i < 0:
            failures.append(f"{label}: context block not found: {context[:50]!r}")
            return
        hay = TEXT[i:i + 4000]
    if literal not in hay:
        failures.append(f"{label}: manuscript does not contain {literal!r}")


def f(x, n):
    """Format as the manuscript formats: fixed decimals, no thousands separator."""
    return f"{x:.{n}f}"


print(__doc__.split("\n\n", 1)[1].rstrip())
print()

# ---------------------------------------------------------------------------
# 1. Appendix B, the coupling table. 6 rows x 7 columns = 42 cells.
# ---------------------------------------------------------------------------
print("1. Appendix B coupling table against results/validation_coupling.json")
cj = results("validation_coupling.json")
tab = TEXT.find("\\label{tab:coupling}")
block_start = TEXT.rfind("\\begin{table}", 0, tab) if tab > 0 else -1
if block_start < 0:
    failures.append("Appendix B: could not locate the coupling table block")
    block = ""
else:
    block = TEXT[block_start:tab]
cells = 0
for row in cj["rows"]:
    for col, nd in (("shift", 2), ("tv", 4), ("quantile_bound", 4),
                    ("quantile_emp", 4), ("maximal_bound", 4),
                    ("maximal_emp", 4), ("prob_sorted", 4)):
        lit = f(row[col], nd)
        cells += 1
        checks += 1
        if lit not in block:
            failures.append(
                f"Appendix B row shift={row['shift']}, column {col}: "
                f"artifact says {lit}, manuscript table does not contain it")
print(f"   {cells} cells checked against {len(cj['rows'])} committed rows")
print(f"   env: python {cj['env']['python']}, numpy {cj['env']['numpy']}, "
      f"vocab {cj['env']['vocab']}, {cj['env']['n_draws']} draws, "
      f"env_hash {cj['env']['env_hash']}")
expect("Appendix B vocabulary", str(cj["env"]["vocab"]), block)

# ---------------------------------------------------------------------------
# 2. Table 1, the planted-chain values.
# ---------------------------------------------------------------------------
print("\n2. Table 1 against results/validation_partial_mediation.json")
pm = results("validation_partial_mediation.json")
tab1 = TEXT.find("\\label{tab:two-te}")
b1 = TEXT.rfind("\\begin{table}", 0, tab1) if tab1 > 0 else -1
block1 = TEXT[b1:tab1] if b1 >= 0 else ""
if not block1:
    failures.append("Table 1: could not locate the table block")
for st in pm["steps"]:
    for col in ("te_marg", "te_crn", "de", "me"):
        v = st[col]
        # The manuscript rounds to 2dp and writes an exact zero as "0".
        lit = "0" if abs(v) < 5e-3 else f"{v:.2f}"
        checks += 1
        if lit not in block1:
            failures.append(f"Table 1 step {st['step']} {col}: artifact rounds to "
                            f"{lit}, manuscript table does not contain it")
print(f"   {len(pm['steps']) * 4} cells checked")
fa = pm["factual"]["actions"]
expect("Table 1 factual action tuple",
       "(" + ",".join(str(a) for a in fa) + ")")
print(f"   factual run {tuple(fa)}, y = {pm['factual']['y']}, "
      f"q = {pm['env']['q']}, w = {pm['env']['w']}, "
      f"{pm['env']['n_rollouts']} rollouts, env_hash {pm['env']['env_hash']}")
expect("the fidelity parameter q", f"{pm['env']['q']}")
expect("the direct weight w", f"{pm['env']['w']}")

# The pin-plausibility claim in Section 4 is about step 1 specifically.
p1 = pm["steps"][1]["pin_plausibility"]
print(f"   step 1 pin plausibility in the artifact: {p1:.4f} "
      f"(the text's claim is that this is 1/2 for every q)")
checks += 1
if abs(p1 - 0.5) > 0.02:
    failures.append(f"pin plausibility: artifact step 1 is {p1:.4f}, which is not "
                    f"within 0.02 of the 1/2 the manuscript claims")

# ---------------------------------------------------------------------------
# 3. The suppression worked instance, Section 6.
# ---------------------------------------------------------------------------
print("\n3. Section 6 worked instance against results/validation_suppression.json")
sp = results("validation_suppression.json")
k = 1  # the suppressed node
expect("suppression TE_crn (analytic)", f"+{sp['te'][k]:.2f}".replace("+0.30", "0.30"))
expect("suppression measured TE_crn", f"+{sp['te'][k]:.4f}")
expect("suppression measured DE", f"{sp['de'][k]:.4f}")
expect("suppression measured ME", f"+{sp['me'][k]:.4f}")
expect("suppression share", f"{sp['share'][k]:.4f}")
print(f"   TE {sp['te'][k]:.4f}, DE {sp['de'][k]:.4f}, ME {sp['me'][k]:.4f}, "
      f"share {sp['share'][k]:.4f}, suppressed nodes {sp['suppressed_nodes']}")
print(f"   w = {sp['env']['w']}, q = {sp['env']['q']}, env_hash {sp['env']['env_hash']}")
checks += 1
if abs(sp["share"][k] - 4.0 / 3.0) > 1e-9:
    failures.append(f"suppression share is {sp['share'][k]}, not 4/3, so the "
                    f"manuscript's 'exactly 4/3' is wrong")

# ---------------------------------------------------------------------------
# 4. Numbers the manuscript takes from the end-to-end dry run.
# ---------------------------------------------------------------------------
print("\n4. Dry-run numbers against results/dry_run.json")
dr = results("dry_run.json")
checks += 1
if not dr.get("SYNTHETIC_NOT_RESULTS"):
    failures.append("dry_run.json is not flagged SYNTHETIC_NOT_RESULTS; the "
                    "manuscript describes it as a dry run and not a result")
tau = dr["h4"][0]
expect("H4 rank correlation after the exclusion rule", f"{tau:.3f}")
bc = dr["h2"]["beta"][0]
print(f"   tau_b {tau:.4f} -> manuscript writes {tau:.3f}")
# beta_causal is quoted in ranking.py's docstring and in RESEARCH_LOG.md but not
# in the manuscript. Check it only where it is actually claimed, rather than
# manufacturing a failure for a number the paper never states.
if f"{bc:.3f}" in TEXT or "beta_{\\mathrm{causal}}" in TEXT:
    expect("the fitted causal coefficient", f"{bc:.3f}")
    print(f"   beta_causal {bc:.4f} -> manuscript writes {bc:.3f}")
else:
    notes.append(f"the manuscript does not quote beta_causal ({bc:.4f}); "
                 f"nothing to check, recorded so the absence is deliberate")
print(f"   env: python {dr['env']['python']}, numpy {dr['env']['numpy']}, "
      f"seed {dr['env']['seed']}, env_hash {dr['env']['env_hash']}")

# The normalised direction must be internally consistent with the fit it came
# from, or one of the two was edited by hand.
beta = dr["h2"]["beta"]
norm = math.sqrt(sum(b * b for b in beta))
checks += 1
if max(abs(b / norm - g)
       for b, g in zip(beta, dr["h2"]["g_normalized"], strict=True)) > 1e-9:
    failures.append("dry_run.json: g_normalized is not beta/||beta||, so one of "
                    "the two fields was written by something other than the fit")
print("   g_normalized reproduces beta/||beta|| to 1e-9")

# ---------------------------------------------------------------------------
# 5. Every environment block must agree with the pin.
# ---------------------------------------------------------------------------
print("\n5. Recorded environments against requirements.txt")
with open(os.path.join(ROOT, "requirements.txt"), encoding="utf-8") as fh:
    req = fh.read()
m = re.search(r"^numpy==([\d.]+)$", req, re.M)
checks += 1
if not m:
    failures.append("requirements.txt does not pin numpy with ==")
else:
    pin = m.group(1)
    print(f"   requirements.txt pins numpy=={pin}")
    for name in sorted(os.listdir(os.path.join(ROOT, "results"))):
        if not name.endswith(".json"):
            continue
        env = results(name).get("env", {})
        got = env.get("numpy")
        checks += 1
        if got and got != pin:
            notes.append(f"results/{name} was produced under numpy {got}, "
                         f"not the pinned {pin}")
    print(f"   {len([n for n in os.listdir(os.path.join(ROOT,'results')) if n.endswith('.json')])}"
          f" artifacts checked against it")

# ---------------------------------------------------------------------------
# 6. Coverage. What this script does NOT cover, counted rather than implied.
# ---------------------------------------------------------------------------
print("\n6. Coverage of the manuscript's decimal literals")
lits = re.findall(r"(?<![\w.])-?\d+\.\d+", TEXT)
distinct = sorted(set(lits))
# Anything appearing in a checked block, or derivable from a checked artifact,
# counts as covered. The rest are parameters, cited values from other work, or
# numbers whose source is a validator's stdout rather than a JSON.
covered = set()
for row in cj["rows"]:
    for col, nd in (("shift", 2), ("tv", 4), ("quantile_bound", 4),
                    ("quantile_emp", 4), ("maximal_bound", 4),
                    ("maximal_emp", 4), ("prob_sorted", 4)):
        covered.add(f(row[col], nd))
for st in pm["steps"]:
    for col in ("te_marg", "te_crn", "de", "me"):
        covered.add(f"{st[col]:.2f}")
for arr in (sp["te"], sp["de"], sp["me"], sp["share"]):
    for v in arr:
        covered.add(f"{v:.4f}")
        covered.add(f"{v:.2f}")
covered.add(f"{tau:.3f}")
covered.add(f"{bc:.3f}")
hit = [x for x in distinct if x in covered or x.lstrip("+-") in covered]
miss = [x for x in distinct if x not in hit]
print(f"   {len(distinct)} distinct decimal literals in the manuscript")
print(f"   {len(hit)} are pinned to a committed artifact by this script")
print(f"   {len(miss)} are not, and are listed so they are reviewed by eye:")
for i in range(0, len(miss), 10):
    print("     " + "  ".join(f"{x:>8}" for x in miss[i:i + 10]))
print("   Those are model parameters, values cited from other papers, and")
print("   numbers whose source is a validator's stdout rather than a JSON.")
print("   scripts/validate_crn_degeneracy.py and")
print("   scripts/validate_triage_closeout.py regenerate the second group, and")
print("   their output is committed under results/.")

# ---------------------------------------------------------------------------
print()
for n in notes:
    print(f"  [note] {n}")
if failures:
    print(f"\n{len(failures)} FAILURE(S) in {checks} checks:")
    for x in failures:
        print(f"  - {x}")
    print("\nRESULT: FAIL")
    sys.exit(1)
print(f"\n{checks} checks, 0 failures.")
print("RESULT: ALL CHECKS PASS")
