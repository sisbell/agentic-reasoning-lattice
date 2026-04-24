# Regional Review — ASN-0034/Span (cycle 2)

*2026-04-24 10:10*

### Speculative reference to a future "tumbler subtraction" operation
**Class**: REVISE
**Foundation**: (foundation ASN; internal)
**ASN**: Tumbler arithmetic section intro — "Its inverse — tumbler subtraction (⊖), which recovers the displacement between two positions — is a companion operation carried by a separate claim."
**Issue**: Forward reference to an operation (⊖) with no claim label or body in this ASN and no citation to a downstream ASN where the claim is expected to live. A precise reader cannot verify that such a claim exists or consume its properties; a downstream consumer cannot cite it. This is designed-but-not-presented content in the reader contract — neither framing nor a statement of what ⊕ does/does-not-do, but a promise about ⊖.
**What needs resolving**: Drop the "carried by a separate claim" clause (keep the contrast with ⊕ as framing if desired, but without forward-promising a separate claim object), or make the reference concrete by citing a specific downstream ASN/claim label once one exists.

### NAT-closure "(this ASN)" marker inconsistent across Depends lists
**Class**: REVISE
**Foundation**: (foundation ASN; internal)
**ASN**: T0 Depends: "NAT-closure (NatArithmeticClosureAndIdentity, this ASN)". T1 Depends: "NAT-closure (NatArithmeticClosureAndIdentity, this ASN)". TA-Pos, ActionPoint, TumblerAdd all cite "NAT-closure (NatArithmeticClosureAndIdentity)" without the "(this ASN)" marker. No NAT-closure body appears in the content.
**Issue**: The marker "(this ASN)" asserts the referent lives in ASN-0034; the absence of the marker in peer Depends lists — and the absence of any NAT-closure body — contradicts that assertion. Either NAT-closure is internal (then TA-Pos/ActionPoint/TumblerAdd are under-marking and the body should appear) or external (then T0 and T1 are over-marking). The same ambiguity propagates to the other NAT-* labels (NAT-order, NAT-zero, NAT-wellorder, NAT-discrete, NAT-sub, NAT-addcompat, NAT-cancel), none of which are marked "this ASN" anywhere, yet sit in the same foundation tier. A downstream consumer cannot tell which labels are ASN-0034's exports and which are inherited from a lower layer.
**What needs resolving**: Settle where NAT-* claims live and make the Depends markers uniform. If internal, add the marker uniformly and show the bodies; if external, strip "(this ASN)" from T0 and T1.

VERDICT: REVISE
