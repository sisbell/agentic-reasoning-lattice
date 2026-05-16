# Review of ASN-0051

## REVISE

### Issue 1: J0 compliance gap in three-span variant witness

**ASN-0051, "Three-span variant exhibiting mechanism (a)"**: "Let a₆ and a₇ be two further sibling addresses allocated past a₅ by two K.α steps (so dom(Σ.C) now contains a₆ and a₇ with a₅ + 1 = a₆ and a₆ + 1 = a₇ in the ordinal sequence at the same tumbler length), but *leave them unmapped* in d — M(d) is unchanged..."

**Problem**: J0 (AllocationRequiresPlacement, ASN-0047) requires every newly allocated content address to be placed in *some* M(d') in the post-state. The witness allocates a₆ and a₇ via K.α but explicitly says they are unmapped in d, without specifying any auxiliary placement in another document. As constructed, the composite violates J0 and is not a valid composite under ValidCompositeExtended.

This is also inconsistent with the SV10 witness's careful J0 handling, which states: "Of these three tumblers, only i₂ will be allocated by K.α in the chain below; i₁ and i₃ remain well-defined T4-valid tumblers in T but are *not* placed into dom(Σ.C). This is essential for J0 (AllocationRequiresPlacement, ASN-0047) compliance — J0 obligates placement in some M(d) *only* for newly allocated content addresses, so allocating i₁ or i₃ without also placing them via K.μ⁺ would falsify the composite against J0."

The asymmetric handling within the three-span variant compounds the issue: a₈ is correctly framed as not requiring allocation ("a₈ need not be allocated for the span to be well-formed (L4, EndsetGenerality, ASN-0043)"), but a₆ and a₇ — playing the same span-endpoint role — are framed as allocated. There is no semantic reason for the asymmetry.

**Required**: Either (a) reframe a₆ and a₇ as well-defined T4-valid tumblers not in dom(Σ.C) (consistent with the SV10 J0 discipline and with a₈'s handling in the same example — the span (a₆, a₈ ⊖ a₆) is well-formed by T12 + L4 without requiring a₆ ∈ dom(Σ.C)), or (b) explicitly construct auxiliary K.α + K.μ⁺ + K.ρ steps placing a₆ and a₇ into some other document d′ such that J0 and J1★ are satisfied for the composite. Option (a) is cleaner because the SV11 decomposition formula does not depend on the allocation status of span endpoints — only on the well-formedness of the spans and the block decomposition of M(d).

VERDICT: REVISE
