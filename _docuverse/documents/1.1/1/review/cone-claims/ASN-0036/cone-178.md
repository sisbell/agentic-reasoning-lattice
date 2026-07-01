I reviewed ASN-0036 as a system, checking cross-claim consistency — particularly quantifier grounding, precondition chains, and the elaborate D-CTG-depth / D-INJ proof machinery — against the ASN-0034 foundations and the previously-declined findings (to avoid resurfacing the D-CTG-depth Depends misattribution and the S8 circularity, both already fixed).

The core D-CTG-depth and D-INJ proofs hold up: case coverage for the interior-disagreement argument is complete, the T0(a)/S8-fin pigeonhole contradiction is built correctly (N fixed first, N+1 witnesses via repeated T0(a) applications at fixed base `u`, pulled back through S8-fin's bijection, counted via D-INJ against NAT-card's upper bound), and D-INJ's ρ-construction handles all index-placement subcases. I did find one recurring structural gap in how document-quantification is grounded.

### D-CTG's outer quantifier leaves `d` untyped, unlike S8-depth/S8-fin's grounded restriction
**Class**: REVISE
**Foundation**: T0 (CarrierSetDefinition); Σ.M(d) (Arrangement)
**ASN**: D-CTG (VContiguity), Axiom: `(A d, u, q : u ∈ V_1(d) ∧ q ∈ V_1(d) ∧ u < q : (A v ∈ T : subspace(v) = 1 ∧ #v = #u ∧ zeros(v) = 0 ∧ u < v < q : v ∈ V_1(d)))`
**Issue**: The outer binder quantifies `d` with no domain restriction at all. Compare S8-depth's `(A d ∈ T :: ...)` and S8-fin's `(A d ∈ T :: (E n : ...))`, both of which explicitly restrict `d` to `T` and justify it at length ("no `d ∉ T` let in for which `Σ.M(d)` would be undefined and that domain ill-formed"), grounding the restriction against T0 and Σ.M(d)'s own declaration in their Depends lists. D-CTG's guard `u ∈ V_1(d)` presupposes `V_1(d)` (hence `Σ.M(d)`) is defined, which by Σ.M(d)'s own declaration holds only for `d ∈ T`; for `d ∉ T` the guard is ill-typed. D-CTG's Depends cites T0 only for the *inner* candidate `v ∈ T`, never for the outer `d` — nothing in the formal contract grounds why the outer quantifier is well-formed as written.
**What needs resolving**: Restrict the outer quantifier to `(A d ∈ T, u, q : ...)` and add a Depends entry (T0 / Σ.M(d)) grounding that restriction, matching the convention already established in S8-depth and S8-fin.

### AX-1 and S8a leave `d` untyped, same gap as D-CTG
**Class**: REVISE
**Foundation**: T0 (CarrierSetDefinition); Σ.M(d) (Arrangement)
**ASN**: AX-1 (InitialEmpty), Axiom: `(A d :: dom(Σ₀.M(d)) = ∅)`; S8a (ArrangementDomainRestriction), Axiom (stated only in prose): "For every reachable state Σ and every document d, `dom(Σ.M(d)) ⊆ {t ∈ T : zeros(t) = 0 ∧ #t ≥ 2}`"
**Issue**: Same pattern as D-CTG. AX-1's bracket notation `(A d :: ...)` binds `d` with no stated domain. S8a never renders its quantifier in bracket notation at all, leaving the restriction entirely to the prose phrase "every document d," with no formal grounding — its Depends section (Σ.M(d), T4, NAT-card, NAT-zero, NAT-order, T0) never addresses why `d` ranges over `T`, unlike S8-depth's and S8-fin's explicit T0 entries for exactly this point.
**What needs resolving**: Align both claims with the S8-depth/S8-fin convention — bind `d ∈ T` explicitly (giving S8a a proper bracketed quantifier to do so) and add a Depends entry grounding the restriction against T0/Σ.M(d).

VERDICT: REVISE