# Review of ASN-0093

## REVISE

### Issue 1: ValidAddress predicate not tied to T4-validity

**ASN-0093, M0 invariant and K.σ precondition**: M0 states `(A d ∈ dom(M) :: ValidAddress(d) ∧ zeros(d) = 2)`. K.σ's precondition uses `ValidAddress(d)`. The discharge matrix's K.σ row says "precondition pins `ValidAddress(d) ∧ zeros(d) = 2`". In contrast, the L1c/C1c chain exhibitions reference "T4-valid(s)" and rely on T10a's per-step admissibility constraints (which assume T4-validity).

**Problem**: The substrate never explicitly identifies `ValidAddress` with the foundation's T4-validity (ASN-0034 T4). A reader must infer the identification to follow the chain exhibitions and the L14 derivation (T7 requires T4-valid operands).

**Required**: Add an explicit identification `ValidAddress(d) ≡ d satisfies T4 (HierarchicalParsing, ASN-0034)` at first use — either near M0's introduction or in the state model section — and use one term consistently throughout.

### Issue 2: ChainMembershipForOrigin K.σ step proof gap

**ASN-0093, ChainMembershipForOrigin proof, K.σ(d_new) case**: "For the freshly registered `d_new`, the intersection sets are empty (no content/link has yet been emitted with `origin(·) = d_new`), so both inclusions hold vacuously at `d_new` in `Σ'`."

**Problem**: "No content/link has yet been emitted with origin(·) = d_new" is an informal temporal appeal. The formal derivation requires citing C2 (resp. L1a) at Σ together with K.σ's precondition `d_new ∉ dom(M)`. The proof as written elides these load-bearing citations.

**Required**: Spell out the derivation explicitly. By IH on C2 at Σ, every `a ∈ dom(C(Σ))` satisfies `origin(a) ∈ dom(M(Σ))`. By K.σ's precondition, `d_new ∉ dom(M(Σ))`. Therefore `origin(a) ≠ d_new` for every `a ∈ dom(C(Σ))`. Since `C` is in frame, `dom(C(Σ')) ∩ {a' : origin(a') = d_new} = ∅ ⊆ A_C(d_new)`. Analogous derivation for the L-clause via L1a.

### Issue 3: "T10a chain-lemma applicability" remark imprecise on T10a.4 dependency

**ASN-0093, "Remark — T10a chain-lemma applicability"**: "the proofs in ASN-0034 confirms that they depend only on per-step structure of an `inc(·, 0)` chain together with T4-validity preservation (via TA5(c) and T10a.4)".

**Problem**: T10a.4 (T4PreservationUnderDiscipline) explicitly requires the chain to be embedded in T10a's allocator tree — its proof inducts on allocator tree depth with a strengthened hypothesis over `dom(A)`. The substrate's chains are not tree-embedded (ChainDiscipline explicitly disclaims this). So T10a.4 cannot be directly invoked for substrate chains; only T10a.4's *conclusion* (chain-wide T4-validity) can be re-established for substrate chains, via TA5a (IncrementPreservesT4) applied per-step from FirstEmission's T4-valid starting point. The prose "(via TA5(c) and T10a.4)" reads as if T10a.4 directly applies, masking the substrate's actual mechanism.

The same imprecision recurs in the sentence "None invokes ... the tree-embedding structure": T10a.8 transitively invokes tree-embedding through T10a.4 in ASN-0034, even though T10a.8's own proof body does not.

**Required**: Clarify that the substrate provides T10a.4's conclusion (T4-validity of chain elements) via TA5a applied inductively from the T4-valid first emission, not by invoking T10a.4 directly. Suggested phrasing: "T4-validity preservation via TA5a applied per-step from the T4-valid first emission (FirstEmission's structural form `[d.0.s_C.1]` / `[d.0.s_L.1]`), independently establishing T10a.4's conclusion without requiring tree-embedding".

## OUT_OF_SCOPE

The substrate's Scope section and Open Questions already document these as deferred:

### Topic 1: Arrangement mutation (K.μ family)
M(d) = ∅ throughout this layer; extension is deferred.

### Topic 2: Entity stratification (E_node/E_account/E_doc)
The E_doc → dom(M) downgrade is the substrate's factoring choice.

### Topic 3: Provenance recording (Σ.R, K.ρ)
No provenance relation at this layer.

### Topic 4: Link withdrawal / tombstoning
L12 enforces immutability; retraction deferred.

### Topic 5: Higher-arity links (N > 3)
L3 narrowed to fixed-three at this substrate.

### Topic 6: Document address discipline (hierarchical baptism)
K.σ admits any T4-valid `zeros = 2` tumbler.

### Topic 7: Concurrent emissions
SequentialTransitionAxiom commits to atomic, sequential transitions.

### Topic 8: Sub-allocator stratification beyond A_C(d) and A_L(d)
SubAllocatorAxiom commits to two sub-allocators per document.

VERDICT: REVISE
