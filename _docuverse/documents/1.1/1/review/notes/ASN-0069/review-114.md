# Review of ASN-0069

## REVISE

### Issue 1: §"The Empty-Source Case" closing paragraph re-states empty-case vacuity that the individual properties already carry

**ASN-0069, §"The Empty-Source Case"**: "The single organising principle is quantifier domain: the structural properties — V1 (identity), V2 (prefix-encoded ancestry), V3 (no content allocated), and V12(a) ... — hold substantively ... while every property whose universal quantifier ranges over `V_{s_C}(d_op)` or `V_{s_C}(d_src)` holds vacuously, because that domain is empty ... V6 reduces to `V_{s_L}(d_new) = ∅`..."

**Problem**: This paragraph is an after-the-fact organizing essay that re-asserts vacuity already established at each property's own site. V4 already carries it: "V4 holds unconditionally: the formal universal is vacuously true when `V_{s_C}(d_op) = ∅` (V7's empty-source case...)". V6's derivation already reduces to `V_{s_L}(d_new) = ∅` via K.δ's `M'(d_new) = ∅`. V7 already states the empty-fork effect (`M'(d_new) = ∅`, `R' = R`), and the Worked Example walks the empty case concretely. The paragraph is the "two paragraphs say the same thing in different words" / use-site-inventory pattern the anti-bloat pass targets: it enumerates which properties are substantive vs. vacuous without establishing anything V4/V6/V7 do not already say. A reader must skip past it to follow the actual claim (V7).

**Required**: Delete the "single organising principle is quantifier domain" paragraph. V4's self-contained unconditional clause, V6's reduction, V7's effect statement, and the Worked Example's empty-source walkthrough already cover the empty case at the points where each property is stated. If a single forward-pointer is wanted in §"The Empty-Source Case", one sentence ("each Vn whose quantifier ranges over `V_{s_C}(d_op)` is vacuous; see each property's own clause") suffices.

## OUT_OF_SCOPE

### Topic 1: Transitivity of the prefix order ≼ is a general tumbler-algebra fact, not a fork property

**Why out of scope**: V11a derives `≼` transitivity inline (full NAT-order disjunct case analysis) because foundation ASN-0034's `Prefix` claim states only the definition and `p ≺ q ⟹ #p < #q`, not transitivity. ASN-0069 genuinely needs it for the fork chain, so the inline derivation is currently necessary — it is not a defect in this ASN. The clean home for a general `≼`-transitivity lemma is the foundation (ASN-0034), which would let V11a cite rather than re-derive. That is a foundation amendment, not a revision to ASN-0069.

### Topic 2: Concurrent fork during source modification, descendant enumeration, snapshot-vs-living forks, transcludent sources, byte-equal/address-distinct correspondence

**Why out of scope**: These are the ASN's own Open Questions and concern link operations, concurrency semantics beyond the sequential atomic axiom, and value-equality machinery — new territory for future ASNs, correctly deferred here.

VERDICT: REVISE
