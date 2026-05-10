# Rebase Review of ASN-0043

## REVISE

### Issue 1: GlobalUniqueness cites S4 but exceeds its scope

**ASN-0043, Properties table**: "GlobalUniqueness | LEMMA | No two allocation events produce the same address — S4 (OriginBasedIdentity, ASN-0036) applied to all allocations | cited, S4 ASN-0036"

**Problem**: S4 (OriginBasedIdentity, ASN-0036) is formally quantified over I-addresses — content store addresses: "For I-addresses `a₁`, `a₂` produced by distinct allocation events: `a₁ ≠ a₂`". GlobalUniqueness claims "no two allocation events produce the same address" without the I-address restriction, extending the guarantee to link subspace allocations. The body text correctly argues that S4's underlying proof mechanism (T9, T10, T10a + TA5(d) + T3) "depends only on tumbler algebra and applies uniformly to all allocations" — but this is ASN-0043's own extension, not a citation of S4's stated scope. Marking GlobalUniqueness as "cited, S4 ASN-0036" misrepresents a scope extension as a direct citation.

**Required**: Either (a) change GlobalUniqueness to status "introduced" with its own derivation citing T9, T10, T10a, TA5, T3 from ASN-0034 directly (the scope-agnostic foundation properties), or (b) keep the S4 reference but note explicitly that S4's formal statement covers I-addresses and that the generalization to all element-level allocations follows from the same tumbler-algebra mechanism.

### Issue 2: Downstream references bypass GlobalUniqueness, citing S4 directly for link uniqueness

**ASN-0043, Link Distinctness and Permanence**: "By S4 (OriginBasedIdentity, ASN-0036), no two allocation events anywhere in the system produce the same address."

**Problem**: If GlobalUniqueness is the property that bridges S4 to link allocations, then downstream properties should cite GlobalUniqueness — not S4 directly. Currently L11a (body text and table entry: "link addresses inherit S4"), the Home and Ownership prose ("by S4, ASN-0036"), the L11b worked example ("L11a uniqueness for `a'` by S4 (ASN-0036)"), and L9's proof verification all cite S4 directly for link-address uniqueness, applying it beyond its stated I-address scope without going through the bridge property. GlobalUniqueness appears in the properties table but is never referenced by any downstream property.

**Required**: Either (a) update L11a's body and table entry, the Home and Ownership prose, and the worked-example references to cite GlobalUniqueness instead of S4 for link-address uniqueness, or (b) remove GlobalUniqueness as a separate table entry and fold the scope-extension argument into L11a's own derivation.

VERDICT: REVISE
