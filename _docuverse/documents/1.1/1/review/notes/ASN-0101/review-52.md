# Review of ASN-0101

I checked the operation specification (D0), the gap-closure bijection (D1), the preservation claims (D2–D8), the projection characterisation (D9), the ValidComposite★ extension (D10), and the weakest-precondition calculations (D11), together with the three worked examples and the boundary-case enumeration. The proof content is genuinely thorough: D8's three-group partition accounts for every per-state invariant in ASN-0047's ExtendedReachableStateInvariants list, the S8★ condition-(c) discharge correctly refuses the singleton decomposition as a uniqueness witness and routes through M12, the "justification of the reduction" handles `m_S = 2` vacuously and `m_S ≥ 3` by least-divergence-position, and D10 correctly shows vacuity does *not* lift to multi-step composites with a concrete J0-breaking counterexample. I found no skipped proof step or missing edge case.

The note carries the `review-mode.anti-bloat` classifier; the remaining findings are residual accretion plus one notation gap.

## REVISE

### Issue 1: Projection-picture preamble duplicates D9
**ASN-0101, "Link discoverability: the projection picture"**: the three bullets ("Projection into `d`'s shifted subspace ... two contributions ... Positions in `X` ... are removed", "Projection into `d`'s other subspace. Unchanged, by D6", "Projection into any other document `d'`. Unchanged, by D5") are immediately followed by "We extract this as an abstract characterisation: **D9**", whose three clauses state the same three cases formally.
**Problem**: The informal bullets advance no reasoning that D9 does not formalise two lines later; they are the same three cases in different words. This is the "two paragraphs say the same thing" pattern.
**Required**: Drop the bullet preamble and lead directly with D9, or keep a single motivating sentence rather than a parallel three-way restatement.

### Issue 2: D3 closing paragraph restates the content/link parallel without new content
**ASN-0101, D3 section, final paragraph**: "DELETE establishes a pattern of *structural persistence with conditional visibility* ... It is the same pattern by which content survives deletion: the bytes persist in `C` ... The link case is the natural extension of the content case to the second store."
**Problem**: The substantive reasoning (endsets carry I-addresses not positions; coverage is state-independent; coverage is preserved under D3) is already given in the two preceding paragraphs. This paragraph only asserts that the link case parallels the content case — a restatement, not a step.
**Required**: Remove the paragraph; the parallel is self-evident once D2 and D3 are both stated.

### Issue 3: `V_S(·)` overloaded onto arrangements without definition
**ASN-0101, "The setting"**: `V_S(d) := {v ∈ dom(M(d)) : subspace(v) = S}` is defined as a function of a *document* `d` (reading `M(d)`). From D0 onward the note writes `V_S(M'(d))`, `V_{S'}(M'(d))`, applying `V_S` to an *arrangement* rather than a document.
**Problem**: `V_S` applied to an arrangement is never defined. The intended meaning (`{v ∈ dom(M'(d)) : subspace(v) = S}`) is inferable, but the note is otherwise meticulous about notation (e.g., the explicit `ℓ_σ` vs `ℓ` convention), so the silent overload is a gap a precise reader must patch.
**Required**: Either define `V_S(N) := {v ∈ dom(N) : subspace(v) = S}` for an arrangement `N` once, or write `{v ∈ dom(M'(d)) : subspace(v) = S}` explicitly at the post-state use sites.

### Issue 4: D2 "cardinality consequence" over-reaches past DELETE
**ASN-0101, D2 section**: "Combined with the cardinality non-decrease across allocation (K.α), the content store is monotonically non-decreasing across the entire transition vocabulary."
**Problem**: This asserts a property of operations other than DELETE (K.α and the rest of the vocabulary), which is not this ASN's to establish. DELETE's contribution is the strict equality `dom(C') = dom(C)`; the cross-vocabulary monotonicity claim belongs to whatever ASN owns those transitions.
**Required**: Trim the sentence to DELETE's own consequence (`|dom(C)|` unchanged under DEL), or drop the vocabulary-wide assertion.

## OUT_OF_SCOPE

### Topic 1: Recoverability / versioning section
**Why out of scope**: The "A note on recoverability and historical reconstruction" section is careful to say versioning "is out of scope here," and its load-bearing content (D2 + D5 make reconstruction possible) is already captured by the D2 "Prior versions of `d` can be reconstructed" bullet. It is not an error in this ASN, but it is the natural seam for a future version-mechanism ASN, and the section largely re-derives the D2 bullet at length. Not flagged as REVISE, but consider compressing to a back-reference.

VERDICT: REVISE
