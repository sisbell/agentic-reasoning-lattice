# Review of ASN-0077

## REVISE

### Issue 1: Form (F2) is introduced and proven equivalent but never consumed

**ASN-0077, "Lifting origin to a V-span"**: "We work with three equivalent expressions… *(F2)* `origins_V(Σ, d, σ) = ⋃_{j=1}^{k} { origin(aⱼ + i) : 0 ≤ i < nⱼ }`… We adopt (F1) as the definition and derive (F2) and (F3) as equivalent forms."

**Problem**: The equivalence chain establishes (F1)≡(F3) directly — it proves `(F1) ⊆ (F3)` and `(F3) ⊆ (F1)` without routing through (F2). The only place (F2) appears thereafter is the `(F2) = (F3)` step itself. No downstream claim (O7, O11, O12, the worked example, the wp's) consumes (F2); the worked example reasons in (F3)'s block-collapsed form. (F2) is a dead intermediate.

**Required**: Either cite a load-bearing use of (F2) or remove it, proving (F1)≡(F3) and noting the block-collapsed form (F3) as the only auxiliary needed.

### Issue 2: Five claims forward-defer to the operation spec's well-formedness preconditions

**ASN-0077, O11 / O11' / O11.1 / O11★★ / O13**: e.g. "any V-span `σ` over `d` satisfying the SHOWORIGIN_V well-formedness preconditions at Σ — in particular precondition (vi)".

**Problem**: O11, O11', O11.1, O11★★, and O13 all reference "the SHOWORIGIN_V well-formedness preconditions" and re-name "precondition (vi)" by ordinal, but those preconditions (i)–(vi) are only enumerated later, in "The operation." A reader hitting O11 must jump forward to resolve "(vi)," and the parenthetical "(in particular precondition (vi))" is repeated across five sites — the forward-reference-accretion pattern (multiple sections deferring to one downstream location).

**Required**: Hoist a named predicate — e.g. `WF_V(Σ, d, σ)` — stating the six conjuncts once, before O11, and have the O11-series and O13 reference it by name. This removes the by-ordinal forward references and the repeated parentheticals.

### Issue 3: Cross-subspace I-span behavior is both decided and re-posed as open

**ASN-0077, edge case "Cross-subspace I-span"**: "The lift's intersection with `dom(C)` therefore silently drops link addresses… This is a deliberate choice of the I-span lift's definition: SHOWORIGIN over an I-span reports origins of content, not of links."

**ASN-0077, Open Questions**: "What must SHOWORIGIN guarantee when its input span crosses subspace boundaries (content addresses and link addresses both present in the I-stream range)?"

**Problem**: The edge case already decides the I-span case (link origins dropped, by definition). The first Open Question re-poses the same scenario as unresolved, without distinguishing what residual question remains (e.g., whether a *unified* content-and-link origin operation is wanted).

**Required**: Either drop the Open Question (the I-span behavior is settled) or narrow it to the genuinely open part — a combined operation reporting link origins — so it does not appear to contradict the edge case's "deliberate choice."

### Issue 4: Intro and summary state the span-derivation point in duplicate

**ASN-0077, opening**: "Span-level results are derived from this pointwise guarantee rather than inheriting it unchanged — a multi-source span returns the *set* of homes present, and that set grows as content is allocated and, for a span named by arrangement position, depends on the arrangement."

**ASN-0077, Summary (final paragraph)**: "Span-level answers are derived from this pointwise invariant rather than sharing it: an I-span's reported set grows monotonically under content allocation… while a V-span's answer is arrangement-dependent…"

**Problem**: The two passages make the same claim in different words — the duplicate-paragraph pattern called out for anti-bloat notes.

**Required**: Let the Summary carry the precise (claim-cited) statement and trim the intro sentence to the bare motivation, or vice versa.

## OUT_OF_SCOPE

### Topic 1: Historical-containment operation over `Σ.R`
**Why out of scope**: The note correctly flags (in "What SHOWORIGIN does not promise" and its fourth Open Question) that an operation reporting documents that *ever* contained content — distinct from current arrangement origin — is separate territory. That belongs in a future ASN, not a revision here.

### Topic 2: Surfacing the intermediate transclusion chain
**Why out of scope**: O4 and the worked example establish that SHOWORIGIN reports the direct origin and walks no chain. A complementary operation that exposes the `d₁ → … → dₙ` chain is new territory, properly left to a future ASN.

VERDICT: REVISE
