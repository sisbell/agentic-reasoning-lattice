# Review of ASN-0077

## REVISE

### Issue 1: O0(c) totality argument has incomplete citation for the dom(C) case

**ASN-0077, O0 derivation conjunct (c)**: "(for x ∈ dom(C), by S7 of ASN-0036; for x ∈ dom(L), by K.λ's precondition d ∈ E_doc together with P1 (EntityPermanence, ASN-0047), which keeps d in E_doc at every subsequent reachable state)."

**Problem**: The claim being discharged is `origin(x) ∈ E_doc` *at the current state*. For the dom(C) case, the text cites only S7 of ASN-0036, but S7's postcondition (b) establishes only "origin(a) is the tumbler of the document that allocated a" — it does not state that this document is currently in E_doc. (S7's invariance clause (d) speaks about origin(a) being invariant, not about E_doc membership.) The dom(L) case correctly chains K.λ's allocation-time precondition `d ∈ E_doc` with P1 (entity permanence) to bridge this gap. The dom(C) case requires the analogous chain — K.α's precondition `d ∈ E_doc` at the allocation event (ASN-0047), plus P1 to propagate that membership through every subsequent reachable state. Without explicitly citing K.α + P1, the conjunct "origin(x) ∈ E_doc" for x ∈ dom(C) is asserted from S7 alone, which underdetermines the conclusion.

**Required**: Make the dom(C) chain symmetric to the dom(L) chain. Replace "for x ∈ dom(C), by S7 of ASN-0036" with "for x ∈ dom(C), by K.α's precondition `d ∈ E_doc` (ASN-0047) at the allocation event together with P1 (EntityPermanence, ASN-0047)". Closure that every x ∈ dom(C) arose through some K.α event follows from the same enumeration argument used for dom(L) (K.α is the only ASN-0047 transition whose effect clause names C); since this closure step is already implicit in the dom(C) reasoning, it should be made explicit alongside K.α + P1.

VERDICT: REVISE
