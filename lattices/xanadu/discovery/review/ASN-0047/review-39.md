# Review of ASN-0047

## REVISE

### Issue 1: Circular dependency in the dom_C = ∅ case of K.μ~

**ASN-0047, K.μ~ definition section**: "For any v ∈ dom_L(M(d)), the K.μ~ definition gives M'(d)(π(v)) = M(d)(v), and S3★'s link clause gives M(d)(v) ∈ dom(L), so M'(d)(π(v)) ∈ dom(L); by S3★-aux, subspace(π(v)) ∈ {s_C, s_L}, and the case subspace(π(v)) = s_C is eliminated because S3★'s content clause would require M'(d)(π(v)) ∈ dom(C), contradicting dom(C) ∩ dom(L) = ∅"

**Problem**: The argument uses S3★-aux and S3★'s content clause *at the post-state* M'(d) to derive π = id. But S3★-aux and S3★ at the post-state are among the very invariants K.μ~ must preserve — they cannot be cited before being established for this transition. The dom_C ≠ ∅ case avoids this because it establishes S3★ at the post-state first via the decomposition ("S3★ by decomposition") and only then invokes the fixity argument. For the dom_C = ∅ case, no independent establishment of S3★ at the post-state precedes its use.

One can rescue the argument by case analysis: either K.μ~ is zero steps (S3★ trivially preserved since M'(d) = M(d)) or nonzero steps (S3★ preserved by decomposition). Either way S3★ holds at the post-state, and the fixity argument follows. But the ASN doesn't make this case analysis explicit — it uses S3★ at the post-state as if it were already available.

**Required**: Either (a) add the case-analytic justification ("S3★ holds at the post-state: if zero steps, trivially; if nonzero, by decomposition"), or — more cleanly — (b) replace the S3★-based argument entirely with K.μ⁺'s referential integrity precondition. The simpler proof: suppose K.μ~ decomposes into nonzero steps when dom_C(M(d)) = ∅. K.μ⁻ removes r ≥ 1 link-subspace positions. K.μ⁺ (amended) adds r content-subspace positions to maintain the bijection's cardinality. For each such new content-subspace position π(v), M'(d)(π(v)) = M(d)(v) ∈ dom(L) (by S3★ at the *pre*-state). But K.μ⁺'s referential integrity precondition requires M'(d)(π(v)) ∈ dom(C), and dom(C) ∩ dom(L) = ∅ (L14) — contradiction. Therefore r = 0, and since dom_C(M(d)) = ∅ leaves nothing else to remove, K.μ⁻ cannot fire. Zero steps; M'(d) = M(d). This uses only pre-state S3★ and K.μ⁺'s precondition — no reference to post-state invariants.

### Issue 2: Properties table omits link-store entries

**ASN-0047, Properties Introduced table**

**Problem**: The ExtendedReachableStateInvariants theorem explicitly lists L0, L1, L1a, L3, L12, L14 as additions to the reachable-state invariant set ("adding... L3 (triple endset structure), and the remaining link invariants L0, L1, L1a, L12, L14"). These properties are formally integrated into the state-transition framework for the first time in this ASN. The Endset and Link type definitions, the Σ.L state component, and the subspace identifier definitions (s_C, s_L) are likewise introduced here. None appear in the properties table.

**Required**: Add entries for Σ.L (link store state component), Endset/Link (type definitions), s_C/s_L (subspace identifiers), L0 (SubspacePartition), L1 (LinkElementLevel), L1a (LinkScopedAllocation), L3 (TripleEndsetStructure), L12 (LinkImmutability), and L14 (StoreDisjointness). The "restated for self-containment" framing is fine in the body text, but the table is the reference for future ASNs and should track every property that enters the formal invariant framework in this ASN.

## OUT_OF_SCOPE

### Topic 1: Link endset referential integrity
**Why out of scope**: L3 requires endsets to be finite sets of well-formed spans (T12), but no invariant constrains endset spans to reference addresses in dom(C). Whether endset addresses must satisfy referential integrity — and what happens to link semantics when endset-referenced content is removed from arrangements — is a link-semantics question beyond the state-transition layer.

### Topic 2: Link placement uniqueness
**Why out of scope**: K.μ⁺_L does not prevent the same link ℓ from appearing at multiple V-positions in a single document's link subspace (no ℓ ∉ ran(M(d)) precondition). The current invariants permit duplicate link placement — CL-OWN, S3★, D-CTG/D-MIN are all satisfied. Whether a uniqueness constraint is architecturally required (Nelson's "permanent order of arrival" suggests each link has a unique position) is a link-subspace design question for a future ASN.

VERDICT: REVISE
