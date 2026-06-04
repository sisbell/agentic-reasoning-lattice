# Review of ASN-0077

This ASN has clearly been through many cycles and its proofs are largely sound. My findings are concentrated where the note carries its own `review-mode.anti-bloat` / forward-reference-accretion classifier: redundant prose and duplicated derivations that the precise reader must skip past. I found no incorrect proof.

## REVISE

### Issue 1: Duplicate link-subspace V-span paragraph
**ASN-0077, "Lifting origin to a V-span" and edge case "V-span over link subspace"**: The first reads "When `u₁ = s_L`, the V-span lies in `d`'s link subspace. By S3★... by CL-OWN..., `origin(M(d)(v)) = d`... reduces to `{d}`..."; the second reads "When `u₁ = s_L`, the V-span lies in `d`'s link subspace. By S3★... by CL-OWN..., `origin(M(d)(v)) = d`. So `origins_V(Σ, d, σ) = {d}`..."
**Problem**: Two paragraphs in different sections state the same claim with the same S3★+CL-OWN derivation. One is noise.
**Required**: Keep the link-subspace result in one location (the edge-case slot, since it documents an operational corner) and delete the duplicate.

### Issue 2: O4 restates itself in "calculational form"
**ASN-0077, Claim O4**: After the derivation, "The same point in calculational form. Let `f_{Mᵢ} = origin ∘ M(dᵢ)`. Then for every `i`: `f_{Mᵢ}(vᵢ) = origin(M(dᵢ)(vᵢ)) = origin(a) = d₁`..."
**Problem**: This paragraph re-expresses the just-proved equality in different notation, advancing no new reasoning ("two paragraphs say the same thing in different words"). The preceding "The substantive claim is therefore not that origin is computable from `a` alone — that was already O3 — but that..." is also a meta-paragraph relitigating the boundary with O3.
**Required**: Delete the calculational restatement; fold any genuinely new content of the O3-boundary paragraph into a single sentence or remove it.

### Issue 3: Open Question 1 deferred twice
**ASN-0077, edge case "Cross-subspace I-span" and Summary item (2)**: "(Reporting link origins from an I-span is left as Open Question 1...)" and "(The I-span lift restricts to content by definitional choice; the link-subspace case is left as Open Question 1.)"
**Problem**: Two paragraphs defer the same gap to the same downstream location — the compounding forward-reference pattern the classifier targets.
**Required**: Keep the deferral at the point where the definitional choice is made (the I-span lift definition or its edge case); drop the Summary repetition.

### Issue 4: Defensive proof-method prose in O0(c)
**ASN-0077, Claim O0 derivation (c)**: "Each case is discharged by a foundation invariant directly, with no transition-vocabulary enumeration."
**Problem**: This justifies *how* the proof proceeds (and what it avoids) rather than advancing the derivation — a defensive justification the reader skips.
**Required**: Remove the sentence; the per-case citations of P6 and L1a already carry the argument.

## OUT_OF_SCOPE

None. The open questions on cross-subspace I-span reporting, intermediate-chain surfacing, native-vs-transcluded distinction, and historical containment are correctly deferred rather than half-specified here.

VERDICT: REVISE
