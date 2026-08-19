#!/usr/bin/env bash
# Single command that answers "is the repo currently correct".
# Every validation script asserts against a closed form or an exact answer and
# exits non-zero on failure. If this prints ALL GREEN, every number in
# docs/DERIVATIONS.md is reproducible on this machine.
set -uo pipefail
cd "$(dirname "$0")"
fail=0
for s in validate_estimators validate_coupling validate_analysis validate_ranking validate_mediation validate_primary; do
  printf '%-24s' "$s"
  if out=$(python3 "scripts/$s.py" 2>&1); then
    echo "PASS  $(echo "$out" | grep -o 'env_hash [0-9a-f]*' | head -1)"
  else
    echo "FAIL"; echo "$out" | tail -5; fail=1
  fi
done
printf '%-24s' "import surface"
python3 - <<'PY' || fail=1
import sys; sys.path.insert(0,'src')
import numpy as np
from p2 import scm, effects, coupling, mediation, observability, analysis, ranking
from p2.observability import ATTRIBUTORS
from p2.ranking import chi2_sf_df2, joint_wald
assert len(ATTRIBUTORS)==3, [a.name for a in ATTRIBUTORS]
assert all(a.provenance.startswith("VERIFIED") for a in ATTRIBUTORS)
assert abs(chi2_sf_df2(5.9915)-0.05) < 1e-4
W,q,p = joint_wald(np.array([0.,1.,1.]), np.diag([1.,.25,.25]), (1,2))
assert q==2 and abs(W-8.0)<1e-9
print("PASS  3 attributors, all VERIFIED; chi2 and Wald exact")
PY
[ $fail -eq 0 ] && echo "ALL GREEN" || { echo "NOT GREEN"; exit 1; }
