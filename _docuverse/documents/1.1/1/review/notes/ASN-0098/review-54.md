# Review of ASN-0098

The mathematics here is, on the whole, sound — the LP9/LP10/LP11 exact-difference formulas are properly proved by mutual inclusion, the LP-Fin finitude argument is genuinely worked through its structural sub-cases, and the boundary cases (empty arrangement, `R = ∅`, empty endset) are addressed rather than waved at. My findings are almost entirely the accretion this note was flagged for: re-derivation of results already established, and roadmap/rationale prose that the reader must step around.

## REVISE

### Issue 1: LP12b re-derives `dom(Σ.L) ⊆ F`, which LP-Sub already proves
**ASN-0098, LP12b**: "We derive `dom(Σ.L) ⊆ F` via an explicit three-step citation chain. First, by ChainMembershipForOrigin (ASN-0093)... Second, by FirstEmission and ChainDiscipline (ASN-0093)... Third, the document parameter `d'` is T4-valid... so `dom(Σ.L) ⊆ F`."
**Problem**: LP-Sub already establishes `dom(Σ.C) ∪ dom(Σ.L) ⊆ F` from exactly these citations (ChainMembershipForOrigin, FirstEmission, ChainDiscipline, M0). LP12b reproduces the full derivation verbatim instead of citing the lemma stated a few paragraphs earlier. This is the duplicate-derivation pattern: two passages proving the same thing in different words.
**Required**: Replace the three-step paragraph with "by LP-Sub, `dom(Σ.L) ⊆ F`." The parenthetical StoreT4Validity aside can stay if needed, but the chain re-citation should be deleted.

### Issue 2: Achievability section is roadmap/meta-prose deferring to the worked example
**ASN-0098, "Achievability" (after the tight definition)**: "The tight case is reached by the canonical construction, instantiated concretely in the worked example below; the one fact that construction turns on but the example shows only by instance is that the emission-frontier bound `s ⊕ ℓ ≤ inc(t_m^X(d_0), 0)` is what discharges tightness..." and "Cross-chain interference is excluded by LP-Fin Corollary, which already establishes... What remains, and is not implied by the corollary, is tightness against `A_X(d_0)`'s own *future* emissions: the corollary characterises interval membership but does not say which of those chain indices are allocated at `Σ_e`. The emission-frontier choice below supplies that."
**Problem**: This is prose *about* the proof's structure — what the corollary does and does not imply, what the example shows "only by instance," what "the emission-frontier choice below supplies" — rather than the argument itself. Two sentences forward-point to the same downstream worked example ("instantiated concretely in the worked example below," "supplies that" / "below"). The reader must skip this to reach the actual construction (the `ℓ = δ(n, #s)` with `s ⊕ ℓ ≤ inc(t_m^X(d_0), 0)` choice), which is self-contained.
**Required**: Delete the meta-discussion and keep only the construction itself: the emission-frontier choice and the one-sentence ChainMembershipForOrigin contiguity argument that discharges tightness. The relationship to LP-Fin Corollary is already evident from the construction's reliance on it.

### Issue 3: Rationale-for-`F`-definition prose accreted at two sites
**ASN-0098, `F` definition**: "This direct check covers registered and unregistered `d` uniformly, since it appeals only to the form `[d, 0, s, k]` and not to any active chain."
**ASN-0098, LP19a**: "F's quantification over *all* T4-valid document tumblers — including those registered only after `Σ_e` — is what makes this membership hold even when `d_alloc` was registered later along the sequence `Σ_e →* Σ`."
**Problem**: Both sentences explain *why `F` is quantified the way it is* rather than advancing the proof. The load-bearing facts ("every `a ∈ F` satisfies T4 from its structural form"; "`a_new ∈ F`") are stated immediately adjacent; the "covers... uniformly, since" and "is what makes this membership hold" framings are defensive justification of the definition's shape — the axiom/definition-rationale pattern.
**Required**: Drop both rationale clauses. The structural T4 check and the `a_new ∈ F` membership stand on their own; registration-independence is a property the reader reads off the form, not a point that needs arguing.

### Issue 4: Worked trace re-derives chain mechanics already established upstream
**ASN-0098, "A Worked Trace"**: "All four share the common chain length `#d_alloc + 3`: FirstEmission (ASN-0093) fixes the chain's first element at `[d_alloc, 0, s_C, 1]` with `#E = 2`, hence length `#d_alloc + 3`, and ChainDiscipline (ASN-0093) advances each subsequent element by `inc(·, 0)`, which by TA5(c) of ASN-0034 modifies only the significant position and preserves length. By ChainEnumerationInjectivity (ASN-0093) the enumeration `n ↦ tₙ` is strictly increasing..."
**Problem**: The trace re-proves chain length-uniformity, sibling ordering, and injectivity from first principles — facts already fixed by the cited lemmas and used in identical form in the F-definition and LP-Sub. A worked example should *exhibit* the numbers, not re-derive the substrate lemmas.
**Required**: Replace with the conclusion plus a single citation: `i₁ < i₂ < i₃ < i₄` are consecutive `A_C(d_alloc)` chain elements of common length `#d_alloc + 3` (ChainDiscipline, ChainEnumerationInjectivity, ASN-0093). Drop the TA5(c) re-derivation.

## OUT_OF_SCOPE

### Topic 1: Discoverability preservation for link-canonical endsets under content-emptying contraction
The final Open Question (LP-Fin Corollary at the link subspace not yielding disjointness) correctly defers the inverse of LP12b to future work rather than asserting it here. This is appropriately scoped as an open question, not a gap in the current claims.

### Topic 2: Reverse-discovery, V-order/I-order correspondence, cross-document operation comparability
The Open Questions list these as future invariants. They are genuinely new territory (new primitives or new guarantees), not omissions in the projection-displacement model this ASN establishes.

VERDICT: REVISE
