# Regional Review — ASN-0034/T4c (cycle 1)

*2026-04-23 00:52*

### T4c Injectivity cites irreflexivity where disjointness is needed
**Class**: REVISE
**Foundation**: NAT-order (NatStrictTotalOrder) — Axiom clause 4, disjointness of `<` and `=`: `(A m, n ∈ ℕ : m < n : m ≠ n)`; and irreflexivity: `¬(n < n)`
**ASN**: T4c, Injectivity paragraph: "NAT-order transitivity chains these to `0 < 1 < 2 < 3`, so `m < n` holds for every pair... ; NAT-order irreflexivity then excludes `m = n` for each such pair."
**Issue**: From `m < n`, deriving `m ≠ n` via irreflexivity alone requires substituting `m = n` into `m < n` to obtain `m < m` (or `n < n`) — i.e., substitution of equals under `<`. But T4c's own Exhaustion paragraph explicitly flags that "substitution of equals under `<` is not among NAT-order's stated properties." The two paragraphs of the same claim therefore contradict each other on what is available. The correct citation is NAT-order's disjointness clause, which directly yields `m < n ⟹ m ≠ n`.
**What needs resolving**: Replace the irreflexivity citation in Injectivity with NAT-order's disjointness-of-`<`-and-`=` axiom clause (and update T4c's Depends bullet for NAT-order correspondingly). Alternatively, if substitution-of-equals is intended to be available, state it explicitly as a property of `=` (not of NAT-order) and reconcile with the Exhaustion paragraph.

### T4c Exhaustion duplicates T4's Consequence proof verbatim
**Class**: OBSERVE
**Foundation**: n/a
**ASN**: T4c Exhaustion paragraph vs T4 Consequence paragraph — the two walk the same `m ∈ {0,1,2,3}` case analysis with the same uniform-exclusion mechanism in near-identical prose. T4 already exports `zeros(t) ∈ {0, 1, 2, 3}` as a Consequence, and T4c's Depends list cites T4.
**Issue**: T4c could cite the exported Consequence rather than re-derive it. The duplication is reviser drift: content replicated rather than referenced. The argument is correct; the issue is noise, not soundness.

### NAT-card depends on T0 only for a disambiguation aside
**Class**: OBSERVE
**Foundation**: NAT-card — Depends bullet: "T0 (CarrierSetDefinition) — supplies the tumbler-length operator `#· : T → ℕ` referenced in the disambiguation remark"
**ASN**: NAT-card, prose + Depends.
**Issue**: The NAT-card axiom body defines `|·|` on subsets of initial segments of ℕ; nothing in the axiom requires `#·`. The T0 dependency exists only to support the sentence "|·| is distinct from T0's tumbler-length `#·`." That is meta-prose in an axiom slot dragging in a non-load-bearing dependency, and it places a tumbler-specific foundation upstream of a purely arithmetic one.

### ℕ⁺ introduced in T4 prose but never used
**Class**: OBSERVE
**Foundation**: n/a
**ASN**: T4 prose: "write `ℕ⁺ = {n ∈ ℕ : 0 < n}` for the strictly positive naturals." The per-k schema in the Axiom uses `0 < Nᵢ`, `0 < Uⱼ`, etc., not `ℕ⁺`; no later paragraph references `ℕ⁺` either.
**Issue**: Unused notation. Minor noise.

VERDICT: REVISE
