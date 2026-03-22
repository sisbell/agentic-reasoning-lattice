# Review of ASN-0063

## REVISE

### Issue 1: Incorrect disjointness claim for CL0 I-spans from different-depth blocks

**ASN-0063, Resolve definition paragraph**: "CL0 I-spans from blocks with I-addresses of different depths are automatically disjoint: by T10 (PartitionIndependence, ASN-0034), tumblers under incomparable prefixes cannot coincide, so spans over I-addresses from different document origins occupy non-overlapping regions of T regardless of depth differences."

**Problem**: Two errors in one sentence.

(a) *Over-broad claim.* "Different depths" does not imply disjointness. Two blocks in the same document's arrangement can have the same origin but different I-address depths (the document allocates content at element field depths 2 and 3 via child allocators per T10a). Counterexample: block β₁ with I-start `1.0.1.0.1.0.1.1` (depth 8, element field `[1,1]`) and block β₂ with I-start `1.0.1.0.1.0.1.1.1` (depth 9, element field `[1,1,1]`). The CL0 I-span from β₁ — say `(1.0.1.0.1.0.1.1, δ(2,8))` with reach `1.0.1.0.1.0.1.3` — contains `1.0.1.0.1.0.1.1.1` in its denotation (by T1(ii): `1.0.1.0.1.0.1.1 < 1.0.1.0.1.0.1.1.1`; and by T1(i) at position 8: `1 < 3`, so `1.0.1.0.1.0.1.1.1 < 1.0.1.0.1.0.1.3`). The I-spans overlap.

(b) *Incomplete justification.* T10 requires *incomparable* prefixes (`p₁ ⋠ p₂ ∧ p₂ ⋠ p₁`). Document origins can be comparable — when D₁ is a prefix of D₂ (e.g., D₁ = `[1]` and D₂ = `[1,2]`, produced via T10a child allocation), origin₁ = `N.0.U.0.1` is a proper prefix of origin₂ = `N.0.U.0.1.2`. Disjointness still holds for comparable origins (the field separator 0 after origin₁'s document field is less than origin₂'s continuation component ≥ 1, placing all origin₁ I-addresses below all origin₂ I-addresses by T1(i)), but T10 does not establish this — T4 and T1 do.

**Required**: Correct the claim to: "CL0 I-spans from blocks whose I-addresses fall under *different document origins* are disjoint — regardless of depth differences." Justify with: T10 for incomparable origins; T4 (field separator structure) + T1 for comparable origins. Drop the "different depths implies disjoint" formulation. Note that same-origin different-depth I-spans can overlap, which is consistent with the subsequent observation that the CL0 I-span collection is "not necessarily normalized."

This claim is not load-bearing — no proof depends on it, and `Endset = 𝒫_fin(Span)` admits overlapping spans — but a wrong statement in a specification invites wrong reasoning in future ASNs.

## OUT_OF_SCOPE

### Topic 1: Fork composite (J4) in the extended state

The K.μ⁺ amendment (content-subspace restriction) is necessary and correct for this ASN. However, Fork (J4, ASN-0047) is defined as a composite including K.μ⁺. In the extended state where a source document has link-subspace mappings, Fork's step (ii) — K.μ⁺ populating `M'(d_new)` — cannot copy link-subspace V-positions (the amended K.μ⁺ rejects `subspace(v) = s_L`). Fork requires extension with K.μ⁺_L steps or an equivalent mechanism. This belongs in a version-creation ASN; the open questions could note the dependency.

**Why out of scope**: The scope section explicitly excludes version creation. The K.μ⁺ amendment is backward-compatible with pre-extension states (where no link-subspace mappings exist), so no existing behavior is broken.

VERDICT: REVISE
