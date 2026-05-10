# Cone Review — ASN-0034/T10a.3 (cycle 1)

*2026-04-18 03:46*

### T10a.8 omits NAT-zero + NAT-discrete for the "non-zero ⇒ strictly positive" step
**Foundation**: TA5's Depends establishes the document's per-step convention: the inference "non-zero ⇒ strictly positive on ℕ" is sourced from **T0 + NAT-zero + NAT-discrete jointly**, "rather than collapsing the lower-bound step into an implicit appeal to NAT-discrete alone," and the same trio is applied "in T4a's opening, T4c's exhaustion step, TA5-SigValid, and TA5a."
**ASN**: T10a.8 (UniformSiblingZeroCount) proof: "T4's field-segment constraint forces the terminal component non-zero, hence strictly positive (T0's carrier ℕ)." Depends lists only T10a, T10a.4, T4, TA5, TA5-SigValid.
**Issue**: T10a.8 makes exactly the "non-zero ⇒ strictly positive on ℕ" inference that the rest of the document has committed to sourcing per-step from NAT-zero (lower bound `0 ≤ n`) + NAT-discrete (no natural strictly between 0 and 1). The proof handwaves it with "(T0's carrier ℕ)" and the Depends list omits both lemmas. T4 alone gives `t_{#t} ≠ 0`; it cannot sharpen that to `t_{#t} ≥ 1` without the ℕ-arithmetic lemmas.
**What needs resolving**: T10a.8's proof and Depends must cite NAT-zero and NAT-discrete (alongside T0) at the step where the non-zero terminal component is sharpened to strictly positive, matching the convention TA5 explicitly names and applies.

### T10a.2 smuggles T3 into the Prefix citation
**Foundation**: Prefix defines `p ≼ t ≡ #p ≤ #t ∧ (A i : 1 ≤ i ≤ #p : pᵢ = tᵢ)` — positional agreement on the shorter prefix, nothing more. The step from "equal-length + positional agreement" to "identical" is supplied by T3 (CanonicalRepresentation): `#a = #b ∧ (A i : aᵢ = bᵢ) ≡ a = b`.
**ASN**: T10a.2 (NonNestingSiblingPrefixes) Depends: "T10a.1 (#a = #b) and Prefix (equal-length tumblers are prefix-related only if identical)."
**Issue**: "Equal-length tumblers are prefix-related only if identical" is not a Prefix property — Prefix only yields component-wise agreement on `1..#a`. Getting from there to `a = b` requires T3. The Depends list folds T3's content into a parenthetical on Prefix rather than citing T3 as a distinct dependency, which breaks the per-clause sourcing discipline the rest of the ASN (e.g., T10a.3, T10a.5, T10a.6) applies.
**What needs resolving**: T10a.2's Depends must name T3 (CanonicalRepresentation) as the authority that converts equal-length + positional agreement into identity, with Prefix cited only for positional agreement.

### T10a.4 omits T10a from its Depends despite consuming the axiom's two constitutive clauses
**Foundation**: T10a.4 asserts T4-preservation across the allocator tree. The proof consumes two clauses of T10a itself: (i) the root-initialization constraint ("the root allocator's base address satisfies T4 by the initialization constraint") as the base case, and (ii) the discipline's runtime `zeros(t) ≤ 2` check at `k' = 2` as the premise that places child-spawning inside TA5a's preservation envelope.
**ASN**: T10a.4 Depends: "T4 (HierarchicalParsing — the invariant preserved by induction), TA5a (inc(·, 0) and inc(·, 1) preserve T4 unconditionally on T4-valid inputs; inc(·, 2) preserves T4 under `zeros(t) ≤ 2`)."
**Issue**: T10a.1, T10a.3, T10a.5, T10a.7, and T10a.8 all explicitly list T10a in their Depends when they consume axiom clauses. T10a.4 consumes the root-initialization clause and the runtime-bound clause of T10a but omits T10a from its Depends, breaking the citation pattern used by every sibling postcondition. A reader reconstructing T10a.4's dependencies from its Depends list alone cannot see that the base case and the `k' = 2` case are sourced from the axiom itself.
**What needs resolving**: T10a.4's Depends must name T10a (AllocatorDiscipline) with the two clauses it consumes — root T4-initialization and the runtime `zeros(t) ≤ 2` check at `k' = 2` — matching the sibling-postcondition pattern.
