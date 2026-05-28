# Review of ASN-0077

## REVISE

### Issue 1: K.σ is referenced but undefined in any foundation ASN
**ASN-0077, O11★★ derivation (case iii) and surrounding multi-step lemmas**: "an `M(d')`-modifying step for `d' ≠ d`, or a non-arrangement-modifying transition (K.α, K.λ, K.δ, K.ρ, K.σ)."
**Problem**: K.σ is not defined in any of the listed foundation ASNs (0034, 0036, 0040, 0047, 0053, 0058, 0098). It originates in ASN-0093, which is not a foundation. The multi-step claims O11★/O11'★/O11★★ assert preservation across "any reachable state sequence," and their case (iii) must be exhaustive over the *complete* transition vocabulary. Because the vocabulary is drawn from "ASN-0047 + ASN-0093" but ASN-0093 is neither restated nor a foundation, the ASN is not self-contained: the exhaustiveness of the interleaved-step case analysis rests on an unenumerated set of transition kinds.
**Required**: Either define K.σ locally, restrict the multi-step lemmas to the foundation transition vocabulary, or supply an explicit closure argument that the enumerated kinds are complete. Remove or ground the bare K.σ reference.

### Issue 2: Singleton I-span edge case over-claims the intersection and discharges it via vocabulary closure
**ASN-0077, "Singleton I-span" edge case**: establishes "`⟦σ_a⟧ ∩ dom(C) = {a}`," with the `#b > #a` exclusion relying on "K.α (ContentAllocation, ASN-0047) — the only elementary transition placing addresses into `dom(C)`" and the induction that "every output of `A_C(d)` [has] the length `#d + 3`."
**Problem**: The strict-singleton conclusion requires that *every* content address have element field of length exactly 2 (hence length `#d+3`). S7c only gives `#E(a) ≥ 2`. To force exactly 2 the proof needs (a) K.α to be the *sole* content allocator and (b) K.α to use only `inc(·, 0)` — a transition-vocabulary-closure assumption. This is precisely the closure that O0's derivation takes pains to avoid ("no vocabulary-completeness assumption"). Moreover the strict singleton is not even needed: a strict extension `b` of `a` with a longer element field would still lie in `[a, a⊕ℓ)` and still yield `origin(b) = origin(a)`, so the operationally relevant conclusion (single origin) holds regardless.
**Required**: Weaken the claim to the single-origin result (`origins_I(Σ, σ_a) = {origin(a)}`), which is robustly derivable, or explicitly justify the content-address-length closure within the self-contained ASN.

### Issue 3: Internal inconsistency in the attribution of O0(b) for dom(L)
**ASN-0077, O0(b) derivation vs Summary**: O0(b) states the `dom(L)` correspondence is "established from L1c and the Allocator hierarchy alone, with no K.λ-event closure and no vocabulary-completeness assumption." The Summary states origin is grounded "semantically in K.λ's allocation precondition `origin(ℓ) = d`."
**Problem**: The body deliberately routes around K.λ; the Summary credits K.λ. These attributions conflict, and the conflict matters because the whole point of O0(b) is that it avoids transition-vocabulary closure.
**Required**: Reconcile the Summary with the O0(b) derivation (cite L1c + Allocator hierarchy + SubAllocatorAxiom, as the body and the Claims-Introduced table do).

### Issue 4: O3's V-span computability claim leans on a state invariant
**ASN-0077, O3 derivation (V-span)**: "computable from `M(d) ↾ ⟦σ⟧` alone," with well-definedness "discharged by S3★ (GeneralizedReferentialIntegrity, ASN-0047)."
**Problem**: S3★ is a state invariant that reads `dom(C)` and `dom(L)` from Σ; invoking it to discharge well-definedness undercuts the "from the restriction alone" claim. The pure projection `origin` is in fact total on any tumbler with `zeros ≥ 2`, so well-definedness needs no state read — but the proof as written introduces a state dependency it then claims not to have.
**Required**: Either state that `origin` is well-defined structurally on any `zeros ≥ 2` tumbler (so the restriction's values suffice without S3★), or weaken the "from the restriction alone" phrasing to acknowledge the invariant appeal.

## OUT_OF_SCOPE

### Topic 1: Reporting link origins from an I-span (cross-subspace I-stream ranges)
**Why out of scope**: Correctly deferred to Open Question 1; the I-span lift's restriction to `dom(C)` is a stated definitional choice, not an error.

### Topic 2: Surfacing the intermediate transclusion chain; native-vs-transcluded distinction; historical containment vs current origin
**Why out of scope**: All three are appropriately recorded as Open Questions and as explicit non-promises ("What SHOWORIGIN does not promise"); they belong to separate future operations, not to this ASN.

VERDICT: REVISE
