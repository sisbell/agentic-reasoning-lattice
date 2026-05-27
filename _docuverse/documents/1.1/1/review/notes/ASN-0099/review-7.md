# Review of ASN-0099

## REVISE

### Issue 1: F2/F3 conflation in worked example
**ASN-0099, Worked Example, "Verifying F2 (Completeness)"**: "F2 demands `ℓ ∈ result({α₂}, Σ)` (and tolerates no spurious `ℓ'`)."
**Problem**: F2 is completeness (matching ⟹ in result); it does *not* "tolerate no spurious" anything. The "no spurious" constraint is F3 (soundness). The parenthetical conflates the two properties.
**Required**: Remove the parenthetical from F2's verification, or rephrase as "F2 demands `ℓ ∈ result({α₂}, Σ)` (the no-spurious obligation is F3's, addressed next)."

### Issue 2: A1 introduced as "convention" but used as load-bearing axiom
**ASN-0099, "Arrangement Independence" section + Claims table**: A1 (EffectClauseExhaustivity) is introduced via "we adopt:" as a "reading convention" but labeled "introduced" in the claims table and used as a load-bearing premise in F9's derivation for K.μ⁺ and K.μ⁻.
**Problem**: An axiom about how to read other ASNs' frame clauses is a meta-axiom whose justification is "this is how authors write specs." F9's K.μ⁺/K.μ⁻ derivation collapses without A1, yet A1 has no formal grounding inside this ASN. The author's open question item 7 explicitly recognizes that revising ASN-0047's frames would eliminate the dependency.
**Required**: Either (a) state A1 clearly as a structural axiom whose validity is asserted (not "adopted"), with explicit acknowledgment that it depends on the closure of the operation vocabulary, or (b) push for the ASN-0047 frame revision and remove A1 entirely, or (c) explicitly mark F9's K.μ⁺/K.μ⁻ case as conditional pending the frame revision.

### Issue 3: Determinism and survivability for filtered/scoped forms not stated as explicit claims
**ASN-0099, "Scope" section**: "We state F8 and F9 explicitly for `findlinks` because that is the unrestricted form most often analysed; the corresponding claims for the filtered and scoped forms hold by identical arguments and the abstract specification accords them the same status."
**Problem**: "By identical arguments" without explicit statement is a Dijkstra-style hand-wave. If the filtered and scoped forms enjoy the same determinism and survivability, name the claims (F8★, F9★ or similar) and show the derivation — even briefly. The prose argument given is sound but the explicit claims are missing from the claims table.
**Required**: Add explicit claims for filtered-form determinism, filtered-form survivability, scoped-form determinism, and scoped-form survivability, each with their (one-line) derivations. They follow directly but should not be left implicit.

### Issue 4: Set-level monotonicity across reachable sequences not stated as a claim
**ASN-0099, F11 closing paragraph**: "we hold `I` fixed and let `Σ` evolve, `findlinks(I, ·)` is monotone non-decreasing in `Σ.L`."
**Problem**: This is a load-bearing consequence — it's what guarantees that an indexed implementation never has to *remove* entries during state evolution. It follows from F11 by a one-line derivation but is buried in prose rather than named as a claim.
**Required**: Add a named claim (e.g., F11★ or F15) stating `findlinks(I, Σ) ⊆ findlinks(I, Σ')` for every reachable `Σ →* Σ'`, with a short derivation citing F11.

### Issue 5: Implementation section drifts toward implementation specifics
**ASN-0099, "What Completeness Demands of Implementations"**: Discusses indexes, atomic index-with-link writes, crash recovery, fallback paths, and durability obligations.
**Problem**: While framed as "demands of implementations," the middle paragraphs prescribe a particular implementation pattern (index + atomic write + fallback). The abstract spec demand is just F2 ∧ F3 — `result(I, Σ) = findlinks(I, Σ)`. Discussion of K.λ-time index maintenance and crash-recovery fallback paths is implementation guidance, not abstract specification.
**Required**: Either remove the middle paragraphs (keeping the opening and closing that correctly frame completeness as result-equality) or relocate to an implementation-notes section explicitly outside the abstract spec.

### Issue 6: Image function not given a named property claim
**ASN-0099, "The Image Set" section**: `image(R, d, Σ)` is defined but no F-style claims characterize its properties (set-additivity in R, behavior under empty R, behavior on R disjoint from `dom(Σ.M(d))`, idempotence of silent projection).
**Problem**: F13 (SetAdditive) is stated for `findlinks` over I-input. The corresponding V-side additivity for `findlinks_V` is derived in one sentence of prose but is not named. Similarly, image's behavior on boundary inputs is discussed in the "Empty Query" section but not formalized.
**Required**: Add at least an image-additivity claim: `image(R₁ ∪ R₂, d, Σ) = image(R₁, d, Σ) ∪ image(R₂, d, Σ)`. The V-side additivity for `findlinks_V` would then follow as a one-line composition.

## OUT_OF_SCOPE

### Topic 1: Querying with addresses outside `dom(Σ.C) ∪ dom(Σ.L)`
**Why out of scope**: The ASN explicitly defers this in its open questions. The match predicate handles such addresses mechanically (intersection is well-defined for any `I ⊆ T`), but the operational meaning is acknowledged as unsettled. Future ASN territory.

### Topic 2: Multi-instance / partition tolerance for the link store
**Why out of scope**: The ASN is stated against a single state `Σ` per ASN-0093's SequentialTransitionAxiom. Cross-instance consistency belongs to a future BEBE-layer ASN.

### Topic 3: Inverse direction (resolving result endsets back to V-positions)
**Why out of scope**: FOLLOWLINK / RETRIEVEENDSETS is explicitly identified as a separate operation with its own specification obligations. FINDLINKS' scope ends at returning the link set.

### Topic 4: Access control as a filter
**Why out of scope**: The ASN mentions access control as composable with discovery but declines to formalize it. Belongs in a separate access-control ASN.

VERDICT: REVISE
