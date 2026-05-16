# Review of ASN-0047

## REVISE

### Issue 1: K.λ first-link case lacks rigorous T10a-conformance

**ASN-0047, K.λ definition and Allocator hierarchy section**: "the link-prefix base is `t = b_L(d) = [d.0.s_L]` — the link sub-allocator anchor... a virtual allocator predecessor: not itself in `dom(L)`, but the formal starting point for the link allocator under d"

**Problem**: T10a (ASN-0034) defines the allocator tree as a structure of allocators with each non-root allocator carrying a spawning triple `(parent(A), spawnPt(A), spawnParam(A))` where `spawnPt(A) ∈ dom(parent(A))`. The virtual anchor `b_L(d)` is not in any allocator's domain — it has no inc-history. T10a's GlobalUniqueness applies to inc-produced addresses within the allocator tree, not to virtual anchors. The K.λ precondition `ℓ = inc(b_L(d), 1)` cannot directly invoke GlobalUniqueness for `ℓ ∉ dom(L) ∪ dom(C)`. The "two sub-allocators are siblings" claim conflates "siblings in the tumbler sense" with "sibling allocators in T10a's tree". A document `d` at zeros=2 cannot spawn two distinct allocators via the single inc(d, 2) operation (T10a's at-most-once constraint).

**Required**: Either (a) construct b_L(d) as a real T10a allocation output by showing a specific inc chain from d that produces it, demonstrating which allocator owns the spanning event, or (b) introduce an axiom underwriting the existence of the link sub-allocator and its disjointness with the content sub-allocator (parallel to NodeUniqueAllocation, which solves the analogous problem for nodes).

### Issue 2: Foundation-update proposal misplaced

**ASN-0047, Amendments section**: "The foundation should be updated to incorporate D-CTG★ and D-MIN★ (i.e., to drop the link-subspace exemption clauses from ASN-0036's D-CTG and D-MIN)"

**Problem**: Foundation ASNs are verified and stable. Proposing updates to them inside a downstream ASN conflates "this ASN's local extension" with "retrofit the foundation". Similar language appears for L0 ("The foundation should be updated to incorporate this amended L0") and L3.

**Required**: Remove all "the foundation should be updated" language. Treat D-CTG★/D-MIN★/L0/L3 amendments as new properties defined locally and used throughout this ASN's extended state. Foundation modifications are out of this ASN's mandate.

### Issue 3: NodeUniqueAllocation axiom scope is ambiguous

**ASN-0047, NodeUniqueAllocation axiom**: "every K.δ node-allocation event produces an address fresh to the entity set"

**Problem**: Two scope ambiguities. (a) Does the axiom cover the bootstrap node n₀ in Σ₀? The bootstrap is not a K.δ event but a state-initial parameter. The K.δ precondition for IsNode requires `e ∉ E`, and if n₀ is in E₀, no K.δ ever places it. But the axiom's wording doesn't make this distinction. (b) The axiom relies on "any allocator satisfying the namespace property `e ∉ E` suffices" — but this is circular if the namespace property is what the axiom is meant to underwrite. The axiom should state the structural mechanism (Nelson's hierarchical baptism, Gregory's global granfilade, or both as alternative realizations) and clarify which scope it covers.

**Required**: Clarify the axiom's scope: explicitly note that n₀ is a state-initial parameter (not a K.δ event), and state the structural mechanism the axiom presumes (e.g., "all node addresses descend from a single root by a chain of ownership-derived baptism events"). Distinguish the axiom from a tautology.

### Issue 4: "Replacement decomposes into K.μ⁻ + K.μ⁺" claim is overly broad

**ASN-0047, Elementary transitions section**: "replacement — changing which I-address a V-position maps to — decomposes into K.μ⁻ followed by K.μ⁺"

**Problem**: Under K.μ⁻'s admissibility (per-subspace suffix or full clearance), replacement at a non-maximum V-position cannot remove just that position — it requires removing all positions at or after it within the subspace, then re-adding them all. The simple "K.μ⁻ + K.μ⁺" gloss obscures this requirement. As stated, a reader could believe replacement at any position is straightforward.

**Required**: Qualify the claim: "Replacement at the maximum position in a subspace decomposes into a single K.μ⁻ + K.μ⁺ pair; replacement at an interior position requires K.μ⁻ removing the affected suffix followed by K.μ⁺ rebuilding it with the modified mapping." Or provide a worked decomposition example for the interior case.

### Issue 5: K.δ k=1 sub-case admits version-shaped addresses without version semantics

**ASN-0047, K.δ precondition, k=1 sub-case note**: "the relationship between a version `[N, 0, U, 0, D, k]` and its base document `[N, 0, U, 0, D]` is richer than the entity-hierarchy parent(·) operation captures"

**Problem**: K.δ admits k=1 events with t = any previously allocated address. For t = a document d, the result is a "version-shaped" entity at zeros=2 with parent(e) = parent(d) (same user account, not d). The version-to-base lineage is not captured by P8 or any other invariant in this ASN. So a system could create [N, 0, U, 0, D, 5] without [N, 0, U, 0, D, 4] or [N, 0, U, 0, D] ever existing, with no constraint linking them. This admits structural anomalies that contradict the version semantics the ASN gestures toward.

**Required**: Either (a) add a precondition for K.δ with k=1 from a document that the "base" t = [N, 0, U, 0, D] (or some prior version-shaped entity) be in E_doc, or (b) explicitly reject k=1 from documents as inadmissible in this ASN and defer all version creation to a future ASN, or (c) prove that the omission is harmless by showing no invariant relies on the missing constraint.

### Issue 6: K.μ~ decomposition for non-trivial bijections is scattered

**ASN-0047, K.μ~ definition and ExtendedReachableStateInvariants proof**

**Problem**: The argument that K.μ~ with non-trivial π decomposes into K.μ⁻ + K.μ⁺ is spread across (i) the K.μ~ definition's degenerate-case analysis, (ii) the K.μ⁻ admissibility precondition's local derivation, (iii) the S3★ link-subspace fixity argument, and (iv) the ExtendedReachableStateInvariants proof for K.μ~. The reader must assemble: K.μ⁻ does *full content-subspace clearance* (admissible by n'_S = 0), then K.μ⁺ rebuilds with permuted mappings (admissible because intermediate V_{s_C}(d_int) = ∅ trivially satisfies D-CTG/D-MIN, then K.μ⁺ adds positions {[s_C, 1, ..., 1, k] : 1 ≤ k ≤ n} satisfying postconditions). This is not articulated as a single decomposition.

**Required**: Consolidate the K.μ~ decomposition into a single subsection at K.μ~'s definition site, explicitly stating: "for non-trivial π, K.μ⁻ removes V_{s_C}(d) entirely (full clearance, n'_S = 0); K.μ⁺ then adds {π(v) ↦ M(d)(v) : v ∈ V_{s_C}(d)} rebuilding the content subspace." Verify the intermediate state's admissibility once, in one place.

### Issue 7: Worked example does not verify P7a, P3★, or several link invariants

**ASN-0047, Worked example section**

**Problem**: The first worked example verifies J0, J1, J2, J3, J4, P4, P5, P6, P7, P8 at each step but omits P7a (provenance coverage). After step "Insert new content into d₂", the verification should include "P7a: a₃ ∈ dom(C₃) has provenance (a₃, d₂) ∈ R₃". The second worked example (link allocation) verifies several link invariants but omits P3★, L-fin, and explicit P7a checks. ExtendedReachableStateInvariants enumerates a much larger invariant set than the example exercises.

**Required**: Add P7a verification to step 3 of example 1 ("(a₃, d₂) ∈ R₃ — every a ∈ dom(C₃) has provenance"). Add P3★ verification across all steps. Add L-fin verification to step 1 of example 2. Either verify all reachable-state invariants explicitly or annotate which are trivially preserved by frame conditions.

### Issue 8: ShiftPreservation for link-subspace V-positions is invoked but not derived

**ASN-0047, K.μ⁺_L precondition**: "v_ℓ = shift(max(V_{s_L}(d)), 1), extending the contiguous range (D-CTG)"

**Problem**: The K.μ⁺_L precondition uses `shift(max(V_{s_L}(d)), 1)` and relies on shift preserving subspace, depth, and well-formedness. ASN-0036's OrdShiftHom and ShiftPreservation establish these for content-subspace addresses, but the lemmas were stated within a single-subspace context. The extension to s_L = 2 (or general subspace identifiers) requires citing the lemmas' subspace-independence. The ASN does not make this citation.

**Required**: Cite OrdShiftHom (b) for `subspace(shift(v, 1)) = subspace(v)`, and ShiftPreservation/OrdAddS8a for preservation of S8a/S8-depth. Verify these lemmas are stated subspace-independently in the foundation (they are, since `subspace(v) = v₁` is just a projection and δ(n, m) has v₁-position-zero).

### Issue 9: ExtendedReachableStateInvariants proof's composite invariants treatment conflates J0 sequencing

**ASN-0047, ExtendedReachableStateInvariants proof, Class (b)**

**Problem**: J0 is presented as a coupling constraint, and the proof says "At composite boundaries, J0 guarantees every newly allocated content address is placed in some document's arrangement". But J0's formal statement (`(A Σ → Σ', a : a ∈ dom(C') \ dom(C) : (E d, v : d ∈ E'_doc ∧ v ∈ dom(M'(d)) : M'(d)(v) = a))`) is evaluated between initial Σ and final Σ' of the composite. The proof's invocation of J0 "at composite boundaries" is right, but the proof also relies on a specific intra-composite sequencing (K.α before K.μ⁺) for S3 to hold at the intermediate state. This sequencing is necessary but not explicitly required by the coupling constraints.

**Required**: Clarify that valid composites are sequences of elementary transitions where (a) coupling constraints hold between initial and final states, and (b) each intermediate state satisfies the *elementary* preconditions of the next step. The intra-composite sequencing of K.α before K.μ⁺ is enforced by clause (b), not by J0 directly. Make this distinction explicit in the proof.

### Issue 10: Self-containment gaps — `subspace_I`, `subspace`, `origin`, `home`, `fields`, `parent`

**ASN-0047, throughout**

**Problem**: The ASN uses projections from foundation ASNs without local definitions: `subspace_I(a)` (ASN-0036 S7c), `subspace(v)` (ASN-0036), `origin(a)` (ASN-0036 S7), `home(a)` (ASN-0043), `fields(a).E₁` (ASN-0034 T4b), `parent(e)` (introduced here but for entity hierarchy only). Different notations are used inconsistently (`subspace_I(a)` vs `fields(a).E₁`). For an ASN that defines new state components and amends existing invariants, the reader benefits from a brief notational summary or formal definition citation.

**Required**: Add a "Notation" subsection near the top of the ASN listing the projection functions used and their sources (or, where introduced here, their definitions). Use the citations consistently — pick one of `subspace_I(a)` or `fields(a).E₁` and use it throughout, not both.

## OUT_OF_SCOPE

### Topic 1: Withdrawal mechanism for links
**Why out of scope**: The ASN flags this as an open question. Nelson's tombstoning design (links transition to "not currently addressable" status while preserving permanent address) requires a status-flag mechanism outside K.μ⁻'s contraction contract. The precise design is correctly deferred.

### Topic 2: Version-management semantics
**Why out of scope**: The K.δ k=1 sub-case admits version-shaped addresses structurally, but the semantic contract relating a version to its base document (content-allocator sharing, lineage invariants, provenance flow) is outside this ASN's transition model. Flagged as open question.

### Topic 3: Concurrent allocation across actors
**Why out of scope**: Whether K.α, K.δ, K.λ can be performed concurrently by distinct actors without coordination, and what serialization is required, are deferred to a concurrency model. Flagged as open question.

### Topic 4: Authority and authorization
**Why out of scope**: Listed in the ASN's Scope exclusions. Who can perform which transitions is an access-control concern orthogonal to the transition model.

### Topic 5: Atomicity of composites
**Why out of scope**: Listed in the ASN's Scope exclusions. Whether composite transitions are atomic from an observer's perspective is an implementation/concurrency concern.

### Topic 6: Link-allocation failure due to address space exhaustion
**Why out of scope**: T0(b) (ASN-0034) guarantees unbounded length and T0(a) guarantees unbounded sibling values — so the abstract specification has no address exhaustion. Implementation-level limits are deferred. Flagged as open question.

VERDICT: REVISE
