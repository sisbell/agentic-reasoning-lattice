# Review of ASN-0086

## REVISE

### Issue 1: R7's proof is one sentence for a meta-claim
**ASN-0086, R7 (NullifyIsEmit)**: "Proof. By Definition. At the relational layer, the substrate exposes exactly two visible-operation primitives..."
**Problem**: "By Definition." is the entire formal proof. The claim that "Nullify is not a separate primitive at the relational layer" is a non-trivial meta-claim about the operation set's structure — that the relational layer's state-transforming operations are closed under "Emit_K with designated arguments." The surrounding paragraph asserts this but the proof does not argue it. A reader who doubts that the enumeration {Emit_K, Observe} is exhaustive gets no formal traction from "By Definition."
**Required**: Replace the proof body with a substantive argument: (i) enumerate the relational-layer operations defined in this ASN; (ii) show Nullify unfolds to `Emit_R(Σ, d_retr, ∅, {(a, δ(1, #a))})` by its own Definition; (iii) argue closure — no other state-transforming operation at this layer is defined, and any future relational-layer mutation must be expressible as an Emit_K composition by L12 (which forbids in-place modification); (iv) conclude that the operation set has exactly two state-affecting primitives, of which Nullify is not one.

### Issue 2: Emit_K determinism in Case B is implicit
**ASN-0086, Definition — Emit_K**: "the Case B address (a = inc^i(b, 0) for the least i ≥ 1 with inc^i(b, 0) ∉ dom(Σ.L), where b ∈ dom(Σ.L) has home(b) = d)"
**Problem**: The definition does not say which b is chosen. Read naively, the operation is non-deterministic. Under R0a's sibling-stream invariant, the result inc^{i'}(d.0.s_L.1, 0) at the frontier index i' is independent of b — but this independence is what makes Emit_K well-defined as a function, and it is not argued. A reader walking through Emit_K's specification has to reconstruct the R0a-based independence argument themselves before they can trust the signature `Σ × dom(Σ.M) × Endset × Endset → Σ' × A_rel^{Σ'}` returns a single Σ'.
**Required**: Add a remark immediately after the Case B description: if b = inc^k(d.0.s_L.1, 0) (by R0a's sibling-stream invariant), then the least i with inc^i(b, 0) ∉ dom(Σ.L) corresponds to the least j = i+k with inc^j(d.0.s_L.1, 0) ∉ dom(Σ.L), so the resulting address inc^j(d.0.s_L.1, 0) is fixed by Σ and d alone — independent of the chosen b. Therefore Emit_K is a function, not a relation.

### Issue 3: Shared-allocator interpretation buried in proof prose
**ASN-0086, R0 Step 2 Case A**: "the L1c chain from d to a describes a walk through the depth-1 element-field allocator A_d (which is a single shared allocator across all subspaces under d, not one allocator per subspace)"
**Problem**: The parenthetical is load-bearing. The chain (d, 2) → sibling sweep within A_d → (d.0.s_L, 1) traverses subspace 1 (content) and subspace s_L (link) within a single sibling stream. If a reader interprets subspaces as separate allocators, the chain steps appear illegal (no inter-allocator sibling step exists in T10a). The author flags this in passing but the model commitment — "subspaces are first-element-field labels enumerated by a single depth-1 allocator under d, not independent allocator trees" — is not stated as an axiom of this ASN and is not derived from foundation ASNs.
**Required**: Either (i) derive the shared-allocator structure as the unique consistent reading of T10a + L0 + S7c (showing T10a's at-most-once spawn discipline forces a single A_d^{(d,2)} producing all element-field-depth-1 positions), or (ii) state it as a named model commitment at the head of the Setup section, with a brief argument that no alternative reading is admissible.

### Issue 4: Arrangement-modification frame inheritance not specifically cited
**ASN-0086, Scoping note**: "Arrangement-modification frame (inherited from ASN-0036). The substrate-level frame on every arrangement-modifying transition is (Σ'.C, dom(Σ'.M), Σ'.L) = (Σ.C, dom(Σ.M), Σ.L)..."
**Problem**: R6c-Corollary's preservation argument depends on this frame, but the inheritance route is asserted without citation. ASN-0036's invariants (in the foundation extracts) include S9 (Σ.C invariance under Σ.M modification) but do not directly state the (Σ'.C, dom(Σ'.M), Σ'.L) frame — most pointedly because ASN-0036 does not include Σ.L. The "inheritance" is in fact: arrangement-modifying transitions are defined on (Σ.C, Σ.M) and so leave Σ.L unchanged when state is extended to include it (and dom(Σ.M) is preserved by the operation class's definition). This indirect derivation should be made explicit.
**Required**: Cite the specific ASN-0036 source for each frame component: S9 for Σ.C invariance; the definitional restriction of arrangement modifications to existing documents for dom(Σ.M) invariance; the absence of Σ.L from ASN-0036's state (combined with L12 + L12a from ASN-0043) for Σ.L invariance. Without this, R6c-Corollary's foundation is unstated.

## OUT_OF_SCOPE

### Topic 1: Self-referential and self-nullifying tuples
Under R0a's discipline, Emit_K is deterministic, so a caller can predict the fresh address and place it in the emission's own endset (self-targeting), or construct a retraction that nullifies itself. The semantic implications of these recursive cases are not analyzed.
**Why out of scope**: Recursive emission patterns are a separable analysis; substrate primitives are well-defined for them.

### Topic 2: Higher-arity links and active subsets for L_K^{(n)}
The Open Questions section explicitly flags this as future work; L_K and A_K are defined only over arity-3 links.
**Why out of scope**: Already named.

### Topic 3: Coverage collisions between K and R
If a caller chooses K with coverage(K) = coverage(R), tuples emitted as K are classified as retractions by the coverage-equivalence relation, with surprising semantic consequences. This is a discipline-level concern about caller behavior.
**Why out of scope**: The substrate behaves correctly under any caller choice; collision-avoidance is a layered convention.

### Topic 4: Concurrent emissions
The Open Questions section explicitly flags concurrency model and atomicity of Emit vs. Observe.
**Why out of scope**: Already named.

VERDICT: REVISE
