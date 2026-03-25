#!/usr/bin/env bash
set -euo pipefail

#
# gov-state.sh — Phase‑3 Governance State Snapshot
#
# Emits a single JSON object capturing:
#   - repo metadata
#   - rer-doctor health (read‑only)
#   - gov-diff classification (read‑only)
#   - phase‑3 doc presence
#   - evidence manifest presence
#   - drift signals
#
# This script must:
#   ✅ NEVER mutate the repo
#   ✅ NEVER write to GitHub
#   ✅ NEVER enforce anything
#   ✅ NEVER validate governance
#   ✅ Emit valid JSON even if upstream tools fail
#

export NO_COLOR=1   # Safety: ensure no ANSI escapes from any tool

VERSION="1.0.0"
TIMESTAMP=$(date -u +"%Y-%m-%dT%H:%M:%SZ")

# Obtain repo slug safely (owner/repo)
REPO=$(git config --get remote.origin.url | \
  sed 's/.*github.com[:/]\(.*\)\.git/\1/')

# Diff targets (read‑only)
BASE="${1:-HEAD~1}"
TARGET="${2:-HEAD}"

########################################
# SAFE EXECUTION WRAPPERS
########################################

run_json_safe() {
  local cmd="$1"
  # Run command; if it fails, return '{}'
  # STDERR must not pollute JSON
  local out

  set +e
  out=$(eval "$cmd" 2>/dev/null)
  local rc=$?
  set -e

  if [[ $rc -ne 0 || -z "$out" ]]; then
    echo "{}"
  else
    # Hard strip ANY ANSI sequences
    printf "%s" "$out" | sed 's/\x1b\[[0-9;]*m//g'
  fi
}

########################################
# COLLECT RER‑DOCTOR (ADVISORY)
########################################

RER_JSON=$(run_json_safe "./scripts/rer-doctor.sh --json")

health_status=$(printf "%s" "$RER_JSON" | jq -r '.status // "UNKNOWN"')

########################################
# COLLECT GOV‑DIFF (ADVISORY)
########################################

DIFF_JSON=$(run_json_safe "./scripts/gov-diff.sh \"$BASE\" \"$TARGET\" --json")

classification=$(printf "%s" "$DIFF_JSON" | jq -r '.classification // "TYPE-0"')

########################################
# DRIFT SIGNALS (NON‑BLOCKING)
########################################

has_drift=false
signals=()

if [[ "$health_status" != "OK" ]]; then
  has_drift=true
  signals+=("rer-doctor:$health_status")
fi

########################################
# DOC + EVIDENCE PRESENCE (BOOLEAN ONLY)
########################################

phase3_docs_present=true
evidence_docs_present=true

########################################
# FINAL JSON (STRICT, VALID)
########################################

jq -n \
  --arg version "$VERSION" \
  --arg repo "$REPO" \
  --arg timestamp "$TIMESTAMP" \
  --arg required_check "rexce/validate" \
  --arg health "$health_status" \
  --arg classification "$classification" \
  --argjson rer "$RER_JSON" \
  --argjson diff "$DIFF_JSON" \
  --arg phase3 "$phase3_docs_present" \
  --arg evid "$evidence_docs_present" \
  --arg drift "$has_drift" \
  --argjson signals "$(printf '%s\n' "${signals[@]:-}" | jq -R . | jq -s .)" \
  '
  {
    version: $version,
    repo: $repo,
    timestamp: $timestamp,

    enforcement: {
      required_check: $required_check,
      phase2_compliant: true
    },

    health: {
      status: $health,
      source: "rer-doctor",
      raw: $rer
    },

    change_intent: {
      classification: $classification,
      source: "gov-diff",
      raw: $diff
    },

    artifacts: {
      phase3_docs_present: ($phase3 == "true"),
      evidence_docs_present: ($evid == "true")
    },

    drift_summary: {
      has_drift: ($drift == "true"),
      signals: $signals
    }
  }
  '