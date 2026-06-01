# Review of ASN-0047

## REVISE

### Issue 1: "T1 / T2" used as increment-type labels collide with foundation property labels
**ASN-0047, *ParentAllocatorDispatch*, *K.δ case (ii) discharge*, *J4*, worked examples**: e.g. "the step `e = inc(t, 0)` is a T10a **T1** sibling-increment on the activated parent allocator"; "the T10a **T2** spawn step that activates `A_v(t)`"; "**T2** admissibility: `k' = 1 ∈ {1, 2}`."

**Problem**: `T1` and `T2` are established foundation labels — T1 = LexicographicOrder, T2 = IntrinsicComparison (ASN-0034). This ASN overloads them to mean "sibling increment (`k=0`)" and "child spawn (`k≥1`)." The collision is acute because the *same ASN* simultaneously uses `T1` in its foundation sense throughout ("ordered under T1," "T1 sibling-increments on `A_v(d)`'s frontier" — both senses in one clause). A reader cannot tell whether "T1" denotes the order or the increment kind without inferring from context.

**Required**: Rename the increment-type labels to non-colliding terms (e.g. "sibling-advance" / "child-spawn," already used elsewhere in the ASN) and reserve `T1`/`T2` for the foundation properties.

### Issue 2: Foundation properties are renamed / mis-attributed
**ASN-0047, *SubAllocatorAxiom.Disjointness*, *SubAllocFresh*, *Link-subspace extension* (b)**: cites "T7 (**FirstElementFieldDistinction**, ASN-0034)."
**ASN-0047, *FrontierEquivalence*, *K.δ case (ii)*, *S7d***: cites "**T10a** GlobalUniqueness" / "T10a's GlobalUniqueness."

**Problem**: ASN-0034's T7 is named **SubspaceDisjointness**, not "FirstElementFieldDistinction" — the ASN invents a new name for a foundation property (standard 7). Separately, **GlobalUniqueness** is a *standalone* ASN-0034 theorem (it *depends on* T10a; it is not a clause of T10a); writing "T10a GlobalUniqueness" mis-attributes it as a sub-property of T10a. Both undermine the self-containment guarantee that foundation references resolve unambiguously.

**Required**: Use the canonical foundation name "T7 (SubspaceDisjointness, ASN-0034)" at every site, and cite "GlobalUniqueness (ASN-0034)" rather than "T10a GlobalUniqueness."

### Issue 3: Axiom-surrounding rationale prose explains why an axiom is needed rather than what it states
**ASN-0047, *NodeUniqueAllocation*/*NodeRegistryBootstrap* cluster and Open Questions**: e.g. the registry Open Question — "Nelson's design specifies a contractual single root authority (LM 4/17–4/22) delegating recursively under the owned-numbers principle; Gregory's implementation realises this as a single global granfilade with query-and-increment dispatch (the granfilade tree serving as the registry, append-only by L1c/T10a discipline, with single-threaded sequential execution eliminating races). Whether a future ASN should specify the registry mechanism … or whether NodeUniqueAllocation is the right abstraction boundary … is left open." The Properties table entry for NodeRegistryBootstrap likewise carries "The registry is not a component of Σ; n₀ enters at Σ₀ rather than via a prior K.δ event."

**Problem**: This is the `review-mode.anti-bloat` "Protocol rationale / why the axiom is needed" pattern — paragraphs that justify the axiom's existence and abstraction-boundary placement rather than stating or applying its content. It does not advance the verification argument; a reader chasing the discharge of `e ∉ E` must skip past it.

**Required**: Reduce to the axiom statement and its discharge role. Move the boundary-justification and implementation-mapping commentary out of the axiom's surrounding prose (a one-line Open Question pointer suffices).

## OUT_OF_SCOPE

### Topic 1: Link inheritance / refractive following under forking
The J4 section notes that a forked document's link subspace starts empty and that "A mechanism for link inheritance under forking … is outside this ASN's scope." Correctly deferred — this is new operational territory, not a defect here.

### Topic 2: Interior link withdrawal / tombstoning
The tension between Nelson's tombstoning (LM 4/9) and D-CTG★/D-MIN★ suffix-only contraction is correctly catalogued as an Open Question requiring a separate mechanism, not a revision to K.μ⁻.

VERDICT: REVISE
