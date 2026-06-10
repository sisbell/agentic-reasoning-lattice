# Review of ASN-0127

This is a careful note, and most of its machinery holds up. The two-phase factoring is clean, the keystone meta-lemma F-CIL and its per-link weakening are correctly stated and used, the existence/discovery anchoring distinction is sharply drawn (the LP3★-vs-LP13 point in E-INV is genuinely good), and the worked illustration verifies the principal behaviors against concrete tumblers. The problems are localized to the **D-NONMONO K.μ~ (reorder) clause**, where the reasoning does not survive contact with the non-injective arrangements the note itself admits.

## REVISE

### Issue 1: Reorder motion wrongly claimed to never be a containment
**ASN-0127, D-NONMONO, K.μ~ clause**: "unlike the extension and contraction clauses, the motion here is not a containment in either direction, so the F-IMONO step those clauses turn on does not apply and must be replaced by a direct witness."

**Problem**: This asserts, as a universal property of K.μ~, that the image (hence discovery) motion is never a containment and F-IMONO never applies. F-IMG-SWING — invoked in the very next sentence — contradicts it. Under non-injective `Σ.M(d_q)` (content sharing, M13/M14), F-IMG-SWING's own non-injective witness exhibits `image(W,d,Σ) = {a} ⊊ {a,b} = image(W,d,Σ')` — a **proper containment**. In that step `image(W,d,Σ) ⊆ image(W,d,Σ')`, so F-IMONO *does* apply and `findlinks_disc(W,d,Σ) ⊆ findlinks_disc(W,d,Σ')` — the discovery set grows monotonically. The ⊇ direction is equally realizable: with `Σ.M(d): v₁↦a, v₂↦b, v₃↦b`, `W={v₁,v₂}` (so `image={a,b}`), the reorder `π(v₁)=v₃, π(v₂)=v₁, π(v₃)=v₂` yields `Σ'.M(d): v₁↦b, v₂↦b, v₃↦a`, hence `image(W,Σ')={b} ⊊ {a,b}` — a contraction-direction containment, again admitting F-IMONO. So "not a containment in either direction / F-IMONO does not apply" is false; it holds *only* for the injective (equal-cardinality, genuinely incomparable) swing. The clause collapses two distinct cases and states a false universal in front of the case that refutes it.

**Required**: Scope the no-containment / direct-witness argument to the injective swing — there image cardinality is pinned (F-IMG-SWING), so two distinct images are necessarily incomparable and F-IMONO genuinely fails to give a direction. Treat non-injective reorders separately: the in-region image can move as a containment in either direction, F-IMONO applies, and the discovery set moves monotonically in that single step. Relatedly, "F-IMG-SWING moves the image — membership always" overstates F-IMG-SWING (which says the image *may* change membership): when `W` is fixed setwise by `π` the image does not move at all — a fact the worked illustration's own closing sentence concedes ("Had the query stayed at `W = {v₁, v₂}` — fixed setwise by `π` — both image and discovery set would be invariant").

### Issue 2: Discovery-set cardinality change under reorder is asserted but never witnessed
**ASN-0127, D-NONMONO, K.μ~ clause**: "the change respects no containment — neither ⊆ nor ⊇, and (as distinct I-addresses match distinct link-counts) not necessarily cardinality-preserving — with no link created or retracted. That such a containment-free swing is realizable is established concretely in the worked illustration's reorder clause, which lifts F-IMG-SWING through Phase 2 to a lateral swing {L_1} ↦ {L_2}."

**Problem**: The cited concrete witness — the illustration's `{L_1} ↦ {L_2}` — is **cardinality-preserving** (both singletons). It establishes the containment-free (lateral) swing, but the bundled sub-claim "not necessarily cardinality-preserving" is left as a one-phrase parenthetical with no scenario. The note witnesses every other behavior concretely (contraction shrink, extension rise, store-fixed rise, K.λ increment, existence vs. discovery zero); the cardinality-changing discovery swing is the single behavior asserted but un-witnessed, in a note whose discipline is to exhibit each behavior.

**Required**: Supply a witness — e.g. extend the illustration so `a₂` is reached by two links and `a₁` by one, so the single-position reorder on `W₀ = {v₁}` swings `{L₁} ↦ {L₂, L₂'}` (cardinality 1 → 2). Note this does not even require non-injectivity: it turns purely on distinct I-addresses matching distinct link-counts, so an injective reorder already realizes it. Alternatively, qualify the claim and drop the implication that the cited witness establishes it.

### Issue 3: Imprecise foundation citation for the I-run structure of an image
**ASN-0127, Phase 1 (paragraph after F-IMG)**: "When `W` is a contiguous V-span in some subspace `S`, ASN-0058's mapping-block decomposition gives the image as a union of I-runs (B1+B2, ASN-0058)."

**Problem**: B1 (coverage) and B2 (disjointness) place the V-positions of `W` into disjoint blocks but say nothing about the I-side being a run. The fact that each block's I-extent is the contiguous run `{aⱼ + k : 0 ≤ k < nⱼ}` is exactly B3 (consistency, `M(d)(vⱼ+k) = aⱼ+k`). The "union of I-runs" conclusion rests on B3, which the citation omits. Minor, but a citation slip in a note that otherwise cites per-step.

**Required**: Cite B3 (or the block decomposition as a whole), not B1+B2 alone.

## OUT_OF_SCOPE

### Topic 1: Content-keyed query through Σ.C (Open Question 1)
**Why out of scope**: A query that names addresses through `Σ.C` rather than resolving them through `Σ.M` is a genuinely different primitive (no arrangement mediation). New territory, not a defect here.

### Topic 2: Composition with ASN-0098 link projection displacement (Open Question 4)
**Why out of scope**: "Project a link through arrangement, then test the projection against a content region" composes two `Σ.M`-consulting operations; the note legitimately defers this rather than over-reaching.

### Topic 3: Uniform weakest-precondition across the full K-vocabulary (Open Question 3)
**Why out of scope**: D-CWP supplies a non-trivial wp for the contraction case, discharging the wp-depth obligation. The extension-side, reorder-side, and off-document wp companions — and their uniform characterization — are a natural next note, not a gap in this one. (The extension wp is the closest companion and would be cheap to add, but its absence is incompleteness, not error.)

### Topic 4: Filter-set constraints preserving union-distributivity into filtered forms (Open Question 2)
**Why out of scope**: The interaction of F-UDIST with filtered `findlinks` forms, and where the per-slot-universal vs per-link-existential distinction bites, is new compositional content.

VERDICT: REVISE
