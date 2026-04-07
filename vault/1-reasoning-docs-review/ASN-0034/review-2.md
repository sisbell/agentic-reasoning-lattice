# Review of ASN-0034

## REVISE

### Issue 1: T4 does not explicitly require non-empty fields

**ASN-0034, T4 (Hierarchical parsing)**: "Every tumbler `t ∈ T` used as an address contains at most three zero-valued components, appearing in order as field separators, and every non-separator component is strictly positive."

**Problem**: The positive-component constraint requires each field *component* to be strictly positive, but this is vacuously true for an empty field. The formal statement does not require each present field to have at least one component. A tumbler like `[1, 0, 0, 3]` (consecutive zeros) has `zeros = 2`, classifying it as a document address with node field `[1]`, empty user field, and document field `[3]`. The positive-component constraint holds vacuously on the empty user field. Similarly, `[1, 0, 3, 0]` (trailing zero) has `zeros = 2` with an empty document field. Both are clearly not intended as valid addresses.

The phrase "appearing in order as field separators" *could* be read as requiring that each zero separate two non-empty fields, but this interpretation is not formalized. The formal statement `zeros(t) = #{i : 1 ≤ i ≤ #t ∧ tᵢ = 0}` counts zeros syntactically, without regard to whether they separate non-empty fields.

**Required**: Add an explicit non-empty field constraint: each present field has at least one component. Equivalently: no two zeros are adjacent, no tumbler used as an address begins with zero, and no tumbler used as an address ends with zero. This is necessary for the claim "the zero count → level mapping uniquely determines the hierarchical level" to carry its intended force — without it, degenerate parses are formally admitted.

---

### Issue 2: T12 omits the TA0 precondition

**ASN-0034, T12 (Span well-definedness)**: "A span `(s, ℓ)` with `ℓ > 0` denotes the set `{t ∈ T : s ≤ t < s ⊕ ℓ}`."

**Problem**: The span definition depends on `s ⊕ ℓ` being well-defined. By TA0, this requires the action point `k` of `ℓ` to satisfy `k ≤ #s`. If `ℓ` has more leading zeros than `s` has components — say `s = [1, 0, 3]` and `ℓ = [0, 0, 0, 0, 5]` — then `k = 5 > 3 = #s` and `s ⊕ ℓ` is undefined. T12 does not state this precondition. The non-emptiness argument ("TA-strict gives `s ⊕ ℓ > s`") inherits the same dependency but does not acknowledge it.

**Required**: T12 should state explicitly: `(s, ℓ)` is a well-formed span when `ℓ > 0` and the action point of `ℓ` satisfies `k ≤ #s`. Alternatively: the displacement's leading zero count must be strictly less than `#s`.

---

### Issue 3: Worked example states a false set equality

**ASN-0034, Worked example, T12**: "The span denotes `{t : a₂ ≤ t < a₅} = {a₂, a₃, a₄}`."

**Problem**: The set `{t ∈ T : a₂ ≤ t < a₅}` is infinite. Between `a₂` and `a₃` alone, there are infinitely many tumblers: `a₂.0`, `a₂.1`, `a₂.0.0`, etc. — all proper extensions of `a₂` that precede `a₃` under T1. The ASN itself recognizes this distinction: "A span that contains nothing today may at a later time contain a million documents." T12 defines the span over all of T, not over allocated addresses. The equality as written is a mathematical error.

**Required**: Replace the equality with a statement about the allocated content of the span: "Among the five allocated addresses, the span covers `{a₂, a₃, a₄}`." Or: "The allocated addresses within the span are `a₂, a₃, a₄`." The distinction between the span as a range in T (infinite) and the span's current population (finite) is load-bearing for the entire design and should not be blurred in the canonical worked example.

---

### Issue 4: TA3 verification, Case 0 has two gaps

**ASN-0034, Verification of TA3, Case 0**: "a is a proper prefix of b."

