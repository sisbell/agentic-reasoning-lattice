## Foundation Consistency Check — ASN-0043

### 1. Stale Labels

(none)

All foundation citations resolve to current labels. T6, which was present in an earlier draft, was removed in revision 34 per commit `98091ab`. No surviving citation points to a deprecated label.

---

### 2. Local Redefinitions

(none)

All properties in the summary table are `introduced`. None restates a foundation statement verbatim.

---

### 2a. Unjustified Domain Extensions

**Finding 1.** `home(a)` applies the `origin` formula outside `origin`'s stated domain.

The foundation (ASN-0036, Definition — Origin) defines:

> `origin(a) = (fields(a).node).0.(fields(a).user).0.(fields(a).document)` for every `a ∈ dom(Σ.C)`.

ASN-0043 introduces `home(a)` using the identical formula for `a ∈ dom(Σ.L)`:

> "This is the same formula as `origin` (ASN-0036), applied here to link addresses rather than content addresses."

This applies the `origin` formula to a domain (`dom(Σ.L)`) outside `origin`'s stated domain (`dom(Σ.C)`). The registry correctly says `introduced`, and the ASN provides justification (T4, L1, L1a). Per Category 2a this is a finding regardless.

---

### 2b. Incomplete Precondition Transfer

(none)

**S7 link analog — mechanical check.** S7's Follows-from: `S7a, S7b, T4, T9, T10, T10a, TA5, T3 (ASN-0034)`.

The transfer statement ("by the same three cases … with L1a replacing S7a and L1 replacing S7b") accounts for S7a → L1a ✓, S7b → L1 ✓, T9/T10/T10a/TA5/T3 explicit ✓, and T4 is addressed in the immediately preceding sentence: "by L1 and T4 (HierarchicalParsing, ASN-0034), the prefix is recoverable from the address alone."

**S4 → GlobalUniqueness — mechanical check.** S4's Follows-from: `T9, T10, T10a + TA5(d) + T3`. All three cases are explicitly enumerated in the GlobalUniqueness argument, with each axiom's domain-independence verified in turn.

---

### 2c. Transfer by Assertion

(none)

GlobalUniqueness verifies each of T9, T10, and T10a step-by-step ("T9 … carries no subspace restriction; T10 … no subspace restriction; T10a … applies uniformly regardless of which subspace") before concluding transfer. The S7 link analog is backed by this prior verification. Neither transfer relies on unverified "same reasoning" claims.

---

### 2d. Quantifier Domain Mismatch

(none)

T7 is quantified over `T`; L1 and S7b establish `zeros = 3` for both link and content addresses before T7 is invoked to derive `dom(Σ.L) ∩ dom(Σ.C) = ∅`. T9, T10, T10a carry no subspace restrictions in their quantifier domains.

---

### 2e. Scope Narrowing in Citations

(none)

---

### 3. Structural Drift

(none)

TumblerAdd, OrdinalShift, T4 field structure, and T12 span condition are all used in forms consistent with their current foundation definitions.

---

### 4. Missing Dependencies

(none)

Every cited property is from ASN-0034 or ASN-0036, both in the declared depends list.

---

### 5. Exhaustiveness Gaps

(none)

L6 restricts its formal statement to the standard triple ("for the standard triple: `F ≠ G ⟹ (F,G,Θ) ≠ (G,F,Θ)`"), but the general case follows definitionally from L3 (links are sequences; sequence equality is component-wise). The restriction is explicitly qualified and not a gap.

---

### 6. Registry Mismatches

(none)

All `introduced` entries contain non-trivial proofs or witness constructions. No property contains a local proof while being listed as `cited` (all are `introduced`). L7's `META` type and L4's `(definitional from L3)` annotation are minor labelling observations but do not contradict body content.

---

`RESULT: 1 FINDING`
