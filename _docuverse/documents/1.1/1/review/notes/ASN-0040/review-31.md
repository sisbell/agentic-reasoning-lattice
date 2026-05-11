# Review of ASN-0040

## REVISE

### Issue 1: B_type proof references B_fin before B_fin is established
**ASN-0040, §The baptismal registry, B_type proof Case 2**: "The maximum exists because B is finite (B_fin) and children(B, p, d) ⊆ B is a non-empty finite subset of T totally ordered by T1."
**Problem**: B_type is proved immediately after Σ.B is introduced. But its Case 2 of the inductive step depends on B_fin — which is established by an independent induction presented several sections later (after Bop, B1, B₀ conf.). The linear reading thus encounters a justification ("B is finite") that has not yet been established. The Properties Introduced table records the dependency, but the proof presentation order does not respect it. Without finiteness, max(children(B, p, d)) is not guaranteed to exist (a non-empty subset of a well-ordered set need not have a maximum unless bounded above).
**Required**: Either (a) reorder so B_fin precedes B_type, (b) restructure B_type's proof to avoid B_fin (deferring max-existence to once B1 establishes children as a finite contiguous prefix), or (c) explicitly present B_type and B_fin as a single joint induction with both invariants maintained at each transition step.

### Issue 2: Bop's correctness proof forward-references B1
**ASN-0040, §The baptism operation, Bop proof "Well-definedness"**: "If non-empty, the result is inc(max(children(Σ.B, p, d)), 0). By B1, children(Σ.B, p, d) = {c₁, ..., cₘ} for some m ≥ 1, a finite contiguous prefix, so max exists and equals cₘ."
**Problem**: Bop's proof uses B1 as a state invariant available at the precondition state. But B1's own preservation proof (in §The contiguous prefix property) uses Bop's correctness in the target-namespace sub-case. The two proofs are mutually recursive, requiring joint induction. The document does not state this explicitly — it presents Bop's correctness first, then B1's preservation, leaving the reader to reconstruct the joint structure. The same concern applies to B10's invocation in B1's non-B6 namespace sub-case.
**Required**: Either present Bop, B1, B10, and B_fin as an explicit joint induction with a single inductive step establishing all preservation claims simultaneously; or reorder so that B1, B10, B_fin are established first, with Bop's contract appealing to them as already-proved invariants at the precondition state.

### Issue 3: Misattribution in Bridge1 uniqueness proof
**ASN-0040, §The baptismal registry, Bridge1 uniqueness proof**: "By the freshness clause of Bop, next(Σ.B, p, d) ∈ S(p, d) and next(Σ.B, p', d') ∈ S(p', d')..."
**Problem**: Bop's freshness clause states `next(Σ.B, p, d) ∉ Σ.B` (the new address is not already baptized). It does not say next ∈ S(p, d). That latter fact follows from the *definition* of next (NextAddress), which returns either inc(p, d) = c₁ or inc(cₘ, 0) = c_{m+1}, both of which are stream elements by construction.
**Required**: Replace "By the freshness clause of Bop" with "By the definition of next (NextAddress)".

### Issue 4: B_type's TA5(d) citation
**ASN-0040, §The baptismal registry, B_type proof Case 2 (sub-case 1)**: "By B6(ii), d ∈ {1, 2} so d ≥ 1. TA5(d) (ASN-0034) gives `inc(p, d) ∈ T` for any p ∈ T and d ≥ 1."
**Problem**: In ASN-0034, TA5(d) is the length-increment postcondition (`#t' = #t + k` for `k > 0` with the appended-zeros/trailing-1 structure), not the membership claim. The membership `t' ∈ T` is the unlabeled first postcondition of TA5 (preceding the (a)–(d) labels).
**Required**: Cite TA5's first (unlabeled) postcondition `t' ∈ T` rather than TA5(d).

## OUT_OF_SCOPE

(None substantial — the ASN explicitly defers parent prerequisite enforcement, authorization, content storage, and the activation-discipline bridges to future ASNs with appropriately labeled forward requirements and open questions.)

VERDICT: REVISE
