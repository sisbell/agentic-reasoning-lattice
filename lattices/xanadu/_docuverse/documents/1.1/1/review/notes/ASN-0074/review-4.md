# Review of ASN-0074

## REVISE

### Issue 1: Forward reference cites C0 for subspace confinement; the result is C0a
**ASN-0074, Content References (definition paragraph)**: "Precondition (iv) ensures subspace confinement — that ⟦σ⟧ does not cross subspace boundaries; the derivation follows from C0 below."
**Problem**: C0 establishes that the displacement is ordinal (action point = m). Subspace confinement — the claim that every t ∈ ⟦σ⟧ satisfies t₁ = u₁ — is the distinct result C0a, which combines C0 with m ≥ 2 and TumblerAdd's component-copying rule. The sentence attributes the confinement conclusion to the wrong label. A reader who looks up C0 sees "action point of ℓ equals m" and must infer the additional step through C0a, which is labeled "SubspaceConfinement" for exactly this purpose.
**Required**: Change "the derivation follows from C0 below" to "the derivation follows from C0a below" (or "from C0 and C0a below").

## OUT_OF_SCOPE

### Topic 1: Content references to the link subspace
**Why out of scope**: The definition does not restrict u₁ ≥ 1. A content reference with u₁ = 0 would target the link subspace, whose V-position properties (beyond S8-depth) are not yet established. This belongs in a future link-subspace ASN, not a defect in ASN-0074's definitions — C0, C0a, C1a, C1, C2 all hold for any subspace where S8-depth applies.

### Topic 2: Content reference splitting and merging
**Why out of scope**: Operations that partially modify a referenced range (splitting a content reference at an interior point, merging adjacent references to the same document) would parallel S4/S3 from ASN-0053 at the block level. These are needed for editing operations but are new territory beyond the resolution mechanism defined here.

### Topic 3: Content reference sequence well-formedness
**Why out of scope**: The ASN defines per-reference well-formedness but imposes no constraints on sequences as a whole (e.g., whether references may overlap within the same source document, or whether the sequence length interacts with target capacity). The open question about ordering is a symptom of this. Future operation ASNs that consume content reference sequences will need to specify these constraints.

VERDICT: REVISE
