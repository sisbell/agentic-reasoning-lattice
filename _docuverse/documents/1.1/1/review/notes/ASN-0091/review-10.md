# Review of ASN-0091

## REVISE

### Issue 1: π non-uniqueness phrasing characterizes only the identity case

**ASN-0091, "REARRANGE as Vstream-Only Operation"**: "any permutation π of `dom(Σ.M(d))` that fixes the partition into arrangement pre-images `{Σ.M(d)⁻¹(a) := {v ∈ dom(Σ.M(d)) : Σ.M(d)(v) = a}}_{a ∈ ran(Σ.M(d))}` while otherwise permuting freely within each pre-image satisfies RA-π."

**Problem**: A permutation π that fixes the Σ.M(d) pre-image partition set-wise satisfies `Σ.M(d)(π(v)) = Σ.M(d)(v)` for every v. For RA-π to hold (`Σ'.M(d)(π(v)) = Σ.M(d)(v)`), we then need `Σ'.M(d) = Σ.M(d)` on all of `dom(Σ.M(d)) = dom(Σ'.M(d))` (by RA-dom). This forces `Σ' = Σ` — the characterization given covers *only* the identity case. For a non-identity transition Σ → Σ' with shared I-addresses on both sides, valid bijections π send `Σ.M(d)⁻¹(a)` to `Σ'.M(d)⁻¹(a)` bijectively (these sets are generally distinct in dom(M(d))); such π do not "fix Σ.M(d)'s partition". Concrete failure: with `Σ.M(d) = {v₁ ↦ a, v₂ ↦ a, v₃ ↦ b}` and `Σ'.M(d) = {v₁ ↦ b, v₂ ↦ a, v₃ ↦ a}`, the valid π must swap v₁ with v₃, which sends block "a"={v₁,v₂} to {v₂,v₃} — not back to itself. The phrasing presents an identity-only subcase as if it were the general non-uniqueness statement, even though the surrounding text ("the specific π witnessing the transition") implies generality.

**Required**: Either explicitly restrict the characterization to the identity case (Σ' = Σ), or restate it in general form: for any fixed transition Σ → Σ', π is a witness iff for each `a ∈ ran(Σ.M(d))`, π bijects `Σ.M(d)⁻¹(a)` onto `Σ'.M(d)⁻¹(a)` (with the within-pair bijection free).

## OUT_OF_SCOPE

None — the Open Questions section enumerates appropriate future topics (cross-document cut-split semantics, link-subspace REARRANGE, observational equivalence, cardinality bounds, completeness of cut-sequence rearrangements).

VERDICT: REVISE
