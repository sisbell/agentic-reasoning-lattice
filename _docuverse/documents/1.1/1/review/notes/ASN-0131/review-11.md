# Review of ASN-0131

I checked this ASN against the standard that showing the common case works does not establish the edge cases. I focused hardest on the three places a hidden error would most likely lurk: the retraction-stability argument (RE-RET), the contraction weakest precondition (RE-CWP), and the field-agreement argument that the type address `θ` (and the retraction type `R`) avoids content. I also verified the transition taxonomy in RE-EDIT is exhaustive over the full vocabulary, and that the worked instance computes correctly. All hold up.

## REVISE

None.

For the record, the following were scrutinized and found sound:

- **RE-DEF factoring and finiteness.** `RE(W,d,Σ) = {(i,e) ∈ Avail(Σ) : touch_W(e)}` factors correctly because `touch_W(e)` is link-independent and pulls out of the existential. The answer is finite (`Avail ⊆` finite links × finite slots; `dom(Σ.L)` finite by L-fin) and the touch test is decidable pointwise over the finite image, with the cell-decomposition caveat (it characterises `coverage(e)`, not `I`) correctly stated.
- **RE-RET, both directions.** `nullified(Σ') = nullified(Σ) ∪ {ℓ}` is correctly pinned by R-Scope (`{t : ℓ ≼ t} ∩ dom(Σ'.L) = {ℓ}`); the emitter `b ∉ nullified(Σ')` follows from R0a's antichain; the forward half (sole bearer ⟹ drop) correctly rules out `b` re-witnessing the touching `e` (since `e ≠ ∅`, `e ≠` the to-set, `e ≠ R` each contradict `touch_W(e)`); the backward half (other live bearer survives) uses `ℓ ⋠ ℓ'` (R0a) and frame `M'=M` correctly. The dependence of the type-set half on an *imposed* discipline (seat `R` at `s_R ≠ s_C`) is honestly flagged as a layer convention with the conditional alternative stated — a legitimate conditional system guarantee, not an overclaim.
- **RE-CWP.** The drop condition `coverage(e) ∩ Δ ≠ ∅ ∧ coverage(e) ∩ I_R = ∅` is derived correctly from `image(Σ) = I_R ⊎ Δ` and the D-CWP bridge; the `R = ∅` collapse to `RE(Σ) = ∅` is correct; the "strictly finer than D-CWP" observation (same endset must reach both, vs. a link reaching via different slots) is right.
- **The `θ` argument.** The propagation of the subspace identifier along `≼` via field-segment agreement (third zero + 1 position) is rigorous, and the ASN correctly distinguishes it from T7 (which converts a *known* mismatch to distinctness) and correctly scopes it to the element-level case (`θ.0.x` being T4-invalid). The caveat that this is strictly stronger than `θ ∉ dom(Σ.C)` is a genuinely sharp observation.
- **RE-EDIT transition completeness.** All of {K.α (LP6), K.δ (LP8 + node/account M'=M), K.λ (split: ordinary adds via Σ.L, retraction removes via population), K.μ⁺ (F-IMG-MONO), K.μ⁺_L (image fixed since `v_ℓ ∉ W`), K.μ⁻ content vs link-subspace (F-IMG-CONTR / image-fixed), K.μ~ (F-IMG-SWING), K.ρ (LP14), other-document (LP5)} are classified with a specific cited lemma each — no "by similar reasoning."
- **Boundary cases.** Empty image, empty region, no addressable links, empty endset slot (`coverage(∅)=∅`), full clearance (`R=∅`), arity > 3, and unarranged positions in `W` are all handled.

## OUT_OF_SCOPE

### Topic 1: Whole-endset vs touching-spans-only surfacing (the ASN's Open Question 1)
**Why out of scope**: RE-DEF commits to returning the whole endset and flags RE-WHOLE provisional. RE-CLIP (no truncation) is firm under either reading, so the operation's faithfulness guarantee does not depend on resolving this. The choice is a genuine future design question, not an error here.

### Topic 2: Link-subspace regions (`W ⊆ s_L`) — Open Question 7
**Why out of scope**: The ASN restricts `W ⊆ s_C` as a caller obligation and correctly notes the points a link-subspace region would reopen (the retraction emitter's to-set could meet a link image; RE-RET's "iff" would acquire an emitter conjunct). This is new territory the content-subspace restriction deliberately buys out.

### Topic 3: Intersection-distributivity of region queries — Open Question 4
**Why out of scope**: The ASN correctly proves only the union half (RE-UDIST) and explains why intersection fails (the forward image does not distribute over intersection under the non-injective arrangement, M13/M14). Genuinely separate.

### Topic 4: Rendered V-position output mode — Open Question 3
**Why out of scope**: The content-identity answer is fixed under rearrangement; a mode that renders surfaced endsets into the querying document's V-positions (with the piecewise-display fragmentation of ASN-0082) is a distinct deliverable, correctly deferred.

### Topic 5: Non-co-resident link stores — Open Question 5
**Why out of scope**: Completeness when touching anchoring resides in a non-co-resident link store is replication/inter-server territory, excluded by the stated scope.

VERDICT: CONVERGED
