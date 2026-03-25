# RER Doctor API — Version 1.0.0

## Overview
RER Doctor is a **read‑only**, **non‑blocking**, **non‑mutating** governance health tool.

It supports:

- Human-readable diagnostics
- JSON machine-readable diagnostics
- Stable exit codes
- Deterministic ordering for time-series analysis
- Versioned schema

## Usage

### Human-readable

./rer-doctor.sh

### JSON output

./rer-doctor.sh --json

## Exit Codes
| Code | Meaning |
|------|---------|
| 0 | OK |
| 10 | WARN |
| 20 | FAIL |
| 30 | INTERNAL ERROR |

## JSON Schema
See:

rer-doctor.schema.v1.json

## Determinism
All lists in JSON output are sorted lexicographically.

## Invariants
RER Doctor:
- never mutates state
- never blocks merges
- never enforces policy
- never rewrites workflows
- only provides visibility

This makes it safe for org‑wide, fleet-level telemetry.