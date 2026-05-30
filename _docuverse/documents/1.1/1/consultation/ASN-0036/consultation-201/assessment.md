# Channel Assignment — ASN-0036 review-201

**Date:** 2026-05-30 00:52

## Issue 1: S8 statement asserts the δ-formula for `shift(a, k)` at `k = 0`, where it is undefined
Reason: Internal fix. The defect is a mismatch between the statement's blanket `0 ≤ k < n` δ-formula and the proof's own `k = 0` / `k ≥ 1` case split; the convention `shift(t, 0) := t` and OrdinalDisplacement's `n ≥ 1` precondition are already present in the ASN. No design intent or implementation evidence is needed.

## Issue 2: S8 statement carries proof-grade derivation duplicated in the proof body
Reason: Internal fix. Removing the re-derived well-definedness argument from conjunct (b) and leaving it to the proof is a pure restatement using S2 and S3, both already established in this ASN.

## Issue 3: S8a definition enumerates its downstream consumers
Reason: Internal fix. Deleting the consumer list is a mechanical removal that subtracts no semantic content from S8a; nothing external is consulted.

## Issue 4: Domain restriction and S8a state one constraint twice
Reason: Internal fix. Collapsing the duplicated set-form and per-component statements into one, with the T0 equivalence note, relies only on the ASN's own definitions and T0 (ASN-0034).
