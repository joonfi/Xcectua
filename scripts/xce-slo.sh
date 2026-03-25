#!/usr/bin/env bash
set -euo pipefail

#
# xce-slo.sh
#
# Governance SLO modeling tool.
#
# Invariants:
# - read-only
# - advisory only
# - no enforcement
# - no validation
# - no repo mutation
#

if [[ $# -ne 1 ]]; then
  echo "Usage: xce-slo.sh <governance-metrics.json>" >&2
  exit 30
fi

INPUT="$1"

if [[ ! -f "$INPUT" ]]; then
  echo "ERROR: file not found: $INPUT" >&2
  exit 30
fi

if ! command -v jq >/dev/null 2>&1; then
  echo "ERROR: jq is required" >&2
  exit 30
fi

OUTDIR="reports/performance"
mkdir -p "$OUTDIR"

REPORT="$OUTDIR/slo-report.md"

ORG=$(jq -r '.org' "$INPUT")
FROM=$(jq -r '.window.from' "$INPUT")
TO=$(jq -r '.window.to' "$INPUT")

AVG=$(jq -r '.metrics.avg_duration_sec' "$INPUT")
P95=$(jq -r '.metrics.p95_duration_sec' "$INPUT")
P99=$(jq -r '.metrics.p99_duration_sec' "$INPUT")
TOTAL=$(jq -r '.metrics.runs_total' "$INPUT")

cat > "$REPORT" <<EOF
# Governance SLO Report

**Organization:** $ORG  
**Window:** $FROM → $TO  

## Overall Validation Performance

- Total validation runs: $TOTAL
- Average validation time: ${AVG}s
- P95 validation time: ${P95}s
- P99 validation time: ${P99}s

## Validation Performance by Change Classification

| Classification | Runs | Avg Duration (s) |
|----------------|------|------------------|
EOF

jq -r '
.metrics.by_classification
| to_entries[]
| "| \(.key) | \(.value.runs) | \(.value.avg_duration_sec) |"
' "$INPUT" >> "$REPORT"

cat >> "$REPORT" <<EOF

## Interpretive Guidance (Advisory)

- This report is **observational**, not normative.
- SLOs are **expectations**, not enforcement thresholds.
- Longer runtimes for TYPE‑3 changes are expected and healthy.
- Sudden regressions, not absolute values, warrant investigation.

## Explicit Non‑Goals

This report:
- does NOT block merges
- does NOT alter enforcement
- does NOT judge governance correctness
- does NOT recommend bypasses
- does NOT optimize away validation

Governance cost is measured to be **understood**, not minimized blindly.
EOF

echo "[xce-slo] generated $REPORT"
exit 0