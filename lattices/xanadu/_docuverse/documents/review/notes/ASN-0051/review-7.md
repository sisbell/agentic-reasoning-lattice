# Review of ASN-0051

## REVISE

### Issue 1: SV5 proof asserts domain equality not guaranteed by K.μ~

**ASN-0051, SV5 (ReorderingProjectionInvariance) proof**: "Since π is a bijection on dom(M(d)) = dom(M'(d)), v' = π(v) for a unique v"

**Problem**: K.μ~ defines π as a bijection `π : dom(M(d)) → dom(M'(d))` — a map *between* two potentially distinct sets. Since K.μ~ is a distinguished composite of K.μ⁻ (which removes V-positions) followed by K.μ⁺ (which adds new ones), the post-state domain dom(M'(d)) may contain entirely different V-positions than dom(M(d)). Witness: dom(M(d)) = {[1], [2]}, π([1]) = [3], π([2]) = [4] gives dom(M'(d)) = {[3], [4]} ≠ dom(M(d)). The assertion "dom(M(d)) = dom(M'(d))" is false in general.

The proof's *conclusion* is correct — it needs only that π is a bijection from dom(M(d)) to dom(M'(d)), which K.μ~ guarantees. The false intermediate claim is extraneous to the logical chain.

**Required**: Replace "Since π is a bijection on dom(M(d)) = dom(M'(d))" with "Since π is a bijection from dom(M(d)) to dom(M'(d))".

### Issue 2: π overloaded between projection and reordering bijection

**ASN-0051, SV5 section**: π(e, d) denotes endset projection throughout the ASN; in the SV5 proof, π is rebound to the K.μ~ reordering bijection: "Let π be the reordering bijection from K.μ~."

**Problem**: Within three lines, the reader encounters `π_{Σ'}(e, d)` (projection with state subscript) and `{π(v) : v ∈ resolve_Σ(e, d)}` (bijection applied to a V-position). The two uses are distinguishable by arity but share the same symbol, and the rebinding is easy to miss. This ASN introduces π for projection; K.μ~ (ASN-0047) already uses π for the bijection. Using the same letter for a newly introduced concept that appears alongside a foundation concept invites misreading.

**Required**: Use a distinct symbol for the reordering bijection (e.g., ψ or ρ_π) throughout the SV5 section and in SV13(e), keeping π exclusively for endset projection.

## OUT_OF_SCOPE

### Topic 1: Link-subspace contribution to endset projection
SV11 restricts to the text-subspace projection π\_text(e, d) and notes that no current operation creates non-text V-positions. When a Link Subspace ASN introduces link-subspace V-positions (v₁ = 0), the full projection π(e, d) will include an additional term. The fragment decomposition machinery will need extension to cover the link-subspace block structure.
**Why out of scope**: SV11 correctly identifies the boundary and explicitly defers. The text-subspace restriction is accurate for all reachable states under the current operation set.

### Topic 2: Formal closure of byte-level coverage
The "Content Allocation and Coverage Stability" section argues architecturally that sequential sibling allocation closes byte-level spans to future same-origin entries, but acknowledges this "follows from allocation discipline assumptions not formalised in this ASN." A formal result would require a theorem of the form: for level-uniform element-level spans with reach at or below the current allocation maximum, no future sibling allocation enters the span.
**Why out of scope**: This requires formalizing T10a's sequential allocation guarantee at the element-ordinal level, which is a separate concern from link survivability. SV6 (cross-origin exclusion) is the formalizable half; the same-origin half depends on allocation-regime axioms this ASN properly declines to introduce.

VERDICT: REVISE
