# Governance State API — Version 1.0.0

## Purpose
The governance state snapshot provides a **single, read‑only representation**
of repository governance posture at a point in time.

It composes:
- RER Doctor health
- gov-diff change intent
- static enforcement metadata

## Generation

./gov-state.sh > governance_state.json

## Invariants
The governance state:
- does not validate governance
- does not enforce policy
- does not block merges
- does not invent signals
- is safe to aggregate org-wide
