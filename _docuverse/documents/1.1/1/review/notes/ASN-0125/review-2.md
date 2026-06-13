# Review of ASN-0125

I read the note as a specification of a derived operation (EDITLINK) plus a layer of state-derived relations (`succ_h`, `succ_o`, `current`) over a designated coverage class. I checked the central proofs against the substrate it cites, traced the worked example end to end, and hunted specifically for skipped cases and "by similar reasoning" gaps. My findings below.

## Verification performed

I confirmed the load-bearing results rather than taking them on assertion:

- **EL0 (MutationExclusion).** The inductive predicate `J ≡ a ∈ dom(L) ∧ L(a) = ℓ₀` is preserved by *every* elementary transition — framed transitions verbatim, and `K.λ` because its binding precondition forces `ℓ_f ∉ dom(L)` hence `ℓ_f ≠ a`. The induction covers the complete vocabulary (Vocabulary fact V enumerates all eight ASN-0047 transitions), so `wp(S, R_mut) = false` at `Σ₀` is sound. This is a genuine, non-trivial wp result, not a decorative one.
- **EL7 (EditContract).** Both steps' preconditions discharge correctly at the intermediate state; `a' ≠ a ≠ b` by freshness at each emission; the C/M/E/R frame holds because both steps are `K.λ`. The discipline-preservation argument (vi) is non-circular — it rests on `DC(ℓ')` and EL6(v), not on (iv).
- **EL6(iv) full-frame.** The unconditional `nullified(Σ') ∩ dom(Σ.L) = nullified(Σ)` (no `[R]`-growth, since `K_sup ≁ R`) and the disciplined `b ∉ nullified(Σ')` (fresh `b` prefix-incomparable to every existing unit-depth retraction target by R0a) both check out. The invocation of ASN-0086's wp Case 2 is legitimate: that simplification is itself attributed to unit-depth-discipline + R0a, which is exactly Df-DISC(i).
- **EL4 (SingleTarget).** The per-claim derivation (PrefixSpanCoverage + R0a) genuinely needs only schema-conformance of the single claim, not whole-state discipline. The `Ŝ^Σ` restriction in Df-SUCC is consistently propagated (EL5a, EL11b, EL12, EL14), keeping the successor relations total even at non-disciplined states.
- **EL11(a).** The content-address exclusion (a `t ≽ old(e)` would force `E(t)₁ = s_L` against `E(t)₁ = s_C`, using `#E ≥ 2` to place the witness position) and the link-address exclusion (R0a) are both correct; the biconditional with `listed(old(e), d, Σ)` follows.
- **EL10 / EL13 / EL14 / worked example.** The position-reuse construction, the cross-home commutation, the four currency cardinalities (including the `∅` standoff from a 2-cycle), and all six addresses in the worked example (`ℓ₁=H.0.s_L.2`, `c₁=…3`, `r₁=…4`, `c₃=…5`, `r₂=…6`; `ℓ₂`, `c₂` on P's chain) trace exactly.

All cross-ASN references are to foundation ASNs (0034, 0036, 0040, 0042, 0043, 0047, 0086, 0093, 0098); none are improper. The note defines no claims for any scoped-out topic.

## REVISE

None. I scrutinized three candidates and dismissed each:

- **`DC(ℓ')` completeness for claim/retraction-class successors.** Under the natural reading — schema-conformance (including the membership conjuncts `x,y ∈ dom(L)`, target `∈ A_rel`) evaluated at the invocation state `Σ` — `dom(Σ.L) ⊆ dom(Σ₁.L)` carries conformance to `Σ₁`, and EL7(vi) holds. The condition is complete; the evaluation state is the only thing left implicit, and it is forced.
- **EL9(2) de-listing.** "Listing is mutable in both directions" is already secured by the simple full-clear case (`n'_{s_L}=0` then `K.μ⁺_L`); the arbitrary-middle-link contract-and-re-extend is a stronger claim whose sketch is correct (each re-seat satisfies `K.μ⁺_L`'s precondition; D-SEQ★ reshapes). Adequate for its role.
- **EL14(d) "no canonical selector."** Read as "no temporally-meaningful unique selector" — supported by EL13 plus the explicit concession that address-based tie-breaks "rank namespaces, not times." Consistent with the prose-claim convention of the foundation ASNs.

## OUT_OF_SCOPE

None. Discoverability in EL11 concerns the *standing of a supersession claim* as a state function (via ASN-0098 `project`), not the scoped-out FINDLINKSFROMTOTHREE read surface. The Open Questions (non-asserter retraction authority, meta-claim stratification, endset span-level correspondence, listing-coupling) are correctly deferred as future territory, not gaps here.

The note stays squarely in specification territory: it defines a derived operation, the relations its state induces, and the invariants any implementation must satisfy, with the implementation notes clearly marked as evidence rather than mechanism. No drift.

VERDICT: CONVERGED
