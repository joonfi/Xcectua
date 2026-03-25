# gov-diff API — Version 1.0.0

## Purpose
gov-diff provides **read-only, deterministic governance-aware diffs**.

It:
- never enforces policy
- never blocks merges
- never mutates state
- classifies changes using documented rules

## Usage

./gov-diff.sh <base> <target>
./gov-diff.sh <base> <target> --json

## Classification
Classification is derived strictly from:

docs/GOVERNANCE-DIFF-CLASSIFICATION.md

gov-diff does not invent policy.

## Exit Codes
0 — diff produced  
30 — internal error

## Invariants
gov-diff:
- is informational only
- has no authority
- cannot affect enforcement