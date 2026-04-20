# Review of ASN-0082

## REVISE

### Issue 1: VD and VP preservation not derived as postconditions

**ASN-0082, Post-Insertion Shift / Consistency**: The postconditions I3, I3-L, I3-X, I3-V, and I3-D fully specify the disposition of every pre-existing V-position, but the ASN does not derive the consequence that its own structural preconditions — VD (uniform depth) and VP (positive subspace) — hold for M'(d).

**Problem**: The ASN introduces VB/VD/VP as preconditions on M(d) and uses them throughout (VD for the depth-compatibility check, VP and the m ≥ 2 argument for subspace preservation). If I3 is ever composed with itself or with a future operation that also requires VD/VP, those preconditions must be verified against the post-state M'(d). The proof is straightforward:

- *VD for M'(d)*: Left-region positions have depth m by VD on M(d). Shifted positions have depth #shift(v, n) = #v = m (TumblerAdd result-length identity; VD on M(d)). All V-positions in dom(M'(d)) within subspace S share depth m.
- *VP for M'(d)*: Left-region positions inherit VP from M(d). Shifted positions: subspace(shift(v, n)) = shift(v, n)₁ = v₁ ≥ 1 (shift copies position 1 from v when m ≥ 2; VP on M(d)).

The ASN partially argues VP preservation in the "Ordinal Shift" section ("VP is preserved because shift copies position 1 from v when m ≥ 2") but does not consolidate this into a postcondition covering all regions of dom(M'(d)), and does not address VD preservation at all.

**Required**: Add a short derived-postcondition section (after the consistency verification or within it) explicitly stating and proving:

- I3-VD: `(A v₁, v₂ ∈ dom(M'(d)) : subspace(v₁) = subspace(v₂) = S ⟹ #v₁ = #v₂ = m)` — by case split on left vs shifted region.
- I3-VP: `(A v ∈ dom(M'(d)) : v₁ ≥ 1)` — by case split on left, shifted, and cross-subspace regions.

Add both to the statement registry.

## OUT_OF_SCOPE

### Topic 1: Complete INSERT specification (content placement in the gap)
**Why out of scope**: I3 specifies the shift aspect of insertion. The n gap positions in [p, shift(p, n)) are where newly inserted content will be mapped; the content-placement postcondition (what I-addresses appear in M'(d) at those positions) is a separate concern that the ASN correctly defers.

### Topic 2: External reference update mechanism
**Why out of scope**: The open question — "When external state records a V-position, what must the system provide to allow that reference to be updated after a shift?" — is a design question for link integrity and external indexing, not a gap in this ASN's shift property.

VERDICT: REVISE
