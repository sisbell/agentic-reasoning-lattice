# Review of ASN-0091

## REVISE

### Issue 1: K.μ~ frame "matches exactly" claim elides dom(M) preservation
**ASN-0091, REARRANGE_K realization paragraph**: "K.μ~'s ASN-0047 frame reads `C' = C; E' = E; R' = R; L' = L; (A d' : d' ≠ d : M'(d') = M(d'))`, which matches each RA-frame conjunct exactly"
**Problem**: RA-frame includes `dom(Σ'.M) = dom(Σ.M)` as a conjunct, but K.μ~'s explicit ASN-0047 frame does not state this. The match is correct in substance (K.μ~ doesn't modify the document registry, being a composite of K.μ⁻ and K.μ⁺ neither of which adds or removes documents), but it's not "exact" at the level of explicit clauses.
**Required**: Acknowledge that `dom(M') = dom(M)` is implicit in K.μ~'s definition rather than explicit in its frame, citing the structural argument (K.μ~ is named composite that only rearranges).

### Issue 2: Non-uniqueness of π lacks a worked example
**ASN-0091, "REARRANGE as Vstream-Only Operation" section**: The ASN devotes extensive prose (multiple paragraphs) to discussing how π is non-unique when S5-style sharing occurs — pre-image partitions, free permutation within blocks, and the worked illustration `Σ.M(d) = {v₁ ↦ a, v₂ ↦ a, v₃ ↦ b}` with two distinct valid π witnesses.
**Problem**: No worked example in the three traces demonstrates this. All three examples (3-cut pivot, 4-cut swap, interior cuts) have unique I-addresses per V-position, so the non-uniqueness machinery is never concretely exercised. The standards demand a concrete example demonstrating key claims; the uniformity-of-RE-proj-across-witnesses argument is abstract.
**Required**: Add a concrete trace where multiple V-positions share an I-address, exhibit two distinct valid π witnesses for that transition, and verify that RE-proj's set image is uniform across both witnesses.

### Issue 3: P4a preservation cites an unstated "append-only" property
**ASN-0091, abstract class discussion and worked example admissibility**: "the transition trace is append-only (REARRANGE produces `Σ' = Σ_{n+1}` and modifies no earlier `Σ_k`)"
**Problem**: This is treated as a parenthetical fact rather than derived from a foundation source. ASN-0093's SequentialTransitionAxiom describes transitions as atomic and totally ordered but doesn't explicitly state "earlier states are immutable." The intuition is sound but unsourced.
**Required**: Either cite ASN-0093's SequentialTransitionAxiom as the source (and explain how atomicity implies prior-state immutability), or derive the append-only property as a corollary.

### Issue 4: Chain-distinctness argument is repeated inline three times
**ASN-0091, "Reverse witness (coalescence)", "Equality witness", and "Worked Example — Interior Cuts" setup paragraphs**: The argument "addresses from distinct sub-allocator chains cannot be chain-adjacent because each chain element has structural form `[d, 0, s, k]` with chain-specific (d, s)" is restated in each of these three sections.
**Problem**: A reusable lemma would tighten the presentation. As stated, the reader must re-verify the same structural argument three times, with subtle variants (single chain pair, three-document pair, etc.). Combined with the TA5(c) appeal, this is dense enough to deserve a one-line lemma name.
**Required**: Factor the chain-distinctness fact into a single inline lemma (e.g., "ChainDisjointAdjacency: for `a ∈ A_C(d_X)`, `c ∈ A_C(d_Y)` with `d_X ≠ d_Y`, neither `c = a + 1` nor `a = c + 1` holds") and reference it from each use site.

## OUT_OF_SCOPE

### Topic 1: Link-subspace REARRANGE semantics
**Why out of scope**: Correctly identified in Open Questions. CS3 fixes the cut subspace at S = s_C, and the ASN explicitly notes that a different concrete realization of the abstract class could operate on the link subspace. This is future-ASN territory.

### Topic 2: Cross-document transclusion behavior when a cut splits a transcluded span
**Why out of scope**: Open Question 1. RE-trans verifies the relationship persists with multiplicity, but the geometric semantics of a split transclusion (one referent, two V-positions in d, both pointing into d's source span) deserves its own ASN.

### Topic 3: Upper bounds on fragmentation-induced cardinality increase
**Why out of scope**: Open Question 4. The existential claim RE-frag is appropriate scope for this ASN; characterizing the magnitude is a quantitative extension.

### Topic 4: Realizability of arbitrary bijections by cut-sequence compositions
**Why out of scope**: Open Question 5. The relationship between the abstract class and what REARRANGE_K can actually express belongs to expressiveness analysis, not the current ASN's role.

### Topic 5: Observational equivalence at link-discoverability granularity
**Why out of scope**: Open Question 3. A finer notion of equivalence than arrangement equality is a future refinement.

VERDICT: REVISE
