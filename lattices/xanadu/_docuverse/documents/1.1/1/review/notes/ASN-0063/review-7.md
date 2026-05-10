# Review of ASN-0063

## REVISE

### Issue 1: K.μ~ identity claim not established by cardinality argument
**ASN-0063, "Extending the Transition Framework" (S3★ preservation by K.μ~):** "Therefore r = 0 — no link-subspace positions are removed, and the bijection π acts as the identity on dom_L(M(d))."
**Problem**: The cardinality argument proves r = 0 (no link-subspace positions removed) and that π restricted to dom_L(M(d)) is a bijection onto dom_L(M'(d)) = dom_L(M(d)). It does not prove π(v) = v for each v in dom_L(M(d)). When M(d) is non-injective on link-subspace positions (permitted by S5, UnrestrictedSharing), π could be a non-trivial permutation — e.g., if v₁ and v₂ both map to the same link ℓ, π could swap them while satisfying M'(d)(π(v)) = M(d)(v). The identity claim is a non sequitur that the proof does not support.

The conclusion (S3★ preserved, link-subspace mappings fixed) is correct by a simpler route that avoids π entirely: K.μ⁻ removes r = 0 link-subspace positions, so all survive with values unchanged (K.μ⁻ frame: `(A v : v ∈ dom(M'(d)) : M'(d)(v) = M(d)(v))`). K.μ⁺ (amended) adds no link-subspace positions and preserves pre-existing values (K.μ⁺ frame: `(A v : v ∈ dom(M(d)) : M'(d)(v) = M(d)(v))`). Therefore M'(d) agrees with M(d) on all link-subspace positions, and S3★'s link clause holds because each value remains in dom(L).

**Required**: Replace the identity claim with this direct argument. State: "M'(d) restricted to dom_L(M(d)) equals M(d) restricted to dom_L(M(d)), because K.μ⁻ removes none of these positions (r = 0) and K.μ⁺ (amended) neither adds nor modifies link-subspace positions." Drop the reference to π acting as identity.

### Issue 2: S0 claimed independently sufficient for C' = C
**ASN-0063, "What Is Preserved" (CL4 reinforcement):** "two of which (#2 and #4) are independently sufficient as formal proofs"
**Problem**: Principle #2 (Istream immutability, S0) establishes `dom(C) ⊆ dom(C') ∧ (A a ∈ dom(C) : C'(a) = C(a))` — preservation of existing content. It does not establish `dom(C') ⊆ dom(C)` — prevention of new content. S0 proves half of C' = C (no modification or deletion) but not the other half (no addition). The full equality requires the frame conditions of K.λ and K.μ⁺_L, each of which specifies C' = C. Principle #4 (K.λ isolation) establishes C' = C for the K.λ step but not for K.μ⁺_L. Neither principle alone covers the full composite.
**Required**: Correct the parenthetical. S0 and K.λ's frame are each sufficient for their respective guarantees (existing content preserved; K.λ does not modify C) but neither is independently sufficient for the composite's C' = C. The main proof (frame analysis of both steps) is correct and should remain the authoritative derivation.

### Issue 3: P3 and P5 not extended for L
**ASN-0063, "Invariant Preservation" (CL11):** "L is a new state component not addressed by P3, but the extension is monotonic, consistent with P3's design."
**Problem**: The ASN extends the system state from (C, E, M, R) to (C, L, E, M, R) and updates four invariants for the extended state: S3 → S3★, P4 → P4★, J1 → J1★, J1' → J1'★. P3 (ArrangementMutabilityOnly) enumerates "(C, E, R)" as components that admit no contraction or reordering, and P5 (DestructionConfinement) enumerates the same three. Both exclude L. The ASN acknowledges P3's gap but does not resolve it; P5 is handled similarly ("both by extension — no information is lost"). This treatment is inconsistent with the other four invariant updates, where the ASN defines starred replacements with explicit formal statements.

L admits only extension (by L12, LinkImmutability) — the analog of P0 for links. The fact is present in the system but not reflected in P3 or P5.
**Required**: Define P3★ and P5★ (or equivalent) that include L in their enumerations. P3★: "No component other than M — specifically C, L, E, R — admits contraction or reordering." P5★: "dom(C), dom(L), E, and R can only grow; only M can lose information." The proofs are immediate from L12.

## OUT_OF_SCOPE

### Topic 1: K.μ⁺ amendment narrows the fork composite
The K.μ⁺ content-subspace restriction (`subspace(v) = s_C`) prevents the fork composite (J4, ASN-0047) from copying link-subspace mappings from d_src to d_new. In the pre-extension framework this is vacuous (no link-subspace mappings existed). In the extended framework, a document with links has link-subspace mappings that the fork's K.μ⁺ step cannot reproduce — it would need K.μ⁺_L instead. Whether forked versions should inherit link-subspace mappings is a design question for the version-creation ASN.
**Why out of scope**: Version creation is explicitly excluded from this ASN's scope.

### Topic 2: Foundation quantifier scope expansion
ASN-0036 S8a's commentary states "The range guard v₁ ≥ 1 excludes link-subspace V-positions (where v₁ = 0)." ASN-0063 correctly derives s_L > 0 (from L1 + T4: element-field components of valid addresses are strictly positive). This means v₁ ≥ 1 does NOT exclude link-subspace V-positions — it covers them. The formal quantifiers in S8, S8a, and B1 (ASN-0058) now range over both text and link subspaces, which is mathematically sound (link-subspace blocks are valid mapping blocks) but conflicts with the foundations' informal intent of "text subspace only." This is a pre-existing inconsistency in the foundation commentary, not an error introduced by ASN-0063.
**Why out of scope**: This requires updating foundation ASN commentary (ASN-0036, ASN-0058), not revising ASN-0063.

VERDICT: REVISE
