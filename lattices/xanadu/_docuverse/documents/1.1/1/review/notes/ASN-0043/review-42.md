# Review of ASN-0043

## REVISE

### Issue 1: Non-transcludability of links is derived but claimed as deliberate

**ASN-0043, Dual-Primitive Architecture (L14 discussion)**: "This asymmetry is deliberate. Content wants to be shared — that is the point of transclusion. But a connection is an assertion by a specific principal about specific content, and assertions are not transferable by reference."

**Problem**: The non-transcludability claim is derived from S3 + L0: S3 restricts arrangements to `dom(Σ.C)`, L0 gives disjointness, therefore no arrangement can map to a link address. But the same section acknowledges that S3 may need relaxation: "Accommodating this in the abstract model would require extending the arrangement semantics beyond S3." If S3 is relaxed to allow link V-positions (as the implementation evidence in the parenthetical suggests is necessary), the derivation breaks and non-transcludability loses its formal backing. Calling a property "deliberate" while deriving it from an axiom you yourself flag as provisional is a contradiction — either the property is contingent on S3's current formulation, or it stands independently of S3. The ASN cannot have it both ways.

**Required**: If non-transcludability is a design requirement, state it as an explicit invariant independent of S3, e.g.: `(A d, v : v ∈ dom(Σ.M(d)) : Σ.M(d)(v) ∉ dom(Σ.L))`. Then when S3 is extended to accommodate link V-positions, this invariant survives on its own terms and the design intent is formally preserved. The current derivation from S3 becomes a verification that the present model satisfies the invariant, not the sole source of the guarantee. Alternatively, weaken the prose to say the asymmetry is a consequence of S3's current formulation rather than calling it "deliberate."

### Issue 2: L9 witness — L1c verification does not handle initial allocation

**ASN-0043, L9 (TypeGhostPermission), witness verification**: "L1c — The address `a` is the next output of a T10a-conforming allocator within `d'`'s link subspace, produced by `inc(·, 0)` from the allocator's current frontier."

**Problem**: The proof says "Pick any document prefix `d'`" and then asserts `a` is produced by `inc(·, 0)` from "the allocator's current frontier." But `dom(Σ.L) = ∅` is a valid conforming state — all link invariants hold vacuously. For such a `Σ`, no document has any link allocations and no frontier exists. `inc(·, 0)` requires a base address to increment; the proof does not construct one. The cardinality argument (infinitely many valid addresses, finitely many occupied) correctly establishes that a fresh address exists, but T10a conformance requires showing the address is *reachable* by the allocation discipline — and for the initial case that requires a child-spawning sequence from the document level through element level into the link subspace, not a sibling increment from a nonexistent frontier.

**Required**: Add one sentence handling the initial case: when `d'` has no prior link allocations, the first link address is established by the child-spawning sequence from `d'`'s element-level allocator — `inc` to reach subspace `s_L` at element field depth 1, then `inc(·, 1)` to reach depth 2 — which is T10a-conforming by TA5a bounds (`k' = 1` with `zeros ≤ 3`). All subsequent link addresses in that subspace are then producible by `inc(·, 0)`.

## OUT_OF_SCOPE

### Topic 1: PrefixSpanCoverage as a foundation result
**Why out of scope**: PrefixSpanCoverage — that the unit-depth span at `x` covers exactly `{t : x ≼ t}` — is a general tumbler-algebra fact with no dependency on link ontology. It is correctly proved and properly used here (for L9 and L10), but it belongs in ASN-0034 or a span algebra ASN so that other ASNs can cite it without depending on the link ontology. This is a promotion suggestion, not a defect.

### Topic 2: Link arrangement semantics
**Why out of scope**: The ASN acknowledges that Gregory's implementation places links in document arrangements (V-positions `1.1`, `2.1`, `3.1`), but S3 restricts `Σ.M(d)` to content addresses. Extending the arrangement model to accommodate link V-positions is future work that belongs in an arrangement or operations ASN, not in link ontology.

VERDICT: REVISE
