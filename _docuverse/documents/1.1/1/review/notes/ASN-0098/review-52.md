# Review of ASN-0098

This note is mathematically thorough — every operation case is proved explicitly, edge cases (empty arrangement, `R = ∅`, empty endset, non-tight contrast) are handled, the wp analyses (LP12a/LP12b) are non-trivial, and the worked trace exercises the key postconditions concretely. I found no correctness gap, no hand-wave, no checkmark-proof, no reinvented foundation notation. The cross-references are all to foundation ASNs (0034/0036/0043/0047/0093). The remaining findings are the forward-reference and meta-prose accretion that the `review-mode.anti-bloat` classifier asks me to surface.

## REVISE

### Issue 1: Achievability paragraph is meta-framing wrapped around a forward reference
**ASN-0098, "Boundary and Width Behaviour" (Achievability)**: "The tight case is reached by the canonical construction, **instantiated concretely in the worked example below**; the one fact that construction turns on but the example shows only by instance is that the emission-frontier bound `s ⊕ ℓ ≤ inc(t_m^X(d_0), 0)` is what discharges tightness against the relevant chain's own future emissions."
**Problem**: This is essay-in-a-structural-slot. The reader must skip past the description of *what the worked example will show* to reach the actual construction argument ("Choose `ℓ = δ(n, #s)` with `s ⊕ ℓ ≤ inc(...)`…") that immediately follows it. The substantive emission-frontier reasoning is the next paragraph; this one only narrates the relationship to a downstream example.
**Required**: Delete the meta-framing; lead with the construction. The emission-frontier fact is carried by the paragraph that follows, and the example stands on its own.

### Issue 2: Cross-chain interference paragraph defers downstream
**ASN-0098, "Boundary and Width Behaviour"**: "What remains, and is not implied by the corollary, is tightness against `A_X(d_0)`'s own *future* emissions: the corollary characterises interval membership but does not say which of those chain indices are allocated at `Σ_e`. **The emission-frontier choice below supplies that.**"
**Problem**: "The emission-frontier choice below supplies that" is a forward pointer to the next paragraph in the same section — bookkeeping that defers the argument rather than making it. Combined with Issue 1, two adjacent paragraphs both defer to the same downstream emission-frontier construction before it is stated.
**Required**: Merge the cross-chain exclusion (LP-Fin Corollary) and the emission-frontier discharge into one forward-moving argument, eliminating the "supplies that below" defer.

### Issue 3: LP12a enabledness justification explains why the conjunct exists rather than stating it
**ASN-0098, LP12a**: "The enabledness conjunct is required for total correctness: at a state where K.μ⁻ is not applicable, no post-state exists, so the second conjunct **(the postcondition pullback derived below)** can hold vacuously while `discoverable_from(a, d, Σ')` is unrealisable."
**Problem**: This is the "explains why the clause is needed rather than what it says" pattern. The wp statement already carries `enabled(K.μ⁻[d, R])` as a conjunct with its own unfolded definition immediately after; this sentence is a defensive rationale for its presence. The parenthetical "(the postcondition pullback derived below)" additionally forward-references the claim's own later derivation.
**Required**: Drop the rationale sentence (or compress to a half-line). The enabledness definition that follows is sufficient; the reader does not need the meta-argument for why a wp must include enabledness.

### Issue 4: LP4 frame note is defensive scaffolding rendered moot by M1
**ASN-0098, LP4 (Frame note)**: "LP4 quantifies `d` over `dom(Σ.M) ∩ dom(Σ'.M)` so that both sides of the hypothesis and conclusion are well-defined under the same membership obligation."
**Problem**: By M1 (ASN-0093), `dom(Σ.M) ⊆ dom(Σ'.M)` on every transition, so `dom(Σ.M) ∩ dom(Σ'.M) = dom(Σ.M)` — the note records this itself in the Claims table ("downstream lifts via M1 from `d ∈ dom(Σ.M)`"). The intersection and its justifying note add a well-definedness obligation that the foundation already discharges.
**Required**: State LP4 over `d ∈ dom(Σ.M)` and drop the frame note, or keep the intersection silently without the defensive paragraph.

## OUT_OF_SCOPE

None. The note does not define claims for link type semantics or replication/BEBE; the related questions (link-to-link induced discovery, reverse discovery) are correctly parked in Open Questions as future territory, not asserted here.

VERDICT: REVISE
