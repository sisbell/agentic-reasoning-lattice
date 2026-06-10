# Review of ASN-0127

This is a careful note. The labeled results (F-IMG through D-ZERO) are, as far as I can verify, correct: F-IMG-SWING's injective/non-injective witnesses check out under K.μ~ admissibility, F-UDIST's unrestricted form is correctly motivated by content sharing, D-CWP's weakest precondition derivation is sound, and the worked illustration verifies each motion against the actual coverage arithmetic (the prefix-incomparability premise on `a_1, a_2, a_3, a_θ` genuinely discharges the slot reductions). The two findings below are precision and framing defects, not breaks in the mathematics — but the note's own citation discipline is otherwise scrupulous (per-step foundation attributions), which is exactly why these two stand out.

## REVISE

### Issue 1: Mapping-block citation misattributes B1/B2 to the query region

**ASN-0127, Phase 1 (after F-IMG)**: "When `W` is a contiguous V-span in some subspace `S`, ASN-0058's mapping-block decomposition gives the image as a union of I-runs: B1 and B2 partition `W`'s V-positions into disjoint blocks `βⱼ = (vⱼ, aⱼ, nⱼ)`, and B3 (consistency, `Σ.M(d)(vⱼ + k) = aⱼ + k`) makes each block's I-extent the contiguous run `{aⱼ + k : 0 ≤ k < nⱼ}` (B1–B3, ASN-0058)."

**Problem**: B1 (Coverage), B2 (Disjointness), B3 (Consistency) are conditions on a block decomposition of the *full arrangement* `M(d)` — B1 quantifies over `dom(M(d))`, not over `W`. The blocks `βⱼ` are blocks of `M(d)`; a block may straddle `W`'s boundary, with `V(βⱼ)` partially inside and partially outside `W`. Taken literally, the claim that "each block's I-extent [is] the contiguous run `{aⱼ + k : 0 ≤ k < nⱼ}`" overstates the image: `image(W, d, Σ)` is the union of the *W-restricted* sub-runs `{Σ.M(d)(v) : v ∈ V(βⱼ) ∩ W}`, not the union of full block I-extents `I(βⱼ)`. For a `W` not aligned to block boundaries the difference is real (the full-block reading computes too large an I-set). This is the one place the note's otherwise exact per-step citation convention slips.

**Required**: Cite C1a (RestrictionDecomposition, ASN-0058) instead. C1a gives a unique maximally merged block decomposition for any restriction `f = M(d)|X` whose induced domain lies in a single subspace — exactly the situation for `X = W` contiguous in subspace `S`. Under C1a the blocks *are* W-confined, their I-extents *are* the image's runs, and the prose becomes accurate. B1/B2/B3 describe a decomposition of `M(d)`; the image of a sub-region needs the restriction decomposition, not the global one.

### Issue 2: The keystone's reach is overstated — existence anchoring does not propagate from F-CIL

**ASN-0127, "The stability keystone"**: "The single result that propagates to every preservation claim in the rest of the note: **F-CIL (ComprehensionInvariantUnderΣL — meta-lemma).**"

**Problem**: This is contradicted by the note's own existence-anchoring derivations. F-CIL's hypothesis is `Σ.L = Σ'.L` (store *fixed*), and "Operational consequences" makes this explicit: the keystone "turns the question 'which transitions preserve the result?' into the question 'which transitions preserve `Σ.L`?'". But E-INV (CoveragePermanence) — itself a preservation claim — operates across `Σ →* Σ'` in the regime where the store *grows* (K.λ admitted on the path), where F-CIL's store-equality hypothesis fails outright. Its derivation correctly roots in LP13, not F-CIL: "LP13 (UnconditionalLinkPersistence, ASN-0098) gives `a ∈ dom(Σ'.L) ∧ Σ'.L(a) = Σ.L(a)`… LP3★ alone fixes per-slot coverage but not the arity bound… LP13 supplies both." E-MONO and E-CONS then chain off E-INV. So an entire preservation lane — the existence-anchoring section — propagates from LP13's *per-link persistence under a growing store*, never touching F-CIL. "Every preservation claim in the rest of the note" is therefore literally false.

**Required**: Scope the keystone claim to the `Σ.L`-preservation lane it actually governs (F-INERT, F-LAMBDA via F-CIL-perlink, and what D-NONMONO/D-CWP draw from F-INERT). State plainly that the existence-anchoring preservation claims (E-INV → E-MONO → E-CONS) rest on a distinct foundation — LP13's per-link value persistence — precisely because the fixed-`I` regime tolerates a growing store where `Σ.L = Σ'.L` does not hold. The note in fact runs on *two* keystones (F-CIL for the store-fixed lane, LP13 for the fixed-`I` lane); the prose should say so rather than collapse them into one.

## OUT_OF_SCOPE

### Topic 1: Specialization of `findlinks_disc` to the full domain recovers ASN-0098's discoverability set

`findlinks_disc(W, d_q, Σ)` taken at `W = dom(Σ.M(d_q))` is `findlinks(ran(Σ.M(d_q)), Σ) = {a ∈ dom(Σ.L) : discoverable_from(a, d_q, Σ)}` by LP12 (DiscoverabilityCharacterisation, ASN-0098), since `matches(a, ran(M(d_q)), Σ)` is exactly LP12's per-link biconditional. Drawing this would anchor the new region-general primitive in the existing foundation discoverability notion (`findlinks_disc` is `discoverable_from` generalized from "the whole document" to "a named V-region").

**Why out of scope**: This is a grounding connection, not a defect in any claim — the note's region-general primitive is strictly more general, and the connection is distinct from open question 4 (which concerns composition with `project`, the I→V direction). It would strengthen a future revision but blocks nothing here.

VERDICT: REVISE
