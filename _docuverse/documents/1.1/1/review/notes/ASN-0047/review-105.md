# Review of ASN-0047

This review focuses on the most substantive structural and proof issues. The ASN is large and well-organized, but several issues require correction before downstream ASNs can rely on it.

## REVISE

### Issue 1: NodeUniqueAllocation clause (c) — structural mismatch

**ASN-0047, NodeUniqueAllocation axiom**: "Every K.δ node-allocation event...produces an address satisfying two conditions: (a) Freshness:...; (b) Bootstrap lineage:.... A third clause anchors the registry's initial state: (c) Bootstrap registry seeding: `n₀` inhabits the node-allocation registry's tracked domain at `Σ₀`..."

**Problem**: Clauses (a) and (b) commit *what every K.δ event produces*. Clause (c) commits *initial-state registry membership of n₀* — n₀ has no K.δ event. The clause is being smuggled into an event-based axiom to handle the bootstrap discharge in K.δ case (ii) k = 2 with operand t = n₀. The axiom as written is structurally incoherent: an event-based universal cannot contain an initial-state existential.

**Required**: Split into two axioms — one over K.δ node-allocation events (clauses a and b), one as an initial-state commitment (clause c). Or reformulate as a uniform registry property that the K.δ discharge can cite directly.

### Issue 2: SubAllocatorAxiom — T10a-membership of A_C(d), A_L(d) not committed

**ASN-0047, SubAllocatorAxiom**: Four sub-clauses (Subspace, FirstEmission, Namespace, Disjointness).

**Problem**: The K.α and K.λ subsequent-emission discharges invoke "T10a's GlobalUniqueness on the inc chain." For this to be sound, A_C(d) and A_L(d) must be T10a-conforming allocators whose subsequent emissions are tracked by T10a's discipline. SubAllocatorAxiom commits the first emission and the namespace structure, but does not explicitly commit that A_C(d) and A_L(d) are T10a allocators from the second emission onward. The L1c paragraph asserts this as a side remark ("T10a's full discipline applies only to subsequent emissions on the activated A_L(d) frontier"), but this is not part of the axiom. The axiom's load-bearing role in S4's discharge for subsequent emissions depends on T10a-membership that the axiom does not state.

