# Review of ASN-0131

This is a careful, largely rigorous note. The worked instance is excellent and exercises every distinctive postcondition; the contraction wp (RE-CWP) is a genuine, non-trivial analysis correctly shown to be strictly finer than D-CWP; the field-agreement disjointness arguments (e₃, the retraction to-set) are airtight. The problems are concentrated in the retraction/addressability machinery and in how the standing assumption is grounded.

## REVISE

### Issue 1: "any fresh K.λ output is addressable" is false for self-targeting retractions

**ASN-0131, "Stability … Under link emission"**: "under the standing unit-depth retraction discipline, **any fresh K.λ output is addressable in its post-state.** That discipline makes every pre-existing retraction to-set unit-depth at a prior target, while R0a/FlatLinkDomain (ASN-0086) makes dom(Σ'.L) a prefix-antichain, so no pre-existing retraction to-set covers the fresh, distinct address (this is the vacuity of wp Case 2's third conjunct, ASN-0086)".

**Problem**: The supporting argument rules out only **pre-existing** retraction to-sets — it discharges exactly the *third* conjunct of ASN-0086's wp Case 2. But addressability of a fresh emission requires the full wp, including the *second* conjunct `(K ≁ R ∨ a_emit(Σ, d) ∉ coverage(G))`, which guards against *self*-nullification. ASN-0086's `Nullify` permits a self-emit (P-tgt: `a = a_emit(Σ, d_retr)`); such a step emits `b = a_emit` with to-set `{(b, δ(1, #b))}`, whose coverage `{t : b ≼ t}` contains `b`, so `b ∈ nullified(Σ')` and `b` is **not** addressable. A self-emit `Nullify` is a fresh K.λ output (the note itself states "a retraction is itself a link emission"), so the universal claim has a concrete counterexample — and it contradicts ASN-0086's own wp Case 2 second conjunct.

This is the classic gap: showing no *prior* operation nullifies the fresh address does not establish that the *freshly emitted* operation does not nullify itself.

The note's substantive conclusions survive (in RE-RET, `b` targets `ℓ ≠ b`, so non-self-targeting; the emission monotonicity is separately scoped to `K ≁ Θ`), but the stated lemma is wrong as written and is the kind of general fact a downstream ASN could cite.

**Required**: Scope the claim to non-self-targeting emissions — e.g. "any fresh K.λ output that does not retract its own emitter address (`a_emit ∉ coverage` of its own to-set) is addressable" — or invoke the full wp Case 2 (both the second and third conjuncts), not the third alone.

### Issue 2: The standing assumption is grounded in the wrong layer

**ASN-0131, "The unit of the answer"**: "equivalently, we work over the layer-reachable states of ASN-0086's relational layer, where the discipline holds at every reachable state by induction."

**Problem**: ASN-0086's relational layer is defined over `→ ≡ K.σ ∪ K.α ∪ K.λ` (StateTransition, ASN-0086), sitting on the ASN-0093 substrate, where every allocated document carries the **empty** arrangement (M2, ASN-0093) and there is no arrangement-populating transition. So *every* layer-reachable state of ASN-0086 has `Σ.M(d) = ∅` for all `d`. But ASN-0131 is built over ASN-0047 and its entire purpose is to query **populated** arrangements (the worked instance has four mappings; `image(W, d, Σ)` must be non-empty for RE to return anything). Populated arrangements require K.μ⁺ steps that ASN-0086's layer does not contain. Hence ASN-0131's states are *not* ASN-0086-layer-reachable, and the asserted equivalence is false.

This is not merely cosmetic: the retraction-stability argument applies ASN-0086's link-store lemmas (R0a, R-Scope, R6a, `nullified`) at populated-arrangement states — i.e. outside those lemmas' stated `→*`/layer-reachable domain — and the false equivalence is what is supposed to license that application. The lemmas *do* transfer (only K.λ touches `Σ.L`; K.μ/K.δ/K.ρ/K.α leave it fixed), but the note never argues the transfer; it substitutes the inaccurate layer claim for it.

**Required**: Drop the "equivalently, ASN-0086 layer-reachable" clause and carry the unit-depth discipline as a standing assumption directly over ASN-0047's vocabulary, noting it is preserved because only K.λ touches `Σ.L` (and the discipline restricts retraction-typed K.λ to `Nullify`); state explicitly that the imported ASN-0086 link-store lemmas hold at ASN-0047-reachable states because the added transitions (K.μ, K.δ, K.ρ) frame `Σ.L`.

### Issue 3: Duplicated rationale (anti-bloat)

**ASN-0131**: the wide-retraction rationale appears twice — in "The unit of the answer" ("such a value could pre-nullify links not yet allocated; the discipline is precisely what excludes it") and again in "Under link emission" ("absent the discipline a wide pre-existing retraction could pre-nullify ℓ_new, which is exactly what the standing assumption excludes"). Likewise the content-identity-invariance point ("coverage permanent / spans don't move, only membership") is restated three times: in the transclusion section ("the content-level answer … is invariant … arrangement-independent"), in the K.μ~ stability bullet ("no surfaced endset's spans change shape"), and again in the "Through all of this" editing recap.

**Problem**: This is the "same thing in different sections" / "axiom rationale re-litigated at the use site" pattern the anti-bloat classifier targets. The second wide-retraction statement re-justifies the standing assumption rather than simply invoking it; the editing recap re-states RE-IDENT a third time.

**Required**: State the wide-retraction rationale once (at the standing assumption) and at the use site invoke the discipline without re-deriving what would happen absent it. Collapse the repeated content-identity-invariance statements into a single citation of RE-IDENT at the head of the stability section.

## OUT_OF_SCOPE

None. The note stays within the RETRIEVEENDSETS query; it cites (does not rebuild) ASN-0127's image machinery and existence/discovery taxonomy, withholds link identities (no overlap with FINDLINKSFROMTOTHREE / counting / pagination), and defers genuinely new territory (rendered V-order answer, intersection-distributivity, non-co-resident stores, type-slot/content matches, link-subspace regions) to its Open Questions appropriately.

VERDICT: REVISE
