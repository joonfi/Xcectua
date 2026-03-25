# Evidence Manifest API

## Purpose
Declare what evidence exists for a governance change
and allow **machine verification of completeness**.

---

## Properties

- GCP identifier
- Classification
- Required evidence list
- Optional evidence list

---

## Invariants

- Completeness ≠ correctness
- No auto‑publication
- No validation authority
- Local‑first by default

---

## Lifecycle

1. Manifest created
2. Evidence produced
3. Completeness checked
4. Evidence bundled explicitly
5. PR submitted