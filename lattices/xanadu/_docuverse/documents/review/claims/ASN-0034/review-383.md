# Regional Review — ASN-0034/TA-Pos (cycle 2)

*2026-04-22 22:21*

### Trichotomy clause contains conjuncts derivable from sibling axioms in the same slot
**Class**: REVISE
**Foundation**: NAT-order (NatStrictTotalOrder)
**ASN**: NAT-order formal contract: "`(A m, n ∈ ℕ :: (m < n ∧ ¬(m = n) ∧ ¬(n < m)) ∨ (¬(m < n) ∧ m = n ∧ ¬(n < m)) ∨ (¬(m < n) ∧ ¬(m = n) ∧ n < m))` (trichotomy)."
**Issue**: With irreflexivity and transitivity already declared as sibling axioms in the same slot, every negative conjunct inside the three trichotomy disjuncts is derivable. Asymmetry `m < n ⟹ ¬(n < m)` follows from irreflexivity + transitivity (assume both, conclude `m < m`, contradiction). `m < n ⟹ ¬(m = n)` follows from irreflexivity alone (substitute `n` for `m`, get `n < n`). Symmetric reasoning eliminates the negative conjuncts in the second and third disjuncts. The minimal axiom is the totality clause `(A m, n ∈ ℕ :: m < n ∨ m = n ∨ n < m)`; the mutual-exclusivity content is logical fallout of the other two axioms. This is the same defect cycle-3 flagged for successor-closure and cycle-7 flagged for `(A m, n :: m + n ∈ ℕ)` against the `+` signature — derivable clauses listed alongside the axioms that derive them, blurring which content is primitive.
**What needs resolving**: Either reduce the trichotomy clause to its non-derivable core (totality: `m < n ∨ m = n ∨ n < m`) and let asymmetry/exclusivity follow as consequences, or restructure so the asymmetry content lives in a slot separate from the strict-order axioms it follows from. The Axiom slot should not contain conjuncts that other clauses in the same slot already entail.

### NAT-closure does not axiomatize `0 ≠ 1`
**Class**: OBSERVE
**Foundation**: NAT-closure (NatArithmeticClosureAndIdentity); NAT-zero (NatZeroMinimum)
**ASN**: NAT-closure formal contract: "`1 ∈ ℕ` (one is a natural number)…". NAT-zero formal contract: "`0 ∈ ℕ` … `(A n ∈ ℕ :: 0 < n ∨ 0 = n)`."
**Issue**: The two distinguished naturals `0` and `1` are introduced separately, but no axiom asserts `0 ≠ 1`. Under just these axioms, instantiating NAT-zero's disjunction at `n = 1` yields `0 < 1 ∨ 0 = 1`, and nothing rules out the second disjunct. TA-Pos itself does not break under `0 = 1` (its claims are about equality of components against the literal `0`), so this does not invalidate anything in the present region — but a precise reader notes that the NAT cluster as written admits a degenerate model where `0 = 1`. (OBSERVE only.)

### TA-Pos typing-rationale paragraph explains why bound variables are typed rather than stating axiom content
**Class**: OBSERVE
**Foundation**: TA-Pos (PositiveTumbler)
**ASN**: TA-Pos prose: "The bound variable `i` is typed to ℕ because the projection `tᵢ` is defined by T0 only on the index domain `{1, …, #t} ⊆ ℕ` and the bounding relation `≤` is ℕ-typed; the explicit `i ∈ ℕ` keeps parity with the `(A n ∈ ℕ :: …)` form used by the sibling NAT axioms…"
**Issue**: The paragraph reads as remediation narration for the cycle-6 finding ("type the bound `i`") — it explains *why* `i` is typed `i ∈ ℕ` and offers a parity argument with sibling axioms. The fix itself (writing `i ∈ ℕ` in the quantifiers) is silent and self-evident in the contract; the surrounding prose justifying the choice is meta-content of the kind cycle-7 flagged in NAT-closure. (OBSERVE only — logged for register.)

VERDICT: REVISE
