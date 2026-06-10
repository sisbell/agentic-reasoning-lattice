# Review of ASN-0127

I checked every claim in this note against its derivation and against the foundation contracts it cites. The arithmetic of the witnesses, the keystone separation, the wp derivation, and the worked illustration all hold up. I found no REVISE items. Detail on the load-bearing checks below, then the genuinely out-of-scope items.

## Verification notes (no REVISE items)

**F-IMG-SWING witnesses recomputed.** Injective: `π = (v₁ v₂)` gives `Σ'.M(d): v₁↦b, v₂↦a`, `π⁻¹({v₁}) = {v₂}`, image `{a}↦{b}` (cardinality fixed). Non-injective: `π(v₁)=v₁, π(v₂)=v₃, π(v₃)=v₂` gives `Σ'.M(d): v₁↦a, v₂↦b, v₃↦a`, `π⁻¹({v₁,v₂}) = {v₁,v₃}`, image `{a}↦{a,b}` with `ran` preserved. Both correct, and both admissible as K.μ~ (domain fixed by K.μ~-FIX ⇒ D-CTG★/D-MIN★/S8a/S8-depth inherited; length/subspace/link-fixing satisfied; net effect non-trivial).

**D-NONMONO K.μ~ clause (the recently revised one).** The injective-regime argument is now sound: it correctly observes F-IMONO is *unavailable* when the moved image takes two distinct equal-cardinality (hence ⊆-incomparable) values, and establishes non-monotonicity *directly* via the worked illustration's lateral swing `{L_1}↦{L_2}` rather than by an invalid appeal to image-order. The shrink witness `v₁↦a, v₂↦b, v₃↦b` under the 3-cycle yields image `{a,b}↦{b}` as claimed, and is a valid non-injective K.μ~. The "image-motion is necessary" sub-claim is correct (store fixed ⇒ `findlinks_disc` motion forces image motion via F-INERT).

**D-CWP wp recomputed.** Bridge `image(W,d_q,Σ') = {Σ.M(d_q)(v) : v ∈ W∩R} = I_R` holds (`R ⊆ dom(Σ.M(d_q))` by D-SEQ★, retained-domain agreement). With `image(W,d_q,Σ) = I_R ∪ Δ` (justified: `I_R ⊆ image` by F-IMG-CONTR), F-INERT + F-UDIST give `findlinks_disc(Σ) = A ∪ B`, `A = findlinks_disc(Σ')`, so stability `⟺ B ⊆ A`. This is a genuine biconditional (weakest), evaluable on `(Σ,R)` alone — every post-state quantity eliminated. The `R = ∅` boundary collapses correctly to "pre-state set already empty," and the grain contrast with LP12a's single-link `wp ≡ false` is accurate.

**Worked illustration.** The slot reductions rest on pairwise prefix-incomparability of `a_1,a_2,a_3` (siblings on `A_C(d)`, T10a.2) and of `a_θ` (subspace `s_L`); all `coverage({x}) ∩ I = {x} ∩ I` reductions verified. The store-fixed rise (`L_2` persists undiscoverable at `Σ₁`, re-enters at `Σ₂` under pure K.μ⁺) and the cardinality-changing swing (`{L_1}↦{L_2,L_2'}` at fixed image cardinality, via `L_2'=({a_2},∅,Θ)`) both check out and concretely discharge the D-NONMONO clauses.

**Keystone separation.** F-CIL (store-fixed lane, needs `Σ.L = Σ'.L`) is correctly held distinct from LP13 (existence lane, survives a *growing* store under K.λ). E-INV correctly leans on LP13's full value persistence — not LP3★, which fixes coverage but not the arity bound the `matches` existential ranges over. F-CIL-perlink's role under K.λ (where F-CIL's global hypothesis fails) is correctly motivated. F-PRES's per-operation frame check confirmed against the amended ASN-0047 frames (all of `V_atomic ∖ {K.λ}` and K.μ~ publish `L' = L`).

**No scope violations.** All cross-references are to the seven listed foundation ASNs. `image` and `findlinks` are new primitives, not reinventions of `project`/`coverage`. The note stays in abstract state/query/invariant territory — no implementation drift, no META.

## OUT_OF_SCOPE

### Topic 1: Type-slot participation in content-region matching
**Why out of scope**: F-MATCH's existential ranges over *all* slots, including the type slot (3), so a region resolving to a type address would match a link via its type endset. This is internally consistent and intentional for the foundation primitive (endsets may target any address, L4). Whether a *reader-facing* content-region operation should restrict matching to from/to slots is a refinement for a future operation ASN — the note's Q2 already gestures at the per-slot-universal vs per-link-existential distinction.

### Topic 2: The note's four open questions
**Why out of scope**: Content-keyed query through `Σ.C` (Q1), filter-set preservation of F-UDIST (Q2), the uniform wp across the whole K-vocabulary of which D-CWP is the contraction instance (Q3), and composition with ASN-0098's projection-displacement (Q4) are all genuinely new territory, correctly deferred. D-CWP discharging only the contraction wp (mirroring LP12a, which likewise does only contraction) is an acceptable parallel, not an omission.

VERDICT: CONVERGED
