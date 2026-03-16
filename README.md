# Xcectua

Xcectua is the **reference implementation of the Xcectua Interface** and is a
**separate repository** from `rexce`.

The **Xcectua Interface** (published inside the `rexec` repository) defines the
mandatory consumer governance circuit for validating release evidence.  
Xcectua demonstrates how that interface behaves in a real repository, with real
CI execution, real signature verification, and real PDR generation.

---

## What Xcectua *is*

- A **runnable, auditable example** of a consumer repository
- A demonstration of **correct enforcement** of the Xcectua Interface
- A showcase of:
  - pinning `rexce` through `rer.lock.yml`
  - running the mandatory governance gate
  - verifying cosign signatures
  - generating and uploading a **Policy Decision Record (PDR)**

It exists to help developers understand and correctly implement the interface.

---

## What Xcectua *is not*

- **Not** part of `rexec`
- **Not** a policy authority
- **Not** a source of truth for governance templates
- **Not** a dependency for other repositories

Consumers must **not** copy files from the Xcectua repo.  
They must copy governance files **only** from the Xcectua Interface inside:
rexec/rexce/xcectua-interface/templates/xcectua-circuit/

This ensures governance invariants cannot drift.

---

## Non‑negotiable Requirements (as interface implementer)

Xcectua implements the following mandatory behaviors:

- Evidence is required (`releases/**/release-record.json` must exist)
- Rexec is pinned via: rer/rer.lock.yml
- Cosign signature verification is mandatory  
- Required refs must match: data.policy.signature.verify_refs.required
- The PDR (Policy Decision Record) is always uploaded (`if: always()`)
- Mandatory CI workflow: .github/workflows/rer-governance-gate.yml
- Governance‑sensitive files protected via CODEOWNERS: /rer/rer.lock.yml
/.github/workflows/rer-governance-gate.yml

---

## Required Secrets

The repository requires one secret to run the governance gate:

- `COSIGN_PUBLIC_KEY` — public half of the cosign keypair used to verify evidence signatures

---

## Summary

Xcectua is a **live, enforced, end‑to‑end reference implementation** of the
consumer governance circuit.  
It shows exactly how a real repo should behave when implementing the **Xcectua
Interface**, while remaining separate from and subordinate to the `rexec`
policy authority:

rexce  →  publishes policies + interface,
Xcectua Interface  →  canonical consumer templates,
Xcectua repo  →  human-readable, runnable example.
