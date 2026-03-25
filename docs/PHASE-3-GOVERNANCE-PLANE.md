# Phase‑3 Governance Plane — v1.0

## Status
**Locked — Stable**

This document defines the formal scope, authority boundaries, and immutability
of the Phase‑3 Governance Plane.

---

## Purpose

Phase‑3 enables governance **evolution, observability, and evidence handling**
without altering Phase‑2 enforcement.

It introduces:
- telemetry
- diff visibility
- evidence automation
- org‑wide observability
- performance modeling

It introduces **no enforcement authority**.

---

## Included Capabilities (v1.0)

### Repo‑Level Telemetry
- RER Doctor JSON API
- gov‑diff JSON API
- governance state snapshot

### Org‑Level Visibility
- xcelist aggregation
- org governance snapshot
- human‑readable reports

### Evidence Automation
- evidence manifest
- deterministic bundling
- completeness signaling (non‑blocking)

### Performance Modeling
- validation runtime telemetry
- governance metrics
- advisory SLO modeling

---

## Explicit Non‑Goals

Phase‑3 does **not**:
- validate governance
- enforce policy
- block merges
- modify branch protection
- publish evidence automatically
- mutate repositories

---

## Authority Boundaries

| Layer | Role |
|-----|-----|
| rexce | Canonical validator (authoritative) |
| GitHub | Enforcement engine |
| Xcectua | Orchestration & visibility only |
| govops | Human interpretation only |

---

## Versioning Rules

- Phase‑3 v1.0 is **stable**
- Schemas are frozen under `v1`
- Breaking changes require `v2` + GCP
- Additive changes may occur under `v1.x`

---

## Forward Compatibility

- Phase‑4 extends platform support only
- Phase‑5 extends lifecycle orchestration only
- Neither may alter Phase‑3 semantics

This document is the **constitution of Phase‑3**.
