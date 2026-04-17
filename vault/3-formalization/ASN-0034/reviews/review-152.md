# Cone Review — ASN-0034/T1 (cycle 5)

*2026-04-17 11:33*

Looking through the ASN carefully, paying attention to what Previous Findings have already surfaced.

### Case 2's k'=k case-(i) rebuttal is counted as a separate NAT-order site while Case 3's co-pair rebuttals are folded into the opening site

**Foundation**: NAT-order (NatStrictTotalOrder).

**ASN**: T1 (LexicographicOrder), Depends enumeration — NAT-order trichotomy sites 2 and 3.

Site 2 (Case 2 opening): *"to resolve the ordering of disagreeing components `aₖ` and `bₖ` into `aₖ < bₖ` or `bₖ < aₖ`"* — trichotomy at the component pair `(aₖ, bₖ)`.

Site 3 (Case 2's k'=k case-(i) rebuttal): *"to exclude the opposite inequality at position `k` against the forward witness already fixed by the opening step"* — trichotomy's exactly-one clause at the same component pair `(aₖ, bₖ)`.

Compare the Case 3 opening site, which the enumeration explicitly describes as folding three co-pair uses into one: *"the same invocation's exactly-one clause additionally underwriting both the mutual exclusivity of the m<n and n<m branches and the case-(ii) reverse-witness rebuttals within each branch... so no second trichotomy use at the length level is required to eliminate m=n past the case hypothesis or to refute the case-(ii) rebuttals' derived strict comparisons."*

**Issue**: Site 3's use of the exactly-one clause at `(aₖ, bₖ)` — acknowledged in the site description as deriving directly from "the forward witness already fixed by the opening step" — is the exact same pattern Case 3's opening absorbs: a follow-on exactly-one consumption at the same pair as the opening invocation, used to foreclose a candidate inequality once the opening has fixed the surviving outcome. Under the per-instance convention ("branches that instantiate an axiom at distinct symbols count as separate sites"), co-pair reuses of the same invocation's exactly-one clause fall on the single-site side of the rule (same symbols = same instance), which is why Case 3's three-way fold is valid. Applying the same rule to Case 2, site 3 should fold into site 2. Keeping them separate treats the Case 2 opening's exactly-one clause as generating a fresh site when reused downstream at the same pair, while the Case 3 opening's exactly-one clause does not — the two cases then apply opposite conventions for the same structural move.

**What needs resolving**: Either fold site 3 into site 2 (reducing trichotomy to eleven sites and the NAT-order preamble total to eighteen, consistent with Case 3's co-pair absorption), or split Case 3's opening invocation into separate sites for each downstream use of its exactly-one clause (the m≠n → dichotomy resolution, mutual exclusivity of branches, the m<n branch's case-(ii) rebuttal foreclosure, and the n<m branch's case-(ii) rebuttal foreclosure — raising trichotomy and the preamble total correspondingly). The convention must be applied uniformly: either reuses at a common pair are always one site, or they are always separate sites.
