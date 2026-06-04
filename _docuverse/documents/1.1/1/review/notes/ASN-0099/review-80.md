# Review of ASN-0099

I reviewed the FINDLINKS specification for correctness, boundary coverage, and (per the anti-bloat classifier on this note) accreted meta-prose. The core argument is sound: the two-phase factoring (F12), the match predicate (F1), the preservation story (F9/F9-λ/F11/F19), and the worked example (Queries 1–6) are rigorous, with boundary cases (empty `I`, empty `dom(Σ.L)`, `d ∉ dom(Σ.M)`, empty constraint set, empty scope) handled explicitly. The V-side non-preservation under K.μ⁻ is demonstrated concretely in Query 5 rather than hand-waved. No correctness defect found.

The findings below are prose/bloat items the precise reader must work around.

## REVISE

### Issue 1: "Claims Introduced" table cells carry derivation prose, duplicating the body
**ASN-0099, "Claims Introduced" table**: The `A1a` cell reads "atomic ops publish `L' = L` (K.μ⁺, K.μ⁻ via ASN-0047's amended extended-state frames), and K.μ~ by transitive composition" — a verbatim re-proof of A1a's own body text. Other cells embed rationale/contrast rather than statements: `F11` ("distinct from ASN-0098's V-side discoverable_from, which is not persistent"), `F9` ("single-step or multi-step"), `F2★/F3★` ("the V form is the primary obligation on result_V").

**Problem**: The table's `Status` column establishes it as a terse index. Packing the A1a composition proof and the F11 contrast into table cells duplicates content the body already carries, and is exactly the "essay content in a structural slot" pattern that compounds across cycles.

**Required**: Reduce each cell to a one-line statement of what the claim asserts; move proof sketches and cross-ASN contrasts back to the body (where they already appear for A1a and F11).

### Issue 2: V-side asymmetry stated twice with a downstream deferral
**ASN-0099, after F11 and after F19**: After F11 — "the V-side analogue ... is not a theorem of this ASN and could not be, since K.μ⁻ can shrink ran(Σ.M(d)) (Query 5 below exhibits the divergence concretely)." After F19 — "The V-side asymmetry noted at F11 applies equally here."

**Problem**: The same observation is asserted in two sections, the F19 sentence adding only a back-pointer, and the F11 instance forward-references "Query 5 below." This is the "multiple paragraphs defer to the same downstream location" / "say the same thing in different words" pattern.

**Required**: State the V-side asymmetry once (it governs both F11 and F19), and let Query 5 carry the concrete divergence without the prose pre-announcement.

### Issue 3: F1 follow-on paragraph restates the formal predicate
**ASN-0099, "The Match Predicate"**: After F1's formal definition, the paragraph "F1's match is **per-endset overlap**: within each endset, satisfaction is existential over spans, and the per-span test is overlap (`coverage(eᵢ) ∩ I ≠ ∅` unfolds to ...)" re-expresses F1's structure in prose.

**Problem**: The unfolding of `coverage(eᵢ) ∩ I ≠ ∅` to the span-existential is a syntactic restatement of the just-given formula; it advances no new reasoning. The "identifiable witness span" remark is the only added content and could attach directly to F4, which is its sole consumer.

**Required**: Drop the restatement; if the witness-span observation is load-bearing for F4, fold it there.

## OUT_OF_SCOPE

### Topic 1: FOLLOWLINK / RETRIEVEENDSETS (inverse direction)
**Why out of scope**: Resolving result endsets back to V-positions is a distinct operation; the ASN correctly lists it under "What We Have Not Specified."

### Topic 2: Replication, caching, consistency models, combined filtered-and-scoped form
**Why out of scope**: These are future-ASN territory and are explicitly disclaimed; their absence is not an error here.

VERDICT: REVISE
