# Review of ASN-0125

I checked the construction end to end: the two-allocation composite, the discipline-maintenance induction (EL-DM → EL6(v) → EL7(vi), which I confirmed is well-founded and non-circular), the arrangement-touching operations in EL9(2) and EL10 (K.μ⁻/K.μ⁺_L preserve D-CTG★/D-MIN★ by the prefix-retention and shift shapes, boundaries j=1 / j=n / only-link covered), the wp results (EL0 non-trivially false; EL6/EL7 via ASN-0086 wp Case 2), and the worked example (recomputed every address: ℓ₁=H.0.s_L.2, c₁=H.0.s_L.3, ℓ₂=P.0.s_L.1, r₁..r₂, the empty-`current` standoff). The mathematics is sound and the boundary cases hold. All cross-references are to foundation ASNs. The remaining items are the forward-reference meta-prose the active anti-bloat classifier asks me to surface.

## REVISE

### Issue 1: EDITop definition previews its own downstream proof
**ASN-0125, EDITop (Df, editlink)**: "The schema clause's `|ℓ'| = 3` guard, the forward transfer of its pre-state witnesses across the emission, and its vacuity in the unguarded case are the load-bearing steps of discipline preservation, discharged at EL7(vi)."
**Problem**: This sentence sits in the operation-definition slot but defines nothing about `editlink`. It enumerates the three "load-bearing steps" of a proof and points forward to where that proof lives (EL7(vi)). The definition is complete without it — the immediately preceding sentence already explains why `DC`'s leading conjunct excludes a retraction-class successor (that one *does* advance the predicate's meaning and should stay), and the next paragraph discharges `assert_sup`'s precondition. A precise reader must recognize this sentence as a description of the proof-to-come and skip it. This is the named pattern "new prose around a definition explains the downstream proof rather than what the definition says."
**Required**: Delete the sentence; EL7(vi) already carries the case analysis (claim-guard fires / vacuous unguarded / leading conjunct) in full.

### Issue 2: Df-CUR and EL14(e) develop the "activity-agnostic on members" point twice
**ASN-0125, Df-CUR**: "The closure and the sink test therefore consult no member link's own activity: `current` is *activity-agnostic on its members*, a property made precise and consequential in EL14(e)."
**ASN-0125, EL14(e)**: "*Activity-agnostic membership.* `current(y, Σ)` is built from `succ_o(Σ)`, whose only activity filter is the *claim*-address test `addr(e) ∉ nullified(Σ)` — never a test on the endpoint links…"
**Problem**: The observation (the sink test filters claim activity, not member activity) is stated in the definition slot with a forward-deferral ("made precise and consequential in EL14(e)"), then restated and proved in EL14(e). The definition only needs to introduce `reach_o`/`current`; the analytical observation and its consequence (`z ∈ current(y)` need not be active) belong in one place. As written the reader meets the same claim twice in different words across two sections, with the first instance carrying a "see below" pointer.
**Required**: In Df-CUR, keep at most the bare disambiguation that the sink test reads `succ_o` (i.e., operative *claims*); move the "activity-agnostic on members" statement, the forward-pointer, and the consequence to EL14(e) alone.

### Issue 3: Minor forward-pointer accretion in the substrate preliminaries
**ASN-0125, "Layer transfer"**: "…the link store changes only by `K.λ`'s fresh appends (Vocabulary fact V below)…"; **EL7(ii)**: "How the successor is then discovered … is characterised in EL11."
**Problem**: These are the lower-grade tail of the same accretion — a definition/contract slot leaning on a fact stated later in the document. Individually each is a defensible one-line navigation aid; flagged here only because they compound with Issues 1–2 as the systemic "defer to a downstream location" pattern the classifier names. The "Vocabulary fact V below" pointer in particular forward-references a lemma stated two paragraphs later in the same section, where forward-ordering buys nothing.
**Required**: Reorder so "Vocabulary fact V" precedes its first use (it is short and self-contained), removing the forward pointer; the EL7(ii) → EL11 pointer can stay if Issues 1–2 are resolved, but reconsider it as part of trimming the deferral pattern.

## OUT_OF_SCOPE

The Open Questions correctly defer the genuinely new territory (retraction authority, meta-claims targeting claims, span-level endset correspondence under reshaping, prefix-rooted subtype closure). None of these is an error in this ASN, and the ASN does not over-reach into the harness-listed retired/future operations (MAKELINK, FOLLOWLINK, READLINK, etc.). No findings.

VERDICT: REVISE
