# Review of ASN-0087

I checked the composite decomposition, the precondition reduction, the wp analysis, the worked example, and the full invariant-preservation argument. The technical content is sound: the `ℓ ∉ ran(M(d))` derivation, the two-part S2 exclusion, the arbitrary-depth D-CTG★ proof, the reflexive/standard-authoring split in the wp, and the backward freshness transfer in the side-effects section all hold. The concrete example and the non-trivial wp (reflexive case) satisfy the depth requirements. All ASN references are to foundation ASNs (0034, 0036, 0043, 0047, 0093, 0098), so none violate the self-containment rule.

The remaining findings are accretion in the *What Is Indexed?* section, surfaced under the anti-bloat classifier.

## REVISE

### Issue 1: Duplicated sentence bracketing the LP12 formula
**ASN-0087, "What Is Indexed?"**: before the LP12 formula — "The function is *computed* from `Σ'.L(ℓ)` and `Σ'.M(d)` — no separate state component is required." — and immediately after it — "LP12 computes discoverability from `Σ'.L(ℓ)` and `Σ'.M(d)` alone — no separate state component participates."
**Problem**: Two sentences in the same section state the identical fact in different words, bracketing the LP12 statement. This is the "two paragraphs say the same thing in different words" pattern; the reader must notice they carry no new content.
**Required**: Delete one. The post-LP12 sentence (which then licenses M-NoIndexState) is the load-bearing one; the pre-formula restatement can go.

### Issue 2: Teaser forward-reference that does not advance reasoning
**ASN-0087, "What Is Indexed?"**: "The discovery function treats every document by the same rule; whether that uniformity yields symmetric discoverability — and where the home document's allocation of `ℓ` breaks it — is settled by the wp analysis below (M-DiscSymmetry, M-Reflexive)."
**Problem**: This sentence poses a question and defers it to a downstream section rather than establishing anything at its location — essay/teaser prose forward-pointing to the wp analysis. The wp section (Case 2, M-Reflexive, M-DiscSymmetry) already derives and states the result; this preview only adds a pointer.
**Required**: Remove the sentence. The symmetry/asymmetry distinction is fully carried by M-DiscSymmetry and the wp Case-1/Case-2 split where it is derived.

## OUT_OF_SCOPE

### Topic 1: Well-formedness of forward-reaching endsets
The first Open Question (constraints on endsets whose spans reference not-yet-allocated I-addresses) is genuinely new territory — a discipline beyond `e₃ ≠ ∅` and the optional StandardAuthoring predicate. Correctly deferred.

VERDICT: REVISE
