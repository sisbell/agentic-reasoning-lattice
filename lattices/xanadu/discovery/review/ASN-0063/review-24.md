# Review of ASN-0063

## REVISE

### Issue 1: Cross-origin I-span disjointness proof omits short-tumbler case
**ASN-0063, Resolve definition**: "Every tumbler in the first span's denotation [a₁, reach₁) has value (p₁)_k at position k: the start a₁ and reach both agree at position k (ordinal increment affects only the element ordinal, deeper than k), so any tumbler t with a₁ ≤ t < reach₁ must have t_k = (p₁)_k"
**Problem**: This claim is stated for all tumblers in the range but only holds for tumblers with at least k components. A tumbler t with #t < k can satisfy t ≥ a₁ if it diverges upward at some position j < k (i.e., t_j > (a₁)_j). However, such a tumbler is excluded from the range: since (a₁)_j = (reach₁)_j for j < k (ordinal increment preserves the document prefix), t_j > (reach₁)_j implies t ≥ reach₁ by T1(i), contradicting t < reach₁. The conclusion (disjointness) is correct, but the reasoning is incomplete — the short-tumbler case must be explicitly ruled out. The same gap applies to the comparable-origins case.
**Required**: Add a sentence establishing that no tumbler with fewer than k components lies in [a₁, reach₁): "If #t < k and t ≥ a₁, then t diverges from a₁ at some j ≤ #t < k with t_j > (a₁)_j = (reach₁)_j, so t ≥ reach₁ — contradiction."

### Issue 2: S8 scope expansion not explicitly acknowledged
**ASN-0063, CL11 Per-subspace arrangement invariants**: "S8 (SpanDecomposition): derived from S8-fin, S8a, S2, and S8-depth (ASN-0036), all verified above. The new link-subspace mapping (v_ℓ, ℓ) either forms a new width-1 correspondence run or extends the last existing link-subspace run..."
**Problem**: S8 in ASN-0036 is described as covering the "text-subspace portion of the arrangement" but uses the formal quantifier v₁ ≥ 1. Since s_L ≥ 1 (established earlier in CL11 for S8a), link-subspace positions now fall under S8's quantifier, expanding its effective scope beyond ASN-0036's stated intent. The ASN correctly handles this for S8a with an explicit note ("the quantifier covers *all* V-positions with v₁ ≥ 1, including link-subspace positions. We must establish that s_L ≥ 1...") but provides no parallel acknowledgment for S8. The analysis is correct — the CL11 proof implicitly treats S8 as covering link-subspace runs — but the scope change should be stated.
**Required**: Add a note parallel to the S8a treatment: "S8's quantifier v₁ ≥ 1 captures all V-positions in the extended state — since both s_C ≥ 1 and s_L ≥ 1 (established above for S8a) — extending coverage to the link subspace."

### Issue 3: Link-subspace ownership invariant not formally labeled
**ASN-0063, K.μ⁺_L section**: "The origin restriction origin(ℓ) = d distinguishes link-subspace extension from content-subspace extension..."
**Problem**: The derived property that every document's link-subspace arrangement contains only its own links — `(A d, v : v ∈ dom(M(d)) ∧ subspace(v) = s_L : origin(M(d)(v)) = d)` — is established through two independent arguments (K.μ⁺_L's origin precondition for creation, link-subspace fixity for preservation under K.μ~) and discussed at length, but never stated as a labeled invariant. This is an important structural guarantee (it formalizes Nelson's "a document includes only the links of which it is the home document") that future ASNs will need to reference. Without a label, they must re-derive it from K.μ⁺_L's precondition and the fixity argument.
**Required**: State the property as a formally labeled invariant (e.g., "CL-OWN — LinkSubspaceOwnership") in the Properties Introduced table and in the ExtendedReachableStateInvariants theorem.

## OUT_OF_SCOPE

### Topic 1: Link withdrawal mechanism
**Why out of scope**: The ASN correctly identifies that link withdrawal (removal from the current arrangement while the link persists in L) involves constraints beyond D-CTG suffix truncation, and defers to an open question. This is new territory requiring its own invariant analysis — not an error in this ASN.

### Topic 2: Link inheritance under forking
**Why out of scope**: The ASN explicitly notes that J4 (Fork) does not copy link-subspace mappings and defers any link-inheritance mechanism to future work. The architectural rationale (each document owns only its home links; shared content carries link discoverability via I-addresses) is sound.

### Topic 3: Discovery mechanism data structures and efficiency
**Why out of scope**: The ASN defines disc as a derived function on system state and establishes its properties (monotonicity, completeness, independence). The implementation of efficient disc evaluation (enfilade indexing, range queries) is an implementation concern, not an abstract specification requirement.

VERDICT: REVISE
