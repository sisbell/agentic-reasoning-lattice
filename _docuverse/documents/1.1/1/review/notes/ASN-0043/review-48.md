# Review of ASN-0043

## REVISE

### Issue 1: T7 cited under reinvented name "SubspaceDisjointness"
**ASN-0043, L0 derivation**: "...T7's precondition holds, yielding the fundamental disjointness"; elsewhere "by T7 (SubspaceDisjointness)".
**Problem**: Foundation T7 is named **FirstElementFieldDistinction** with postcondition `a.E₁ ≠ b.E₁ ⟹ a ≠ b`. The ASN renames it to "SubspaceDisjointness", which is misleading — T7 supplies pairwise distinctness, not set disjointness.
**Required**: Use the foundation name. State the lift from pairwise distinctness to set disjointness explicitly: T7 applied to every (a, b) ∈ dom(Σ.L) × dom(Σ.C) gives `a ≠ b`, hence `dom(Σ.L) ∩ dom(Σ.C) = ∅`.

### Issue 2: `fields(·)` notation reinvents T4b's projections
**ASN-0043, home(a) definition, L0, L1a, L1b, worked example**: `fields(a).node`, `fields(a).user`, `fields(a).document`, `fields(a).element`, `fields(a).E₁`, `#fields(a).element`.
**Problem**: Foundation T4b establishes `N(a)`, `U(a)`, `D(a)`, `E(a)` as the partial projection functions on T4-valid tumblers. ASN-0036 uses this notation directly (`N(a).0.U(a).0.D(a)`). ASN-0043 introduces a competing `fields(a).X` style that the foundation does not define.
**Required**: Replace all `fields(a).X` with the foundation projections — `home(a) = N(a).0.U(a).0.D(a)`, `E(a)₁`, `#E(a)` throughout.

### Issue 3: `fields(a).E₁` competes with ASN-0036's `subspace_I(a)`
**ASN-0043, L0, L1, worked example**: `fields(a).E₁ = s_L`, `fields(a).E₁ = s_C`.
**Problem**: ASN-0036 already defines `subspace_I(a) = E(a)₁` as the canonical name for this projection on content addresses. The link analog should reuse that name (or directly use `E(a)₁`), not introduce a third spelling.
**Required**: Choose one — either `E(a)₁` (foundation T4b) or `subspace_I(a)` extended uniformly across content and link addresses (ASN-0036). State the choice once and apply it consistently.

### Issue 4: L11a conflates uniqueness with permanence
**ASN-0043, L11a**: "Therefore every link has a globally unique, permanent identity..."
**Problem**: The proof appeals only to GlobalUniqueness, which establishes distinctness across allocation events. "Permanent" requires that the address-to-link binding does not change — which is L12's content, not GlobalUniqueness's. The conclusion silently bundles two claims with one citation.
**Required**: Split the conclusion. Cite GlobalUniqueness for uniqueness; cite L12 (LinkImmutability) for permanence of the binding once allocated.

### Issue 5: L8 uses `.type` notation inconsistent with L3's `.eᵢ`
**ASN-0043, L8**: `same_type(a₁, a₂) ⟺ Σ.L(a₁).type = Σ.L(a₂).type`.
**Problem**: L3 introduces indexed slot access `Σ.L(a).eᵢ`. L8 then writes `Σ.L(a).type` without defining the named accessor against the indexed form. The Convention StandardTriple names `(F, G, Θ)` for the arity-3 case but does not establish `.type` as an accessor for arbitrary arity.
**Required**: Either define `Σ.L(a).type ≡ Σ.L(a).e₃` explicitly under Convention StandardTriple (and confirm slot 3 is the type endset for all arity ≥ 3 per L3), or replace `.type` with `.e₃` throughout.