**Problem (a)**: The proof begins "Since `a ≥ w`, the divergence `dₐ` between `a` (zero-padded) and `w` (zero-padded) satisfies `dₐ ≤ #a`" and proceeds to reason about `dₐ` as though it exists. But the precondition `a ≥ w` admits `a = w`, in which case no divergence exists — the subtraction definition handles `a = w` as a separate case (result is the zero tumbler). This sub-case is reachable (since `a < b` and `a = w` are compatible), and is trivially resolved (`a ⊖ w = [0, ..., 0] ≤ b ⊖ w` since `b > w`), but is not stated.

**Problem (b)**: The proof concludes: "Since `a ⊖ w` is no longer than `b ⊖ w` and at every shared position `(a ⊖ w)ᵢ ≤ (b ⊖ w)ᵢ`, we have `a ⊖ w ≤ b ⊖ w`." Pointwise comparison does not determine lexicographic order. The conclusion happens to be correct here because the two results agree on positions `1, ..., #a` and beyond that `(a ⊖ w)ᵢ = 0 ≤ bᵢ = (b ⊖ w)ᵢ` — so the first lexicographic disagreement (if any) has `a ⊖ w` at 0 and `b ⊖ w` at a positive value, and if no disagreement occurs, `a ⊖ w` is a prefix of `b ⊖ w`. But the justification as written invokes a principle (pointwise ⟹ lexicographic) that does not hold in general.

**Required**: (a) Handle the `a = w` sub-case explicitly at the start of Case 0 — it's one sentence. (b) Replace the pointwise-comparison summary with the correct lexicographic argument: the first disagreement position (if any) has `(a ⊖ w) = 0 < (b ⊖ w)`, and if no disagreement exists, `a ⊖ w` is a prefix of `b ⊖ w`.

---

### Issue 5: Reverse inverse proof omits a precondition check

**ASN-0034, Corollary (Reverse inverse)**: "Apply TA3-strict (the equal-length precondition holds: `#a = k = #(y ⊕ w)`)."

**Problem**: TA3-strict requires three preconditions beyond strict ordering: `a ≥ w`, `b ≥ w` (where `b` is `y ⊕ w` or `a` depending on the case), and `#a = #b`. The proof verifies the equal-length condition but does not verify `y ⊕ w ≥ w`. The check is straightforward: under the assumption `y ⊕ w ≠ a`, the displacement `y` must have `yₖ > 0` (otherwise `y` is all-zeros, `y ⊕ w = w = a`, contradicting the assumption). Then `(y ⊕ w)ₖ = yₖ + wₖ > wₖ` with agreement on positions before `k`, giving `y ⊕ w > w`. But this argument is absent.

**Required**: State the `y ⊕ w ≥ w` check explicitly: note that `y ⊕ w = a` when `yₖ = 0` (contradicting the assumption), so `yₖ > 0`, giving `y ⊕ w > w`.

---

## OUT_OF_SCOPE

### Topic 1: Finite implementation constraints
The ASN notes that Gregory's fixed-width representation violates T0 and asks (in Open Questions) what constraints a finite implementation must satisfy. Characterizing when bounded representations are adequate — e.g., a finite-model property guaranteeing that no reachable allocation state exercises the bound — is a future ASN about implementation correctness, not a revision of the abstract algebra.

**Why out of scope**: T0 defines the abstract requirement; whether and how a finite implementation can satisfy it in practice is a separate question.

### Topic 2: Zero sentinel interaction with span arithmetic
The ASN defines zero tumblers as sentinels (TA6) and spans as intervals (T12), but does not specify how span operations behave when an endpoint is a zero sentinel. This is listed as an open question in the ASN itself.

**Why out of scope**: The sentinel convention requires operational rules (e.g., "zero-endpoint spans denote unbounded ranges") that depend on the system's containment and intersection semantics, which this ASN does not define.

### Topic 3: Shift composition
The ASN asks under what conditions `(a ⊕ w₁) ⊕ w₂ = a ⊕ (w₁ ⊕ w₂)` holds. Since `⊕` is explicitly non-associative and shifts are applied as single operations, composition conditions belong in a future ASN if any system guarantee turns out to depend on them.

**Why out of scope**: The current ASN establishes the non-associativity and identifies this as an open question. No property in this ASN depends on the answer.

VERDICT: REVISE
