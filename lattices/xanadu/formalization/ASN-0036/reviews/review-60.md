# Cone Review — ASN-0036/S7 (cycle 3)

*2026-04-14 12:39*

### S7 postcondition (c) introduces universally quantified variables absent from the precondition scope

**Foundation**: GlobalUniqueness (ASN-0034) — "For every pair of addresses a, b arising from distinct allocation events in any reachable system state: a ≠ b"
**ASN**: S7 formal contract — preconditions: "a ∈ dom(Σ.C) in a system conforming to S0, S4, D-DOC, S7a, S7b, S7d, origin(a), T4, and GlobalUniqueness"; postconditions: "(a) origin(a) is well-defined … (b) origin(a) is the identifier (D-DOC) … (c) For a₁, a₂ allocated under distinct documents (D-DOC), origin(a₁) ≠ origin(a₂)"
**Issue**: The precondition binds a single address `a` and establishes a system context. Postconditions (a) and (b) and the invariant are all consequences for this specific `a`. Postcondition (c) introduces fresh variables `a₁, a₂` with their own qualification ("allocated under distinct documents") — a universally quantified system-level claim, not a consequence of the input `a`. A formalizer translating S7 into TLA+ must decide: produce one THEOREM binding `a` (in which case `a₁` and `a₂` in (c) are unbound), or two separate theorems (one for (a)/(b)/invariant about `a`, one for (c) about pairs). The contract conflates an input-specific property with a system-wide theorem under a single precondition that binds neither `a₁` nor `a₂`.
**What needs resolving**: Either extract postcondition (c) into a separate property with its own preconditions (binding `a₁, a₂ ∈ dom(Σ.C)` allocated under distinct documents `d₁ ≠ d₂` per D-DOC, with S7d and GlobalUniqueness as dependencies), or restructure S7's precondition to bind the pair `a₁, a₂` alongside the system context — clarifying which postconditions apply to which inputs.

---

### S7 lists S4 as a precondition but no formal postcondition or invariant requires it

**Foundation**: S4 (Origin-based identity) — postcondition: "a₁ ≠ a₂, regardless of whether Σ.C(a₁) = Σ.C(a₂)"; S0 (Content immutability) — "a ∈ dom(Σ.C) ⟹ a ∈ dom(Σ'.C) ∧ Σ'.C(a) = Σ.C(a)"
**ASN**: S7 formal contract — preconditions include "S4 (origin-based identity)"; S7 permanence proof — "By S7d, a was itself produced by a T10a-conforming allocation event; S4 therefore applies, and distinct allocation events produce distinct addresses, so a is never reassigned or reused. The attribution cannot be severed."
**Issue**: S4 is invoked only in the Permanence section for the intermediate claim "a is never reassigned or reused," supporting the informal assertion "the attribution cannot be severed." Neither claim appears in S7's postconditions or invariant. The formal invariant — "origin(a) is invariant across all state transitions" — follows from S0 alone (a persists in dom(Σ'.C) for all successors) and the purity of origin(a) (computed from a's components, independent of system state), without any appeal to S4. Postcondition (a) uses only the origin definition, S7b, and T4. Postcondition (b) uses S7a. Postcondition (c) uses D-DOC, S7d, and GlobalUniqueness. None reference S4. The result is a precondition that inflates S7's dependency set — any downstream property citing S7 inherits a dependency on S4 that contributes to no formal conclusion. (Same pattern as finding #7, where T3 supports only a decidability remark absent from S4's postconditions.)
**What needs resolving**: Either add a formal postcondition capturing the "non-reuse" or "unseverability" claim so S4 has a conclusion to support, or remove S4 from S7's precondition list and reframe the permanence proof's S4 invocation as commentary rather than a formal proof step.

---

### S7d asserts per-event T10a conformance but S7's uniqueness proof requires single-system membership

**Foundation**: GlobalUniqueness (ASN-0034) — precondition: "a, b ∈ T produced by distinct allocation events … within a system conforming to T10a"; proof structure: "Strong induction on allocator tree depth d"
**ASN**: S7d axiom — "For every a ∈ dom(Σ.C): (i) origin(a) was produced by a distinct allocation event within a system conforming to T10a; (ii) a itself was produced by a distinct allocation event within a system conforming to T10a"; S7 proof, Uniqueness — "By S7d, each of these creating events is T10a-conforming. GlobalUniqueness therefore applies"
**Issue**: GlobalUniqueness's precondition requires both addresses to arise from events "within a system conforming to T10a" — a single allocator tree, as its depth-based induction proof assumes. S7d's axiom asserts that each address's producing event is "within a system conforming to T10a," but the indefinite article "a system" is existentially quantified per-event: for a₁ and a₂ in dom(C), S7d yields ∃S₁: origin(a₁)'s event ∈ S₁ and ∃S₂: origin(a₂)'s event ∈ S₂. GlobalUniqueness requires S₁ = S₂. S7's uniqueness proof collapses the two existentials into one shared system ("By S7d, each of these creating events is T10a-conforming. GlobalUniqueness therefore applies") without establishing that both events belong to the same T10a-conforming system. In a multi-node Xanadu network where distinct nodes might host independent allocator trees, per-event conformance does not entail cross-tree uniqueness.
**What needs resolving**: S7d's axiom should establish that all allocation events across all addresses in dom(C) — at both document and element levels — occur within a single T10a-conforming system, not merely that each event individually occurs within some T10a-conforming system. Alternatively, a system-level axiom asserting single-system membership should be stated so that S7's proof can discharge GlobalUniqueness's single-system precondition explicitly.

## Result

Cone converged after 4 cycles.

*Elapsed: 7254s*
