# Review of ASN-0086

I checked the arithmetic of the worked sketch (`a₁ = 1.0.1.0.1.0.2.1` through `b₂ = 1.0.1.0.1.0.2.4`), the freshness discharges in R0, the antichain argument in R0a (both cross-home and same-home cases), the chain inductions in R0a-Cor1/Cor2, and the wp derivations. The mathematics is sound and the proofs are, for once, mostly complete to the level the standards demand. The findings below are predominantly the meta-prose accretion the `review-mode.anti-bloat` classifier flags, plus one scope observation.

## REVISE

### Issue 1: The R6a-vs-R6b distinction is stated three times
**ASN-0086, R6b (body, proof, and Properties table)**:
- Body: "This is a *within-state* claim, distinct from R6a's cross-`→` persistence (R6a's formula instead relates `nullified(Σ)` to `nullified(Σ')` across a transition; here both sides are evaluated at the single state Σ)."
- Proof: "(That a nullification, once established, persists across `Σ → Σ'` is R6a, proved separately.)"
- Table: "Cross-`→` persistence is R6a."

**Problem**: The same orientation note — "R6b is within-state, R6a is cross-transition" — appears in three slots within one short property. This is the "two paragraphs say the same thing in different words" pattern. The reader who has read the formula of each (one quantifies `Σ`, the other `Σ → Σ'`) does not need the distinction restated, let alone thrice.
**Required**: Keep the distinction once (the body parenthetical suffices) and delete the proof aside and the table clause.

### Issue 2: The `a ∈ A_rel^Σ` restriction rationale is repeated across three properties
**ASN-0086, Definition — Nullified / R6a proof / R6b**:
- Nullified: "The set-builder restriction `a ∈ A_rel^Σ` is intentional: only tuple addresses are eligible for nullification..."
- R6a proof: "The codomain is `℘(T)` — the full tumbler space — not the state-dependent address universe `A^Σ`; coverage may include addresses outside `dom(Σ.C) ∪ dom(Σ.L)`..."
- R6b: "The restriction `a ∈ A_rel^Σ` is carried for the same reason R6a carries it: `coverage`'s codomain is `℘(T)`, not `A^Σ`, so `coverage(G')` may include ghost or content addresses..."

**Problem**: The identical justification — coverage's codomain is `℘(T)`, so the `A_rel` restriction confines `nullified` to tuple addresses — is given essentially verbatim in three places. R6b explicitly says it carries the restriction "for the same reason R6a carries it," which is itself the tell of relocated/duplicated prose.
**Required**: State the codomain/restriction rationale once at the `nullified` definition (its natural home) and have R6a/R6b cite it without re-deriving.

### Issue 3: The `→` definition inlines ASN-0093 emission forms already fixed in foundation
**ASN-0086, "State transition relation"**: "a *K.α-step* — content allocation, extending `dom(Σ.C)` with a fresh content address `a` produced by `d`'s content sub-allocator `A_C(d)` ... (first-emission `a = [d.0.s_C.1]` or subsequent-emission `a = inc(a_prev, 0)`); a *K.λ-step* — ... (first-emission `ℓ = [d.0.s_L.1]` or subsequent-emission `ℓ = inc(ℓ_prev, 0)`)."

**Problem**: `→ ≡ K.σ ∪ K.α ∪ K.λ` already defines the relation by reference to ASN-0093. The inlined first/subsequent emission forms restate the K.α/K.λ contracts verbatim from the foundation, adding no notation this note uses (the emission forms are re-derived where actually needed, e.g. in R0 and `a_emit`). This is a foundation restatement in a definitional slot.
**Required**: Reduce the bullets to "K.σ extends `dom(Σ.M)`, K.α extends `dom(Σ.C)`, K.λ extends `dom(Σ.L)`, each at a fresh key per its ASN-0093 contract," and drop the inlined emission arithmetic.

### Issue 4: WP Case 2 builds out a direct-K.λ-caller regime analysis the note's own operation set never reaches
**ASN-0086, Weakest-Precondition Analysis, Case 2**: "We compute the wp for a *direct K.λ caller* — the most permissive scope ... Under this scope all three regimes below are live"; and later "The substrate-conformance hypothesis is load-bearing and cannot be dropped: over the bare state-local-conforming domain ... Concretely, instantiate the non-conformance witness `a ≼ a''` ..."

**Problem**: The four-conjunct wp, regime (ii) crafted-span retractions, and the load-bearing-conformance necessity witness all characterize callers/states outside the relational layer. The note then states the "Relational-layer specialization" collapses the wp to `d ∈ dom(Σ.M) ∧ K ∈ T_admissible`. Since the relational layer (this note's actual operation set `{Emit_K, Observe_K, Nullify}`) is substrate-conforming and unit-depth-disciplined by construction, the elaborate direct-caller machinery analyzes regimes the layer excludes. Per the anti-bloat guidance ("a paragraph imagines a case the claim's carrier or precondition already excludes"), the regime-(ii) and load-bearing-witness paragraphs are candidates for removal or relocation to the foundation that actually owns direct K.λ.
**Required**: Either (a) scope WP Case 2 to the relational layer's reachable states (the two-conjunct form) and drop the direct-caller regimes, or (b) state explicitly and briefly that the direct-caller wp is a foundation-level observation about K.λ retained here only for contrast, and compress regimes (ii)/(iii) and the necessity witness to one sentence each.

## OUT_OF_SCOPE

### Topic 1: Visibility coupling between `L_K` and arrangements `Σ.M`
**Why out of scope**: The note's first Open Question (relational predicates that depend on whether from/to content is currently visible in some document) requires invariants relating the link store to arrangement state. ASN-0093's M2 keeps every arrangement empty, so no such coupling can yet be exercised; this belongs to a future ASN that admits non-empty arrangements, not to a revision here.

VERDICT: REVISE
