# Review of ASN-0127

## REVISE

### Issue 1: F-UDIST's consequences are neither derived nor connected to the note's own use sites

**ASN-0127, F-UDIST and D-NONMONO**: F-UDIST's derivation closes with "The unrestricted form is what Phase 1 needs: images of two disjoint V-regions need not be disjoint I-sets..."

**Problem**: F-UDIST is proved, but the two consequences it exists to support are never extracted.

(a) *The promised Phase-1 payoff is absent.* The note defines the two-phase combinator F-V but never states the distributivity that F-UDIST is explicitly motivated to enable: `findlinks_V(R₁ ∪ R₂, d, Σ) = findlinks_V(R₁, d, Σ) ∪ findlinks_V(R₂, d, Σ)`. This is the natural algebraic property of the composite and the entire stated reason F-UDIST must be unrestricted — image distributes over V-region union, the resulting I-sets may overlap (M13/M14), and F-UDIST closes the composition. The note sets up this application and then omits the one-line derivation.

(b) *A downstream step silently depends on monotonicity-in-I.* D-NONMONO's contraction bullet — "the arrangement contracts, so image(W, d_q, Σ') ⊆ image(W, d_q, Σ) (F-IMG-CONTR); the resolved request can only shrink" — is meant to deliver the "findlinks_disc shrinks" half of non-monotonicity. The step from "the I-set shrinks" to "the link set shrinks" requires `I' ⊆ I ⟹ findlinks(I', Σ) ⊆ findlinks(I, Σ)`. That monotonicity is an immediate corollary of F-UDIST (`findlinks(I) = findlinks(I') ∪ findlinks(I ∖ I') ⊇ findlinks(I')`), but it is never stated, so the general D-NONMONO argument has an unjustified link. The worked illustration patches the gap only for the specific numbers `{a_1, a_2} → {a_1}`.

**Required**: State and derive (i) `findlinks` monotone in its I-argument as a corollary of F-UDIST, and cite it explicitly in D-NONMONO's contraction case; and (ii) `findlinks_V` distributivity over V-region unions — the Phase-1 application the note claims F-UDIST is for.

### Issue 2: F-IMG-SWING's "gain, lose" cases are claimed but only "change membership" is justified

**ASN-0127, F-IMG-SWING**: "the forward image of a fixed sub-region R may differ — gain, lose, or change membership," justified by "That π need not fix R setwise is exactly why a fixed sub-region's image may gain, lose, or change membership even though the total range is preserved."

**Problem**: The realizability argument given — π does not fix R setwise — establishes only *change of membership*. It does not establish *gain* or *lose* (cardinality change). Because π is a bijection of `dom(Σ.M(d))` onto itself with `dom` fixed (K.μ~-FIX), `π⁻¹(R) ∩ dom` and `R ∩ dom` always have equal cardinality; when `Σ.M(d)` is injective (no content sharing), the two images therefore have equal size, so the image can only change membership, never gain or lose. A genuine gain or loss requires non-injective `Σ.M(d)` — content sharing (M13/M14, ASN-0058) — which the justification never invokes. The proof exhibits one of three claimed behaviors and asserts the other two. (This is specifically an F-IMG-SWING defect: D-NONMONO's K.μ~ bullet correctly restricts itself to "a position with otherwise-unshared image," i.e., the membership-change case, and is unaffected.)

**Required**: Either restrict F-IMG-SWING's realizability gesture to "change membership," or add the content-sharing hypothesis the gain/lose cases require, with a concrete shared-content witness — e.g., `M(d): v₁↦a, v₂↦a, v₃↦b` reordered to `v₁↦a, v₃↦a, v₂↦b`, so `image({v₁,v₂})` rises from `{a}` to `{a,b}`.

### Issue 3: "K.λ is the unique single-step source of change in the result" is unqualified and clashes with the note's own findlinks_V framing

**ASN-0127, Operational consequences (after F-LAMBDA)**: "K.λ is therefore the unique single-step source of change in the result, and its effect is fully characterized."

**Problem**: This holds only for `findlinks(I, Σ)` against a *fixed* I — the object F-INERT/F-LAMBDA range over. But the note's headline object is `findlinks_V`/`findlinks_disc` (the abstract opens with "which links does this content region reach, and what stays stable"), and for that object the claim is false: D-NONMONO shows K.μ⁺, K.μ⁻, and K.μ~ on the query document all move the discovery-anchored result with no link created or retracted. Taken at face value, this summary sentence erases the existence-vs-discovery distinction that is the note's central contribution.

**Required**: Scope the claim — "the unique single-step source of change in `findlinks(I, Σ)` for fixed I" (equivalently, in the existence-anchored result) — so it cannot be read as a statement about `findlinks_V`.

## OUT_OF_SCOPE

### Topic 1: Weakest precondition for discovery-anchored stability
**Why out of scope**: The note's third open question. The wp for `findlinks_V(R, d, Σ) = findlinks_V(R, d, Σ')` under a specific transition is a separate result; its absence is not an error here — though once Issue 1 supplies findlinks-monotone-in-I, the K.μ⁻ case becomes a tractable successor.

### Topic 2: Content-keyed queries and composition with ASN-0098
**Why out of scope**: The relationship between `findlinks_V` and a `Σ.C`-keyed query, and the composition of `image()` with ASN-0098's projection displacement, are listed open questions — new territory, not gaps in the arrangement-mediated algebra this note delivers.

VERDICT: REVISE
