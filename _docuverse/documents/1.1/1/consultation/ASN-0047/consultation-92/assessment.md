# Channel Assignment — ASN-0047 review-92

**Date:** 2026-05-17 22:26

## Issue 1: J4 derivation incorrectly claims `ran(M(d_src)) ⊆ dom(C)`
Reason: Pure internal logical error. S3★'s content clause (already in the ASN) only gives `ran(M(d_src)|_{V_{s_C}(d_src)}) ⊆ dom(C)`; the fix is to restrict the chain to the content-subspace projection using definitions already established.

## Issue 2: K.μ~ link-subspace fixity step (4) cites CL-UNIQ at Σ' as if established
Reason: Inductive logical flow error. The fix is to invoke CL-UNIQ at Σ (the inductive hypothesis) combined with step (3)'s pointwise equality `M'(d)|_{dom_L} = M(d)|_{dom_L}`, which is derivable from the proof's own prior steps.

## Issue 3: J2 and J3 statements omit L' = L
Reason: Editorial synchronization with the Frame extension paragraph already in the ASN. The amendment is purely textual — the L' = L conjunct is already established by the Frame extension that follows.

## Issue 4: "Why S7d★ rather than S7d" meta-prose
Reason: Anti-bloat trim of meta-rationale. No design intent or implementation detail is at stake — only deletion of explanatory prose surrounding an already-stated invariant.

## Issue 5: NodeAllocationRegistry definition contains essay content
Reason: Editorial trim of essay content from a definitional slot. The definition's core content is already present; the Nelson/Gregory citations are surrounding rationale that can be removed or moved to design notes.

## Issue 6: Link-withdrawal gap content spread across four sections
Reason: Editorial consolidation; the canonical statement already exists in the dedicated paragraph and the other three sites can be reduced to pointers without changing semantic content.

## Issue 7: Worked examples violate the invariant verification convention
Reason: Internal consistency choice between two stated alternatives (remove P3★ lines or amend the convention). Either option is editorial and self-contained within the ASN.

## Issue 8: "Justification for uniform contiguity" paragraph is design rationale
Reason: Editorial condensation; the trade-off statement and L12-mitigation summary can be derived from the D-CTG★/D-MIN★ definitions and L12 (LinkImmutability) already in the ASN. The Nelson/Gregory references in the paragraph are explanatory backing rather than load-bearing claims.

## Issue 9: "Reading" footnote on D-CTG★
Reason: Editorial trim; the clarifications are restatements of S8-depth and S8a properties already in the ASN's notation/foundation blocks, so no external content is needed to remove or inline them.

## Issue 10: K.μ⁻ exhaustiveness lemma's case (b) precondition is too restrictive
Reason: Internal proof-hygiene issue. The partition algorithm's routing is already correct as written; the fix is to add an explicit note that any non-suffix K' with `1 ∈ K'` exhibits an interior hole reachable by the k_min/k_max construction — derivable from the proof's own structure.

## Issue 11: NodeAllocationRegistry and SubAllocatorAxiom asymmetric stratification
Reason: The discharge table consolidates information already distributed across K.δ, K.α, K.λ, and the Foundation invariants block. The structural asymmetry (nodes have no parent allocator at zeros = 0, so T10a's parent-chain discipline does not apply) is derivable from the foundation ASNs already cited.

## Issue 12: Convention-dependent chain in L1c discharge
Reason: Internal consistency issue. SubspaceConventionAxiom is globally fixed in the ASN, so the convention-dependence qualifiers are dead weight under the ASN's own axiomatization. The fix is to commit fully to the convention, derivable from the existing axiom statement.
