# Review of ASN-0042

## REVISE

### Issue 1: T2 misattribution in NestingByDelegation proof
**ASN-0042, NestingByDelegation Inductive step**: "by the most-specific property of `π_d` and the covering-chain structure (any two prefixes covering a common prefix are themselves comparable — a consequence of T2's prefix-closure of the tumbler order), `pfx(π₁) ≼ pfx(π_d)`."
**Problem**: T2 (IntrinsicComparison) is about lexicographic comparison being a pure function of two tumblers; it says nothing about prefix-linearity. The lemma "two prefixes of a common tumbler are ≼-comparable" derives directly from the Prefix (PrefixRelation) definition componentwise — precisely the argument carried out in O2's proof Step 2. T2 has no "prefix-closure" content to cite.
**Required**: Replace the parenthetical with a citation to the Prefix (PrefixRelation) definition, or to the covering-chain lemma established in O2's proof Step 2.

### Issue 2: Unilateral O10★ depends on an unaxiomatized "baptismal coupling"
**ASN-0042, Unilateral feasibility paragraph and Formal Contract**: "By the baptismal coupling above, `u ∉ S'`... The unilateral guarantee is unconditional."
**Problem**: For the `zeros(pfx(π)) = 0` case, the proof relies on `S' ⊆ {1, ..., hwm_0}` — i.e., every Form B (=length) sub-delegate `π_i` with `pfx(π_i) = pfx(π).0.k` satisfies `pfx(π_i) ∈ Σ.B`. The justification given is narrative: "Delegation establishes a new principal, and a principal cannot enter the registry without an allocated prefix... the act of delegation by `π` to a sub-account at slot `k` materially baptizes `pfx(π).0.k`." But no state axiom enforces this. Conditions (i)–(vi) of the `delegated` relation only require `T4(pfx(π'))` (validity), not `pfx(π') ∈ Σ'.B` (membership in the baptismal registry). Without the coupling, a sub-delegate could exist with `pfx(π_i) = pfx(π).0.k` where `k > hwm_0`, making `u = hwm_0 + 1 = k` a collision and breaking O5-authorization at step 1. The zeros=1 case does not depend on the coupling and is genuinely unilateral; the zeros=0 case is not.
**Required**: Add a state axiom (e.g., O18 DelegationBaptizes: `delegated_Σ(π, π') ⟹ pfx(π') ∈ Σ'.B`), or strengthen `delegated` condition (v) to include `pfx(π') ∈ Σ'.B`, or qualify the Unilateral O10★ claim as conditional on the baptismal coupling for the zeros=0 case.

### Issue 3: T10a misnamed and misused in O9 supporting prose
**ASN-0042, O9 proof Case 1**: "Note that the inequality may be strict: T10a (SiblingShallowChildDeep) permits `inc([1, 2], 1) = [1, 2, 1]` with `zeros = 0`..."
**Problem**: T10a's foundation name is "AllocatorDiscipline", not "SiblingShallowChildDeep". Further, the structural fact `inc([1, 2], 1) = [1, 2, 1]` with the resulting zero-count comes from TA5(d) (HierarchicalIncrement, k > 0 branch — `#t' = #t + k`, position `#t + k` is `1`, intermediate positions are zero), not from T10a. T10a constrains allocator discipline (which `inc` calls can appear in sibling vs child spawn), which is not what is being cited here.
**Required**: Replace the citation with "TA5(d)" and remove the incorrect parenthetical name.

## OUT_OF_SCOPE

None. The ASN explicitly delimits out-of-scope topics in its Scope section and its Open Questions list, which correctly handle items like ownership transfer, federation, modification rights, and authentication mechanisms.

VERDICT: REVISE
