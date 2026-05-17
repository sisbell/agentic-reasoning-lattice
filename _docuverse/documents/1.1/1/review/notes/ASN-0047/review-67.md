# Review of ASN-0047

## REVISE

### Issue 1: TA5/T10a conflation in ghost-base versioning Step 3 counterfactual

**ASN-0047, "Worked example: ghost-base document versioning", Step 3 counterfactual**: "*T10a-side rejection.* T10a's GlobalUniqueness (ASN-0034) governs the inc operator: for any `(t, k)` pair with `t ∈ T` and `k ∈ {0, 1, 2}`, the address `inc(t, k)` is uniquely determined and constitutes a single allocation event at the tumbler-allocation layer."

**Problem**: This contradicts the K.δ definition's own claim. The K.δ ghost-operand discussion explicitly says: "T10a's GlobalUniqueness does *not* underwrite `e ∉ E`: T10a governs inc events whose operand lies in some T10a allocator's domain, and a ghost operand is by stipulation outside every entity allocator's domain. ... TA5's role in this sub-case is purely structural, naming which address to check."

Additionally, "inc(t, k) is uniquely determined" is a property of TA5 (inc is defined as a function), not of T10a's GlobalUniqueness (which is about distinct allocation events producing distinct addresses). The actual rejection mechanism for the counterfactual is: TA5 supplies determinism → the candidate is the same address e₁; K.δ's `e ∉ E` precondition fails → rejection. There is only one guardrail (K.δ precondition), not two.

