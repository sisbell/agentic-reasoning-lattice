# Review of ASN-0131

I checked the mathematics throughout — the touch definition, the worked instance's type-disjointness argument, RE-UDIST's `Avail` factoring, RE-SEL's reduction to `findlinks_V ∩ addressable`, RE-CWP's weakest precondition, and the retraction argument (RE-RET) with its explicitly-flagged `coverage(Θ) ∩ dom(Σ.C) = ∅` hypothesis. The reasoning is sound; the ASN-0086 bridge is correctly scoped to the one foundation that lives at a different layer; the transition vocabulary is comprehensively swept in the stability section. The findings below are all prose accretion of the kind this note's `review-mode.anti-bloat` classifier targets, not correctness gaps.

## REVISE

### Issue 1: the "insert/delete are shift primitives, not K.μ~" point is stated five-plus times in one paragraph

**ASN-0131, "Under editing of the queried document"**: a single paragraph makes the same distinction repeatedly:
1. "The user-facing *insert* and *delete* that **shift** content are not these atomic movers"
2. "The two are not competing descriptions of one transition: the atomic `K.μ⁺` *appends* ... whereas an ASN-0082 insert *shifts* existing content ... a genuinely different arrangement transformation"
3. "We take insert and delete here as ASN-0082 displacement primitives in their own right, not as `K.μ` composites."
4. "so a shift is no domain-preserving `K.μ~` reorder ... and, taken as a primitive, its effect on the image is read off the displacement directly rather than through F-IMG-SWING"
5. "(Were the shift instead decomposed into atomic `K.μ` steps, the existing-content motion would live in a domain-preserving `K.μ~` component and route through F-IMG-SWING; we do not take that route.)"

and then once more two sentences later: "it is the displacement itself, not F-IMG-SWING (whose `K.μ~` precondition a shift does not meet), that grounds the swing."

**Problem**: The load-bearing content is one sentence: *insert/delete shift content (I3/D-SHIFT), so a fixed region's image both gains and loses I-addresses — it swings non-monotonically, read off the displacement.* Everything else — "not these atomic movers," "not competing descriptions," "not `K.μ` composites," "no domain-preserving `K.μ~` reorder," and the parenthetical (5) imagining a decomposition the note immediately disclaims ("we do not take that route") — is defensive scaffolding that does not advance the argument. The reader who wants to follow how the image moves must wade through six assertions that the shift is-not-a-`K.μ~`. The parenthetical is the clearest waste: it speculates about an alternative routing whose only stated conclusion is that the note rejects it.

**Required**: State the displacement framing once — insert/delete shift content per I3/D-SHIFT (ASN-0082), so the image swings and is read off the displacement directly, non-monotone. Delete the repeated "not `K.μ~` / not `K.μ` composite / not competing descriptions" assertions and the disclaimed-decomposition parenthetical.

### Issue 2: key claims restated verbatim-ish across sections

**ASN-0131, "The unit of the answer" and worked instance**: the same epigram appears twice — "The anchoring is laid bare; the connection is not made followable." (RE-UNIT discussion) and "the from-end is laid bare; the connection is not made followable." (worked-instance RE-UNIT bullet).

**ASN-0131, transclusion section and RE-EDIT**: RE-IDENT is given in full in the transclusion section ("The operation's content-level answer is therefore arrangement-independent even though its *selection* ... is arrangement-mediated"), then again at the head of RE-EDIT — where the note asserts "One invariant underlies this whole section, and we state it once: each surfaced endset's coverage is permanent (RE-IDENT)." The "we state it once" is contradicted by the earlier transclusion-section statement (and by the claims-table entry).

**Problem**: This is the "two slots say the same thing in different words" pattern. The "we state it once" claim is self-falsifying, which makes the redundancy conspicuous.

**Required**: State RE-UNIT's epigram and RE-IDENT once each, at the point where each is first load-bearing; reference rather than re-state thereafter. If RE-EDIT genuinely needs RE-IDENT, cite it ("by RE-IDENT") rather than re-deriving "coverage is permanent."

### Issue 3: claims-table entries duplicate prose derivations

**ASN-0131, Claims Introduced, RE-RET**: the table entry carries justification, not just the claim: "The emitter `b` is itself addressable by the general fresh-`K.λ`-output addressability fact (its to-set targets `ℓ ≠ b`, so `b` does not retract its own emitter address), and its nullifying reach is confined to `ℓ` alone (R-Scope, R0a, ASN-0086)." RE-EDIT's entry is a similar run-on re-listing of every transition's image-effect with its citation.

**Problem**: A claims table is a structural slot for terse statements. The actual claim of RE-RET is "*a pair `(i,e)` that `ℓ` bore drops iff `ℓ` was its sole addressable bearer, under the discipline and the `coverage(Θ)` hypothesis*." The `b`-addressability and reach-confinement reasoning is the proof — already present, correctly, in the prose — and re-stating it in the table duplicates content.

**Required**: Reduce RE-RET and RE-EDIT table entries to the claim plus its operative conditions; leave the supporting derivation (b-addressability, R-Scope confinement, per-transition citations) to the body where it already lives.

## OUT_OF_SCOPE

I verified the seven Open Questions route genuinely future territory and do not smuggle in this ASN's obligations: entirety-vs-touching-spans (OQ1, RE-WHOLE held provisional), multiplicity preservation (OQ2), rendered-into-V-order answers (OQ3), intersection-distributivity (OQ4, correctly distinguished from the derived union half RE-UDIST), cross-store completeness (OQ5), type-slot-against-content (OQ6, the sole remaining exception to RE-RET's net-removal-only result), and link-subspace regions (OQ7). These are correctly deferred; nothing belonging in a future ASN is treated as a defect of this one, and the note correctly cites (does not rebuild) ASN-0127's image machinery and existence/discovery taxonomy and distinguishes RE from FINDLINKSFROMTOTHREE without specifying it.

VERDICT: REVISE