**Required**: Add a sub-clause to SubAllocatorAxiom committing that A_C(d) and A_L(d) are T10a-conforming allocators (activated by the entity-allocation event for d, with subsequent emissions governed by T10a's GlobalUniqueness on the sibling-increment chain).

### Issue 3: K.μ⁻ admissibility clause (2) — internal contradiction

**ASN-0047, K.μ⁻ amendment, clause (2)**: "*Strict contraction (consequence of the whole-arrangement effect clause `dom(M'(d)) ⊂ dom(M(d))`, not an additional precondition).*..."

**Problem**: Clause (2) is listed in the precondition slot but labeled as "not an additional precondition." The text then says "The reading of clause (2) is therefore *informational*..." This is internally contradictory: a clause is either a precondition (must be verified before the operation fires) or it isn't. Listing a consequence as a precondition and then disclaiming it as informational creates a structural ambiguity — a downstream consumer cannot tell whether clause (2) is load-bearing.

**Required**: Either remove clause (2) from the precondition list (record the per-subspace location of strict contraction as a consequence in a Postconditions paragraph), or commit to it as a precondition the operation must verify.

### Issue 4: K.δ case (ii) k = 0 — frontier requirement implicit

**ASN-0047, K.δ case (ii) k = 0**: "`t ∈ E ∧ ¬IsNode(t) ∧ parent(t) = parent(e) ∧ zeros(t) = zeros(e)`."

**Problem**: For K.δ k = 0 to discharge `e ∉ E` via T10a's GlobalUniqueness, t must be the frontier of the sibling allocator. If t is a non-frontier emission (some earlier sibling), then inc(t, 0) was already done, and its output is already in E — freshness fails. The precondition doesn't enforce frontier-ness explicitly. The discharge prose says "T10a GlobalUniqueness on the inc-chain delivers `e ∉ E` directly," but this works only when t is the frontier. A reader has to infer this from T10a's per-(t, 0) uniqueness.

**Required**: Either state the frontier requirement as part of the precondition (e.g., "t = max{t' ∈ E : parent(t') = parent(e) ∧ zeros(t') = zeros(t)}"), or make the discharge argument explicit about why non-frontier t cannot produce a fresh e.

### Issue 5: K.δ k = 1 — parent-allocator relationship not stated

**ASN-0047, K.δ case (ii) k = 1 discharge**: "...the T10a T2 spawn step that activates `A_v(t)`... The spawnPt premise is discharged by K.δ k = 1's precondition `t ∈ E_doc`, which places `t` in `dom(A_doc(parent(t)))` — the document sub-allocator under t's account that minted t."

**Problem**: The discharge presupposes that the *parent allocator* of A_v(t) in T10a's allocator tree is A_doc(parent(t)). This relationship — parent_allocator(A_v(t)) = A_doc(parent(t)) — is essential for T10a T2 admissibility but is only implicit. The reader must reconstruct it from "t was minted by A_doc(parent(t))" and "A_v(t) is t's version sub-allocator." For a verification proof this implicit chain is brittle.

**Required**: Explicitly state the parent-allocator relationship in T10a's allocator tree (e.g., "A_v(t) is a child of A_doc(parent(t)) in T10a's allocator tree, spawned by this K.δ event with spawnPt = t and spawnParam = 1").

### Issue 6: K.μ⁺ amendment frame omits L' = L

**ASN-0047, K.μ⁺ amendment**: The amendment adds the content-subspace restriction but does not restate the frame.

**Problem**: K.μ⁺ is defined in the four-component setting with frame "C' = C; E' = E; ...; R' = R" — no L. In the extended state, L exists, and K.μ⁺ does not modify it, so the frame should explicitly include L' = L. Compare K.μ⁺_L which states "C' = C; L' = L; E' = E; ...; R' = R" explicitly. K.μ⁻ in the extended state has the same gap (its original frame predates L). Without the explicit frame conjunct, P3's L-clause (dom(L) ⊆ dom(L')) is discharged for K.μ⁺ only implicitly.

**Required**: State the extended-state frame for K.μ⁺ and K.μ⁻ explicitly, including L' = L. The frame is what discharges P3's L-monotonicity conjunct at these transitions.

### Issue 7: Worked example: interior content replacement — composite definition unclear

**ASN-0047, Elementary transitions, replacement description**: "*Replacement* — changing which I-address a V-position maps to — is the named compound K.μ⁻ + K.μ⁺..."

**ASN-0047, Worked example: interior content replacement**: Uses K.μ⁻ + K.α + K.μ⁺ + K.ρ (four elementary steps).

**Problem**: The elementary-transitions section says replacement is "K.μ⁻ + K.μ⁺" (two-step), but the worked example for interior replacement uses four steps. The two-step form holds only for *transcluded replacement* (the new value is already in dom(C)); fresh-content replacement requires K.α and K.ρ in addition. The distinction is buried in the worked example rather than being made at the definition site.

**Required**: At the elementary-transitions section, state both forms explicitly: transcluded replacement (K.μ⁻ + K.μ⁺, two steps) and fresh-content replacement (K.α + K.μ⁻ + K.μ⁺ + K.ρ or K.μ⁻ + K.α + K.μ⁺ + K.ρ, four steps).

### Issue 8: D-SEQ★ forward reference in K.μ⁻ amendment

**ASN-0047, K.μ⁻ amendment**: "the admissible removal pattern applies *per-subspace* under the D-SEQ★ enumeration `V_S(d) = {[S, 1, ..., 1, k] : 1 ≤ k ≤ n_S}`."

**Problem**: D-SEQ★ is defined several paragraphs after the K.μ⁻ amendment (after D-CTG★/D-MIN★/S8★ definitions). The K.μ⁻ amendment uses D-SEQ★ before it is defined. This forward reference within a single document section signals accretion — the K.μ⁻ amendment was likely written before D-SEQ★ was added, and the reference was inserted without reorganizing the text.

**Required**: Reorganize the *Amendments to existing transitions* section so that D-CTG★, D-MIN★, S8★, and D-SEQ★ are defined *before* the K.μ⁻ amendment that consumes them.

### Issue 9: ExtendedReachableStateInvariants — summary verification

**ASN-0047, ExtendedReachableStateInvariants proof**: Class (a) verification proceeds in summary form, e.g., "K.α, K.δ, K.ρ hold M in frame; K.μ⁺ amendment's preconditions on new V-positions..."

**Problem**: For an invariant theorem covering ~25 per-state invariants and 7 elementary transitions, the proof structure should make explicit which invariant is verified at which transition. The current summary style leaves the reader to reconstruct the verification grid. Several invariants get only one-line treatments that elide non-trivial verification (e.g., the L1b derivation invokes "T10a.8 (UniformSiblingZeroCount, ASN-0034)" without re-stating what T10a.8 gives).

**Required**: Either provide a verification matrix (invariant × transition) showing the preservation argument for each cell, or for each transition provide a complete preservation argument covering all Class (a) invariants. The current summary is acceptable as an outline but not as a proof.

### Issue 10: Accretion meta-prose

**ASN-0047, multiple sections**: The ASN contains significant meta-prose around forward references, terminology clarification, and defensive justification:

- "We refer to the full-clearance form as the *canonical* expansion in the sense of universal applicability, not exclusivity" (K.μ~ decomposition) — meta-prose about the word "canonical."
- "The reading of clause (2) is therefore *informational* (locating which subspace(s) carry the contraction) rather than a separate precondition to verify" (K.μ⁻ amendment) — explaining why a precondition isn't a precondition.
- "The check is recorded here for clarity, not because the composite would fail if it did not hold" (worked example) — defensive justification of a verification step.
- "All subsequent references to D-CTG and D-MIN in this ASN denote the amended (per-subspace) forms D-CTG★ and D-MIN★" — meta-prose about naming convention.
- Multiple "see X below" forward references (K.μ~ decomposition, K.μ⁻ amendment, J4 fork, etc.).

**Problem**: These patterns accumulate over revision cycles. A precise reader has to skip past meta-prose to reach the load-bearing claims, and meta-prose suggests prior findings were addressed by adding explanation rather than by reorganizing.

**Required**: Remove meta-prose. The "canonical" wording is fine to use; the parenthetical explanation is not needed. Clause (2) is either a precondition or it isn't — pick one. "See X below" cross-references compress to a single primary site that defines, with downstream uses citing without re-deferring.

### Issue 11: K.μ~ "bijectively into"

**ASN-0047, K.μ~ link-subspace fixity proof, Step 1**: "The restriction `π|_{dom_L(M(d))}` therefore maps dom_L(M(d)) bijectively into dom_L(M'(d))."

**Problem**: A bijection is by definition surjective onto its codomain. "Bijectively into" is awkward — the function is bijective from dom_L(M(d)) onto dom_L(M'(d)).

**Required**: Change "bijectively into" to "bijectively onto" (both occurrences in Step 1).

### Issue 12: SequentialTransitionAxiom — composite-boundary invariants and intermediate-state observability

**ASN-0047, SequentialTransitionAxiom**: "Each transition is an atomic, uninterruptible event...transitions are totally ordered."

**ASN-0047, ExtendedReachableStateInvariants**: Distinguishes "elementary per-state" invariants (always hold) from "composite-boundary" invariants (hold at composite endpoints, may transiently fail at intermediate states).

**Problem**: SequentialTransitionAxiom commits *elementary transitions* to atomicity, not composites. Between elementary steps within a composite, the intermediate state is a real, observable state under SequentialTransitionAxiom. The theorem claims certain invariants (P4★, P4a, P7a) may transiently fail at these intermediate states — but a state machine that exposes real intermediate states where a stated invariant fails is a state machine that violates the invariant. The ASN does not commit composite atomicity, so the "composite-boundary" qualifier on P4★/P4a/P7a degrades them from true invariants to operationally-restored properties.

**Required**: Either commit composite atomicity (intermediate states are not observable) as part of SequentialTransitionAxiom, or weaken the language: P4★/P4a/P7a are not "invariants" in the strict sense — they are "post-composite invariants" or "transactionally restored properties," and the theorem statement should reflect this.

## OUT_OF_SCOPE

### Topic 1: Node-allocation registry protocol mechanics

**Why out of scope**: The ASN's *Open Questions* section already lists this. NodeUniqueAllocation abstracts over the registry's protocol, persistence model, and concurrency discipline. Specifying the registry mechanism (Nelson's hierarchical baptism, Gregory's granfilade-with-query-and-increment) is operational and belongs to a future ASN if needed at all.

### Topic 2: Link-withdrawal mechanism (tombstoning)

**Why out of scope**: Listed in *Open Questions*. K.μ⁻ admits only per-subspace suffix removal under D-CTG★/D-MIN★, which precludes interior link withdrawal. A separate mechanism (tombstone, status flag) reconciling Nelson's withdrawal design with D-CTG★ is a future ASN.

### Topic 3: Fork inheritance of source's link subspace

**Why out of scope**: Listed in *Open Questions*. J4's fork copies the source's content subspace (transclusion) but starts the new document's link subspace empty. Whether to inherit links is a downstream design question, not a defect in ASN-0047.

### Topic 4: Account-level depth-1 tumbler extension

**Why out of scope**: Listed in *Open Questions*. K.δ k = 1 is restricted to `t ∈ E_doc` (versions are documents only). Admitting account-level k = 1 is a downstream policy question.

### Topic 5: Cross-document contraction effects on link discoverability

**Why out of scope**: Listed in *Open Questions*. Link discoverability is a query-side property, governed by future query-model ASNs.

### Topic 6: Concurrency and serialization guarantees

**Why out of scope**: The Scope block explicitly excludes "operation atomicity and concurrency." SequentialTransitionAxiom commits a single total order; multi-node concurrency belongs to a future replication ASN.

VERDICT: REVISE
