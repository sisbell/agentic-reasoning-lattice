# Review of ASN-0079

## REVISE

### Issue 1: SearchConstraint terminology is misleading for type queries

**ASN-0079, SearchConstraint definition**: "A *search constraint* is either ⊤ (unconstrained — matches any endset) or a non-empty finite set P ⊂ T of I-addresses."

**Problem**: The phrase "of I-addresses" implies P ⊆ dom(C), but type-endset queries require P to contain type addresses that may fall outside dom(C) entirely. L9 (TypeGhostPermission, ASN-0043) explicitly permits type endsets to reference addresses outside dom(C) ∪ dom(L). A query constraining slot S₃ with a type-hierarchy prefix (per L10, ASN-0043) would use such addresses. The formal part — "non-empty finite set P ⊂ T" — is correct. The informal gloss "of I-addresses" narrows it incorrectly.

**Required**: Either drop "of I-addresses" (leaving "non-empty finite set P ⊂ T") or explicitly note that P is a set of tumblers that need not belong to dom(C), since type-endset queries reference type-address space.

### Issue 2: F6 pagination is undefined at the boundary

**ASN-0079, F6**: "page(Q, c, N) = ⟨aᵢ, aᵢ₊₁, ..., aⱼ⟩ where i = min{k : aₖ > c} and j = min(i + N − 1, n)"

**Problem**: When FindLinks(Q) = ∅ (n = 0) or when the cursor c ≥ aₙ (past the last result), the set {k : aₖ > c} is empty. min(∅) is undefined. The definition breaks at exactly the boundary that pagination must handle — the end-of-results case.

**Required**: Add: page(Q, c, N) = ⟨⟩ when {k : aₖ > c} = ∅. This covers both the empty-result case and the exhausted-cursor case.

### Issue 3: No concrete example

**ASN-0079, throughout**

**Problem**: The ASN establishes the satisfaction predicate, transclusion transparency, and projection without verifying any of them against a specific scenario. Per review standards, at least one worked example is required. The key properties to verify concretely are F1 (satisfaction), F8 (transclusion transparency), and F11/F13 (projection with partial coverage).

**Required**: A scenario such as: document d₁ with three content addresses a₁ < a₂ < a₃ in its arrangement; document d₂ transcluding a₂ only; a link ℓ with from-endset spanning [a₁, a₃]; a query Q = (⊤, {a₂}, ⊤, ⊤). Verify: (1) sat succeeds because a₂ ∈ coverage(F(ℓ)), (2) the query is equally answerable from d₁ or d₂ (F8), (3) project(ℓ, 1, d₂) returns only the V-position mapping to a₂ while project(ℓ, 1, d₁) returns all three V-positions (F11/F13).

## OUT_OF_SCOPE

### Topic 1: Full access control model
**Why out of scope**: The ASN correctly parameterizes access filtering by an abstract function accessible(u) ⊆ E_doc and derives the interaction properties (F15, F16). Defining what u is (user vs. account), how accessible is computed, and how permissions are granted/revoked is new territory requiring its own state components and invariants.

### Topic 2: Concurrent query semantics
**Why out of scope**: FINDLINKS is defined for a fixed state Σ, which is the right abstraction for specifying the query semantics. Isolation guarantees when link creation and link search execute concurrently require a concurrency model not present in the ASN-0047 transition framework, which is sequential by construction.

### Topic 3: Index invariants for completeness
**Why out of scope**: F19 mandates sublinear retrieval but intentionally does not specify index structure. The question "what invariants must an index maintain to guarantee no satisfying link is omitted?" (acknowledged in open questions) is an implementation-specification bridge that belongs in a separate treatment, likely alongside the enfilade formalization.

VERDICT: REVISE
