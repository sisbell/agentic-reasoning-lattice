# Review of ASN-0087

This ASN identifies MAKELINK as the composite `K.λ ; K.μ⁺_L` and is, on the technical merits, careful and complete: the `ℓ ∉ ran(M(d))` derivation through S3★/S3★-aux, the wp analysis (both arrangement-reach and reflexive routes), the D-CTG★ contiguity proof at arbitrary depth `m ≥ 2`, the S2 two-part exclusion, and the three-class invariant discharge all hold up. The worked example checks out against the concrete tumblers. I found no correctness gap.

The findings below are placement/accretion issues surfaced under the `review-mode.anti-bloat` mandate.

## REVISE

### Issue 1: Forward-staged derivation about the output `ℓ` parked in the *Inputs* section
**ASN-0087, Inputs ("Fresh-address exclusion (M-FreshExcl)")**: "The home-link application instantiates M-FreshExcl at `x = ℓ`, the fresh link address. We establish `ℓ ∈ F` structurally: `ℓ` is an `A_L(d)` emission, so FirstEmission and ChainDiscipline (ASN-0093) fix its form `[d, 0, s_L, k]` ... F's definition then yields `ℓ ∈ F`. When `ℓ ∉ dom(Σ.C) ∪ dom(Σ.L)`, M-FreshExcl at `x = ℓ` gives `ℓ ∉ coverage(eᵢ)` for every standardly authored `eᵢ`."

**Problem**: The *Inputs* section's job is to describe what the caller supplies and the authoring discipline on those inputs. The general lemma M-FreshExcl belongs there. But this "home-link application" paragraph derives facts about a **system-derived output** — `ℓ ∈ F` and the coverage-exclusion of `ℓ` — at a point where `ℓ` has not yet been introduced as the operation's derived address (that happens in *Decomposition*/*Preconditions*). The ASN itself states the caller "does not specify the link's address." The exclusion result `ℓ ∉ coverage(eᵢ)` is consumed only downstream, in the wp "Reduction under standard authoring" (M-Reflexive collapse) and in *Side Effects* (vacuity argument). The reader must hold this forward across several sections. This is the placement pattern the anti-bloat note names: useful concrete reasoning in the wrong structural slot.

**Required**: Relocate the `ℓ ∈ F` / home-link-application derivation to where its consequence is used — the wp standard-authoring reduction or *Side Effects*. Keep only the general M-FreshExcl lemma (a property of the authoring discipline) in *Inputs*.

VERDICT: REVISE
