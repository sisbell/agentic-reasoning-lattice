# Review of ASN-0036

## REVISE

### Issue 1: S7c postcondition (c) layers two vacuous conditionals
**ASN-0036, S7c Formal Contract, postcondition (c)**: "When `#E(a) ≥ 2`, the within-subspace ordinal `[E(a)₂, ..., E(a)_δ]` is a non-empty tumbler that lies in `S` whenever all its components are positive, satisfying TA7a's operand precondition `o ∈ S` so that `⊕` and `⊖` are directly applicable."
**Problem**: Two redundant qualifiers stack. (a) The "When `#E(a) ≥ 2`" guard is redundant: S7c's own axiom is `(A a ∈ dom(Σ.C) :: #E(a) ≥ 2)`, so on the precondition domain the guard always holds. (b) The "whenever all its components are positive" antecedent is also redundant: by T4 (HierarchicalParsing), every non-separator component of a T4-valid tumbler is strictly positive, and `E(a)` contains *only* non-separator components — separators delimit fields, not positions within a field. So every component of `E(a)` is unconditionally positive on the precondition domain. The conditional phrasing falsely suggests `dom(Σ.C)` contains addresses where the antecedent could fail.
**Required**: Restate (c) unconditionally. Suggested form: "The within-subspace ordinal `[E(a)₂, ..., E(a)_δ]` is a non-empty tumbler in `S` — every component positive by T4's positive-component constraint — satisfying TA7a's operand precondition `o ∈ S` so that `⊕` and `⊖` are directly applicable." Compare the cleaner phrasing in OrdShiftHom postcondition (c), which writes "satisfies S8a unconditionally" without spurious guards.

### Issue 2: S5 cross-document construction asserts existence of N+1 distinct documents without citation
**ASN-0036, S5 proof, "Cross-document construction"**: "`N + 1` documents `d₁, …, d_{N+1}`, with `M_N(dᵢ) = {vᵢ ↦ a}` ..."
**Problem**: The proof simply names N+1 documents as if they exist for the asking. The Depends list cites T3 (ASN-0034) for distinguishing dⱼ tumblers, but the proof body never specifies tumbler structure for the dⱼ — it leaves implicit how N+1 distinct document identifiers are obtained. Two paragraphs later the within-document construction is similarly terse but at least gives explicit witnesses (`vₖ = [1, k]`). For a Dijkstra-grade existence proof, the witness must be exhibited.
**Required**: Either (a) cite the foundation results that supply N+1 distinct document tumblers — T0(b) (UnboundedLength) and T0(a) (UnboundedComponentValues) of ASN-0034 give an injective map from ℕ into T, so any N+1 distinct tumblers serve — or (b) exhibit explicit witnesses (e.g., `dᵢ = [1, 0, 1, 0, i]` for i = 1, …, N+1, with distinctness from T3 via distinct last components). Without one of these, the construction has the same hand-wave ("such things exist") it asks the reader to verify in the more careful within-document case.

### Issue 3: S8 Postconditions assert subspace preservation as if load-bearing for the singleton decomposition
**ASN-0036, S8 Formal Contract, Postconditions**: "For each run, `shift(aⱼ, k)` preserves the I-address subspace `subspace_I(aⱼ)` — by S7c, the action point of `δ(k, #aⱼ)` falls strictly after the position of `subspace_I(aⱼ)` ..."
**Problem**: For the existence claim S8 actually proves (the singleton decomposition with `nⱼ = 1`), `k` ranges over `{0}` only, and `shift(aⱼ, 0) = aⱼ` by convention — subspace preservation is trivial and S7c is *never invoked*. The S7c-based justification only matters for the auxiliary lemma's `k ≥ 1` branch, which the proof itself notes is "vacuous for the singleton decomposition." The Depends list lifts S7c to a top-level dependency of S8 even though the existence proof does not consume it. This conflates "what would be needed for a coarser decomposition" with "what is needed for what S8 actually proves."
**Required**: Either (a) split the S8 contract into "existence of some decomposition" (which doesn't depend on S7c) and a separate auxiliary claim "any decomposition preserves subspace" (which does), or (b) explicitly mark S7c in the Depends list as "required for the auxiliary lemma; vacuous on the singleton witness." Currently a reader inspecting Depends sees S7c as load-bearing for the existential, when it isn't.

### Issue 4: S5 within-document construction's S2 check cites distinctness "by hypothesis" when it's by construction
**ASN-0036, S5 proof, within-document construction**: "S2 (arrangement functionality): the `vᵢ` are pairwise distinct **by hypothesis**, so each V-position maps to exactly one I-address ..."
**Problem**: There is no hypothesis here — the proof *constructs* `vₖ = [1, k]`. The pairwise distinctness comes from the explicit construction together with T3 (distinct last components → distinct tumblers, which the body does cite). "By hypothesis" mis-attributes the source of the fact and contradicts the explicit construction one paragraph above. The cross-document construction has the same wording in reverse — there the documents *are* taken as distinct by hypothesis since they are unspecified, but the V-positions are not.
**Required**: Replace "by hypothesis" with "by construction (distinct last components, T3)" in the within-document case. Keep "by hypothesis" only for the document distinctness in the cross-document case (and even there, see Issue 2).

## OUT_OF_SCOPE

None — the ASN's Scope section already lists the topics it defers (operations, links, version semantics, enfilade internals) and the Open Questions section captures the remaining design questions (operation preservation of D-CTG/D-MIN, displacement-mechanism invariants, allocation-convention choice of `m` for empty subspaces, subtraction homomorphism conditions, round-trip property). Subspace alignment is correctly relocated to the operations layer via the Remark following S8a.

VERDICT: REVISE