**Required**: Revise Step 3 to attribute determinism to TA5 (not T10a's GlobalUniqueness), drop the "T10a-side rejection" framing for the ghost-operand case (it contradicts the K.δ definition), and replace "two guardrails" with a clear single-mechanism account: "TA5 determinism + K.δ's `e ∉ E` precondition." The "Composite reading" paragraph similarly needs revision.

### Issue 2: SubAllocatorAxiom's operational-vs-structural tension is acknowledged but underspecified

**ASN-0047, "Allocator hierarchy under documents"**: "The two sub-allocators ... are *not* 'sibling allocators in T10a's tree' in the spawning-event sense — T10a's at-most-once constraint precludes a single spawning event yielding both. Their disjointness and existence are axiomatized separately (SubAllocatorAxiom below), not derived from T10a's spawning discipline."

**Problem**: The axiom is necessary, but the relationship to T10a's `allocated(s)` and `Act(s)` predicates isn't specified. T10a's GlobalUniqueness depends on allocators being tracked in `Act(s)` with proper spawning events. If b_C(d) and b_L(d) head two independent allocator frontiers that aren't single-event-spawned under T10a, then T10a's machinery (Act(s), parent(A), spawnPt(A), allocated(s)) doesn't cleanly track them. Subsequent appeals to T10a's GlobalUniqueness for subsequent allocations within these frontiers ("T10a underwrites every subsequent emission") assume each sub-allocator is itself a T10a-conforming chain, but the bootstrap event that activates each sub-allocator isn't specified as a T10a (T2) transition.

**Required**: Either specify how SubAllocatorAxiom maps onto T10a's `Act(s)`/spawning machinery, or explicitly state that SubAllocatorAxiom extends T10a with "virtual spawning events" that activate the two sub-allocators outside T10a's (T2) shape. The current treatment leaves an implicit assumption that "everything works out" without making the lift explicit.

### Issue 3: Inconsistency in T10a applicability to ghost operands

**ASN-0047, K.δ ghost-operand discussion**: "ghost operand is by stipulation outside every entity allocator's domain" → T10a doesn't apply.

**ASN-0047, "Worked example: ghost-base document versioning", initial state**: "We take `T₆` (T10a's universe of allocated tumblers) to include `t` — the address has been issued at the tumbler-allocation layer (so T10a's GlobalUniqueness governs subsequent inc operations on it)..."

**Problem**: The two statements use different scopes of "T10a's domain." The K.δ definition uses "entity allocator's domain" to exclude ghosts; the worked example places the ghost in "T10a's universe of allocated tumblers." The reader cannot tell whether T10a's at-most-once spawning constraint applies to (ghost_operand, k) pairs. The worked example then says T10a does govern subsequent inc operations on ghost t, but K.δ says T10a doesn't underwrite freshness for K.δ events with ghost operand. These are confusable; clarify whether T10a's universe contains ghosts and what T10a guarantees on them.

**Required**: Distinguish "T10a's universe of allocated tumblers" from "an entity allocator's domain in E" with named predicates, and state which T10a properties apply to ghost operands. Reconcile the K.δ definition and the worked example's framing.

### Issue 4: Convention s_C = 1, s_L = 2 is treated as conventional but is structurally load-bearing

**ASN-0047, "Allocator hierarchy under documents"**: "under the canonical subspace convention `s_C = 1`, `s_L = 2`, `b_C(d) = inc(d, 2)` ... and `b_L(d) = inc(b_C(d), 0)`"

**Problem**: The inc-chain `d → b_C(d) → b_L(d)` exhibited here requires `s_C = 1` and `s_L = 2` precisely. Under TA5(d), inc(d, 2) appends `.0.1` with terminal 1, which is s_C only if s_C = 1. For other subspace identifiers (e.g., s_C = 3), the inc-chain would require additional sibling-increment steps to reach the desired terminal value. The ASN treats this as "conventional" but the structural producibility argument (cited by L1c reconciliation) depends on the convention.

**Required**: State explicitly that the structural producibility derivation is *parametric* on the convention s_C = 1, s_L = 2, and either: (a) bake the convention into a definitional commitment of this ASN, or (b) exhibit the general-case inc-chain (with sibling increments) that works for arbitrary s_C, s_L ≥ 1 with SC-NEQ.

### Issue 5: K.μ⁻ effect clause requires non-empty `dom(M(d))` only via precondition narrative

**ASN-0047, K.μ⁻ definition**: "*Effect clause*: `dom(M'(d)) ⊂ dom(M(d)) ∧ (A v : v ∈ dom(M'(d)) : M'(d)(v) = M(d)(v))`"

**Problem**: The strict-subset clause `dom(M'(d)) ⊂ dom(M(d))` is unsatisfiable when `dom(M(d)) = ∅` (vacuously: no proper subset of ∅ exists). The ASN's precondition list says "`dom(M(d)) ≠ ∅` — d's arrangement must contain at least one mapping to be contracted; combined with the effect clause `dom(M'(d)) ⊂ dom(M(d))`, this ensures K.μ⁻ is a strict contraction at a state where contraction is well-defined" — but this argument is somewhat circular. The undefinedness of K.μ⁻ on empty arrangements should be stated more directly as a definitional consequence of the strict-subset clause, not as a separate precondition requirement.

**Required**: State explicitly that K.μ⁻'s effect clause is unsatisfiable when `dom(M(d)) = ∅`, making the precondition `dom(M(d)) ≠ ∅` a consequence rather than an independent requirement. Alternatively, lift the strict-subset clause to a non-strict subset and have the precondition supply the strictness.

### Issue 6: K.μ~ degenerate cases not consistently handled in elementary-sequence reading

**ASN-0047, "Decomposition of K.μ~", Case 1**: "K.μ⁻'s strict-contraction precondition `dom(M'(d)) ⊂ dom(M(d))` cannot be met when M'(d) = M(d), so a vacuous round-trip is not a valid elementary path; the correct expansion is the empty sequence."

**Problem**: The "K.μ~ as zero elementary steps" reading is structurally correct for π = id cases, but the ValidComposite★ definition requires K.μ~ to be "shorthand for its decomposition" — if K.μ~ expands to zero steps in degenerate cases, then a "composite" containing only K.μ~ has zero elementary steps, which is the identity composite. The ValidComposite★ machinery should make this case explicit: zero-step composites are valid composites and trivially satisfy J0/J1★/J1'★ (vacuously, since no net change occurs).

**Required**: Add an explicit "identity composite" or "zero-step composite" case to ValidComposite★, noting that K.μ~ with π = id expands to zero steps and the resulting composite trivially preserves all invariants.

### Issue 7: P4★ "load-bearing" classification at intermediate state in worked example is confusing

**ASN-0047, "Worked example: interior content replacement"**: "*P4★ at M_int (load-bearing).* `Contains_C(M_int) = ∅ ⊆ R_int = R`. P4★ holds at M_int because K.μ⁻ can only shrink Contains_C..."

**Problem**: The ASN classifies P4★ as a "composite invariant" that may be violated at intermediate states and is restored at composite boundaries. But the worked example claims P4★ "holds at M_int" and calls this "load-bearing." This is technically true in this specific case (because K.μ⁻ shrinks Contains_C), but obscures the general principle that intermediate states do not need to satisfy composite invariants. The "load-bearing" qualifier suggests intermediate P4★ is *required*, when in fact it's just incidentally satisfied here.

**Required**: Clarify that P4★ at M_int is incidentally satisfied (not required) in this example, or remove the "load-bearing" qualifier. The actual load-bearing check for P4★ is at the composite boundary, supplied by J1★/K.ρ.

### Issue 8: ASN-0036's S0 subsumption by P0 — but S0 is per-transition

**ASN-0047, ExtendedTransitionInvariants narrative**: "ASN-0036's S0 (ContentImmutability) and S1 (StoreMonotonicity) are subsumed by P0 and are not listed as separate conjuncts."

**Problem**: This is correct, but the subsumption argument relies on P0's quantifier `(A Σ → Σ' :: dom(C) ⊆ dom(C') ∧ ...)`. Foundation S0 has a slightly different form: `(A a : a ∈ dom(Σ.C) : a ∈ dom(Σ'.C) ∧ Σ'.C(a) = Σ.C(a))`. The subsumption is sound but the ASN doesn't show the equivalence explicitly. Readers who haven't internalized P0's structure may be unsure why S0 is dropped.

**Required**: Briefly show that P0's `dom(C) ⊆ dom(C') ∧ (A a ∈ dom(C) : C'(a) = C(a))` is logically equivalent to S0's `(A a : a ∈ dom(C) : a ∈ dom(C') ∧ C'(a) = C(a))`. The two are equivalent by elementary logic, but the trace should be visible.

### Issue 9: SubspaceAxiom listing omitted

**ASN-0047, Properties Introduced table** lists `s_C, s_L` under "Foundation restatements" with source "ASN-0043"

**Problem**: ASN-0043's definitions use the inequality `s_C ≠ s_L` inline (as the foundation review states), but the ASN-0047 table treats `s_C, s_L` as foundation restatements. This is correct, but SC-NEQ is listed separately as "axiom of this ASN." This split is potentially confusing — both halves of the subspace identifier story (the names s_C, s_L and the SC-NEQ axiom) should be clearly grouped.

**Required**: Either group s_C/s_L definition with SC-NEQ in the table (both new to this ASN if SC-NEQ is new), or explicitly note that SC-NEQ is *promoted* from ASN-0043's inline stipulation to a named axiom of this ASN. The current split obscures the relationship.

### Issue 10: K.λ first-link case discharges `ℓ ∉ dom(L) ∪ dom(C)` via SubAllocatorAxiom but the structural producibility chain is left implicit

**ASN-0047, K.λ first-link case**: "SubAllocatorAxiom's link namespace property gives `ℓ ∉ dom(L) ∪ dom(C)` directly; no inc derivation from a previously allocated `t` is invoked, because the axiom underwrites the first allocation by structural construction rather than by T10a's per-owner inc discipline."

**Problem**: But the ASN later (in the L1c reconciliation) says L1c requires an inc-chain from the document seed to the link address. For the first link `ℓ = [d.0.s_L.1]`, the chain is `d → [d.0.1] → [d.0.2] → [d.0.2.1] = ℓ`. The chain's intermediates `[d.0.1]` and `[d.0.2]` are not in any state component but are structural witnesses. K.λ's precondition list does *not* mention this chain — it relies on SubAllocatorAxiom for `ℓ ∉ dom(L) ∪ dom(C)` and on origin/subspace properties separately. A reader checking L1c (foundation) would need to construct the chain themselves.

**Required**: Either add a brief note in K.λ's first-link case showing the L1c chain witness, or explicitly cite that L1c is satisfied by the SubAllocatorAxiom's structural producibility (reconciled in the *Allocator hierarchy under documents* section). Cross-link the precondition's "produced by d's link sub-allocator" clause to L1c's chain-existential.

### Issue 11: NodeUniqueAllocation justification cites "ownership-derived uniqueness" without formal premise

**ASN-0047, NodeUniqueAllocation axiom**: "The axiom presumes the following structural mechanism for the node-allocation protocol... **every node address descends from the single bootstrap root n₀ by a chain of ownership-derived baptism events**..."

**Problem**: This is a presumption about *implementation*, lifted to an axiom of this ASN. The axiom should stand on its own as a uniqueness premise (`every K.δ node event yields e ∉ E`), without relying on protocol justification text. The presumption section is helpful as motivation but mixes meta-level (justification) with object-level (axiom content).

**Required**: Separate the axiom statement (object-level: `e ∉ E` at every K.δ node event) from the protocol justification (meta-level: Nelson's baptism / Gregory's granfilade). The axiom is what's load-bearing for the proofs; the protocol mechanism is rationale.

### Issue 12: Worked example "node baptism" presents counterfactuals without clear pass/fail criterion

**ASN-0047, "Worked example: node baptism under the bootstrap root", Step 2/3**: counterfactual transitions are presented as "rejected" but the rejection mechanism isn't formally tied to a transition's failure mode.

**Problem**: In a formal system, a counterfactual transition either (a) violates a precondition (so the transition isn't admitted) or (b) violates a postcondition (so the transition produces an invalid state). The Step 2 counterfactual says "K.δ case (i) precondition `e ∉ E` fails directly" — this is (a). The Step 3 counterfactual says "case (i) precondition `n₀ ≼ n'` fails" — also (a). But the example doesn't formally state the rejection model: are rejected transitions silently discarded, do they produce errors, or are they considered "not in the transition set"?

**Required**: State explicitly that the ASN's transition model rejects precondition violations as "not in the transition set" (or equivalent formal status). The counterfactual examples then exhibit transitions outside the set, which is informally useful but should be flagged as outside the model rather than as "rejected" within it.

### Issue 13: D-SEQ★ derivation appeals to "infinite-cardinality contradiction" that requires careful S8-fin invocation

**ASN-0047, D-SEQ★ derivation Step 1**: "These u_M are pairwise distinct (they differ at position j + 1), giving an infinite subset of V_S(d), which contradicts `|V_S(d)| = n < ∞` (S8-fin)."

**Problem**: S8-fin is `dom(M(d))` is finite, which implies V_S(d) ⊆ dom(M(d)) is finite. But the derivation constructs `{u_M : M ≥ 2}` as a subset of V_S(d), and claims this is infinite. The construction supplies u_M for each `M ∈ ℕ⁺ ∩ [2, ∞)` — an infinite set. The contradiction is sound but requires checking that the constructed u_M are *distinct* and *all in V_S(d)*. The ASN does check both, but the wording could be tighter.

**Required**: Restructure the contradiction to make explicit that (i) the u_M for M ≥ 2 are pairwise distinct (verified by position j+1 differing), (ii) each u_M is forced into V_S(d) by D-CTG★'s closed-interval-membership (verified above), so (iii) V_S(d) contains an infinite subset, contradicting S8-fin. The current text packs these into a single sentence; expansion would improve clarity.

### Issue 14: Frame extension table doesn't cover K.μ⁺_L

**ASN-0047, "Frame extension (all existing transitions)"** lists frames for K.α, K.δ, K.μ⁺, K.μ⁻, K.μ~, K.ρ.

**Problem**: K.μ⁺_L is missing from this listing. While its frame is stated at its own definition site, the central catalogue is incomplete. Same for K.λ (mentioned but not in the table list).

**Required**: Add K.μ⁺_L and K.λ to the frame extension table for consistency.

### Issue 15: K.μ⁻ admissibility's per-subspace independence requires at least one subspace to contract

**ASN-0047, K.μ⁻ admissibility precondition**: "The per-subspace patterns are independent across the two subspaces `s_C` and `s_L`: each subspace may independently exhibit partial suffix removal, full clearance, or no change, provided at least one subspace contracts strictly..."

**Problem**: The "at least one subspace contracts strictly" requirement is buried in a parenthetical. It's the key requirement that makes `dom(M'(d)) ⊂ dom(M(d))` satisfiable. Should be flagged more prominently as a precondition.

**Required**: Lift "at least one subspace contracts strictly" to a numbered precondition clause, not embedded in the per-subspace pattern description.

## OUT_OF_SCOPE

(None identified — the ASN appropriately defers known gaps to subsequent ASNs.)

VERDICT: REVISE
