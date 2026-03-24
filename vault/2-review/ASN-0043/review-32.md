## Foundation Consistency Check: ASN-0043 (Link Ontology)

---

### 1. Stale Labels

(none)

All citations — T4, T7, T9, T10, T10a, TA5(d), T3, T5, T6, T12, T0(a), T1, T2, T3, S0–S3, S4, S5, S7, S7a, S7b, OrdinalDisplacement, OrdinalShift — match current labels in ASN-0034 and ASN-0036.

---

### 2. Local Redefinitions

(none)

`home(a)` uses the same formula as `origin(a)` (ASN-0036) but is introduced as a new function on a new domain (`dom(Σ.L)`), not as a restatement of `origin`. `GlobalUniqueness` extends S4 to a strictly broader domain and is correctly marked `introduced`. No introduced property merely restates a foundation statement.

---

### 2a. Unjustified Domain Extensions

(none)

`home(a)` applies `fields(a)` to link addresses. T4 (HierarchicalParsing) is an axiom on *every tumbler used as an address*, not restricted to content addresses. L1 establishes `zeros(a) = 3`, placing link addresses at element level with all four fields present. The domain extension is justified explicitly: "T4's format guarantee and L1's zero count ensure `fields` is well-defined for link addresses."

---

### 2b. Incomplete Precondition Transfer

(none)

**GlobalUniqueness** (extends S4). S4 Follows-from verbatim: *T9, T10, T10a + TA5(d) + T3*. The ASN checks each prerequisite: T9 is "quantified over all tumblers sharing an allocator — no subspace restriction"; T10 is "quantified over all prefix pairs — no subspace restriction"; T10a "applies uniformly regardless of subspace." All three cases are individually verified to be subspace-agnostic. Complete.

**Link analog of S7**. S7 Follows-from verbatim: *S7a, S7b, T4, T9, T10, T10a, TA5, T3*. The analog claim reads "by the same three cases... — T9, T10, and T10a + TA5(d) + T3 — with L1a replacing S7a and L1 replacing S7b." T4 is absent from the parenthetical, but the preceding paragraph in the same section explicitly establishes T4's role: "T4 (HierarchicalParsing, ASN-0034) constrains all tumblers used as addresses to satisfy its format requirements. Link addresses are tumblers used as addresses — they are keys in Σ.L — so T4 applies to them directly." T4 is accounted for; the omission is notational, not substantive.

---

### 2c. Transfer by Assertion

(none)

The GlobalUniqueness argument explicitly works through each of the three cases for subspace-agnosticism rather than asserting transfer. The link analog of S7 references GlobalUniqueness (which has already established the subspace-agnostic nature of T9/T10/T10a) and states the structural analogs L1a/L1 by definition. Each step is supported.

---

### 2d. Quantifier Domain Mismatch

(none)

T7 is applied to element-level tumblers only: both `dom(Σ.L)` (L1: zeros = 3) and `dom(Σ.C)` (S7b: zeros = 3) consist of element-level tumblers, so `E₁` notation is well-defined in each application. T5 is applied to `{t ∈ T : p ≼ t}`, which is exactly its stated domain. TA5(d) and T3 are used for nesting-prefix distinctness, within their stated quantifier domains.

---

### 2e. Scope Narrowing in Citations

(none)

S3 is cited as `(A d, v : v ∈ dom(Σ.M(d)) : Σ.M(d)(v) ∈ dom(Σ.C))` — the full statement — and used correctly to conclude that no V-mapping can target a link address. No conditions are silently dropped.

---

### 3. Structural Drift

(none)

The ASN's use of T12 (SpanWellDefinedness), OrdinalDisplacement, OrdinalShift, TumblerAdd, and the tumbler ordering all match the current foundation definitions verbatim. The `fields` field-parsing structure matches T4's current form. The coverage definition correctly invokes TA0 preconditions via T12 well-formedness.

---

### 4. Missing Dependencies

(none)

All cited properties belong to ASN-0034 or ASN-0036, which are both in the declared depends list.

---

### 5. Exhaustiveness Gaps

(none)

L14's claim that stored entities partition into `dom(Σ.C) ∪ dom(Σ.L)` is consistent with the two-component model of ASN-0036 extended by the link store introduced here. V-positions are element-field tumblers (zeros = 0, per S8a) structurally disjoint from element-level addresses (zeros = 3), so they do not constitute a third stored-entity category. L12's immutability claim covers all entries in `dom(Σ.L)` for every state transition, paralleling S0 exhaustively.

---

### 6. Registry Mismatches

(none)

All `introduced` properties contain either a definition, a proof, or a design rationale consistent with their listed type. No `cited` properties appear in the table (there are none). L2 (OwnershipEndsetIndependence) is listed as LEMMA; while it is definitionally obvious from `home`'s construction, no contradiction exists between the registry entry and body text — the body states it as a first-principle consequence of the definition rather than claiming a non-trivial derivation. L4 is listed as LEMMA but the body correctly explains that its formal content is definitional while its substantive content is about the *absence* of constraints; this is consistent with the registry classification.

---

`RESULT: CLEAN`
