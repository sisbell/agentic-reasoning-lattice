# Review of ASN-0099

## REVISE

### Issue 1: Operation vocabulary V conflates two incompatible state models

**ASN-0099, A1 (vocabulary scope) and F9-cor**: "Vocabulary scope: V = {K.σ, K.α, K.λ, K.δ, K.μ⁺, K.μ⁻, K.μ~, K.μ⁺_L, K.ρ} as published in ASN-0047 and ASN-0093."

**Problem**: This ASN operates in ASN-0047's *extended* state Σ = (C, L, M, E, R) — it uses E_doc, R, P8, etc. throughout. But the vocabulary imports K.σ from ASN-0093, whose state is the *un-extended* substrate (C, L, M) with no entity set and no provenance relation. ASN-0047's own transition vocabulary (ValidComposite★) is {K.α, K.δ, K.λ, K.μ⁺, K.μ⁺_L, K.μ⁻, K.ρ} plus the named composite K.μ~ — it does **not** include K.σ, because document registration in the extended state is performed by K.δ (Document case), which adds the document to both dom(M) and E and records the K.δ-ID bookkeeping. ASN-0093's K.σ adds a document to dom(M) without touching E. Applied in the extended state, K.σ would produce a state with a document in dom(M) but not in E_doc, violating M1 (dom(M) = E_doc, ASN-0047) and P8 (EntityHierarchy). There is no single published vocabulary equal to "the union as published in ASN-0047 and ASN-0093"; the two models register documents differently.

This does not break the findlinks *results* (K.σ publishes L′ = L, so A1a would hold for it vacuously). But A1 ("K.λ is the unique operation of V that modifies the link store"), F9-cor's single-step quantifier, and F9★'s multi-step closure all quantify over this V, and a downstream ASN consuming A1 "against an evolved vocabulary" (as A1 itself anticipates) inherits a mis-specified operation set.

**Required**: Either (a) drop K.σ and state V as ASN-0047's extended-state vocabulary {K.α, K.δ, K.λ, K.μ⁺, K.μ⁻, K.μ~, K.μ⁺_L, K.ρ}, noting that document registration is K.δ; or (b) if K.σ is genuinely intended to coexist, reconcile it with M1/P8 — explain how a K.σ transition keeps dom(M) = E_doc in the extended state, or restrict K.σ to the substrate layer and state explicitly that it is unreachable in the (C, L, M, E, R) model this ASN inhabits.

## OUT_OF_SCOPE

### Topic 1: Semantics of querying with I-addresses outside dom(Σ.C) ∪ dom(Σ.L)
**Why out of scope**: `findlinks(I, Σ)` is operationally total for any I ⊆ T (a ghost-endset link, per L9 of ASN-0043, would match against an unallocated coverage address). The ASN correctly defers the *interpretation* of such queries to a future ASN rather than constraining the operation. The deferral is appropriate.

### Topic 2: Inverse direction (FOLLOWLINK / endset-to-V-position resolution)
**Why out of scope**: This is the dual reader-side operation, properly named as a separate future ASN. FINDLINKS legitimately stops at producing the matching link set.

VERDICT: REVISE
