# Review of ASN-0087

## REVISE

### Issue 1: "bounded" terminology in cascade discussion is non-standard
**ASN-0087, Side Effects on Prior Links' Discoverability**: "We claim this cascade is bounded — no chain of MAKELINK invocations can violate any per-state invariant of the substrate."
**Problem**: "Bounded" typically denotes finiteness of length, but the argument that follows establishes invariant *preservation* across arbitrary-length sequences, not length-boundedness. A reader expecting a termination argument may be confused by the term, then re-orient against the em-dash. The actual claim — invariant preservation under composition — is correct and well-supported.
**Required**: Substitute "invariant-preserving" or "safe under composition" for "bounded", or expand the gloss to make the redefinition unambiguous.

### Issue 2: M-Inv-Trans claim lists P3 alongside its constituents
**ASN-0087, M-Inv-Trans**: "M1, L12, P0, P1, P2, and P3 hold; S9 follows from P0. ... P3 is the conjunction P0 ∧ P1 ∧ P2 ∧ L12."
**Problem**: P3 is defined as the conjunction of P0, P1, P2, and L12. Listing both the conjunction and its conjuncts as items to be discharged is redundant — once the four constituents are discharged, P3 holds automatically. The redundancy is harmless but obscures the logical structure: a reader cross-checking ExtendedTransitionInvariants might wonder if there is hidden content in P3 beyond the conjuncts.
**Required**: Either drop P3 from the enumeration (it is implied) or replace the constituents with "P3 (= P0 ∧ P1 ∧ P2 ∧ L12)" so the dependency is one-directional.

### Issue 3: M1's role in the wp membership clause needs sharper attribution
**ASN-0087, M-WP / Weakest Precondition section**: "By M1 (with equality at MAKELINK), the membership clause is equivalent to d_target ∈ dom(Σ'.M)."
**Problem**: M1 alone only gives `dom(Σ.M) ⊆ dom(Σ'.M)` — the inclusion, not the equality. The equality at MAKELINK comes from the *fact* that neither K.λ nor K.μ⁺_L modify `dom(M)` (K.λ's frame on M; K.μ⁺_L's effect extends `dom(M(d))` but not `dom(M)`). M1 supplies the `⊆` direction; the `⊇` direction is a frame consequence not entailed by M1 itself. The current phrasing risks being read as "M1 gives equality" when it does not.
**Required**: Reword to e.g. "By M1 combined with the K.λ and K.μ⁺_L frames on `dom(M)` (giving equality at MAKELINK), the membership clause is equivalent to d_target ∈ dom(Σ'.M)."

### Issue 4: Worked example does not exercise the reflexive-endset or prior-link cascade cases
**ASN-0087, A Worked Example**: The example covers home-document and cross-document discoverability through arrangement-reach, plus the inert type endset. The reflexive-endset case (M-Reflexive) and the prior-link discoverability cascade (M-PriorLinkDisc) are treated abstractly but not exercised concretely.
**Problem**: Per the depth standard ("verify key postconditions against at least one specific scenario"), M-Reflexive and M-PriorLinkDisc are non-trivial derived guarantees whose mechanics deserve concrete verification. A reader might accept the abstract argument but miss a subtle behavior of `v_ℓ ∈ project(ℓ, i, d, Σ')` in the reflexive case, or the LP18-resurrection pattern when a prior link's endset covers the freshly allocated `ℓ`.
**Required**: Add a brief second sub-example — either a reflexive endset (deliberate `ℓ ∈ coverage(eᵢ)`) showing `v_ℓ ∈ project(ℓ, i, d, Σ')`, or a prior link `ℓ'` whose endset covers `ℓ` showing the discoverability transition `¬discoverable_from(ℓ', d, Σ) ∧ discoverable_from(ℓ', d, Σ')`. One worked computation suffices; do not over-elaborate.

### Issue 5: L1c chain construction is correct but distorts the section's readability
**ASN-0087, Per-State Invariants at Σ' / L1c discharge**: The chain construction occupies roughly 60 lines covering both an existence chain (with step-by-step TA5 inspection) and a uniqueness table. Each step is correct and necessary for full rigor, but the result is that L1c — one of 31 per-state invariants — dominates the section disproportionately, while neighboring invariants get a single-line discharge.
**Problem**: The uniqueness argument exceeds L1c's existential obligation; L1c only demands existence of the chain. The uniqueness is supplementary. Bundling it inline with the existence proof makes the discharge of L1c look load-bearing in ways it is not.
**Required**: Move the uniqueness table to a separate paragraph after the existence verification, labelled clearly as a strengthening beyond L1c's existential. Alternately, defer the uniqueness analysis to an appendix or to a future ASN focused on chain-canonicalisation, keeping the L1c discharge proportionate to its peers.

### Issue 6: Cascade-vacuity dependence on Store Monotonicity★ is implicit
**ASN-0087, Side Effects on Prior Links' Discoverability**: "When ℓ' was authored under standard authoring at its own authoring state — StandardAuthoring(Σ.L(ℓ').eᵢ, Σ_{ℓ'}) holds at the state Σ_{ℓ'} at which ℓ' was incorporated — no such endset can cover a future fresh ℓ, and the side effect is vacuous."
**Problem**: The argument requires that K.λ's freshness `ℓ ∉ dom(Σ_ℓ.C) ∪ dom(Σ_ℓ.L)` (evaluated at the allocation state `Σ_ℓ`) implies `ℓ ∉ dom(Σ_{ℓ'}.C) ∪ dom(Σ_{ℓ'}.L)` (the authoring state of the prior link `ℓ'`, which precedes `Σ_ℓ`). This implication uses Store Monotonicity★ (ASN-0098): if `Σ_{ℓ'} →* Σ_ℓ` then `dom(Σ_{ℓ'}.C) ∪ dom(Σ_{ℓ'}.L) ⊆ dom(Σ_ℓ.C) ∪ dom(Σ_ℓ.L)`, so the freshness at `Σ_ℓ` transfers backward. The ASN states the conclusion but does not name this premise.
**Required**: Cite Store Monotonicity★ explicitly in the vacuity argument, since the temporal direction of the inclusion is load-bearing.

## OUT_OF_SCOPE

None to flag. The ASN's own *Open Questions* section enumerates eight reasonable topics for future ASNs (endset well-formedness for forward-reaching spans, atomicity-layer placement, semantic deduplication, deferred-consistency models, late-allocation discoverability behavior, V-position movement under REARRANGE, the structural distinction between pre- and post-completion states, and ghost-type-endset semantics). These cleanly identify what is deferred without flagging anything that should have been in scope.

VERDICT: REVISE
