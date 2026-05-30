# Review of ASN-0082

## REVISE

### Issue 1: OrdinalExceedsDisplacement quantifies over tumblers its depth justification does not cover

**ASN-0082, Lemma OrdinalExceedsDisplacement**: "For any V-position v with `subspace(v) = 1` and `v ≥ r` — where `#v = 2` by S8-depth (the depth axiom fixes every subspace-1 V-position of d at the common depth `#p = 2`) … so `#v = #r` independently of the order relation, which is what licenses OrdinalOrderEquivalence (precondition `#v₁ = #v₂`) to give `ord(v) ≥ ord(r)`"

**Problem**: Two distinct defects in one statement.

(a) *Quantifier over-reach.* S8-depth (ASN-0036) constrains depth only for positions actually in `dom(M(d))` — i.e. for `v ∈ V_1(d)`. But the quantifier admits any tumbler with `subspace(v) = 1` and `v ≥ r`, which includes depth-3 tumblers absent from the arrangement. Concretely, `[1, 5, 2]` has `subspace = 1`, `#v = 3`, and satisfies `[1, 5, 2] ≥ r = [1, p₂+c]` (case (i) when `5 > p₂+c`, case (ii) when `5 = p₂+c`). For such a `v`, "`#v = 2` by S8-depth" is simply false, and OrdinalOrderEquivalence's `#v₁ = #v₂` precondition is not met. Every actual application (D-BJ, D-SHIFT, D-SEP) uses the lemma only for `v ∈ R ⊆ V_1(d)`, so the conclusions hold — but the lemma *as stated* is unsound for its written domain.

(b) *Precondition-justification embedded in the statement.* The clause "… so `#v = #r` independently of the order relation, which is what licenses OrdinalOrderEquivalence … to give `ord(v) ≥ ord(r)`" is a proof step about why a downstream invocation is licensed. It sits inside the lemma's quantifier preamble, forcing the reader past defensive meta-prose before reaching postconditions (i)–(iii). This is the anti-bloat pattern the note flags (justification of downstream applicability in a structural slot).

**Required**: Restrict the quantifier to `v ∈ V_1(d)` with `v ≥ r` (equivalently `v ∈ R`), or add `#v = 2` as an explicit hypothesis rather than deriving it from S8-depth over an unrestricted domain; handle the `v = r` case (where `r` need not lie in `dom(M(d))`) via the result-length identity, as the proof already does. Move the OrdinalOrderEquivalence-licensing sentence into the proof body.

## OUT_OF_SCOPE

### Topic 1: Contraction at ordinal depth greater than one
**Why out of scope**: The depth scoping axiom (`#p = 2`) restricts the post-contraction shift to single-component ordinals, while insertion (I3) is proved for general `m ≥ 2`. The asymmetry is genuine future territory — TA4's zero-prefix precondition collides with S8a's interior positivity at deeper ordinals — and the ASN already records it correctly in the Open Questions. No error in the present ASN; it is appropriately deferred, not skipped.

VERDICT: REVISE
