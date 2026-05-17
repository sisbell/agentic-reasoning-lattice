# Review of ASN-0047

## REVISE

### Issue 1: NodeLineage axiom not formalized as invariant or precondition

**ASN-0047, NodeLineage section**: "*Scope.* The axiom covers every node in E at every reachable state, including ... (ii) every node added by a K.δ node-allocation event (where the protocol mechanism establishes prefix descent from n₀ at the moment of allocation)."

**Problem**: NodeLineage is presented as an axiom asserting `(A e ∈ E : IsNode(e) : n₀ ≼ e)`, but:
- It is **not** listed in the per-state theorem `ExtendedReachableStateInvariants` (which enumerates 30 conjuncts but omits NodeLineage).
- It is **not** a precondition of K.δ case (i), which requires only `ValidAddress(e) ∧ IsNode(e) ∧ e ∉ E` and `NodeUniqueAllocation` for freshness.
- The protocol mechanism "establishes" it externally, but the ASN's formal machinery contains no connection between K.δ and the n₀-prefix requirement.

A K.δ event allocating a node `e = [7, 3]` (no n₀ prefix, fresh) satisfies every stated precondition and produces a state violating NodeLineage. Nothing in the ASN's proof or definitions rules this out.

**Required**: Either (a) add `n₀ ≼ e` to K.δ case (i)'s explicit precondition list alongside `ValidAddress(e) ∧ IsNode(e) ∧ e ∉ E`, or (b) add NodeLineage as a conjunct of `ExtendedReachableStateInvariants` with an explicit preservation argument that cites the protocol-established `n₀ ≼ e` at every K.δ node event.

### Issue 2: L14a from ASN-0043 contradicted without amendment

**ASN-0047, K.μ⁺_L definition**: "*Effect:* `M'(d) = M(d) ∪ {v_ℓ ↦ ℓ}`" where `ℓ ∈ dom(L)`.

**Problem**: ASN-0043's L14a (NonTranscludability) states: `(A d, v : v ∈ dom(Σ.M(d)) : Σ.M(d)(v) ∉ dom(Σ.L))` — no V-position may map to a link address. K.μ⁺_L's effect directly produces `M'(d)(v_ℓ) = ℓ ∈ dom(L)`, violating L14a as stated. The ASN amends S3 → S3★ explicitly but is **silent** on L14a. The string "L14a" does not appear in the ASN. CL-OWN appears to be the intended replacement (restricting link-subspace mappings to home-document links) but the ASN does not say so.

