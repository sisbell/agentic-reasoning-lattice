# Review of ASN-0079

## REVISE

### Issue 1: Variable naming collision between EndsetProjection definition and F12

**ASN-0079, Endset Projection section**: The definition introduces `project(a, i, d)` where `a` is a link address (`a ∈ dom(Σ.L)`). F12 then reuses `a` for an I-address (`M(d)(v₁) = M(d)(v₂) = a`) and switches to `ℓ` for the link address (`project(ℓ, i, d)`).

**Problem**: In a specification document, the same letter should not denote a link address in one formula and an I-address two paragraphs later. The formulas are each locally consistent, but a reader consulting the definition of `project` (where `a` is a link address) and then reading F12 (where `a` is an I-address and the link address is now `ℓ`) will be confused about what `a` means.

**Required**: Use a consistent naming convention throughout the projection section. The natural choice: `ℓ` for link addresses everywhere (matching F12, F13's context), and `a` exclusively for I-addresses. Rewrite the EndsetProjection definition as `project(ℓ, i, d) = {v ∈ dom(M(d)) : M(d)(v) ∈ coverage(Σ.L(ℓ).eᵢ)}`.

## OUT_OF_SCOPE

### Topic 1: Type hierarchy queries via the SearchConstraint framework

The ASN mentions L10 (TypeHierarchyByContainment) and L9 (TypeGhostPermission), suggesting that type-prefix queries are a use case. But the intersection-based satisfaction predicate operates point-wise: a link whose type endset is a span at a *child* type address does not match a query containing only the *parent* type address (since the parent is lexicographically before the child span, not within it). Expressing "find all links of type X or any subtype" requires either enumerating all allocated subtype addresses in P or introducing a prefix-based satisfaction mode. This interaction between type hierarchies and the query mechanism deserves its own treatment.

**Why out of scope**: The ASN correctly defines the intersection-based predicate and doesn't claim to solve type hierarchy queries. The L10 reference is context, not a claim of coverage.

### Topic 2: Formal definition of `accessible(u)` and its grounding in the entity hierarchy

The ASN introduces "user u" and `accessible(u) ⊆ E_doc` without connecting "user" to the entity hierarchy (nodes, accounts, documents in ASN-0047). The access filter properties (F15, F16) are correctly parameterized over an abstract access function.

**Why out of scope**: Access control is a separate concern. The ASN shows how any access model interacts with link discovery without over-specifying the model itself.

VERDICT: REVISE
