#!/usr/bin/env bash
set -euo pipefail

ORG="$1"
FROM="$2"
TO="$3"

# Requires gh + jq
runs=$(gh run list --org "$ORG" --workflow rexce-validation.yml --json startedAt,completedAt,repository)

# Aggregation omitted for brevity — produce metrics JSON per schema

echo "[xce-metrics] metrics collected for $ORG"
``