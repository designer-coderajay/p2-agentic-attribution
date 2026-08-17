# Getting this onto your machine and into GitHub

## 1. Desktop

Download `p2-agentic-attribution.zip` from this conversation and unzip it wherever
you keep work. It already contains a `.git` directory with a real commit, so it is
a working repository the moment it lands, not a folder of loose files.

```bash
cd ~/Desktop
unzip p2-agentic-attribution.zip
cd p2-agentic-attribution
git log --stat          # the initial commit, timestamped
python3 -m pip install -r requirements.txt
python3 scripts/validate_estimators.py
python3 scripts/validate_coupling.py
```

Both scripts should print their tolerance tables and exit 0. If either fails on
your machine, that is a real signal: the numbers in `docs/DERIVATIONS.md` are
environment-dependent in a way they should not be, and it needs investigating
before anything is written.

## 2. GitHub

I cannot push for you. Pushing needs credentials, and I do not handle tokens or
passwords. Two lines from you:

```bash
gh repo create p2-agentic-attribution --private --source=. --remote=origin --push
```

or, without the GitHub CLI, create an empty private repo in the web UI and then:

```bash
git remote add origin git@github.com:<you>/p2-agentic-attribution.git
git branch -M main
git push -u origin main
```

**Make it private.** Not for secrecy about the method, but because
`docs/POSITIONING.md` contains a frank internal assessment of which contributions
survived contact with the 2026 literature and which did not. That document is for
you, not for a reviewer who finds it before the paper exists.

## 3. If you want me pushing directly from here

There is no GitHub connector active in this session. If you connect one, I can
commit and push as part of the daily loop rather than handing you a zip each time.
Worth doing before Stage 1 starts producing results, because at that point the
commit-per-figure discipline in standing rule 10 stops being optional.