### Issue 6: L5's formal statement is tautological
**ASN-0043, L5**: "`Σ.L(a).e is characterized by {(s, ℓ) : (s, ℓ) ∈ Σ.L(a).e}`"
**Problem**: Given the type `Endset = 𝒫_fin(Span)`, a set is trivially characterized by its members. The substantive claim — that ordering of spans within an endset carries no semantics, and that endset equality is set equality — lives only in the prose.
**Required**: State the substantive content formally. For example: `Σ.L(a).eᵢ = Σ.L(a').eⱼ ⟺ (A (s, ℓ) :: (s, ℓ) ∈ Σ.L(a).eᵢ ⟺ (s, ℓ) ∈ Σ.L(a').eⱼ)`, with an explicit note that the model exposes no positional accessor within an endset.

### Issue 7: L1a's formal predicate is informal
**ASN-0043, L1a**: "`(A a ∈ dom(Σ.L) :: (fields(a).node).0.(fields(a).user).0.(fields(a).document) identifies the allocating document)`"
**Problem**: "Identifies the allocating document" is English glued onto the quantifier, not a formal predicate. A reviewer cannot check satisfaction.
**Required**: State the predicate in terms of `home(a)` and the allocator chain: e.g., `(A a ∈ dom(Σ.L) :: (E d :: d is a document tumbler ∧ home(a) = d ∧ a ∈ dom(A) for some allocator A spawned under d))`. Or anchor it to T10a's spawning relation.

### Issue 8: PrefixSpanCoverage proof lacks explicit foundation citations
**ASN-0043, PrefixSpanCoverage**: The proof uses "divergence(t, x)", "T1(i)", "T1(ii)", and reasons about positions exceeding shifted values without naming the NAT axioms invoked.
**Problem**: The proof's three-case structure (same depth, greater depth, shorter depth) is sound, but the step "t_{#x} ≥ x_{#x} + 1 = shift(x, 1)_{#x}" relies on NAT-discrete (forward direction) without citing it. The use of `divergence` cites no foundation lemma despite Divergence being a foundation definition.
**Required**: Cite Divergence at the introduction of each divergence index; cite NAT-discrete where strict-to-`+1` promotion is used; cite TA-strict where `x < shift(x, 1)` is invoked.

### Issue 9: L0 set-disjointness derivation jumps from pairwise to set
**ASN-0043, L0 prose**: "With T4-validity discharged and `zeros(a) = zeros(b) = 3`, T7's precondition holds, yielding the fundamental disjointness: `dom(Σ.L) ∩ dom(Σ.C) = ∅`"
**Problem**: T7 is a pairwise statement. The lift to set disjointness requires universal instantiation over `dom(Σ.L) × dom(Σ.C)`. The prose elides this step.
**Required**: Make the universal explicit: for every `a ∈ dom(Σ.L)` and every `b ∈ dom(Σ.C)`, T7 (with T4-validity and zero-count premises discharged on each side, and `s_L ≠ s_C`) yields `a ≠ b`; hence `dom(Σ.L) ∩ dom(Σ.C) = ∅`.

### Issue 10: Worked example does not demonstrate higher-arity links
**ASN-0043, Worked Example**: All links use arity 3 — the StandardTriple form.
**Problem**: L3 admits N ≥ 3, and the prose specifically references Nelson's "4-sets, 5-sets ... n-sets". A worked example that never exhibits N > 3 leaves the higher-arity case unverified against L3, L6, and L8's "slot 3 is type endset" claim for general N.
**Required**: Add a small extension showing an arity-4 link, verifying L3 (`|Σ.L(a)| = 4 ≥ 3`), L6 (slot permutation among the four), and L8 (`Σ.L(a).e₃` is the type for the arity-4 case).

## OUT_OF_SCOPE

### Topic 1: Open Question on transclusion–link interactions
**Why out of scope**: The first Open Question ("invariants between link store and content store when same I-address appears in multiple arrangements via transclusion") concerns how arrangement-layer transclusion (S5, ASN-0036) interacts with link endsets referencing transcluded content. Belongs in a future ASN that models the arrangement–link interface, not in this ASN whose subject is the link store structure.

### Topic 2: Coverage-based endset equivalence
**Why out of scope**: The coverage definition prose notes that two endsets with different span decompositions can have identical coverage. Whether they should be treated as query-equivalent is an operations/query-interface question, not a state invariant.

VERDICT: REVISE
