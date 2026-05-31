# Review of ASN-0043

## REVISE

### Issue 1: L11a's shared-home merge conflates `#E ≥ 2` with `#E = 2`
**ASN-0043, L11a — LinkUniqueness, "Shared home" case**: "Reaching a link address `d.0.s_L.ω` (element field `[s_L, ω]`, depth `#E ≥ 2` by L1b) ... its `inc(·, 0)` siblings `d.0.s_L.1, d.0.s_L.2, …` are the link ordinals ... Hence `a₁` and `a₂` are distinct siblings of the one link-ordinal allocator."

**Problem**: The argument writes the element field as the 2-tuple `[s_L, ω]` and concludes `a₁, a₂` are *siblings of the single grandchild (link-ordinal) allocator* with base `d.0.s_L.1`. That conclusion holds only when `#E(a) = 2`. But L1b guarantees only `#E(a) ≥ 2`, and no invariant in this ASN caps element-field depth at 2 (Gregory's depth-2 allocation is implementation evidence, not an abstract bound). For a permitted link address with `#E(a) = 3` — e.g. `d.0.s_L.x.y` — the address is a *grandchild* of the link-ordinal allocator, not a sibling of `d.0.s_L.1`, so the two existence-chains share a *third* child-spawn `inc(d.0.s_L.x, 1)` that the argument never traces. The proven structural merge ("distinct siblings of one link-ordinal allocator") is therefore established only for the minimal-depth case. Showing the `#E = 2` case works does not establish the `#E > 2` case L1b admits.

**Required**: Either (a) generalize the merge to arbitrary `#E ≥ 2` — observe that both chains share the single `inc(d, 2)` child-spawn and are thereafter nodes of the one subtree of 𝒯 rooted there, which is all GlobalUniqueness's single-system precondition needs, without claiming sibling-of-one-allocator structure; or (b) introduce an upper-bound invariant `#E(a) = 2` and derive it, then keep the current narrative.

### Issue 2: Properties table cell carries a proof sketch, not an index entry
**ASN-0043, "Properties Introduced", L11a row**: "... body embeds the L1c chains as genuine events of the single tree 𝒯 (same-home chains share both child-spawns — `inc(home, 2)` and `inc(home.0.s_L, 1)` — per at-most-once, leaving `a₁, a₂` siblings of one link-ordinal allocator; distinct-home chains lie in T10-incomparable subtrees) before invoking GlobalUniqueness."

**Problem**: This is essay/proof content in a structural slot. The summary table should index each property in one line; instead this cell re-encodes the entire two-case shared/distinct-home argument from the body, duplicating it in different words (and re-importing the same `#E = 2` over-specification flagged in Issue 1). A reader who must reconcile a mini-proof in the table against the body proof is working around accreted prose, not reading an index. (The L11b row similarly recapitulates its FSE construction.)

**Required**: Reduce the cell to a one-line statement of what L11a asserts (e.g., "distinct T10a allocation events yield distinct link addresses; single-system precondition discharged by embedding link chains in 𝒯"). Move any reasoning into the body, where it already lives.

### Issue 3: Defensive/plausibility prose that does not advance the claim
**ASN-0043, L10**: "The exclusion direction is essential: without it, a span query at `p` that also matched non-subtypes would not give a clean type hierarchy."
**ASN-0043, L-fin**: "The set of valid link addresses ... is countably infinite, but only finitely many are occupied in any reachable state."

**Problem**: Both are commentary on why a result is desirable or plausible rather than steps in the argument. L10 has already proven `coverage = subtypes(p)` (all and only); the "is essential" sentence justifies the result's value, not its truth. L-fin's gloss restates the invariant's intuition without deriving anything. Per the anti-bloat classifier, defensive justifications of an already-discharged claim are noise the precise reader must skip.

**Required**: Delete both sentences; the proven biconditional (L10) and the invariant statement (L-fin) stand on their own.

## OUT_OF_SCOPE

### Topic 1: Upper bound on link element-field depth
**Why out of scope**: Whether `#E(a)` should be fixed at exactly 2 (rather than `≥ 2`) is a candidate new invariant, already noted indirectly by the open questions on allocation ordering. If Issue 1 is fixed by route (a), no such invariant is needed; introducing one is a separate design decision, not a defect in the current claims.

VERDICT: REVISE
