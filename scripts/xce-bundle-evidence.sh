#!/usr/bin/env bash
set -euo pipefail

MANIFEST="$1"

if [[ ! -f "$MANIFEST" ]]; then
  echo "ERROR: manifest not found: $MANIFEST" >&2
  exit 30
fi

if ! command -v jq >/dev/null; then
  echo "ERROR: jq required" >&2
  exit 30
fi

# Validate schema (optional but recommended)
# jsonschema -i "$MANIFEST" schemas/evidence-manifest.schema.v1.json

missing=0
paths=$(jq -r '.required_evidence[].path' "$MANIFEST")

for p in $paths; do
  if [[ ! -f "$p" ]]; then
    echo "ERROR: missing required evidence: $p" >&2
    missing=1
  fi
done

[[ $missing -eq 1 ]] && exit 20

OUT="evidence-bundle-$(date -u +%Y%m%dT%H%M%SZ).tar.gz"
tar -czf "$OUT" $(jq -r '.required_evidence[].path' "$MANIFEST") "$MANIFEST"

sha256sum "$OUT"

echo "[xce-bundle-evidence] created $OUT"
``