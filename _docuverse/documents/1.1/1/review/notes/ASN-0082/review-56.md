# Review of ASN-0082

## REVISE

### Issue 1: Imagined excluded case in the ordinal-level discussion
**ASN-0082, "Span Width Preservation" (preamble to I3-S)**: "A width with actionPoint(ℓ) < m would change structure above the deepest ordinal: for the typical m = 2 case this changes the subspace identifier; for m > 2 it changes intermediate sub-structure within the subspace. In either case the width operates on a different axis than the shift, and the commutativity that I3-S depends on does not apply."
**Problem**: I3-S's precondition is `actionPoint(ℓ) = m`. This paragraph elaborates on what happens when `actionPoint(ℓ) < m` — a configuration the precondition already excludes. A reader following I3-S does not need the excluded-case walkthrough to verify the lemma; it is meta-prose justifying the precondition rather than advancing the claim. This is exactly the flagged "paragraph imagines a case the claim's precondition already excludes" pattern.
**Required**: Reduce to the operative statement — I3-S requires `actionPoint(ℓ) = m` (width acts at the deepest component). Drop the counterfactual analysis of the excluded case.

### Issue 2: Scoping-axiom prose explains why-needed and defers to Open Question
**ASN-0082, "Scoping axioms" (Depth axiom)**: "`#p = 2` ... restricting the analysis to single-component ordinals, where TA4's zero-prefix condition is vacuously satisfied and TA3-strict's equal-length precondition holds trivially. Whether contraction generalizes past depth 1 is the second Open Question below."
**Problem**: The axiom statement is `#p = 2`. The trailing prose explains *why* the restriction is imposed (to make TA4/TA3-strict preconditions discharge) and forward-points to the Open Question — the flagged "new prose around an axiom explains why the axiom is needed rather than what it says" plus downstream deferral. The Subspace axiom paragraph carries the same shape (link-exemption rationale + "deferred to a future ASN").
**Required**: State each scoping axiom as the constraint it imposes. The TA4/TA3-strict-precondition rationale belongs at the proof sites that consume it (D-SEP, D-BJ already cite these), not bundled onto the axiom; the Open-Question forward-pointer is redundant with the Open Questions section.

### Issue 3: Insertion "Scope." paragraph is forward-deferral essay
**ASN-0082, "Post-Insertion Shift" (Scope.)**: "The full INSERT additionally places n new content elements at the vacated gap positions [p, shift(p, n)), which entails extending dom(C) with n new I-addresses, allocating mappings for the gap positions, and re-deriving the contiguity invariants D-CTG, D-MIN, D-SEQ across the complete post-state. Content placement and the dom(C) extension are future work, belonging in a composing INSERT ASN."
**Problem**: One sentence ("this ASN characterizes the shift sub-operation, not the full INSERT") sets scope. The enumeration of what the full INSERT *would* entail is essay content describing a future ASN — it does not advance any claim in this one. The frame I3-C already states content is untouched.
**Required**: Keep the single scoping sentence. Remove the inventory of future-INSERT obligations.

## OUT_OF_SCOPE

### Topic 1: NAT-CA placement
**ASN-0082** introduces NAT-CA (commutativity/associativity of ℕ addition) as a *local* axiom, used in I3-S(a) and D-S(a). ASN-0034's NAT-* family (NAT-addcompat, NAT-closure, NAT-order, NAT-discrete, NAT-wellorder) deliberately enumerates the ℕ facts proofs may cite, but omits commutativity/associativity.
**Why out of scope**: Local introduction is defensible since the foundation genuinely lacks these facts — not an error in this ASN. But the project's per-step convention sources ℕ arithmetic from ASN-0034. Adding commutativity/associativity to the foundation's NAT-* family (then citing it here) is foundation work, not a revision to ASN-0082.

VERDICT: REVISE
