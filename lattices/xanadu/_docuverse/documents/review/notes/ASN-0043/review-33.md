## Foundation Consistency Check: ASN-0043

### 1. Stale Labels

All citations checked against ASN-0034 and ASN-0036 foundation statements: T2, T3, T4, T5, T6, T7, T9, T10, T10a, T12, TA5(d), TA-strict, OrdinalDisplacement, OrdinalShift; S0, S3, S4, S5, S7, S7a, S7b. All present and correctly named.

(none)

### 2. Local Redefinitions

`GlobalUniqueness` extends S4 (OriginBasedIdentity) beyond I-addresses to all element-level tumblers. S4 in ASN-0036 is explicitly scoped to `dom(Σ.C)`. GlobalUniqueness is a genuine domain extension — not present in either foundation — correctly labeled `introduced`.

(none)

### 2a. Unjustified Domain Extensions

`home(a)` applies the `origin` formula to `dom(Σ.L)`. The ASN justifies this: link addresses are tumblers used as addresses (keys in `Σ.L`), so T4 applies; L1 establishes `zeros(a) = 3`, making `fields` well-defined. The extension is explicitly argued, not assumed.

(none)

### 2b. Incomplete Precondition Transfer

**Mechanical check — link analog of S7.** S7's "Follows from" list: S7a, S7b, T4, T9, T10, T10a, TA5, T3 (ASN-0034). The ASN maps these as: L1a → S7a, L1 → S7b, and the same three cases via T9, T10, T10a + TA5(d) + T3. T4 is cited explicitly in the surrounding text. All prerequisites accounted for.

**Mechanical check — GlobalUniqueness extending S4.** S4 Follows from: T9, T10, T10a + TA5(d) + T3. GlobalUniqueness cites all five. Complete.

**Principled check — GlobalUniqueness.** The three foundation axioms are verified to have no subspace or store-specific quantifier restrictions: T9 quantifies over all allocator-produced tumblers, T10 over all prefix pairs, T10a over any allocator. No implicit assumption applies only to content-subspace addresses. Principled transfer is supported.

(none)

### 2c. Transfer by Assertion

The GlobalUniqueness extension uses "apply identically to link-subspace allocations." Each of the three cases is checked individually: (1) T9 is universally quantified, giving `a < b` hence `a ≠ b` for any same-allocator pair regardless of subspace; (2) T10 is universally quantified over prefix pairs; (3) T10a + TA5(d) + T3 describes allocator depth discipline independent of subspace — child outputs have strictly greater depth than parent, ensuring distinctness by T3. The claim is verified per-case, not merely asserted.

(none)

### 2d. Quantifier Domain Mismatch

**Finding 1.** In the "Endset Structure" section, the motivating text for hierarchical type classification cites T6 for the claim that "tumbler containment is decidable":

> "Because tumbler containment is decidable (T6, ASN-0034), type addresses support hierarchical relationships: a type at address `p` and a subtype at an address extending `p` are related by prefix ordering."

T6 (DecidableContainment) establishes decidability for four specific questions: whether two tumblers share the same node field (a), node+user fields (b), node+user+document-lineage fields (c), and whether the *document field* of one is a prefix of the *document field* of the other (d). T6 does not cover element-field prefix containment — the relevant relationship for type hierarchies, where type addresses are element-level tumblers. For `p = 1.0.2.6` and `c = 1.0.2.6.2`, the question "is `p` a prefix of `c`?" involves the full tumbler, not the document field; T6(d) covers document-field prefix containment specifically and does not extend to this case. The correct foundation citation for this claim is T2 (IntrinsicComparison) — comparison is computable from the tumblers alone — combined with the PrefixRelation definition. The formal proof of L10 itself is unaffected (it relies on T5 and PrefixSpanCoverage, not T6), but the motivating citation misapplies T6's stated scope.

### 2e. Scope Narrowing in Citations

(none)

### 3. Structural Drift

T4 field notation (`N.0.U.0.D.0.E`), `zeros(t)`, `fields(t)`, and the `origin` formula all match current foundation definitions. The subspace designation via `E₁` in L0 is consistent with ASN-0036's `subspace(v) = v₁`. No outdated content.

(none)

### 4. Missing Dependencies

All cited properties trace to ASN-0034 or ASN-0036, both in the declared depends list. No undeclared dependency.

(none)

### 5. Exhaustiveness Gaps

L14 (DualPrimitive) claims only two categories of stored entity. The state is defined as `Σ = (Σ.C, Σ.M, Σ.L)` with arrangements `Σ.M(d)` explicitly not storing entities. The claim "no third category" is grounded in the state definition. S3 restricts arrangements to content addresses; L0 excludes link addresses from content; the exhaustiveness follows definitionally.

(none)

### 6. Registry Mismatches

All properties in the table verified against body text: `introduced` entries contain new content; none listed as `cited` (so the converse does not apply). L4 (LEMMA) follows from L3 by definitional unpacking — the body explains this explicitly. L7 (META) is a meta-statement with no formal proof; the type META is non-standard but internally consistent. PrefixSpanCoverage (LEMMA) has a complete formal proof. No mismatch between registry status and body treatment.

(none)

---

`RESULT: 1 FINDING`
