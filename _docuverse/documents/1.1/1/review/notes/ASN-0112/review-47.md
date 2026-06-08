# Review of ASN-0112

## REVISE

### Issue 1: Level-uniformity of the returned span never characterized
**ASN-0112, V0 / V2 / V-ReachTight**: "`RETRIEVEDOCVSPAN : dom(M) → SpanSet`" and "the span `(origin_d, extent_d)` is always a well-formed T12 span"
**Problem**: V0 commits the result to ASN-0053's `SpanSet` type, and V2 proves T12 well-formedness, but the ASN never states whether `σ_d` is *level-uniform* (S6: `#start = #width`). The same depth axis that drives V-ReachTight settles this: `#extent_d = max(#origin_d, #reach_d)`, so when `#origin_d < #reach_d` (the abstract cross-subspace case `m_C < m_L`, which the ASN deliberately admits and handles in V2 case 1), the span is **not** level-uniform, whereas in the implementation-realized regime (`m_C = m_L`, Q2) it is. Since the ASN carefully tracks the `#origin_d` vs `#reach_d` relationship everywhere else and types its output as an ASN-0053 span-set, the level-uniformity status is a directly derivable consequence that is currently unexplored.
**Required**: Add a derived clause stating the level-uniformity status of `σ_d` (level-uniform iff `#origin_d ≥ #reach_d`, equivalently always level-uniform under the realized `m_C = m_L` discipline), parallel to V-ReachTight.

### Issue 2: V18 accretes redundant framing around V8 and defers within the document
**ASN-0112, V18**: "Origin permanence (V8) holds exactly while content is present; among editing transitions... the to-empty/from-empty transitions are governed by V11."
**Problem**: V18 opens by restating V8's own scope, then closes by punting two transition classes to V11 — an intra-document deferral chain (V8 ↔ V18 ↔ V11) for a single coherent fact about origin behavior. The sentence "Every other defined-origin editing transition leaves the content-occupancy status unchanged and so fixes the origin" is an exhaustiveness claim asserted without naming the transition vocabulary (K.μ⁺, K.μ⁺_L, K.μ⁻, K.μ~) it ranges over.
**Required**: Consolidate the origin-permanence story (V8 + its boundary) into one claim; if the exhaustiveness over editing transitions is load-bearing, enumerate the vocabulary rather than asserting "every other."

### Issue 3: Ghost-element analogy conflates two distinct concepts in V11
**ASN-0112, V11**: "a document address with nothing stored against it — a 'ghost element' (4/23) — answers identically, with the empty span-set."
**Problem**: The "ghost element" of the cited material (ASN-0040 B3: a baptized tumbler `t ∈ s.B` with nothing stored) is an *element-level* notion, not an empty *document* (`d ∈ dom(M)` with `M(d) = ∅`). The analogy places a foundation concept where it misdescribes the case under discussion.
**Required**: Either drop the ghost-element phrasing or state the empty-document case directly (`O(d) = ∅` for an allocated `d`) without borrowing the element-level term.

## OUT_OF_SCOPE

(none — the scope exclusions are respected; ASN-0113 appears only in the exclusion list, and the multi-subspace extent/count question is correctly left to the Open Questions.)

VERDICT: REVISE
