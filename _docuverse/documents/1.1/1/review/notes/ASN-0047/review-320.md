# Review of ASN-0047

## REVISE

### Issue 1: Imprecise foundation citation for `origin`
**ASN-0047, Notation (I-address projections)**: "`origin(a)` (ASN-0036, S7a): the document address `d ∈ E_doc` under whose allocator a was minted."

**Problem**: In ASN-0036, `origin(a) = N(a).0.U(a).0.D(a)` is defined in **S7** (StructuralAttribution). S7a is DocumentScopedAllocation, an axiom about *where* allocation happens, not the definition of the `origin` function. A reader cross-checking the foundation against the citation lands on the wrong claim. The same function is used pervasively (S7a/L1a couplings, CL-OWN, P6, fork `d_op`), so the anchor should be exact.

**Required**: Cite the defining claim — `origin(a)` is ASN-0036 **S7**. If the intent is to credit S7a for the allocation semantics, state both: definition (S7), allocation grounding (S7a).

### Issue 2: Node-nesting claim duplicated across NodeRootedForest and CrossNodeAccountBase
**ASN-0047, NodeRootedForest**: "NodeBaptism admits repeatedly baptising distinct nodes, including nodes that nest as T4-legal multi-component tumblers (e.g. `[1,2] ≼ [1,2,3]`, CrossNodeAccountBase)."
**ASN-0047, CrossNodeAccountBase**: "...multi-component node tumblers are T4-legal (`zeros = 0`, `t₁ ≠ 0`, `t_{#t} ≠ 0`, so e.g. `N₁ = [1,2] ≼ [1,2,3] = N₂`)..."

**Problem**: The same factual claim — node tumblers may nest, with the identical worked example `[1,2] ≼ [1,2,3]` — is asserted in two sections, with NodeRootedForest forward-pointing to the section that actually uses it (CrossNodeAccountBase). This is the relocated/previewed-content pattern: NodeRootedForest's sentence does not advance the forest derivation (which only needs "each baptised node roots an independent inc-subtree"); the nesting example earns its keep solely inside CrossNodeAccountBase's non-nesting case split. The duplication is a maintenance hazard — a future edit to one example will silently desync the other.

**Required**: Remove the nesting example from NodeRootedForest, leaving only the independent-root claim it needs; let CrossNodeAccountBase be the sole site of the node-nesting analysis and its example.

### Issue 3: Defensive meta-prose in FrontierEquivalence "Freshness discharge" note
**ASN-0047, FrontierEquivalence, Freshness discharge (scope note)**: "...no structural fact forces it, since GlobalUniqueness (ASN-0034) establishes distinctness only *across distinct allocation events* and so supplies cross-event distinctness once `e ∉ E` grants the event is new, never freshness itself."

**Problem**: The operative content of this note is the per-`k` distinction (which state fact the guard `e ∉ E` encodes at `k = 0` vs `k ∈ {1,2}`) — that is load-bearing and cited downstream. But the lead-in is a defensive justification *about what a foundation lemma does not do* ("never freshness itself"), restated again in the K.δ box ("freshness ... discharged as a single live-state read"). It explains why freshness isn't a theorem rather than stating the discharge. The "GlobalUniqueness gives cross-event distinctness, not freshness" point is made twice (here and in FrontierEquivalence's reverse-direction proof).

**Required**: Trim the lead-in to the operative statement ("freshness `e ∉ E` is a live-state read against Σ; cross-event distinctness then follows from GlobalUniqueness"), keeping the per-`k` encoding distinction, and drop the duplicate "never freshness itself" phrasing.

## OUT_OF_SCOPE

### Topic 1: Renumbering-aware interior link-arrangement contraction
**Why out of scope**: The final open question (interior `DELETEVSPAN` compaction) correctly defers a contraction *operation* beyond the suffix-removal K.μ⁻ this ASN models. This is new operational territory, not an error in the present transition taxonomy — the suffix-only K.μ⁻ is internally consistent with D-CTG★/D-MIN★.

### Topic 2: One-sided / type-only link admissibility
**Why out of scope**: Whether K.λ should require non-empty from/to endsets (the second-to-last open question) concerns link semantics and endset-iterating consumers (L8 `same_type`), which belong to link-model refinement, not the state/transition taxonomy under review here.

VERDICT: REVISE
