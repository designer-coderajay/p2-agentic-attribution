"""Assert that the double-blind build does not identify its author.

ONE implementation, called by paper/Makefile, by CI, and by the session gate.
There were briefly two: a shell pipeline in the Makefile and a Python check in
the release gate. They disagreed, because the shell version anchored on a line
matching `^References$` and pdftotext emits that heading with trailing
whitespace, so `sed -n '1,/^References$/p'` fell through to end of file and the
bibliography entry was scanned as though it were body text. A false failure is
cheaper than a false pass, but two implementations of one rule is the defect
either way.

THE RULE. The author's name may appear in the bibliography, which is the ordinary
third-person citation of one's own published prior work and is accepted at most
double-blind venues. It must not appear anywhere before the References heading.

Confirm the bibliography allowance against the venue's submission guide before
submitting; a minority of venues require prior work to be cited as anonymous.

Usage: python3 scripts/check_anonymous.py [path/to/anon.pdf]
"""
import os
import re
import subprocess
import sys

# Names that identify the author. Kept here rather than in the caller so that
# adding a co-author is one edit in one place.
IDENTIFIERS = ("Ajay", "Mahale")

ROOT = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..")
DEFAULT = os.path.join(ROOT, "paper", "anon.pdf")


def main(pdf):
    if not os.path.exists(pdf):
        print(f"FAIL  {pdf} does not exist; build it with `make anon`")
        return 1
    try:
        txt = subprocess.run(["pdftotext", pdf, "-"], capture_output=True,
                             text=True, check=True).stdout
    except FileNotFoundError:
        print("SKIP  pdftotext is not installed, so the anonymous build was not "
              "checked. Install poppler-utils. This is a SKIP and not a PASS.")
        return 0
    except subprocess.CalledProcessError as e:
        print(f"FAIL  pdftotext exited {e.returncode} on {pdf}")
        return 1

    # Anchor on the heading with surrounding whitespace tolerated, and take the
    # LAST such heading, so a cross-reference to the word earlier in the text
    # cannot truncate the body early and hide a leak behind it.
    heads = list(re.finditer(r"(?m)^\s*References\s*$", txt))
    if not heads:
        print("FAIL  no References heading found; refusing to guess where the "
              "body ends, because guessing here fails open")
        return 1
    cut = heads[-1].start()
    body, refs = txt[:cut], txt[cut:]

    leaks = []
    for name in IDENTIFIERS:
        for m in re.finditer(re.escape(name), body):
            line = body.count("\n", 0, m.start()) + 1
            ctx = body[max(0, m.start() - 70):m.start() + 70].replace("\n", " ")
            leaks.append(f"    line {line}: ...{ctx}...")
    if leaks:
        print(f"FAIL  the author is identified in the body of {os.path.basename(pdf)}:")
        print("\n".join(leaks[:10]))
        return 1

    n_refs = sum(refs.count(name) for name in IDENTIFIERS)
    print(f"PASS  {os.path.basename(pdf)} body is anonymous; the author's name "
          f"is matched {n_refs} time(s) in the bibliography, which is the accepted "
          f"third-person citation of prior work")
    print("      Confirm that allowance against the venue's submission guide.")
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1] if len(sys.argv) > 1 else DEFAULT))
