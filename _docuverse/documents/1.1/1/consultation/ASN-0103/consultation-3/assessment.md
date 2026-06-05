# Channel Assignment — ASN-0103 review-3

**Date:** 2026-06-05 00:14

## Issue 1: Ownership conclusion rests on an unjustified registry extension
Reason: The ASN's state model `(C,L,E,M,R)` has no `B` component, so the entity→registry coupling cannot be derived internally; deciding whether a document-creation `K.δ` is intended to be a baptism that extends the ownership registry is a design-intent question for Nelson. Gregory is not needed — the gap is about intended formal semantics, not what the code does.
Nelson question: Is creating a document intended to be a baptismal act that necessarily registers the new address in the ownership registry (establishing the creating account as owner at the instant of creation), such that entity allocation and registry extension are coextensive?

## Issue 2: Blanket invariant claim outruns what is verified
Reason: The review itself supplies the full conjunct list (from the already-cited ASN-0047 theorem) and the discharge pattern — vacuous for `d` via `dom(M'(d))=∅`, frame-inherited for `d'≠d` via `C'=C ∧ L'=L ∧ R'=R ∧ M'(d')=M(d')`. Every premise needed is already present in the ASN's own post-state, so the fix is purely mechanical enumeration.
