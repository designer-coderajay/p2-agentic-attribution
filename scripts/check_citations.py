"""Every citation in committed SOURCE must appear in the citation ledger.

WHY THIS EXISTS. The ledger rule was practised as "nothing enters a MANUSCRIPT
until it appears here as VERIFIED". Code docstrings were treated as outside that
boundary. They are not.

On 2026-08-20 the `normalized_beta` docstring in src/p2/ranking.py was committed
containing "(Fieller 1954)" as the authority for the ratio-of-normals argument
that justifies the paper's headline reporting convention. That reference was
never added to docs/CITATION-LEDGER.md. It sat in committed source, in a
RECALLED state, in the justification for a pre-registered analysis choice, and
would have travelled from the docstring into the manuscript's methods section
without ever being checked. It was caught three days later by a different
session, by eye.

In this project the docstrings ARE where the methodological arguments are
written, so a citation in a docstring is load-bearing. Noticing is not a
control. This is the control.

WHAT IT CHECKS. Two classes of reference in src/ and scripts/:
  1. arXiv identifiers, NNNN.NNNNN
  2. author-year citations, "(Surname YYYY)" / "Surname (YYYY)" /
     "Surname et al. YYYY" / "Surname and Surname YYYY"
Each must appear somewhere in docs/CITATION-LEDGER.md. Exits non-zero if any
does not.

WHAT IT DELIBERATELY DOES NOT CHECK. Whether the ledger entry says VERIFIED.
A reference may legitimately sit in source while still RECALLED, as long as it
is tracked and gets resolved before the manuscript. Presence in the ledger is
the invariant; status is the researcher's call at the final ledger pass (WS0.9).
"""
import os
import re
import sys

ROOT = os.path.join(os.path.dirname(__file__), "..")
LEDGER = os.path.join(ROOT, "docs", "CITATION-LEDGER.md")
SCAN_DIRS = ["src", "scripts"]

# Words that look like a surname before a year but are not citations. Kept
# explicit rather than clever: a silent false negative here defeats the purpose,
# so anything genuinely ambiguous should stay IN and be dismissed by eye.
NOISE = {
    "verified", "added", "recalled", "false", "checked", "on", "since",
    "until", "by", "and", "the", "in", "at", "of", "to", "from", "see",
    "before", "after", "sprint", "day", "gate", "arxiv", "car", "prereg",
    "august", "september", "october", "november", "december", "july",
}

ARXIV = re.compile(r"\b(\d{4}\.\d{4,5})\b")
# Surname(s) then a year, in the usual citation shapes. Requires a capitalised
# surname so ordinary prose containing a year does not match.
AUTHOR_YEAR = re.compile(
    r"\(?\b([A-Z][A-Za-z\-']{2,})"
    r"(?:\s+(?:and|&)\s+[A-Z][A-Za-z\-']{2,}|\s+et\s+al\.?)?"
    r",?\s*\(?\b(1[89]\d{2}|20\d{2})\b\)?"
)


def scan():
    hits = {}          # reference string -> list of "path:line"
    for d in SCAN_DIRS:
        base = os.path.join(ROOT, d)
        if not os.path.isdir(base):
            continue
        for dirpath, dirnames, filenames in os.walk(base):
            dirnames[:] = [x for x in dirnames if x != "__pycache__"]
            for fn in filenames:
                if not fn.endswith((".py", ".sh")):
                    continue
                path = os.path.join(dirpath, fn)
                rel = os.path.relpath(path, ROOT)
                with open(path, encoding="utf-8", errors="replace") as fh:
                    for n, line in enumerate(fh, 1):
                        for m in ARXIV.finditer(line):
                            hits.setdefault(m.group(1), []).append(f"{rel}:{n}")
                        for m in AUTHOR_YEAR.finditer(line):
                            surname, year = m.group(1), m.group(2)
                            if surname.lower() in NOISE:
                                continue
                            # An arXiv id already captured on this line makes a
                            # bare "Xiv 2606"-style fragment redundant.
                            if ARXIV.search(line) and year.startswith("26"):
                                continue
                            hits.setdefault(f"{surname} {year}", []).append(f"{rel}:{n}")
    return hits


def main():
    if not os.path.exists(LEDGER):
        print(f"FAIL  ledger not found at {LEDGER}")
        return 1
    ledger = open(LEDGER, encoding="utf-8", errors="replace").read()

    hits = scan()
    if not hits:
        print("no citations found in src/ or scripts/ (suspicious, check the regexes)")
        return 1

    missing = []
    print(f"{'reference':<26} {'in ledger':<11} where")
    for ref in sorted(hits):
        locations = sorted(set(hits[ref]))
        if ref.startswith(tuple("0123456789")):
            present = ref in ledger
        else:
            surname, year = ref.rsplit(" ", 1)
            present = surname in ledger and year in ledger
        print(f"  {ref:<24} {'yes' if present else 'NO':<11} {', '.join(locations[:3])}"
              + (f" (+{len(locations)-3} more)" if len(locations) > 3 else ""))
        if not present:
            missing.append((ref, locations))

    print()
    if missing:
        print("FAIL: cited in committed source but ABSENT from docs/CITATION-LEDGER.md")
        for ref, locations in missing:
            print(f"  {ref}   at {', '.join(locations)}")
        print()
        print("Add each to the ledger before committing. A reference may sit there")
        print("as RECALLED; what it may not do is exist only in the source.")
        return 1

    print(f"All {len(hits)} source citations are tracked in the ledger.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
