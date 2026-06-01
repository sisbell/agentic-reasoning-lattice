# Review of ASN-0047

I verified the elementary-transition definitions, the K.δ case-(ii) discharge tree, the K.μ~ decomposition (admissibility clauses, K.μ~-FIX, link-subspace fixity, necessity/sufficiency), the S8★ per-subspace routes, the FrontierEquivalence and CrossNodeAccountBase lemmas, and all five worked examples against the foundation contracts. The mathematics holds up: the freshness discharges, the range-based J1★/J1'★ scoping, the content/link subspace partitioning, and the per-state vs composite-boundary classification are all sound. My findings are confined to forward-reference/meta-prose accretion, which the note explicitly directs me to surface.

## REVISE

### Issue 1: Document-structure meta-prose in the K.δ per-k freshness mechanism
**ASN-0047, *Elementary transitions*, K.δ case (ii)**: "This is the sole statement of the freshness discharge; §*K.δ case (ii) discharge and parent-allocator activation* and the worked examples invoke it only for activation context (which parent allocator each step acts on) and do not restate it."

**Problem**: This sentence advances no part of the freshness claim. It is a use-site inventory plus a promise about where the discharge is and is not restated — the exact "definition's introduction enumerates downstream consumers" / "prose justifies document ordering" pattern the forward-reference accretion check names. The substantive content (the k-dependent uniqueness fact, FrontierEquivalence at k=0, the direct per-`(t,k')` axiom at k∈{1,2}) is complete without it.

**Required**: Delete the sentence. The per-k mechanism stands on its own; downstream sections can cite it without this sentence announcing that they will.

### Issue 2: "Cite rather than restate" / "Not restated here" scaffolding in the Class (a) verification
**ASN-0047, *Extended reachable-state invariants*, Class (a)**: two instances —
- "*K.μ~ discharge for the arrangement-shape package (uniform argument).* … The per-property paragraphs below give only their non-K.μ~ discharge plus any per-property delta; their K.μ~ clauses cite this argument rather than restate it."
- "*P6 (Existential coherence), P7 (Provenance grounding), P8 (Entity hierarchy).* Each is established by the inductive *Derivation* in its definition box … Not restated here."

**Problem**: Both passages narrate the document's own internal cross-referencing rather than discharging the invariant. A bare cross-reference ("P6/P7/P8: see definition boxes") carries all the information; the surrounding explanation of *which* arguments are and are not restated where is meta-prose the reader must read past to reach the actual discharge.

**Required**: Replace each with a one-line pointer to the source paragraph/definition box, dropping the commentary about restatement policy.

## OUT_OF_SCOPE

### Topic 1: Concurrent allocation under a shared home document
The ASN's own Open Questions raise serialization of link allocation under concurrent operations. This is correctly deferred — SequentialTransitionAxiom assumes total ordering, and concurrency is a separate concern.

### Topic 2: Link-withdrawal / tombstoning mechanism
The tension between D-CTG★/D-MIN★ (link suffix-truncation only) and Nelson's interior-link tombstoning (LM 4/9) is flagged in the Open Questions and belongs in a future ASN, not here.

VERDICT: REVISE
