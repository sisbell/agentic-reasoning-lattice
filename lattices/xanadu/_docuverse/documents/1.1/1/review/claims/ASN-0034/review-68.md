# Cone Review — ASN-0034/T9 (cycle 3)

*2026-04-16 04:14*

I'll read the document carefully, cross-checking definitions, dependency chains, and quantifier scopes across all properties.

### T10a-N necessity claim exceeds what the proof establishes

**Foundation**: (internal — foundation ASN)
**ASN**: T10a (AllocatorDiscipline), postcondition T10a-N: "The axiom is therefore both sufficient (T10a.1–T10a.5) and necessary for prefix-incomparability across all non-ancestor-descendant allocator output domains."
**Issue**: The necessity proof constructs one counterexample: relaxing the sibling stream to permit k > 0 yields a₁ ≺ a₂ within the same allocator. This proves that the sibling restriction (k = 0 only) is necessary for prefix-incomparability. The concluding sentence then claims the entire axiom — including the k' ∈ {1, 2} child-spawning bound, the at-most-once constraint, and the root T4 initialization — is "necessary for prefix-incomparability." These three constraints serve different purposes and are not addressed by the proof: (a) The k' ∈ {1, 2} bound is necessary for T4 preservation (TA5a), not prefix-incomparability — any k' > 0 produces a child at a different depth, and children from the same parent with different k' values diverge at position #parent + 1 (one has a nonzero value, the other has zero), so prefix-incomparability holds for arbitrary k' > 0. (b) The at-most-once constraint prevents two child allocators from sharing a base address, which is a uniqueness concern (and admittedly a prefix-comparability concern in the degenerate case x = y, since x ≼ x), but its necessity is never demonstrated. (c) The root T4 requirement is not necessary for prefix-incomparability because child-spawning via inc(t, k') with k' > 0 always sets position #t + k' to 1, guaranteeing sig(result) = #result regardless of whether t satisfies T4 — so the prefix-preservation argument through sibling increments holds without T4. The "therefore" in T10a-N draws a universal conclusion from a single-case proof.
**What needs resolving**: T10a-N should state precisely which component of the axiom the necessity proof covers (the sibling k = 0 restriction), and either prove necessity for the remaining components separately or acknowledge that they serve distinct purposes (T4 preservation, uniqueness) that the prefix-incomparability necessity argument does not address.

---

### T8's formal contract uses `allocated(s)` without any definition of the state model

**Foundation**: (internal — foundation ASN)
**ASN**: T8 (AllocationPermanence), formal contract: "Invariant: For every state transition s → s', allocated(s) ⊆ allocated(s')."
**Issue**: T8's invariant is parameterized by three concepts — *state*, *state transition*, and `allocated(s)` — none of which are defined anywhere in the provided ASN. T10a defines how allocators produce addresses (behavioral constraints on inc), and T9 defines `dom(A)` (per-allocator output sets), but no property bridges these to T8's state-indexed formulation. The intended meaning is presumably `allocated(s) = ⋃{dom(A) : A activated by state s}`, but this is never stated. The gap is consequential: a formalizer cannot write T8's invariant in TLA+ without knowing what the state variable is, what the transition relation comprises, and how `allocated` is computed from the allocation mechanism defined by T10a. Every other formal contract in the document defines or cites its terms — T9 defines `dom(A)`, `same_allocator`, and `allocated_before`; T1 cites T0 for length and component projection. T8 alone uses terms with no anchor.
**What needs resolving**: A definition of `allocated(s)` — either as a state variable with an initial value and update rule, or as a derived function of the allocator tree state — together with enough state-model vocabulary for T8's invariant to be a checkable statement rather than a natural-language assertion.

---

### Consequence 5 defers to T10a.5 for a proof that T10a.5 does not contain

**Foundation**: (internal — foundation ASN)
**ASN**: T10a (AllocatorDiscipline), Consequence 5: "The at-most-once child-spawning constraint, combined with positional inheritance through the allocator tree, ensures that non-ancestor-related allocators diverge at some fixed position inherited from their branching point in the tree. The inductive argument is given in T10a.5."
**Issue**: The sentence "The inductive argument is given in T10a.5" is a cross-reference that promises a proof at a specific location. T10a.5 in the formal contract states the conclusion ("For any two allocators X and Y not in an ancestor-descendant relationship, for all x ∈ domain(X) and y ∈ domain(Y), x ⋠ y ∧ y ⋠ x") and lists eight dependencies, but contains no argument — inductive or otherwise. The pieces needed for the proof are identified in the dependency list (at-most-once constraint, positional inheritance via TA5(b) and TA5-SigValid, divergence via T3), and the prose of Consequence 5 sketches the intuition, but neither location assembles the actual induction: base case (sibling allocators diverge at the parent's spawning positions), inductive step (divergence propagates through the allocator tree via positional inheritance), and closure (prefix-incomparability follows from divergence plus Prefix). The cross-reference creates the appearance that the proof exists when it does not.
**What needs resolving**: Either write the inductive proof in Consequence 5 (or in T10a.5's body), or correct the cross-reference to acknowledge that T10a.5 states the claim and its dependencies but the assembling argument remains to be supplied.
