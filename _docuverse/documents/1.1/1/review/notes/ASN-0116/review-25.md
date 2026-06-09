# Review of ASN-0116

The substance is rigorous. I worked the composite-validity argument (K.α×n → K.μ⁻ → K.μ⁺ → K.ρ×n), the three-interval disjointness, the I3 transfer with block-fill, the four-part link decomposition, the P6 wp, and the worked example with both boundary cases — they hold. The findings below are the forward-reference/meta-prose accretion the anti-bloat classifier flags, plus one organizational defect that creates a genuine internal forward dependency.

## REVISE

### Issue 1: The contiguity/interval-disjointness argument is deferred from two sites and proven after a clause that depends on it
**ASN-0116, "The document remains one coherent sequence"**: "The interval computation behind that equality is the load-bearing one promised above; we give it once, in full, under *Contiguity of the filled post-state* below, after the intervening subsections establish the per-region well-formedness on which the dense-run conclusion rests."
And **same section, *Single-valuedness***: "...is disjoint from the left set... and the shifted-suffix set... — by the pairwise disjointness of the three index intervals established once under *Contiguity of the filled post-state* below."
**Problem**: Two paragraphs in the section defer to the same downstream subsection (the flagged "multiple deferrals to one location" pattern), and the deferral is not merely stylistic: the *Single-valuedness* clause uses interval disjointness that is only proven *later*, in *Contiguity of the filled post-state*. A clause should not rest on a fact established below it. The "promised above ... below, after the intervening subsections establish..." phrasing is structure-narration carrying ordering rationale, and reads as relocated-pointer content rather than a removed/reordered argument.
**Required**: State the three-interval consecutiveness-and-disjointness fact once, before any clause consumes it (it is small — it is already sketched inline in I-DOM), then cite it locally in *Single-valuedness* and *Contiguity*. Drop the "promised above / given once below / after the intervening subsections" narration.

### Issue 2: Defensive justification of clause placement in the precondition
**ASN-0116, INSERT Precondition**: "...each inserted unit is a well-formed content value, the typing obligation the K.α step below carries (ASN-0093: K.α commits `a ↦ v` only for `v ∈ Val`), discharged here at the boundary rather than left implicit in the Effect."
**Problem**: The clause `(A k : 0 ≤ k < n : w_k ∈ Val)` is self-explanatory; the trailing prose explains *why it is stated here rather than elsewhere* — a placement justification that advances no reasoning. This is the "essay content in a structural slot" pattern.
**Required**: Keep the typing conjunct and the one-clause K.α citation; delete "discharged here at the boundary rather than left implicit in the Effect."

## OUT_OF_SCOPE

### Topic 1: Insertion at a position currently shared by transclusion with another document
**Why out of scope**: The first Open Question (transclusion-shared insertion point) is correctly deferred — transclusion is ASN-0118 territory, not an INSERT obligation.

### Topic 2: Concurrent insertions without a serializing authority
**Why out of scope**: Freshness here is proven against a single reachable trace (SequentialTransitionAxiom); concurrency/serialization is a separate model concern, correctly left as an Open Question.

VERDICT: REVISE
