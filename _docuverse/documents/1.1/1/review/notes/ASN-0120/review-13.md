# Review of ASN-0120

The mathematics here is largely sound — the V→I confinement derivation (T5 over the ordinal-displacement endpoints), the ML9 weakest-precondition argument (Facts (a)/(b), including the `d' = d` boundary), and the worked example all check out. My findings are a precondition-surface gap and several anti-bloat patterns the `review-mode.anti-bloat` classifier asks me to surface.

## REVISE

### Issue 1: Load-bearing spec-set well-formedness is not part of the formal precondition
**ASN-0120, "What the endset arguments name" + ML9 / claim table**: The body requires each `σ_j` to be content-subspace, at common depth `m ≥ 2`, and "to carry an *ordinal displacement* `ℓ_j = δ(n_j, m)`." This ordinal-displacement condition is what the confinement step uses to force `t₁ = s_C` and hence `ρ(R,Σ) ⊆ dom(Σ.C)` (ML1). But the formal precondition `enabled(makelink) ≡ d ∈ dom(Σ.M) ∧ ρ(R₃, Σ) ≠ ∅` omits it, and the ASN explicitly downgrades source-allocation to "definedness of `ρ`" rather than a guard.
**Problem**: A non-ordinal `σ_j` still yields a *defined* `ρ(R_j, Σ)` whose images can land in `dom(Σ.L)` (exactly the `ℓ_j = [c,0,…,0]` escape the ASN itself exhibits). So ML1's `ρ ⊆ dom(Σ.C)` — stated unconditionally in the claim table — silently depends on a precondition that appears only as prose in the spec-set definition and is absent from both `enabled` and the ML1 row. A reader taking ML1 at face value gets a false invariant.
**Required**: Consolidate the spec-set well-formedness conditions (content-subspace, depth `m`, ordinal displacement, `d_j ∈ dom(Σ.M)`) into the operation's precondition surface, and qualify the ML1 claim-table row by that precondition.

### Issue 2: Defensive scope-justification prose around the type restriction
**ASN-0120, "Three endsets" section**: "This is a deliberate confinement, not an oversight: ... That *direct-address input mode* ... is a distinct operation with a distinct argument shape, and is **out of scope** here. The present ASN specifies MAKELINK-via-content-V-specs exclusively..."
**Problem**: The substantive content (V-spec resolution can produce only content-backed endsets, so ghost/foreign endsets are unreachable) is one sentence. The surrounding paragraph defends the choice ("not an oversight"), narrates an out-of-scope alternative facility at length, and re-asserts scope twice. This is meta-prose occupying a claim-supporting slot.
**Required**: State the restriction as a consequence of ML1/ML3, drop the "not an oversight" defense and the extended direct-address narration.

### Issue 3: Repeated "this is implementation, not an abstract claim" disclaimer tails
**ASN-0120, implementation notes after ML1, ML0, and ML9**: "...the sporgl layout itself is implementation, not an abstract claim." / "...the append-at-end mechanism is implementation." / "The abstract claim is the biconditional, not the index."
**Problem**: Implementation evidence is house style and fine, but the same abstract-vs-implementation boundary is redrawn three times in identical defensive form. The disclaimer adds no information once established. (The `do2.c:122`/`do2.c:136` line-level citation in the ML6 main prose is the same drift in sharper form — source-line granularity in an abstract claim's body.)
**Required**: Drop the repeated disclaimer tails; if the abstract/implementation boundary needs stating, state it once.

### Issue 4: Counterexample motivates a precondition the precondition already excludes
**ASN-0120, "What the endset arguments name"**: "A merely level-uniform `ℓ_j` ... whose action point `k < m` would let the half-open interval `⟦σ_j⟧` escape the content subspace — e.g. `ℓ_j = [c, 0, …, 0]` ... sweeps in link-subspace V-positions..."
**Problem**: This imagines an input the ordinal-displacement precondition forbids, to argue why the precondition is needed — the "explains why the axiom is needed rather than what it says" pattern. The load-bearing content is the T5 confinement derivation that follows; the escape example is motivation, not reasoning. (If Issue 1 is fixed by surfacing the precondition formally, a one-line justification suffices.)
**Required**: Reduce to a one-clause justification attached to the precondition, or remove once the precondition is formalized.

## OUT_OF_SCOPE

### Topic 1: Meaning of an empty from/to endset
The Open Question on `ρ(R, Σ) = ∅` for non-type endsets is correctly deferred — L3 permits `e₁, e₂ = ∅`, and the operation remains well-defined. New territory, not an error here.

### Topic 2: Endsets referencing the link subspace
The second Open Question (link-to-link endsets) is properly deferred; the present ASN's content-V-spec resolution does not reach it.

VERDICT: REVISE
