#!/usr/bin/env bash
# Shell only orchestrates. Sounio assertions and executable exit codes judge
# mathematical instances; no Python or foreign-runtime numerical golden.
set -euo pipefail
: "${SOUNIO_REPO:?Set SOUNIO_REPO to a Sounio checkout with Madaros available}"
HERE="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
OUT="${RCDA_OUT_DIR:-$HERE/verification}"
mkdir -p "$OUT"
if [[ -n "${SOUNIO_SOUC_BIN:-}" || "${SOUNIO_SOUC_ENGINE:-}" == lean_single ]]; then
  echo 'FAIL: raw/legacy engine overrides are not accepted by this gate' >&2
  exit 1
fi
source "$SOUNIO_REPO/scripts/lib/resolve_souc.sh"
sounio_require_souc
printf '%s\n' "$SOUC_BIN" > "$OUT/resolved-entrypoint.txt"
"$SOUC_BIN" --version > "$OUT/compiler-version.log" 2>&1
if ! grep -q 'Madaros' "$OUT/compiler-version.log"; then
  echo 'FAIL: this gate requires the default Madaros engine' >&2
  exit 1
fi
"$SOUNIO_REPO/bin/madaros" info > "$OUT/compiler-info.log" 2>&1
RAW="$(sed -n 's/^raw_elf: *//p' "$OUT/compiler-info.log")"
test -f "$RAW"
sha256sum "$RAW" > "$OUT/compiler.sha256"
sha256sum "$SOUC_BIN" "$SOUNIO_REPO/bin/madaros" > "$OUT/wrappers.sha256"
git -C "$SOUNIO_REPO" rev-parse HEAD > "$OUT/repository-head.txt"
git -C "$SOUNIO_REPO" branch --show-current > "$OUT/repository-branch.txt"
git -C "$SOUNIO_REPO" status --porcelain | wc -l > "$OUT/repository-dirty-count.txt"
sha256sum "$HERE/rcda_core.sio" "$HERE/verify.sh" > "$OUT/source.sha256"

compile_case() {
  local source="$1" label="$2"
  timeout 45 "$SOUC_BIN" check "$source" > "$OUT/$label.check.log" 2>&1
  timeout 45 "$SOUC_BIN" compile "$source" -o "$OUT/$label.elf" > "$OUT/$label.compile.log" 2>&1
  if grep -q 'NATIVE_REFUSAL' "$OUT/$label.compile.log"; then
    echo "FAIL: native refusal in $label" >&2
    exit 1
  fi
  test -s "$OUT/$label.elf"
}
compile_case "$HERE/rcda_core.sio" positive
timeout 20 "$OUT/positive.elf" > "$OUT/positive.run.log" 2>&1
grep -qx 'RCDA_SOUNIO_PASS' "$OUT/positive.run.log"
printf 'case\texpected\tobserved\npositive\t0\t0\n' > "$OUT/results.tsv"

expect_rejection() {
  local source="$1" label="$2" marker="$3"
  compile_case "$source" "$label"
  local code=0
  timeout 20 "$OUT/$label.elf" > "$OUT/$label.run.log" 2>&1 || code=$?
  if [[ "$code" == 0 || "$code" == 124 || "$code" == 137 || "$code" == 139 ]]; then
    echo "FAIL: $label did not produce a controlled rejection (exit $code)" >&2
    exit 1
  fi
  grep -Fq "$marker" "$OUT/$label.run.log"
  if grep -qx 'RCDA_SOUNIO_PASS' "$OUT/$label.run.log"; then
    echo "FAIL: $label reported success after rejection" >&2
    exit 1
  fi
  printf '%s\tcontrolled_nonzero\t%s\n' "$label" "$code" >> "$OUT/results.tsv"
}

# Mutation 1: a compiler/kernel that returns zero for every product must fail.
sed 's/let term = basis_sign(a.dim, i, j) \* a.c\[i as usize\] \* b.c\[j as usize\]/let term: i64 = 0/' \
  "$HERE/rcda_core.sio" > "$OUT/mutant_zero.sio"
expect_rejection "$OUT/mutant_zero.sio" mutant_zero 'FAIL embedded basis product vanished'

# Mutation 2: wrong complementary zero divisor must fail.
sed 's/let y = cd_sub(cd_basis(16, 4), cd_basis(16, 15))/let y = cd_sub(cd_basis(16, 4), cd_basis(16, 14))/' \
  "$HERE/rcda_core.sio" > "$OUT/mutant_pair.sio"
expect_rejection "$OUT/mutant_pair.sio" mutant_pair 'FAIL nontrivial annihilation'

# Mutation 3: omission of the quadratic curvature contribution must fail.
sed 's/let rhs = m_add(m_add(reference, linear_term), quadratic)/let rhs = m_add(reference, linear_term)/' \
  "$HERE/rcda_core.sio" > "$OUT/mutant_curvature.sio"
expect_rejection "$OUT/mutant_curvature.sio" mutant_curvature 'FAIL curvature deformation'

# Bounds are runtime refusals, never silent overflow or silent projection.
sed 's/fn main()/fn original_main()/' "$HERE/rcda_core.sio" > "$OUT/reject_bound.sio"
cat >> "$OUT/reject_bound.sio" <<'SIO'
fn main() -> i64 with IO, Mut, Panic, Div {
    var a = cd_basis(8, 1)
    a.c[1] = 1000001
    let ignored = cd_mul(a, cd_basis(8, 0))
    0
}
SIO
expect_rejection "$OUT/reject_bound.sio" reject_bound 'RCDA: coefficient outside exact domain'

sed 's/fn main()/fn original_main()/' "$HERE/rcda_core.sio" > "$OUT/reject_dimension.sio"
cat >> "$OUT/reject_dimension.sio" <<'SIO'
fn main() -> i64 with IO, Mut, Panic, Div {
    let ignored = cd_mul(cd_basis(8, 1), cd_basis(16, 1))
    0
}
SIO
expect_rejection "$OUT/reject_dimension.sio" reject_dimension 'RCDA: dimension mismatch'

sha256sum -c "$OUT/compiler.sha256" > "$OUT/compiler-stability.log"
sha256sum -c "$OUT/wrappers.sha256" >> "$OUT/compiler-stability.log"
sha256sum -c "$OUT/source.sha256" > "$OUT/source-stability.log"
sha256sum "$OUT/positive.elf" > "$OUT/executable.sha256"
cat "$OUT/results.tsv"
echo 'RCDA_SOUNIO_GATE_PASS'
