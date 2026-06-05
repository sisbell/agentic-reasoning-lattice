# Review of ASN-0100

## REVISE

### Issue 1: Opening atomicity promise overstated against the note's own result
**ASN-0100, The Question**: "and atomically, with no observable intermediate state in which some invariant is violated?"
**Problem**: The Atomicity section establishes a weaker, correct result: per-state invariants (Class (a)) hold at every intermediate, but the composite-boundary properties P4★, P4a, P7a hold *only* at the boundary. P4★ (`Contains_C(Σ) ⊆ R`) is in fact violated at the post-K.μ⁺/pre-K.ρ intermediate — content is arranged but provenance is not yet recorded. So there *is* an observable intermediate state at which a property the note itself verifies does not hold. The unqualified word "invariant" in the framing is imprecise against the body.
**Required**: Qualify the opening to "no observable intermediate state in which a *per-state* invariant is violated," and state explicitly that the coupling/boundary properties (P4★, P4a, P7a) are transiently unestablished mid-composite and restored at the boundary `Σ →* Σ'`.

### Issue 2: Garbled, redundant phrasing in the K.μ⁻-before-K.μ⁺ forced-ordering argument
**ASN-0100, Atomicity and Canonical Order**: "the position shift(p, 0) = p (when j = 0) or p itself (interior), is in pre-state dom(M(d)) with M(d)(p) ≠ a_0"
**Problem**: `shift(p, 0) = p` and "p itself" name the same tumbler; the `(when j = 0)` / `(interior)` split is spurious, since `p ∈ dom(M(d))` holds uniformly whenever Right is non-empty (`p_m ≤ N`). The reader must work past the false case-split to recover the actual point. This reads like relocated/garbled reviser content.
**Required**: Collapse to a single statement: when `Right ≠ ∅`, `p ∈ dom(M(d))` with `M(d)(p) ≠ a_0`, so a K.μ⁺ firing before K.μ⁻ would violate its image-preserving precondition at `p`.

### Issue 3: Re-insertion sub-case re-derives a V-side checklist it simultaneously declares insensitive
**ASN-0100, A Worked Example (empty-document re-insertion after full clearance)**: enumerates "D-MIN★ holds…; D-SEQ★ holds…; D-CTG★ holds…; S8-depth holds…; S8a holds…; and S8★'s…" then concludes "every V-side invariant is insensitive to that difference."
**Problem**: The genuine content of this sub-case is the I-side distinction (K.α subsequent-emission branch keyed on `dom(C)`, chain continued past the persisted frontier `a_prev`). The full V-side invariant re-derivation is redundant exhaustiveness — by the paragraph's own insensitivity claim, the V-side discharges identically to the first-insertion example. This is the bloat pattern the anti-bloat classifier targets.
**Required**: Compress the V-side to one sentence ("V-side invariants discharge exactly as in the first-insertion example; only the K.α branch and the chain continuation past `a_prev` differ"), retaining only the I-side argument as the sub-case's distinct content.

## OUT_OF_SCOPE

(none — the Open Questions section correctly defers partial-failure recovery, link-subspace insertion, self-composition, concurrency, and derived-property maintenance to future ASNs.)

VERDICT: REVISE
