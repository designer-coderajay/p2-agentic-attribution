# Getting this onto your machine and into GitHub

## 1. Desktop

Target location:

```
~/Desktop/Evidential Validity of AI Explanations/p2-agentic-attribution
```

The folder name has spaces, so every path below is quoted. Unquoted paths are
why the first attempt failed.

```bash
cd ~/Downloads
unzip -o p2-agentic-attribution.zip
rsync -a p2-agentic-attribution/ \
  ~/Desktop/"Evidential Validity of AI Explanations"/p2-agentic-attribution/
cd ~/Desktop/"Evidential Validity of AI Explanations"/p2-agentic-attribution
git log --stat
python3 -m pip install -r requirements.txt
python3 scripts/validate_estimators.py
python3 scripts/validate_coupling.py
```

`rsync` rather than `mv` because the destination folder already exists.

## 2. iCloud, and why this location is a bad idea

Your Desktop is iCloud-synced and Finder reports storage full, zero bytes
available. Two consequences, both real:

1. **iCloud evicts files it thinks are cold and replaces them with placeholders.**
   When it does that to objects inside `.git`, the repository corrupts, and the
   corruption is usually discovered later, at the point of a push or a checkout.
   Git in an iCloud-synced folder is a known way to lose work.
2. With zero bytes available, writes may fail silently or partially.

Recommendation: keep the working repository outside iCloud and let the synced
folder hold only the finished artifacts.

```bash
mkdir -p ~/research && cd ~/research
rsync -a ~/Downloads/p2-agentic-attribution/ ./p2-agentic-attribution/
```

Your call. If you want it on the Desktop regardless, at minimum clear iCloud
space first, because a repository that cannot write is worse than no repository.

## 3. GitHub

I cannot push. That needs credentials, and I do not handle tokens or passwords.
There is also no GitHub connector available in this session, so there is no
authorised path from here either.

```bash
gh repo create p2-agentic-attribution --private --source=. --remote=origin --push
```

or, without the GitHub CLI, create an empty private repo in the web UI, then:

```bash
git remote add origin git@github.com:<you>/p2-agentic-attribution.git
git branch -M main
git push -u origin main
```

**Private.** `docs/POSITIONING.md` is a frank internal assessment of which
contributions survived the 2026 literature and which did not. That document is
for you, not for a reviewer who finds it before the paper exists.
