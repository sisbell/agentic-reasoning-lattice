# Channel Assignment — ASN-0047 review-47

**Date:** 2026-05-15 19:51

## Issue 1: L3 amendment weakens foundation without semantic justification
Reason: Both channels are needed — Nelson to clarify whether the design admits or forbids empty type endsets and what such a link means semantically, and Gregory to confirm the implementation behavior and any consequences (does empty Θ make the link inert, untyped, or invalid in subsequent operations?).
Nelson question: Does Xanadu's design admit links with empty type endsets, and if so, what is their intended semantics — untyped link, sentinel for default-type, or a degenerate state to be avoided?
Gregory question: Does udanax-green's link-handling code (creation, traversal, type-based queries) treat a link with empty type endset Θ identically to one with non-empty Θ, or does empty Θ change downstream behavior?

## Issue 2: K.δ precondition for nodes contradicts the analysis text
Reason: The fix is internal — the ASN's own analysis text already establishes the node/non-node distinction (NodeUniqueAllocation for nodes, T10a-conforming for non-nodes), and only the precondition statement needs restructuring to match.

## Issue 3: L-fin omitted from ExtendedReachableStateInvariants theorem
Reason: The fix is internal — L-fin is defined in ASN-0043, the inductive argument is trivial (L₀ = ∅ finite, K.λ adds one address, others hold L in frame), and parallels the existing S8-fin treatment.

## Issue 4: Missing wp analysis for content/link coupling asymmetry
Reason: The fix is internal — the ASN's own structure already shows no link-provenance invariant analogous to P4★/P7a exists, and the wp argument can be stated by appealing to the absence of such an invariant in the existing invariant set.

## Issue 5: K.μ⁻ precondition forward-references D-SEQ★ before its derivation
Reason: The fix is internal — pure structural reorganization (move the D-SEQ★ derivation before the K.μ⁻ amendment, or restate the precondition in terms of its underlying conjuncts plus a forward citation of D-SEQ★ as a derived lemma).
