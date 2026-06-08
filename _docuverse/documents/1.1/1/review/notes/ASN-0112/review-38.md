# Review of ASN-0112

## REVISE

### Issue 1: Depth-divergence / reach-tightness prose is distributed redundantly across five sites

**ASN-0112, V2 prose / V3 prose / V3 table row / Implementation remark / worked variant**: The single fact — "the denotational reach attains the constructed endpoint `reach_d` iff `#origin_d ≤ #reach_d` (equivalently `m_C ≤ m_L`), and the implementation only realizes `m_C = m_L`" — is carved out or restated in five places:
- V2 prose: "What the endpoint relation governs is only the reach. We record V-ReachTight..."
- V3 prose: "Whether `σ_d`'s own reach attains `reach_d` is governed by V-ReachTight."
- V3 table row: "Whether `σ_d`'s own denotational reach `r⋆` attains `reach_d` is the separate V-ReachTight question."
- Implementation remark (reach tightness): restates `m_C = m_L` so "V-ReachTight fires affirmatively."
- Worked depth-divergent variant: "what lapses is V-ReachTight `reach(σ_d) = reach_d`."

**Problem**: This is the flagged accretion pattern — multiple paragraphs in different sections deferring to / restating the same downstream claim. After V-ReachTight was promoted to a named claim (per the latest revision), the carve-out sentences in V2 prose, V3 prose, and the V3 table row are pointers that no longer advance the argument; the V3 prose sentence and V3 table-row sentence are near-verbatim duplicates of each other.

**Required**: State the reach-attainment question once, at V-ReachTight, where it is now named. Drop the duplicated pointer from either V3 prose or the V3 table row, and trim V2 prose to the bare statement that the reach equals `reach_d` under D1 (deferring the biconditional to V-ReachTight without re-explaining it). Keep the implementation remark and the worked variant as concrete evidence, but they need not re-derive the iff.

### Issue 2: V3's "tightest bound" reads as a property of the returned span but characterizes only the constructed intermediate `reach_d`

**ASN-0112, V3**: "`reach_d` is the least strict upper bound of `max O(d)` among tumblers at the depth of `max O(d)`."

**Problem**: The operation returns `σ_d = (origin_d, extent_d)`, whose denotational reach is `r⋆`, and `r⋆ > reach_d` exactly when `#origin_d > #reach_d` (V-ReachTight). So in the depth-divergent case V3's tightness claim is about a value that is *not* the reach of the span the caller receives. A reader tracking "is the returned span tight?" has to cross-reference V-ReachTight to learn that the answer is no in that case. The claim is correct as stated about `reach_d`, but its placement next to V2's coverage claim invites reading it as tightness of the delivered span.

**Required**: Reframe V3 to make explicit at the point of statement that it bounds the *constructed endpoint* `reach_d`, and that the delivered span's reach equals `reach_d` only under V-ReachTight — rather than leaving that qualification to a trailing pointer.

### Issue 3: Residual rhetorical meta-prose in a structural slot

**ASN-0112, "The substrate we measure" intro**: "The entire content of this note is: what is that value, and what must hold of it?"

**Problem**: This is motivational framing that does not advance the reasoning; it restates the section header's purpose. Under the anti-bloat classifier this is noise the precise reader works around.

**Required**: Delete, or fold into the operative sentence that actually introduces `O(d)`.

## OUT_OF_SCOPE

(none — the note correctly confines itself to the boundary query and routes per-subspace extent, link counting, version comparison, and content delivery to their own operations.)

## Notes on what was checked and holds

- V2 coverage: both depth cases (`#origin_d ≤ #reach_d` via D1; `#origin_d > #reach_d` via D0 + direct TumblerAdd computation, `reach_d ≺ r⋆`) are exhaustive and the T12 well-formedness derivation (D0 gives `Pos(extent_d)`, `actionPoint = divergence ≤ #origin_d`) is sound. The single-subspace/cross-subspace divergence-bound split (`k ≤ #origin_d`) is complete.
- V5/V6 exhaustiveness rests correctly on S3★-aux; the V6 strictness witness `w⋆ = [s_C,1,…,1,n_C+1]` checks out (`origin_d ≤ w⋆ < reach_d`, `w⋆ ∉ O(d)`).
- V8/V18 are mutually consistent (V18 correctly bounds V8 at the two content-occupancy toggles; both reachable per ASN-0047 K.μ⁻ per-subspace retention).
- V9 relies correctly on K.μ~-FIX (`dom(M'(d)) = dom(M(d))`).
- Worked example and depth-divergent variant arithmetic verified.

META: not applicable — the note specifies a query operation, its codomain, and value-level invariants abstractly; it has not drifted into implementation mechanics.

VERDICT: REVISE
