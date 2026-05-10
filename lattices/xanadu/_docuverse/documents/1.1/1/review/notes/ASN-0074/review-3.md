# Review of ASN-0074

## REVISE

### Issue 1: Subspace confinement of ⟦σ⟧ assumed but not established; m ≥ 2 precondition missing

**ASN-0074, C1a**: "S8-depth (fixed depth): every position in dom(f) belongs to dom(M(d_s)), so all share the common depth m of subspace u₁ in d_s."

**ASN-0074, C2**: "There are ℓₘ such positions, so |dom(f)| = ℓₘ where f = M(d_s)|⟦σ⟧."

**Problem**: Both claims depend on an unstated property: every tumbler in ⟦σ⟧ has first component u₁ (subspace confinement). Without this, dom(f) = dom(M(d_s)) ∩ ⟦σ⟧ could include V-positions from other subspaces with different depths, breaking S8-depth for f and inflating |dom(f)| beyond ℓₘ.

Subspace confinement holds when reach(σ)₁ = u₁. By C0, the action point of ℓ is m. By TumblerAdd, for i < m: reach(σ)ᵢ = uᵢ. Setting i = 1 requires 1 < m, i.e., m ≥ 2. At m = 1 the action point is 1, so reach(σ)₁ = u₁ + ℓ₁ ≠ u₁, and ⟦σ⟧ spans subspaces u₁, u₁+1, …, u₁+ℓ₁−1. Then dom(f) may include positions from subspaces whose common depth differs from m, falsifying C1a's S8-depth check. And dom(f) may contain non-depth-m positions, so |dom(f)| > ℓₘ, falsifying C2.

The C2 proof establishes that there are exactly ℓₘ depth-m tumblers in ⟦σ⟧ and that well-formedness puts them all in dom(f) — but it never shows dom(f) has no *other* elements. The reverse direction requires: (a) subspace confinement (all of ⟦σ⟧ is in subspace u₁), and (b) S8-depth (all subspace-u₁ positions have depth m). Step (a) is the gap.

The content reference definition's remark that "the depth-m restriction is structurally guaranteed" addresses (b) but not (a). It says dom(M(d_s)) has only depth-m positions in subspace u₁ — true, but the conclusion requires first knowing that dom(f) ⊆ subspace u₁.

**Required**: Three additions:
1. Add m ≥ 2 as precondition (iv) to the content reference definition. (Derivable from V-position structure — by D-SEQ and D-MIN, m = 1 gives at most a single-element subspace, but the derivation is not stated.)
2. State the subspace confinement property explicitly: for m ≥ 2, reach(σ)₁ = u₁ (TumblerAdd preserves components before action point m), so every t ∈ ⟦σ⟧ satisfies t₁ = u₁ (any t₁ ≠ u₁ falls outside [u, reach(σ)) by T1(i)).
3. In the C2 proof, close the |dom(f)| = ℓₘ argument: by subspace confinement, dom(f) ⊆ subspace u₁; by S8-depth, all subspace-u₁ positions in dom(M(d_s)) have depth m; by the enumeration, there are exactly ℓₘ depth-m tumblers in ⟦σ⟧ ∩ subspace u₁; therefore |dom(f)| = ℓₘ.

## OUT_OF_SCOPE

### Topic 1: Link-subspace content references
**Why out of scope**: The ASN works with text-subspace V-positions (v₁ ≥ 1, per S8a). Content references to link-subspace positions (v₁ = 0) involve different well-formedness constraints and are new territory.

### Topic 2: Resolution I-address uniqueness
**Why out of scope**: Whether resolved I-addresses are distinct across runs depends on the arrangement (transclusion can produce repeated I-addresses, consistent with S5/M13). The ASN correctly does not claim injectivity — that is a property of specific arrangements, not of the resolution mechanism.

VERDICT: REVISE
