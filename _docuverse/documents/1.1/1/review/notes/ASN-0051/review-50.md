# Review of ASN-0051

I traced each survivability claim against its proof, verified the explicit witnesses (SV10's chain, CrossDocumentDecoupling's K.δ + K.α + K.μ⁺ extension, SV11's two-span and three-span variants, SV14(d)'s K.μ⁻ shrinkage, the Worked Example's K.μ~+K.μ⁻ composite), and checked SV6's structural argument component-by-component. The proofs are detailed, the witnesses arithmetically explicit, and edge cases (empty endsets, empty arrangements, within-document sharing under S5, the K.δ caveat for newly seeded M(d_new), the K.μ~ intermediate-state composite-scope) are handled. The withdrawn labels SV0/SV1/SV12 are documented. I found one substantive error.

## REVISE

### Issue 1: T12's preconditions misstated in the three-span variant

**ASN-0051, Worked Example → "Three-span variant exhibiting mechanism (a)"**: "T12 (SpanWellDefinedness, ASN-0034) requires only T4-validity of the start and reach tumblers, both of which hold by construction"

**Problem**: T12's actual preconditions (ASN-0034) are `s ∈ T`, `ℓ ∈ T`, `Pos(ℓ)`, `actionPoint(ℓ) ≤ #s`. T4-validity is *not* among them. The note inverts the relationship — it asserts T12 *requires* T4-validity, when in fact T12 doesn't require T4-validity at all. T4-validity matters in this ASN where `origin()` must be evaluated (e.g., SV6); for the span `(a₆, a₈ ⊖ a₆)` in the three-span variant, the variant computes only decomposition terms, so `origin()` isn't invoked and T4-validity is irrelevant to the span's well-formedness.

**Required**: Replace the T12 citation with the four actual preconditions: `a₆ ∈ T` and `a₈ ⊖ a₆ ∈ T` (by TA2, since a₆ ≤ a₈ as same-length siblings); `Pos(a₈ ⊖ a₆)` (the difference at position #a₆ is 2 > 0); `actionPoint(a₈ ⊖ a₆) ≤ #a₆` (they diverge at the last component, so action point equals #a₆). Drop the appeal to T4-validity here, or relocate it to a context where `origin()` is actually being computed.

## OUT_OF_SCOPE

None worth flagging — the ASN's Open Questions section identifies the deferred topics (within-document sharing semantics, link revival, fragment ordering, fork-time bilateral vitality, etc.), and the explicit scope notes (cross-origin exclusion at element-level only, broader-level spans deferred to ASN-0034, link-subspace projection deferred to a future Link Subspace ASN) are appropriately bounded.

VERDICT: REVISE
