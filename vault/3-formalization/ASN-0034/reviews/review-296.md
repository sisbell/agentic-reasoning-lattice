# Cone Review — ASN-0034/TS5 (cycle 6)

*2026-04-18 14:36*

### TS3 and TS4 Depends enumerate only `n ∈ ℕ` at their OrdinalShift invocations, diverging from TS5's explicit per-step discipline

**Foundation**: TS5's own OrdinalShift Depends entry (applied after the previous finding flagged its omission) articulates the discipline: "OrdinalShift's three preconditions at the instantiation `v = v, n = n₁` are discharged to named sources: `v ∈ T` from TS5's own precondition... `n₁ ∈ ℕ` from TS5's own precondition... `n₁ ≥ 1` from TS5's own precondition... Each of the three transfers is trivial — all three sources are TS5's own preconditions — but under the per-step discharge discipline TS5 enforces at its TS3 and TS4 entries (where every precondition is named to a source regardless of transfer-triviality)... each must still be the named source."

**ASN**:
- TS3's Depends for OrdinalShift: "OrdinalShift's `n ∈ ℕ` precondition is discharged at each of the three invocation sites to a named source: at `(v, n₁)` from TS3's own precondition `n₁ ∈ ℕ`... at `(u, n₂)` from TS3's own precondition `n₂ ∈ ℕ`... at `(v, n₁ + n₂)` from the right-side preface's `n₁ + n₂ ∈ ℕ`". Only `n ∈ ℕ` is enumerated at each of the three sites; `v ∈ T` / `u ∈ T` is treated separately only at the non-trivial second-shift site (via TA0's exported postcondition), and `n ≥ 1` (and `n₁ + n₂ ≥ 1`) is named only where non-trivial derivation is required. The trivial transfers of `v ∈ T` at the first and third shifts, and `n₁ ≥ 1` / `n₂ ≥ 1` at the first two shifts, are not enumerated.
- TS4's Depends for OrdinalShift: "OrdinalShift's `n ∈ ℕ` precondition is discharged at the invocation site from TS4's own precondition `n ∈ ℕ` (trivial transfer under the substitution `n = n`)". Only `n ∈ ℕ` is enumerated; `v ∈ T` and `n ≥ 1` are not named to sources.

**Issue**: TS5's OrdinalShift entry explicitly claims to follow a per-step discipline that TS5 "enforces at its TS3 and TS4 entries (where every precondition is named to a source regardless of transfer-triviality)". But TS3's and TS4's OrdinalShift entries — the cited authority for that discipline — in fact enumerate only the `n ∈ ℕ` precondition. TS5's claim that TS3 and TS4 follow this discipline at *their own OrdinalShift entries* is not borne out by the text: the trivial `v ∈ T` and `n ≥ 1` transfers are unnamed at the OrdinalShift invocation sites in both TS3 and TS4. Either TS5's appeal to precedent is mis-stated, or TS3 and TS4 are now out of step with the discipline TS5 attributes to them.

**What needs resolving**: Reconcile the discipline across the three siblings. Either tighten TS3's and TS4's OrdinalShift Depends entries to enumerate all three preconditions at each invocation site (matching what TS5 now does, and what TS5 claims TS3/TS4 already do), or weaken TS5's appeal-to-precedent wording and articulate the convention by which trivial transfers are enumerated in some Depends entries and elided in others.
