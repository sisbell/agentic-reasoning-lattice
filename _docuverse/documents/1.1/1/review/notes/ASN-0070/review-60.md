# Review of ASN-0070

I read this as a query specification (inverse image of endset coverage under a document's arrangement) and checked the F-canonical existence/uniqueness proof, the six worked configurations, the WP analysis, and the derived-property catalogue. The core mathematics is sound: Step 1's case split on `actionPoint(ℓ)` correctly rules out `k < m_S(d)` by infinitude and proves both inclusions for `k = m_S(d)`; the consecutivity Characterisation and partition argument in Step 2 are complete; the V-restricted ↔ full denotation bridge in Step 4 is rigorous, including both right- and left-closure of inter-component gaps. F-sound/F-complete correctly split the postcondition equality. I found no correctness holes. The findings below are the anti-bloat / redundancy items this cycle was flagged for.

## REVISE

### Issue 1: Worked Configuration 2 is subsumed by Configuration 5
**ASN-0070, "A Worked Example", Second configuration (multiplicity) and Fifth configuration (cross-subspace straddle)**: Config 2 uses `e₁ = {(a₀, δ(1, m_a))}` and produces `Σ_V^{s_C} = ⟨([1,1], δ(1,2)), ([1,6], δ(1,2))⟩`. Config 5's content branch resolves `a₀` to the *identical* result `⟨([1,1], δ(1,2)), ([1,6], δ(1,2))⟩` and explicitly states "F-multi is exercised" in its verification.
**Problem**: The same content-subspace multiplicity result (one I-address `a₀` at V-positions `[1,1]` and `[1,6]`) is demonstrated twice against the same arrangement. Config 2 adds nothing that Config 5's content branch does not already exhibit. Six configurations in an anti-bloat-flagged note should each carry distinct demonstrative load.
**Required**: Drop Configuration 2 and point F-multi's example to Configuration 5's content branch; or, if a multiplicity-isolating example is preferred for clarity, drop the multiplicity claim from Config 5's verification and keep only Config 2. One site, not two.

### Issue 2: Open Questions 1 and 3 overlap
**ASN-0070, "Open Questions"**: Q1 — "When an endset's coverage spans I-addresses with multiple distinct homes, what relationship must hold between resolutions against documents that transclude from different subsets of those homes?" Q3 — "What relationship must hold between `follow(ℓ, d, i)` and `follow(ℓ, d', i)` when `d` and `d'` share transclusion lineage?"
**Problem**: Both pose the inter-document resolution-relationship question under transclusion; Q3 is a special case of Q1's "documents that transclude from different subsets." Two open questions restating one open direction is accretion at the note's tail.
**Required**: Consolidate into a single open question on inter-document resolution relationships under shared/overlapping transclusion sources.

### Issue 3: Forward-reference framing in the Setting
**ASN-0070, "The Setting"**: "follow reads the current M(d), so only these current-state facts about `m_S(d)` are consumed below."
**Problem**: This is use-site framing ("consumed below") that does not advance the definition of `m_S(d)`; the surrounding sentences already establish that `m_S(d)` is undefined when `V_S(d) = ∅`. Minor, but it is exactly the forward-reference meta-prose this cycle targets.
**Required**: Delete the clause; the depth facts stand on their own.

## OUT_OF_SCOPE

### Topic 1: Multi-home / transclusion-lineage resolution relationships
**Why out of scope**: The consolidated open question (Issue 2) genuinely belongs to a future ASN — it asks for a cross-document invariant that FOLLOWLINK, as a single-document query, does not and should not establish. Correctly left as an open question, not a gap in this note.

VERDICT: REVISE
