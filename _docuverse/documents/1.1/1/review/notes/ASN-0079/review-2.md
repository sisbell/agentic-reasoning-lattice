# Review of ASN-0079

## REVISE

### Issue 1: Worked example span excludes a₃ (off-by-one)
**ASN-0079, Worked Example**: "(Concretely, F = {(a₁, a₃ ⊖ a₁)} when a₁, a₂, a₃ are contiguous at the same depth.)"
**Problem**: The span (a₁, a₃ ⊖ a₁) has reach = a₁ ⊕ (a₃ ⊖ a₁) = a₃ by D1. The denotation is {t : a₁ ≤ t < a₃} — a half-open interval excluding a₃. For contiguous depth-m addresses a₁ = [..., x], a₂ = [..., x+1], a₃ = [..., x+2], the displacement a₃ ⊖ a₁ = δ(2, m), reach = [..., x+2], and the depth-m tumblers in the interval are only a₁ and a₂. The claim coverage(F) ⊇ {a₁, a₂, a₃} is false; a₃ ∉ coverage(F).

This cascades to the F11 verification: "project(ℓ, 1, d₁) = {v₁, v₂, v₃}" requires M(d₁)(v₃) = a₃ ∈ coverage(F), which fails. The correct projection with the stated span is {v₁, v₂}.

**Required**: Change the span to (a₁, δ(3, m)), equivalently (a₁, shift(a₃, 1) ⊖ a₁), giving reach = [..., x+3] and denotation covering all three addresses. Alternatively, rephrase: "coverage(F) ⊇ {a₁, a₂, a₃}" requires width 3, not the difference between endpoints. Propagate the fix through the F11/F14 projection verification.

### Issue 2: Empty-endset boundary case unverified
**ASN-0079, EndsetSatisfaction / Worked Example**: No discussion of sat(e, P) when e = ∅.
**Problem**: Empty endsets are valid (Endset = 𝒫_fin(Span), ∅ ∈ Endset, per ASN-0047). When e = ∅, coverage(∅) = ∅, so sat(∅, P) = ∅ ∩ P ≠ ∅ = false for any P ≠ ⊤, while sat(∅, ⊤) = true. This means a link with an empty from-endset is never found by a from-endset content query but IS found by the fully unconstrained query (⊤, ⊤, ⊤, ⊤). The behavior follows from the formalism but is never stated or verified. A reader expecting "find all links whose from-endset touches this content" might not realize that links with empty from-endsets are silently excluded.
**Required**: State the boundary case explicitly — either in the EndsetSatisfaction definition or in the worked example. One sentence suffices: "When e = ∅, coverage(e) = ∅, so sat(∅, P) = false for every P ≠ ⊤: a link with an empty endset in slot i is invisible to any constrained query on that slot."

### Issue 3: F1a states unnecessary disjointness precondition
**ASN-0079, F1a**: "For disjoint sets P₁, ..., Pₘ and endset e: sat(e, P₁ ∪ ... ∪ Pₘ) ⟺ sat(e, P₁) ∨ ... ∨ sat(e, Pₘ)"
**Problem**: The proof — "coverage(e) ∩ (P₁ ∪ ... ∪ Pₘ) ≠ ∅ iff (E j : coverage(e) ∩ Pⱼ ≠ ∅)" — is the distributive law A ∩ (∪ Bⱼ) = ∪ (A ∩ Bⱼ) followed by "a union is non-empty iff some component is non-empty." Neither step uses disjointness. The precondition restricts the lemma to resolution-derived queries when the result holds for arbitrary finite unions, limiting downstream use.
**Required**: Remove "disjoint" from the precondition: "For sets P₁, ..., Pₘ and endset e: ..."

### Issue 4: F19 scaling requirement internally inconsistent
**ASN-0079, F19 — ScaleIndependence**: "The cost of evaluating FindLinks(Q) must not grow with |dom(Σ.L)| — the total number of links in the system — but rather with the query size and the result size."
**ASN-0079, same section**: "The constraint mandates that any conforming implementation maintain index structures enabling sublinear retrieval."
**Problem**: "Must not grow with |dom(Σ.L)|" means cost = f(query_size, result_size) with no dependence on the total link count — this is O(1) in |dom(L)|. "Sublinear retrieval" admits O(log |dom(L)|) or O(√|dom(L)|), which are sublinear but DO grow with |dom(L)|. A tree-based index provides O(log n) lookups — sublinear but not independent of n. The formal statement and the informal discussion impose different requirements, and an implementation satisfying one might violate the other.
**Required**: Clarify the precise scaling requirement. Either weaken the formal statement to "sublinear in |dom(Σ.L)|" (admitting logarithmic overhead from index traversal), or justify the O(1) claim by describing the index structure that achieves it (e.g., hash-based direct lookup on I-addresses). The two paragraphs must agree.

## OUT_OF_SCOPE

### Topic 1: Span-based search constraints for type hierarchy queries
**Why out of scope**: The SearchConstraint definition restricts to finite address sets P ⊂ T. But L10 (TypeHierarchyByContainment, ASN-0043) defines subtypes(p) = {c : p ≼ c} — an infinite set. A query "find all links of any subtype of p" cannot be expressed as a finite P. Extending SearchConstraint to accept span-based constraints (matching the structure of endsets themselves) would enable efficient type-hierarchy queries. This is a natural extension of the query algebra, not an error in the current definitions.

### Topic 2: Access control model specification
**Why out of scope**: The ASN introduces accessible(u) as an opaque function without grounding it in the state model Σ = (C, L, E, M, R). Whether access control is a component of Σ, what "user" means in terms of entities (accounts? nodes?), and what invariants accessible(u) must satisfy are all deferred. The composition of FINDLINKS with access filtering (F15, F16) is correctly specified given the abstract accessible function; defining that function belongs in a future ASN on authorization.

VERDICT: REVISE
