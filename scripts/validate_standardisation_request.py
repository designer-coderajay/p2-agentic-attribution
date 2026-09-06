"""Check Section 8's quotation of the standardisation request against the
committed primary source, and check that the paper names the operative
instrument rather than the repealed one.

Why this exists. An earlier draft of the paragraph quoted Annex II point 2.3 of
Commission Implementing Decision C(2023) 3215 of 22 May 2023 and argued from the
length of that text relative to the other nine deliverables. C(2023) 3215 has
been repealed, by Article 4 of C(2025) 3871 of 23 June 2025, and it had been
drafted against the AI Act *proposal* rather than the adopted Regulation. A
paper about what the law currently requires cannot quote a repealed instrument
as if it were in force, and no reading caught it: the eNorm register entry did,
on the second retrieval. This script pins the corrected quotation so that the
manuscript and the source cannot drift apart again, and so that a later reader
can see which document is being quoted without taking it on trust.

Three assertions:
  1. the block quotation in paper/main.tex matches the verbatim text in
     docs/sources/C2025_3871_standardisation_request.md, word for word, after
     normalising LaTeX quote marks, line breaks and hyphenation;
  2. the word count the paper states is the word count of that text;
  3. the paper names C(2025) 3871 as the request, and mentions C(2023) 3215 only
     in the company of the word "repeal".
"""
import os
import re
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SRC = os.path.join(ROOT, "docs", "sources", "C2025_3871_standardisation_request.md")
TEX = os.path.join(ROOT, "paper", "main.tex")

# The paper states this count in words, not digits, so it is checked by name.
STATED_COUNT = 32
COUNT_WORD = "Thirty-two"


def norm(s):
    """Collapse the differences that are typesetting rather than text."""
    s = s.replace("``", '"').replace("''", '"').replace("\u201c", '"').replace("\u201d", '"')
    s = s.replace("~", " ")
    s = re.sub(r"\\emph\{([^}]*)\}", r"\1", s)
    s = " ".join(s.split())
    # The manuscript wraps the quotation in quotation marks and the source file
    # does not, because in the source it is already a Markdown blockquote.
    return s.strip('"').strip()


def source_quote():
    with open(SRC, encoding="utf-8") as fh:
        lines = fh.read().split("\n")
    want = "## Annex II, point 2.3, verbatim and in its entirety"
    try:
        i = lines.index(want)
    except ValueError:
        return None
    for line in lines[i + 1:]:
        if line.startswith("> "):
            return line[2:].strip()
        if line.startswith("## "):
            break
    return None


def paper_quote(tex):
    """The one \\begin{quote} block in the regulatory section."""
    blocks = re.findall(r"\\begin\{quote\}(.*?)\\end\{quote\}", tex, re.S)
    hits = [b for b in blocks if "record keeping" in b or "specifications for record" in b]
    return hits[0] if len(hits) == 1 else None


def main():
    src = source_quote()
    if not src:
        print("FAIL  the verbatim Annex II 2.3 quotation is missing from")
        print(f"      {os.path.relpath(SRC, ROOT)}")
        return 1

    with open(TEX, encoding="utf-8") as fh:
        raw = fh.read()
    tex = "\n".join(ln for ln in raw.split("\n") if not ln.lstrip().startswith("%"))

    bad = []

    quoted = paper_quote(tex)
    if quoted is None:
        bad.append("could not find exactly one quote block naming record keeping in main.tex")
    elif norm(quoted) != norm(src):
        bad.append("the manuscript's quotation does not match the committed source")
        bad.append(f"  source: {norm(src)[:96]}...")
        bad.append(f"  paper : {norm(quoted)[:96]}...")

    n = len(norm(src).split())
    if n != STATED_COUNT:
        bad.append(f"the source quotation is {n} words; this script claims {STATED_COUNT}")
    flat = norm(tex)
    if f"{COUNT_WORD} words" not in flat:
        bad.append(f'the manuscript no longer says "{COUNT_WORD} words"')

    if "C(2025) 3871" not in flat:
        bad.append("the manuscript does not name C(2025) 3871, the operative request")
    for m in re.finditer(re.escape("C(2023) 3215"), flat):
        window = flat[max(0, m.start() - 220): m.end() + 220]
        if "repeal" not in window.lower():
            bad.append("C(2023) 3215 is named without saying it was repealed")
            break

    if bad:
        print("FAIL")
        for b in bad:
            print("    " + b)
        return 1

    print(f"  quotation matches docs/sources/, {n} words, and the operative")
    print("  instrument named is C(2025) 3871")
    print("  PASS  3 checks")
    return 0


if __name__ == "__main__":
    sys.exit(main())
