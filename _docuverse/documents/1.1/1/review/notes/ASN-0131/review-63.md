# Review of ASN-0131

I read the operation definition, the worked instance, the composition laws, and the stability analysis against the cited foundations (all of ASN-0034/0036/0043/0045/0047/0053/0058/0082/0086/0093/0098/0127 are foundation, so cross-citation is in order). The core contract (RE-DEF, RE-LOC, RE-UNIT, RE-OVL, RE-CLIP, RE-BND), the worked instance, RE-ADDR, RE-RET, and RE-CWP all check out under their stated conditions; I verified the worked example's `e₃` content-disjointness argument, the `Avail(Σ)` factoring, the retraction-emitter harmlessness chain, and the contraction weakest-precondition equivalence line by line. One analytical claim does not hold.

## REVISE

### Issue 1: The `⊇` failure of the intersection law is mis-attributed to non-injectivity, and injectivity cannot recover equality

**ASN-0131, "Composing regions: union-distributivity" (the intersection paragraphs) / RE-UDIST-∩ / Open Question 4**: "The reverse inclusion, by contrast, **fails in general** ... It turns on non-injectivity (M13, M14, ASN-0058) ... What remains open is the refinement — whether some restriction on the arrangement, injectivity of `Σ.M(d)` the natural candidate, recovers equality (Open Question 4)." Table RE-UDIST-∩: "the reverse `⊇` **fails in general**, exhibited by a concrete counterexample whenever `Σ.M(d)` is non-injective ... Whether an arrangement restriction (injectivity) recovers equality is the open refinement (Open Question 4)."

**Problem**: The `⊇` direction fails *even under an injective arrangement*, so the failure does not "turn on non-injectivity," and no arrangement restriction — injectivity included — can recover the stated equality. The root cause is the existential "meets" structure of `touch_W` itself (`coverage(e) ∩ image(W) ≠ ∅`): one endset can witness `touch_{W₁}` and `touch_{W₂}` through **different** addresses, and "meets A" ∧ "meets B" does not imply "meets A∩B" — this is independent of whether `image` distributes over intersection. The ASN correctly diagnoses that the *image* intersection law `image(W₁∩W₂) ⊆ image(W₁)∩image(W₂)` can be strict under non-injectivity (layer 1), but then incorrectly carries that diagnosis up to the RE-level `⊇` failure (layer 2), which is a separate and arrangement-independent obstruction.

Injective counterexample. Take the typical, fully reachable arrangement

> `Σ.M(d) = { [1,1] ↦ a,  [1,2] ↦ b }`,  with `a ≠ b` in `dom(Σ.C)` — **injective**,

and an addressable link bearing in slot 1 the two-span endset `e = {(a, δ(1, #a)), (b, δ(1, #b))}`, so `coverage(e) = {t : a ≼ t} ∪ {t : b ≼ t} ⊇ {a, b}` (PrefixSpanCoverage, ASN-0043) and `(1, e) ∈ Avail(Σ)`. With `W₁ = {[1,1]}`, `W₂ = {[1,2]}` (both ⊆ `s_C`, disjoint): `image(W₁) = {a}`, `image(W₂) = {b}`, `W₁ ∩ W₂ = ∅`. Then `touch_{W₁}(e)` holds via `a` and `touch_{W₂}(e)` via `b`, so `(1, e) ∈ RE(W₁, d, Σ) ∩ RE(W₂, d, Σ)`; but `image(W₁∩W₂, d, Σ) = ∅`, so `RE(W₁∩W₂, d, Σ) = ∅` (RE-BND) and `(1, e) ∉ RE(W₁∩W₂, d, Σ)`. Hence `⊇` fails with `Σ.M(d)` injective. The same shape works for *overlapping* `W₁, W₂` (an endset covering one address from each region's exclusive part), so the obstruction is not even confined to disjoint regions.

**Required**: Correct the attribution — the `⊇` failure stems from `touch_W`'s existential "meets" test, not from arrangement non-injectivity. Present (or at least acknowledge) the injective counterexample alongside the existing non-injective one. Reframe or drop Open Question 4: an arrangement restriction such as injectivity provably cannot recover `RE(W₁∩W₂) = RE(W₁) ∩ RE(W₂)`; if equality is recoverable at all, the governing condition lives in the endset coverage relative to the images (e.g. single-point coverage), not in `Σ.M(d)`. (The `⊆` half is sound and unaffected.)

## OUT_OF_SCOPE

None beyond the seven open questions the ASN already defers, which are appropriately scoped (whole-vs-touching surfacing, multiplicity, V-rendered answers, type-slot/content matches, link-subspace regions, non-co-resident stores).

VERDICT: REVISE
