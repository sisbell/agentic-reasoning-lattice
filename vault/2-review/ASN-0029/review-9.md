# Review of ASN-0029

## REVISE

### Issue 1: T10 incorrectly cited for between-allocator uniqueness

**ASN-0029, Address Allocation (D1)**: "Per-account uniqueness is guaranteed by T10 (PartitionIndependence): different allocators operate in non-nesting prefix domains, so their outputs are always distinct."

**Problem**: The root allocator for account `a = N.0.U` has ownership prefix `a`. A child allocator for document `a.0.D₁` has ownership prefix `a.0.D₁`. Since `a ≼ a.0.D₁`, these prefixes nest — T10 requires `p₁ ⋠ p₂ ∧ p₂ ⋠ p₁`, which fails. The universal claim "different allocators operate in non-nesting prefix domains" is false for every root-vs-child pair under the same account.

**Required**: Split the between-allocator argument:
- Between child allocators with distinct parents (e.g., `a.0.3` vs `a.0.5`): T10 applies — prefixes are non-nesting. Correct as-is.
- Between root allocator and any child allocator: uniqueness follows from structural length difference. Root allocator outputs have single-component document fields (`#doc = 1`); child allocator outputs have multi-component document fields (`#doc ≥ 2`). Different tumbler lengths give distinctness by T3 (CanonicalRepresentation).

### Issue 2: Worked examples skip allocation values without explanation

**ASN-0029, D0 worked example**: "The root allocator's current maximum is 3; D0 produces d = 1.0.1.0.5 via inc(·, 0)"

**ASN-0029, D12 Case 2 worked example**: "Suppose 2.0.1 already has root document 2.0.1.0.2 ... the root allocator produces d_v = 2.0.1.0.4"

**Problem**: TA5(c) defines `inc(t, 0)` as incrementing position `sig(t)` by exactly 1. From max 3, the next allocation is 4; from max 2, the next is 3. The Address Allocation section confirms: "walks the existing address structure ... to find the current maximum, then returns max+1." Both examples skip a value with no explanation, contradicting the stated mechanism.

**Required**: Use consistent values (3→4 and 2→3), or explain the gap (which would require acknowledging intermediate allocations and listing them in the pre-state).

### Issue 3: P3 preservation for new document in D12 not verified

**ASN-0029, Preservation of ASN-0026 Invariants**: "For existing documents, all four operations preserve V-space in their frames, so P2, P3, and P7 carry forward from the pre-state."

**Problem**: P2 for the new document `d_v` in D12 is explicitly verified in the preceding sentence. P3 for `d_v` is not — the "existing documents" sentence does not cover it. The verification is one step: `Σ'.I(Σ'.V(d_v)(p)) = Σ'.I(Σ.V(d_s)(p))` by D12(c), `= Σ.I(Σ.V(d_s)(p))` by D12(e), which satisfies P3 by P3 on Σ. But it should be shown rather than subsumed under "existing documents."

**Required**: Add a sentence for P3 on `d_v`, parallel to the P2 sentence.

### Issue 4: Summary overstates address-purity of ancestry

**ASN-0029, Summary of State**: "these encodings are pure functions of the address value, all of them are permanent — no mutable state is consulted, so no state transition can alter them"

**Problem**: The ≺ relation (D14) is address-intrinsic. But `parent(d) = max≼ {d' ∈ Σ.D : d' ≺ d}` consults `Σ.D`, which is mutable. The claim "no mutable state is consulted" is false for parent. Parent stability holds by a different argument: D2 ensures `Σ.D` only grows, and D12 Case 1 allocates children one level below the source via `inc(d_s, 1)`, leaving no tumbler in the prefix order between parent and child for future allocations to interpose. This is a D2 + allocation-structure argument, not an address-purity argument.

**Required**: Distinguish the ≺ relation (address-intrinsic) from the parent function (Σ.D-dependent). State the parent-stability argument: once `parent(d) = d_s` at creation, no future document can interpose between `d_s` and `d` in the prefix order, so `parent(d)` is invariant across all subsequent states.

## OUT_OF_SCOPE

The ASN's Open Questions are well-chosen and comprehensive. No additional out-of-scope topics identified.

VERDICT: REVISE
