# Review of ASN-0043

## REVISE

### Issue 1: Worked-example step introduces `a₂` without defining its address
**ASN-0043, Worked Example, meta-link step (producing `Σ_2`)**: "The final state is `Σ_2` with `Σ_2.L = {a ↦ (F, G, Θ), a' ↦ (F, G, Θ), a₂ ↦ (F₂, G₂, Θ₂)}`."
**Problem**: The step defines the spans `F₂, G₂, Θ₂` and the entry `a₂ ↦ (F₂, G₂, Θ₂)`, but never states the tumbler value of `a₂`. The address is only disclosed later, in Step 3 ("sibling advance from `a₂ = 1.0.1.0.1.0.2.3`"). The reader must look ahead to a subsequent step to learn what `a₂` is, and cannot check `L0`/`L1`/`L1c` for `a₂` at the point it is introduced. The verifications attached to this step (`L13`, `L0 for a₂`, `L4 for a₂`) all depend on `a₂`'s address.
**Required**: State `a₂ = 1.0.1.0.1.0.2.3` (the next link-subspace sibling after `a'`) in the meta-link step where it is introduced, before its invariant checks.

### Issue 2: Double deferral of the L0a disjointness — forward-reference accretion
**ASN-0043, L0a and the L0b preamble**: L0a — "We therefore defer it until those premises are in hand, deriving it as L0b's corollary immediately after L1c." Then before L0b — "With L1 and L1c now in hand, we discharge the disjointness deferred in L0a."
**Problem**: Two paragraphs in different sections defer to the same downstream location and justify the document ordering of the disjointness derivation. This is exactly the forward-reference pattern the anti-bloat classifier flags ("multiple paragraphs defer to the same downstream location"; "prose justifies document ordering"). One sentence at the L0a definition site noting that disjointness is derived as L0b suffices; the second cross-reference at the L0b site restates it.
**Required**: Collapse to a single pointer. Keep L0a's slice definition plus one clause ("disjointness is derived as L0b, after L1c"); drop the "With L1 and L1c now in hand, we discharge the disjointness deferred in L0a" preamble and let L0b's body state the derivation directly.

### Issue 3: Axiom-rationale prose around L1c
**ASN-0043, L1c (LinkAllocatorConformance), opening**: "The *Chain* clause below supplies the witnessing step sequence; the `inc(·, 0)` / `inc(·, k')` discipline it instantiates is fixed by T10a and not re-derived here."
**Problem**: This sentence explains what the axiom does *not* re-derive and where its discipline comes from, rather than advancing the statement — the flagged pattern "new prose around an axiom explains why ... rather than what it says." The *Chain* clause that follows is self-describing; the disclaimer that T10a is not re-derived adds no content (no ASN re-derives a cited foundation).
**Required**: Delete the sentence; let the *Chain* clause stand.

### Issue 4: L11a shared-home case re-applies T10a mechanics at excessive length
**ASN-0043, L11a, "Shared home" paragraph**: the argument tracing "the subspace identifier sits at position `#d + 2` ... every sibling advance `inc(·, 0)` acts on the `sig` position ... any descent freezes it (TA5(b)) ... `k' = 1` is the unique admissible second child-spawn ..."
**Problem**: The single-system embedding genuinely needs that both chains route through `inc(d, 2)`, the `s_L − 1` sweep, and `inc(d.0.s_L, 1)`. But the paragraph re-derives the position-freezing behaviour of `inc` and the admissibility ruling-out of `k' = 2`/further siblings from TA5/TA5a/TA5-SigValid step by step, repeating mechanics the foundation already fixes. The load-bearing claim — "both chains share the edges `inc(d,2)`, `…→d.0.s_L`, `inc(d.0.s_L,1)`, so `a₁, a₂` descend from one shared link-ordinal allocator" — is buried under the re-derivation.
**Required**: Reduce to the forced-routing skeleton: both chains open with the one `inc(d, 2)` (T10a at-most-once on `(d,2)`), reach `d.0.s_L` (only depth-1 siblings raise position `#d+2`, frozen on descent), then take the one `inc(d.0.s_L, 1)` (the unique T4-preserving, depth-extending, `s_L`-fixing step), citing TA5/TA5a/L0b/L0 without re-proving them.

## OUT_OF_SCOPE

### Topic 1: Global content-subspace constant
The first Open Question (extending disjointness from the `s_C`-resident slice to all of `dom(Σ.C)`) is correctly deferred — it requires a content-side invariant this ASN does not own.

### Topic 2: Link/transclusion interaction and compound-link well-formedness
Constraints between the link store and arrangements under transclusion, and well-formedness of compound link structures, are future-ASN territory; the Open Questions list them appropriately.

VERDICT: REVISE
