# Review of ASN-0127

This is careful, well-factored work. The two-phase factoring (image consults `Σ.M`, comprehension consults `Σ.L`) is the right decomposition, and the keystone F-CIL plus the existence/discovery anchoring split is the substantive contribution. The derivations I checked — F-IMG-MONO/CONTR/SWING (the swing witness `v₁↦a, v₂↦a, v₃↦b` with `π(v₂)=v₃, π(v₃)=v₂` does yield image `{a}→{a,b}`), F-UDIST, F-VDIST, F-LAMBDA's disjoint increment, E-CONS's exclusion direction, and the subtle F-INERT-at-fixed-image step inside D-NONMONO's K.μ⁻ clause — are correct. The findings below are depth gaps, not errors.

## REVISE

### Issue 1: The distinctive discovery-rise is asserted, never witnessed

**ASN-0127, D-NONMONO (K.μ⁺ clause) and Worked illustration**: "new I-addresses falling in `W`'s positions can then add new link matches, evaluated against the unchanged store."

**Problem**: The worked illustration concretely witnesses the discovery *fall* — "`image(R, d, Σ')` shrinks to `{a_1}` and `findlinks_disc(R, d, Σ')` shrinks to `{L_1}`. ✓ D-NONMONO contraction clause" — but the *rise* under K.μ⁺ is left as a "can." This is the sharpest demonstration of the note's entire thesis: a discovery query that **grows under a pure arrangement extension with no link created** is exactly what existence anchoring (E-MONO) can never do. The only rise the illustration actually exhibits is under K.λ, which also raises the existence-anchored set — so it does *not* distinguish discovery from existence. The distinctive, store-fixed rise is the postcondition that carries the asymmetry, and it is the one left unverified.

**Required**: Add a concrete store-fixed K.μ⁺ rise to the worked illustration — a resurrection-style scenario (cf. the orphan/resurrection mechanics in the foundation): a pre-existing link `L` whose from-endset is `{a_2}`, with `a_2 ∈ dom(C)` but not yet in `d`'s arrangement and `W` already naming the V-position that will carry it; then `Σ.M(d): v_2 ↦ a_2` via K.μ⁺ moves `L` *into* `findlinks_disc(W, d, ·)` with `Σ.L` untouched. Show `L ∉ findlinks_disc(W, d, Σ)` and `L ∈ findlinks_disc(W, d, Σ')`.

### Issue 2: No weakest-precondition computed — all of it deferred to the open questions

**ASN-0127, Open questions**: "What conditions on `R` and on a transition `Σ → Σ'` are jointly sufficient to preserve `findlinks_V(R, d, Σ) = findlinks_V(R, d, Σ')` — i.e., the weakest precondition for discovery-anchored stability under a specific transition?"

**Problem**: D-NONMONO gives *directional* characterizations (grows under K.μ⁺, shrinks under K.μ⁻) and E-CONS gives an exact set-difference on the existence side, but no transition-stability wp is computed anywhere. Deferring the *general* characterization (all transitions, arbitrary `R`) to a future ASN is fine; deferring *every* wp leaves this note without the wp-depth its directly-cited sibling foundation carries (ASN-0098's LP12a, ContractionDiscoverabilityWP, computes precisely this for `discoverable_from`). The machinery here closes one in a few lines.

**Required**: Compute at least one concrete wp — the natural one is findlinks_disc stability under K.μ⁻ on `d_q`. Writing `Δ = image(W, d_q, Σ) ∖ image(W, d_q, Σ')` for the I-addresses the contraction drops inside the queried region, F-UDIST (`image(W,Σ) = image(W,Σ') ∪ Δ`) and F-INERT (store fixed) give:

> `findlinks_disc(W, d_q, Σ') = findlinks_disc(W, d_q, Σ)` **iff** `findlinks(Δ, Σ) ⊆ findlinks(image(W, d_q, Σ'), Σ)`

— every link reaching a dropped I-address also reaches a retained one. Leave the general form to open Q3.

### Issue 3: E-INV lacks an explicit derivation and cites an incomplete premise

**ASN-0127, Existence anchoring**: "coverage is invariant across all transitions (LP3★, ASN-0098). **E-INV (CoveragePermanence).** *... every `a ∈ dom(Σ.L)` satisfies `matches(a, I, Σ') ⟺ matches(a, I, Σ)`.*"

**Problem**: E-INV is the load-bearing input to E-MONO, E-CONS, and D-ZERO, yet it is the only lemma in the section without a `Derivation.` block — its sole justification is the preceding prose clause. That clause cites LP3★ (per-slot coverage), but `matches`'s existential ranges over `1 ≤ i ≤ |Σ.L(a)|`, so the biconditional also needs **arity invariance** `|Σ'.L(a)| = |Σ.L(a)|`, which LP3★ does not supply. The complete premise is LP13 (UnconditionalLinkPersistence: `Σ'.L(a) = Σ.L(a)`), which gives arity and per-slot coverage together. Given the per-step citation discipline this family otherwise maintains, the unstated arity step is a real gap.

**Required**: Give E-INV a one-line derivation citing LP13 for full link-value persistence: `matches(a, I, Σ') = (E i ≤ |Σ'.L(a)| : coverage(Σ'.L(a).eᵢ) ∩ I ≠ ∅) = (E i ≤ |Σ.L(a)| : coverage(Σ.L(a).eᵢ) ∩ I ≠ ∅) = matches(a, I, Σ)`, the middle equality by LP13.

## OUT_OF_SCOPE

### Topic 1: Content-keyed query through `Σ.C`
**Why out of scope**: Open Q1 names a genuinely different primitive (addresses resolved through the content store rather than the arrangement). New territory, correctly deferred.

### Topic 2: General wp characterization and composition with ASN-0098's displacement results
**Why out of scope**: Beyond the single concrete wp requested in Issue 2, the full characterization over all transitions and arbitrary `R` (open Q3) and the `image()`-with-LP** composition (open Q4) are legitimate follow-on work, not defects here.

### Topic 3: Filtered-form distributivity / per-slot-universal vs per-link-existential
**Why out of scope**: Open Q2 explores variants of F-UDIST under filtering; the base algebra established here is self-contained without it.

VERDICT: REVISE
