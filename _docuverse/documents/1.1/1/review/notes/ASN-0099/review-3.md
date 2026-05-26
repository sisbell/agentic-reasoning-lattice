# Review of ASN-0099

## REVISE

### Issue 1: F1 and F12 listed in claims table but never labeled in prose
**ASN-0099, Claims Introduced table**: "F1 | Match predicate as set-theoretic overlap, existential over slots | introduced" and "F12 | Two-phase factoring: `findlinks_V` composes `image` (V→I) and `findlinks` (I→Link) | introduced"
**Problem**: The body presents `matches(a, I, Σ) ≡ (E i : … : coverage(eᵢ) ∩ I ≠ ∅)` and `findlinks_V(R, d, Σ) = findlinks(image(R, d, Σ), Σ)` as inline definitions, never as numbered F1 or F12 statements. Other F-claims (F2, F3, F4, F5, F6, F7, F8, F9, F10, F11, F13) are explicitly labeled in prose; F1 and F12 are not. As "claims" they are also vacuous — F1 restates the definition of `matches`, F12 restates the operational definition of `findlinks_V`.
**Required**: Either label them explicitly in the body where introduced, or mark them as DEF rather than INTRODUCED in the table.

### Issue 2: F10's cross-document ordering claim lacks derivation
**ASN-0099, Result Ordering**: "Across home documents, T1 sorts by document prefix — addresses with the same `home(·)` group together, and home documents themselves order lexicographically."
**Problem**: The within-document part is derived (chain enumeration is T1-increasing via ChainEnumerationInjectivity). The across-document claim is asserted without derivation. To establish that all links homed at `d₁` precede all links homed at `d₂` (when `d₁ < d₂`), one needs CrossDocDisjointness (ASN-0093) to establish that the sub-allocator anchors are non-nesting, plus PrefixOrderingExtension (ASN-0034) to lift the prefix ordering to all extensions. Neither is cited.
**Required**: Cite CrossDocDisjointness (ASN-0093) and PrefixOrderingExtension (ASN-0034), or derive the cross-document ordering claim explicitly.

### Issue 3: F9 frame citation imprecise for K.μ⁺ and K.μ⁻
**ASN-0099, Arrangement Independence**: "F9 follows from F8 once we observe that each K.μ-family transition's frame clause holds `L' = L` (ASN-0047, ASN-0093), so the F8 hypothesis `Σ.L = Σ'.L` is satisfied at every such step."
**Problem**: In ASN-0047, only K.μ~ and K.μ⁺_L include `L' = L` in their frame. K.μ⁺'s frame is "C' = C; E' = E; (A d' : d' ≠ d : M'(d') = M(d')); R' = R" — no L mentioned. K.μ⁻'s frame is similar. F9 lists all four K.μ-family operations as preserving L, but the frame-clause justification is only direct for two of them. The other two rely on the convention that operations modify only what their effect clauses name, which is not formally stated as a derivation step.
**Required**: Either note that L preservation under K.μ⁺/K.μ⁻ follows from their effect clauses (which only modify M(d)) rather than from explicit frame clauses, or flag this as a gap in ASN-0047 requiring frame amendment.

### Issue 4: Filtered form behavior at out-of-range slot indices is informal
**ASN-0099, Endset Filtering**: "findlinks_filtered(C, Σ) = {a ∈ dom(Σ.L) : (A (i, J) ∈ C : coverage(Σ.L(a).eᵢ) ∩ J ≠ ∅)}" and prose "For `i > n`, the constraint `(i, I)` references a slot absent from `a` and is unsatisfiable, so `a` is excluded from `findlinks_filtered({(i, I)}, Σ)` at that `i`."
**Problem**: The formal definition uses `coverage(Σ.L(a).eᵢ)` without specifying its semantics when `i > |Σ.L(a)|`. By L6 (ASN-0043), the positional accessor `Σ.L(a).eᵢ` is only defined for `i ∈ {1, …, |Σ.L(a)|}`. The author's "unsatisfiable" interpretation is one of several possible (undefined predicate, false predicate, vacuous constraint), and the derivation of `findlinks(I, Σ) = ⋃_{i ∈ ℕ⁺} findlinks_filtered({(i, I)}, Σ)` depends on the chosen semantics.
**Required**: Make the out-of-range semantics explicit in the definition — e.g., "coverage(Σ.L(a).eᵢ) ∩ J ≠ ∅ is false when i > |Σ.L(a)|" — or restrict the constraint quantifier to slots within the link's arity.