**Required**: Add an explicit amendment paragraph stating that L14a is superseded by CL-OWN (or by S3★'s link clause), with the same form as the other amendments (K.α amendment, K.μ⁺ amendment, K.μ⁻ amendment). The amendment must justify why dropping L14a's universal constraint is consistent with the design intent.

### Issue 3: K.δ case (i) precondition does not establish lineage

**ASN-0047, K.δ case (i)**: "The only structural constraints are ValidAddress(e) ∧ IsNode(e) ∧ e ∉ E"

**Problem**: This is incomplete given the NodeLineage axiom (Issue 1). The K.δ case (i) handles n₀ at the bootstrap but says nothing about subsequent node allocations being constrained to descend from n₀.

**Required**: K.δ case (i)'s precondition list must include `n₀ ≼ e` (either explicitly or by reference to NodeLineage as a precondition).

### Issue 4: K.μ⁻ undefined when M(d) is empty

**ASN-0047, K.μ⁻ definition**: "`dom(M'(d)) ⊂ dom(M(d)) ∧ (A v : v ∈ dom(M'(d)) : M'(d)(v) = M(d)(v))`"

**Problem**: The strict subset `⊂` requires `|dom(M'(d))| < |dom(M(d))|`, so if `dom(M(d)) = ∅`, no valid post-state exists and K.μ⁻ is undefined. This is implicit but should be stated. More importantly, the per-subspace admissibility precondition quantifies over `(A S : V_S(d) ≠ ∅ : ...)`, which is vacuously true on empty M(d), giving the impression K.μ⁻ is admissible there.

**Required**: Add an explicit precondition `dom(M(d)) ≠ ∅` to K.μ⁻, or restate the strict-subset clause to make this explicit.

### Issue 5: "Completeness" claim is informal

**ASN-0047, "Extended completeness"**: "Seven elementary transition kinds — K.α, K.δ, K.λ, K.μ⁺, K.μ⁺_L, K.μ⁻, K.ρ — plus the distinguished composite K.μ~, are complete for the five-component state (C, L, E, M, R)."

**Problem**: The notion of "complete" is not defined. The justification — "Any modification to a finite partial function decomposes into additions and removals" — is true for arbitrary modifications, but K.μ⁻'s admissibility precondition forbids interior removals. So the elementary set is complete only with respect to *invariant-preserving* state transitions, not all state changes. This restriction is not stated, and the argument doesn't establish that every invariant-preserving transition can be decomposed into these primitives (only that replacement at interior positions decomposes into K.μ⁻ + K.μ⁺ via suffix removal and rebuild).

**Required**: Either prove the completeness claim formally (define the class of transitions covered and show every transition in the class decomposes into a sequence of the seven primitives plus K.μ~), or weaken the claim to a statement of what it actually establishes (e.g., "every example transition we analyze decomposes into elementary kinds").

### Issue 6: Property table omits several introduced axioms and invariants

**ASN-0047, "Properties Introduced" table**: 

**Problem**: The following are introduced as axioms or invariants in the body but missing from the property table:
- NodeLineage axiom (entirely absent).
- SubAllocatorAxiom (only "Allocator hierarchy" is in the table, which is the hierarchy structure, not the axiom).
- D-CTG★, D-MIN★, D-SEQ★ — referenced in `ExtendedReachableStateInvariants` and K.μ⁻ amendment but not given separate table entries (despite being explicitly named per-subspace strengthenings).
- ExtendedTransitionInvariants theorem.
- L1b restated.

**Required**: Add table entries for NodeLineage, SubAllocatorAxiom, D-CTG★, D-MIN★, D-SEQ★, and ExtendedTransitionInvariants. The table is the canonical inventory; missing entries make the per-state theorem harder to verify against introduced material.

### Issue 7: Convoluted K.μ~ redundancy argument

**ASN-0047, "Link-subspace fixity under K.μ~ (redundancy remark)"**: A multi-paragraph argument shows the link-subspace identity precondition is structurally compelled by S3★ + CL-UNIQ at the output state.

**Problem**: The argument uses CL-UNIQ at the *output state*, which is established inductively assuming the K.μ~ precondition holds. The chain reads: "the precondition holds because removing it would violate CL-UNIQ at the output, but CL-UNIQ at the output is preserved precisely because the precondition holds." This is consistent (the argument is a structural consistency check, not a derivation), but the recursive reliance on CL-UNIQ at the post-state is not explicitly disentangled. A reader cannot easily verify whether the redundancy argument is independent of the inductive proof or a circular justification.

**Required**: Restructure the redundancy argument to clearly separate "the precondition is stipulated" from "any K.μ~ violating only the weaker subspace-preservation clause would produce a state inconsistent with the per-state invariants" — making explicit that CL-UNIQ is consumed as an established invariant of all reachable states (the inductive hypothesis), not as a property of the K.μ~ output that depends on the precondition. Alternatively, drop the redundancy argument and present the identity clause as a stipulation justified by Nelson's "permanent order of arrival" semantics.

### Issue 8: Worked example does not verify J1'★ for the link-allocation steps

**ASN-0047, "Worked example: link allocation and arrangement"**: Each step lists verified invariants but J1'★ is never explicitly checked.

**Problem**: J1'★ is a coupling constraint and one of the load-bearing per-composite invariants in `ValidComposite★`. The worked example claims comprehensive coverage but J1'★ verification is implicit ("frame-preserved invariants" suggests no R change, so J1'★ is vacuous — but this should be stated).

**Required**: For each step in both worked examples, explicitly verify J1'★ (likely vacuous in most steps because R is unchanged, but state this).

### Issue 9: Decomposition of K.μ~ Case 1 conflates two distinct subcases

**ASN-0047, "Decomposition of K.μ~"**: "Case 1: π = id (zero elementary steps). When π is the identity on dom(M(d)) — whether because dom(M(d)) = ∅ (empty bijection) or because π = id on a non-empty domain — K.μ~ produces M'(d) = M(d) and expands into *zero elementary steps*."

**Problem**: The case "dom(M(d)) = ∅" and "π = id on a non-empty domain" are merged into Case 1. But "π = id on a non-empty domain" is K.μ~'s degenerate trivial application — a no-op. The ASN later says "We do not restrict π to non-identity bijections" but doesn't define what K.μ~ with π = id on non-empty M(d) *does* — it can't decompose into K.μ⁻ + K.μ⁺ (K.μ⁻'s strict-contraction precondition would fail). The "zero elementary steps" resolution is correct but glosses over whether such a K.μ~ instance is even meaningful as an elementary transition or whether it should be excluded as ill-formed.

**Required**: Clarify whether "K.μ~ with π = id and non-empty M(d)" is a valid elementary instance (a no-op, equivalent to taking zero elementary steps) or whether the K.μ~ definition implicitly excludes π = id. The ASN's choice to subsume it under "zero elementary steps" is acceptable but should be stated as a definitional choice with rationale.

### Issue 10: The "Decomposition of K.μ~" forward references CL-UNIQ before establishing it inductively

**ASN-0047, "Decomposition of K.μ~", Case 2 consistency check**: "[...] forcing π = id throughout."

**Problem**: The Case 2 argument invokes "the K.μ~ precondition [link-subspace identity clause]" which depends on CL-UNIQ at the output state for the redundancy derivation. CL-UNIQ is established later in the document under "Link-subspace ownership". The forward reference is not flagged, and the order of presentation makes the dependency hard to track.

**Required**: Either reorder the sections so CL-UNIQ is established before the K.μ~ decomposition, or add a forward-reference note (parallel to the K.μ⁻/D-CTG★/D-MIN★ forward-reference note) acknowledging the citation.

## OUT_OF_SCOPE

### Topic 1: Specific protocol mechanism for node allocation

**Why out of scope**: The ASN deliberately leaves the node-allocation protocol unspecified (citing two equivalent realizations: Nelson's baptism, Gregory's granfilade). The protocol mechanism itself is implementation territory; the axiom-level abstraction (NodeUniqueAllocation) is the appropriate vehicle. Implementation specifics belong in a future implementation-binding ASN.

### Topic 2: Link withdrawal / tombstoning mechanism

**Why out of scope**: The ASN explicitly defers this to an open question, noting that D-CTG★ prevents single-interior-link withdrawal and that Nelson's tombstoning semantics requires a separate mechanism (status flag, retraction link, or similar). A future withdrawal-mechanism ASN should specify this — the present ASN's K.μ⁻ correctly admits only suffix removals.

### Topic 3: Detailed version semantics under K.δ k = 1

**Why out of scope**: The ASN's "Deferred semantics" paragraph explicitly defers richer version semantics — version graph acyclicity, base-to-version content allocator linkage, provenance flow between versions, etc. — to a future version-management ASN. The present ASN admits k = 1 events as structurally well-formed without legislating their richer interpretation, and this scope boundary is deliberate.

### Topic 4: Per-document link arity uniformity

**Why out of scope**: The ASN narrows L3 to fixed arity 3 locally but preserves the foundation's `N ≥ 3` generality. Whether different documents (or different links within a document) may use different arities is left for future extensions. The current narrowing is sufficient for the transition model.

VERDICT: REVISE
