#!/usr/bin/env bash
set -euo pipefail

ORG="$1"
VERSION="1.0.0"
TIMESTAMP=$(date -u +"%Y-%m-%dT%H:%M:%SZ")

repos=$(gh repo list "$ORG" --limit 500 --json nameWithOwner -q '.[].nameWithOwner')

results=()
repos_total=0
repos_phase2=0
repos_drift=0
repos_type3=0

for repo in $repos; do
  repos_total=$((repos_total+1))
  tmp=$(mktemp)

  gh repo clone "$repo" -- --depth 1 >/dev/null 2>&1
  dir=$(basename "$repo")
  pushd "$dir" >/dev/null

  ./scripts/gov-state.sh > "$tmp"
  health=$(jq -r '.health.status' "$tmp")
  class=$(jq -r '.change_intent.classification' "$tmp")
  drift=$(jq -r '.drift_summary.has_drift' "$tmp")

  [[ "$drift" == "true" ]] && repos_drift=$((repos_drift+1))
  [[ "$class" == "TYPE-3" ]] && repos_type3=$((repos_type3+1))
  [[ "$health" == "OK" ]] && repos_phase2=$((repos_phase2+1))

  results+=("{\"repo\":\"$repo\",\"health\":\"$health\",\"classification\":\"$class\",\"has_drift\":$drift}")

  popd >/dev/null
  rm -rf "$dir" "$tmp"
done

cat <<EOF
{
  "version": "$VERSION",
  "timestamp": "$TIMESTAMP",
  "org": "$ORG",
  "summary": {
    "repos_total": $repos_total,
    "repos_phase2_compliant": $repos_phase2,
    "repos_with_drift": $repos_drift,
    "repos_type3_changes": $repos_type3
  },
  "repos": [
$(printf '    %s,\n' "${results[@]}" | sed '$s/,$//')
  ]
}
EOF