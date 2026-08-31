#!/usr/bin/env bash
# Single command that answers "is the repo currently correct".
# Every validation script asserts against a closed form or an exact answer and
# exits non-zero on failure. If this prints ALL GREEN, every number in
# docs/DERIVATIONS.md is reproducible on this machine.
set -uo pipefail
cd "$(dirname "$0")"
fail=0
for s in validate_estimators validate_coupling validate_analysis validate_ranking validate_mediation validate_primary validate_suppression; do
  printf '%-24s' "$s"
  if out=$(python3 "scripts/$s.py" 2>&1); then
    echo "PASS  $(echo "$out" | grep -o 'env_hash [0-9a-f]*' | head -1)"
  else
    echo "FAIL"; echo "$out" | tail -5; fail=1
  fi
done
printf '%-24s' "citation coverage"
# Every reference cited in committed SOURCE must be tracked in the ledger.
# Added 2026-08-23 after "(Fieller 1954)" sat in a ranking.py docstring for
# three days with no ledger entry, justifying a pre-registered analysis choice
# while in a RECALLED state. It was caught by eye, by a different session.
# Noticing is not a control; this is.
if out=$(python3 scripts/check_citations.py 2>&1); then
  echo "PASS  $(echo "$out" | tail -1)"
else
  echo "FAIL"; echo "$out" | tail -8; fail=1
fi

printf '%-24s' "import surface"
python3 - <<'PY' || fail=1
import sys; sys.path.insert(0,'src')
import numpy as np
from p2 import scm, effects, coupling, mediation, observability, analysis, ranking
from p2.observability import ATTRIBUTORS
from p2.ranking import chi2_sf_df2, joint_wald, normalized_beta, CAUTION_K
assert len(ATTRIBUTORS)==3, [a.name for a in ATTRIBUTORS]
assert all(a.provenance.startswith("VERIFIED") for a in ATTRIBUTORS)
assert abs(chi2_sf_df2(5.9915)-0.05) < 1e-4
W,q,p = joint_wald(np.array([0.,1.,1.]), np.diag([1.,.25,.25]), (1,2))
assert q==2 and abs(W-8.0)<1e-9
# CAUTION_K is pre-registered (PREREG s2). Pin the value so a silent retune
# cannot change what a reader is told about how far to trust the direction.
assert CAUTION_K == 2.0, f"CAUTION_K retuned to {CAUTION_K}; PREREG s2 locks 2.0"
# g = beta/||beta|| must be exactly invariant to the PL scale ambiguity.
b = np.array([-0.029, 0.067, 0.780]); V = np.diag([0.0055, 0.0092, 0.0098])
g1,_,_ = normalized_beta(b, V); g2,_,_ = normalized_beta(7.5*b, 56.25*V)
assert np.allclose(g1, g2, atol=1e-12), "normalized_beta lost scale invariance"
print("PASS  3 attributors; chi2/Wald exact; CAUTION_K=2.0; g scale-invariant")
PY
[ $fail -eq 0 ] && echo "ALL GREEN" || { echo "NOT GREEN"; exit 1; }
