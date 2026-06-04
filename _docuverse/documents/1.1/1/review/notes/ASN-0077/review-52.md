# Review of ASN-0077

This note carries `review-mode.anti-bloat`. The mathematics is largely sound — O0–O14 are carefully derived against the provided foundations, and the binary modifies-`M(d)`/leaves-`M(d)`-fixed partition in O11★★ correctly avoids a transition-vocabulary-closure assumption. The findings below are accretion patterns: duplicated prose, defensive justification, and use-site inventories that a precise reader must skip past.

## REVISE

### Issue 1: Verbatim-duplicated failure-mechanism sentence
**ASN-0077, O14 "Failure mechanism" and worked example (Σ₁ → Σ₁')**: both contain "The argument used in O11's derivation — invoking K.μ⁺'s mapping-preservation clause `M'(d)(v) = M(d)(v)` for `v ∈ dom(M(d))` — has no K.μ~ analogue, because K.μ~ permits exactly the opposite..."
**Problem**: The same sentence (mapping-preservation has no K.μ~ analogue) appears in the claim's failure mechanism and again in the worked example. Two paragraphs in the same document say the same thing.
**Required**: State the mechanism once (in O14) and let the worked example cite it, not restate it.

### Issue 2: Recurring "projection-level counterpart" asides
**ASN-0077, O13 Consequence, O14 Failure mechanism, and worked example**: "(The projection-level counterpart is LP10 (ContractionMonotonicity, ASN-0098)...)" / "(The projection-level counterpart is LP11...)" plus "The asymmetry between LP10 and O13 reflects different total/partial conventions for the operation, not different facts about K.μ⁻."
**Problem**: These asides explain the *relationship between this ASN and a foundation* rather than advancing this ASN's reasoning — meta-prose comparing conventions. The pattern recurs across O13, O14, and the worked example.
**Required**: Drop the LP10/LP11 cross-references and the convention-asymmetry sentence; they add no obligation this ASN must discharge.

### Issue 3: "load-bearing" essay content in the Summary
**ASN-0077, Summary**: "O0 is load-bearing: without the extension of `origin` to `dom(L)`... O13 and O14 are load-bearing in the opposite direction — they bound the preservation claims... so that downstream ASNs do not over-generalize O11/O11'/O11★★..."
**Problem**: Defensive justification of why each claim exists, plus a warning addressed to downstream ASNs. This is essay content in a structural slot; it does not state a guarantee.
**Required**: Remove the "load-bearing" justifications. The claims stand on their statements; the summary should restate guarantees, not argue for their necessity.

### Issue 4: Use-site inventory and labeled-claim justification in O0
**ASN-0077, "Where origin already lives" / O0**: "We make the extension a labeled claim on the same footing as S7, so subsequent uses of `origin` on `dom(L)` rest on a discharged definition rather than on prose." And: "The membership preservation for `dom(L)` that the V-span and permanence claims (O5/O5★, O7) consume is supplied directly by P3..."
**Problem**: The first sentence justifies the document-structure decision (why this is a labeled claim) rather than advancing the definition. The second enumerates downstream consumers (O5/O5★, O7) of a fact — a use-site inventory.
**Required**: Delete the labeled-claim rationale. State P3's membership-preservation fact without naming which later claims consume it.

### Issue 5: Preview paragraph restating the proof that immediately follows
**ASN-0077, paragraph preceding O11**: "The (⊆) direction parallels O6 (via K.μ⁺'s mapping preservation); the (⊇) direction requires case-analysis showing that newly-added V-positions cannot simultaneously satisfy σ's level-uniformity (C0a) and well-formedness condition (vi)."
**Problem**: This previews O11's two-direction structure one paragraph before O11 proves exactly that, in the same words. The reader reads the proof sketch twice.
**Required**: Remove the preview; O11's derivation already carries both directions.

### Issue 6: Mutual deferral between negative claims and the worked example
**ASN-0077, O13 "Witness" and O14 "Witness"**: each reads "(exhibited concretely in the worked example)", while the worked example reads "This is the canonical witness of O13" / "the canonical witness of O14 (K.μ~ non-preservation)".
**Problem**: Claim and example point at each other; the explanatory prose (mapping reassignment, admissibility loss) is then written out in both locations rather than once.
**Required**: Keep the concrete numeric witness in the worked example only; in O13/O14 assert the existential and the failure condition without re-narrating the mechanism.

## OUT_OF_SCOPE

The four Open Questions (cross-subspace I-span link origins, surfacing the intermediate transclusion chain, native-vs-transcluded distinction, historical containment from `Σ.R`) are correctly registered as future work rather than claims in this ASN — no action needed.

VERDICT: REVISE
