# Review of ASN-0047

## REVISE

### Issue 1: K.μ⁺ uses C' and R' in two incompatible senses

**ASN-0047, K.μ⁺ (Arrangement extension)**: The frame states `C' = C`, meaning K.μ⁺'s post-state content store equals its pre-state. But the referential integrity case analysis then says:

> "(i) a ∈ dom(C') \ dom(C) — freshly allocated, co-occurring with K.α."

Under the frame `C' = C`, `dom(C') \ dom(C) = ∅` — case (i) is vacuously empty. The case analysis is clearly describing the *composite* transition's pre/post states (before K.α vs after K.α), not K.μ⁺'s own local states.

The same pattern appears in J1's derivation:

> "wp(K.μ⁺, Contains(Σ') ⊆ R') = (A a : a ∈ ran(M'(d)) \ ran(M(d)) : (a, d) ∈ R')"

K.μ⁺'s frame gives `R' = R`, so the wp should yield `(a, d) ∈ R`, not `(a, d) ∈ R'`. The formula uses `R'` in the composite sense (after K.ρ co-occurs), not K.μ⁺'s local sense.

**Problem**: The same prime notation means "post-state of this elementary transition" in frames and "post-state of the composite transition" in preconditions and case analyses. A reader applying the frame substitution `C' = C` to the case analysis gets a contradiction.

**Required**: Either (a) introduce distinct notation for composite-level pre/post states (e.g., `Σ_init`, `Σ_final` for the composite, reserving primes for elementary transitions), or (b) relocate the case (i)/(ii) analysis and the J1 wp computation to the coupling section where composite transitions are explicitly discussed, or (c) add a sentence at the start of K.μ⁺'s precondition block stating that `C'` here refers to the composite's final state, not K.μ⁺'s local post-state.

### Issue 2: Worked example does not verify P8

**ASN-0047, Worked example**: The final paragraph states:

> "The three steps exercise J0, J1, J2, J4, P4, P5, P6, and P7"

P8 (entity hierarchy) is introduced in this ASN and is non-trivially exercised by the fork step — K.δ creates d₂ = 1.0.1.0.2 with parent(d₂) = 1.0.1, which must be in E. The verification is straightforward (parent is in E₁ by the starting state), but P8 is never checked.

**Problem**: P8 is among the main new invariants of this ASN. Omitting it from the verification checklist breaks the pattern of thorough per-step checking that the example otherwise maintains.

**Required**: Add P8 verification to the fork step (parent(d₂) = 1.0.1 ∈ E₁, and all existing non-node entities retain their parents in E₂ ⊇ E₁) and include P8 in the summary sentence.

### Issue 3: K.μ⁺ S8-depth precondition is stated per-position but the invariant is cross-position

**ASN-0047, K.μ⁺ (Arrangement extension)**: The precondition says:

> "new V-positions satisfy S8a (all components strictly positive) and S8-depth (uniform depth within subspace)"

S8a is a per-position property — each individual position can satisfy it independently. S8-depth is a cross-position property: *all* V-positions in a subspace share the same depth. A new position satisfying S8-depth "on its own" is meaningless — it must match the depth of existing positions in its subspace.

**Problem**: The precondition's phrasing suggests S8-depth is a property of the new positions alone. A reader could conclude that adding depth-3 positions to a subspace currently at depth-2 satisfies the precondition, since the new positions have "uniform depth" among themselves.

**Required**: State the precondition as: "new V-positions satisfy S8a, and the resulting arrangement `M'(d)` satisfies S8-depth" — or equivalently, "for each new V-position v, `#v` equals the depth of existing positions in the same subspace of d."

## OUT_OF_SCOPE

### Topic 1: J0 does not bind fresh content to its origin document

J0 requires every fresh I-address to appear in *some* arrangement, but does not require it to appear in `origin(a)`'s arrangement. Content allocated under d₁'s prefix could be placed only in d₂, leaving d₁ with no record. The provenance pair `(a, d₁)` would never enter R. No invariant (P4, P6, P7) would be violated, yet the structural attribution guarantee of S7 would be "detached" — origin identifies the allocating document, but the system need never have placed the content there.

**Why out of scope**: This is a constraint on named operations (INSERT allocates under the inserting document and places content there). At the elementary transition level, J0's weakness is deliberate — it states the minimal coupling. A future ASN on operations can strengthen J0 to require placement in `origin(a)`.

### Topic 2: Provenance semantics under transitive transclusion chains

If document d₁ creates content a, d₂ transcludes a from d₁, and d₃ transcludes a from d₂, then R records `(a, d₁)`, `(a, d₂)`, and `(a, d₃)` — but the chain of provenance (who got it from whom) is not captured. R is flat, not a graph.

**Why out of scope**: The ASN correctly defines R as recording *which* documents have contained *which* content. The *path* of content through documents is a higher-level concern, likely requiring version history or a separate provenance-chain structure.

VERDICT: REVISE
