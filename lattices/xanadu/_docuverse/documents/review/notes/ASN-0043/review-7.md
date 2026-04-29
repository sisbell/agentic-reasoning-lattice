# Review of ASN-0043

## REVISE

### Issue 1: L11 formal statement is prose inside a quantifier

**ASN-0043, Link Distinctness and Permanence**: "`(A a₁, a₂ ∈ dom(Σ.L) :: a₁ ≠ a₂ ⟹ a₁ and a₂ designate separate link entities, even when Σ.L(a₁) = Σ.L(a₂))`"

**Problem**: "designate separate link entities" is not a formal predicate. For any partial function, distinct domain elements are trivially distinct domain elements — ordered triples give you that for free. The substantive content of L11 is twofold: (a) GlobalUniqueness (ASN-0034) applies to link addresses, guaranteeing that distinct allocation events produce distinct addresses; and (b) the link store is deliberately non-injective — `Σ.L(a₁) = Σ.L(a₂)` with `a₁ ≠ a₂` is a conforming state, not an error. The current statement captures neither precisely. The derivation via GlobalUniqueness and T9 is correct, but the formal statement it derives needs to be actually formal.

**Required**: Reformulate L11 with a precise predicate. The uniqueness half should state that link addresses are produced by the allocation mechanism governed by T9, inheriting GlobalUniqueness. The non-injectivity half could be an existential: for any conforming state with at least one link `(F, G, Θ)`, there exists a conforming extension with a second address mapping to the same triple. Alternatively, state clearly that no injectivity constraint holds: `¬(A a₁, a₂ ∈ dom(Σ.L) :: Σ.L(a₁) = Σ.L(a₂) ⟹ a₁ = a₂)` for states with `|dom(Σ.L)| ≥ 2`.

### Issue 2: L10 and L13 prove overlapping results for identical span constructions; L10 is incomplete

**ASN-0043, The Type Endset (L10)**: "`(A c : p ≼ c : c ∈ coverage({(p, ℓ_p)}))`" followed by "Hierarchical type relationships follow from the tumbler ordering without any additional mechanism."

**ASN-0043, Reflexive Addressing (L13)**: detailed three-case exclusion proof establishing `coverage({(b, ℓ_b)}) = {t ∈ T : b ≼ t}`.

**Problem**: L10 and L13 both construct a unit-width span at the last significant position of a tumbler (`ℓ_p` and `ℓ_b` respectively — identical structure, different variable names). L13 proves the full coverage equality (both inclusion and exclusion) via a thorough case analysis across same-depth, greater-depth, and shorter-depth tumblers. L10 proves only the inclusion direction — all extensions of `p` lie in the coverage — and does not establish that non-extensions are excluded. The claim that "hierarchical type relationships follow from the tumbler ordering" is incomplete without the exclusion direction: a span query at `p` that also matched non-subtypes would not give a clean type hierarchy. The exclusion IS true (the same case analysis from L13 applies verbatim), but L10 doesn't prove it or reference it.

**Required**: Factor the shared argument into a general lemma: for any tumbler `x` with `#x ≥ 1`, the unit-depth span `(x, ℓ_x)` has `coverage({(x, ℓ_x)}) = {t ∈ T : x ≼ t}`. Prove both directions once. Then L10 references it for type hierarchies (the span covers all and only subtypes) and L13 references it for reflexive addressing (the canonical span targets exactly the entity and its extensions). This eliminates the current asymmetry where L13 has a full proof and L10 has half of one, and removes the duplicated argument structure.

### Issue 3: Worked example L12 transition verification checks an address not in the pre-state

**ASN-0043, Worked Example — Extension**: "*L12 across the transition `Σ → Σ_2`.* The original link is preserved: `a ∈ dom(Σ_2.L)` and `Σ_2.L(a) = (F, G, Θ) = Σ.L(a)`. Similarly `a' ∈ dom(Σ_2.L)` with `Σ_2.L(a') = (F, G, Θ)`. L12 holds non-vacuously. ✓"

**Problem**: The original state is `Σ` with `dom(Σ.L) = {a}`. The address `a'` was introduced informally in the L11 non-vacuous check ("extend the example: add `a' = 1.0.1.0.1.0.2.2`") but was never incorporated into a named intermediate state. The transition is labeled `Σ → Σ_2`, and L12 requires: for all addresses in `dom(Σ.L)`, they persist with the same value in `Σ_2`. Since `a' ∉ dom(Σ.L) = {a}`, the "`a'`" check is not a verification of L12 for this transition — it confuses "exists in the successor state" with "preserved from the predecessor state." The check for `a` is correct; the check for `a'` is not applicable to the stated transition.

**Required**: Either (a) define the sequence of transitions explicitly — name the intermediate state after adding `a'`, then verify L12 for each transition separately — or (b) remove the `a'` check from the `Σ → Σ_2` transition verification, since `a' ∉ dom(Σ.L)` makes L12 inapplicable to it. The L12a check has the same issue: it states `dom(Σ.L) = \{a\} ⊆ \{a, a', a_2\}`, which is correct but doesn't exercise `a'` preservation — only `a`'s persistence.

## OUT_OF_SCOPE

### Topic 1: Compound link well-formedness constraints

L13 establishes that link-to-link references are structurally valid, enabling arbitrary relational structures. The ASN correctly asks (in Open Questions) what constraints, if any, should govern such structures — acyclicity, depth bounds, self-reference prohibition. These constraints would be properties of link configurations, not of individual links, and belong in a future ASN on compound link structures.

**Why out of scope**: L13 establishes the mechanism; constraints on its use are new territory requiring analysis of compound structures as objects in their own right.

VERDICT: REVISE