### Issue 5: Empty filter constraint set boundary not addressed
**ASN-0099, Endset Filtering**: "findlinks_filtered(C, Σ) = {a ∈ dom(Σ.L) : (A (i, J) ∈ C : coverage(Σ.L(a).eᵢ) ∩ J ≠ ∅)}"
**Problem**: The boundary case `C = ∅` is not addressed. By the vacuous universal over an empty constraint set, `findlinks_filtered(∅, Σ) = dom(Σ.L)`. This is a meaningful boundary — a query with no constraints returns every link — but the ASN's boundary discussion only covers empty I-set and empty link store, not empty constraint set. Boundary cases are mandatory; this one is missing.
**Required**: Add the empty-constraint-set case to either the "Endset Filtering" section or "The Empty Query" section, and verify the vacuous universal yields `dom(Σ.L)`.

### Issue 6: F8 conflates abstract determinism with implementation conformance
**ASN-0099, Determinism**: "F8 (Determinism): result(I, Σ) = result(I, Σ') whenever Σ.L = Σ'.L."
**Problem**: F8 is stated in terms of `result(I, Σ)` — the implementation's actual output — but the derivation that follows operates entirely on `findlinks(I, Σ)`, the abstract comprehension. Determinism is fundamentally a property of the definition (the comprehension is a function of `Σ.L` and `I`), not of the implementation. Other claims using `result` (F2, F3) are clearly conformance claims; F8 reads as a fundamental property but is stated as a conformance claim. The cleanest form would be `findlinks(I, Σ) = findlinks(I, Σ')`, with conformance to `result` then flowing through F2 + F3.
**Required**: Restate F8 as a property of `findlinks` rather than `result`, or split into two claims: F8a for the abstract determinism of `findlinks`, F8b for the consequence that `result` is determined by `Σ.L` (via F2 + F3).

### Issue 7: Phase 1 formal definition's precondition incomplete
**ASN-0099, Two-Phase Factoring**: "image(R, d, Σ) = {Σ.M(d)(v) : v ∈ R}"
**Problem**: The prose lists two preconditions ("`d ∈ dom(Σ.M)` so that `Σ.M(d)` is defined as a partial function, and `R ⊆ dom(Σ.M(d))` so that every `Σ.M(d)(v)` is defined for `v ∈ R`"), but the formal expression lacks a "defined when" clause stating both. The companion `project` definition (used in Phase 2 discussion) does use a "defined when" form. The asymmetry leaves the formal `image` ill-formed without consulting prose.
**Required**: Add an explicit `defined when d ∈ dom(Σ.M) ∧ R ⊆ dom(Σ.M(d))` clause to the formal definition of `image`.

### Issue 8: F5 not exercised in the worked example
**ASN-0099, A Worked Example**: The example exercises F2, F3, F6, F11, F13 against a concrete instance.
**Problem**: F5 (IdentityNotValue) is a load-bearing property — distinct I-addresses with equal content values produce different match results. The example uses three distinct values `v₁, v₂, v₃` and so has no case where equal-value-distinct-address scenarios are tested. F5 would be more concrete with a scenario like "if `α₁` and `α₂` happened to have equal content values, the link covering only `α₁` would still not match a query for `{α₂}`."
**Required**: Add a brief F5 verification to the worked example — either by constructing an equal-value-distinct-address scenario, or by noting that the example's address-based matching at slot 1 (`coverage = {α₂}`) discriminates `α₂` from `α₃` regardless of any value relationship.

## OUT_OF_SCOPE

### Topic 1: Behavior on queries with addresses outside `dom(Σ.C) ∪ dom(Σ.L)`
**Why out of scope**: The ASN's open questions explicitly flag this. The match predicate works mechanically for any `I ⊆ T`, but the operational interpretation of querying with "phantom" addresses (sub-allocator anchors, never-allocated addresses) is a separate semantic question.

### Topic 2: Multi-instance link store consistency and BEBE-layer concerns
**Why out of scope**: The prompt's scope rules explicitly exclude replication and inter-server protocols. The ASN correctly defers this to a multi-instance specification.

### Topic 3: I→V inverse direction (FOLLOWLINK/RETRIEVEENDSETS)
**Why out of scope**: The ASN explicitly factors this as a separate operation with distinct semantics. Resolution of endset coverage back to V-positions belongs in its own specification.

### Topic 4: Access control composition with completeness
**Why out of scope**: Access control filtering is identified as orthogonal scope narrowing that composes with FINDLINKS via F14. The detailed access-control semantics belong in a separate authorization specification.

### Topic 5: Concurrency model between K.λ and FINDLINKS
**Why out of scope**: The sequential transition axiom (ASN-0093) establishes atomic transitions at the substrate level; higher-protocol-layer concurrency is appropriately deferred.

VERDICT: REVISE
