# Phase‑2 Invariants (Frozen)

## Status
**Frozen — Non‑Negotiable**

Phase‑2 defines the immutable enforcement foundation of the governance system.
No Phase‑3, Phase‑4, or Phase‑5 work may weaken or reinterpret these invariants.

---

## Canonical Enforcement Rules

1. **Single Required Check**
   - Exactly one required status check:
     ```
     rexce/validate
     ```
   - Case‑ and slash‑sensitive.
   - No substitutes.

2. **Canonical Validator**
   - All governance validation logic exists **only** in `rexce`.
   - No duplication.
   - No shadow validators.
   - No local re‑implementation.

3. **Non‑Bypassable Enforcement**
   - Admin bypass is disabled.
   - No override mechanisms.
   - Failure of `rexce/validate` makes merge impossible.

4. **GitHub‑Native Enforcement Only**
   - Enforcement uses GitHub branch protection primitives only.
   - No external enforcement systems.
   - No fork‑only authority.

5. **Determinism**
   - Validation behavior is deterministic.
   - No environment‑dependent exceptions.
   - No silent auto‑fixes.

---

## Change Policy

- Phase‑2 behavior **cannot be changed** via Phase‑3 governance evolution.
- Any modification requires escalation beyond Phase‑3.

---

## Purpose

Phase‑2 exists to ensure that:
- governance truth is singular
- enforcement is unambiguous
- evolution never weakens protection

Phase‑3 may evolve **process**, **visibility**, and **evidence** —
but **never enforcement semantics**.