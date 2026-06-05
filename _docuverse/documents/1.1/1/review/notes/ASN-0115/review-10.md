# Review of ASN-0115

I read the ASN as a read-only delivery operation: resolve each named V-position through its document's arrangement, then dereference the immutable store, concatenating in spec-set order. The substrate citations are all to foundation ASNs (0034, 0036, 0043, 0045, 0047, 0053, 0058, 0082, 0086, 0093, 0098), so no cross-ASN-reference violation. The subspace-confinement argument (ordinal-level ⟹ `actionPoint(ℓ) = #ℓ ≥ 2` ⟹ T5 with prefix `[s₁]`) is correct, R8's link-vacuity argument (CL-OWN + CL-UNIQ) is sound, and R7's restriction to comparable states `Σ →* Σ'` is a genuinely careful (not lazy) treatment. The depth-mismatch case (spec depth `#s` ≠ the subspace's common bound depth `m_S`) is gracefully absorbed by R6's silent-gap discipline rather than being a defect. One well-definedness gap remains.

## REVISE

### Issue 1: `item` is applied to all of `act` without establishing its two cases are exhaustive there

**ASN-0115, "What a spec-set is, and what delivery is" (item definition)**: "`item(v, ρ, Σ) = ⟨content, Σ.C(a)⟩ if subspace(v) = s_C … ⟨ref, a⟩ if subspace(v) = s_L`"

**Problem**: `deliver₁(ρ, Σ)` enumerates every `v ∈ act(ρ, Σ) ⊆ dom(Σ.M(d))` and applies `item` to each. The definition gives two subspace cases and justifies *store membership within each case* (`a ∈ dom(Σ.C)` / `a ∈ dom(Σ.L)` by S3★), but it never establishes that the two cases *exhaust* the active positions. If some `v ∈ act` had `subspace(v) ∉ {s_C, s_L}`, `item` — and hence `deliver₁` and `deliver` — would be undefined. The totality of `item` on `act` rests on S3★-aux (SubspaceExhaustiveness, ASN-0047: every active V-position has subspace `s_C` or `s_L`), which the substrate section states in prose but the definition does not invoke. As written, the central delivered object `deliver(R, Σ)` is not shown to be total on its stated domain.

**Required**: At the `item` definition (or where `deliver₁` enumerates `act`), cite S3★-aux to discharge that the two cases are exhaustive on active positions, making `item` total on `act` and `deliver₁`/`deliver` well-defined. This is the companion to the per-case S3★ citations already present and closes the case analysis.

## OUT_OF_SCOPE

(none — the boundary-crossing single span and inline-provenance questions are already deferred to Open Questions and need not be flagged as missing.)

VERDICT: REVISE
