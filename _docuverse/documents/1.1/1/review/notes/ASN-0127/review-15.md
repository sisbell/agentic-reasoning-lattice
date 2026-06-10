# Review of ASN-0127

I checked the algebra in full. Phase 1 (F-IMG and its four motion lemmas), Phase 2 (F-MATCH/F-FIND/F-UDIST/F-IMONO), the two-phase factoring (F-V/F-VDIST), the store-fixed keystone (F-CIL/F-CIL-perlink → F-PRES/F-INERT/F-LAMBDA), and both anchoring lanes (E-INV/E-MONO/E-CONS off LP13; D-PRES/D-NONMONO/D-CWP/D-ZERO off F-CIL) all hold. I re-derived every witness in F-IMG-SWING and the worked illustration (including the transposition reorder `π=(v₁ v₂)` giving `{L_1}↦{L_2}` and the cardinality variant `{L_1}↦{L_2,L_2'}`); the bijection-equation reindexing, the F-IMG-CONTR/F-UDIST splitting in D-CWP, and the `R=∅` boundary all check out. Foundation citations resolve correctly and no non-foundation ASN is referenced. The note defines abstract state-reading primitives and component-keyed stability guarantees — it is in scope and has not drifted.

One issue stands.

## REVISE

### Issue 1: D-NONMONO's K.μ~ clause buries its load-bearing argument under meta-commentary and duplicated witnesses

**ASN-0127, "Anchoring: discovery anchoring — D-NONMONO, third bullet (K.μ~ on `d_q`)"**: this is a single ~600-word bullet whose actual proof obligation is short but is interleaved with caveats, repetition, and example-previews that re-do work the Worked illustration already does.

The load-bearing content of the injective regime is exactly: image cardinality is pinned (F-IMG-SWING), so any image-motion under an injective reorder is between distinct equal-size sets, hence incomparable, hence F-IMONO supplies no containment to lift; `findlinks` is monotone (F-IMONO) but not order-reflecting, so the image's incomparability does *not* transfer to the discovery set; therefore non-monotonicity must be established by exhibiting an actual incomparable discovery swing — which the Worked illustration's `{L_1}↦{L_2}` does. That is the whole proof.

Surrounding it are passages that are either meta-narration of the proof or duplicated illustration:

- Meta-narration, not proof steps: *"and the two regimes must be kept separate"*; *"the discovery set's behavior must be read off directly rather than inherited from the image"*; *"the point on which this regime must not be overstated"*; *"The invalid step is therefore 'incomparable image change ⟹ incomparable discovery change'; what the injective regime does establish, and all the lemma needs, is the existence claim that…"*.
- Repetition: *"no link created or retracted"* recurs four times across the bullet and again in the Worked illustration; *"incomparable"* is restated roughly six times.
- Abstractly-asserted, non-load-bearing examples: the `{L_1}↦∅` *"strict shrink"* and the `{L_1}↦{L_1,L_2}` growth are described in prose with no arrangement or link set given — unlike the genuinely-worked `{L_1}↦{L_2}`. They illustrate "not order-reflecting," which the lemma's conclusion does not need (the lateral swing alone refutes monotonicity). The cardinality-changing swing `{L_1}↦{L_2,L_2'}` is then *previewed* here in prose and *worked* again in the Worked illustration's reorder clause — the same two swings stated twice.

**Problem**: the proof obligation a reviewer must check (does some injective reorder produce an incomparable discovery swing?) is correct but hard to extract, because it is mixed with commentary about the proof and with example sketches that duplicate the Worked illustration. This is precisely the failure mode where prose volume corrupts verifiability rather than aiding it.

**Required**: compress the K.μ~ bullet to its skeleton — (i) image moves iff `W` is not π-fixed setwise; (ii) non-injective: image-motion can be a containment either way, F-IMONO applies in that step (one witness each direction suffices); (iii) injective: image cardinality pinned ⟹ image-motion incomparable ⟹ F-IMONO unavailable, and `findlinks` is not order-reflecting so the discovery set's behavior is not inherited from the image; (iv) conclusion: non-monotone, witnessed by the Worked illustration's incomparable swing. Defer the concrete `{L_1}↦{L_2}` and `{L_1}↦{L_2,L_2'}` swings to the Worked illustration (where they already live) rather than previewing them. Either ground the `{L_1}↦∅` and `{L_1}↦{L_1,L_2}` examples in a concrete arrangement or cut them — as written they are unproven sketches of a point the lemma does not require. The `necessary-but-not-sufficient` and `sole-witness` observations are correct and may stay, but as one tightened sentence, not three.

## OUT_OF_SCOPE

The four open questions (content-keyed query through `Σ.C`, filter-set distributivity, the uniform cross-vocabulary stability wp of which D-CWP is the contraction instance, and composition with ASN-0098's projection displacement) are correctly deferred — each is new territory, not a gap in this note.

VERDICT: REVISE
