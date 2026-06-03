# Review of ASN-0098

I checked the projection definition, the immutability lemmas (LP2–LP3, LP13), the frame conditions (LP4–LP8), the per-operation displacement results (LP9–LP11), the discoverability characterisation and wp (LP12, LP12a, LP12b), the finitude machinery (LP-Sub, LP-Fin, LP-Fin Corollary), the tightness results (LP19a, LP19), range confinement (LP20), and the worked trace. The mathematics is sound: I re-derived LP-Fin's count (= n) against concrete sub-cases, verified the K.μ~ bijection arithmetic in both trace branches, and confirmed the LP20 partition is genuine via store disjointness. No correctness defects found.

The findings below are anti-bloat: accreted meta-prose and English restatements that the precise reader must read past.

## REVISE

### Issue 1: LP3 proof closes with a redundant English restatement
**ASN-0098, LP3 (CoverageInvariance)**: "The set of I-addresses the link refers to is computed from its endsets; if the endsets are byte-identical between states, the coverage is identical between states."
**Problem**: The preceding sentence already discharges LP3 formally ("`Σ'.L(a).eᵢ = Σ.L(a).eᵢ` from which the coverage equation follows by applying `coverage` to both sides"). The quoted sentence re-says exactly this in prose and advances no reasoning.
**Required**: Delete the trailing sentence.

### Issue 2: Roadmap meta-prose at the projection definition duplicates LP4
**ASN-0098, "The Projection Operation"**: "Of these two inputs, `coverage(e)` is endset-fixed (immune to transitions, by L12) and only `Σ.M(d)` varies; we therefore characterise projection displacement by examining what each editing operation does to `Σ.M(d)`."
And **"Immutability of the Stored Link"** opener: "Before we can reason about how projection displaces, we must pin down what does *not* move."
**Problem**: Both are roadmap sentences describing the document's plan rather than advancing a claim. The "two inputs" observation is then restated a third time as load-bearing content inside LP4's proof ("The projection function depends on exactly two inputs: `coverage(e)` and `Σ.M(d)`"). The same fact appears in three places; only the LP4 occurrence does work.
**Required**: Drop the two roadmap sentences; let LP4's proof carry the "two inputs" fact at its point of use.

### Issue 3: Closing tightness paragraph restates the worked numerical contrast
**ASN-0098, after LP19**: "Tightness is a construction discipline, not a structural invariant the system enforces. The system permits endsets whose spans extend past the relevant sub-allocator's current emission frontier; such endsets are not tight, and an `a_new` allocated within their forward extent ... would in fact enter the coverage — LP9's growth behaviour then applies."
**Problem**: The immediately preceding "Non-tight contrast" worked example (`ℓ' = δ(4, m)`, `a_new = [d.0.1.4]` entering coverage, LP9 growth) already exhibits exactly this, concretely. The paragraph re-states the example's conclusion in conceptual prose.
**Required**: Keep one sentence stating tightness is a construction discipline the system does not enforce; drop the re-derivation of the non-tight case already shown in the worked example.

## OUT_OF_SCOPE

The Open Questions (reverse-discovery, V-order reflection, contiguity-as-finite-union under K.μ~, link-to-link induced discovery, cross-document determinism, fork non-transclusion, link-canonical contraction) are correctly parked as future work and not claimed here. No action.

VERDICT: REVISE
