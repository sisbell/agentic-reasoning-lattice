# Channel Assignment — ASN-0077 review-3

**Date:** 2026-05-25 15:35

## Issue 1: Extension of origin to dom(L) is informal
Reason: The fix is derivable from existing foundation ASNs — L1b (ASN-0047) supplies structural well-definedness of the projection on dom(L), and K.λ's precondition (ASN-0047) supplies the semantic correspondence to home document. Both are already in the formal substrate; the task is to assemble them into a labeled definition.

## Issue 2: O2 link case omits the subspace justification for CL-OWN
Reason: Pure citation bridge — M-sub(a) of ASN-0058 (subspace preserved under shift given #v ≥ 2) and S8a of ASN-0036 (depth lower bound). Both lemmas are already established; the fix is to thread them into the existing derivation.

## Issue 3: (F2) ≡ (F3) cites a content-only lemma to discharge a step that includes the link case
Reason: Internal citation correction — O2 (just derived in this ASN) is the right authority for the collapse across both subspaces; M16a is content-only and was mis-cited. No external information needed.

## Issue 4: "resolve" is invoked on link-subspace V-spans, but ASN-0058's resolve targets dom(C)
Reason: The simpler fix — rephrasing prose to invoke C1a's block decomposition (subspace-agnostic) directly without naming `resolve` — is internal and matches the derivations already in place. CL-OWN already establishes link arrangements as first-class structure.

## Issue 5: Singleton I-span argument omits the #b < #a case
Reason: The missing case is ruled out by T1 (ASN-0034) — a proper-prefix `b` of `a` gives `b < a`, contradicting `a ≤ b ∈ ⟦σ_a⟧`. Purely internal proof completion.
