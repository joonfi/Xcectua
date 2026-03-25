#!/usr/bin/env bash
set -euo pipefail

#
# xcereport.sh
#
# Render human-readable governance reports from a generated
# governance-org.json snapshot.
#
# Invariants:
# - read-only
# - no repo mutation
# - no enforcement
# - no validation
# - no network calls
#

if [[ $# -ne 1 ]]; then
  echo "Usage: xcereport.sh <governance-org.json>" >&2
  exit 30
fi

INPUT="$1"

if [[ ! -f "$INPUT" ]]; then
  echo "ERROR: file not found: $INPUT" >&2
  exit 30
fi

# jq is required for report rendering
if ! command -v jq >/dev/null 2>&1; then
  echo "ERROR: jq is required" >&2
  exit 30
fi

ORG=$(jq -r '.org' "$INPUT")
TIMESTAMP=$(jq -r '.timestamp' "$INPUT")

OUTDIR="reports/latest"
mkdir -p "$OUTDIR"

SUMMARY_MD="$OUTDIR/governance-summary.md"
DRIFT_CSV="$OUTDIR/drift-matrix.csv"

# -----------------------------
# Governance Summary (Markdown)
# -----------------------------

cat > "$SUMMARY_MD" <<EOF
# Org Governance Summary

**Organization:** $ORG  
**Snapshot Timestamp:** $TIMESTAMP  

## Overview

EOF

jq -r '
.summary
| "- Total repositories: \(.repos_total)\n"
+ "- Phase-2 compliant: \(.repos_phase2_compliant)\n"
+ "- Repositories with drift: \(.repos_with_drift)\n"
+ "- Repositories with TYPE-3 changes: \(.repos_type3_changes)\n"
' "$INPUT" >> "$SUMMARY_MD"

cat >> "$SUMMARY_MD" <<EOF

## Repository Status

| Repository | Health | Change Type | Drift |
|-----------|--------|-------------|-------|
EOF

jq -r '
.repos[]
| "| \(.repo) | \(.health) | \(.classification) | \(.has_drift) |"
' "$INPUT" >> "$SUMMARY_MD"

# -----------------------------
# Drift Matrix (CSV)
# -----------------------------

cat > "$DRIFT_CSV" <<EOF
repo,health,classification,has_drift
EOF

jq -r '
.repos[]
| "\(.repo),\(.health),\(.classification),\(.has_drift)"
' "$INPUT" >> "$DRIFT_CSV"

# -----------------------------
# Console Output
# -----------------------------

echo "[xcereport] rendered reports:"
echo "  - $SUMMARY_MD"
echo "  - $DRIFT_CSV"

exit 0