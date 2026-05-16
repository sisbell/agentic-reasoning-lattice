# Review of ASN-0051

## REVISE

### Issue 1: K.ρ omission in J1★-required witness composites

**ASN-0051, SV10 main witness construction and SV10 Corollary (CrossDocumentDecoupling)**

Two places describe composite chains that include K.μ⁺ extending M(d) with a new content-subspace mapping but omit the K.ρ step required to satisfy J1★.

*Main witness:* "The state Σ.M(d) = {v₁ ↦ i₂} is reachable from a state where V_{s_C}(d) = ∅ by a single K.μ⁺ step seeding the content subspace at depth 2..."

*Corollary, Step 3:* "K.μ⁺ places v₁ ↦ j in M(d₂)." The chain ends after Step 3.

**Problem:** Per ValidCompositeExtended (ASN-0047), a composite must satisfy J1★ between initial and final states. J1★ requires that any new content-subspace mapping `v ↦ a` in M'(d) (where no such mapping existed in M(d)) be coupled with `(a, d) ∈ R'`. The K.μ⁺ steps in both witnesses add fresh content-subspace mappings to newly allocated addresses (i₂ in the main witness, j in the corollary); without K.ρ, R' = R and the required provenance records are missing. The composite as written is invalid, so the witness states aren't reachable as described.

**Note that SV7's TransclusionCouplingAbsence corollary explicitly acknowledges this requirement** in its parenthetical: "A valid composite transition containing K.μ⁺ may additionally require K.ρ to satisfy J1★...". The SV10 witnesses should apply the same acknowledgment for consistency.

**Required:** Either add K.ρ explicitly (as Step 4 in the corollary chain; as part of a K.μ⁺ + K.ρ composite in the main witness) or add an SV7-style parenthetical noting the K.ρ requirement. The existential claims remain witnessed with the corrected composite.

### Issue 2: SV6 worked example silently uses non-conforming s_8

**ASN-0051, "Cross-origin exclusion (SV6)" worked example**

The example takes s = 1.0.1.0.1.0.1.2.3 and concludes "zeros(s) = 3 at positions 2, 4, 6. ✓" and uses this s as the span start address. But s_7 = 1 and s_8 = 2 mean the element field of s is E(s) = [1, 2, 3]. The example never verifies that s_8 = 2 satisfies fields(s).E₁ = s_C — i.e., it never declares whether this s is meant to be a stored I-address (in which case the K.α amendment fixes E(s)_1, the *first* element-field component, to s_C, not s_2 = 2 = some second component). The leading 1 *is* the first element-field component, so the example is consistent if s_C = 1, but the example never says so.

**Problem:** The example uses concrete tumbler values but doesn't anchor them against the subspace conventions used elsewhere (where the SV10 witness explicitly states "Fix the content subspace identifier s_C = 1"). A reader trying to verify the example against the K.α amendment cannot tell whether s is supposed to be a content address, a link address, or just a structural witness for SV6's purely structural claim. SV6 itself does not require any subspace condition (it's about origins and field separators only), so the example is logically correct — but the absence of a subspace declaration is a clarity gap.

**Required:** Add a one-line note explaining that SV6 is a structural claim independent of subspace, and that the example's s and b are taken as element-level T4-valid tumblers without commitment to s_C/s_L. Alternatively, declare s_C = 1 and verify the example as a content-side witness.

### Issue 3: SV10 main witness elides multi-step reachability from Σ₀

**ASN-0051, SV10, witness construction**

The witness describes the state Σ with i₁, i₂, i₃ ∈ dom(C), link a ∈ dom(L) with F = {(i₁, ℓ_span)}, and M(d) = {v₁ ↦ i₂}. The text gestures at reachability via "a single K.μ⁺ step seeding the content subspace at depth 2 with this minimum position."

**Problem:** This is misleading. Reaching Σ from Σ₀ requires: K.δ for the node at 1, K.δ for account 1.0.1, K.δ for document d, three K.α steps for i₁/i₂/i₃, K.μ⁺ + K.ρ for placement of i₂ in M(d), then K.δ for the document hosting link a (or specification that d hosts it), then K.λ for the link. The "single K.μ⁺ step" wording obscures these. While each step is unproblematic individually, leaving them implicit makes the witness less directly checkable.

**Required:** Either trace the full reachability chain (verbose but explicit), or replace "by a single K.μ⁺ step" with "by a standard composite chain (allocation of node, account, document, content addresses, then K.μ⁺ + K.ρ placement of i₂, then K.λ creating a)" so the reader knows what's being assumed.

### Issue 4: SV13(e) "M-frame transitions" listing is potentially misleading

**ASN-0051, SV13(e), 5th bullet:** "K.α, K.δ, K.ρ, and K.λ all preserve M in their frame, so locate(e, d) is unchanged for every endset e that existed prior to the transition."

**Problem:** For K.δ that creates a *new* document d_new, M(d_new) goes from "undefined" to "= ∅". This is not strictly "M unchanged" — a new key enters the function family M. The statement about "locate(e, d) is unchanged for every endset e that existed prior to the transition" is correct for pre-existing d, but for the new d_new, locate(e, d_new) was not defined pre-transition and is now ∅. The bullet doesn't address this nuance.

**Required:** Add a clarifying clause: "K.α, K.δ, K.ρ, and K.λ preserve M for all pre-existing documents in their frame; K.δ additionally introduces M(d_new) = ∅ for a freshly created d_new, in which case locate(e, d_new) = ∅ for every endset e."

### Issue 5: Same-origin coverage growth — counterexample missing tumbler-level verification

**ASN-0051, "Counterexample to a universal exclusion claim" within the same-origin discussion**

The counterexample claims that if a₁ < a₂ < ... < aₙ are sequential allocations and a span (a₁, ℓ) has reach a₁ ⊕ ℓ = aₙ + 1, then a child-depth c = inc(aₙ, 1) satisfies aₙ < c < aₙ + 1 and so c ∈ ⟦(a₁, ℓ)⟧.

**Problem:** The proof sketch ("c < aₙ + 1" because "c diverges from aₙ + 1 at the position where c has a smaller value") is asserted without showing the divergence position. For aₙ that ends in nonzero component, aₙ + 1 increments the last component. c = inc(aₙ, 1) appends a 1 to aₙ (by TA5(d)). To verify c < aₙ + 1: both share aₙ's first #aₙ components, but at position #aₙ, c_{#aₙ} = aₙ_{#aₙ} while (aₙ + 1)_{#aₙ} = aₙ_{#aₙ} + 1, so the first divergence is at position #aₙ where c has the smaller value, giving c < aₙ + 1 by T1(i). This should be made explicit.

**Required:** Add the divergence-position argument explicitly, similar to the level of detail in SV6's worked example. The current sketch is correct but underspecified for a passage that grounds an architectural distinction.

## OUT_OF_SCOPE

(none — the ASN's existing scope exclusions cover link type semantics, replication, broader-level spans, link-subspace projection details, same-origin coverage growth formal treatment, and fork survivability adequately)

VERDICT: REVISE
