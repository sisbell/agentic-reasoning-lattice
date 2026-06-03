# Review of ASN-0071

I checked the PC derivation (componentwise fact, totality, prefix agreement), the PC-RANGE biconditional at both depth cases, F-DEEP, the routing/subspace-confinement arguments (F-CONTENT, F-ORIGIN), and the four worked queries against their reach computations. The mathematics is sound: TumblerAdd prefix-copy + T1 case (i)/(ii) + T0 trichotomy discharge PC correctly; the t-vs-r contradiction in the componentwise fact correctly leans on `u_p = r_p` below the action point; PC-RANGE's order reductions at component `#u` are genuine biconditionals; and the example reaches/intersections check out. The remaining findings are anti-bloat accretion, not correctness.

## REVISE

### Issue 1: Empty-source case stated three times
**ASN-0071, *A worked scenario* (F-DEEP dual)**: "(The empty-source case `V_{s_C}(d_s) = ∅` lands the same way for a more basic reason — a document with no content-subspace position has `dom(M(d_s))` carrying nothing for `⟦σ⟧` to intersect.)"
**Problem**: This parenthetical restates the empty-source split already derived in *Resolution* ("If `V_{s_C}(d_s) = ∅` the source carries no content-subspace position ... the intersection is empty and `iaddrs_one(d_s, σ)(Σ) = ∅` trivially") and again recorded in the F-DEEP claims-table row ("the companion empty-source case ... holds trivially"). The worked dual demonstrates the `#u > m_C` case on the non-empty `d_A`; the empty-source aside is unrelated to the example it sits in — meta-prose pulled into the example slot, the kind of accretion this note flags.
**Required**: Delete the parenthetical. The empty-source case is already carried by *Resolution* and the claims table.

### Issue 2: Order disclaimer restates itself
**ASN-0071, *What we do not specify* (i)**: "Order is a presentation choice. Two implementations both meeting the specification may return the same elements in different orders, and neither violates the specification by virtue of order alone."
**Problem**: The second sentence re-expresses "Order is a presentation choice" without adding a distinct claim — two sentences, one point.
**Required**: Collapse to a single statement that order is unspecified and not a conformance criterion.

## OUT_OF_SCOPE

### Topic 1: Result-to-`R` relationship and rejection-vs-filter policy
**Why out of scope**: The three Open Questions (current result vs. ever-containing `R`, when to reject unresolvable positions, the contraction-transition invariant) are correctly deferred — they concern operations and history relations outside this query's remit.

VERDICT: REVISE
