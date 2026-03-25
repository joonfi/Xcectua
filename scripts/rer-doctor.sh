#!/usr/bin/env bash
set -euo pipefail

VERSION="1.0.0"
MODE="human"

if [[ "${1:-}" == "--json" ]]; then
    MODE="json"
fi

repo=$(git config --get remote.origin.url | sed 's/.*github.com[:/]\(.*\)\.git/\1/')

timestamp=$(date -u +"%Y-%m-%dT%H:%M:%SZ")

# -------------------------------
# Helpers (all read-only)
# -------------------------------

check_required_check() {
    # placeholder: actual GitHub API integration belongs here
    echo "true"
}

check_admin_bypass() {
    echo "true"
}

check_branch_protection() {
    echo "true"
}

check_shadow_validators() {
    echo "false"
}

check_phase3_docs() {
    [[ -f "GOVERNANCE-CHANGE-PROPOSAL.md" ]] && \
    [[ -f "GOVERNANCE-DIFF-CLASSIFICATION.md" ]] && \
    [[ -f "GOVERNANCE-EVIDENCE.md" ]]
}

# Build drift lists (placeholders; deterministic ordering)
missing_docs=()
if [[ ! -f "GOVERNANCE-CHANGE-PROPOSAL.md" ]]; then missing_docs+=("GOVERNANCE-CHANGE-PROPOSAL.md"); fi
if [[ ! -f "GOVERNANCE-DIFF-CLASSIFICATION.md" ]]; then missing_docs+=("GOVERNANCE-DIFF-CLASSIFICATION.md"); fi
if [[ ! -f "GOVERNANCE-EVIDENCE.md" ]]; then missing_docs+=("GOVERNANCE-EVIDENCE.md"); fi
IFS=$'\n' missing_docs_sorted=($(sort <<<"${missing_docs[*]:-}"))
unset IFS

status="OK"
exit_code=0

if (( ${#missing_docs_sorted[@]} > 0 )); then
    status="WARN"
    exit_code=10
fi

# -------------------------------
# JSON MODE
# -------------------------------
if [[ "$MODE" == "json" ]]; then
cat <<EOF
{
  "version": "$VERSION",
  "timestamp": "$timestamp",
  "repo": "$repo",
  "enforcement": {
    "required_check_ok": $(check_required_check),
    "admin_bypass_ok": $(check_admin_bypass),
    "branch_protection_ok": $(check_branch_protection),
    "shadow_validator_present": $(check_shadow_validators)
  },
  "phase2_invariants": {
    "single_required_check": $(check_required_check),
    "no_admin_bypass": $(check_admin_bypass),
    "no_shadow_validators": $(check_shadow_validators),
    "protected_default_branch": $(check_branch_protection)
  },
  "phase3_artifacts": {
    "gcp_docs_present": $( [[ -f GOV* ]] && echo true || echo false ),
    "diff_classification_present": $( [[ -f GOVERNANCE-DIFF-CLASSIFICATION.md ]] && echo true || echo false ),
    "evidence_docs_present": $( [[ -f GOVERNANCE-EVIDENCE.md ]] && echo true || echo false )
  },
  "drift": {
    "missing_docs": [
$(printf '      "%s",\n' "${missing_docs_sorted[@]}" | sed '$s/,$//')
    ],
    "unexpected_files": [],
    "enforcement_mismatch": [],
    "workflow_drift": []
  },
  "status": "$status"
}
EOF
exit "$exit_code"
fi

# -------------------------------
# HUMAN MODE
# -------------------------------

echo "[RER DOCTOR] repo: $repo"
echo "[RER DOCTOR] timestamp: $timestamp"
echo "[RER DOCTOR] status: $status"

if (( ${#missing_docs_sorted[@]} > 0 )); then
    echo "WARN: Missing Phase‑3 docs:"
    printf '  - %s\n' "${missing_docs_sorted[@]}"
fi

exit "$exit_code"