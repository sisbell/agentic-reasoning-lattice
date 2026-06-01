# Review of ASN-0047

## REVISE

### Issue 1: Triplicated child-spawn-premise discharge across K.δ case (ii) k=2 sub-cases A/B/C
**ASN-0047, *K.δ case (ii) discharge and parent-allocator activation*, k=2 paragraph**: Sub-cases A (t an account), B (t a non-bootstrap node), and C (t = n₀) each conclude with the *same* discharge: "the K.δ precondition `t = parent(e) ∈ E` discharges the child-spawn spawnPt requirement against whichever allocator (or external commitment) is the minting source of t."

**Problem**: The three sub-cases differ only in (i) the spawned allocator's name (`A_doc(t)` / `A_account(t)`) and (ii) which axiom supplies the spawnPt premise (ParentAllocatorDispatch's account case / NodeUniqueAllocation(c) / NodeRegistryBootstrap). The common discharge pattern — "t already inhabits its minting allocator's tracked domain, preserved by monotonicity, `k' = 2` admissible, zeros bound a fortiori" — is written out three times. This is the forward-reference-accretion "same thing in different words" pattern at triple multiplicity, and the reader must re-read three near-identical paragraphs to extract one dispatch rule.

**Required**: Collapse to a single discharge statement parameterised by the premise source: "the spawnPt premise `t ∈ dom(parent_allocator)` is supplied by [account: ParentAllocatorDispatch; non-bootstrap node: NodeUniqueAllocation(c); bootstrap: NodeRegistryBootstrap], and `k' = 2` admissibility + the zeros bound discharge uniformly." One paragraph, a three-row dispatch.

### Issue 2: NodeRegistryBootstrap / registry-tracking prose explains why the axiom is needed, not what the system guarantees
**ASN-0047, NodeUniqueAllocation clause (c), NodeRegistryBootstrap, and sub-case C**: Clause (c) ("Registry tracking — every `t ∈ Σ.E_node` inhabits the external node-allocation registry's tracked domain") and NodeRegistryBootstrap ("at Σ₀, n₀ inhabits the node-allocation protocol's tracked domain") reference an *external registry* that is not a component of `Σ = (C, L, E, M, R)`.

**Problem**: These axioms exist solely to discharge the k=2 child-spawn spawnPt premise for nodes (sub-cases B and C), and the surrounding prose is "why the axiom is needed" rather than a checkable system guarantee — the tracked domain cannot be evaluated against `Σ`. This is the flagged pattern (new prose around an axiom justifying its necessity), and Open Question 9 already concedes the registry "is itself the right abstraction boundary" is unresolved. Carrying a non-Σ mechanism inside load-bearing axioms weakens the self-containment the reachable-state proof depends on.

**Required**: Either (a) fold the node-baptism premise into one named lemma whose guarantee is stated over `Σ` alone (e.g., a freshness+lineage postcondition on `E_node` without appeal to an external tracked domain), or (b) state explicitly that node baptism is a boundary input and confine all registry language to a single clearly-delimited axiom, removing the per-sub-case necessity elaboration.

### Issue 3: "Content-store invariance under arrangement mutation" restated three times
**ASN-0047, intro, *Destruction confinement* (P3 paragraph), and *Temporal decomposition***: The derived fact that every M-mutating transition carries `C' = C` (so arrangement mutation never touches stored content) is asserted in the opening motivation, re-derived in the post-P3 paragraph ("follows from P0 by the arrangement frames..."), and reasserted in the temporal-decomposition layer table.

**Problem**: A one-line corollary of P0 + the arrangement frames is stated and partially re-derived in three locations. This is mild but compounding redundancy of the kind the anti-bloat classifier flags.

**Required**: Derive it once (in the P3 paragraph), and let the intro and temporal-decomposition sections reference rather than restate it.

## OUT_OF_SCOPE

### Topic 1: Link inheritance under forking
**Why out of scope**: The fork composite (J4) intentionally leaves `d_new`'s link subspace empty, and the ASN states a link-inheritance mechanism "is outside this ASN's scope." This is correctly deferred (Open Question on transclusion chains / link permanence), not an error in the transition taxonomy.

### Topic 2: Concurrent allocation under a shared home document
**Why out of scope**: Serialization of link/content allocation under concurrent operations is raised in the Open Questions and depends on the concurrency model, which is explicitly out of scope. The SequentialTransitionAxiom suffices for the present single-event model.

META: (not applicable — the ASN defines abstract state, elementary transitions, and reachable-state invariants that an alternative implementation would also have to satisfy; it has not drifted to implementation mechanics, the external-registry axioms notwithstanding.)

VERDICT: REVISE
