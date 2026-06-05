# Review of ASN-0100

I checked the substrate decomposition, the three-region effect specification, every invariant discharge (per-state and composite-boundary), the worked examples, and the wp analysis. The mathematics is sound: the region partition is exact and exhaustive, the K.μ⁻/K.μ⁺ ordering is correctly forced, the projection-shift correspondence (INS.proj) checks numerically against the exhibited `M'(d)`, and the provenance coupling (J0/J1★/J1'★) is properly discharged. The edge cases the checklist demands — position 0 (`j=0`), append (`j=N`), empty content subspace — are all covered with the K.μ⁻-omission logic stated cleanly in (INS.μ⁻-fires). I found no correctness gap.

The findings below are anti-bloat (this note carries `review-mode.anti-bloat`): cross-section duplication of discharge work that forces the reader to re-read the same argument.

## REVISE

### Issue 1: Per-address content-invariant discharge is duplicated across two sections
**ASN-0100, §Post-state V-position well-formedness vs. §Atomicity and Canonical Order**: The fresh-`a_k` discharge of S7a, S7b, C1b, C1c (and L0's content clause, P6, P7) appears twice.

In §Post-state: "For each freshly allocated `a_k ∈ dom(C') ∖ dom(C)`: `origin(a_k) = d` discharges S7a … `zeros(a_k) = 3` discharges S7b … `#E(a_k) ≥ 2` discharges C1b … C1c … is discharged for `a_k` because `a_k` is an element of `A_C(d)` …".

In §Atomicity ("K.α and K.ρ frame M"): "The fresh `a_k` that K.α commits discharge the per-address content invariants directly: S7a, S7b, C1b, C1c (each `a_k` … `zeros(a_k) = 3`, `#E(a_k) ≥ 2`, reached by `A_C(d)`'s T10a-conforming inc-chain), P6 …, P7 and L14 …, and L0's content clause …".

**Problem**: These are the same invariants, the same `a_k`, and the same justifications. For invariants ranging over `dom(C)`, the post-state's `dom(C)` is identical to the final K.α intermediate's `dom(C)` (K.μ⁻/K.μ⁺/K.ρ frame `C`), and §Atomicity explicitly concludes that its final K.ρ intermediate "*is* the composite boundary Σ'." So §Atomicity already covers Σ' for these invariants; the §Post-state per-address paragraph re-proves what §Atomicity establishes. The reader must verify the same chain twice.
**Required**: Discharge each per-address content invariant once (it holds the moment `a_k` enters `dom(C)` and persists by P0/L12), and have the other section cite it rather than restate it.

### Issue 2: "First insertion pins m_C" is stated three times
**ASN-0100, §The Operation's Inputs, §The Operation: Formal Contract (State Preconditions), §Verifying / Sequential structure**:
- "this first insertion pins `m_C = #p` for `d` (established at the empty-case S8-depth verification in §Sequential text-subspace structure)"
- "the operation then sets `m_C := #p`, binding the third argument of `ValidFirstInsertionPosition`"
- "Pre-state `V_{s_C}(d) = ∅` imposes no depth constraint, so this first insertion fixes `m_C = m` for `d`"

**Problem**: The same fact (empty-case insertion fixes `m_C = #p`) is asserted in three sections, with the first carrying a forward reference to the third. This is the "multiple paragraphs say the same thing" pattern compounded by a forward-defer to where it is said again.
**Required**: State the `m_C := #p` binding once (at the precondition, where it belongs) and drop the restatements and the forward reference.

### Issue 3: §Background restates foundation vocabulary
**ASN-0100, §Background: The Two-Stream Asymmetry**: "The I-address is the *identity* of a piece of content; the V-position is the *current location* of that identity within an arrangement."

**Problem**: The address-vs-position identity/location distinction is already a Key Distinction in the shared vocabulary ("A tumbler address is permanent (content identity in the Istream). A position in a document is mutable (arrangement in the Vstream)"). The surrounding prose describing INSERT's asymmetric action on `C` and `M` is legitimate (it states what the operation does), but the closing identity/location paragraph re-derives settled vocabulary.
**Required**: Trim the vocabulary restatement; keep only the INSERT-specific behavioral claim (existing content keeps its I-address across the operation).

## OUT_OF_SCOPE

### Topic 1: Recovery to canonical order after partial failure during the composite
Listed as the first Open Question; the abstract spec fixes the boundary semantics and leaves implementation-level failure recovery to a future note. Correctly deferred.

### Topic 2: Concurrent INSERTs at the same V-position; INSERT composition closure
Open Questions 3–4. New territory (concurrency model, operation algebra), not defects in this note.

VERDICT: REVISE
