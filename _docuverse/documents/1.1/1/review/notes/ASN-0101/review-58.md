# Review of ASN-0101

I reviewed the operation spec (D0), the gap-closure and well-formedness proofs (D1, D8), the projection and wp characterisations (D9, D11), the three worked examples, the boundary-case enumeration, and the ValidComposite★ extension (D10). The core algebra and the per-document/per-subspace shift argument are sound, the examples compute correctly against D0/D1/D8/D9/D11, and the cross-ASN references are all to foundation ASNs. My findings concentrate on the D10 composite-boundary section, where a genuine derivation is compressed and where accreted attribution-policing prose has built up across paragraphs.

## REVISE

### Issue 1: P4★/P7a at a DEL-terminated composite boundary asserted, not derived
**ASN-0101, D10, "Multi-step composite ending in DEL"**: "What actually secures P4★ and P7a at the endpoint is the composite's coupling constraints, evaluated between Σ and Σ': J0 and J1★ force every content address allocated by an earlier step to be matched by an arrangement placement and a provenance record, **which is precisely what P4★ (Contains_C(Σ') ⊆ R') and P7a ... demand at Σ'**, given that P4★ and P7a already hold at the prior boundary Σ."

**Problem**: This is the one genuinely new obligation D10 incurs — ASN-0047's ExtendedReachableStateInvariants theorem guarantees P4★/P4a/P7a at composite boundaries only for the *pre-DEL* vocabulary, so extending the vocabulary with DEL requires re-establishing that DEL-terminated composites still yield these at the boundary. But the step from "J0 and J1★ hold" to "P4★ and P7a hold at Σ'" is asserted via "precisely what they demand," not shown. J0 ranges over `dom(C')\dom(C)`; J1★ over content-subspace range-new pairs; P4★ is `Contains_C(Σ') ⊆ R'` and P7a is per-`a` provenance coverage. The chain — prior-boundary inclusion at Σ, plus J0/J1★ on the earlier steps, plus DEL's monotone-shrinking of `Contains_C` and `R' = R` — is the actual derivation and is exactly the kind of "X follows from Y + Z" multi-step argument the standards require to be written out. As stated, a reader cannot check that J0/J1★ are *sufficient* (not merely necessary) for P4★/P7a at Σ'.

**Required**: Either (a) write the chain explicitly — name the premises (P4★/P7a at Σ, validity conditions J0/J1★, D8's monotone-shrinking/`R'=R` neutrality) and show each conjunct of P4★ and P7a at Σ'; or (b) restructure so D10 confines its own claim to DEL's neutrality (D8) and cites the foundation's boundary guarantee for the non-DEL steps, rather than presenting J0/J1★ ⟹ P4★/P7a as if derived here.

### Issue 2: Accreted attribution-policing prose in the composite-boundary section
**ASN-0101, D10**: three paragraphs ("Single-step composite," "Multi-step composite ending in DEL," "Vacuity does not extend to multi-step composites") plus the closing meta-lines: "**For this case the attribution 'by D8' is exact.**" and "Thus P4★ and P7a at Σ' are the joint product of the coupling constraints J0/J1★ and DEL's neutrality (D8), **not of D8 alone — consistent with the Vacuity does not extend to multi-step composites paragraph below.**"

**Problem**: The substantive contribution here is D8's neutrality result. The surrounding prose has accreted into commentary that polices *which paragraph's attribution is exact* and cross-references sibling paragraphs ("consistent with the ... paragraph below"). The single-step and multi-step paragraphs both re-walk the K.α/K.μ⁺/DEL coupling interaction (the multi-step paragraph abstractly, the "Vacuity" paragraph concretely), and the closing sentences add no mathematics — they adjudicate the precision of the document's own earlier attribution. This is the meta-prose pattern flagged for this note: prose a reader must work around to follow the actual claim.

**Required**: Collapse the boundary treatment to: (i) the neutrality result (D8), (ii) the single derivation Issue 1 asks for, and (iii) the one concrete counterexample showing DEL can invalidate a composite via J0. Drop the inter-paragraph attribution commentary ("the attribution 'by D8' is exact," "not of D8 alone — consistent with the paragraph below").

## OUT_OF_SCOPE

### Topic 1: Causal ordering / versioning reconstruction
**Why out of scope**: The recoverability note correctly defers full reconstruction to a versioning mechanism and the open questions; DEL's frame (D0) bounds what this ASN can claim, and the deferral is a legitimate boundary statement, not an error.

VERDICT: REVISE
