#!/usr/bin/env bash
set -euo pipefail

VERSION="1.0.0"
MODE="human"

if [[ "${3:-}" == "--json" ]]; then
  MODE="json"
fi

BASE="$1"
TARGET="$2"
TIMESTAMP=$(date -u +"%Y-%m-%dT%H:%M:%SZ")

changed_files=$(git diff --name-only "$BASE" "$TARGET" | sort)

gov_paths=()
nongov_paths=()

while read -r f; do
  case "$f" in
    docs/GOVERNANCE-*|schemas/*|scripts/rer-*|scripts/gov-diff.sh)
      gov_paths+=("$f")
      ;;
    *)
      nongov_paths+=("$f")
      ;;
  esac
done <<< "$changed_files"

classification="TYPE-0"
reasons=()

if (( ${#gov_paths[@]} > 0 )); then
  classification="TYPE-2"
  reasons+=("Governance-relevant paths modified")
fi

if [[ "$MODE" == "json" ]]; then
cat <<EOF
{
  "version": "$VERSION",
  "base": "$BASE",
  "target": "$TARGET",
  "timestamp": "$TIMESTAMP",
  "summary": {
    "files_changed": $(echo "$changed_files" | wc -l),
    "governance_files_changed": ${#gov_paths[@]}
  },
  "classification": "$classification",
  "classification_reason": [
$(printf '    "%s",\n' "${reasons[@]}" | sed '$s/,$//')
  ],
  "governance_paths": [
$(printf '    "%s",\n' "${gov_paths[@]}" | sed '$s/,$//')
  ],
  "non_governance_paths": [
$(printf '    "%s",\n' "${nongov_paths[@]}" | sed '$s/,$//')
  ],
  "status": "OK"
}
EOF
exit 0
fi

echo "[GOV-DIFF] base=$BASE target=$TARGET"
echo "[GOV-DIFF] classification=$classification"
printf "  GOV  %s\n" "${gov_paths[@]}"
printf "  FILE %s\n" "${nongov_paths[@]}"
``