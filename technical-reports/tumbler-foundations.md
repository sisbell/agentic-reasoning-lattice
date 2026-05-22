# ASN-0034: Tumbler Algebra

*Shane Isbell* · *Last revised 2026-03-26*

The Xanadu addressing system assigns every entity a permanent address — a *tumbler* — and requires these addresses to support comparison, containment testing, arithmetic for span computation and position advancement, and coordination-free allocation across a global network. This report states the minimal set of properties any correct implementation must provide, deriving each from design requirements rather than from any particular representation.

Nelson conceived the system as "the tumbler line" — a flat linearization of a hierarchical tree, yielding a total order on all addresses. Gregory implemented it as fixed-width sign-magnitude arithmetic over 16-digit mantissas. Between these two accounts we find the abstract algebra: what must hold for any correct implementation, regardless of representation.

The properties are organized by dependency. Sections 2–13 develop the carrier set and order, hierarchical structure, allocation, arithmetic, spans, shifts, displacements, and global properties. Section 1 collects the natural-number axioms (NAT-*) on which the development depends.

---

## 1. Natural-number preliminaries

The development depends on a small set of axioms about the natural numbers ℕ — carrier set, total order, arithmetic closure, well-ordering, discreteness, and cancellation. These are stated here as a dependency layer; readers familiar with ℕ as a discrete ordered commutative monoid may skim this section and proceed.

**NAT-carrier (NatCarrierSet).** `ℕ` is a set, the carrier of natural numbers on which the NAT-* claims posit their operations and relations.

*Formal Contract:*
- *Axiom:* `ℕ` is a set (the carrier of natural numbers).
- *Depends:* (none).

**NAT-order (NatStrictTotalOrder).** Posited on the carrier `ℕ` — the set introduced by NAT-carrier — the binary relation `<` is a strict total order, with non-strict companion `≤` defined by `m ≤ n ⟺ m < n ∨ m = n` and reverse companions `≥` and `>` defined by `m ≥ n ⟺ n ≤ m` and `m > n ⟺ n < m`.

Strict total order on ℕ means three clauses hold jointly:
- Irreflexivity: `¬(n < n)` for every `n ∈ ℕ`
- Transitivity: `m < n ∧ n < p ⟹ m < p` for every `m, n, p ∈ ℕ`
- At-least-one trichotomy: for any `m, n ∈ ℕ`, at least one of `m < n`, `m = n`, `n < m` holds

Together the three clauses yield *exactly-one trichotomy*: for any `m, n ∈ ℕ`, exactly one of `m < n`, `m = n`, `n < m` holds. Exactly-one is the at-least-one disjunction conjoined with three pairwise mutual-exclusion clauses. `¬(m < n ∧ n < m)` follows from transitivity — which chains `m < n` and `n < m` to `m < m` — against irreflexivity. `¬(m < n ∧ m = n)` follows by substituting `m = n` into `m < n` via indiscernibility of `=`, rewriting to `m < m`, which irreflexivity at `n := m` rules out. `¬(m = n ∧ n < m)` follows by the same substitution applied to `n < m`: rewriting under `m = n` yields `m < m`, again against irreflexivity.

The non-strict companion `≤` inherits transitivity from `<` and `=` jointly: `m ≤ n ∧ n ≤ p ⟹ m ≤ p`. Unfolding each hypothesis against the defining disjunction `x ≤ y ⟺ x < y ∨ x = y` yields four cases, and each discharges to `m ≤ p`. If both are strict — `m < n ∧ n < p` — `<`-transitivity gives `m < p`, so `m ≤ p` by the definition. If the first is strict and the second is equality — `m < n ∧ n = p` — indiscernibility of `=` substitutes `n = p` into `m < n` to yield `m < p`. The symmetric case `m = n ∧ n < p` substitutes `m = n` into `n < p` to yield `m < p`. If both are equalities — `m = n ∧ n = p` — transitivity of `=` gives `m = p`, so `m ≤ p`.

*Formal Contract:*
- *Axiom:* `< ⊆ ℕ × ℕ` (`<` is a binary relation on ℕ); `(A n ∈ ℕ :: ¬(n < n))` (irreflexivity); `(A m, n, p ∈ ℕ : m < n ∧ n < p : m < p)` (transitivity); `(A m, n ∈ ℕ :: m < n ∨ m = n ∨ n < m)` (at-least-one trichotomy).
- *Definition:* `(A m, n ∈ ℕ :: m ≤ n ⟺ m < n ∨ m = n)`; `(A m, n ∈ ℕ :: m ≥ n ⟺ n ≤ m)`; `(A m, n ∈ ℕ :: m > n ⟺ n < m)`.
- *Consequence:* Exactly-one trichotomy: `(A m, n ∈ ℕ :: (m < n ∨ m = n ∨ n < m) ∧ ¬(m < n ∧ n < m) ∧ ¬(m < n ∧ m = n) ∧ ¬(m = n ∧ n < m))`. The disjunction is the at-least-one axiom clause directly; `¬(m < n ∧ n < m)` follows from transitivity and irreflexivity; `¬(m < n ∧ m = n)` follows by substituting `m = n` into `m < n` via indiscernibility of `=`, rewriting to `m < m` against irreflexivity at `n := m`; `¬(m = n ∧ n < m)` follows by the same substitution applied to `n < m`.
- *Consequence:* `≤`-transitivity: `(A m, n, p ∈ ℕ : m ≤ n ∧ n ≤ p : m ≤ p)`. Unfolding each hypothesis by the definition `x ≤ y ⟺ x < y ∨ x = y` yields four cases. `m < n ∧ n < p` gives `m < p` by `<`-transitivity, hence `m ≤ p`. `m < n ∧ n = p` gives `m < p` by substituting `n = p` into `m < n` via indiscernibility of `=`, hence `m ≤ p`. `m = n ∧ n < p` gives `m < p` by substituting `m = n` into `n < p`, hence `m ≤ p`. `m = n ∧ n = p` gives `m = p` by transitivity of `=`, hence `m ≤ p`.
- *Depends:*
  - NAT-carrier (NatCarrierSet) — supplies `ℕ` as the underlying set on which the strict order `<` is posited (`< ⊆ ℕ × ℕ`), over which the bounded quantifiers `(A n ∈ ℕ :: ...)`, `(A m, n ∈ ℕ :: ...)`, and `(A m, n, p ∈ ℕ : ... :: ...)` appearing in the irreflexivity, trichotomy, and transitivity clauses range, and on which the non-strict companion `≤` and the reverse companions `≥` and `>` are defined.

**NAT-closure (NatArithmeticClosureAndIdentity).** The binary operation `+ : ℕ × ℕ → ℕ` is posited directly on ℕ; the numeral `1` is in ℕ; `0` is a two-sided additive identity for `+`; and the addition-based successor `n + 1` is strictly above `0` for every `n ∈ ℕ`.

The signature `+ : ℕ × ℕ → ℕ` makes `+` total on `ℕ × ℕ` and closes its result in ℕ.

The membership clause `1 ∈ ℕ` names a second constant in ℕ.

The clause `(A n ∈ ℕ :: 0 < n + 1)` is the Peano no-predecessor-of-zero condition phrased for the addition-based successor: no `n ∈ ℕ` has `n + 1 = 0`. The strict-order placement of `1` falls out as a consequence: instantiating successor-positivity at `n := 0` gives `0 < 0 + 1`; the left-identity clause `(A n ∈ ℕ :: 0 + n = n)` at `n := 1` gives `0 + 1 = 1`; substitutivity of `=` then rewrites the right-hand side of the inequality, yielding `0 < 1`. This derivation pins down only the single sum `0 + 1`; without the universal clause, a model could satisfy the signature, the identity laws, and the bare `0 < 1` while still permitting `m + 1 = 0` at some `m ≥ 1`. The universal clause closes that gap uniformly across ℕ.

*Formal Contract:*
- *Axiom:* `+ : ℕ × ℕ → ℕ` (`+` is a binary operation on ℕ); `1 ∈ ℕ` (one is a natural number); `(A n ∈ ℕ :: 0 + n = n)` (left additive identity); `(A n ∈ ℕ :: n + 0 = n)` (right additive identity); `(A n ∈ ℕ :: 0 < n + 1)` (successor positivity — the addition-based successor is never `0`).
- *Consequence:* `0 < 1` (the named constants `0` and `1` are distinct in the strict order) — derived from the successor-positivity clause `(A n ∈ ℕ :: 0 < n + 1)` instantiated at `n := 0`, the left-identity clause `(A n ∈ ℕ :: 0 + n = n)` instantiated at `n := 1`, and substitutivity of `=`, as shown in the preceding prose.
- *Depends:*
  - NAT-carrier (NatCarrierSet) — supplies `ℕ` as the underlying set appearing as the domain `ℕ × ℕ` and codomain `ℕ` of the signature `+ : ℕ × ℕ → ℕ`, in the membership clause `1 ∈ ℕ`, and over which the bounded quantifiers `(A n ∈ ℕ :: 0 + n = n)`, `(A n ∈ ℕ :: n + 0 = n)`, and `(A n ∈ ℕ :: 0 < n + 1)` of the left-identity, right-identity, and successor-positivity clauses range.
  - NAT-zero (NatZeroMinimum) — supplies `0 ∈ ℕ` for the literal `0` appearing in the left-identity clause `0 + n = n`, the right-identity clause `n + 0 = n`, the successor-positivity clause `0 < n + 1`, and the *Consequence:* `0 < 1`.
  - NAT-order (NatStrictTotalOrder) — supplies the strict-order primitive `<` used in the successor-positivity clause `0 < n + 1` and in the *Consequence:* `0 < 1`.

**NAT-addcompat (NatAdditionOrderAndSuccessor).** Addition on ℕ is compatible with the order on either side, and `n < n + 1` for every `n ∈ ℕ`.

The two compatibility clauses are posited independently because at this stratum no commutativity has been declared: neither NAT-closure nor any predecessor supplies `(A x, y ∈ ℕ :: x + y = y + x)`, so the prefix `m + ·` of the left clause cannot be rewritten as the suffix `· + m` of the right. A model that orders its left additions faithfully while distorting its right ones satisfies left compatibility and violates right; neither clause yields the other in the absence of commutativity, and proofs that add a fixed summand on either side need both placements directly.

The strict successor inequality `n < n + 1` is bundled with the compatibility clauses rather than placed in NAT-closure beside the *Consequence:* `0 < 1`. NAT-closure's successor-positivity clause `(A n ∈ ℕ :: 0 < n + 1)` locates `n + 1` only above the constant `0`: instantiated at `n := 0` and rewritten by the left-identity `(A k ∈ ℕ :: 0 + k = k)` at `k := 1`, it yields `0 < 1`. The strict successor inequality is the stronger, schematic statement that `+1` strictly advances every `n ∈ ℕ`, so it sits with the other clauses parameterised in `n` that connect `+` to `<` and `≤`, not with the constant inequality NAT-closure derives.

*Formal Contract:*
- *Axiom:* `(A m, n, p ∈ ℕ : p ≤ n : m + p ≤ m + n)` (left order compatibility); `(A m, n, p ∈ ℕ : p ≤ n : p + m ≤ n + m)` (right order compatibility); `(A n ∈ ℕ :: n < n + 1)` (strict successor inequality).
- *Depends:*
  - NAT-carrier (NatCarrierSet) — supplies `ℕ` as the underlying set over which the bounded universals `(A m, n, p ∈ ℕ : p ≤ n : m + p ≤ m + n)` and `(A m, n, p ∈ ℕ : p ≤ n : p + m ≤ n + m)` of the two compatibility clauses range, and over which the bounded universal `(A n ∈ ℕ :: n < n + 1)` of the strict successor inequality ranges.
  - NAT-order (NatStrictTotalOrder) — supplies the primitive strict order `<` (used in the strict successor inequality `n < n + 1`) and its non-strict companion `≤` (defined by `m ≤ n ⟺ m < n ∨ m = n`, used in the antecedents `p ≤ n` and the consequents `m + p ≤ m + n` and `p + m ≤ n + m` of both compatibility clauses).
  - NAT-closure (NatArithmeticClosureAndIdentity) — posits `1 ∈ ℕ` and closes ℕ under addition, so every sum `m + p`, `m + n`, `p + m`, `n + m`, and `n + 1` appearing in the axiom lies in ℕ, and the successor inequality `n < n + 1` compares two ℕ-elements.

**NAT-addassoc (NatAdditionAssociative).** Addition on ℕ is associative: `(m + n) + p = m + (n + p)` for every `m, n, p ∈ ℕ`.

Two primitives appear in the axiom that are not introduced here. The binary operation `+` is the one posited by NAT-closure's signature clause `+ : ℕ × ℕ → ℕ`; the associativity equation uses `+` at exactly that arity, and without NAT-closure supplying the signature the left- and right-hand sides would reference an ungrounded symbol. The carrier `ℕ` governing the quantifier range is the set introduced by NAT-carrier; both prereqs are listed directly, matching the convention the surrounding NAT-* claims follow of naming every directly-used predecessor rather than relying on transitive reachability.

*Formal Contract:*
- *Axiom:* `(A m, n, p ∈ ℕ :: (m + n) + p = m + (n + p))` (associativity of addition on ℕ).
- *Depends:*
  - NAT-carrier (NatCarrierSet) — supplies `ℕ` as the underlying set over which the bounded universal `(A m, n, p ∈ ℕ :: (m + n) + p = m + (n + p))` of the associativity axiom ranges.
  - NAT-closure (NatArithmeticClosureAndIdentity) — supplies the binary operation `+ : ℕ × ℕ → ℕ` whose associativity is here posited, ensuring every sum `m + n`, `n + p`, `(m + n) + p`, and `m + (n + p)` appearing in the axiom is an ℕ-element.

**NAT-addbound (NatAdditionDominatesOperands).** For every `m, n ∈ ℕ`, the sum `m + n` is bounded below by each of its operands: `m + n ≥ n` (right dominance) and `m + n ≥ m` (left dominance).

*Right dominance.* Fix `m, n ∈ ℕ`. NAT-zero's minimality clause `(A k ∈ ℕ :: 0 < k ∨ 0 = k)`, instantiated at `k := m`, delivers `0 < m ∨ 0 = m`; NAT-order's defining equivalence `a ≤ b ⟺ a < b ∨ a = b`, instantiated at `(a, b) := (0, m)`, rewrites this disjunction as `0 ≤ m`. NAT-addcompat's right order compatibility `(A m', n', p ∈ ℕ : p ≤ n' : p + m' ≤ n' + m')`, instantiated under the renaming `(p, n', m') := (0, m, n)`, then yields the implication `0 ≤ m ⟹ 0 + n ≤ m + n`; modus ponens with the just-established `0 ≤ m` gives `0 + n ≤ m + n`. NAT-closure's left additive identity `(A k ∈ ℕ :: 0 + k = k)`, instantiated at `k := n`, rewrites the left-hand side to `n`, leaving `n ≤ m + n`. NAT-order's defining equivalence `a ≥ b ⟺ b ≤ a`, instantiated at `(a, b) := (m + n, n)`, then converts this to the stated `m + n ≥ n`. The choice of `m, n` was arbitrary, so the conclusion holds universally. ∎

*Left dominance.* Fix `m, n ∈ ℕ`. NAT-zero's minimality clause, instantiated at `k := n`, delivers `0 < n ∨ 0 = n`; NAT-order's `≤`-definition at `(a, b) := (0, n)` rewrites this disjunction as `0 ≤ n`. NAT-addcompat's left order compatibility `(A m', n', p ∈ ℕ : p ≤ n' : m' + p ≤ m' + n')`, instantiated under the renaming `(m', n', p) := (m, n, 0)`, then yields the implication `0 ≤ n ⟹ m + 0 ≤ m + n`; modus ponens with the just-established `0 ≤ n` gives `m + 0 ≤ m + n`. NAT-closure's right additive identity `(A k ∈ ℕ :: k + 0 = k)`, instantiated at `k := m`, rewrites the left-hand side to `m`, leaving `m ≤ m + n`. NAT-order's `≥`-definition at `(a, b) := (m + n, m)` then converts this to the stated `m + n ≥ m`. The choice of `m, n` was arbitrary, so the conclusion holds universally. ∎

*Formal Contract:*
- *Consequence:* `(A m, n ∈ ℕ :: m + n ≥ n)` (the sum dominates its right operand) — derived from NAT-zero, NAT-addcompat (right order compatibility), NAT-closure (left additive identity), and NAT-order as shown in the preceding *Right dominance* prose.
- *Consequence:* `(A m, n ∈ ℕ :: m + n ≥ m)` (the sum dominates its left operand) — derived from NAT-zero, NAT-addcompat (left order compatibility), NAT-closure (right additive identity), and NAT-order as shown in the preceding *Left dominance* prose.
- *Depends:*
  - NAT-carrier (NatCarrierSet) — supplies `ℕ` as the underlying set over which the bounded universals `(A m, n ∈ ℕ :: m + n ≥ n)` and `(A m, n ∈ ℕ :: m + n ≥ m)` of the two dominance Consequences range, and from which the fixed `m, n` of the right- and left-dominance derivations are drawn.
  - NAT-zero (NatZeroMinimum) — supplies the minimality clause `(A k ∈ ℕ :: 0 < k ∨ 0 = k)`, consumed by both the right-dominance and left-dominance derivations.
  - NAT-addcompat (NatAdditionOrderAndSuccessor) — supplies the right order compatibility clause `(A m', n', p ∈ ℕ : p ≤ n' : p + m' ≤ n' + m')`, consumed by the right-dominance derivation; and the left order compatibility clause `(A m', n', p ∈ ℕ : p ≤ n' : m' + p ≤ m' + n')`, consumed by the left-dominance derivation.
  - NAT-closure (NatArithmeticClosureAndIdentity) — supplies the left additive identity `(A k ∈ ℕ :: 0 + k = k)`, consumed by the right-dominance derivation, and the right additive identity `(A k ∈ ℕ :: k + 0 = k)`, consumed by the left-dominance derivation; also underpins the binary operation `+` whose value `m + n` is here bounded below by each operand.
  - NAT-order (NatStrictTotalOrder) — supplies the defining equivalences `a ≤ b ⟺ a < b ∨ a = b` and `a ≥ b ⟺ b ≤ a`, consumed by both derivations.

**NAT-cancel (NatAdditionCancellation).** Addition on ℕ is cancellative on either side. A sum equals one of its summands only when the other summand is zero — a consequence of cancellation together with NAT-closure's two-sided additive identity.

- Left cancellation (axiom): `m + n = m + p ⟹ n = p` for every `m, n, p ∈ ℕ`.
- Right cancellation (axiom): `n + m = p + m ⟹ n = p` for every `m, n, p ∈ ℕ`.
- Summand absorption (consequence): `m + n = m ⟹ n = 0` for every `m, n ∈ ℕ`.

Summand absorption follows from cancellation and NAT-closure's two-sided additive identity, in both its posited form `m + n = m ⟹ n = 0` and its mirror form `n + m = m ⟹ n = 0`. From the hypothesis `m + n = m` and NAT-closure's right identity `m + 0 = m` we have `m + n = m + 0`; left cancellation, instantiated at `p := 0`, then delivers `n = 0`. The mirror form admits the parallel walk: from the hypothesis `n + m = m` and NAT-closure's left identity `0 + m = m` we have `n + m = 0 + m`; right cancellation, instantiated at `p := 0`, then delivers `n = 0`.

*Formal Contract:*
- *Axiom:* `(A m, n, p ∈ ℕ : m + n = m + p : n = p)` (left cancellation); `(A m, n, p ∈ ℕ : n + m = p + m : n = p)` (right cancellation).
- *Consequence:* `(A m, n ∈ ℕ : m + n = m : n = 0)` (summand absorption, posited form) — derived from the left-cancellation axiom and NAT-closure's right additive identity `n + 0 = n` instantiated at `n := m`, as shown in the preceding prose; the mirror form `(A m, n ∈ ℕ : n + m = m : n = 0)` is the parallel consequence, derived from right cancellation and NAT-closure's left additive identity `0 + n = n` instantiated at `n := m`.
- *Depends:*
  - NAT-carrier (NatCarrierSet) — supplies `ℕ` as the underlying set over which the bounded universals `(A m, n, p ∈ ℕ : m + n = m + p : n = p)` and `(A m, n, p ∈ ℕ : n + m = p + m : n = p)` of the two cancellation axioms range, and over which `(A m, n ∈ ℕ : m + n = m : n = 0)` (and the mirror form) of the summand-absorption Consequence ranges.
  - NAT-closure (NatArithmeticClosureAndIdentity) — supplies the binary operation `+ : ℕ × ℕ → ℕ` used in all clauses; the right additive identity `(A n ∈ ℕ :: n + 0 = n)`, instantiated at `n := m`, used to rewrite the RHS of `m + n = m` to `m + 0` in the derivation of the posited absorption form from left cancellation; and the left additive identity `(A n ∈ ℕ :: 0 + n = n)`, instantiated at `n := m`, used to rewrite the RHS of `n + m = m` to `0 + m` in the parallel derivation of the mirror form from right cancellation.
  - NAT-zero (NatZeroMinimum) — supplies `0 ∈ ℕ` for the literal `0` on the right-hand side of the absorption conclusion `m + n = m ⟹ n = 0`.

**NAT-sub (NatPartialSubtraction).** Subtraction on ℕ is a partial binary operation `− : {(m, n) ∈ ℕ × ℕ : m ≥ n} → ℕ`: whenever `m, n ∈ ℕ` satisfy `m ≥ n`, the difference `m − n` is the unique natural number characterised by `(m − n) + n = m`.

The axiom slot introduces `−` before constraining it: its first clause `− : {(m, n) ∈ ℕ × ℕ : m ≥ n} → ℕ` posits the signature — fixing arity (binary), domain of definition `{(m, n) ∈ ℕ × ℕ : m ≥ n}`, and codomain ℕ. Positing `−` as a function fixes single-valuedness on its domain: for each `(m, n)` with `m ≥ n`, `m − n` denotes a unique element of ℕ.

The following facts about partial subtraction and its interaction with addition and order on ℕ are stated together:

- Conditional closure: `m ≥ n ⟹ m − n ∈ ℕ` for every `m, n ∈ ℕ`.
- Right-inverse characterisation: `m ≥ n ⟹ (m − n) + n = m` for every `m, n ∈ ℕ`.
- Left-inverse characterisation: `m ≥ n ⟹ n + (m − n) = m` for every `m, n ∈ ℕ`.
- Right telescoping: `(m + n) − n = m` for every `m, n ∈ ℕ`.
- Left telescoping: `(n + m) − n = m` for every `m, n ∈ ℕ`.

Strict monotonicity — `m ≥ p ∧ n ≥ p ∧ m < n ⟹ m − p < n − p` — derives from the right-inverse together with NAT-addcompat's right order compatibility and NAT-order's at-least-one trichotomy with irreflexivity. Assume `m, n, p ∈ ℕ` with `m ≥ p`, `n ≥ p`, and `m < n`. Right-inverse at `(m, p)` and `(n, p)` delivers `(m − p) + p = m` and `(n − p) + p = n`; substituting both into `m < n` via indiscernibility of `=` rewrites the hypothesis to `(m − p) + p < (n − p) + p`. Abbreviate `a := m − p` and `b := n − p` — conditional closure places both in ℕ — so the rewritten hypothesis reads `a + p < b + p`. NAT-order's at-least-one trichotomy on `(a, b)` presents three cases. The `a < b` case is the desired conclusion `m − p < n − p`. The `a = b` case substitutes into `a + p < b + p` via indiscernibility to yield `a + p < a + p`, contradicting NAT-order's irreflexivity at `n := a + p`. The `b < a` case unfolds via NAT-order's `≤`-definition to `b ≤ a`; NAT-addcompat's right order compatibility applied at antecedent `b ≤ a` then delivers `b + p ≤ a + p`, which the `≤`-definition splits into `b + p < a + p ∨ b + p = a + p`. The `<` branch, conjoined with the already-established `a + p < b + p`, contradicts exactly-one trichotomy's `¬(x < y ∧ y < x)` clause at `(x, y) := (a + p, b + p)`; the `=` branch substitutes into `a + p < b + p` via indiscernibility to yield `a + p < a + p`, again against irreflexivity. Both disjuncts of the `b < a` case collapse, leaving `a < b`, i.e., `m − p < n − p`.

Strict positivity — `m > n ⟹ m − n ≥ 1` — derives from the right-inverse together with NAT-discrete: lifting `m − n ≠ 0` to `m − n ≥ 1` requires the discreteness fact that no natural number lies strictly between `0` and `1`, which NAT-discrete names. Assume `m, n ∈ ℕ` with `m > n`. NAT-order's reverse companion `m > n ⟺ n < m` and the `≤`-definition deliver `n ≤ m`, hence `m ≥ n`; conditional closure then places `m − n ∈ ℕ`. Suppose, for contradiction, that `m − n = 0`; the right-inverse rewrites `(m − n) + n = m` to `0 + n = m`, which NAT-closure's left-identity collapses to `n = m`, contradicting NAT-order's exactly-one-trichotomy Consequence's `¬(m < n ∧ m = n)` conjunct at `(m, n) := (n, m)` — the conjunction `n < m ∧ n = m` is ruled out, yet both sides are established (`n < m` from the hypothesis `m > n` unfolded by NAT-order's `m > n ⟺ n < m`, `n = m` from the collapse just derived). Hence `m − n ≠ 0`. NAT-zero's axiom clause `(A k ∈ ℕ :: 0 < k ∨ 0 = k)` at `k := m − n` then leaves `0 < m − n` once the equality branch is discarded, and NAT-discrete at `(m, n) := (0, m − n)` delivers `0 + 1 ≤ m − n`, which NAT-closure's left-identity reduces to `1 ≤ m − n`, i.e., `m − n ≥ 1`.

*Formal Contract:*
- *Axiom:* `− : {(m, n) ∈ ℕ × ℕ : m ≥ n} → ℕ` (signature: `−` is a partial binary operation on ℕ, single-valued on its domain of definition); `(A m, n ∈ ℕ : m ≥ n : m − n ∈ ℕ)` (conditional closure); `(A m, n ∈ ℕ : m ≥ n : (m − n) + n = m)` (right-inverse characterisation); `(A m, n ∈ ℕ : m ≥ n : n + (m − n) = m)` (left-inverse characterisation); `(A m, n ∈ ℕ :: (m + n) − n = m)` (right telescoping); `(A m, n ∈ ℕ :: (n + m) − n = m)` (left telescoping).
- *Consequence:* `(A m, n, p ∈ ℕ : m ≥ p ∧ n ≥ p ∧ m < n : m − p < n − p)` (strict monotonicity) — derived from the right-inverse clause, NAT-addcompat (right order compatibility), and NAT-order (at-least-one trichotomy, irreflexivity, the `≤`-definition, and the exactly-one-trichotomy Consequence's `¬(x < y ∧ y < x)` clause) as shown in the preceding strict-monotonicity prose.
- *Consequence:* `(A m, n ∈ ℕ : m > n : m − n ≥ 1)` (strict positivity) — derived from the right-inverse clause, NAT-closure (left additive identity and `1 ∈ ℕ`), NAT-order (the `>`/`≤`/`≥` definitions and the exactly-one-trichotomy Consequence's `¬(m < n ∧ m = n)` conjunct at `(m, n) := (n, m)`, contrapositively `n < m ⟹ n ≠ m`), NAT-zero (`(A k ∈ ℕ :: 0 < k ∨ 0 = k)`), and NAT-discrete (discreteness instantiated at `(0, m − n)`) as shown in the preceding strict-positivity prose.
- *Depends:*
  - NAT-carrier (NatCarrierSet) — supplies `ℕ` as the underlying set appearing in the signature `− : {(m, n) ∈ ℕ × ℕ : m ≥ n} → ℕ` (both as the Cartesian factor `ℕ × ℕ` filtering the domain and as the codomain), in the conditional-closure clause `m − n ∈ ℕ`, and over which the bounded universals of the inverse-characterisation, telescoping, strict-monotonicity, and strict-positivity clauses range.
  - NAT-order (NatStrictTotalOrder) — supplies the strict order `<` and its companions `≤`, `≥`, `>` (defined by `m ≤ n ⟺ m < n ∨ m = n`, `m ≥ n ⟺ n ≤ m`, `m > n ⟺ n < m`), used in the signature's domain condition `{(m, n) ∈ ℕ × ℕ : m ≥ n}` and in the antecedents `m ≥ n` of the conditional-closure and inverse-characterisation clauses; supplies the at-least-one trichotomy axiom and irreflexivity axiom, together with two conjuncts of the exactly-one-trichotomy Consequence — `¬(x < y ∧ y < x)`, against which the strict-monotonicity derivation dispatches the `a = b`, `b < a`-and-`<`, and `b < a`-and-`=` subcases, and `¬(m < n ∧ m = n)` at `(m, n) := (n, m)` (contrapositively `n < m ⟹ n ≠ m`), against which the strict-positivity derivation contradicts the `m − n = 0` case.
  - NAT-closure (NatArithmeticClosureAndIdentity) — posits `1 ∈ ℕ` and closes ℕ under addition, so every sum `(m − n) + n`, `n + (m − n)`, `m + n`, `n + m` appearing in the inverse-characterisation and telescoping clauses is an ℕ-element; additionally supplies the left-identity `(A k ∈ ℕ :: 0 + k = k)`, which the strict-positivity derivation invokes twice — once to collapse `0 + n = m` to `n = m`, once to collapse `0 + 1 ≤ m − n` to `1 ≤ m − n`.
  - NAT-addbound (NatAdditionDominatesOperands) — supplies the right-dominance clause `(A m, n ∈ ℕ :: m + n ≥ n)`, which discharges the conditional-closure precondition `m + n ≥ n` implicit in the right-telescoping clause `(m + n) − n = m`; and the left-dominance clause `(A m, n ∈ ℕ :: m + n ≥ m)`, instantiated at `(m, n) := (n, m)` to yield `n + m ≥ n`, which discharges the conditional-closure precondition implicit in the left-telescoping clause `(n + m) − n = m`.
  - NAT-addcompat (NatAdditionOrderAndSuccessor) — supplies right order compatibility `(A m, n, p ∈ ℕ : p ≤ n : p + m ≤ n + m)`, instantiated at antecedent `b ≤ a` in the strict-monotonicity derivation's `b < a` case to lift `b ≤ a` through right-addition by `p` to `b + p ≤ a + p`.
  - NAT-zero (NatZeroMinimum) — supplies the axiom clause `(A k ∈ ℕ :: 0 < k ∨ 0 = k)`, instantiated at `k := m − n` in the strict-positivity derivation to lift `m − n ≠ 0` to `0 < m − n` before NAT-discrete fires.
  - NAT-discrete (NatDiscreteness) — supplies `(A m, n ∈ ℕ :: m < n ⟹ m + 1 ≤ n)`, instantiated at `(m, n) := (0, m − n)` in the strict-positivity derivation to yield `0 + 1 ≤ m − n`, which NAT-closure's left-identity reduces to `m − n ≥ 1`.

**NAT-card (NatFiniteSetCardinality).** For every `n ∈ ℕ` and every subset `S ⊆ {j ∈ ℕ : 1 ≤ j ≤ n}`, we postulate `|·|` as a primitive operator with `|S| ∈ ℕ` the unique `k ∈ ℕ` for which there exists a strictly increasing function `f : {j ∈ ℕ : 1 ≤ j ≤ k} → ℕ` with `S = {f.j : 1 ≤ j ≤ k}` (at `k = 0` the domain `{j ∈ ℕ : 1 ≤ j ≤ 0}` is empty, `f` is the empty function, vacuously strictly increasing with image `∅`, forcing `S = ∅` and `|∅| = 0` without recourse to a convention on empty lists), and `|S| ≤ n`.

*Formal Contract:*
- *Axiom:* `(A n ∈ ℕ, S : S ⊆ {j ∈ ℕ : 1 ≤ j ≤ n} :: |S|` is the unique `k ∈ ℕ` such that `(E f :: f : {j ∈ ℕ : 1 ≤ j ≤ k} → ℕ ∧ (A i, j : 1 ≤ i < j ≤ k : f.i < f.j) ∧ S = {f.j : 1 ≤ j ≤ k}))` — strictly-increasing-function characterisation, existence-and-uniqueness of `k` carried by "the unique"; `(A n ∈ ℕ, S : S ⊆ {j ∈ ℕ : 1 ≤ j ≤ n} :: |S| ≤ n)` — upper bound.
- *Depends:*
  - NAT-carrier (NatCarrierSet) — supplies `ℕ` as the underlying set appearing in the outer membership clause `n ∈ ℕ`, in the initial-segment domain `{j ∈ ℕ : 1 ≤ j ≤ n}` whose subsets `S` ranges over, in the cardinality clause `|S| ∈ ℕ` and the inner existential over `k ∈ ℕ`, in the domain `{j ∈ ℕ : 1 ≤ j ≤ k}` and codomain ℕ of the enumerating function `f : {j ∈ ℕ : 1 ≤ j ≤ k} → ℕ`, and in the upper-bound clause `|S| ≤ n` over which `n` is the ℕ-bound.
  - NAT-order (NatStrictTotalOrder) — supplies the strict order `<` (used in the strictly-increasing condition `(A i, j : 1 ≤ i < j ≤ k : f.i < f.j)` on the enumerating function `f`) and the non-strict companion `≤` (used in the upper bound `|S| ≤ n`, in the initial-segment domain `{j ∈ ℕ : 1 ≤ j ≤ n}` bounding `S`, and in the domain `{j ∈ ℕ : 1 ≤ j ≤ k}` of `f`); the strict-total-order discipline (irreflexivity, transitivity, trichotomy `m < n ∨ m = n ∨ n < m`) makes "strictly increasing function" a well-formed predicate on ℕ-valued functions.
  - NAT-closure (NatArithmeticClosureAndIdentity) — supplies `1 ∈ ℕ`, the lower bound in the initial segment `{j ∈ ℕ : 1 ≤ j ≤ n}` and in the domain `{j ∈ ℕ : 1 ≤ j ≤ k}` of the enumerating function; combined with NAT-order's `≤` and the outer `n ∈ ℕ`, this grounds `S ⊆ {j ∈ ℕ : 1 ≤ j ≤ n}` with ℕ-typed elements. Also supplies `0 < 1`, which forces `{j ∈ ℕ : 1 ≤ j ≤ 0} = ∅` and so renders the `k = 0` and `n = 0` cases of the axiom well-formed.
  - NAT-zero (NatZeroMinimum) — supplies `0 ∈ ℕ` for the literal `0` appearing in the empty-domain case `k = 0` (where `{j ∈ ℕ : 1 ≤ j ≤ 0}` is forced empty by `0 < 1`) and in the empty-set cardinality `|∅| = 0`.

**NAT-discrete (NatDiscreteness).** For every `m, n ∈ ℕ`, `m < n ⟹ m + 1 ≤ n`.

No natural number lies strictly between `n` and its successor `n + 1`: whenever `m < n`, the successor `m + 1` is already bounded above by `n`, so `m + 1 ≤ n`. This is the discreteness of ℕ.

The axiom has a familiar no-interval reformulation `(A m, n ∈ ℕ :: m ≤ n < m + 1 ⟹ n = m)` — "nothing strictly between `m` and `m + 1`". The derivation (axiom ⟹ no-interval): assume `m ≤ n < m + 1`; unfolding `m ≤ n` by the NAT-order definition `m ≤ n ⟺ m < n ∨ m = n` splits into two cases, each of which we walk to `n = m`. In the case `m < n`, the axiom gives `m + 1 ≤ n`, which unfolds to `m + 1 < n ∨ m + 1 = n`; paired with the hypothesis `n < m + 1`, either disjunct is contradictory — `m + 1 < n` together with `n < m + 1` is excluded by NAT-order's exactly-one trichotomy (specifically its `¬(a < b ∧ b < a)` clause, instantiated at `(m + 1, n)`), while `m + 1 = n` rewrites `n < m + 1` to `n < n`, contradicting irreflexivity. The case `m < n` is therefore impossible; it contributes nothing to the conclusion and is discharged by contradiction. In the case `m = n`, symmetry of `=` gives `n = m` directly. With the `m < n` branch vacuous and the `m = n` branch yielding `n = m`, the case analysis is exhausted and the conclusion `n = m` stands. ∎

*Formal Contract:*
- *Axiom:* `(A m, n ∈ ℕ :: m < n ⟹ m + 1 ≤ n)` (discreteness).
- *Consequence:* `(A m, n ∈ ℕ :: m ≤ n < m + 1 ⟹ n = m)` (no-interval form) — derived from the axiom together with NAT-order (the `≤`-definition used to split `m ≤ n`, the exactly-one-trichotomy clause `¬(a < b ∧ b < a)` instantiated at `(m + 1, n)`, and irreflexivity `¬(n < n)` after rewriting `n < m + 1` to `n < n` via `m + 1 = n`) via the forward walk in the preceding prose.
- *Depends:*
  - NAT-carrier (NatCarrierSet) — supplies `ℕ` as the underlying set appearing in the carrier-side clause `m, n ∈ ℕ` of the bounded universal `(A m, n ∈ ℕ :: m < n ⟹ m + 1 ≤ n)` in the Axiom and likewise of the bounded universal `(A m, n ∈ ℕ :: m ≤ n < m + 1 ⟹ n = m)` in the no-interval Consequence, over which the bound variables `m, n` range before being further restricted by the term-side hypotheses.
  - NAT-order (NatStrictTotalOrder) — supplies the non-strict companion `≤` (defined by `m ≤ n ⟺ m < n ∨ m = n`) used in the axiom's consequent `m + 1 ≤ n` and in the Consequence derivation's case split on `m ≤ n`, the exactly-one-trichotomy clause `¬(a < b ∧ b < a)` instantiated at `(m + 1, n)` in the derivation, and irreflexivity `¬(n < n)` used to discharge the rewritten `n < n`.
  - NAT-closure (NatArithmeticClosureAndIdentity) — posits `1 ∈ ℕ` and closes ℕ under addition, so the successor `m + 1 ∈ ℕ` and the inequalities `m + 1 ≤ n` and `n < m + 1` are comparisons of two ℕ-elements.

**NAT-wellorder (NatWellOrdering).** ℕ is well-ordered by `<`: every nonempty subset `S ⊆ ℕ` has a least element.

Formally: for every `S ⊆ ℕ` with `S ≠ ∅`, there exists `m ∈ S` such that `m ≤ n` for every `n ∈ S`.

*Formal Contract:*
- *Axiom:* `(A S : S ⊆ ℕ ∧ S ≠ ∅ : (E m ∈ S :: (A n ∈ S :: m ≤ n)))` (least-element principle).
- *Depends:*
  - NAT-carrier (NatCarrierSet) — supplies `ℕ` as the underlying set appearing in the carrier-side clause `S ⊆ ℕ` of the axiom and as the ambient set whose elements `S` ranges over and from which the bound variables `m, n ∈ S` of the inner quantifiers `(E m ∈ S :: ...)` and `(A n ∈ S :: ...)` draw their values (since `S ⊆ ℕ`).
  - NAT-order (NatStrictTotalOrder) — supplies the non-strict companion `≤` (defined by `m ≤ n ⟺ m < n ∨ m = n`), used in the inner quantifier `(A n ∈ S :: m ≤ n)` that characterizes `m` as a least element of `S`.

**NAT-zero (NatZeroMinimum).** `0` is the minimum of ℕ: `0 ∈ ℕ` and `(A n ∈ ℕ :: 0 < n ∨ 0 = n)`.

Combined with NAT-order's irreflexivity `¬(n < n)` and transitivity `m < n ∧ n < p ⟹ m < p`, the Axiom's two clauses `0 ∈ ℕ` and `(A n ∈ ℕ :: 0 < n ∨ 0 = n)` identify `0` as the minimum: `(A n ∈ ℕ :: ¬(n < 0))`. Suppose some `n ∈ ℕ` did satisfy `n < 0`; the second clause forces `0 < n ∨ 0 = n`. In the first case, `0 < n` and `n < 0` together yield `0 < 0` by transitivity, contradicting irreflexivity. In the second case, `0 = n` rewrites `n < 0` to `0 < 0` by indiscernibility of `=`, again contradicting irreflexivity.

*Formal Contract:*
- *Axiom:* `0 ∈ ℕ` (zero is a natural number); `(A n ∈ ℕ :: 0 < n ∨ 0 = n)` (every natural number is strictly above or equal to zero).
- *Consequence:* `(A n ∈ ℕ :: ¬(n < 0))` (no natural number is strictly below zero — the minimum reading).
- *Depends:*
  - NAT-carrier (NatCarrierSet) — supplies `ℕ` as the underlying set appearing in the membership clause `0 ∈ ℕ` and over which the bounded quantifiers `(A n ∈ ℕ :: 0 < n ∨ 0 = n)` of the axiom's second clause and `(A n ∈ ℕ :: ¬(n < 0))` of the *Consequence:* range.
  - NAT-order (NatStrictTotalOrder) — supplies `<` for the axiom's second clause and the irreflexivity `¬(n < n)` + transitivity `m < n ∧ n < p ⟹ m < p` used in the body's derivation of the *Consequence:* bullet `¬(n < 0)`.


---

## 2. Carrier set and order

A tumbler is a nonempty finite sequence of natural-number components. The carrier set is unbounded in two dimensions: at any position the value may exceed any given bound, and at any depth there exist tumblers longer than any given length. The set is totally ordered lexicographically, with the prefix convention placing a proper prefix below any of its extensions. Equality is component-wise.

**T0 (CarrierSetDefinition).** `T` is the set of nonempty finite sequences over ℕ, written `d₁.d₂. ... .dₙ` with each `dᵢ ∈ ℕ`. For each `a ∈ T`, write `#a` for the length of `a`. The component positions of `a` form the index domain `{j ∈ ℕ : 1 ≤ j ≤ #a}`, and component projection is the typed operator `i ↦ aᵢ : {j ∈ ℕ : 1 ≤ j ≤ #a} → ℕ` — total and single-valued on the index domain — so `aᵢ ∈ ℕ` at each `i ∈ {j ∈ ℕ : 1 ≤ j ≤ #a}`. `(A a ∈ T :: 1 ≤ #a)` forces each tumbler to have at least one component, so the index domain is nonempty. Elements of T are *extensional*: two tumblers with equal length and identical components at every position are the same tumbler — there is no hidden structure beyond the length-and-components data. T is also *populated by every such sequence*: for every length `p ∈ ℕ` with `p ≥ 1` and every component assignment `r : {j ∈ ℕ : 1 ≤ j ≤ p} → ℕ`, there is a tumbler `t ∈ T` with `#t = p` and `tᵢ = r(i)` at each `i` — extensionality makes this `t` unique, but existence is what licenses the construction of new tumblers from a length and a component map.

*Formal Contract:*
- *Axiom:* `T` is a set (the carrier of tumblers); `#· : T → ℕ` (length operator on T); `(A a ∈ T :: 1 ≤ #a)` (nonemptiness — each tumbler has at least one component); `(A a ∈ T :: i ↦ aᵢ : {j ∈ ℕ : 1 ≤ j ≤ #a} → ℕ)` (component projection signature — for each tumbler `a ∈ T`, the projection `i ↦ aᵢ` is a total, single-valued function from the index domain `{j ∈ ℕ : 1 ≤ j ≤ #a}` into ℕ; in particular `aᵢ ∈ ℕ` at each `i` in the index domain); `(A p ∈ ℕ : p ≥ 1 : (A r : {j ∈ ℕ : 1 ≤ j ≤ p} → ℕ :: (E t ∈ T :: #t = p ∧ (A i ∈ ℕ : 1 ≤ i ≤ p : tᵢ = r(i)))))` (comprehension — every nonempty finite sequence of naturals, presented as a length `p ≥ 1` and a component map `r` from the index domain `{j ∈ ℕ : 1 ≤ j ≤ p}` into ℕ, is represented in T by some `t` with `#t = p` and `tᵢ = r(i)`); `(A a, b ∈ T : #a = #b ∧ (A i ∈ ℕ : 1 ≤ i ≤ #a : aᵢ = bᵢ) : a = b)` (extensionality — tumblers with equal length and pointwise-equal components are identical).
- *Depends:*
  - NAT-carrier (NatCarrierSet) — supplies `ℕ` as the underlying set appearing as the codomain of the length operator `#· : T → ℕ`, as the codomain of the component-projection signature `i ↦ aᵢ : {j ∈ ℕ : 1 ≤ j ≤ #a} → ℕ` and the comprehension's component map `r : {j ∈ ℕ : 1 ≤ j ≤ p} → ℕ`, in the index-domain comprehensions `{j ∈ ℕ : 1 ≤ j ≤ #a}` and `{j ∈ ℕ : 1 ≤ j ≤ p}`, over which the bounded quantifier `(A p ∈ ℕ : p ≥ 1 : ...)` of the comprehension axiom ranges, and over which the inner index variable `i` of the comprehension's `(A i ∈ ℕ : 1 ≤ i ≤ p : tᵢ = r(i))` and the extensionality axiom's `(A i ∈ ℕ : 1 ≤ i ≤ #a : aᵢ = bᵢ)` ranges before being further restricted by the term-side range.
  - NAT-closure (NatArithmeticClosureAndIdentity) — supplies `1 ∈ ℕ` for the lower bound of the nonemptiness clause `1 ≤ #a` and for the lower bound `1` in the index domain `{j ∈ ℕ : 1 ≤ j ≤ #a}` of the component-projection signature.
  - NAT-order (NatStrictTotalOrder) — supplies the non-strict relation `≤` on ℕ appearing in the nonemptiness clause `1 ≤ #a` and in the index-domain bound `1 ≤ j ≤ #a` of the component-projection signature.

**T0(a) (UnboundedComponentValues).** `(A t ∈ T, i : 1 ≤ i ≤ #t : (A M ∈ ℕ :: (E t' ∈ T :: #t' = #t ∧ t' agrees with t except t'.dᵢ > M)))`.

For every tumbler and every component position, there exists a tumbler whose value at that position exceeds any given bound.

*Proof.* Let `t = d₁.d₂. ... .dₙ` be an arbitrary member of T, let `i` satisfy `1 ≤ i ≤ n`, and let `M ∈ ℕ` be an arbitrary bound. Define

> `t' = d₁. ... .dᵢ₋₁.(M + 1).dᵢ₊₁. ... .dₙ`

— the sequence obtained from `t` by replacing its `i`-th component with `M + 1`.

*(i)* `t' ∈ T`. The sequence `t'` has length `n ≥ 1`; for `j ≠ i`, `dⱼ ∈ ℕ` by hypothesis; for `j = i`, `M + 1 ∈ ℕ` by NAT-closure's addition closure at `(M, 1)` with `1 ∈ ℕ` from the same axiom. Hence `t' ∈ T`.

*(ii)* `t'` agrees with `t` at every position `j ≠ i`, by construction.

*(iii)* `t'.dᵢ > M`. By construction `t'.dᵢ = M + 1`, and `M + 1 > M`.

*(iv)* `#t' = #t`. Replacing a component does not alter the sequence length. ∎

*Formal Contract:*
- *Postcondition:* For every tumbler `t ∈ T` and every component position `i` with `1 ≤ i ≤ #t`, and for every bound `M ∈ ℕ`, there exists `t' ∈ T` with `#t' = #t` that agrees with `t` at all positions except `i`, where `t'.dᵢ > M`.
- *Depends:*
  - T0 (CarrierSetDefinition) — carrier characterisation of T, length operator `#·`, component projection `·ᵢ`.
  - NAT-closure (NatArithmeticClosureAndIdentity) — addition closure `(A m, n ∈ ℕ :: m + n ∈ ℕ)` instantiated at `(M, 1)` with `1 ∈ ℕ` from the same axiom to place `M + 1 ∈ ℕ`.
  - NAT-addcompat (NatAdditionOrderAndSuccessor) — strict successor inequality `(A n ∈ ℕ :: n < n + 1)`.

**T0(b) (UnboundedLength).** `(A n ∈ ℕ : n ≥ 1 : (E t ∈ T :: #t ≥ n))`.

In words: there is no maximum tumbler length — for every bound, a tumbler of at least that length exists in T.

*Proof.* Let `n ∈ ℕ` with `n ≥ 1` be arbitrary. Define

> `t = 1.1. ... .1` (n components)

that is, `t = d₁.d₂. ... .dₙ` with `dᵢ = 1` for all `1 ≤ i ≤ n`.

*(i)* `t ∈ T`. The sequence `t` has length `n ≥ 1`, and each component `dᵢ = 1 ∈ ℕ` — the membership `1 ∈ ℕ` is supplied by NAT-closure, which asserts `1 ∈ ℕ` as an explicit clause. By T0, `t ∈ T`.

*(ii)* `#t ≥ n`. By construction `#t = n`. Reflexivity of equality supplies `n = n`, whence the disjunction `n < n ∨ n = n` holds by disjunction-introduction on the right disjunct; NAT-order's defining clause `m ≤ n ⟺ m < n ∨ m = n` instantiated at `m = n` then yields `n ≤ n`, and the defined converse `n ≥ n ⟺ n ≤ n` yields `n ≥ n`. Substituting `#t = n` gives `#t ≥ n`. ∎

*Formal Contract:*
- *Postcondition:* For every `n ∈ ℕ` with `n ≥ 1`, there exists `t ∈ T` with `#t ≥ n`.
- *Depends:*
  - T0 (CarrierSetDefinition) — carrier characterisation of T as finite sequences over ℕ with length ≥ 1, and the length operator `#·`.
  - NAT-closure (NatArithmeticClosureAndIdentity) — supplies `1 ∈ ℕ`, required to conclude that each witness component `dᵢ = 1` lies in ℕ.
  - NAT-order (NatStrictTotalOrder) — supplies the defining clause `m ≤ n ⟺ m < n ∨ m = n` and the converse `n ≥ n ⟺ n ≤ n`, required to lift `n = n` (reflexivity of equality) to `n ≥ n` and hence discharge `#t ≥ n`.
- *Forward References:*
  - T0(a) (UnboundedComponentValues) — named as the sibling dimension (unlimited siblings at any level) to contrast with the nesting-depth unboundedness established here

T0(b) is what separates the tumbler design from fixed-width addressing. Nelson: "New items may be continually inserted in tumbler-space while the other addresses remain valid." The word "continually" carries the weight — the process of creating new addresses never terminates. Between any two sibling addresses, the forking mechanism can always create children: "One digit can become several by a forking or branching process. This consists of creating successive new digits to the right." Each daughter can have daughters without limit.

The address space is unbounded in two dimensions: T0(a) gives unlimited siblings at any level; T0(b) gives unlimited nesting depth. Nelson calls this "finite but unlimited" — at any moment finitely many addresses exist, but there is no bound on how many can be created: "A span that contains nothing today may at a later time contain a million documents."

Gregory's implementation uses a fixed 16-digit mantissa of 32-bit unsigned integers. When `tumblerincrement` would require a 17th digit, it detects the overflow and terminates fatally; `tumbleradd` silently wraps on digit-value overflow. Both violate T0(b). The comment `NPLACES 16 /* increased from 11 to support deeper version chains */` records that the original bound of 11 was concretely hit — version chains deeper than 3–4 levels caused fatal crashes.

### Canonical form

Equality of tumblers must mean component-wise identity.

**T3 (CanonicalRepresentation).** `(A a, b ∈ T : #a = #b ∧ (A i ∈ ℕ : 1 ≤ i ≤ #a : aᵢ = bᵢ) ≡ a = b)`.

If two tumblers have the same length and the same components at every position, they are the same tumbler. Conversely, if they differ in any component or in length, they are distinct.

*Proof.* Both directions follow directly from T0. T0 characterises each `a ∈ T` as a finite sequence over ℕ together with its length `#a` and components `aᵢ`, and commits that these data fully determine the tumbler (the extensionality clause). The biconditional decomposes equality along these two directions.

*Forward direction.* Let `a, b ∈ T` and suppose `#a = #b = n` and `aᵢ = bᵢ` for all `1 ≤ i ≤ n`. T0's extensionality clause — `(A a, b ∈ T : #a = #b ∧ (A i ∈ ℕ : 1 ≤ i ≤ #a : aᵢ = bᵢ) : a = b)` — instantiated at `(a, b)` yields `a = b` directly.

*Reverse direction.* Let `a, b ∈ T` and suppose `a = b`. By Leibniz's law, `#a = #b`, and `aᵢ = bᵢ` for each `i` with `1 ≤ i ≤ #a`, since these are well-defined functions applied to equal arguments. ∎

*Formal Contract:*
- *Postcondition:* Tumbler equality is sequence equality: `a = b ⟺ #a = #b ∧ (A i ∈ ℕ : 1 ≤ i ≤ #a : aᵢ = bᵢ)`.
- *Depends:*
  - T0 (CarrierSetDefinition) — the extensionality clause `(A a, b ∈ T : #a = #b ∧ (A i ∈ ℕ : 1 ≤ i ≤ #a : aᵢ = bᵢ) : a = b)` supplies the forward direction; length `#·` and component projection `·ᵢ` supply the reverse direction via Leibniz's law.

### The total order

We require a total order on T. Nelson describes the "tumbler line" as a single linear sequence: "In a sense the tumbler line is like the real line, i.e., the line of integers and all the numbers in between." The system maps a hierarchical tree — servers containing accounts containing documents containing elements — onto this flat line via depth-first traversal, which produces a total order: for any two nodes, traversal visits one before the other. The ordering rule is lexicographic:

**T1 (LexicographicOrder).** For tumblers `a = a₁. ... .aₘ` and `b = b₁. ... .bₙ`, define `a < b` iff there exists `k` with `1 ≤ k` such that `(A i : 1 ≤ i < k : aᵢ = bᵢ)` and either:

  (i) `k ≤ m ∧ k ≤ n` and `aₖ < bₖ`, or

  (ii) `k = m + 1 ≤ n` (that is, `a` is a proper prefix of `b`).

The prefix convention — a prefix is less than any proper extension — is what makes depth-first traversal work. The server address `2` is less than every address within server `2`'s subtree, because every such address extends the prefix `2` with further components. Server `2`'s subtree begins immediately after `2` in the order and extends until some address whose first component exceeds `2`.

*Proof.* We show that `<` is a strict total order on T by establishing irreflexivity, trichotomy, and transitivity. The argument relies on `<` on ℕ (NAT-order) and on T3 (CanonicalRepresentation): tumblers with the same length and identical components at every position are equal.

*(a) Irreflexivity.* We must show: `(A a ∈ T :: ¬(a < a))`.

Suppose `a < a` for some `a ∈ T` with `#a = m`. Then there exists `k` with `1 ≤ k` and `aᵢ = aᵢ` for all `1 ≤ i < k` (vacuously satisfied) and either (i) `k ≤ m` and `aₖ < aₖ`, or (ii) `k = m + 1 ≤ m`. Case (i) violates NAT-order's irreflexivity. Case (ii) requires `m + 1 ≤ m`; NAT-addcompat gives `m < m + 1`, and NAT-order's trichotomy then excludes both `m + 1 < m` and `m + 1 = m`. Both cases produce contradictions.

*(b) Trichotomy.* We must show: `(A a, b ∈ T :: (a < b ∨ a = b ∨ b < a) ∧ ¬(a < b ∧ a = b) ∧ ¬(a < b ∧ b < a) ∧ ¬(a = b ∧ b < a))`.

Let `a, b ∈ T` with `#a = m` and `#b = n`. A *divergence position* is an index `k` with `1 ≤ k` satisfying one of the clauses (α) `k ≤ m ∧ k ≤ n ∧ aₖ ≠ bₖ`, (β) `k = m + 1 ∧ k ≤ n`, or (γ) `k = n + 1 ∧ k ≤ m`. The proof splits first on whether any divergence position exists; when at least one does, NAT-wellorder applied to the nonempty set of such positions delivers a least element — the *first divergence position* `k` — after which a sub-split on which clause `k` satisfies completes the analysis. The three branches below are exhaustive.

*Case 1: no divergence position exists.* Then `aᵢ = bᵢ` for all `i` with `1 ≤ i ≤ m ∧ i ≤ n` (no index satisfies clause (α)), and the two exhaustion-shape divergences are absent too: `¬(m + 1 ≤ n)` and `¬(n + 1 ≤ m)` (no index satisfies (β) or (γ)). NAT-discrete's forward direction `m < n ⟹ m + 1 ≤ n` contraposes with the first to yield `¬(m < n)`; symmetrically, `¬(n < m)`. NAT-order's trichotomy at `(m, n)` then forces `m = n`. The shared-position equalities now range over all `1 ≤ i ≤ m`, so `a = b` by T3. Part (a) gives `¬(a < a)` and `¬(a > a)`.

*Case 2: the first divergence position `k` satisfies clause (α)* — `k ≤ m ∧ k ≤ n ∧ aₖ ≠ bₖ`. Minimality of `k` gives `aᵢ = bᵢ` for all `i < k`, but `aₖ ≠ bₖ`, so `a ≠ b` by T3. By NAT-order's trichotomy, exactly one of `aₖ < bₖ` or `bₖ < aₖ` holds. If `aₖ < bₖ`, then `k` witnesses `a < b` via T1(i); if `bₖ < aₖ`, then `k` witnesses `b < a` via T1(i). No reverse witness `k'` exists. If `k < k'`, agreement fails at position `k`. If `k' = k`, case (i) requires the opposite inequality at `k`, excluded by NAT-order's trichotomy, and case (ii) requires `k = n + 1` (resp. `m + 1`), contradicting `k ≤ n` (resp. `k ≤ m`). If `k' < k`, minimality of `k` gives `a_{k'} = b_{k'}`, so case (i) is excluded by NAT-order's trichotomy at `(a_{k'}, b_{k'})`, and case (ii) requires `k' = n + 1 ≤ m`, contradicting `k' < k ≤ n`.

*Case 3: the first divergence position `k` satisfies clause (β) or (γ).* Minimality of `k` rules out any shared-position mismatch: under clause (β), `k = m + 1`, so any shared-position index `j` (one with `j ≤ m ∧ j ≤ n`) satisfies `j ≤ m < k` via NAT-addcompat's `m < m + 1`; under clause (γ), `k = n + 1`, so symmetrically any shared-position `j` satisfies `j ≤ n < k`. In either case, an (α)-mismatch at such `j` would witness a divergence position strictly below `k`, contradicting minimality. So `aᵢ = bᵢ` for all `i` with `1 ≤ i ≤ m ∧ i ≤ n`. Both clauses force `m ≠ n`: under (β), `m + 1 ≤ n`, and the `≤`-clause expands this into `m + 1 < n ∨ m + 1 = n` — the first branch combines with NAT-addcompat's `m < m + 1` by NAT-order's transitivity to yield `m < n`, and the second substitutes `m + 1 = n` into `m < m + 1` to yield `m < n`; either way `m < n`. Symmetrically, (γ) yields `n < m` from `n + 1 ≤ m` and NAT-addcompat's `n < n + 1`. So `a ≠ b` by T3. NAT-order's trichotomy at `(m, n)` resolves `m ≠ n` into `m < n ∨ n < m`. If `m < n`, then clause (γ) is impossible: (γ) would give `n + 1 ≤ m`, and the `≤`-clause expands this into `n + 1 < m ∨ n + 1 = m` — the first branch combines with NAT-addcompat's `n < n + 1` by NAT-order's transitivity to yield `n < m`, and the second substitutes `n + 1 = m` into `n < n + 1` to yield `n < m`; either way `n < m`, and NAT-order's trichotomy at `(m, n)` excludes `m < n ∧ n < m`. So `k` satisfies (β), giving `k = m + 1 ≤ n`; `a` is a proper prefix of `b` and `k` witnesses `a < b` via T1(ii). No reverse witness for `b < a` exists: case (i) would require `bⱼ < aⱼ` at some shared position `j`, excluded by NAT-order's trichotomy at `(aⱼ, bⱼ)` given `aⱼ = bⱼ`; case (ii) would require `n + 1 ≤ m`; the `≤`-clause expands this into `n + 1 < m ∨ n + 1 = m` — the first branch combines with NAT-addcompat's `n < n + 1` by NAT-order's transitivity to yield `n < m`, and the second substitutes `n + 1 = m` into `n < n + 1` to yield `n < m`; either way `n < m`, contradicting `m < n`. If `n < m`, then clause (β) is impossible: (β) would give `m + 1 ≤ n`, and the `≤`-clause expands this into `m + 1 < n ∨ m + 1 = n` — the first branch combines with NAT-addcompat's `m < m + 1` by NAT-order's transitivity to yield `m < n`, and the second substitutes `m + 1 = n` into `m < m + 1` to yield `m < n`; either way `m < n`, and NAT-order's trichotomy at `(m, n)` excludes `m < n ∧ n < m`. So `k` satisfies (γ), giving `k = n + 1 ≤ m`; `b` is a proper prefix of `a` and `k` witnesses `b < a` via T1(ii). No reverse witness for `a < b` exists: case (i) would require `aⱼ < bⱼ` at some shared position `j`, excluded by NAT-order's trichotomy at `(aⱼ, bⱼ)` given `aⱼ = bⱼ`; case (ii) would require `m + 1 ≤ n`; the `≤`-clause expands this into `m + 1 < n ∨ m + 1 = n` — the first branch combines with NAT-addcompat's `m < m + 1` by NAT-order's transitivity to yield `m < n`, and the second substitutes `m + 1 = n` into `m < m + 1` to yield `m < n`; either way `m < n`, contradicting `n < m`.

These three cases partition `T × T`, and in each case exactly one of the three relations holds.

*(c) Transitivity.* We must show: `(A a, b, c ∈ T : a < b ∧ b < c : a < c)`.

Let `k₁` witness `a < b` and `k₂` witness `b < c`, with `#a = m`, `#b = n`, `#c = p`. For all `i < k₁ ∧ i < k₂`, `aᵢ = bᵢ = cᵢ` by transitivity of equality. Case analysis on `k₁` and `k₂`.

*Case k₁ < k₂.* We first establish `k₁ ≤ p`, which puts `k₁` in `c`'s component-projection domain and licenses access to `cₖ₁`. The witness `k₂` for `b < c` satisfies `k₂ ≤ p` in every case: T1(i) supplies `k₂ ≤ p` directly from its `k₂ ≤ #b ∧ k₂ ≤ #c` clause, and T1(ii) supplies `k₂ = #b + 1 ≤ p` from its `k₂ = #b + 1 ≤ #c` clause. The `≤`-clause expands `k₂ ≤ p` into `k₂ < p ∨ k₂ = p` — the first branch combines with `k₁ < k₂` by NAT-order's transitivity to yield `k₁ < p`, and the second substitutes `k₂ = p` into `k₁ < k₂` to yield `k₁ < p`; either way `k₁ < p`, hence `k₁ ≤ p` via the `≤`-clause. With `cₖ₁` now well-defined and `k₁` strictly below `k₂` (the witness for `b < c`), the agreement condition for `b < c` applies at position `k₁` and gives `bₖ₁ = cₖ₁`. If `a < b` via T1(i): `aₖ₁ < bₖ₁ = cₖ₁` with `k₁ ≤ m` (from this clause) and `k₁ ≤ p` (just derived); position `k₁` witnesses `a < c` via T1(i). If `a < b` via T1(ii): `k₁ = m + 1 ≤ n`, and substituting `k₁` for `m + 1` in the previously-derived `k₁ ≤ p` yields `m + 1 ≤ p`; `k₁` witnesses `a < c` via T1(ii).

*Case k₂ < k₁.* Position `k₂` lies in the agreement range of `a < b`, so `aₖ₂ = bₖ₂`. If `b < c` were via T1(ii), then `k₂ = n + 1`. But `a < b` requires `k₁ ≤ n` (directly in case (i), via `k₁ = m + 1 ≤ n` in case (ii)), and NAT-addcompat gives `n < n + 1`; since `k₂ = n + 1`, this rewrites to `n < k₂`. The `≤`-clause expands `k₁ ≤ n` into `k₁ < n ∨ k₁ = n`: the first branch combines with `n < k₂` by NAT-order's transitivity to yield `k₁ < k₂`, and the second substitutes `k₁` for `n` in `n < k₂` to yield `k₁ < k₂`. Either way, `k₁ < k₂` together with `k₂ < k₁` violates NAT-order's trichotomy. Therefore `b < c` is via T1(i): `bₖ₂ < cₖ₂` with `k₂ ≤ n ∧ k₂ ≤ p`. Witnessing `a < c` via T1(i) at position `k₂` requires `k₂ ≤ m`, and the argument splits on how `a < b` is witnessed. If via T1(i), then `k₁ ≤ m`, and the `≤`-clause expands into `k₁ < m ∨ k₁ = m`: the first branch combines with `k₂ < k₁` by NAT-order's transitivity to yield `k₂ < m`, and the second substitutes `m` for `k₁` in `k₂ < k₁` to yield `k₂ < m`; either way `k₂ ≤ m` via the `≤`-clause. If via T1(ii), then `k₁ = m + 1`, so `k₂ < m + 1`; NAT-order's trichotomy at `(m + 1, k₂)` excludes both `m + 1 < k₂` and `m + 1 = k₂`, yielding `¬(m + 1 ≤ k₂)`, and NAT-discrete's forward direction `m < k₂ ⟹ m + 1 ≤ k₂` contraposes to `¬(m < k₂)`; NAT-order's trichotomy at `(m, k₂)` then leaves `k₂ < m ∨ k₂ = m`, i.e., `k₂ ≤ m` via the `≤`-clause. In either sub-case, `k₂ ≤ m`, so `aₖ₂ = bₖ₂ < cₖ₂`, and `k₂` witnesses `a < c` via T1(i).

*Case k₁ = k₂ = k.* We have `aᵢ = cᵢ` for all `i < k`.

*Sub-case (i, i):* `aₖ < bₖ < cₖ` with `k ≤ m ∧ k ≤ p`. NAT-order transitivity gives `aₖ < cₖ`; T1(i) witnesses `a < c`.

*Sub-case (ii, i):* `k = m + 1 ≤ n` and `k ≤ p`, so `m + 1 ≤ p`; T1(ii) witnesses `a < c`.

*Sub-case (i, ii):* `k ≤ n` together with `k = n + 1` (from `k = n + 1 ≤ p`) gives `n + 1 ≤ n`; NAT-addcompat gives `n < n + 1`, and NAT-order's trichotomy excludes both `n + 1 < n` and `n + 1 = n`; contradiction.

*Sub-case (ii, ii):* `k = m + 1 ≤ n` and `k = n + 1 ≤ p`. Then `m + 1 = n + 1`, so `m = n` by NAT-cancel. The `≤`-clause expands `m + 1 ≤ n` into `m + 1 < n ∨ m + 1 = n` — the first branch combines with NAT-addcompat's `m < m + 1` by NAT-order's transitivity to yield `m < n`, and the second substitutes `m + 1 = n` into `m < m + 1` to yield `m < n`; either way `m < n`, contradicting `m = n` by NAT-order's trichotomy.

In every realizable combination, a witness for `a < c` under T1 is produced. ∎

The strict total order `<` admits the customary non-strict companions and the reverse strict companion: `a ≤ b` abbreviates `a < b ∨ a = b`, `a ≥ b` abbreviates `b ≤ a`, and `a > b` abbreviates `b < a` (parallel to NAT-order's treatment of `>` on ℕ).

*Formal Contract:*
- *Definition:* `a < b` iff `∃ k ∈ ℕ` with `1 ≤ k` and `(A i ∈ ℕ : 1 ≤ i < k : aᵢ = bᵢ)` and either (i) `k ≤ #a ∧ k ≤ #b ∧ aₖ < bₖ`, or (ii) `k = #a+1 ≤ #b`.
- *Abbreviations:* `a ≤ b` abbreviates `a < b ∨ a = b`; `a ≥ b` abbreviates `b ≤ a`; `a > b` abbreviates `b < a`.
- *Depends:*
  - T0 (CarrierSetDefinition) — length `#a` and component projection `aₖ` for `a ∈ T`.
  - T3 (CanonicalRepresentation, this ASN) — bridge between component-level agreement and tumbler equality; Case 1 concludes `a = b`, Cases 2 and 3 conclude `a ≠ b`.
  - NAT-carrier (NatCarrierSet) — supplies `ℕ` as the underlying set over which the bound variable `k` of the existential quantifier `∃ k ∈ ℕ` and the bound variable `i` of the universal quantifier `(A i ∈ ℕ : 1 ≤ i < k : aᵢ = bᵢ)` in the *Definition* range.
  - NAT-order (NatStrictTotalOrder) — irreflexivity, trichotomy, and transitivity of `<` on ℕ; `≤`-defining clause `m ≤ n ⟺ m < n ∨ m = n` for composing strict with non-strict bounds.
  - NAT-closure (NatArithmeticClosureAndIdentity) — supplies `1 ∈ ℕ` and the signature `+ : ℕ × ℕ → ℕ`.
  - NAT-addcompat (NatAdditionOrderAndSuccessor) — strict successor inequality `n < n + 1`.
  - NAT-cancel (NatAdditionCancellation) — right cancellation at `1`, used in sub-case (ii, ii) to pass from `m + 1 = n + 1` to `m = n`.
  - NAT-discrete (NatDiscreteness) — forward direction `m < n ⟹ m + 1 ≤ n`, used contrapositively in Case 1 to rule out `m < n` and `n < m` from the exhaustion-shape negations `¬(m + 1 ≤ n) ∧ ¬(n + 1 ≤ m)` and in part (c) Case `k₂ < k₁` case-(ii) branch to obtain `k₂ ≤ m` from `k₂ < m + 1`.
  - NAT-wellorder (NatWellOrdering) — least-element principle, invoked in part (b) within the branch where at least one divergence position exists, to define the first divergence position `k`.
- *Postconditions:* (a) Irreflexivity — `(A a ∈ T :: ¬(a < a))`. (b) Trichotomy — `(A a,b ∈ T :: (a < b ∨ a = b ∨ b < a) ∧ ¬(a < b ∧ a = b) ∧ ¬(a < b ∧ b < a) ∧ ¬(a = b ∧ b < a))`. (c) Transitivity — `(A a,b,c ∈ T : a < b ∧ b < c : a < c)`.

**T2 (IntrinsicComparison).** The order relation T1 is computable from the two tumblers alone, without consulting any external data structure. The number of component pairs the comparison examines is bounded by both `#a` and `#b` — at most `#a` pairs and at most `#b` pairs.

*Proof.* Let `a = a₁. ... .aₘ` and `b = b₁. ... .bₙ`. The definition of `<` in T1 asks for a witness position `k ≥ 1` with agreement at all positions before `k`, and either a component divergence at `k` or prefix exhaustion at `k`. The comparison scans positions `i = 1, 2, ...` and compares the pair `(aᵢ, bᵢ)` at each. Two outcomes are possible.

*Case 1: divergence at some position `k` with `k ≤ m ∧ k ≤ n`.* The scan finds `aₖ ≠ bₖ` after verifying `aᵢ = bᵢ` for all `1 ≤ i < k`. Then `k` is the least element of `{i ∈ ℕ : 1 ≤ i ∧ i ≤ m ∧ i ≤ n ∧ aᵢ ≠ bᵢ}`, well-defined by NAT-wellorder. By minimality, the examined positions are precisely `{1, 2, ..., k}`, so exactly `k` component pairs are examined; `k ≤ m = #a` and `k ≤ n = #b` by the case hypothesis. NAT-order's trichotomy at `(aₖ, bₖ)` resolves `aₖ ≠ bₖ` into `aₖ < bₖ ∨ bₖ < aₖ`. By T1 case (i), `aₖ < bₖ` yields `a < b` and `bₖ < aₖ` yields `b < a`.

*Case 2: no divergence within the shared range.* The scan exhausts every position `i` with `1 ≤ i ∧ i ≤ m ∧ i ≤ n`. NAT-order's trichotomy at `(m, n)` partitions the outcome.

*Sub-case `m < n`.* By NAT-order transitivity `i ≤ m ∧ m < n ⟹ i ≤ n`, the shared range equals `{i : 1 ≤ i ≤ m}`, so exactly `m` pairs are examined; `m ≤ m` and `m ≤ n`. T1 case (ii) requires a witness `k = m + 1 ≤ n`; NAT-discrete's forward direction `m < n ⟹ m + 1 ≤ n` bridges the case hypothesis to that arithmetic witness. Taking `k = m + 1`, we identify the scan's agreement domain `{i : 1 ≤ i ≤ m}` with T1 case (ii)'s witness domain `{i : 1 ≤ i < k}`: the forward inclusion `i ≤ m ⟹ i < m + 1` uses NAT-addcompat's strict successor inequality `m < m + 1` composed with NAT-order transitivity, and the reverse `i < m + 1 ⟹ i ≤ m` uses NAT-discrete's no-interval Consequence. T1 case (ii) then gives `a < b`.

*Sub-case `n < m`.* By the mirrored transitivity, the shared range equals `{i : 1 ≤ i ≤ n}`, so exactly `n` pairs are examined; `n ≤ n` and `n ≤ m`. NAT-discrete's forward direction `n < m ⟹ n + 1 ≤ m`, applied with roles swapped, supplies the witness `k = n + 1 ≤ m` demanded by T1 case (ii); the domain identification `{i : 1 ≤ i ≤ n} = {i : 1 ≤ i < n + 1}` is furnished symmetrically by NAT-addcompat's `n < n + 1` with NAT-order transitivity for the forward inclusion and NAT-discrete's no-interval Consequence for the reverse. T1 case (ii) with roles swapped gives `b < a`.

*Sub-case `m = n`.* The shared range covers every position of either tumbler, so exactly `m` pairs are examined; `m ≤ m` and `m ≤ n` by substitution. Componentwise agreement with `m = n` gives `a = b` by T3.

In every case, the count of pairs examined is at most `#a` and at most `#b`. Every value consulted — the components `aᵢ`, `bᵢ`, and the lengths `m`, `n` — belongs to the two tumblers themselves; no tree, index, or external state participates. ∎

Span containment tests, link search, and index traversal all reduce to tumbler comparison. If comparison required a lookup, these operations would depend on auxiliary state and the decentralization guarantee would collapse.

Gregory's `tumblercmp` delegates to `abscmp`, which performs a purely positional comparison: exponent first, then lexicographic mantissa slot-by-slot. No external state is consulted.

*Formal Contract:*
- *Preconditions:* `a, b ∈ T` — two well-formed tumblers (finite sequences over ℕ with `#a ≥ 1` and `#b ≥ 1`, per T0).
- *Depends:*
  - T0 (CarrierSetDefinition) — length operator `#·` and component-projection `·ᵢ`.
  - T1 (LexicographicOrder) — the order relation being shown computable; case (i) and case (ii) dispatch the two scan outcomes.
  - T3 (CanonicalRepresentation) — bridges componentwise agreement with `m = n` to `a = b` in the equality sub-case.
  - NAT-wellorder (NatWellOrdering) — least-element principle establishing that `k` is the first divergence position in Case 1.
  - NAT-order (NatStrictTotalOrder) — trichotomy at `(aₖ, bₖ)` and at `(m, n)`; transitivity in the mixed form `i ≤ p ∧ p < q ⟹ i ≤ q` for shared-range identification in Case 2.
  - NAT-discrete (NatDiscreteness) — forward direction `m < n ⟹ m + 1 ≤ n`, used in Case 2 sub-cases `m < n` and `n < m` to bridge the case hypothesis to the arithmetic witness `k = m + 1 ≤ n` (resp. `k = n + 1 ≤ m`) required by T1 case (ii); its no-interval Consequence also supplies the reverse inclusion `i < m + 1 ⟹ i ≤ m` (resp. `i < n + 1 ⟹ i ≤ n`) of the agreement-domain identification in those same sub-cases.
  - NAT-addcompat (NatAdditionOrderAndSuccessor) — strict successor inequality `m < m + 1` (and symmetrically `n < n + 1`), used in Case 2 sub-cases `m < n` and `n < m` to identify the scan's agreement domain `{i : 1 ≤ i ≤ m}` (resp. `{i : 1 ≤ i ≤ n}`) with the `{i : 1 ≤ i < k}` domain required by T1 case (ii) at `k = m + 1` (resp. `k = n + 1`); it supplies the forward inclusion `i ≤ m ⟹ i < m + 1` (resp. `i ≤ n ⟹ i < n + 1`) via NAT-order transitivity, which NAT-discrete's forward/no-interval directions cannot produce without circularity.
- *Postconditions:* (a) The ordering among `a` and `b` under T1 is determined. (b) The number of component pairs examined is at most `#a` and at most `#b`. (c) The only values consulted are `{aᵢ : 1 ≤ i ≤ #a}`, `{bᵢ : 1 ≤ i ≤ #b}`, `#a`, and `#b`.
- *Frame:* No external data structure is read or modified — the comparison is a pure function of the two tumblers.


---

## 3. Hierarchical structure

A tumbler is parsed into nested *partitions* by treating each component position as a hierarchical level. The prefix relation `≼` captures containment: `p ≼ a` when `p` is an initial segment of `a`. Sub-properties decompose hierarchical parsing into its constituent disciplines.

### Hierarchical structure

Tumblers encode a containment hierarchy. Nelson uses zero-valued components as structural delimiters:

> "There are four major fields, each expandable indefinitely, with three major dividers between them. These fields are Server, User, Document and Contents."

> "A tumbler address may have at most three zero digits... These are interpreted as the major dividers, and have lexical significance as punctuation."

We formalize this, writing *node* for Nelson's *server* and *element* for his *contents* and retaining *user* and *document* verbatim; the renaming is notational. An address tumbler has up to four fields separated by zero-valued components; which fields are present in a given tumbler is determined by its zero count. As an illustration of the structure that T4-validity admits, the maximal written form — the case with all four fields present, `zeros(t) = 3` — is:

`t = N₁. ... .Nₐ . 0 . U₁. ... .Uᵦ . 0 . D₁. ... .Dᵧ . 0 . E₁. ... .Eδ`

where `0 < Nᵢ, 0 < Uⱼ, 0 < Dₖ, 0 < Eₗ` at every position. The four fields — each of which may be absent at lower zero counts — are:

- **Node field** `N₁. ... .Nₐ`: identifies the server. "The server address always begins with the digit 1, since all other servers are descended from it."
- **User field** `U₁. ... .Uᵦ`: identifies the account. "Typically, the user will have no control over the node address he, she or it is assigned; but once assigned a User account, the user will have full control over its subdivision forevermore."
- **Document field** `D₁. ... .Dᵧ`: identifies the document and version. Nelson notes the boundary between base document and version is not syntactically marked — "the version, or subdocument number is only an accidental extension of the document number, and strictly implies no specific relationship of derivation."
- **Element field** `E₁. ... .Eδ`: identifies the content element. T4 constrains only `0 < Eₗ` at every element-field position; typed interpretations of `E₁` are the concern of downstream ASNs.

The count of zero-valued components determines the specificity level; T4c is the single definitional site for the resulting address-kind labels.

**T4 (HierarchicalParsing).** Define `zeros(t) = |{i : 1 ≤ i ≤ #t ∧ tᵢ = 0}|`, with `|·|` NAT-card's set-cardinality operator (distinct from T0's tumbler-length `#·`, which acts on sequences); the argument `{i : 1 ≤ i ≤ #t ∧ tᵢ = 0}` is a subset of the index domain `{1, …, #t} ⊆ ℕ` (T0), so NAT-card applies at `n = #t` and `zeros(t) ∈ ℕ` with `zeros(t) ≤ #t`. We say a position `i` of `t` is a *field separator* iff `tᵢ = 0`, and a *field component* otherwise; the two roles are decidable by inspecting `tᵢ`. The non-adjacency clause names two component accesses, `tᵢ` and `tᵢ₊₁`, both of which T0's component-projection signature requires to be indexed in `{j ∈ ℕ : 1 ≤ j ≤ #t}`. For `i` in the quantifier's range `1 ≤ i < #t`, `tᵢ` is licensed directly by the range; the neighbour `tᵢ₊₁` requires `1 ≤ i + 1 ≤ #t`, and we discharge each bound separately. The upper bound `i + 1 ≤ #t` is NAT-discrete at `(m, n) := (i, #t)` applied to the range hypothesis `i < #t`. The lower bound `1 ≤ i + 1` is NAT-closure's successor-positivity axiom `(A n ∈ ℕ :: 0 < n + 1)`, instantiated at `n := i`, which yields `0 < i + 1`; NAT-discrete at `(m, n) := (0, i + 1)` then promotes this to `0 + 1 ≤ i + 1`, and NAT-closure's left additive identity `(A n ∈ ℕ :: 0 + n = n)` at `n := 1` rewrites the left-hand side to `1`, leaving `1 ≤ i + 1`. Both bounds in hand, `i + 1 ∈ {j ∈ ℕ : 1 ≤ j ≤ #t}`, so T0's projection signature gives `tᵢ₊₁ ∈ ℕ` and the access is well-defined throughout the quantifier's range — including the `i ≥ 1` indices for which NAT-zero alone would leave `0 = i + 1` unrefuted. Call `t ∈ T` *T4-valid* iff the four conditions `zeros(t) ≤ 3`, `(A i : 1 ≤ i < #t : ¬(tᵢ = 0 ∧ tᵢ₊₁ = 0))`, `t₁ ≠ 0`, `t_{#t} ≠ 0` all hold; we name the last three conjuncts collectively the *field-segment constraint*. The *field segments* of `t` are the maximal contiguous sub-sequences of field-component positions, delimited by the field separators; the equivalence between every-segment-non-empty and the field-segment constraint is proved downstream in T4a rather than stipulated here.

*Exhaustion.* We derive as a Consequence — universally quantified by the bound alone — that `(A t ∈ T : zeros(t) ≤ 3 : zeros(t) ∈ {0, 1, 2, 3})`, i.e. for every `t ∈ T` with `zeros(t) ≤ 3`, `zeros(t) ∈ {0, 1, 2, 3}`. NAT-order's trichotomy at `(zeros(t), 0)` asserts that exactly one of `zeros(t) < 0`, `zeros(t) = 0`, `0 < zeros(t)` holds; NAT-zero supplies `0 < zeros(t) ∨ 0 = zeros(t)`, two of those three alternatives, so by trichotomy's exactly-one clause `zeros(t) < 0` is forbidden. Either `zeros(t) = 0`, whereupon `zeros(t) ∈ {0, 1, 2, 3}`, or `0 < zeros(t)`, which NAT-discrete at `(m, n) := (0, zeros(t))` promotes to `0 + 1 ≤ zeros(t)`, which NAT-closure's left additive identity `(A n ∈ ℕ :: 0 + n = n)` at `n := 1` reduces to `1 ≤ zeros(t)`. At `m = 1` (continuing the `0 < zeros(t)` branch): trichotomy at `(zeros(t), 1)` excludes `zeros(t) < 1` because `1 ≤ zeros(t)` unfolds via NAT-order's `≤` to `1 < zeros(t) ∨ 1 = zeros(t)`, two of trichotomy's three alternatives, forcing the third out by exactly-one; so either `zeros(t) = 1`, whereupon `zeros(t) ∈ {0, 1, 2, 3}`, or `1 < zeros(t)`, which NAT-discrete at `(m, n) := (1, zeros(t))` promotes to `1 + 1 ≤ zeros(t)`, which the *Numerals* definition `2 := 1 + 1` rewrites to `2 ≤ zeros(t)`. At `m = 2` (continuing the `1 < zeros(t)` branch): trichotomy excludes `zeros(t) < 2` by the same route from `2 ≤ zeros(t)`, so either `zeros(t) = 2`, whereupon `zeros(t) ∈ {0, 1, 2, 3}`, or `2 < zeros(t)`, which NAT-discrete at `(m, n) := (2, zeros(t))` promotes to `2 + 1 ≤ zeros(t)`, which the *Numerals* definition `3 := 2 + 1` rewrites to `3 ≤ zeros(t)`. At the final step, trichotomy at `(zeros(t), 3)` is confronted with two bounds: `3 ≤ zeros(t)` excludes `zeros(t) < 3` (unfolding `3 ≤ zeros(t)` to `3 < zeros(t) ∨ 3 = zeros(t)` makes one of the other two trichotomy alternatives hold, forcing `zeros(t) < 3` out by exactly-one), and symmetrically `zeros(t) ≤ 3` excludes `3 < zeros(t)` (unfolding to `zeros(t) < 3 ∨ zeros(t) = 3` makes one of the other two alternatives hold, forcing `3 < zeros(t)` out by exactly-one), leaving `zeros(t) = 3`. Every branch terminates with `zeros(t) ∈ {0, 1, 2, 3}`.

*Formal Contract:*
- *Definition:*
  - *Zero-count.* `zeros(t) = |{i : 1 ≤ i ≤ #t ∧ tᵢ = 0}|`; the index set `{i : 1 ≤ i ≤ #t ∧ tᵢ = 0}` is a subset of `{1, …, #t} ⊆ ℕ` (T0's index domain), so NAT-card applies at `n = #t` and yields `zeros(t) ∈ ℕ`.
  - *Field separator.* A position `i` of `t` is a *field separator* iff `tᵢ = 0`; the remaining positions are *field components*.
  - *Field segment.* The *field segments* of `t` are the maximal contiguous sub-sequences of field-component positions, delimited by the field separators. The terminology names what a segment *is*; the equivalence between every-segment-non-empty and the field-segment constraint is proved in T4a, not stipulated here.
  - *Numerals.* `2 := 1 + 1` and `3 := 2 + 1`; closure of ℕ under addition (NAT-closure), applied successively to `1 ∈ ℕ`, gives `2 ∈ ℕ` and then `3 ∈ ℕ`.
  - *T4-valid predicate.* `t ∈ T` is *T4-valid* iff `zeros(t) ≤ 3 ∧ (A i : 1 ≤ i < #t : ¬(tᵢ = 0 ∧ tᵢ₊₁ = 0)) ∧ t₁ ≠ 0 ∧ t_{#t} ≠ 0`; the last three conjuncts are collectively the *field-segment constraint*.
- *Consequence:* `(A t ∈ T : zeros(t) ≤ 3 : zeros(t) ∈ {0, 1, 2, 3})` — for every `t ∈ T` with `zeros(t) ≤ 3`, `zeros(t) ∈ {0, 1, 2, 3}` (equivalently `zeros(t) = 0 ∨ zeros(t) = 1 ∨ zeros(t) = 2 ∨ zeros(t) = 3`). Derived in the *Exhaustion* paragraph above.
- *Preconditions:* `t ∈ T`.
- *Depends:*
  - T0 (CarrierSetDefinition) — supplies the tumbler carrier T (so the precondition `t ∈ T` and the body's component accesses `tᵢ`, `tᵢ₊₁` are meaningful), the tumbler length `#·`, the component-projection signature, and the index domain `{1, …, #t}`.
  - NAT-zero (NatZeroMinimum) — supplies `0 ∈ ℕ` for the literal `0` appearing in the zero-count definition's filter `tᵢ = 0` (within `zeros(t) = |{i : 1 ≤ i ≤ #t ∧ tᵢ = 0}|`), in the T4-valid predicate's clauses `tᵢ = 0`, `tᵢ₊₁ = 0`, `t₁ ≠ 0`, and `t_{#t} ≠ 0`, and in the Consequence's enumeration `zeros(t) ∈ {0, 1, 2, 3}`; also supplies the disjunction `(A n ∈ ℕ :: 0 < n ∨ 0 = n)`, instantiated at `n := zeros(t)` in the *Exhaustion* paragraph and combined with NAT-order's exactly-one trichotomy to forbid `zeros(t) < 0`.
  - NAT-discrete (NatDiscreteness) — supplies the strict-to-`+1` promotion `m < n ⟹ m + 1 ≤ n`, instantiated at `(i, #t)` for the upper bound `i + 1 ≤ #t` of the `tᵢ₊₁` well-definedness, at `(0, i + 1)` for the conversion `0 < i + 1 ⟹ 0 + 1 ≤ i + 1` in that same derivation, and at `(0, zeros(t))`, `(1, zeros(t))`, `(2, zeros(t))` in the *Exhaustion* induction.
  - NAT-order (NatStrictTotalOrder) — supplies `<` on ℕ with its companion `≤` (`m ≤ n ⟺ m < n ∨ m = n`) and the exactly-one trichotomy Consequence.
  - NAT-closure (NatArithmeticClosureAndIdentity) — supplies `1 ∈ ℕ`, closure of ℕ under addition (grounding the numerals `2 := 1 + 1` and `3 := 2 + 1`), the left additive identity `(A n ∈ ℕ :: 0 + n = n)`, and the successor-positivity axiom `(A n ∈ ℕ :: 0 < n + 1)` consumed at `n := i` to discharge the lower bound `1 ≤ i + 1` of the `tᵢ₊₁` well-definedness derivation.
  - NAT-card (NatFiniteSetCardinality) — axiomatizes `|·|` on subsets of every initial segment `{1, …, n} ⊆ ℕ` with codomain ℕ.
- *Forward References:*
  - T4a (SyntacticEquivalence) — proves downstream the equivalence between the field-segment constraint and every-segment-non-empty; T4 defers to it rather than stipulating the biconditional here.
  - T4c (LevelDetermination) — the single definitional site for the address-kind labels (node/user/document/element) that T4's zero-count levels admit.

**T4a (SyntacticEquivalence).** T4's field-segment constraint — stated positionally as (i) no two zeros are adjacent, (ii) `t₁ ≠ 0`, (iii) `t_{#t} ≠ 0` — is equivalent to the condition that every *field segment* of `t` is non-empty, where the field segments are the `zeros(t) + 1` maximal contiguous sub-sequences of non-zero positions delimited by the zeros.

Let `t ∈ T` be a tumbler with `zeros(t) ≤ 3`. Set `k = zeros(t)`; the Forward and Reverse derivations below proceed by the two-case split `k = 0` versus `k ≥ 1`, exhaustive over `k ∈ ℕ` and so over the T4-valid subdomain a fortiori — the upper bound `k ≤ 3` is carried as a precondition (T4-validity) but is not consumed by the case analysis. Enumerate the zeros of `t` at positions `s₁ < s₂ < … < s_k` (strict increase by NAT-order; the length `k` of this enumeration equals `zeros(t)` by NAT-card's enumeration characterisation of `|·|` applied at the zero-index subset `{i : 1 ≤ i ≤ #t ∧ tᵢ = 0} ⊆ {1, …, #t}`, whose cardinality T4 identifies with `zeros(t)`). Set `s₀ = 0` and `s_{k+1} = #t + 1` as sentinels — the sentinel value `0` and the literal `0` appearing in the `k = 0` case branches of Forward Conditions (ii) and (iii) and the Reverse first-segment derivation are the ℕ-element supplied by NAT-zero's first Axiom clause `0 ∈ ℕ`. The arithmetic in what follows — the numerals `2` and `3`, the sums `s_i + 1`, `s_i + 2`, and `#t + 1`, and the last-segment upper bound `s_{k+1} − 1` — is grounded thus: NAT-closure posits `1 ∈ ℕ` and closes ℕ under addition, so `2 := 1 + 1 ∈ ℕ`, `3 := 2 + 1 ∈ ℕ`, and each of `s_i + 1`, `s_i + 2`, `#t + 1` lies in ℕ. NAT-sub's right-telescoping clause `(m + n) − n = m`, instantiated at `m = #t, n = 1`, reduces `s_{k+1} − 1 = (#t + 1) − 1` to `#t` in ℕ, so the last segment occupies the ℕ-interval `[s_k + 1, #t]`. T0's Axiom includes the nonemptiness clause `(A a ∈ T :: 1 ≤ #a)`; instantiating its universally quantified `a` at `t` (licensed by `t ∈ T`) yields `#t ≥ 1` directly as a first-class axiom citation, and this bound underwrites the `k = 0` branches of Forward Conditions (ii) and (iii), where the single segment equals `t` itself. The `k + 1` field segments of `t` are the index ranges `(s_i, s_{i+1})` for `i = 0, 1, …, k` — i.e. the component sub-sequences `t[s_i + 1 .. s_{i+1} - 1]`. A segment is non-empty precisely when `s_{i+1} ≥ s_i + 2`; for the last segment, whose index range is `[s_k + 1, #t]` as shown above, this specialises to the native `+1` form `#t ≥ s_k + 1` — equivalently `s_k + 1 ≤ #t` — which is what the Reverse Last-segment argument lands on directly via NAT-discrete.

*Forward.* Assume every field segment is non-empty. We derive each positional condition.

*Condition (ii): `t₁ ≠ 0`.* The first field segment is `t[1 .. s₁ - 1]` when `k ≥ 1`, or `t[1 .. #t]` when `k = 0`; in either case its first index is 1. Segment non-emptiness gives `s₁ ≥ 2` (when `k ≥ 1`) or `#t ≥ 1` (when `k = 0`), so index 1 lies in the segment and `t₁` is a non-zero component. Hence `t₁ ≠ 0`.

*Condition (iii): `t_{#t} ≠ 0`.* The last field segment is `t[s_k + 1 .. #t]` when `k ≥ 1`, or `t[1 .. #t]` when `k = 0`; in either case its last index is `#t`. Segment non-emptiness, in the last-segment `+1` specialisation stated above, gives `s_k + 1 ≤ #t` (when `k ≥ 1`) or `#t ≥ 1` (when `k = 0`), so index `#t` lies in the segment and `t_{#t}` is a non-zero component. Hence `t_{#t} ≠ 0`.

*Condition (i): no adjacent zeros.* Suppose for contradiction that `tᵢ = 0 ∧ tᵢ₊₁ = 0` for some `i` with `1 ≤ i < #t`. Then `i` and `i + 1` are both zero positions, so `i = s_j` and `i + 1 = s_{j'}` for some enumeration indices `j < j'` (strict monotonicity from `i < i + 1`, where the strict successor inequality `i < i + 1` is NAT-addcompat's third axiom clause `(A n ∈ ℕ :: n < n + 1)` instantiated at `n := i`); since `i + 1 ≤ #t` places the second zero inside the enumerated range `{s_1, …, s_k}`, we have `j' ≤ k`, hence `j + 1 ≤ j' ≤ k` — so `s_{j+1}` is a real enumeration entry (not the sentinel `s_{k+1} = #t + 1`). We claim `s_{j+1} = i + 1`: if instead `j + 1 < j'`, strict monotonicity would give `s_j < s_{j+1} < s_{j'}`, i.e., `i < s_{j+1} < i + 1`, and NAT-discrete's no-interval Consequence `m ≤ n < m + 1 ⟹ n = m`, instantiated at `(m, n) := (i, s_{j+1})`, would force `s_{j+1} = i`, contradicting `s_j < s_{j+1}`. Hence `s_{j+1} = i + 1`, and the interior field segment `t[s_j + 1 .. s_{j+1} - 1] = t[i + 1 .. i]` has no indices, so it is empty. This contradicts segment non-emptiness. Hence no two zeros are adjacent.

*Reverse.* Assume conditions (i), (ii), and (iii) hold. We show every field segment is non-empty.

*First segment (`i = 0`).* The segment occupies indices 1 through `s₁ - 1` (or 1 through `#t` when `k = 0`). If `k = 0` the segment equals `t` itself, which has `#t ≥ 1` indices. If `k ≥ 1`, condition (ii) forces `t₁ ≠ 0`, so index 1 is not a zero position, and therefore `s₁ ≥ 2` — the segment has at least one index.

*Last segment (`i = k`).* The segment occupies indices `s_k + 1` through `#t` (when `k ≥ 1`); non-emptiness of this index range is the `+1` inequality `s_k + 1 ≤ #t`. Condition (iii) forces `t_{#t} ≠ 0`, so index `#t` is not among the zero positions `s₁ < … < s_k`, giving `s_k ≠ #t`. Every zero position `s_j` is an index of `t`, hence `s_k ≤ #t`; unfolding this by NAT-order's definition `s_k ≤ #t ⟺ s_k < #t ∨ s_k = #t` and excluding the `s_k = #t` branch by `s_k ≠ #t` leaves `s_k < #t`. NAT-discrete's axiom `m < n ⟹ m + 1 ≤ n`, instantiated at `(m, n) := (s_k, #t)`, promotes this strict inequality directly to its native `+1` output `s_k + 1 ≤ #t` — the segment has at least one index.

*Interior segments (`1 ≤ i < k`).* Each such segment occupies indices `s_i + 1` through `s_{i+1} - 1`. Strict monotonicity of the enumeration gives `s_i < s_{i+1}`, so NAT-discrete's strict-to-`+1` promotion `m < n ⟹ m + 1 ≤ n`, instantiated at `(m, n) := (s_i, s_{i+1})`, delivers `s_i + 1 ≤ s_{i+1}`. Before invoking condition (i) at `j := s_i` we discharge its range hypothesis `1 ≤ s_i < #t`. The lower bound `1 ≤ s_i` is direct: `s_i` is an entry of the enumeration `{s_1, …, s_k} ⊆ {1, …, #t}` of zero positions, so `1 ≤ s_i ≤ #t`. For the upper bound `s_i < #t`, the same enumeration containment gives `s_{i+1} ≤ #t`; combining with `s_i + 1 ≤ s_{i+1}` already in hand, NAT-order's `≤`-transitivity Consequence, instantiated at `(m, n, p) := (s_i + 1, s_{i+1}, #t)`, yields `s_i + 1 ≤ #t`. Unfolding by NAT-order's `≤`-definition splits this into `s_i + 1 < #t ∨ s_i + 1 = #t`, and NAT-addcompat's strict successor inequality `s_i < s_i + 1` chains with each disjunct — by NAT-order's `<`-transitivity at `(m, n, p) := (s_i, s_i + 1, #t)` in the strict branch, by indiscernibility of `=` substituting `s_i + 1 = #t` into `s_i < s_i + 1` in the equality branch — to deliver `s_i < #t`. With `1 ≤ s_i < #t` in hand, condition (i) at `j := s_i` forbids `s_{i+1} = s_i + 1`; unfolding `≤` by NAT-order's definition `s_i + 1 ≤ s_{i+1} ⟺ s_i + 1 < s_{i+1} ∨ s_i + 1 = s_{i+1}` and excluding the equality branch leaves `s_i + 1 < s_{i+1}`. NAT-discrete's strict-to-`+1` promotion, re-instantiated at `(m, n) := (s_i + 1, s_{i+1})`, then yields `(s_i + 1) + 1 ≤ s_{i+1}`. NAT-addassoc at `(m, n, p) := (s_i, 1, 1)` rewrites `(s_i + 1) + 1 = s_i + (1 + 1) = s_i + 2` (with `2 := 1 + 1` from NAT-closure), so `s_{i+1} ≥ s_i + 2` — the segment has at least one index.

All segments — first, interior, and last — are non-empty. ∎

*Formal Contract:*
- *Consequence:* The three positional conditions (i) `(A i : 1 ≤ i < #t : ¬(tᵢ = 0 ∧ tᵢ₊₁ = 0))`, (ii) `t₁ ≠ 0`, (iii) `t_{#t} ≠ 0` hold if and only if every field segment of `t` is non-empty (SyntacticEquivalence) — derived from T4's field-segment clauses, T0's non-degeneracy of `t ∈ T`, NAT-order's strict total order (specifically `<`-transitivity), `≤`-definition, and `≤`-transitivity Consequence, NAT-discrete's strict-to-`+1` promotion and no-interval Consequence, NAT-addcompat's strict successor inequality `n < n + 1`, NAT-addassoc's regrouping `(m + n) + p = m + (n + p)`, NAT-zero's first Axiom clause `0 ∈ ℕ`, NAT-closure's numerals and closure under addition, NAT-sub's right-telescoping clause, and NAT-card's enumeration characterisation of `|·|`, as shown in the preceding Forward and Reverse derivations; recorded as a Consequence rather than an Axiom because the biconditional is proved from T4's axioms and the foundation dependencies, not posited.
- *Preconditions:* `t ∈ T` with `zeros(t) ≤ 3`.
- *Depends:*
  - T0 (CarrierSetDefinition) — fixes the carrier as ℕ and supplies the Axiom's nonemptiness clause `(A a ∈ T :: 1 ≤ #a)`.
  - NAT-discrete (NatDiscreteness) — supplies the strict-to-`+1` promotion `m < n ⟹ m + 1 ≤ n` and the no-interval Consequence `m ≤ n < m + 1 ⟹ n = m`.
  - NAT-addcompat (NatAdditionOrderAndSuccessor) — supplies the strict successor inequality `(A n ∈ ℕ :: n < n + 1)`.
  - NAT-addassoc (NatAdditionAssociative) — supplies `(A m, n, p ∈ ℕ :: (m + n) + p = m + (n + p))`, instantiated at `(m, n, p) := (s_i, 1, 1)` in the Reverse interior-segment derivation to rewrite the NAT-discrete output `(s_i + 1) + 1` as `s_i + (1 + 1) = s_i + 2` (with `2 := 1 + 1` from NAT-closure), discharging the equational step that would otherwise conflate the two parenthesisations.
  - NAT-order (NatStrictTotalOrder) — supplies `<` on ℕ with its companion `≤` (`m ≤ n ⟺ m < n ∨ m = n`), the `<`-transitivity Axiom clause `(A m, n, p ∈ ℕ : m < n ∧ n < p : m < p)` consumed in the Reverse interior-segment derivation at `(m, n, p) := (s_i, s_i + 1, #t)` to chain `s_i < s_i + 1 < #t` into `s_i < #t`, and the `≤`-transitivity Consequence `(A m, n, p ∈ ℕ : m ≤ n ∧ n ≤ p : m ≤ p)` consumed in the same derivation at `(m, n, p) := (s_i + 1, s_{i+1}, #t)` to chain `s_i + 1 ≤ s_{i+1} ≤ #t` into `s_i + 1 ≤ #t`.
  - NAT-zero (NatZeroMinimum) — supplies the first Axiom clause `0 ∈ ℕ`, which grounds the sentinel value `s₀ = 0` and the literal `0` appearing in the `k = 0` case branches of Forward Conditions (ii) and (iii) and the Reverse first-segment derivation.
  - NAT-closure (NatArithmeticClosureAndIdentity) — supplies `1 ∈ ℕ` and closure of ℕ under addition (grounding the numerals `2 := 1 + 1`, `3 := 2 + 1` and the sums `s_i + 1`, `s_i + 2`, `#t + 1`).
  - NAT-sub (NatPartialSubtraction) — supplies the right-telescoping clause `(m + n) − n = m`.
  - NAT-card (NatFiniteSetCardinality) — supplies the enumeration characterisation of `|·|`.
  - T4 (HierarchicalParsing) — supplies the positional conditions (i)–(iii), the field-segment terminology, and the zero-count bound `zeros(t) ≤ 3` (carried as a precondition; the proof's two-case split `k = 0` versus `k ≥ 1` is exhaustive over `ℕ` without consuming the upper bound).

**T4b (UniqueParse).** Under the constraints of T4 — at most three zero-valued components, no two zeros adjacent, `t₁ ≠ 0`, `t_{#t} ≠ 0` — the four partial functions

  `N, U, D, E : T ⇀ T`

that extract the node, user, document, and element sub-sequences of `t` are well-defined and uniquely determined by `t`. Each projection's image lies in the subset of `T` whose every component is in `ℕ⁺`: a nonempty finite sequence over `ℕ` (by T0) with every component strictly positive by NAT-zero (the disjunction `0 < n ∨ 0 = n` at `n := tᵢ`, with the equality branch excluded by the non-separator distinction `tᵢ ≠ 0`). The four projections share the T4-valid subset of `T` as the outer domain from which absence is carved; field *absence* is encoded by partiality of the projection, and is fixed by `zeros(t)`:

  - `N` is defined on the whole T4-valid subdomain (`N` is never absent).
  - `U` is defined iff `t` is T4-valid and `zeros(t) ≥ 1`.
  - `D` is defined iff `t` is T4-valid and `zeros(t) ≥ 2`.
  - `E` is defined iff `t` is T4-valid and `zeros(t) = 3`.

A field `X` is *absent in `t`* iff `t ∉ dom(X)`. By T4's Exhaustion Consequence, every T4-valid `t` satisfies `zeros(t) ∈ {0, 1, 2, 3}`, so ranging `k` over `{0, 1, 2, 3}` below collectively covers every `t` in the T4-valid subdomain. For each `k ∈ ℕ` with `0 ≤ k ≤ 3` at which `zeros(t) = k`, the presence is fixed as follows:

  - `zeros(t) = 0`: only `N(t)` defined, with `N(t) = (t₁, ..., t_{#t})`.
  - `zeros(t) = 1`: `N(t)` and `U(t)` defined.
  - `zeros(t) = 2`: `N(t)`, `U(t)`, `D(t)` defined.
  - `zeros(t) = 3`: all four projections defined.

To access individual components of a field we introduce the notation `t.X₁`, grounded in T0's projection as follows. Whenever `X(t)` is defined, `X(t)` is a nonempty finite sequence over `ℕ⁺ ⊆ ℕ`, so `X(t) ∈ T` with `#(X(t)) ≥ 1` by T0, and T0's component projection `·ᵢ` is defined at every `i ∈ {1, …, #(X(t))}` — in particular at `i = 1`. We set `t.X₁ := (X(t))₁`, so the dot-accessor is notational shorthand for T0's subscript applied to `X(t)`, and `t.X₁` is defined iff `X(t)` is defined: `t.N₁` on every T4-valid `t`; `t.U₁` iff `zeros(t) ≥ 1`; `t.D₁` iff `zeros(t) ≥ 2`; `t.E₁` iff `zeros(t) = 3`.

*Derivation.* By T4's stipulation, the separator positions of `t` are exactly `{i : 1 ≤ i ≤ #t ∧ tᵢ = 0}`, and every non-separator position carries a field component — strictly positive by NAT-zero on T0's carrier ℕ: NAT-zero's disjunction `(A n ∈ ℕ :: 0 < n ∨ 0 = n)` instantiated at `n := tᵢ` (licensed by `tᵢ ∈ ℕ` from T0) yields `0 < tᵢ ∨ 0 = tᵢ`, and the equality branch is excluded by the non-separator distinction `tᵢ ≠ 0`, leaving `0 < tᵢ`, i.e. `tᵢ ∈ ℕ⁺ = {n ∈ ℕ : 0 < n}`.

Let the zero positions in increasing order be `s₁ < s₂ < ... < s_k`, with `k = zeros(t)` bounded by `0 ≤ k ≤ 3` (T4 supplies `zeros(t) ≤ 3`; NAT-zero supplies `0 ≤ zeros(t)`) and the strictly increasing enumeration licensed by NAT-order; NAT-card's enumeration characterisation of `|·|`, applied to the zero-index subset `{i : 1 ≤ i ≤ #t ∧ tᵢ = 0} ⊆ {1, …, #t}` whose cardinality is `zeros(t)` by T4's definition, identifies the enumeration length `k` with `zeros(t)`. Since `t` is T4-valid, the field-segment constraint (i)–(iii) holds, and T4a's reverse direction yields its exported conclusion: every field segment of `t` is non-empty. We unpack this conclusion locally into the three position-inequalities used in the case analysis below. The arithmetic in what follows — the numeral `2`, sums `s_i + 1` and `s_i + 2`, and the partial subtraction `s_i − 1` — is grounded thus: NAT-closure posits `1 ∈ ℕ` and closes ℕ under addition, so `2 := 1 + 1 ∈ ℕ`, and each `s_i + 1`, `s_i + 2` lies in ℕ; NAT-sub's conditional-closure clause applied at `s_i ≥ 1` (T0's index domain) and `1 ∈ ℕ` gives `s_i − 1 ∈ ℕ`. T0's Axiom includes the nonemptiness clause `(A a ∈ T :: 1 ≤ #a)`; instantiating its universally quantified `a` at `t` (licensed by `t ∈ T`) yields `#t ≥ 1` directly as a first-class axiom citation, and this bound underwrites the `k = 0` branch below where the sole segment equals `t` itself. T4 identifies the field segments as the `k + 1` maximal contiguous non-zero runs delimited by the zero positions and the sequence boundaries. The first segment occupies the indices `1, …, s₁ - 1` (when `k ≥ 1`), so its non-emptiness requires `s₁ ≥ 2`; the last segment occupies the indices `s_k + 1, …, #t` (when `k ≥ 1`), so its non-emptiness requires `s_k + 1 ≤ #t` — the native `+1` form T4a's Reverse Last-segment argument outputs directly via NAT-discrete, consumed here without a subtractive conversion; each interior segment between consecutive zeros (`1 ≤ j < k`) occupies the indices `s_j + 1, …, s_{j+1} - 1`, so its non-emptiness requires `s_{j+1} ≥ s_j + 2`. These three inequalities are the local re-expression of T4a's segment non-emptiness conclusion, and each matches the native form T4a's Reverse direction delivers (no subtractive rewriting is performed; in particular the last-segment inequality is kept in its `+1` form rather than rewritten as `s_k ≤ #t − 1`, which would require NAT-sub's strict-monotonicity Consequence at `p = 1` plus right-telescoping and a split on the `≤`-unfolding). For each `k ∈ ℕ` with `0 ≤ k ≤ 3` at which `zeros(t) = k`, compute the projections, citing the relevant inequality for each segment; T4's Exhaustion Consequence, instantiated at the T4-valid `t`, makes the four-case presentation that follows exhaustive over the T4-valid subdomain, so the four cases collectively cover `dom(N)`:

  - *Case k = 0.* `N(t) = (t₁, ..., t_{#t})`; `U, D, E` undefined at `t`. The sole segment spans indices 1 through `#t`, non-empty because `#t ≥ 1` — T0's Axiom clause `(A a ∈ T :: 1 ≤ #a)` instantiated at `a := t`.
  - *Case k = 1.* `N(t) = (t₁, ..., t_{s₁ - 1})`, `U(t) = (t_{s₁ + 1}, ..., t_{#t})`; `D, E` undefined at `t`. `s₁ ≥ 2` makes `N(t)` non-empty; `s₁ + 1 ≤ #t` makes `U(t)` non-empty.
  - *Case k = 2.* `N(t) = (t₁, ..., t_{s₁ - 1})`, `U(t) = (t_{s₁ + 1}, ..., t_{s₂ - 1})`, `D(t) = (t_{s₂ + 1}, ..., t_{#t})`; `E` undefined at `t`. `s₁ ≥ 2` makes `N(t)` non-empty; `s₂ ≥ s₁ + 2` makes `U(t)` non-empty; `s₂ + 1 ≤ #t` makes `D(t)` non-empty.
  - *Case k = 3.* `N(t) = (t₁, ..., t_{s₁ - 1})`, `U(t) = (t_{s₁ + 1}, ..., t_{s₂ - 1})`, `D(t) = (t_{s₂ + 1}, ..., t_{s₃ - 1})`, `E(t) = (t_{s₃ + 1}, ..., t_{#t})`. `s₁ ≥ 2` makes `N(t)` non-empty; `s₂ ≥ s₁ + 2` makes `U(t)` non-empty; `s₃ ≥ s₂ + 2` makes `D(t)` non-empty; `s₃ + 1 ≤ #t` makes `E(t)` non-empty.

In each present case the components listed lie in `ℕ⁺ ⊆ ℕ` (by the NAT-zero argument above, with `ℕ⁺ = {n ∈ ℕ : 0 < n}`), and the segment length is at least 1 (the per-segment non-emptiness inequalities above unpacking T4a's Reverse direction). The extracted sub-sequence is therefore presented as a length `p ≥ 1` together with a component map into ℕ, and T0's comprehension clause `(A p ∈ ℕ : p ≥ 1 : (A r : {j ∈ ℕ : 1 ≤ j ≤ p} → ℕ :: (E t ∈ T :: #t = p ∧ (A i ∈ ℕ : 1 ≤ i ≤ p : tᵢ = r(i)))))`, instantiated at this length and map, places it in `T`; every component being strictly positive places it in the all-positive subset of `T` claimed as the image. By T0, each `tᵢ` is the value of the `i`-th component of `t` — a function of `t` and `i` — so the set `{i : 1 ≤ i ≤ #t ∧ tᵢ = 0}` of separator positions is determined by `t`, and with it the field boundaries and the sub-sequences extracted above. Two distinct decompositions would require two distinct separator sets; there is exactly one. Therefore each projection is well-defined and unique on its stated domain. ∎

*Formal Contract:*
- *Definition:* The four partial functions `N, U, D, E : T ⇀ T` are characterised as follows. `dom(N)` is the T4-valid subset of `T`; `dom(U) = {t ∈ dom(N) : zeros(t) ≥ 1}`; `dom(D) = {t ∈ dom(N) : zeros(t) ≥ 2}`; `dom(E) = {t ∈ dom(N) : zeros(t) = 3}`. Let `s₁ < s₂ < ... < s_k` enumerate the zero positions of `t`, with `k = zeros(t)` bounded by `0 ≤ k ≤ 3` (T4 supplies `zeros(t) ≤ 3`; NAT-zero supplies `0 ≤ zeros(t)`). T4's Exhaustion Consequence gives `zeros(t) ∈ {0, 1, 2, 3}` at the T4-valid `t` here, so the four cases `k ∈ {0, 1, 2, 3}` collectively cover `dom(N)`; the values are fixed per-`k` — for each `k ∈ ℕ` with `0 ≤ k ≤ 3` at which `zeros(t) = k`: for `k = 0`, `N(t) = (t₁, ..., t_{#t})`; for `k = 1`, `N(t) = (t₁, ..., t_{s₁ - 1})` and `U(t) = (t_{s₁ + 1}, ..., t_{#t})`; for `k = 2`, `N(t) = (t₁, ..., t_{s₁ - 1})`, `U(t) = (t_{s₁ + 1}, ..., t_{s₂ - 1})`, `D(t) = (t_{s₂ + 1}, ..., t_{#t})`; for `k = 3`, `N(t) = (t₁, ..., t_{s₁ - 1})`, `U(t) = (t_{s₁ + 1}, ..., t_{s₂ - 1})`, `D(t) = (t_{s₂ + 1}, ..., t_{s₃ - 1})`, `E(t) = (t_{s₃ + 1}, ..., t_{#t})`. Outside the stated domains, the respective projections are not assigned values.
- *Depends:*
  - T0 (CarrierSetDefinition) — supplies ℕ as the carrier, `T` as the set of nonempty finite sequences over ℕ, the Axiom's nonemptiness clause `(A a ∈ T :: 1 ≤ #a)`, the index domain `{1, …, #t}`, the component projection `tᵢ`, and the Axiom's comprehension clause `(A p ∈ ℕ : p ≥ 1 : (A r : {j ∈ ℕ : 1 ≤ j ≤ p} → ℕ :: (E t ∈ T :: #t = p ∧ (A i ∈ ℕ : 1 ≤ i ≤ p : tᵢ = r(i)))))` — licensing T-membership of each extracted sub-sequence: nonempty (by T4a) with components in ℕ (by the component projection), so the comprehension clause places it in `T`.
  - NAT-zero (NatZeroMinimum) — supplies `(A n ∈ ℕ :: 0 < n ∨ 0 = n)`.
  - NAT-order (NatStrictTotalOrder) — supplies `<` on ℕ with its companion `≤`.
  - NAT-closure (NatArithmeticClosureAndIdentity) — supplies `1 ∈ ℕ` and closure of ℕ under addition (grounding the numeral `2 := 1 + 1` and the sums `s_i + 1`, `s_i + 2`).
  - NAT-sub (NatPartialSubtraction) — supplies the conditional-closure clause `s_i ≥ 1, 1 ∈ ℕ ⟹ s_i − 1 ∈ ℕ`.
  - NAT-card (NatFiniteSetCardinality) — supplies the enumeration characterisation of `|·|`.
  - T4 (HierarchicalParsing) — supplies `zeros(t) ≤ 3`, the field-segment clauses, the separator role of zero-valued positions, the field-segment identification, and the Exhaustion Consequence.
  - T4a (SyntacticEquivalence) — supplies, via its Reverse direction, the conclusion that every field segment of `t` is non-empty.
  - NAT-discrete (NatDiscreteness) — supplies `m < n ⟹ m + 1 ≤ n`, licensing the last-segment non-emptiness inequality `s_k + 1 ≤ #t` in its native `+1` form (from T4a's Reverse direction) without subtractive conversion.
- *Postconditions:* `N, U, D, E : T ⇀ T` are partial functions. `dom(N)` is the T4-valid subset of `T`; `dom(U) ⊆ dom(N)` picks out `zeros(t) ≥ 1`; `dom(D) ⊆ dom(N)` picks out `zeros(t) ≥ 2`; `dom(E) ⊆ dom(N)` picks out `zeros(t) = 3`. On its domain each projection is well-defined, uniquely determined by `t`, and returns a nonempty finite sequence over `ℕ⁺` — an element of `T` whose every component is strictly positive. Field *absence* is encoded by partiality: `X` is *absent in `t`* iff `t ∉ dom(X)`. Presence pattern, exhausted over `dom(N)` by T4's Exhaustion Consequence instantiated at every T4-valid `t` — for each `k ∈ ℕ` with `0 ≤ k ≤ 3` at which `zeros(t) = k`: `k = 0` → only `N` defined; `k = 1` → `N, U` defined; `k = 2` → `N, U, D` defined; `k = 3` → all four defined. The four cases collectively cover every T4-valid `t`. The component-access notation `t.X₁ := (X(t))₁` — T0's component projection at index 1 applied to `X(t)`, which belongs to `T` whenever `X` is defined at `t` because `ℕ⁺ ⊆ ℕ` — is defined iff `X` is defined at `t`: `t.N₁` always on the T4-valid subset; `t.U₁` iff `zeros(t) ≥ 1`; `t.D₁` iff `zeros(t) ≥ 2`; `t.E₁` iff `zeros(t) = 3`. Outside the T4-valid subdomain, none of the projections is assigned a value; consumers must carry T4-validity as a precondition.

**T4c (LevelDetermination).** Let `zeros(t) = |{i : 1 ≤ i ≤ #t ∧ tᵢ = 0}|` as in T4, where `|·|` is the cardinality operator on subsets of initial segments of ℕ axiomatized by NAT-card (codomain ℕ, distinct from T0's tumbler-length `#·` which acts on sequences); the indexed set is a subset of `{1, …, #t} ⊆ ℕ` by T0, so NAT-card applies at `n = #t` and `zeros(t) ∈ ℕ`. On the T4-valid subset of `T` (tumblers satisfying `zeros(t) ≤ 3`, no two zeros adjacent, `t₁ ≠ 0`, `t_{#t} ≠ 0`), T4c defines four hierarchical level labels by zero count: `t` is a *node address* iff `zeros(t) = 0`, a *user address* iff `zeros(t) = 1`, a *document address* iff `zeros(t) = 2`, and an *element address* iff `zeros(t) = 3`.

The four biconditionals are the definition of the labels. The proof obligation reduces to: the four zero-count values exhaust the T4-valid subdomain, and distinct values receive distinct labels.

*Exhaustion.* By T4's Exhaustion Consequence, every T4-valid tumbler satisfies `zeros(t) ∈ {0, 1, 2, 3}`.

*Injectivity.* The values `0, 1, 2, 3` are pairwise distinct in ℕ — `0 ∈ ℕ` by NAT-zero's first Axiom clause, `1 ∈ ℕ` by NAT-closure, and `2 := 1 + 1, 3 := 2 + 1 ∈ ℕ` by NAT-closure's closure of ℕ under addition (the same `0 ∈ ℕ` from NAT-zero grounds the literal `0` appearing in the label-defining biconditional `zeros(t) = 0 ↔ t is a node address`, where `zeros(t) ∈ ℕ` is compared against the ℕ-element `0`). The base link `0 < 1` is the distinctness *Consequence* of NAT-closure, cited directly. NAT-addcompat's strict successor inequality `n < n + 1`, instantiated at `n ∈ {1, 2}` — both instantiations licensed by `1 ∈ ℕ` from NAT-closure and `2 := 1 + 1 ∈ ℕ` by closure under addition — supplies the remaining links `1 < 2` and `2 < 3`; NAT-order transitivity chains these together with `0 < 1` to `0 < 1 < 2 < 3`, so `m < n` holds for every pair with `m` preceding `n` in the chain; NAT-order's exactly-one trichotomy Consequence contains the conjunct `¬(m < n ∧ m = n)`, equivalently `m < n ⟹ m ≠ n`, which yields `m ≠ n` for each such pair directly from `m < n`. Since `zeros(t)` is single-valued, distinct zero counts induce distinct labels. ∎

*Formal Contract:*
- *Preconditions:* `t` satisfies the T4 constraints (`zeros(t) ≤ 3`, no two zeros adjacent, `t₁ ≠ 0`, `t_{#t} ≠ 0`).
- *Definition:* `(A t ∈ T : t is T4-valid :: (zeros(t) = 0 ↔ t is a node address) ∧ (zeros(t) = 1 ↔ t is a user address) ∧ (zeros(t) = 2 ↔ t is a document address) ∧ (zeros(t) = 3 ↔ t is an element address))`.
- *Depends:*
  - T0 (CarrierSetDefinition) — supplies the index domain `{1, …, #t} ⊆ ℕ` that contains the zero-index subset, so NAT-card applies at `n = #t`.
  - NAT-zero (NatZeroMinimum) — supplies the first Axiom clause `0 ∈ ℕ`, which grounds the literal `0` in the label-defining biconditional `zeros(t) = 0 ↔ t is a node address`, where `zeros(t) ∈ ℕ` is compared against the ℕ-element `0`.
  - NAT-card (NatFiniteSetCardinality) — axiomatizes `|·|` on subsets of every initial segment `{1, …, n} ⊆ ℕ` with codomain ℕ, grounding the type `zeros(t) ∈ ℕ` for `zeros(t) = |{i : 1 ≤ i ≤ #t ∧ tᵢ = 0}|`.
  - NAT-order (NatStrictTotalOrder) — supplies transitivity to chain `0 < 1 < 2 < 3` and the exactly-one trichotomy Consequence's conjunct `¬(m < n ∧ m = n)` — equivalently `m < n ⟹ m ≠ n` — to exclude equality within that chain directly from the strict inequalities, so that `0, 1, 2, 3` are pairwise distinct for injectivity.
  - NAT-closure (NatArithmeticClosureAndIdentity) — posits `1 ∈ ℕ` and closes ℕ under addition, grounding the numerals `2 := 1 + 1 ∈ ℕ` and `3 := 2 + 1 ∈ ℕ` used in injectivity's chain `0 < 1 < 2 < 3`; additionally supplies the distinctness *Consequence* `0 < 1` — derived in NAT-closure's prose from successor-positivity at `n := 0` and left-identity at `n := 1` — cited directly in injectivity as the base link of the chain.
  - NAT-addcompat (NatAdditionOrderAndSuccessor) — supplies the strict successor inequality `n < n + 1`, instantiated at `n ∈ {1, 2}` to obtain the links `1 < 2` and `2 < 3` in injectivity's chain.
  - T4 (HierarchicalParsing) — supplies the T4-valid subdomain constraints (`zeros(t) ≤ 3`, no two zeros adjacent, `t₁ ≠ 0`, `t_{#t} ≠ 0`) that delimit T4c's subdomain, and the Exhaustion Consequence `zeros(t) ∈ {0, 1, 2, 3}` cited directly for the exhaustion step.
- *Postconditions:* The label assignment supplied by the *Definition* slot is well-defined on the T4-valid subdomain — every T4-valid tumbler receives exactly one of the four labels. This factors into two clauses, each established by the proof above. *Exhaustion:* `(A t ∈ T : t is T4-valid :: zeros(t) ∈ {0, 1, 2, 3})`, established by the Exhaustion paragraph above. *Pairwise extensional disjointness:* the four label predicates `t is a node address`, `t is a user address`, `t is a document address`, `t is an element address` have pairwise disjoint extensions on the T4-valid subdomain, established by the Injectivity paragraph above.

**Prefix (PrefixRelation).** The prefix relation on tumblers: `p ≼ q` iff `#p ≤ #q ∧ (∀i : 1 ≤ i ≤ #p : qᵢ = pᵢ)`. A proper prefix `p ≺ q` requires `p ≼ q` with `p ≠ q`. We write `p ⋠ q` for the negation `¬(p ≼ q)` — read "p is not a prefix of q".

*Formal Contract:*
- *Definition:* `p ≼ q` iff `#p ≤ #q ∧ (∀i : 1 ≤ i ≤ #p : qᵢ = pᵢ)`. Proper prefix: `p ≺ q` iff `p ≼ q ∧ p ≠ q`. Non-prefix: `p ⋠ q` iff `¬(p ≼ q)`.
- *Depends:*
  - T0 (CarrierSetDefinition) — length `#p` and component projection `pᵢ` for `p ∈ T`.
  - NAT-order (NatStrictTotalOrder) — `≤` on ℕ for length comparison and index range; defining clause `m ≤ n ⟺ m < n ∨ m = n`.
  - T3 (CanonicalRepresentation) — equal-length tumblers agreeing on all components are equal.
- *Derived postcondition (proper-prefix length):* `p ≺ q ⟹ #p < #q`. From `p ≼ q` conclude `#p ≤ #q`. If `#p = #q`, the component condition `(∀i : 1 ≤ i ≤ #p : qᵢ = pᵢ)` covers all positions of both tumblers, so by T3 `p = q`, contradicting `p ≠ q`. Hence `#p ≠ #q`, and by NAT-order's `≤`-unfolding `#p < #q`.
- *Derived postcondition (reflexivity):* `(∀t ∈ T :: t ≼ t)`. Instantiate the Definition at `p = q = t`: `#t ≤ #t` by NAT-order's `≤`-clause at the equality disjunct; `tᵢ = tᵢ` for `1 ≤ i ≤ #t` by reflexivity of equality. Both conjuncts hold, so `t ≼ t`.


---

## 4. Subtree properties

The set of tumblers under a fixed prefix forms a contiguous interval under the lexicographic order: prefix-rooted subtrees are exactly the contiguous spans on the tumbler line. Containment is decidable from the two tumblers alone. Non-nesting prefixes have disjoint subtrees.

### Contiguous subtrees

**T5 (ContiguousSubtrees).** For any tumbler prefix `p`, the set `{t ∈ T : p ≼ t}` forms a contiguous interval under T1:

  `[p ≼ a ∧ p ≼ c ∧ a ≤ b ≤ c ⟹ p ≼ b]`

*Proof.* Let `p` be a tumbler prefix with `#p ≥ 1`, let `a, b, c ∈ T` with `p ≼ a`, `p ≼ c`, and `a ≤ b ≤ c` under T1. We must show `p ≼ b`.

Since `p ≼ a`, by Prefix, `#a ≥ #p` and `aᵢ = pᵢ` for all `1 ≤ i ≤ #p`. Likewise, from `p ≼ c`, Prefix gives `#c ≥ #p` and `cᵢ = pᵢ` for all `1 ≤ i ≤ #p`. We proceed by case analysis on the length of `b`.

*Case 1: `#b ≥ #p`.* We show `bᵢ = pᵢ` for all `1 ≤ i ≤ #p`, which is `p ≼ b`.

Suppose, for contradiction, that `b` diverges from `p` at some position. The set of indices in `{1, ..., #p}` at which `bₖ ≠ pₖ` is nonempty; NAT-wellorder's least-element principle delivers its minimum `k`, giving `bᵢ = pᵢ` for all `1 ≤ i < k` together with `bₖ ≠ pₖ`. NAT-order's trichotomy at `(bₖ, pₖ)` then resolves `bₖ ≠ pₖ` into exactly one of `bₖ < pₖ` or `bₖ > pₖ`.

*Subcase 1a: `bₖ < pₖ`.* Since `p ≼ a`, `aₖ = pₖ`, so `bₖ < aₖ`. For all `i < k`, `bᵢ = pᵢ = aᵢ`. Position `k` is the first divergence between `a` and `b`, with `bₖ < aₖ`, and `k ≤ #p ≤ min(#a, #b)`. By T1 case (i), `b < a`. Now `a ≤ b` abbreviates `a < b ∨ a = b`: the disjunct `a < b` together with `b < a` violates T1 postcondition (b) trichotomy's clause `¬(a < b ∧ b < a)`; the disjunct `a = b` substitutes into `b < a` to yield `a < a`, violating T1 postcondition (a) irreflexivity. Either disjunct produces a contradiction.

*Subcase 1b: `bₖ > pₖ`.* Since `p ≼ c`, `cₖ = pₖ`, so `bₖ > cₖ`. For all `i < k`, `bᵢ = pᵢ = cᵢ`, and `k ≤ #p ≤ min(#b, #c)`. By T1 case (i), `c < b`. Now `b ≤ c` abbreviates `b < c ∨ b = c`: the disjunct `b < c` together with `c < b` violates T1 postcondition (b) trichotomy's clause `¬(a < b ∧ b < a)` instantiated at `(b, c)`; the disjunct `b = c` substitutes into `c < b` to yield `b < b`, violating T1 postcondition (a) irreflexivity. Either disjunct produces a contradiction.

Both subcases yield contradictions, so `bᵢ = pᵢ` for all `1 ≤ i ≤ #p`, giving `p ≼ b`.

*Case 2: `#b < #p`.* We derive a contradiction.

From `p ≼ a`, `#a ≥ #p > #b`. By T3, `#a > #b` implies `a ≠ b`. Since `#a > #b`, `a` cannot be a proper prefix of `b`. Thus `a ≤ b` means `a < b`, which by T1 requires a witness `k ≥ 1` with `aᵢ = bᵢ` for all `i < k` and either: (i) `k ≤ min(#a, #b) = #b` and `aₖ < bₖ`, or (ii) `k = #a + 1 ≤ #b`. Case (ii) supplies `#a + 1 ≤ #b`; NAT-addcompat's strict successor inequality `#a < #a + 1` chains with this through NAT-order's definition of `≤` — unfolding `#a + 1 ≤ #b` into `#a + 1 < #b ∨ #a + 1 = #b`, the first disjunct closing with `#a < #a + 1` under NAT-order's `<`-transitivity and the second substituting into `#a < #a + 1` to give `#a < #b` directly — yielding `#a < #b`, which contradicts `#a > #b` via NAT-order's exactly-one trichotomy clause `¬(m < n ∧ n < m)` at `(#a, #b)`. So case (i) holds: there exists `k ≤ #b` with `aᵢ = bᵢ` for all `1 ≤ i < k` and `aₖ < bₖ`.

Since `k ≤ #b < #p ≤ #a`, position `k` lies within `p`, so `aₖ = pₖ`. Therefore `bₖ > aₖ = pₖ`. Likewise, since `k < #p ≤ #c`, `cₖ = pₖ`, so `bₖ > cₖ`.

For all `i < k`: `bᵢ = aᵢ = pᵢ = cᵢ`. At position `k`, `bₖ > cₖ`, and `k ≤ min(#b, #c)`. By T1 case (i), `c < b`. Now `b ≤ c` abbreviates `b < c ∨ b = c`: the disjunct `b < c` together with `c < b` violates T1 postcondition (b) trichotomy's clause `¬(a < b ∧ b < a)` instantiated at `(b, c)`; the disjunct `b = c` substitutes into `c < b` to yield `b < b`, violating T1 postcondition (a) irreflexivity. Either disjunct produces a contradiction.

Since Case 2 is impossible, `p ≼ b` holds in all cases. ∎

*Formal Contract:*
- *Preconditions:* `a, b, c ∈ T`; `p` is a tumbler prefix with `#p ≥ 1`; `p ≼ a`; `p ≼ c`; `a ≤ b ≤ c` under T1.
- *Depends:*
  - T0 (CarrierSetDefinition) — supplies the length operator `#·` on `b` for the Case 1 hypothesis `#b ≥ #p` and the Case 2 hypothesis `#b < #p`, and the component projection `i ↦ bᵢ` used in Case 1 to construct the divergence-index set `{k ∈ {1, ..., #p} : bₖ ≠ pₖ}`. Neither operator is supplied for arbitrary `b ∈ T` by Prefix (which only unfolds prefix relations on `a`, `c`) or T3 (which speaks to equality from component agreement, not the projection itself).
  - Prefix (PrefixRelation) — unfolds `p ≼ a`, `p ≼ c` into length and component-wise equalities; re-folds component-wise agreement into `p ≼ b`.
  - T1 (LexicographicOrder), case (i) — derives contradictions `b < a` and `c < b` from divergence-position witnesses.
  - T1 (LexicographicOrder), case (ii) — supplies `k = #a + 1 ≤ #b` in Case 2; combined with NAT-addcompat's `#a < #a + 1` this yields `#a < #b`, which contradicts `#a > #b` and excludes case (ii).
  - T1 (LexicographicOrder), postcondition (a) irreflexivity — closes the `a = b` disjunct of `a ≤ b` (Subcase 1a) and the `b = c` disjunct of `b ≤ c` (Subcase 1b and Case 2) by substituting the derived `b < a` / `c < b` into `a < a` / `b < b`.
  - T1 (LexicographicOrder), postcondition (b) trichotomy — closes the `a < b` disjunct of `a ≤ b` (Subcase 1a) and the `b < c` disjunct of `b ≤ c` (Subcase 1b and Case 2) via the clause `¬(a < b ∧ b < a)` at `(a, b)` and `(b, c)` respectively.
  - T3 (CanonicalRepresentation) — distinct lengths imply distinct tumblers, giving `a ≠ b` in Case 2.
  - NAT-order (NatStrictTotalOrder) — trichotomy at `(bₖ, pₖ)` in Case 1 dichotomizes `bₖ ≠ pₖ` into `bₖ < pₖ ∨ bₖ > pₖ`; the `≤`/`<` clauses on ℕ underwrite the length reasoning throughout (`#a ≥ #p`, `#c ≥ #p`, `#b < #p`, `k ≤ #p ≤ min(#a, #b)`); the exclusion of T1(ii) in Case 2 unfolds `#a + 1 ≤ #b` by NAT-order's definition of `≤` and applies either `<`-transitivity (on `#a < #a + 1 < #b`) or equality substitution (on `#a + 1 = #b`) to reach `#a < #b`, then closes via exactly-one trichotomy's `¬(m < n ∧ n < m)` clause at `(#a, #b)` against `#a > #b`.
  - NAT-addcompat (NatAdditionOrderAndSuccessor) — supplies the strict successor inequality `#a < #a + 1`, used in Case 2 to promote T1(ii)'s `#a + 1 ≤ #b` to `#a < #b` and derive the contradiction with `#a > #b`.
  - NAT-wellorder (NatWellOrdering) — least-element principle in Case 1, invoked on the nonempty set of indices `k ∈ {1, ..., #p}` with `bₖ ≠ pₖ` to select the first divergence index.
- *Postconditions:* `p ≼ b` — `b` extends `p` and belongs to the same subtree as `a` and `c`.

Nelson: "The first point of a span may designate a server, an account, a document or an element; so may the last point. There is no choice as to what lies between; this is implicit in the choice of first and last point." A span between two endpoints under the same prefix captures exactly the addresses under that prefix between those endpoints — no addresses from unrelated subtrees can interleave.

Because the hierarchy is projected onto a flat line (T1), containment in the tree corresponds to contiguity on the line. Nelson: "A span may be visualized as a zone hanging down from the tumbler line — what is called in computer parlance a depth-first spanning tree." Every subtree maps to a contiguous range, and every contiguous range within a subtree stays within the subtree.

### Decidable containment

T1 orders tumblers; T6 decides containment — does address `a` belong under address `b`?

**T6 (DecidableContainment).** For any T4-valid tumblers `a, b ∈ T`, the following are decidable from the addresses alone:

  (a) Whether `a` and `b` share the same node field.

  (b) Whether `a` and `b` both carry a user field and those user fields match, alongside matching node fields.

  (c) Whether `a` and `b` both carry a document field and the node, user, and document fields match pairwise.

  (d) Whether `a` and `b` both carry a document field, their node and user fields match, and `D(b)` is a prefix of `D(a)`.

Symmetric or asymmetric absence of the required field fails the shared-presence requirement in (b)–(d).

*Proof.* Each case admits a terminating decision procedure on the tumbler representations alone, via three ingredients.

*Ingredient 1 (field extraction).* By T4, valid tumblers have at most three zeros, no two zeros adjacent, and neither leading nor trailing zero. T4b's four partial projections `N, U, D, E : T ⇀ T` are defined on the T4-valid subset (with each projection's domain further restricted by `zeros(t)`) and uniquely determined on their stated domains by T4b's own derivation (from T4 + T4a); each returns a nonempty element of `T`, which by T0 is a finite sequence over ℕ. Field absence is encoded by partiality of the projection (unambiguous by T4a, since every present segment is non-empty). Extraction is a single finite scan.

*Ingredient 2 (field presence).* Let `zeros(t) = |{i : 1 ≤ i ≤ #t ∧ tᵢ = 0}|` as in T4 (with `|·|` the cardinality operator on finite subsets of ℕ axiomatized by NAT-card, distinct from T0's tumbler-length `#·`), computable by one scan. NAT-card's axiom — `|·|` total on subsets of every initial segment `{1, …, n} ⊆ ℕ` with codomain ℕ — applied to the zero-index subset `{i : 1 ≤ i ≤ #t ∧ tᵢ = 0} ⊆ {1, …, #t}` (a subset of T0's index domain) places `zeros(t) ∈ ℕ`. By T4b's presence-pattern postcondition: `N(t)` is defined on every T4-valid tumbler; `U(t)` is defined iff `zeros(t) ≥ 1`; `D(t)` is defined iff `zeros(t) ≥ 2`; `E(t)` is defined iff `zeros(t) = 3`. NAT-closure grounds these threshold numerals in ℕ (`1 ∈ ℕ` axiomatically; `2 := 1 + 1 ∈ ℕ` and `3 := 2 + 1 ∈ ℕ` by closure of ℕ under addition), so each comparison `zeros(t) ≥ 1`, `zeros(t) ≥ 2`, `zeros(t) = 3` — with the left-hand side in ℕ by NAT-card and the right-hand side in ℕ by NAT-closure — is between two elements of ℕ. Each presence check reduces to comparing `zeros(t)` against a fixed threshold.

*Ingredient 3 (finite-sequence equality).* Sequences `S = (s₁, ..., sₘ)` and `R = (r₁, ..., rₙ)` are equal iff `m = n` and `(A i : sᵢ = rᵢ)`. Decidability of equality on ℕ follows from NAT-order's trichotomy: the three-way disjunction `m < n ∨ m = n ∨ n < m` reduces deciding `=` to deciding `<`, with the middle disjunct holding precisely when both `<`-tests fail. The procedure terminates in at most `m + 1` steps — `m + 1 ∈ ℕ` by NAT-closure's signature `+ : ℕ × ℕ → ℕ` instantiated at `(m, 1)` with `1 ∈ ℕ` from NAT-closure — call this *componentwise comparison*.

*(a) Same node field.* Extract `N(a), N(b)`. Both are present (Ingredient 2). Apply componentwise comparison. Returns *yes* iff `N(a) = N(b)`.

*(b) Matching user and node fields under shared presence.* Extract `N(a), U(a), N(b), U(b)`. Require `zeros(a) ≥ 1 ∧ zeros(b) ≥ 1`; asymmetric absence returns *no*, and symmetric absence returns *no* since both `U` projections being undefined does not furnish a present shared user field. When both thresholds hold, apply componentwise comparison to `N(a) = N(b)` then `U(a) = U(b)`.

*(c) Matching node, user, document fields under shared presence.* Extract all three projections from each. Require `zeros(a) ≥ 2 ∧ zeros(b) ≥ 2`; asymmetric or symmetric absence returns *no*. When both thresholds hold, apply componentwise comparison to `N(a) = N(b)`, `U(a) = U(b)`, `D(a) = D(b)`.

*(d) Document-field prefix within shared document family.* Relaxes (c) along the D-coordinate: keep `N(a) = N(b) ∧ U(a) = U(b)` as the document-family prerequisites, replace `D(a) = D(b)` with `D(b) ⪯ D(a)` (parent `b` a prefix of descendant `a`, since `a` belongs under `b`). Extract `N(a), U(a), D(a) = (D₁ᵃ, ..., Dᵧₐᵃ)` and `N(b), U(b), D(b) = (D₁ᵇ, ..., Dᵧᵦᵇ)`. Require `zeros(a) ≥ 2 ∧ zeros(b) ≥ 2`; this automatically furnishes presence of `N` and `U` on both sides. Asymmetric or symmetric D-absence returns *no*. When both thresholds hold, check `N(a) = N(b)` and `U(a) = U(b)`; if either fails, return *no*. Otherwise `D(b) ⪯ D(a)` iff `γᵦ ≤ γₐ ∧ (A k : 1 ≤ k ≤ γᵦ : Dₖᵃ = Dₖᵇ)`. Check length, then componentwise agreement up to position `γᵦ`.

In every case the procedure examines only the finite component sequences of `a` and `b`, performs finitely many equality or ordering tests on ℕ, and terminates. No mapping tables, version graphs, or system state are consulted. ∎

*Formal Contract:*
- *Preconditions:* `a, b ∈ T` are T4-valid (i.e., `a, b ∈ dom(N)` in the sense of T4b).
- *Depends:*
  - T0 (CarrierSetDefinition) — fixes carrier ℕ.
  - NAT-order (NatStrictTotalOrder) — trichotomy for decidable equality on ℕ; strict order for length comparisons.
  - NAT-zero (NatZeroMinimum) — supplies `0 ∈ ℕ` as the constant tested in `tᵢ = 0` within `zeros(t) = |{i : 1 ≤ i ≤ #t ∧ tᵢ = 0}|` (Ingredient 2), and underlying T4's no-adjacent-zeros and boundary constraints recapitulated in Ingredient 1.
  - NAT-closure (NatArithmeticClosureAndIdentity) — supplies `1 ∈ ℕ` and closure of ℕ under addition, grounding the presence-pattern numerals `1, 2, 3 ∈ ℕ` (`2 := 1 + 1 ∈ ℕ`, `3 := 2 + 1 ∈ ℕ`) used in Ingredient 2 and in the Postconditions as the thresholds `zeros(t) ≥ 1`, `zeros(t) ≥ 2`, `zeros(t) = 3`; the numeral `1` in the componentwise-equality index range `(A k : 1 ≤ k ≤ #D(b) : ...)` of case (d) and postcondition (d); and the successor `m + 1 ∈ ℕ` in Ingredient 3's termination-bound exposition via the signature clause `+ : ℕ × ℕ → ℕ` instantiated at `(m, 1)`.
  - NAT-card (NatFiniteSetCardinality) — axiomatizes `|·|` as a total operator on subsets of every initial segment `{1, …, n} ⊆ ℕ` with codomain ℕ, so `zeros(t) = |{i : 1 ≤ i ≤ #t ∧ tᵢ = 0}|` introduced in Ingredient 2 is well-typed and places `zeros(t) ∈ ℕ`; this typing is what turns the threshold comparisons `zeros(t) ≥ 1`, `zeros(t) ≥ 2`, `zeros(t) = 3` in Ingredient 2 and in postconditions (b)–(d) into comparisons between two elements of ℕ once NAT-closure has placed the right-hand numerals in ℕ. Also fixes `|·|` as distinct from T0's tumbler-length `#·`.
  - T3 (CanonicalRepresentation, this ASN) — supplies the componentwise-equality characterisation of sequence equality on `T`: `a = b ≡ #a = #b ∧ (A i : 1 ≤ i ≤ #a : aᵢ = bᵢ)`. This is the equivalence Ingredient 3 appeals to when it reduces sequence equality to length agreement together with position-by-position comparison, and it is what licences the projection equalities `N(a) = N(b)` in case (a), `N(a) = N(b) ∧ U(a) = U(b)` in case (b), and `N(a) = N(b) ∧ U(a) = U(b) ∧ D(a) = D(b)` in case (c) as finitely many ℕ-equality checks on the extracted field sequences; the same reduction underwrites the `N(a) = N(b)` and `U(a) = U(b)` portions of case (d)'s document-family prerequisites. Uniqueness of the four projections themselves is not T3's role — that is established by T4b directly from T4 + T4a.
  - T4 (HierarchicalParsing) — zero-count bound, no-adjacent-zeros, boundary constraints, role-assignment of zeros as separators.
  - T4a (SyntacticEquivalence) — present field segments non-empty, so partiality of a projection unambiguously indicates field absence.
  - T4b (UniqueParse) — partial projections `N, U, D, E : T ⇀ T`; presence-pattern postcondition tying each projection's domain to `zeros(t)`.
- *Forward References:*
  - T1 (LexicographicOrder) — named as the ordering companion to T6; the claim frames itself as the containment-decision counterpart to T1's sort order, but T6's proof does not consume T1's ordering relation.
- *Postconditions:*
  - (a) Terminates, returns YES iff `N(a) = N(b)`.
  - (b) Terminates, returns YES iff `zeros(a) ≥ 1 ∧ zeros(b) ≥ 1 ∧ N(a) = N(b) ∧ U(a) = U(b)`; NO under asymmetric or symmetric absence.
  - (c) Terminates, returns YES iff `zeros(a) ≥ 2 ∧ zeros(b) ≥ 2 ∧ N(a) = N(b) ∧ U(a) = U(b) ∧ D(a) = D(b)`; NO under asymmetric or symmetric absence.
  - (d) Terminates, returns YES iff `zeros(a) ≥ 2 ∧ zeros(b) ≥ 2 ∧ N(a) = N(b) ∧ U(a) = U(b) ∧ #D(b) ≤ #D(a) ∧ (A k : 1 ≤ k ≤ #D(b) : D(a)ₖ = D(b)ₖ)`; NO under D-absence or when `N(a) ≠ N(b)` or `U(a) ≠ U(b)`.
  - All decisions use only the four projections at `a` and `b` and componentwise comparison on finite ℕ-sequences.

T6 captures allocation hierarchy, not derivation history. Version `5.3` was allocated under `5`, but this alone does not record which version's content was copied. Nelson: "the version, or subdocument number is only an accidental extension of the document number, and strictly implies no specific relationship of derivation." Formal version-derivation requires the version graph.

Shared prefix means shared containing scope: "The owner of a given item controls the allocation of the numbers under it." But: "Tumblers do not affect the user-level structure of the documents; they only provide a mapping mechanism, and impose no categorization and no structure on the contents of a document." Shared prefix guarantees containment and ownership, never semantic categorization.

Gregory's `tumblercmp` (total order) and `tumbleraccounteq` (prefix match with zero-as-wildcard, truncating candidate to parent length) realize the distinction between ordering and containment; `tumbleraccounteq` is the operational form of T6.

### First element-field component distinguishes element-level tumblers

Within a document's element space, the first component after the third zero delimiter identifies the *subspace*: 1 for text, 2 for links. Nelson also mentions that the link subspace "could be further subdivided."

**T7 (FirstElementFieldDistinction).** If two T4-valid element-level tumblers have different first element-field components, they are distinct tumblers:

  `(A a, b ∈ T : a, b satisfy T4 ∧ zeros(a) = zeros(b) = 3 : a.E₁ ≠ b.E₁ ⟹ a ≠ b)`

*Proof.* We are given two T4-valid tumblers `a, b ∈ T` with `zeros(a) = zeros(b) = 3`, so by T4b `a.E₁` and `b.E₁` denote well-defined components, and `a.E₁ ≠ b.E₁`. We must show `a ≠ b`.

By T4, every zero in either tumbler is a field separator. By T4a, T4's positional field-segment constraints force each of the four field segments — node, user, document, element — to be non-empty; NAT-order's `≥` on ℕ then locally re-expresses this conclusion as the field-length inequalities `α, β, γ, δ ≥ 1` and `α', β', γ', δ' ≥ 1`. Strict positivity at every non-separator position is derived locally rather than read off a stipulated display: T0 supplies `tᵢ ∈ ℕ` at each `i ∈ {1, …, #t}`; T4's *field separator* definition makes a non-separator position one with `tᵢ ≠ 0`; NAT-zero's disjunction `(A n ∈ ℕ :: 0 < n ∨ 0 = n)`, instantiated at `n := tᵢ` (licensed by `tᵢ ∈ ℕ` from T0), yields `0 < tᵢ ∨ 0 = tᵢ`, and the equality branch is excluded by the non-separator distinction `tᵢ ≠ 0`, leaving `0 < tᵢ` at every non-separator position; NAT-order supplies `<` on ℕ.

Write the field lengths of `a` as `(α, β, γ, δ)`, so the three separators sit at positions `α + 1`, `α + β + 2`, `α + β + γ + 3`, and `a.E₁` occupies position `pₐ = α + β + γ + 4`. Analogously for `b`, write `(α', β', γ', δ')` with `p_b = α' + β' + γ' + 4`. The arithmetic just introduced — the numerals `2`, `3`, `4` and the separator-position and element-field-position sums `α + 1`, `α + β + 2`, `α + β + γ + 3`, `α + β + γ + 4` (and the primed counterparts) — is grounded thus: NAT-closure posits `1 ∈ ℕ` (the same `1` invoked above in `α, β, γ, δ ≥ 1` and `α', β', γ', δ' ≥ 1`) and closes ℕ under addition, so `2 := 1 + 1 ∈ ℕ`, `3 := 2 + 1 ∈ ℕ`, `4 := 3 + 1 ∈ ℕ`, and each of `α + 1`, `α + β + 2`, `α + β + γ + 3`, `α + β + γ + 4` lies in ℕ.

*Case 1* (`pₐ = p_b`). Both first element-field components sit at position `p`. By hypothesis `a[p] ≠ b[p]`, so by T3, `a ≠ b`.

*Case 2* (`pₐ ≠ p_b`).

*Sub-case 2a* (`#a ≠ #b`). By T3, `a ≠ b`.

*Sub-case 2b* (`#a = #b`). Suppose for contradiction the separator-position sets `{α + 1, α + β + 2, α + β + γ + 3}` and `{α' + 1, α' + β' + 2, α' + β' + γ' + 3}` coincide. To license matching the two enumerations pairwise in ascending order, we first establish that within each enumeration the three listed expressions are strictly ordered: `α + 1 < α + β + 2 < α + β + γ + 3`, and likewise for the primed expressions.

*First strict inequality* (`α + 1 < α + β + 2`). NAT-addbound at `(m, n) := (β, 1)` delivers `β + 1 ≥ 1`, which NAT-order's `≥`-definition rewrites to `1 ≤ β + 1`. NAT-addcompat's left order compatibility `(A m', n', p ∈ ℕ : p ≤ n' : m' + p ≤ m' + n')`, instantiated at `(m', n', p) := (α, β + 1, 1)`, lifts `1 ≤ β + 1` to `α + 1 ≤ α + (β + 1)`. NAT-addassoc at `(m, n, p) := (α, β, 1)` rewrites `α + (β + 1) = (α + β) + 1 = α + β + 1`, so `α + 1 ≤ α + β + 1`. NAT-addcompat's strict successor inequality `(A k ∈ ℕ :: k < k + 1)`, instantiated at `k := α + β + 1`, gives `α + β + 1 < (α + β + 1) + 1`; NAT-addassoc at `(m, n, p) := (α + β, 1, 1)` rewrites `(α + β + 1) + 1 = (α + β) + (1 + 1) = α + β + 2` (with `2 := 1 + 1`), so `α + β + 1 < α + β + 2`. NAT-order's `≤`-definition `a ≤ b ⟺ a < b ∨ a = b`, instantiated at `(a, b) := (α + 1, α + β + 1)`, splits `α + 1 ≤ α + β + 1` into `α + 1 < α + β + 1 ∨ α + 1 = α + β + 1`: in the strict branch NAT-order transitivity at `(α + 1, α + β + 1, α + β + 2)` chains to `α + 1 < α + β + 2`; in the equality branch indiscernibility of `=` rewrites `α + β + 1 < α + β + 2` under `α + 1 = α + β + 1` to `α + 1 < α + β + 2`. Either way, `α + 1 < α + β + 2`.

*Second strict inequality* (`α + β + 2 < α + β + γ + 3`). NAT-addbound at `(m, n) := (γ, 2)` delivers `γ + 2 ≥ 2`, which NAT-order's `≥`-definition rewrites to `2 ≤ γ + 2`. NAT-addcompat's left order compatibility, instantiated at `(m', n', p) := (α + β, γ + 2, 2)`, lifts `2 ≤ γ + 2` to `(α + β) + 2 ≤ (α + β) + (γ + 2)`. NAT-addassoc at `(m, n, p) := (α + β, γ, 2)` rewrites `(α + β) + (γ + 2) = ((α + β) + γ) + 2 = α + β + γ + 2`, so `α + β + 2 ≤ α + β + γ + 2`. NAT-addcompat's strict successor at `k := α + β + γ + 2` gives `α + β + γ + 2 < (α + β + γ + 2) + 1`; NAT-addassoc at `(m, n, p) := (α + β + γ, 2, 1)` rewrites `(α + β + γ + 2) + 1 = (α + β + γ) + (2 + 1) = α + β + γ + 3` (with `3 := 2 + 1`), so `α + β + γ + 2 < α + β + γ + 3`. The same `≤`-definition split — at `(a, b) := (α + β + 2, α + β + γ + 2)` — combined with NAT-order transitivity at `(α + β + 2, α + β + γ + 2, α + β + γ + 3)` (or indiscernibility in the equality branch) chains to `α + β + 2 < α + β + γ + 3`.

*Primed strict ordering*. The two derivations above used only NAT-addbound, NAT-addcompat, NAT-addassoc, and NAT-order — no clause specific to `(α, β, γ)` versus `(α', β', γ')`. Repeating them with `(α', β', γ')` in place of `(α, β, γ)` yields `α' + 1 < α' + β' + 2 < α' + β' + γ' + 3`.

The two sets `{α + 1, α + β + 2, α + β + γ + 3}` and `{α' + 1, α' + β' + 2, α' + β' + γ' + 3}` are now each enumerated in strictly ascending order under `<` on ℕ, so NAT-order's strict total order pins down the canonical sorted enumeration of each as exactly the listed sequence — strict inequality forbids any element from occupying two positions, and the three-element sets admit no other ascending enumeration. The set-equality of the two then forces element-by-element matching at corresponding positions.

From `α + 1 = α' + 1`: by NAT-cancel (right cancellation at `m = 1`), `α = α'`.

From `α + β + 2 = α + β' + 2`: by NAT-addassoc (at `m = α, n = β, p = 2`, and with `β'`), rewrite as `(α + β) + 2 = (α + β') + 2`; by NAT-cancel right cancellation at `m = 2`, `α + β = α + β'`; by NAT-cancel left cancellation at `m = α`, `β = β'`.

From `α + β + γ + 3 = α + β + γ' + 3`: by NAT-addassoc (at `m = α + β, n = γ, p = 3`, and with `γ'`), rewrite as `(α + β + γ) + 3 = (α + β + γ') + 3`; by NAT-cancel right cancellation at `m = 3`, `α + β + γ = α + β + γ'`; by NAT-cancel left cancellation at `m = α + β`, `γ = γ'`.

Then `pₐ = α + β + γ + 4 = α' + β' + γ' + 4 = p_b`, contradicting `pₐ ≠ p_b`.

So the separator-position sets differ: there exists a position `j` that is a separator in one tumbler but not the other. At `j`, one tumbler has `0` and the other has a non-separator component, strictly positive by the local derivation above (T0's `tᵢ ∈ ℕ`, T4's field-separator distinction `tᵢ ≠ 0` at non-separator positions, NAT-zero's disjunction `0 < tᵢ ∨ 0 = tᵢ` with the equality branch excluded by `tᵢ ≠ 0`, with `<` on ℕ supplied by NAT-order). Hence `a[j] ≠ b[j]`, and by T3, `a ≠ b`. ∎

*Formal Contract:*
- *Preconditions:* `a, b ∈ T` satisfy the T4 constraints — at most three zero-valued components, no two zeros adjacent, `a₁ ≠ 0`, `a_{#a} ≠ 0` (and likewise for `b`) — and have `zeros(a) = zeros(b) = 3`.
- *Depends:*
  - T0 (CarrierSetDefinition) — components lie in ℕ; supplies the index domain and component projection on which T4's positivity clauses and T3's positional comparison are stated.
  - T3 (CanonicalRepresentation) — tumblers are equal iff same length and agree at every position; converts positional/length disagreement to tumbler inequality.
  - T4 (HierarchicalParsing) — constrains the bound variables; supplies the role-assignment under which zeros are separators and the *field separator* definition that makes a non-separator position one with `tᵢ ≠ 0`, the antecedent the local strict-positivity derivation feeds into NAT-zero's disjunction.
  - T4a (SyntacticEquivalence) — converts T4's positional clauses to segment non-emptiness, fixing `α, β, γ, δ ≥ 1`.
  - T4b (UniqueParse) — licenses the well-definedness of `t.E₁` on T4-valid inputs with `zeros(t) = 3`.
  - NAT-zero (NatZeroMinimum) — supplies the disjunction `(A n ∈ ℕ :: 0 < n ∨ 0 = n)`, instantiated at `n := tᵢ` (licensed by `tᵢ ∈ ℕ` from T0) and combined with T4's non-separator distinction `tᵢ ≠ 0` to yield strict positivity `0 < tᵢ` at every non-separator position.
  - NAT-order (NatStrictTotalOrder) — supplies `<`/`≤` on ℕ for the zero-count bound (inherited from T4 via the precondition `zeros(a) = zeros(b) = 3`), the `≥ 1` field-length inequalities `α, β, γ, δ ≥ 1` (and the primed counterparts for `b`) locally unpacked from T4a's conclusion, and three further roles in the strict-ordering derivation that drives sub-case 2b: (i) the `≤`-definition `a ≤ b ⟺ a < b ∨ a = b`, used to split `α + 1 ≤ α + β + 1` and `α + β + 2 ≤ α + β + γ + 2` into strict-and-equality branches that then chain into strict inequalities; (ii) transitivity `m < n ∧ n < p ⟹ m < p`, instantiated at `(α + 1, α + β + 1, α + β + 2)` and `(α + β + 2, α + β + γ + 2, α + β + γ + 3)` in the strict branches of those splits; and (iii) the `≥`-definition `a ≥ b ⟺ b ≤ a`, used at `(β + 1, 1)` and `(γ + 2, 2)` to convert NAT-addbound's outputs `β + 1 ≥ 1` and `γ + 2 ≥ 2` into the antecedent forms `1 ≤ β + 1` and `2 ≤ γ + 2` required by NAT-addcompat. Once the strict orderings `α + 1 < α + β + 2 < α + β + γ + 3` and the primed counterpart are established, NAT-order's strict total order pins down the canonical sorted enumeration of each three-element set as exactly the listed sequence (no element can occupy two positions under irreflexive `<`, and a three-element strictly ordered set admits no other ascending enumeration), so the set-equality forces element-by-element matching at corresponding positions.
  - NAT-closure (NatArithmeticClosureAndIdentity) — supplies `1 ∈ ℕ` and closure of ℕ under addition, grounding the numerals `2 := 1 + 1 ∈ ℕ`, `3 := 2 + 1 ∈ ℕ`, `4 := 3 + 1 ∈ ℕ` and the sums `α + 1`, `α + β + 2`, `α + β + γ + 3`, `α + β + γ + 4` (and the primed counterparts for `b`) so that the separator-position expressions and the first element-field position are typed within ℕ; the same `1 ∈ ℕ` underwrites the field-length inequalities `α, β, γ, δ ≥ 1` and `α', β', γ', δ' ≥ 1` locally re-expressed from T4a's segment non-emptiness conclusion.
  - NAT-cancel (NatAdditionCancellation) — right/left cancellation discharges the three pairwise-matching extractions `α = α'`, `β = β'`, `γ = γ'`.
  - NAT-addassoc (NatAdditionAssociative) — regroups `α + β + 2` and `α + β + γ + 3` so NAT-cancel applies at `m = 2` and `m = 3`; additionally regroups inside the strict-ordering derivation of sub-case 2b at `(m, n, p) := (α, β, 1)`, `(α + β, 1, 1)`, `(α + β, γ, 2)`, and `(α + β + γ, 2, 1)` so that NAT-addcompat's left order compatibility and strict successor outputs `α + (β + 1)`, `(α + β + 1) + 1`, `(α + β) + (γ + 2)`, and `(α + β + γ + 2) + 1` are rewritten into the canonical left-associated forms `α + β + 1`, `α + β + 2`, `α + β + γ + 2`, and `α + β + γ + 3` respectively.
  - NAT-addbound (NatAdditionDominatesOperands) — supplies the right-dominance clause `m + n ≥ n` instantiated at `(m, n) := (β, 1)` to deliver `β + 1 ≥ 1` (used to discharge the antecedent `1 ≤ β + 1` of NAT-addcompat's left order compatibility in the first strict inequality) and at `(m, n) := (γ, 2)` to deliver `γ + 2 ≥ 2` (used to discharge the antecedent `2 ≤ γ + 2` of NAT-addcompat's left order compatibility in the second strict inequality), once NAT-order's `≥`-definition rewrites the outputs into the `≤`-form NAT-addcompat consumes.
  - NAT-addcompat (NatAdditionOrderAndSuccessor) — supplies (i) the left order compatibility clause `(A m', n', p ∈ ℕ : p ≤ n' : m' + p ≤ m' + n')`, instantiated at `(m', n', p) := (α, β + 1, 1)` and `(α + β, γ + 2, 2)` to lift the antecedents `1 ≤ β + 1` and `2 ≤ γ + 2` (supplied by NAT-addbound) into `α + 1 ≤ α + (β + 1)` and `(α + β) + 2 ≤ (α + β) + (γ + 2)`; and (ii) the strict successor inequality `(A k ∈ ℕ :: k < k + 1)`, instantiated at `k := α + β + 1` and `k := α + β + γ + 2` to deliver `α + β + 1 < α + β + 2` and `α + β + γ + 2 < α + β + γ + 3`. The `≤` and `<` outputs are then chained by NAT-order's `≤`-split and transitivity into the strict orderings `α + 1 < α + β + 2` and `α + β + 2 < α + β + γ + 3` that license the sorted pairwise matching.
- *Forward References:*
  - T1 (LexicographicOrder) — the ordering T1 induces places all text addresses (subspace 1) before all link addresses (subspace 2) within the same document, as a consequence of `1 < 2` at the subspace position under lexicographic order.
- *Postconditions:* `a.E₁ ≠ b.E₁ ⟹ a ≠ b`.

The ordering T1 places all text addresses (subspace 1) before all link addresses (subspace 2) within the same document, because `1 < 2` at the subspace position — a consequence of the lexicographic order, not an assumption.


---

## 5. Allocation permanence

Once an address is allocated, it persists. The allocator never reclaims an address. Allocation proceeds forward only — a strictly increasing chain. The set of allocated addresses at any state is the union of finite prefixes of per-allocator chains, the *action point* the first nonzero component of a positive tumbler.

### Allocation permanence

**T8 (AllocationPermanence).** If tumbler `a ∈ T` has been allocated at any point in the system's history, then for all subsequent states, `a` remains in the set of allocated addresses. The set of allocated addresses is monotonically non-decreasing.

*Proof.* Let s be a state and s → s' a transition. By AllocatedSet, `allocated(s) = ⋃{domₛ(A) : A activated in s}`. By NoDeallocation, no operation in Σ removes an element from the allocated set, so every transition either leaves `allocated` unchanged or adds elements. In both cases `allocated(s) ⊆ allocated(s')`. Induction on the length of a transition sequence s₀ → s₁ → ··· → sₙ yields `allocated(s₀) ⊆ allocated(sₙ)`. ∎

*Formal Contract:*
- *Invariant:* For every state transition s → s', `allocated(s) ⊆ allocated(s')`.
- *Postcondition:* For every admissible transition sequence s₀ → s₁ → ··· → sₙ, `allocated(sᵢ) ⊆ allocated(sⱼ)` whenever `0 ≤ i ≤ j ≤ n`; equivalently, once `a ∈ allocated(sᵢ)`, `a ∈ allocated(sⱼ)` for all `j ≥ i`.
- *Depends:*
  - AllocatedSet (AllocatedSet) — defines `allocated(s)`, state, and state transition.
  - NoDeallocation (NoDeallocation) — no operation in Σ removes an allocated address.

### Monotonic allocation

**T9 (ForwardAllocation).** Within a single allocator's sequential stream, new addresses are strictly monotonically increasing: if `a` was allocated before `b` by the same allocator, then `a < b`.

Each allocator `A` has domain `dom(A) = {tₙ : n ≥ 0}` with `t₀` the base address and `tₙ₊₁ = inc(tₙ, 0)`; child-spawning outputs are excluded from the parent's domain and serve as base addresses for child allocators. The predicate `same_allocator(a, b)` holds when `a, b ∈ dom(A)` for some `A`. The predicate `allocated_before(a, b)` holds when `a = tᵢ`, `b = tⱼ`, and `i < j` in the enumeration of `dom(A)`; this is well-defined because T10a.6 (DomainDisjointness) fixes `A` uniquely from `(a, b)` and T10a.7 (EnumerationInjectivity) fixes each index uniquely.

The claim:

  `(A a, b : same_allocator(a, b) ∧ allocated_before(a, b) : a < b)`

T9 is per-allocator, not global. When a parent forks a child via `inc(·, k')` with `k' > 0`, the child is inserted between the parent and the parent's next sibling on the tumbler line: `2.1.1` may be created after `2.2`, yet `2.1 < 2.1.1 < 2.2` by T1 case (ii). Concurrent allocators (e.g., distinct users under a shared server prefix) impose no cross-stream ordering.

*Proof.* Assume `same_allocator(a, b) ∧ allocated_before(a, b)`. By T10a.6 (DomainDisjointness), the allocator `A` with `a, b ∈ dom(A)` is uniquely fixed by the pair — no other allocator contains both. By T10a.7 (EnumerationInjectivity), the indices are uniquely fixed too, so there exist unique `i, j ≥ 0` with `a = tᵢ` and `b = tⱼ`; `allocated_before(a, b)` then delivers `i < j`. T10a.7's strict-order postcondition `(A m, n ≥ 0 : m < n : tₘ < tₙ)`, instantiated at `(m, n) = (i, j)`, yields `tᵢ < tⱼ`. Hence `a < b`. ∎

*Formal Contract:*
- *Definitions:*
  - `allocated_before(a, b)` ≡ `a = tᵢ ∧ b = tⱼ ∧ i < j` in T10a's enumeration of `dom(A)`, well-defined on pairs satisfying `same_allocator(a, b)` by T10a.6 and T10a.7.
- *Depends:*
  - T10a (AllocatorDiscipline) — defines `dom(A)`, `same_allocator`, and the enumeration `tₙ₊₁ = inc(tₙ, 0)` that indexes the allocation sequence.
  - T10a.6 (DomainDisjointness) — under `same_allocator(a, b)`, the witnessing allocator `A` is uniquely determined, so the enumeration context in which `i < j` holds is unambiguous.
  - T10a.7 (EnumerationInjectivity) — used in two roles: (i) index uniqueness, so the `i, j ≥ 0` with `a = tᵢ, b = tⱼ` are determined by `(a, b)` and `allocated_before`'s `i < j` is unambiguous; (ii) strict-order postcondition `(A m, n ≥ 0 : m < n : tₘ < tₙ)`, instantiated at `(i, j)`, delivers `tᵢ < tⱼ` in one step and replaces the prior induction on `d = j − i`.
  - T1 (LexicographicOrder) — supplies the total order `<` in which T10a.7's strict-order form and T9's conclusion `a < b` are both phrased.
- *Preconditions:* `a, b ∈ T` with `same_allocator(a, b) ∧ allocated_before(a, b)`.
- *Postconditions:* `a < b` under the tumbler order T1.

**NoDeallocation (NoDeallocation).** The system defines no operation that removes an element from the set of allocated addresses. This is a design constraint accepted as an axiom.

Nelson: "any address of any document in an ever-growing network may be specified by a permanent tumbler address." The permanence guarantee requires that the allocated set can only grow.

Let Σ, 𝒮, and `allocated(s)` be as defined in AllocatedSet — the transition vocabulary, the state space, and the allocated-set function on states, respectively. The axiom asserts: for every operation `op ∈ Σ` and every state `s ∈ 𝒮` in which `op(s)` is defined, `allocated(s) ⊆ allocated(op(s))`. Because Σ is closed — every transition the system can undergo is an application of some `op ∈ Σ` — the axiom constrains any operation the system could ever admit.

*Formal Contract:*
- *Axiom:* `(A op ∈ Σ, s ∈ 𝒮 :: op(s) defined ⟹ allocated(s) ⊆ allocated(op(s)))`, where Σ is the system's complete (closed) transition vocabulary of partial functions on 𝒮 and 𝒮 is the state space of the allocation system. Frame assumption: Σ is closed.
- *Depends:*
  - AllocatedSet (AllocatedSet) — supplies the transition vocabulary Σ, the state space 𝒮, and the symbol `allocated(s) = ⋃ { domₛ(A) : A activated in s }`.

**ActionPoint (ActionPoint).** For w ∈ T with Pos(w), the *action point* of w, written actionPoint(w), is the unique m ∈ S such that (A n ∈ S :: m ≤ n), where S = {i ∈ ℕ : 1 ≤ i ≤ #w ∧ wᵢ ≠ 0}.

*Derivation.* The set S = {i ∈ ℕ : 1 ≤ i ≤ #w ∧ wᵢ ≠ 0} is a nonempty subset of ℕ: nonempty by TA-Pos, and a subset of ℕ by construction (the carrier `i ∈ ℕ` is licensed by T0's commitment that the index domain `{1, …, #w}` of w lies in ℕ). By NAT-wellorder, there exists m ∈ S with (A n ∈ S :: m ≤ n). Such m is unique: if m₁ and m₂ both satisfy the clause, then m₁ ≤ m₂ and m₂ ≤ m₁. Unfolding each via NAT-order's definition `m ≤ n ⟺ m < n ∨ m = n` yields `m₁ < m₂ ∨ m₁ = m₂` from the first and `m₂ < m₁ ∨ m₂ = m₁` from the second, so the conjunction distributes into four disjunct pairings, which we discharge using only NAT-order's irreflexivity `(A n ∈ ℕ :: ¬(n < n))` and transitivity `(A m, n, p ∈ ℕ : m < n ∧ n < p : m < p)`. If `m₁ < m₂` and `m₂ < m₁`, transitivity gives `m₁ < m₁`, contradicting irreflexivity. If `m₁ < m₂` and `m₂ = m₁`, substituting `m₁` for `m₂` in `m₁ < m₂` gives `m₁ < m₁`, again contradicting irreflexivity. The case `m₁ = m₂` with `m₂ < m₁` is handled analogously: substituting `m₁` for `m₂` in `m₂ < m₁` gives `m₁ < m₁`, contradicting irreflexivity. The remaining pairing `m₁ = m₂` with `m₂ = m₁` asserts the equality directly. So `m₁ = m₂`. So actionPoint(w) names this element unambiguously, and actionPoint(w) ∈ S, giving 1 ≤ actionPoint(w) ≤ #w. For any i ∈ ℕ with 1 ≤ i < actionPoint(w), wᵢ = 0. Suppose otherwise, for contradiction: then wᵢ ≠ 0, and to conclude i ∈ S we must also establish the three remaining membership clauses `i ∈ ℕ`, `1 ≤ i`, and `i ≤ #w`; the carrier `i ∈ ℕ` holds by the universal's domain restriction, the bound `1 ≤ i` holds by hypothesis, so only `i ≤ #w` needs discharge. From actionPoint(w) ∈ S we have actionPoint(w) ≤ #w, which NAT-order's definition `m ≤ n ⟺ m < n ∨ m = n` unfolds as `actionPoint(w) < #w ∨ actionPoint(w) = #w`. If `actionPoint(w) < #w`, NAT-order's transitivity applied to `i < actionPoint(w)` and `actionPoint(w) < #w` gives `i < #w`. If `actionPoint(w) = #w`, rewriting `i < actionPoint(w)` by this equality gives `i < #w`. Either way, i < #w, and NAT-order's definition `i ≤ #w ⟺ i < #w ∨ i = #w` then licenses `i ≤ #w` from its left disjunct. So i ∈ S. Instantiating the universal `(A n ∈ S :: actionPoint(w) ≤ n)` at n = i gives `actionPoint(w) ≤ i`, which NAT-order's definition `m ≤ n ⟺ m < n ∨ m = n` unfolds as `actionPoint(w) < i ∨ actionPoint(w) = i`. If `actionPoint(w) < i`, NAT-order's transitivity applied to `actionPoint(w) < i` and `i < actionPoint(w)` gives `actionPoint(w) < actionPoint(w)`, contradicting irreflexivity. If `actionPoint(w) = i`, substituting `actionPoint(w)` for `i` in `i < actionPoint(w)` gives `actionPoint(w) < actionPoint(w)`, again contradicting irreflexivity. Both disjuncts contradict, so the supposition `wᵢ ≠ 0` fails; hence `wᵢ = 0`. For 1 ≤ w_{actionPoint(w)}: membership of actionPoint(w) in S gives w_{actionPoint(w)} ≠ 0. Instantiating NAT-zero's disjunction axiom `(A n ∈ ℕ :: 0 < n ∨ 0 = n)` at n = w_{actionPoint(w)} yields 0 < w_{actionPoint(w)} ∨ 0 = w_{actionPoint(w)}, and w_{actionPoint(w)} ≠ 0 excludes the equality, leaving 0 < w_{actionPoint(w)}. NAT-discrete's forward direction m < n ⟹ m + 1 ≤ n at m = 0, n = w_{actionPoint(w)} yields 0 + 1 ≤ w_{actionPoint(w)}. NAT-closure posits 1 ∈ ℕ directly, licensing its additive identity (A n ∈ ℕ :: 0 + n = n) to be instantiated at n = 1; this gives the equality 0 + 1 = 1, and rewriting 0 + 1 ≤ w_{actionPoint(w)} by it yields 1 ≤ w_{actionPoint(w)}. ∎

*Formal Contract:*
- *Preconditions:* w ∈ T, Pos(w)
- *Definition:* actionPoint(w) is the unique m ∈ S with (A n ∈ S :: m ≤ n), where S = {i ∈ ℕ : 1 ≤ i ≤ #w ∧ wᵢ ≠ 0}.
- *Depends:*
  - NAT-carrier (NatCarrierSet) — supplies `ℕ` as the underlying set appearing in the comprehension `S = {i ∈ ℕ : 1 ≤ i ≤ #w ∧ wᵢ ≠ 0}` defining S, over which the bounded universal `(A i ∈ ℕ : 1 ≤ i < actionPoint(w) : wᵢ = 0)` of the *Postconditions:* ranges, and as the ambient set whose elements the bound variables `m, n` of NAT-wellorder's least-element principle `(E m ∈ S :: (A n ∈ S :: m ≤ n))` inhabit when instantiated on S (since `S ⊆ ℕ`).
  - T0 (CarrierSetDefinition) — supplies T, #w, component projection wᵢ, the commitment that the index domain `{1, …, #w}` of w is a subset of ℕ, and the commitment that the component projection delivers ℕ-valued components (i.e., `wᵢ ∈ ℕ` for each `i ∈ {1, …, #w}`), which types `w_{actionPoint(w)}` as a natural number and thereby licenses the NAT-zero and NAT-discrete instantiations at `n = w_{actionPoint(w)}`.
  - TA-Pos (PositiveTumbler) — supplies Pos(w) and the existential making S nonempty.
  - NAT-wellorder (NatWellOrdering) — least-element principle giving existence of m ∈ S with (A n ∈ S :: m ≤ n).
  - NAT-zero (NatZeroMinimum) — supplies the disjunction axiom `(A n ∈ ℕ :: 0 < n ∨ 0 = n)` instantiated at n = w_{actionPoint(w)}, and 0 ∈ ℕ.
  - NAT-order (NatStrictTotalOrder) — definition of ≤ as `m ≤ n ⟺ m < n ∨ m = n`; irreflexivity and transitivity, used in the case analysis that secures uniqueness of the least element of S and in the derivation that wᵢ = 0 for 1 ≤ i < actionPoint(w) (unfolding actionPoint(w) ≤ #w and chaining with i < actionPoint(w) to reach i < #w, then folding to i ≤ #w).
  - NAT-discrete (NatDiscreteness) — forward direction m < n ⟹ m + 1 ≤ n.
  - NAT-closure (NatArithmeticClosureAndIdentity) — supplies `1 ∈ ℕ` directly and the additive identity `(A n ∈ ℕ :: 0 + n = n)`, whose instantiation at n = 1 gives the equality 0 + 1 = 1 used to rewrite.
- *Postconditions:* 1 ≤ actionPoint(w) ≤ #w; `(A i ∈ ℕ : 1 ≤ i < actionPoint(w) : wᵢ = 0)`; 1 ≤ w_{actionPoint(w)}


---

## 6. Allocator discipline

Allocators advance on a per-partition basis. T10 establishes partition independence; T10a decomposes the allocator discipline into eight sub-properties governing sibling production, child spawning, root structure, and ordering. AllocatedSet realizes the abstract per-allocator domains as concrete state-indexed sets. PartitionMonotonicity tracks the growth of partitions under allocation.

### Coordination-free uniqueness

The tumbler hierarchy exists so that independent actors can allocate addresses without communicating.

**T10 (PartitionIndependence).** The address space is partitioned by prefix into ownership domains. Two allocators with distinct, non-nesting prefixes can allocate simultaneously, and the resulting addresses are guaranteed distinct.

Formally: let `p₁` and `p₂` be prefixes such that neither is a prefix of the other (`p₁ ⋠ p₂ ∧ p₂ ⋠ p₁`). Then for any tumbler `a` with prefix `p₁` and any tumbler `b` with prefix `p₂`, `a ≠ b`.

*Proof.* Given `p₁ = p₁₁. ... .p₁ₘ` and `p₂ = p₂₁. ... .p₂ₙ` with `p₁ ⋠ p₂ ∧ p₂ ⋠ p₁`, and tumblers `a` with `p₁ ≼ a`, `b` with `p₂ ≼ b`, show `a ≠ b`. Let `ℓ = min(m, n)`.

*Case 1: `m ≤ n`.* The hypothesis `m ≤ n` is `#p₁ ≤ #p₂`, satisfying the length clause of `p₁ ≼ p₂`. From `p₁ ⋠ p₂` — that is, `¬(p₁ ≼ p₂)` — Prefix's definition expands the negation by De Morgan to `¬(#p₁ ≤ #p₂) ∨ ¬(∀i : 1 ≤ i ≤ #p₁ : (p₂)ᵢ = (p₁)ᵢ)`. The first disjunct contradicts the `m ≤ n` hypothesis, so the second holds: there exists `j` with `1 ≤ j ≤ m` and `p₁ⱼ ≠ p₂ⱼ`. With `m ≤ n`, `min(m, n) = m`, so `j ≤ m = ℓ`.

*Case 2: `m > n`.* The hypothesis `m > n` unfolds, by NAT-order's reverse-companion definition `m > n ⟺ n < m`, to `n < m`; NAT-order's `≤`-definition `n ≤ m ⟺ n < m ∨ n = m` then yields `n ≤ m` from the left disjunct. Hence `#p₂ ≤ #p₁`, satisfying the length clause of `p₂ ≼ p₁`. From `p₂ ⋠ p₁` — that is, `¬(p₂ ≼ p₁)` — Prefix's definition expands the negation by De Morgan to `¬(#p₂ ≤ #p₁) ∨ ¬(∀i : 1 ≤ i ≤ #p₂ : (p₁)ᵢ = (p₂)ᵢ)`. The first disjunct contradicts the `n ≤ m` just derived, so the second holds: there exists `j` with `1 ≤ j ≤ n` and `p₁ⱼ ≠ p₂ⱼ`. With `m > n`, `min(m, n) = n`, so `j ≤ n = ℓ`.

Let `k = min{j : 1 ≤ j ≤ ℓ ∧ p₁ⱼ ≠ p₂ⱼ}`. Then `p₁ᵢ = p₂ᵢ` for `1 ≤ i < k`, `p₁ₖ ≠ p₂ₖ`, and `k ≤ ℓ ≤ min(m, n)`.

Before extracting components, we must establish that `k` lies in the index domains of both `a` and `b`. From `p₁ ≼ a`, Prefix gives `#p₁ ≤ #a`, i.e. `m ≤ #a`; with `k ≤ m` and NAT-order's `≤`-transitivity Consequence, `k ≤ #a`, so `aₖ` is well-defined. Symmetrically, `p₂ ≼ b` gives `n ≤ #b`; with `k ≤ n` and `≤`-transitivity again, `k ≤ #b`, so `bₖ` is well-defined. Now Prefix's component clause applies: from `p₁ ≼ a` and `k ≤ m`, `aₖ = p₁ₖ`; from `p₂ ≼ b` and `k ≤ n`, `bₖ = p₂ₖ`. Hence `aₖ = p₁ₖ ≠ p₂ₖ = bₖ`. Since `k ≤ #a`, `k` lies in T3's index domain `{1, …, #a}`. By the contrapositive of the reverse direction of T3 (`a = b ⟹ #a = #b ∧ (A i : 1 ≤ i ≤ #a : aᵢ = bᵢ)`), the disagreement `aₖ ≠ bₖ` forces `a ≠ b`. ∎

*Formal Contract:*
- *Preconditions:* `p₁, p₂ ∈ T` with `p₁ ⋠ p₂ ∧ p₂ ⋠ p₁`; `a, b ∈ T` with `p₁ ≼ a` and `p₂ ≼ b`.
- *Postconditions:* `a ≠ b`.
- *Depends:*
  - Prefix — definition of `≼` as componentwise agreement.
  - T0 (CarrierSetDefinition) — tumbler length `#p` and component projection `pᵢ`.
  - NAT-order (NatStrictTotalOrder) — at-least-one trichotomy (for the `m ≤ n` vs `m > n` case split), the reverse-companion definition `m > n ⟺ n < m` and `≤`-definition `n ≤ m ⟺ n < m ∨ n = m` (for deriving `n ≤ m` from `m > n` in Case 2 to satisfy the length clause of `p₂ ≼ p₁`), and the `≤`-transitivity Consequence (for chaining `k ≤ m ≤ #a` and `k ≤ n ≤ #b`).
  - NAT-wellorder (NatWellOrdering) — well-definedness of `min` on nonempty subsets of ℕ.
  - T3 (CanonicalRepresentation) — tumblers differing in any component are distinct.

Nelson: "The owner of a given item controls the allocation of the numbers under it." No central allocator is needed. No coordination protocol is needed. The address structure itself makes collision impossible.

Nelson: "Whoever owns a specific node, account, document or version may in turn designate (respectively) new nodes, accounts, documents and versions, by forking their integers. We often call this the 'baptism' of new numbers." Baptism is the mechanism by which ownership domains are established — the owner of a number creates sub-numbers beneath it, and those sub-numbers belong exclusively to the owner.

**T10a (AllocatorDiscipline).** The root allocator begins from a base address satisfying T4. Each allocator produces sibling outputs exclusively by repeated application of `inc(·, 0)` — shallow increment at the last significant position. To spawn a child allocator, the parent performs one `inc(·, k')` with `k' ∈ {1, 2}`, subject to the runtime precondition `zeros(t) ≤ 2` when `k' = 2`, where `zeros(·)` is the zero-count function defined in T4. The chosen `inc(·, k')` establishes the child's prefix, after which further allocation is delegated to the child. Each pair `(t, k')` — a parent domain element together with a spawning parameter `k' ∈ {1, 2}` — produces at most one child-spawning event. The parent's own sibling stream resumes with `inc(·, 0)`.

T10a constrains what would otherwise be unregulated choice. The child-spawning operation establishes a new prefix at a deeper level, from which a new allocator continues with its own `inc(·, 0)` stream. The restriction to `k' ∈ {1, 2}`, combined with TA5a's `zeros(t) ≤ 2` bound at `k' = 2`, ensures child-spawning preserves T4; `k' ≥ 3` would introduce adjacent zeros, violating T4's field-segment constraint (TA5a, case `k ≥ 3`).

*Definitions.* We formalize allocators as nodes of a tree induced by the axiom's spawning rule, then build the per-allocator domain and the `same_allocator` predicate on that structure.

*Allocator tree.* The *allocator tree* 𝒯 consists of a distinguished *root allocator* together with every allocator reachable by finite iteration of the child-spawning rule. Each non-root allocator `A` carries a *spawning triple* `(parent(A), spawnPt(A), spawnParam(A))`, where `parent(A) ∈ 𝒯`, `spawnPt(A) ∈ dom(parent(A))`, and `spawnParam(A) ∈ {1, 2}`. `A`'s *base address* is `inc(spawnPt(A), spawnParam(A))` by TA5. The root carries no spawning triple; its base address is the T4-valid address fixed by the initialization constraint. The tree is defined inductively on depth: level 0 is `{root}`, and level `d + 1` consists of every allocator whose spawning triple's parent lies at level `d`.

*Identity and distinctness.* Two allocators `X` and `Y` are *equal* iff both are the root, or both are non-root with `parent(X) = parent(Y)`, `spawnPt(X) = spawnPt(Y)`, and `spawnParam(X) = spawnParam(Y)`. Equivalently, `X = Y` iff their root-path sequences of spawning triples coincide. Two allocators are *distinct* iff `X ≠ Y`. The at-most-once child-spawning constraint is the dynamic counterpart: a parent cannot produce two distinct children sharing the same `(t, k')`.

*Derived tree relations.* `Y` is a *child* of `X` iff `parent(Y) = X`. The *depth* function satisfies `depth(root) = 0` and `depth(Y) = depth(parent(Y)) + 1`. `X` is an *ancestor* of `Y` iff `X = Y` or `X` is an ancestor of `parent(Y)`; `Y` is a *descendant* of `X` iff `X` is an ancestor of `Y`. `X` and `Y` are *in an ancestor-descendant relationship* iff one is an ancestor of the other. A *param-1 child* of `X` is a child `C` with `spawnParam(C) = 1`; a *param-2 child* is one with `spawnParam(C) = 2`; both satisfy `depth(C) = depth(X) + 1`. Two distinct allocators `Y₁, Y₂ ∈ 𝒯` with `parent(Y₁) = parent(Y₂)` are *sibling allocators* — the tree-level siblinghood relation, distinct from the allocator-output relation defined next.

*Domain.* For each allocator `A` with base address `t₀`, its *domain* is

  `dom(A) = {tₙ : n ≥ 0}` where `tₙ₊₁ = inc(tₙ, 0)`.

Child-spawning outputs are excluded from the parent's domain: when `A` performs `inc(t, k')` with `k' > 0`, the result `c₀ = inc(t, k')` serves as the base of the child allocator `C` with `parent(C) = A`, `spawnPt(C) = t`, `spawnParam(C) = k'`, becoming the initial element of `dom(C)`. The predicate

  `same_allocator(a, b) ≡ ∃A ∈ 𝒯 : a ∈ dom(A) ∧ b ∈ dom(A)`

asserts that two addresses lie in a common allocator's domain. Elements of `dom(A)` are the *siblings* of `A`; two distinct elements are *distinct siblings* of `A`. Unqualified *sibling* denotes this allocator-output relation throughout; *sibling allocator* denotes the tree-level relation between distinct children of a common parent.

T10a is a design axiom — it constrains allocator behavior rather than following from prior properties. We establish eight consequences on which the coordination-free uniqueness guarantees depend, then prove the sibling restriction necessary for prefix-incomparability.

**Consequence 1: Uniform sibling length.** Since T10a restricts sibling production to `inc(·, 0)`, and TA5(c) gives `#inc(t, 0) = #t`, every sibling has the same length as the allocator's base address (T10a.1).

**Consequence 2: Non-nesting sibling prefixes.** By T10a.1, all siblings have equal length; Prefix supplies the positional-agreement clause on the shorter tumbler's positions, and T3 collapses equal-length positional agreement to identity — so distinct siblings cannot be prefix-related (T10a.2).

**Consequence 3: Length separation between parent and child domains.** When the parent performs `inc(·, k')` with `k' ∈ {1, 2}`, TA5(d) gives `#inc(t, k') = #t + k'`. Since `k' ≥ 1` on ℕ (T0; NAT-zero with NAT-discrete at `m = 0` sharpens `k' > 0` to `1 ≤ k'`), NAT-addcompat's strict successor gives `#t < #t + 1`, and its left order-compatibility lifts `1 ≤ k'` to `#t + 1 ≤ #t + k'`; chaining yields `#inc(t, k') > #t`, so the child's base has length strictly exceeding any parent sibling. T10a.1 propagates this across the child's domain, and across `d` nesting levels the separation is additive (T10a.3).

**Consequence 4: T4 preservation under the discipline.** By induction on the allocator tree. *Base:* the root's base address satisfies T4 by initialization. *Step:* TA5a gives unconditional T4-preservation under `inc(·, 0)` and `inc(·, 1)` on T4-valid inputs, and conditional preservation under `inc(·, 2)` when `zeros(t) ≤ 2`; the inductive hypothesis supplies T4-validity of every `t ∈ dom` of the parent, and the axiom enforces `zeros(t) ≤ 2` at every `k' = 2` spawn. Every child-spawning output `inc(t, k')` therefore satisfies T4 and serves as the child's base, closing the induction. Every output of a conforming allocator satisfies T4 (T10a.4).

**Consequence 5: Cross-allocator prefix-incomparability.** For ancestor-descendant pairs, the construction yields a narrower nesting fact than universal pairwise comparability between domains: at each spawning event `(tᵢ, k')`, TA5(b) gives agreement on positions `1..#tᵢ` and TA5(d) combined with NAT-addcompat (as in Consequence 3) gives `#inc(tᵢ, k') > #tᵢ`, so `tᵢ ≺ inc(tᵢ, k')`. TA5(b) also keeps positions `1..#tᵢ` fixed throughout the spawned child's domain and every descendant traced through `tᵢ`, propagating `tᵢ ≺ c` to every such `c`; elements of `dom(parent)` other than `tᵢ` need not be prefix-comparable to descendant domain elements. Output distinctness across ancestor-descendant pairs follows from length separation (T10a.3). For non-ancestor-descendant pairs, we establish prefix-incomparability (T10a.5).

Let X and Y be allocators not in an ancestor-descendant relationship.

*Existence of a lowest common ancestor.* The ancestor relation makes `Anc(X) = {A ∈ 𝒯 : A is an ancestor of X}` include the root: parent-iteration from X strictly decreases depth (`depth(B) = depth(parent(B)) + 1` for non-root B) and terminates at root since depth ∈ ℕ blocks unbounded descent. Symmetrically `root ∈ Anc(Y)`, making `I = Anc(X) ∩ Anc(Y)` nonempty.

The depth-set `D = {depth(A) : A ∈ I} ⊆ ℕ` is nonempty (contains `0 = depth(root)`) and bounded above by `depth(X)`: every `A ∈ I` lies in `Anc(X)`, so the chain from A to X yields `depth(A) ≤ depth(X)` (each step adds 1, terminating at `depth(X)`).

NAT-wellorder supplies `max(D)` by the upper-bound construction (TA5-SIG's pattern). Form `U = {u ∈ ℕ : (A d ∈ D :: d ≤ u)}`; `depth(X) ∈ U`, so `U ≠ ∅`. NAT-wellorder applied to U delivers a least element, name it δ. Suppose `δ ∉ D`: every `d ∈ D` satisfies `d ≤ δ` (from `δ ∈ U`) and `d ≠ δ`, so NAT-order's `≤`-clause forces `d < δ`, and NAT-discrete's forward direction gives `d + 1 ≤ δ` for every `d ∈ D`. Instantiating at `d = 0 ∈ D` gives `0 + 1 ≤ δ`, which NAT-closure's left-identity reduces to `1 ≤ δ`. NAT-sub's conditional closure at `δ ≥ 1` places `δ − 1 ∈ ℕ`; NAT-sub's right-inverse `(δ − 1) + 1 = δ` and NAT-addcompat's strict successor `(δ − 1) < (δ − 1) + 1` together rewrite to `δ − 1 < δ`. Each `d ∈ D` with `d + 1 ≤ δ` yields `d ≤ δ − 1` by NAT-order's `≤`-clause split into `d + 1 = δ` and `d + 1 < δ` branches: equality via NAT-sub's right-telescoping `(d + 1) − 1 = d` gives `d = δ − 1`; strict via NAT-sub's strict monotonicity at `p = 1` gives `d < δ − 1`, with preconditions `d + 1 ≥ 1` (NAT-zero's `0 ≤ d` lifted by NAT-addcompat's right order-compatibility at `m = 1` to `0 + 1 ≤ d + 1`, then NAT-closure's left-identity to `1 ≤ d + 1`) and `δ ≥ 1` (already established). So `δ − 1 ∈ U` with `δ − 1 < δ`, contradicting minimality of δ in U. Therefore `δ ∈ D`, i.e., `δ = max(D)`.

Let P be the (unique) element of I at depth δ. Uniqueness: every allocator's ancestor chain presents exactly one node at each depth ≤ its own (parent-iteration decrements depth by 1), so `Anc(X)` and `Anc(Y)` each contribute at most one element at depth δ, and the shared element is uniquely determined.

Since X, Y are not ancestor-descendant, `X ∉ Anc(Y)` and `Y ∉ Anc(X)`, so `δ < depth(X)` and `δ < depth(Y)` — were `δ = depth(X)`, the unique ancestor of X at that depth would be X itself, putting `X ∈ I ⊆ Anc(Y)`; symmetrically. Let Cₓ be the unique ancestor of X at depth `δ + 1` (the child of P on the path to X) and Cᵧ the unique ancestor of Y at depth `δ + 1`. By maximality of δ, `Cₓ ≠ Cᵧ` — were `Cₓ = Cᵧ`, that common allocator would lie in I at depth `δ + 1`, contradicting `δ = max(D)`.

Let m be the common length of P's domain elements (T10a.1). P spawns Cₓ from `(tₓ, k'ₓ)` and Cᵧ from `(tᵧ, k'ᵧ)` with `k'ₓ, k'ᵧ ∈ {1, 2}`; the at-most-once constraint forces `(tₓ, k'ₓ) ≠ (tᵧ, k'ᵧ)`. Let `bₓ = inc(tₓ, k'ₓ)` and `bᵧ = inc(tᵧ, k'ᵧ)`.

*Base case: the branching point produces a divergence position.* Either `tₓ ≠ tᵧ` or `k'ₓ ≠ k'ᵧ`. If `tₓ ≠ tᵧ`: with `#tₓ = #tᵧ = m` (T10a.1), T3 gives some `j ≤ m` with `tₓ[j] ≠ tᵧ[j]`; TA5(b) for `k > 0` preserves these positions, so `bₓ[j] ≠ bᵧ[j]`, with `j < #bₓ` and `j < #bᵧ`. If `tₓ = tᵧ` and `k'ₓ ≠ k'ᵧ`: the conclusion `x ⋠ y ∧ y ⋠ x` is symmetric under the relabeling X ↔ Y, which swaps `Cₓ ↔ Cᵧ` and hence `k'ₓ ↔ k'ᵧ`; we relabel if necessary to assume `k'ₓ = 1`, `k'ᵧ = 2`. TA5(d) places a 1 at position `m + 1` of `bₓ` and a 0 at position `m + 1` of `bᵧ` (the zero separator preceding the final 1), so `j = m + 1` with `bₓ[j] = 1 ≠ 0 = bᵧ[j]`.

*Inductive step: divergence propagates.* Within any allocator A, the `inc(·, 0)` chain modifies only position `sig(b_A) = #b_A` (TA5(b), TA5(c); TA5-SigValid and T10a.4 give `sig(b_A) = #b_A`). Child-spawning copies positions `1..#s` into the child's base (TA5(b)), whose length exceeds `#s` (TA5(d)), so inherited positions are thereafter interior and fixed.

When `j < #bₓ`: position j differs from `sig(bₓ)`, so every element of `dom(Cₓ)` carries `bₓ[j]` at position j, and at every deeper level `#b_A > j`, so j remains interior. The value propagates unchanged through the subtree; symmetrically for Cᵧ.

When `j = #bₓ` (the case `k'ₓ = 1`, `k'ᵧ = 2`): successive elements of `dom(Cₓ)` increment position j. NAT-closure places `(tₙ)_j + 1 ∈ ℕ`, NAT-zero gives `0 ≤ (tₙ)_j`, and NAT-addcompat's strict successor gives `(tₙ)_j + 1 > (tₙ)_j ≥ 0`; the values `1, 2, 3, …` are all strictly positive. When Cₓ spawns a grandchild from `s ∈ dom(Cₓ)`, TA5(b) copies `s[j] ≥ 1` into the grandchild's base, whose length exceeds j; from that depth onward position j is interior and the positive value propagates. Every output in Cₓ's subtree has a strictly positive value at position j. On the Cᵧ side, `j = m + 1 < m + 2 = #bᵧ`, so position j is interior to Cᵧ's base; the `inc(·, 0)` chain leaves it at `bᵧ[j] = 0`, and inheritance carries 0 through every descendant.

*Closure.* For any `x ∈ dom(X)` and `y ∈ dom(Y)` we observe that `#x ≥ #bₓ` in both regimes: when `X = Cₓ`, T10a.1 gives `#x = #bₓ`; when `X` is a proper descendant of `Cₓ` (`depth(X) > depth(Cₓ)`), T10a.3 gives `#x > #bₓ`. Symmetrically `#y ≥ #bᵧ`. So `#x ≥ j` and `#y ≥ j`, and `x[j] ≠ y[j]`. Were `x ≼ y`, Prefix would require `x[j] = y[j]`, contradiction. Symmetrically `y ⋠ x`. ∎

**Consequence 6: Domain disjointness.** For an ancestor-descendant pair, T10a.1 and T10a.3 force distinct lengths across streams, so no element can lie in both. For a non-ancestor-descendant pair, T10a.5 gives prefix-incomparability, contradicted by reflexivity `t ≼ t` were `t` shared. When `same_allocator(a, b)` holds, the witnessing `A` is uniquely determined by `(a, b)` (T10a.6). Witness-uniqueness does not yet make enumeration indices single-valued; that requires Consequence 7.

**Consequence 7: Enumeration injectivity.** Within any chain `t₀, t₁, t₂, …`, the map `n ↦ tₙ` is injective. TA5(a) gives `tₙ₊₁ > tₙ`; induction via T1(c) transitivity yields `tₘ < tₙ` for `m < n`; T1(a) irreflexivity excludes `tₘ = tₙ`. Combined with Consequence 6, this makes the indices `i, j` with `a = tᵢ, b = tⱼ` single-valued functions of `(a, b)` whenever `same_allocator(a, b)` holds (T10a.7).

**Consequence 8: Uniform sibling zero count.** Every output of a conforming allocator satisfies T4 (Consequence 4), so TA5-SigValid fixes `sig(tₙ) = #tₙ` and T4 forces `(tₙ)_{#tₙ} ≠ 0`; T0 with NAT-zero and NAT-discrete sharpen this to `(tₙ)_{#tₙ} ≥ 1`. The `inc(·, 0)` step advances only that position (TA5(b), TA5(c)); NAT-closure places `(tₙ)_{sig(tₙ)} + 1 ∈ ℕ`, and NAT-addcompat's strict successor keeps it strictly positive. No position enters or leaves the zero set, and length is preserved. Every sibling shares the base's zero count (T10a.8).

**Necessity.** Relax the discipline to permit any `k ≥ 0` in the sibling stream. Let an allocator with base `b` produce `a₁ = inc(b, 0)`, then `a₂ = inc(a₁, k')` with `k' > 0`. By TA5(b), `a₂` agrees with `a₁` on every position `1 ≤ i ≤ #a₁`. By TA5(d), `#a₂ = #a₁ + k'`; with `k' ≥ 1` on ℕ (T0, NAT-zero, NAT-discrete), NAT-addcompat's strict successor and left order-compatibility sharpen this to `#a₂ > #a₁`. These are the Prefix conditions: `a₁ ≺ a₂`, falsifying T10a.2. The sibling restriction `k = 0` is therefore necessary for within-allocator prefix-incomparability (T10a-N). The remaining axiom components serve distinct purposes: `k' ∈ {1, 2}` is necessary for T4 preservation (Consequence 4, TA5a), the at-most-once constraint ensures child base-address uniqueness (Consequence 5), and the root T4 initialization seeds Consequence 4. ∎

*Formal Contract:*
- *Definitions:*
  - *Allocator tree* `𝒯`: the set of allocators induced by T10a, consisting of a root together with every allocator reachable by finite iteration of the child-spawning rule. Each non-root `A` carries a spawning triple `(parent(A), spawnPt(A), spawnParam(A))` with `parent(A) ∈ 𝒯`, `spawnPt(A) ∈ dom(parent(A))`, `spawnParam(A) ∈ {1, 2}`; `A`'s base address is `inc(spawnPt(A), spawnParam(A))`. The root's base is the T4-valid address fixed by the initialization constraint.
  - *Identity:* `X = Y` iff both are the root, or both are non-root with identical spawning triples.
  - *Derived relations:* `child`, `depth`, `ancestor`, `descendant`, *ancestor-descendant relationship*, *param-1 child* (spawnParam = 1), *param-2 child* (spawnParam = 2), *sibling allocator* (distinct children of a common parent).
  - *Domain:* `dom(A) = {tₙ : n ≥ 0}` where `t₀` is `A`'s base and `tₙ₊₁ = inc(tₙ, 0)`. Child-spawning outputs are excluded from the parent's domain and become the initial element of the child's domain.
  - *Same allocator:* `same_allocator(a, b) ≡ ∃A ∈ 𝒯 : a ∈ dom(A) ∧ b ∈ dom(A)`.
- *Axiom:* The root's base address satisfies T4. Allocators produce sibling outputs exclusively by `inc(·, 0)`; child-spawning uses one `inc(·, k')` with `k' ∈ {1, 2}`, subject to `zeros(t) ≤ 2` when `k' = 2`. Each `(t, k')` pair yields at most one child-spawning event.
- *Depends:*
  - T4 (HierarchicalParsing) — supplies the field-segment constraint (T4-validity) and the `zeros(·)` function. T10a's axiom requires the root's base to satisfy T4 and imposes `zeros(t) ≤ 2` at child-spawning step `k' = 2`; T10a.4 establishes that every conforming allocator output satisfies T4.
  - TA5 (HierarchicalIncrement) — supplies the `inc` operator, positional agreement under `k > 0` (TA5(b)), length preservation under `k = 0` (TA5(c)), strict order `inc(t, k) > t` (TA5(a)), and length increment by `k` (TA5(d)). Threaded through every consequence and the necessity argument.
  - TA5a (IncrementPreservesT4) — supplies the T4-preservation envelope: unconditional under `inc(·, 0)` and `inc(·, 1)` on T4-valid inputs, conditional under `inc(·, 2)` when `zeros(t) ≤ 2`. Drives T10a.4's induction step.
  - Prefix (PrefixRelation) — supplies the prefix relation `≼` and its positional-agreement clause. Used in T10a.2's collapse of sibling prefix-relation to equality and in T10a.5's closure step contradicting `x ≼ y` from a divergence position.
  - T3 (CanonicalRepresentation) — collapses equal-length positional agreement to identity. Used in T10a.2 to rule out distinct equal-length siblings being prefix-related, and in T10a.5's base case to extract a divergence position from `tₓ ≠ tᵧ` at common length `m`.
  - T0 — fixes the carrier ℕ as the index domain for tumbler positions and the spawn parameter `k' ∈ {1, 2}`. Underpins ℕ-typed quantification throughout.
  - NAT-addcompat (NatAdditionOrderAndSuccessor) — supplies the strict successor `n < n + 1`, left order-compatibility on `<`, and right order-compatibility `p ≤ n ⟹ p + m ≤ n + m`. Used in T10a.3's length-separation chain (`#t < #t + 1 ≤ #t + k'`), in T10a-N's necessity argument, in T10a.8's positivity propagation, and in T10a.5's LCA-existence argument (right order-compatibility lifts NAT-zero's `0 ≤ d` at `m = 1` to `0 + 1 ≤ d + 1`, supplying NAT-sub strict monotonicity's `d + 1 ≥ 1` precondition).
  - NAT-zero (NatZeroMinimum) — supplies `0 ≤ n` for `n ∈ ℕ`. Used in T10a.3 to lift `k' > 0` to `1 ≤ k'`, in T10a.5 / T10a.8 to ground positivity in the divergence and zero-count arguments, and in T10a.5's LCA-existence to ground `0 ≤ d` for the right-order-compatibility lift to `1 ≤ d + 1`.
  - NAT-discrete (NatDiscreteness) — sharpens `n > 0` to `n ≥ 1` on ℕ; supplies the forward direction `d < δ ⟹ d + 1 ≤ δ`. Used in T10a.3 and T10a-N to obtain `1 ≤ k'` from `k' > 0`, in T10a.8 to derive `(tₙ)_{#tₙ} ≥ 1`, and in T10a.5's LCA-existence to lift `d ≠ δ` (combined with `d ≤ δ`) into `d + 1 ≤ δ` for every `d ∈ D`.
  - NAT-closure (NatArithmeticClosureAndIdentity) — supplies addition closure (`n + 1 ∈ ℕ`) and the literal `1 ∈ ℕ`. Used in T10a.5 and T10a.8 to keep successor-positivity arguments inside ℕ, and in T10a.5's LCA-existence to collapse `0 + 1 = 1` (left-identity) at two sites — discharging `0 + 1 ≤ δ ⟹ 1 ≤ δ` and `0 + 1 ≤ d + 1 ⟹ 1 ≤ d + 1`.
  - NAT-sub (NatPartialSubtraction) — supplies conditional closure `δ ≥ 1 ⟹ δ − 1 ∈ ℕ`, right-inverse `(δ − 1) + 1 = δ`, right-telescoping `(d + 1) − 1 = d`, and strict monotonicity at `p = 1`. Used in T10a.5's LCA-existence: closure produces `δ − 1 ∈ ℕ`; the right-inverse fed into NAT-addcompat's strict successor delivers `δ − 1 < δ`; right-telescoping handles the `d + 1 = δ` branch (`d = δ − 1`) and strict monotonicity handles the `d + 1 < δ` branch (`d < δ − 1`); together they place `δ − 1 ∈ U` and contradict δ's minimality in U.
  - NAT-wellorder (NatWellOrdering) — least-element principle: every nonempty `S ⊆ ℕ` has a least element. Used in T10a.5's LCA-existence: applied to the upper-bound set `U = {u ∈ ℕ : (A d ∈ D :: d ≤ u)}` of the depth-set `D = {depth(A) : A ∈ Anc(X) ∩ Anc(Y)}`, it delivers a least element δ; the TA5-SIG-pattern minimality contradiction places δ ∈ D, making `δ = max(D)` and locating the LCA P as the unique element of `Anc(X) ∩ Anc(Y)` at depth δ.
  - TA5-SigValid — fixes `sig(t) = #t` for T4-valid tumblers. Used in T10a.5 to identify which positions `inc(·, 0)` modifies and in T10a.8 to localize the zero-count argument to position `#tₙ`.
  - T1 (LexicographicOrder) — supplies irreflexivity (T1(a)) and transitivity (T1(c)) of `<`. Used in T10a.7 to derive injectivity of `n ↦ tₙ` from successor strict-positivity.
  - NAT-order (NatStrictTotalOrder) — supplies trichotomy on ℕ and the `≤`-defining clause `m ≤ n ⟺ m < n ∨ m = n`. Used in T10a.7 to resolve `m ≠ n` into `m < n ∨ n < m` for the injectivity argument, and in T10a.5's LCA-existence to split `d ≤ δ ∧ d ≠ δ` into `d < δ` (driving NAT-discrete's forward direction) and to split `d + 1 ≤ δ` into the `d + 1 = δ` and `d + 1 < δ` branches that NAT-sub dispatches.
- *Postconditions:*
  - T10a.1 (Uniform sibling length): For every allocator with base `b`, all sibling outputs `a` satisfy `#a = #b`.
  - T10a.2 (Non-nesting sibling prefixes): For all siblings `a, b` from the same allocator, `same_allocator(a, b) ∧ a ≠ b → a, b` prefix-incomparable.
  - T10a.3 (Length separation): For every child allocator spawned by `inc(·, k')` with `k' ∈ {1, 2}` from a parent with base length `m`, all child outputs `c` satisfy `#c = m + k'`; across `d` nesting levels the separation is `m + k'₁ + … + k'_d`. For any proper ancestor-descendant pair `(A, B)` — pairs where A is an ancestor of B with A ≠ B (whence `depth(A) < depth(B)`; the converse fails, as allocators in independent subtrees can satisfy `depth(A) < depth(B)` without any ancestor-descendant relationship) — `∀b ∈ dom(B), ∀a ∈ dom(A) : #b > #a`.
  - T10a.4 (T4 preservation): Every output of a conforming allocator satisfies T4.
  - T10a.5 (Cross-allocator prefix-incomparability): For allocators X, Y not in an ancestor-descendant relationship, for all `x ∈ dom(X)`, `y ∈ dom(Y)`, `x ⋠ y ∧ y ⋠ x`. (The ancestor-descendant case carries only a narrower nesting fact, not universal pairwise comparability between domains: at each spawning event `(tᵢ, k')` with `tᵢ ∈ dom(parent)`, `tᵢ ≺ c` for every `c` in the spawned child's domain and, transitively, for every `c` in any descendant allocator's domain whose chain of spawning events passes through `tᵢ`. Elements of `dom(parent)` other than the spawn point `tᵢ` need not be prefix-comparable to descendant domain elements.)
  - T10a.6 (Domain disjointness): For distinct X, Y, `dom(X) ∩ dom(Y) = ∅`. Ancestor-descendant case by T10a.1 + T10a.3; non-ancestor-descendant case by T10a.5 + Prefix reflexivity. Witness-uniqueness corollary: `same_allocator(a, b)` determines the witnessing A uniquely.
  - T10a.7 (Enumeration injectivity): For every allocator A, `n ↦ tₙ` is injective.
  - T10a.8 (Uniform sibling zero count): For every allocator with base `b`, all siblings `a` satisfy `zeros(a) = zeros(b)`.
  - T10a-N (Necessity of sibling restriction): Under the relaxed rule, `a₁ = inc(b, 0)` and `a₂ = inc(a₁, k')` with `k' > 0` satisfy `a₁ ≺ a₂`, falsifying T10a.2. The sibling restriction `k = 0` is necessary for T10a.2. The `k' ∈ {1, 2}` bound, at-most-once constraint, and root initialization serve T4 preservation and child-prefix uniqueness respectively.

**T10a.1 (UniformSiblingLength).** All siblings produced by a single allocator have the same length as its base address.

Let an allocator have base address `t₀` and produce siblings by repeated application of `inc(·, 0)`: define `tₙ₊₁ = inc(tₙ, 0)` for `n ≥ 0`. We prove `#tₙ = #t₀` for all `n ≥ 0` by induction on `n`.

*Base case.* `n = 0`: `#t₀ = #t₀` holds trivially.

*Inductive step.* Assume `#tₙ = #t₀`. By TA5(c), `#inc(tₙ, 0) = #tₙ`, so `#tₙ₊₁ = #tₙ`. By the inductive hypothesis, `#tₙ₊₁ = #t₀`. ∎

*Formal Contract:*
- *Precondition:* Allocator with base address `t₀`, producing siblings by `inc(·, 0)`.
- *Postcondition:* `(A n ≥ 0 : #tₙ = #t₀)`.
- *Depends:*
  - T10a (AllocatorDiscipline) — supplies base address `t₀` and sibling recurrence `tₙ₊₁ = inc(tₙ, 0)`.
  - TA5 (HierarchicalIncrement), postcondition (c) — `#inc(t, 0) = #t`, the per-step length preservation.

**T10a.2 (NonNestingSiblingPrefixes).** Distinct siblings from the same allocator are prefix-incomparable: `tᵢ ⋠ tⱼ ∧ tⱼ ⋠ tᵢ`.

Let `tᵢ` and `tⱼ` be distinct siblings from the same allocator — distinct as tumblers, `tᵢ ≠ tⱼ`. By T10a.1, `#tᵢ = #tⱼ`.

Suppose for contradiction that `tᵢ ≼ tⱼ`. By Prefix, `#tᵢ ≤ #tⱼ` and `(A k : 1 ≤ k ≤ #tᵢ : (tⱼ)ₖ = (tᵢ)ₖ)`. Since `#tᵢ = #tⱼ`, the range `1 ≤ k ≤ #tᵢ` exhausts both tumblers. By T3, equal-length positional agreement gives `tᵢ = tⱼ`, contradicting `tᵢ ≠ tⱼ`. The symmetric argument excludes `tⱼ ≼ tᵢ`.

Therefore `tᵢ ⋠ tⱼ ∧ tⱼ ⋠ tᵢ`. ∎

*Formal Contract:*
- *Precondition:* `tᵢ`, `tⱼ` are distinct siblings from the same allocator (`tᵢ ≠ tⱼ` as tumblers).
- *Postcondition:* `tᵢ ⋠ tⱼ ∧ tⱼ ⋠ tᵢ`.
- *Depends:*
  - T10a (AllocatorDiscipline) — sibling production uses only `inc(·, 0)`, fixing the "same allocator" regime.
  - T10a.1 (UniformSiblingLength) — `#tᵢ = #tⱼ`.
  - Prefix (PrefixRelation) — positional-agreement conjunct of `≼`.
  - T3 (CanonicalRepresentation) — `#a = #b ∧ (A i : 1 ≤ i ≤ #a : aᵢ = bᵢ) ≡ a = b`.

**T10a.3 (LengthSeparation).** Child allocator outputs have strictly greater length than any parent sibling output, with additive separation across nesting levels.

Let a parent allocator have base address `t₀` with sibling length `γ = #t₀`. When the parent spawns a child via `inc(t, k')` with `k' ∈ {1, 2}`, the child's base address `c₀` has length `#c₀ = #t + k'` by TA5(d). Since `t` is a parent sibling, `#t = γ` by T10a.1, so `#c₀ = γ + k'`.

The child allocator produces its own siblings by `inc(·, 0)`. By T10a.1 applied to the child, all child outputs have uniform length `γ + k'`. Since `k' ∈ {1, 2}` places `k'` on ℕ with `k' > 0` (T0), NAT-zero supplies `0 ∈ ℕ` and the minimum reading `¬(n < 0)`, and NAT-discrete instantiated at `m = 0` sharpens `k' > 0` to `1 ≤ k'` (the same sharpening T10a's Consequence 3 performs on this parameter); NAT-addcompat's strict successor at `n = γ` then gives `γ < γ + 1`, and left order-compatibility at `m = γ, p = 1, n = k'` lifts `1 ≤ k'` to `γ + 1 ≤ γ + k'`. NAT-order's mixed `<`-`≤` transitivity chains the two to `γ < γ + k'`, which NAT-order's companion `m > n ⟺ n < m` presents as `γ + k' > γ`: every child output has length strictly greater than `γ`. By T3, tumblers of different lengths are distinct, so no child output equals any parent sibling.

For additive nesting, consider a lineage where at depth `i` the child is spawned by `inc(·, k'_i)` with `k'_i ∈ {1, 2}`. By induction on `d`, the descendant at depth `d` has sibling length `γ + k'₁ + … + k'_d`. Strict increase with depth follows at each boundary from NAT-addcompat's strict successor at `n = γ + k'₁ + … + k'_d` and left order-compatibility lifting `1 ≤ k'_{d+1}`. By T3, outputs at different depths along a lineage never collide.

The running-sum bound `k'₁ + … + k'_d ≥ d` is proved by induction on `d`. Base `d = 1`: `k'₁ ≥ 1`. Step: assume `k'₁ + … + k'_i ≥ i`; NAT-addcompat right order-compatibility at `n = k'₁ + … + k'_i, p = i, m = k'_{i+1}` gives `k'₁ + … + k'_{i+1} ≥ i + k'_{i+1}`, and left order-compatibility at `m = i, p = 1, n = k'_{i+1}` gives `i + 1 ≤ i + k'_{i+1}`; NAT-order's `≤`-transitivity — instantiated at `m = i + 1, n = i + k'_{i+1}, p = k'₁ + … + k'_{i+1}`, with the right-hand bound `i + k'_{i+1} ≤ k'₁ + … + k'_{i+1}` read off from `k'₁ + … + k'_{i+1} ≥ i + k'_{i+1}` via the `≥`/`≤` companion — yields `i + 1 ≤ k'₁ + … + k'_{i+1}`, i.e., `k'₁ + … + k'_{i+1} ≥ i + 1`. Left order-compatibility at `m = γ` delivers `γ + d ≤ γ + k'₁ + … + k'_d`.

*Local monotonicity.* For ancestor A at depth `d_A` and descendant B at depth `d_B > d_A` on the same lineage: by T10a.1, `#output(A) = γ + k'₁ + … + k'_{d_A}` and `#output(B) = γ + k'₁ + … + k'_{d_B}`. Iterated NAT-addassoc regroups the left-associated accumulation `γ + k'₁ + … + k'_{d_B}` at the depth-`d_A` boundary into `(γ + k'₁ + … + k'_{d_A}) + (k'_{d_A+1} + … + k'_{d_B})`, identifying `#output(B) = #output(A) + (k'_{d_A+1} + … + k'_{d_B})`. NAT-sub's conditional-closure at `m = d_B, n = d_A` places `d_B − d_A ∈ ℕ`; NAT-sub's strict-positivity clause `(A m, n ∈ ℕ : m > n : m − n ≥ 1)` at the same instantiation lifts the strict inequality `d_B > d_A` directly to `d_B − d_A ≥ 1` — it is the strict-positivity clause, not a `[0, 1)`-collapse via discreteness, that excludes `d_B − d_A = 0` here. Iterated NAT-addcompat order-compatibility across the `d_B − d_A` terms lifts each `1 ≤ k'_i` to `k'_{d_A+1} + … + k'_{d_B} ≥ d_B − d_A`. NAT-addcompat's strict successor at `n = #output(A)` gives `#output(A) < #output(A) + 1`, and left order-compatibility at `m = #output(A), p = 1, n = k'_{d_A+1} + … + k'_{d_B}` lifts `1 ≤ k'_{d_A+1} + … + k'_{d_B}` (read off from `k'_{d_A+1} + … + k'_{d_B} ≥ d_B − d_A ≥ 1` via NAT-order's `≥`/`≤` companion) to `#output(A) + 1 ≤ #output(A) + (k'_{d_A+1} + … + k'_{d_B})`; NAT-order's mixed `<`-`≤` transitivity chains them to `#output(A) < #output(A) + (k'_{d_A+1} + … + k'_{d_B})`, which the NAT-addassoc regrouping identifies with `#output(A) < #output(B)`. NAT-sub's left-telescoping at `n = #output(A), m = k'_{d_A+1} + … + k'_{d_B}` gives `(#output(A) + (k'_{d_A+1} + … + k'_{d_B})) − #output(A) = k'_{d_A+1} + … + k'_{d_B}`, which the same regrouping identifies as `#output(B) − #output(A) = k'_{d_A+1} + … + k'_{d_B}`. ∎

*Formal Contract:*
- *Precondition:* Parent allocator with sibling length `γ`; `t` is a parent sibling (`#t = γ` by T10a.1); child spawned via `inc(t, k')` with `k' ∈ {1, 2}`.
- *Postcondition:* All child outputs have length `γ + k' > γ`; no child output equals any parent sibling. Descendant at depth `d` along a lineage with parameters `k'₁, …, k'_d` has output length `γ + k'₁ + … + k'_d ≥ γ + d`; cumulative length is strictly increasing with depth, so outputs at different depths never collide. Local monotonicity: for ancestor A at depth `d_A` and descendant B at depth `d_B > d_A` on the same lineage, `#output(B) − #output(A) = k'_{d_A+1} + … + k'_{d_B} ≥ d_B − d_A ≥ 1`.
- *Depends:*
  - T10a (AllocatorDiscipline) — restricts child-spawning to `inc(·, k')` with `k' ∈ {1, 2}`.
  - T10a.1 (UniformSiblingLength) — uniform length `γ` for parent siblings and `γ + k'₁ + … + k'_d` for depth-`d` outputs.
  - TA5 (HierarchicalIncrement) — (c) `#inc(t, 0) = #t`; (d) `#inc(t, k') = #t + k'` for `k' > 0`.
  - T0 (CarrierSetDefinition) — carrier is ℕ; types all length terms, sums, and depth differences for NAT-* instantiations.
  - NAT-order (NatStrictTotalOrder) — supplies the companion definitions `m > n ⟺ n < m` and `m ≥ n ⟺ n ≤ m` (presenting the child-length conclusion as `γ + k' > γ` in paragraph 2, and the local-monotonicity intermediates `k'_{d_A+1} + … + k'_{d_B} ≥ d_B − d_A ≥ 1` and `#output(B) − #output(A) ≥ 1` in `≥`-form); transitivity of `<` together with the mixed `<`-`≤` chain `m < n ∧ n ≤ p ⟹ m < p` (consumed at paragraph 2's chaining step to combine NAT-addcompat's `γ < γ + 1` with `γ + 1 ≤ γ + k'` into `γ < γ + k'`, and again in local monotonicity to combine `#output(A) < #output(A) + 1` with `#output(A) + 1 ≤ #output(A) + (k'_{d_A+1} + … + k'_{d_B})` into `#output(A) < #output(A) + (k'_{d_A+1} + … + k'_{d_B})`); `≤`-transitivity (consumed at the running-sum induction's inductive step to chain `i + 1 ≤ i + k'_{i+1}` with `i + k'_{i+1} ≤ k'₁ + … + k'_{i+1}` — read off via the `≥`/`≤` companion from `k'₁ + … + k'_{i+1} ≥ i + k'_{i+1}` — into `i + 1 ≤ k'₁ + … + k'_{i+1}`, i.e., `k'₁ + … + k'_{i+1} ≥ i + 1`).
  - NAT-addcompat (NatAdditionOrderAndSuccessor) — strict successor `n < n + 1` and order-compatibility of addition.
  - NAT-addassoc (NatAdditionAssociative) — iterated regrouping of the left-associated accumulation `γ + k'₁ + … + k'_{d_B}` at the depth-`d_A` boundary identifies `(γ + k'₁ + … + k'_{d_A}) + (k'_{d_A+1} + … + k'_{d_B}) = γ + k'₁ + … + k'_{d_B}`, i.e., `#output(A) + (k'_{d_A+1} + … + k'_{d_B}) = #output(B)`; this premise is consumed at two sites in the local-monotonicity derivation — the strict-inequality step lifts NAT-addcompat's `#output(A) < #output(A) + (k'_{d_A+1} + … + k'_{d_B})` to `#output(A) < #output(B)`, and the left-telescoping step rewrites `(#output(A) + (k'_{d_A+1} + … + k'_{d_B})) − #output(A) = k'_{d_A+1} + … + k'_{d_B}` as `#output(B) − #output(A) = k'_{d_A+1} + … + k'_{d_B}`.
  - NAT-sub (NatPartialSubtraction) — conditional closure (places `d_B − d_A ∈ ℕ`), strict positivity `m > n ⟹ m − n ≥ 1` (lifts `d_B > d_A` to `d_B − d_A ≥ 1` without recourse to a `[0, 1)`-collapse), and left telescoping `(n + m) − n = m` (instantiated at `n = #output(A), m = k'_{d_A+1} + … + k'_{d_B}` to compute the exact difference; right-telescoping is avoided because the NAT-addassoc regrouping delivers the sum in the order `#output(A) + (k'_{d_A+1} + … + k'_{d_B})`, matching left-telescoping's premise without an unstated commutativity step).
  - NAT-zero (NatZeroMinimum) — supplies `0 ∈ ℕ` (so NAT-discrete can be instantiated at `m = 0`) and the minimum reading `¬(n < 0)`; together with NAT-discrete, sharpens the spawning-parameter fact `k' > 0` (from `k' ∈ {1, 2}`) to `1 ≤ k'` — the form NAT-addcompat's left order-compatibility consumes at each spawning step, including the per-step `1 ≤ k'_i` reused in the lineage induction and local-monotonicity derivation.
  - NAT-discrete (NatDiscreteness) — discreteness of ℕ: `m < n ⟹ m + 1 ≤ n`; instantiated at `m = 0` to sharpen `k' > 0` to `1 ≤ k'`, feeding every NAT-addcompat left order-compatibility lift across the spawning parameters `k', k'_i` (paragraphs 2–5).
  - T3 (CanonicalRepresentation) — tumblers of different lengths are distinct.

**T10a.4 (T4Preservation).** The allocator discipline produces only T4-compliant addresses.

*Proof.* By induction on the allocator tree, with strengthened hypothesis: for every allocator `A` at depth `d`, every `t ∈ dom(A)` is T4-valid. The strengthening is what licenses applying TA5a at a spawning point `t ∈ dom(A)` that need not be `A`'s base; T10a permits `spawnPt(A)` to be any element of `dom(parent(A))`, so the original-proof shortcut of writing the child's base as `inc(b, k')` with `b` the parent's base is literally false whenever spawning occurs past the first sibling.

*Base case (`d = 0`).* The root allocator's base `t₀` satisfies T4 by the initialization constraint of T10a. Its domain is the chain `t₀, t₁ = inc(t₀, 0), t₂ = inc(t₁, 0), …`; TA5a's `k = 0` branch preserves T4 unconditionally on T4-valid inputs, so induction on the chain index gives every `tₙ ∈ dom(root)` T4-valid.

*Inductive step.* Assume the hypothesis at depth `≤ d`. Let `A` be at depth `d + 1`, spawned from `P = parent(A)` at `t = spawnPt(A) ∈ dom(P)` with `spawnParam(A) = k' ∈ {1, 2}`; by T10a, `A`'s base is `t₀ = inc(t, k')`. The inductive hypothesis applied to `P` gives `t` T4-valid — this is the step that requires the strengthened hypothesis rather than merely `P`'s base being T4-valid, since `t` need not equal `P`'s base.

Apply TA5a at `t`:

- *Case `k' = 1`.* TA5a's `k = 1` branch preserves T4 unconditionally on T4-valid inputs, so `inc(t, 1)` satisfies T4.
- *Case `k' = 2`.* TA5a's `k = 2` branch preserves T4 under `zeros(t) ≤ 2`. T10a states its runtime precondition on the spawning point `t` (not on `P`'s base), so the guard `zeros(t) ≤ 2` holds at the very element where TA5a is applied, and `inc(t, 2)` satisfies T4.

In either case `A`'s base `t₀ = inc(t, k')` is T4-valid. The sibling chain `t₀, t₁ = inc(t₀, 0), …` within `dom(A)` then propagates T4 by TA5a's `k = 0` branch exactly as in the base case, so every `t ∈ dom(A)` is T4-valid, closing the induction. ∎

*Formal Contract:*
- *Preconditions:* Allocator tree conforming to T10a; root base address satisfies T4.
- *Postconditions:* For every allocator `A` in the tree and every `t ∈ dom(A)`, `t` satisfies T4. In particular, every address produced at every depth satisfies T4.
- *Proof structure:* Induction on allocator tree depth with strengthened hypothesis — every `t ∈ dom(A)` is T4-valid, not only `A`'s base. Base: root's sibling chain via TA5a `k = 0`. Step: child's base `inc(t, k')` is T4-valid because the strengthened hypothesis supplies `t` T4-valid at the spawning point `t = spawnPt(A) ∈ dom(parent(A))`, TA5a gives preservation for `k' ∈ {1, 2}`, and T10a's `zeros(t) ≤ 2` guard fires at that same `t` when `k' = 2`; the child's sibling chain then propagates T4 via TA5a `k = 0`.
- *Depends:*
  - T10a (AllocatorDiscipline) — root-initialization constraint; spawning rule `spawnPt(A) ∈ dom(parent(A))` and child-base `inc(spawnPt(A), spawnParam(A))`; runtime precondition `zeros(t) ≤ 2` at `k' = 2` stated on the spawning point `t`.
  - T4 (HierarchicalParsing) — invariant preserved by induction.
  - TA5a (IncrementPreservesT4) — per-step preservation: `inc(·, 0)` and `inc(·, 1)` preserve T4 unconditionally on T4-valid inputs; `inc(·, 2)` preserves T4 under `zeros(t) ≤ 2` at the input `t`.

**T10a.5 (CrossAllocatorIncomparability).** For any two allocators X and Y not in an ancestor-descendant relationship, every output of X is prefix-incomparable with every output of Y. This supplies T10's non-nesting precondition `p₁ ⋠ p₂ ∧ p₂ ⋠ p₁` at the domain prefixes of every non-ancestor-descendant allocator pair. (The ancestor-descendant case carries a narrower nesting fact, not universal pairwise comparability between domains: at each spawning event `(tᵢ, k')`, TA5(b) gives agreement on positions `1, …, #tᵢ` and TA5(d) gives `#inc(tᵢ, k') = #tᵢ + k'`; since `k' ∈ {1, 2}`, NAT-addcompat's strict successor `n < n + 1` and left order-compatibility sharpen this to `#inc(tᵢ, k') > #tᵢ`, so `tᵢ ≺ inc(tᵢ, k')`. TA5(b) also keeps positions `1, …, #tᵢ` fixed throughout the spawned child's domain and every descendant allocator traced through `tᵢ`, so `tᵢ ≺ c` for every such `c`; elements of `dom(parent)` other than `tᵢ` need not be prefix-comparable to descendant domain elements.)

*Proof.* Let X and Y be allocators not in an ancestor-descendant relationship.

*Existence of a lowest common ancestor.* The ancestor relation makes `Anc(X) = {A ∈ 𝒯 : A is an ancestor of X}` include the root: parent-iteration from X strictly decreases depth (`depth(B) = depth(parent(B)) + 1` for non-root B) and terminates at root since depth ∈ ℕ blocks unbounded descent. Symmetrically `root ∈ Anc(Y)`, making `I = Anc(X) ∩ Anc(Y)` nonempty.

The depth-set `D = {depth(A) : A ∈ I} ⊆ ℕ` is nonempty (contains `0 = depth(root)`) and bounded above by `depth(X)`: every `A ∈ I` lies in `Anc(X)`, so the chain from A to X yields `depth(A) ≤ depth(X)` (each step adds 1, terminating at `depth(X)`).

NAT-wellorder supplies `max(D)` by the upper-bound construction (the same pattern by which TA5-SIG extracts `max` from NAT-wellorder). Form `U = {u ∈ ℕ : (A d ∈ D :: d ≤ u)}`; `depth(X) ∈ U`, so `U ≠ ∅`. NAT-wellorder applied to U delivers a least element, name it δ. Suppose `δ ∉ D`: every `d ∈ D` satisfies `d ≤ δ` (from `δ ∈ U`) and `d ≠ δ`, so NAT-order's `≤`-clause `d ≤ δ ⟺ d < δ ∨ d = δ` forces `d < δ`, and NAT-discrete's forward direction gives `d + 1 ≤ δ` for every `d ∈ D`. Instantiating at `d = 0 ∈ D` gives `0 + 1 ≤ δ`, which NAT-closure's left-identity reduces to `1 ≤ δ`. NAT-sub's conditional closure at `δ ≥ 1` places `δ − 1 ∈ ℕ`; NAT-sub's right-inverse `(δ − 1) + 1 = δ` and NAT-addcompat's strict successor `(δ − 1) < (δ − 1) + 1` together rewrite to `δ − 1 < δ`. Each `d ∈ D` with `d + 1 ≤ δ` yields `d ≤ δ − 1` by NAT-order's `≤`-clause split into the `d + 1 = δ` and `d + 1 < δ` branches: in the equality branch, NAT-sub's right-telescoping `(d + 1) − 1 = d` gives `d = δ − 1`; in the strict branch, NAT-sub's strict monotonicity at `p = 1` gives `d < δ − 1`, with preconditions `d + 1 ≥ 1` (NAT-zero's `0 ≤ d` lifted by NAT-addcompat's right order-compatibility at `m = 1` to `0 + 1 ≤ d + 1`, then NAT-closure's left-identity to `1 ≤ d + 1`) and `δ ≥ 1` (already established). So `δ − 1 ∈ U` with `δ − 1 < δ`, contradicting minimality of δ in U. Therefore `δ ∈ D`, i.e., `δ = max(D)`.

Let C be the (unique) element of I at depth δ. Uniqueness: every allocator's ancestor chain presents exactly one node at each depth ≤ its own (parent-iteration decrements depth by 1), so `Anc(X)` and `Anc(Y)` each contribute at most one element at depth δ, and the shared element is uniquely determined.

Since X, Y are not ancestor-descendant, `X ∉ Anc(Y)` and `Y ∉ Anc(X)`, so `δ < depth(X)` and `δ < depth(Y)` — were `δ = depth(X)`, the unique ancestor of X at that depth would be X itself, putting `X ∈ I ⊆ Anc(Y)`; symmetrically. Let C_X be the unique ancestor of X at depth `δ + 1` (the child of C on the path to X; `C_X = X` when `depth(X) = δ + 1`) and C_Y the unique ancestor of Y at depth `δ + 1`. By maximality of δ, `C_X ≠ C_Y` — were `C_X = C_Y`, that common allocator would lie in I at depth `δ + 1`, contradicting `δ = max(D)`.

Let s_X be the output of C from which C_X was spawned, and s_Y the output from which C_Y was spawned.

We require a preliminary fact.

**Positional inheritance.** Let allocator A have base b of length m, and let p be a position with 1 ≤ p < m. Then every output of every allocator in the subtree rooted at A has value b_p at position p.

For A itself: every output has length m by T10a.1, and inc(·, 0) modifies only position sig(·) = m (by TA5-SigValid, since every output satisfies T4 by T10a.4). Since p < m, position p is unmodified: every output of A has value b_p at position p. For a child of A spawned from output u via inc(u, k'') with k'' ∈ {1, 2}: the child's base c has length m + k'' and agrees with u on positions 1 through m by TA5(b). Since u_p = b_p, c_p = b_p. Since p < m < m + k'', position p satisfies p < #c, and the argument applies to the child's subtree. By induction on subtree depth, every output of every descendant has value b_p at position p. ∎ (positional inheritance)

**Case 1: s_X ≠ s_Y.** Both are sibling outputs of C, so #s_X = #s_Y = L by T10a.1. Since s_X ≠ s_Y and both have length L, T3 yields a position j with 1 ≤ j ≤ L where (s_X)_j ≠ (s_Y)_j.

The base of C_X is inc(s_X, k'_X) for some k'_X ∈ {1, 2}, which has length L + k'_X and agrees with s_X on positions 1 through L by TA5(b). Since j ≤ L < L + k'_X, positional inheritance gives: every output in C_X's subtree has value (s_X)_j at position j. The base of C_Y is inc(s_Y, k'_Y) for some k'_Y ∈ {1, 2}, and symmetrically every output in C_Y's subtree has value (s_Y)_j at position j.

For any output x of X and y of Y: x_j = (s_X)_j ≠ (s_Y)_j = y_j. Every output in C_X's subtree has length at least L + 1 (by T10a.1 for C_X's own outputs and T10a.3 for deeper descendants); the same for C_Y. So j ≤ L < L + 1 ≤ min(#x, #y). The disagreement at position j excludes both x ≼ y and y ≼ x by the Prefix definition. ∎ (Case 1)

**Case 2: s_X = s_Y = s.** The at-most-once child-spawning constraint of T10a requires that each (t, k') pair produces at most one child. Since C_X ≠ C_Y are both spawned from s, they must use distinct spawning parameters: k'_X ≠ k'_Y with {k'_X, k'_Y} ⊆ {1, 2}. The T10a.5 postcondition is invariant under the exchange (X, Y) ↔ (Y, X), so assume k'_X = 1 and k'_Y = 2.

The base of C_X is inc(s, 1), which has length #s + 1 with (inc(s, 1))_{#s+1} = 1 by TA5(d). The base of C_Y is inc(s, 2), which has length #s + 2 with (inc(s, 2))_{#s+1} = 0 and (inc(s, 2))_{#s+2} = 1 by TA5(d).

We show that every output in C_X's subtree has value ≥ 1 at position #s + 1, while every output in C_Y's subtree has value 0 there.

*Outputs of C_X at position #s + 1.* Position #s + 1 is the last position of C_X's outputs (length #s + 1 by T10a.1). Enumerate C_X's outputs as `t₀, t₁, t₂, …` with `t₀` the base and `tₙ₊₁ = inc(tₙ, 0)`. We prove `(tₙ)_{#s+1} ≥ 1` by induction on `n`. *Base case* `n = 0`: `(t₀)_{#s+1} = 1` by TA5(d). *Inductive step.* Assume `(tₙ)_{#s+1} ≥ 1`. Every output of C_X satisfies T4 (T10a.4), so TA5-SigValid gives `sig(tₙ) = #tₙ = #s + 1`, and TA5(c) yields `(tₙ₊₁)_{#s+1} = (tₙ)_{#s+1} + 1`. T0 places `(tₙ)_{#s+1} ∈ ℕ`; NAT-closure places `(tₙ)_{#s+1} + 1 ∈ ℕ`; NAT-zero gives `0 ≤ (tₙ)_{#s+1}`; NAT-addcompat's strict successor gives `(tₙ)_{#s+1} + 1 > (tₙ)_{#s+1} ≥ 0`; NAT-discrete (at `m = 0`) with NAT-zero's `0 ≤ (tₙ)_{#s+1} + 1` rules out `0 ≤ (tₙ)_{#s+1} + 1 < 1`, forcing `(tₙ)_{#s+1} + 1 ≥ 1`.

*Descendants of C_X at position #s + 1.* Any child of C_X is spawned from an output u with u_{#s+1} ≥ 1. The child's base has length #s + 1 + k'' ≥ #s + 2 for some k'' ∈ {1, 2}, and agrees with u on positions 1 through #s + 1 by TA5(b), inheriting value ≥ 1 at position #s + 1. Since #s + 1 < #s + 1 + k'', positional inheritance propagates this through the child's subtree. By induction on depth, every output in C_X's subtree has value ≥ 1 at position #s + 1.

*All outputs in C_Y's subtree at position #s + 1.* The base of C_Y has value 0 at position #s + 1, and #s + 1 < #s + 2 — T4's *Numerals* definition `2 := 1 + 1` rewrites `#s + 2 = #s + (1 + 1)`, NAT-addassoc at `(#s, 1, 1)` regroups this to `(#s + 1) + 1`, and NAT-addcompat's strict successor at `n = #s + 1` gives `#s + 1 < (#s + 1) + 1 = #s + 2`. Positional inheritance gives: every output in C_Y's subtree has value 0 at position #s + 1.

For any output x of X and y of Y: x_{#s+1} ≥ 1 and y_{#s+1} = 0. Every output in C_X's subtree has length ≥ #s + 1, and every output in C_Y's subtree has length ≥ #s + 2, so position #s + 1 lies within the range of both x and y. The disagreement excludes both x ≼ y and y ≼ x by the Prefix definition. ∎

*Formal Contract:*
- *Precondition:* Allocators X and Y conforming to T10a, not in an ancestor-descendant relationship.
- *Postcondition:* For all x ∈ dom(X) and y ∈ dom(Y): x ⋠ y ∧ y ⋠ x.
- *Depends:*
  - T10a — at-most-once child-spawning constraint; k' ∈ {1, 2}.
  - T10a.1 — uniform sibling length.
  - T10a.3 — length separation across depths.
  - T10a.4 — T4 preservation (enables TA5-SigValid).
  - T4 (HierarchicalParsing) — TA5-SigValid precondition.
  - T3 — distinct same-length tumblers diverge at some position.
  - TA5 — postconditions (b), (c), (d).
  - TA5-SigValid — sig = length for T4-valid addresses.
  - T0 (CarrierSetDefinition) — fixes carrier as ℕ.
  - NAT-closure (NatArithmeticClosureAndIdentity) — addition closure with `1 ∈ ℕ` from the same axiom places `n + 1 ∈ ℕ` for the `+1` steps.
  - NAT-zero (NatZeroMinimum) — lower bound `0 ≤ n`.
  - NAT-addcompat (NatAdditionOrderAndSuccessor) — strict successor `n < n + 1`, left order-compatibility `p ≤ n ⟹ m + p ≤ m + n`, and right order-compatibility `p ≤ n ⟹ p + m ≤ n + m` (the right form is consumed in the LCA-existence argument: NAT-zero's `0 ≤ d` is lifted at `m = 1` to `0 + 1 ≤ d + 1`, which NAT-closure's left-identity reduces to `1 ≤ d + 1`, supplying the `d + 1 ≥ 1` precondition of NAT-sub's strict monotonicity at `p = 1`).
  - NAT-addassoc (NatAdditionAssociative) — regroups `#s + (1 + 1) = (#s + 1) + 1`, which (combined with T4's *Numerals* definition `2 := 1 + 1`) identifies `#s + 2 = (#s + 1) + 1` so that NAT-addcompat's strict successor at `n = #s + 1` reads as `#s + 1 < #s + 2`. Consumed at three sites: (i) the *All outputs in C_Y's subtree at position #s + 1* paragraph, where the inline derivation `#s + 2 = #s + (1 + 1) = (#s + 1) + 1` produces `#s + 1 < #s + 2 = #(inc(s, 2))` and discharges positional inheritance's `p < m` precondition at `(p, m) = (#s + 1, #s + 2)` for C_Y's base; (ii) the closure paragraph's range chain `#s + 1 ≤ #s + 2 ≤ #y` that places position `#s + 1` within `#y`'s domain (the right inequality from T10a.1 on C_Y's outputs and T10a.3 on deeper descendants gives `#y ≥ #s + 2`; the left inequality lifts the same `#s + 1 < #s + 2` via NAT-order's `≤`-definition); (iii) the *Descendants of C_X at position #s + 1* paragraph's child-base length bound `#s + 1 + k'' ≥ #s + 2` for `k'' ∈ {1, 2}`, where at `k'' = 1` NAT-addassoc's `(#s + 1) + 1 = #s + 2` delivers the equality and at `k'' = 2` NAT-addcompat's left order-compatibility at `(m, p, n) = (#s + 1, 1, 2)` lifts `1 ≤ 2` to `(#s + 1) + 1 ≤ (#s + 1) + 2`, with NAT-addassoc rewriting the LHS to `#s + 2`.
  - NAT-order (NatStrictTotalOrder) — supplies the companion definitions `m > n ⟺ n < m` and `m ≥ n ⟺ n ≤ m` that present Case 2's inductive step's chain `(tₙ)_{#s+1} + 1 > (tₙ)_{#s+1} ≥ 0` (with NAT-addcompat's strict successor at `n = (tₙ)_{#s+1}` read in `>` form and NAT-zero's lower bound `0 ≤ (tₙ)_{#s+1}` read in `≥` form) and the output-value conclusion `(tₙ)_{#s+1} + 1 ≥ 1` (propagated to `x_{#s+1} ≥ 1` for outputs in C_X's subtree) in `>` / `≥` form; the mixed `≤`-`<` transitivity `m ≤ n ∧ n < p ⟹ m < p` (a consequence of `<`-transitivity together with `≤`'s defining disjunction `m ≤ n ⟺ m < n ∨ m = n` — splitting the left hypothesis, the strict branch chains via `<`-transitivity and the equality branch substitutes via indiscernibility of `=`), instantiated at `m = 0`, `n = (tₙ)_{#s+1}`, `p = (tₙ)_{#s+1} + 1`, consumes NAT-zero's lower bound `0 ≤ (tₙ)_{#s+1}` as the left arm and NAT-addcompat's strict-successor conclusion `(tₙ)_{#s+1} < (tₙ)_{#s+1} + 1` as the right arm to obtain `0 < (tₙ)_{#s+1} + 1`, the strict-positivity precondition consumed by NAT-discrete (at `m = 0`) to rule out `0 ≤ (tₙ)_{#s+1} + 1 < 1` and force `(tₙ)_{#s+1} + 1 ≥ 1`.
  - NAT-discrete (NatDiscreteness) — non-zero ⇒ ≥ 1 on ℕ; forward direction `d < δ ⟹ d + 1 ≤ δ` consumed in the LCA-existence argument to lift `d ≠ δ` (combined with `d ≤ δ`) into `d + 1 ≤ δ` for every `d ∈ D`.
  - NAT-sub (NatPartialSubtraction) — conditional closure `δ ≥ 1 ⟹ δ − 1 ∈ ℕ`, right-inverse `(δ − 1) + 1 = δ`, right-telescoping `(d + 1) − 1 = d`, and strict monotonicity at `p = 1`. Consumed in the LCA-existence argument to construct `δ − 1 ∈ ℕ`, derive `δ − 1 < δ` (right-inverse fed into NAT-addcompat's strict successor), and case-split `d + 1 ≤ δ` into `d + 1 = δ` (right-telescoping yields `d = δ − 1`) and `d + 1 < δ` (strict monotonicity yields `d < δ − 1`) — placing `δ − 1 ∈ U` and contradicting δ's minimality in U.
  - NAT-wellorder (NatWellOrdering) — least-element principle: every nonempty `S ⊆ ℕ` has a least element. Applied in the LCA-existence argument to the upper-bound set `U = {u ∈ ℕ : (A d ∈ D :: d ≤ u)}` of the depth-set `D = {depth(A) : A ∈ Anc(X) ∩ Anc(Y)}`; the resulting least element δ is placed in D itself by TA5-SIG-pattern minimality contradiction, making `δ = max(D)` and locating the LCA C as the unique element of `Anc(X) ∩ Anc(Y)` at depth δ.
  - Prefix — definition of ≼.
- *Forward References:*
  - T10 (PartitionIndependence) — consumes this claim's postcondition as its non-nesting precondition `p₁ ⋠ p₂ ∧ p₂ ⋠ p₁`.

**T10a.6 (DomainDisjointness).** For any two distinct allocators `X` and `Y`, `dom(X) ∩ dom(Y) = ∅`.

Distinct allocators either share a lineage or they do not; both cases yield disjointness.

*Case 1: X and Y are in an ancestor–descendant relationship.* WLOG X is the ancestor and Y the descendant at strictly greater depth. By T10a.1, every `t ∈ dom(X)` has `#t = γ_X` and every `t ∈ dom(Y)` has `#t = γ_Y`. By T10a.3, `γ_Y > γ_X`. A shared `t ∈ dom(X) ∩ dom(Y)` would force `γ_X = γ_Y`, contradicting the strict inequality.

*Case 2: X and Y are not in an ancestor–descendant relationship.* By T10a.5, every `x ∈ dom(X)` is prefix-incomparable with every `y ∈ dom(Y)`. Instantiating at `x = y = t` for a hypothetical `t ∈ dom(X) ∩ dom(Y)` gives `t ⋠ t`, contradicting reflexivity `t ≼ t` from Prefix. ∎

*Consequence (witness uniqueness).* When `same_allocator(a, b)` holds, the allocator `A` with `a, b ∈ dom(A)` is unique: two distinct containing allocators would place `a` in `dom(X) ∩ dom(Y)`. Single-valuedness of the enumeration indices `(i, j)` with `a = tᵢ, b = tⱼ` requires the within-allocator injectivity of T10a.7.

*Formal Contract:*
- *Precondition:* `X` and `Y` are distinct allocators conforming to T10a.
- *Postcondition:* `dom(X) ∩ dom(Y) = ∅`; equivalently, for every `a` there is at most one `A ∈ 𝒯` with `a ∈ dom(A)`, so `same_allocator(a, b)` determines the witnessing `A` uniquely.
- *Depends:*
  - T10a (AllocatorDiscipline) — allocator identity criterion, tree relations, per-allocator `dom(·)`.
  - T10a.1 (UniformSiblingLength) — per-domain uniform length `γ_X`.
  - T10a.3 (LengthSeparation) — strict inequality `γ_Y > γ_X` for ancestor/descendant.
  - T10a.5 (CrossAllocatorIncomparability) — prefix-incomparability across non-lineage allocators.
  - Prefix (PrefixRelation) — reflexivity `t ≼ t`.
- *Forward References:*
  - T10a.7 (EnumerationInjectivity) — elaborates the witness-uniqueness consequence: supplies within-allocator index injectivity so that the enumeration indices `(i, j)` with `a = tᵢ, b = tⱼ` are single-valued once T10a.6 has fixed the witnessing allocator.

**T10a.7 (EnumerationInjectivity).** For every allocator A with domain `dom(A) = {tₙ : n ≥ 0}` — `t₀` the base address and `tₙ₊₁ = inc(tₙ, 0)` — the indexing map `n ↦ tₙ` is injective: for all `m, n ≥ 0` with `m ≠ n`, `tₘ ≠ tₙ`.

Without this property, a single element of `dom(A)` could be reached by two distinct indices, and any predicate phrased over the enumeration index would receive ambiguous values even when the witnessing allocator is already unique.

*Proof.* Let `m, n ≥ 0` with `m ≠ n`. By NAT-order's trichotomy on ℕ, exactly one of `m < n`, `m = n`, or `n < m` holds; the hypothesis `m ≠ n` rules out equality, leaving `m < n ∨ n < m`. Assume without loss of generality that `m < n`. We show `tₘ < tₙ`; T1(a) irreflexivity then excludes `tₘ = tₙ`, hence `tₘ ≠ tₙ`.

We route the argument through the lemma

  **L:** `(A d : d ≥ 1 :: (A m : m ≥ 0 :: tₘ < t_{m+d}))`,

which carries the "gap" `d` as a positive natural bound universally — so the induction, grounded in NAT-wellorder's least-element principle on ℕ, never forms `n − 1` or `(n − 1) − m` and therefore needs no facts about natural-number subtraction inside the induction itself.

*Base case of L* (`d = 1`). Fix `m ≥ 0`. T10a's enumeration rule instantiated at index `m` gives `t_{m+1} = inc(tₘ, 0)`; TA5(a) gives `inc(tₘ, 0) > tₘ`. Hence `tₘ < t_{m+1}`.

*Inductive step of L* (from `d` to `d + 1`). Assume the IH `(A m : m ≥ 0 :: tₘ < t_{m+d})`. Fix `m ≥ 0`; we show `tₘ < t_{m+(d+1)}`. NAT-addassoc at `(m, d, 1)` rewrites `m + (d + 1) = (m + d) + 1`, so `t_{m+(d+1)} = t_{(m+d)+1}`. T10a's enumeration rule at index `m + d` gives `t_{(m+d)+1} = inc(t_{m+d}, 0)`, and TA5(a) gives `inc(t_{m+d}, 0) > t_{m+d}`; combining, `t_{m+d} < t_{m+(d+1)}`. The IH instantiated at `m` gives `tₘ < t_{m+d}`. T1(c) transitivity chains the two inequalities: `tₘ < t_{m+(d+1)}`.

*Closing.* NAT-order's `≤` definition lifts `m < n` to `n ≥ m`, discharging NAT-sub's preconditions at `(n, m)`. NAT-sub's strict positivity at `(n, m)` — whose antecedent `n > m` is `m < n` under NAT-order's `>` definition — yields `n − m ≥ 1`. NAT-sub's left-inverse characterisation at `(n, m)` yields `m + (n − m) = n`. Setting `d = n − m`, lemma L instantiated at that `d ≥ 1` and at `m` delivers `tₘ < t_{m+d}`, and the left-inverse equation rewrites the right-hand index to `n`, so `tₘ < tₙ`.

By T1(a) irreflexivity, `tₘ < tₙ` excludes `tₘ = tₙ`; hence `tₘ ≠ tₙ`. ∎

*Formal Contract:*
- *Precondition:* Allocator A conforming to T10a, with domain `dom(A) = {tₙ : n ≥ 0}` where `t₀` is the base address and `tₙ₊₁ = inc(tₙ, 0)`.
- *Postcondition:* The map `n ↦ tₙ` is injective: `(A m, n ≥ 0 : m ≠ n : tₘ ≠ tₙ)`. Equivalently, `(A m, n ≥ 0 : m < n : tₘ < tₙ)`.
- *Depends:*
  - T10a (AllocatorDiscipline) — supplies the enumeration `tₙ₊₁ = inc(tₙ, 0)`, instantiated at index `m` in the base of L and at index `m + d` in the step of L.
  - TA5 (HierarchicalIncrement), postcondition (a) — strict monotonicity `inc(tₙ, 0) > tₙ` at the base and step of L.
  - T1 (LexicographicOrder), postcondition (c) — transitivity of `<` chains the IH `tₘ < t_{m+d}` with `t_{m+d} < t_{m+(d+1)}` at the inductive step of L.
  - T1 (LexicographicOrder), postcondition (a) — irreflexivity of `<` converts `tₘ < tₙ` to `tₘ ≠ tₙ` at the close of the overall argument.
  - NAT-order (NatStrictTotalOrder) — trichotomy on ℕ indices resolves `m ≠ n` into `m < n ∨ n < m`; the `≤` and `>` definitions lift `m < n` to `n ≥ m` and `n > m` respectively, discharging NAT-sub's preconditions in the closing.
  - NAT-sub (NatPartialSubtraction) — strict positivity at `(n, m)` (under `n > m`) delivers `n − m ≥ 1`; left-inverse characterisation at `(n, m)` (under `n ≥ m`) delivers `m + (n − m) = n`; together these supply the positive gap `d = n − m ≥ 1` and the index identity `m + d = n` at which lemma L is instantiated in the closing. Used once, at the boundary between the corollary and its lemma — not inside the induction.
  - NAT-addassoc (NatAdditionAssociative) — at the inductive step of L, rewrites `m + (d + 1) = (m + d) + 1` so that T10a's enumeration rule at index `m + d` (which produces `t_{(m+d)+1}`) matches the induction goal indexed at `m + (d + 1)`.
  - NAT-wellorder (NatWellOrdering) — least-element principle on ℕ, the source of the induction principle on `d ≥ 1` underwriting lemma L's proof; without it the base case (`d = 1`) and inductive step (`d → d + 1`) would not extend to `(A d ≥ 1 :: L(d))`.

**T10a.8 (UniformSiblingZeroCount).** All siblings produced by a single allocator have the same zero count as its base address.

Let an allocator have base address `t₀` and produce siblings by `tₙ₊₁ = inc(tₙ, 0)` for `n ≥ 0`. We prove `zeros(tₙ) = zeros(t₀)` by induction on `n`.

*Base case.* `n = 0`: `zeros(t₀) = zeros(t₀)`.

*Inductive step.* Assume `zeros(tₙ) = zeros(t₀)`. By T10a.4, `tₙ` satisfies T4, so TA5-SigValid gives `sig(tₙ) = #tₙ` and T4's field-segment constraint gives `(tₙ)_{#tₙ} ≠ 0`. By T0, `(tₙ)_{#tₙ} ∈ ℕ`; NAT-zero gives `0 ≤ (tₙ)_{#tₙ}`; NAT-discrete at `m = 0` rules out `0 ≤ (tₙ)_{#tₙ} < 1`, so `(tₙ)_{sig(tₙ)} ≥ 1 > 0`.

TA5(b) for `k = 0` preserves every position `i ≠ sig(tₙ)` with `1 ≤ i ≤ #tₙ`; TA5(c) sets `(tₙ₊₁)_{sig(tₙ)} = (tₙ)_{sig(tₙ)} + 1` with `#tₙ₊₁ = #tₙ`. NAT-closure gives `(tₙ)_{sig(tₙ)} + 1 ∈ ℕ`; NAT-addcompat gives `(tₙ)_{sig(tₙ)} < (tₙ)_{sig(tₙ)} + 1`; combined with NAT-zero's `0 ≤ (tₙ)_{sig(tₙ)}` chained via NAT-order's transitivity, `0 < (tₙ)_{sig(tₙ)} + 1`, which by NAT-order's `>` companion definition `m > n ⟺ n < m` reads as `(tₙ₊₁)_{sig(tₙ)} > 0`. NAT-order's irreflexivity `¬(n < n)` (equivalently, the exactly-one trichotomy clause `¬(m < n ∧ m = n)` derived from it) lifts `0 < (tₙ₊₁)_{sig(tₙ)}` to `(tₙ₊₁)_{sig(tₙ)} ≠ 0`.

The set `{i : 1 ≤ i ≤ #tₙ ∧ (tₙ)ᵢ = 0}` is unchanged: the modified position was positive and remains positive (the `≠ 0` conclusion just established excludes `sig(tₙ)` from the primed zero-index subset, while T4(iv)'s `(tₙ)_{#tₙ} ≠ 0` together with TA5-SigValid's `sig(tₙ) = #tₙ` excludes it from the original); every other position is fixed by TA5(b); length preservation rules out new indices. Hence `zeros(tₙ₊₁) = zeros(tₙ) = zeros(t₀)`. ∎

*Formal Contract:*
- *Precondition:* Allocator with base address `t₀`, producing siblings by `inc(·, 0)`, conforming to T10a.
- *Postcondition:* `(A n ≥ 0 : zeros(tₙ) = zeros(t₀))`.
- *Depends:*
  - T10a (AllocatorDiscipline) — supplies `t₀` and restricts siblings to `tₙ₊₁ = inc(tₙ, 0)`.
  - T10a.4 (T4PreservationUnderDiscipline) — every sibling satisfies T4.
  - T4 (HierarchicalParsing) — field-segment constraint gives `(tₙ)_{#tₙ} ≠ 0`.
  - T0 (CarrierSetDefinition) — fixes the carrier as ℕ.
  - NAT-zero (NatZeroMinimum) — lower bound `0 ≤ (tₙ)ᵢ` on ℕ.
  - NAT-discrete (NatDiscreteness) — converts non-zero to strictly positive on ℕ.
  - NAT-closure (NatArithmeticClosureAndIdentity) — `(tₙ)_{sig(tₙ)} + 1 ∈ ℕ`.
  - NAT-addcompat (NatAdditionOrderAndSuccessor) — strict successor inequality `n < n + 1`.
  - NAT-order (NatStrictTotalOrder) — `>` companion definition `m > n ⟺ n < m` reads `0 < (tₙ)_{sig(tₙ)} + 1` as `(tₙ₊₁)_{sig(tₙ)} > 0`; transitivity chains NAT-addcompat's `(tₙ)_{sig(tₙ)} < (tₙ)_{sig(tₙ)} + 1` with NAT-zero's `0 ≤ (tₙ)_{sig(tₙ)}` to give `0 < (tₙ)_{sig(tₙ)} + 1`; irreflexivity `¬(n < n)` (equivalently, the exactly-one trichotomy clause `¬(m < n ∧ m = n)` derived from it) lifts `(tₙ₊₁)_{sig(tₙ)} > 0` to `(tₙ₊₁)_{sig(tₙ)} ≠ 0`, which excludes position `sig(tₙ)` from the primed zero-index subset in the zero-index-set equality argument.
  - TA5 (HierarchicalIncrement) — TA5(b)/(c) restrict the step to a single position with length preserved.
  - TA5-SigValid (SigOnValidAddresses) — `sig(tₙ) = #tₙ` on T4-valid addresses.

**T10a-N (AllocatorDisciplineNecessity).** T10a restricts the sibling stream of an allocator to `inc(·, 0)`. Relaxing this restriction to permit `inc(·, k)` with `k > 0` in the sibling stream falsifies T10a.2 (NonNestingSiblingPrefixes).

*Derivation.* Let `t₀ ∈ T`, fix `k > 0`, and let `t₁ = inc(t₀, 0)` and `t₂ = inc(t₁, k)` be co-sibling outputs of one allocator under the relaxation.

1. From TA5(d), conclude `#t₂ = #t₁ + k`.
2. From `k > 0` with NAT-zero (`0 ≤ k`) and NAT-discrete's no-interval form at `m = 0` (`0 ≤ n < 0 + 1 ⟹ n = 0`, instantiated at `n = k`), conclude `k ≥ 0 + 1`; NAT-closure supplies `1 ∈ ℕ` and its left-identity clause `0 + n = n` (instantiated at `n = 1`) rewrites `0 + 1` to `1`, yielding `k ≥ 1`.
3. From `1 ≤ k` by NAT-addcompat (order-compatibility, `m = #t₁, p = 1, n = k`), conclude `#t₁ + 1 ≤ #t₁ + k`.
4. From NAT-addcompat (strict successor at `n = #t₁`), conclude `#t₁ < #t₁ + 1`.
5. From (3), (4) by NAT-order (`m ≤ n ⟺ m < n ∨ m = n`), conclude `#t₁ < #t₁ + k = #t₂`.
6. From TA5(b) for `k > 0`, conclude `t₂` agrees with `t₁` at every position `1 ≤ i ≤ #t₁`.
7. From (5) by NAT-order, weaken to `#t₁ ≤ #t₂`.
8. From (6), (7) by Prefix, conclude `t₁ ≼ t₂`.

The strict inequality `#t₁ < #t₂` forces `t₁ ≠ t₂`, so `(t₁, t₂)` is a pair of distinct co-sibling outputs of one allocator with `t₁ ≼ t₂`, contradicting T10a.2. The construction is parametric in `k > 0`, so any relaxation admitting `inc(·, k)` with `k > 0` into the sibling stream witnesses such a pair. ∎

*Formal Contract:*
- *Preconditions:* T10a's sibling restriction is relaxed to permit `inc(·, k)` with any `k ≥ 0` in the sibling stream. `t₀ ∈ T`; `k > 0`; the allocator emits `t₁ = inc(t₀, 0)` and `t₂ = inc(t₁, k)` as co-sibling outputs.
- *Postconditions:* `t₁ ≼ t₂` with `t₁ ≠ t₂`, falsifying T10a.2 (NonNestingSiblingPrefixes). The `k = 0` sibling restriction is therefore necessary for T10a.2.
- *Depends:*
  - T0 (CarrierSetDefinition) — carrier `T`, length `#·`.
  - NAT-zero (NatZeroMinimum) — supplies `0 ≤ k` to instantiate NAT-discrete at `m = 0`.
  - NAT-discrete (NatDiscreteness) — no-interval form at `m = 0` with `n = k` yields `k ≥ 0 + 1`, which NAT-closure's left identity rewrites to `k ≥ 1`.
  - NAT-closure (NatArithmeticClosureAndIdentity) — supplies `1 ∈ ℕ` (the symbol in `k ≥ 1`) and the left-identity clause `0 + n = n` (instantiated at `n = 1`) used to rewrite NAT-discrete's conclusion `k ≥ 0 + 1` to `k ≥ 1`.
  - NAT-addcompat (NatAdditionOrderAndSuccessor) — order-compatibility lifts `1 ≤ k` to `#t₁ + 1 ≤ #t₁ + k`; strict successor gives `#t₁ < #t₁ + 1`.
  - NAT-order (NatStrictTotalOrder) — chains the strict inequality and weakens `<` to `≤` for Prefix.
  - TA5 (HierarchicalIncrement) — (d) gives `#t₂ = #t₁ + k`; (b) gives agreement on positions `1..#t₁`.
  - Prefix (PrefixRelation) — converts agreement plus `#t₁ ≤ #t₂` into `t₁ ≼ t₂`.
  - T10a (AllocatorDiscipline) — the discipline whose relaxation is considered.
  - T10a.2 (NonNestingSiblingPrefixes) — the clause falsified by the constructed pair.

**PartitionMonotonicity (PartitionMonotonicity).** Within any prefix-delimited partition of the address space, the set of allocated addresses is totally ordered by T1, and this order is consistent with the allocation order of any single allocator within that partition. Moreover, for any two sibling sub-partitions with non-nesting prefixes `p₁ < p₂`, every address extending `p₁` precedes every address extending `p₂` under T1 — the per-allocator ordering extends to a cross-allocator ordering determined by the prefix structure.

*Proof.*

*Notation.* For `c ∈ T`, `subtree(c) = {t ∈ T : c ≼ t}` is the *prefix closure* of `c`. T10a's `dom(c) = {cₙ : n ≥ 0}` (with `c₀ = c`, `cₙ₊₁ = inc(cₙ, 0)`) is the sibling stream of `c`; TA5(c) preserves length so every `cₙ` has length `#c`, and TA5(b)/(c) with T10a.4 supplying T4-validity for TA5-SigValid make `cₙ` for `n ≥ 1` differ from `c` at position `sig(c) = #c`, so `dom(c) ∩ subtree(c) = {c}`. Define the *allocator reach* `reach(c) = ⋃_{s ∈ dom(c)} subtree(s)`. The partition rooted at `p` decomposes at the sibling level as `{p} ∪ reach(c₁) ∪ reach(c₂)` (when both children spawn), since siblings `inc(c₁, 0), inc(inc(c₁, 0), 0), …` carry values `2, 3, …` at position `#p + 1` and lie outside `subtree(c₁)` yet extend `p`.

**Partition structure.** Consider a partition with prefix `p`. Every allocated address `a` in this partition satisfies `p ≼ a`, placing it in `subtree(p) = {t ∈ T : p ≼ t}`. By T5 (prefix convexity), this set forms a contiguous interval under T1: if `p ≼ a`, `p ≼ c`, and `a ≤ b ≤ c`, then `p ≼ b`. No address from outside the partition can interleave between two addresses inside it.

Within the partition, the parent allocator may spawn child allocators from `p` according to T10a. Since T10a constrains each `(p, k')` pair to at most one child-spawning event with `k' ∈ {1, 2}`, the parent spawns at most two children from `p`: a *param-1 child* with prefix `c₁ = inc(p, 1)` at length `#p + 1` (TA5(d)), and a *param-2 child* with prefix `c₂ = inc(p, 2)` at length `#p + 2` (TA5(d)), the latter carrying a field separator `0` at position `#p + 1`. Either or both may be absent. Each child allocator produces its sibling stream via repeated `inc(·, 0)` (T10a), and the parent's own sibling stream resumes independently at the parent level.

**Sibling prefixes are non-nesting.** Within any single child allocator's sibling stream, we establish that for distinct sibling prefixes `tᵢ` and `tⱼ` with `i ≠ j`: `tᵢ ⋠ tⱼ ∧ tⱼ ⋠ tᵢ`.

*Uniform length.* By TA5(c), `inc(t, 0)` preserves length: `#inc(t, 0) = #t`. Applying this inductively from `t₀` — `#t₁ = #inc(t₀, 0) = #t₀`, and for each `n ≥ 0`, `#tₙ₊₁ = #inc(tₙ, 0) = #tₙ` — we obtain `#tₙ = #t₀` for all `n ≥ 0`. Every sibling prefix has the same length.

*Distinctness.* By TA5(a), each application of `inc(·, 0)` produces a strictly greater tumbler under T1, so the sibling prefix sequence is strictly increasing: `t₀ < t₁ < t₂ < ...`. In particular, `tᵢ ≠ tⱼ` for all `i ≠ j`.

*Non-nesting.* A proper prefix relationship `q ≺ r` requires `#q < #r`, since T1 case (ii) defines `q < r` when `q` is a proper prefix of `r`, which demands `#q = m < n = #r`. Since `#tᵢ = #tⱼ` (uniform length), neither can be a proper prefix of the other. By Prefix, `tᵢ ≼ tⱼ` holds iff `tᵢ = tⱼ` or `tᵢ ≺ tⱼ`; we have excluded both. So `tᵢ ⋠ tⱼ`, and by the symmetric argument `tⱼ ⋠ tᵢ`.

**Cross-partition ordering.** Take two sibling sub-partition prefixes `tᵢ` and `tⱼ` with `i < j`. From the strict monotonicity of the sibling sequence we have `tᵢ < tⱼ`, and we have just established `tᵢ ⋠ tⱼ ∧ tⱼ ⋠ tᵢ`. These are precisely the preconditions of PrefixOrderingExtension: for every address `a` with `tᵢ ≼ a` and every address `b` with `tⱼ ≼ b`, we conclude `a < b`.

**Cross-param ordering.** When both a param-1 and a param-2 child are spawned from the same prefix `p`, every address in `reach(c₂)` precedes every address in `reach(c₁)` under T1.

The param-1 child's base `c₁ = inc(p, 1)` has `(c₁)_{#p+1} = 1` (TA5(d) with `k = 1`) and length `#p + 1`; each subsequent sibling `inc(·, 0)` in `c₁`'s stream modifies only position `sig(t) = #t = #p + 1` (TA5-SigValid, TA5(c)) and increments the value there, yielding components `2, 3, ...` at position `#p + 1`. Every sibling `u ∈ dom(c₁)` has `u_{#p+1} ≥ 1`. For `a ∈ subtree(u)` with `u ∈ dom(c₁)`: if `a = u`, then `a_{#p+1} = u_{#p+1} ≥ 1`; if `u ≺ a`, then `a` is reached from `u` through a chain of child-spawning and sibling increments in descendant allocators. Each child-spawning increment `inc(s, k')` with `k' > 0` preserves positions `1..#s` (TA5(b)), and since every `s` along this chain has `#s ≥ #u = #p + 1`, position `#p + 1` carries through unchanged; each descendant sibling increment acts at position `sig ≥ #base > #p + 1` (TA5(c)), leaving position `#p + 1` fixed. Hence `a_{#p+1} ≥ 1`, and every address in `reach(c₁)` has component `≥ 1` at position `#p + 1`.

The param-2 child's base `c₂ = inc(p, 2)` has `(c₂)_{#p+1} = 0` (TA5(d) with `k = 2`) and length `#p + 2`; each subsequent sibling `inc(·, 0)` in `c₂`'s stream modifies position `sig(t) = #t = #p + 2 ≠ #p + 1` (TA5-SigValid, TA5(c)), leaving position `#p + 1` at `0`. Every sibling `v ∈ dom(c₂)` has `v_{#p+1} = 0`. For `b ∈ subtree(v)` with `v ∈ dom(c₂)`: if `b = v`, then `b_{#p+1} = 0`; if `v ≺ b`, TA5(b) copies `v_{#p+1} = 0` unchanged into every descendant base (since `#v = #p + 2 > #p + 1`), and subsequent sibling increments in descendant allocators act at positions strictly beyond `#p + 1`. Hence `b_{#p+1} = 0`, and every address in `reach(c₂)` has component `0` at position `#p + 1`.

Both reaches extend `p`, agreeing with `p` on positions `1, ..., #p` (TA5(b)). At position `#p + 1`: for any `a ∈ reach(c₁)` and `b ∈ reach(c₂)`, `b_{#p+1} = 0 < 1 ≤ a_{#p+1}`. By T1 case (i), `b < a`.

**Intra-partition ordering (by structural induction).** A sub-partition with prefix `tᵢ` may contain addresses from multiple allocators: the parent allocator may spawn up to two child allocators via `inc(tᵢ, k')` with `k' ∈ {1, 2}` (T10a), each producing addresses extending `tᵢ`, and their own children may do likewise. We prove total ordering within each sub-partition by induction on the depth of allocator nesting.

*Termination.* Each child-spawning increment `inc(s, k)` with `k > 0` yields a prefix of length `#s + k ≥ #s + 1` (TA5(d)). Since every allocated tumbler has finite length, the nesting depth within any sub-partition is bounded.

*Base case (nesting depth 0).* A sub-partition in which no child allocator is spawned contains only the root address `tᵢ` — a single element, trivially ordered.

*Inductive step.* Assume the result holds for every sub-partition of nesting depth less than `d`. Consider a sub-partition with prefix `tᵢ` at nesting depth `d ≥ 1`. The parent allocator spawns one or two child allocators from `tᵢ`: a param-1 child via `inc(tᵢ, 1)` and a param-2 child via `inc(tᵢ, 2)`, one or both present as permitted by T10a. Each child allocator present produces a sibling stream via `inc(·, 0)`, and each sibling `uⱼ` in such a stream heads a sub-sub-partition `subtree(uⱼ) = {a ∈ T : uⱼ ≼ a}`. Within each child's stream, the prefixes have uniform length (TA5(c)) and are strictly increasing (TA5(a)), hence non-nesting; by PrefixOrderingExtension, for `j₁ < j₂`, every address extending `uⱼ₁` precedes every address extending `uⱼ₂`. When two child allocators are present, the cross-param ordering (applied with `tᵢ` in place of `p`) establishes that every address in the param-2 child's reach precedes every address in the param-1 child's reach. Within each sub-sub-partition, the nesting depth is less than `d`, so by the induction hypothesis it is totally ordered by T1 consistently with per-allocator allocation order.

The root address `tᵢ` precedes every other address in the sub-partition: for any `a ≠ tᵢ` with `tᵢ ≼ a`, the inequality `#a > #tᵢ` gives `tᵢ ≺ a`, whence `tᵢ < a` by T1 case (ii). Combining root ordering, cross-param ordering, within-param cross-sub-sub-partition ordering (PrefixOrderingExtension), and within-sub-sub-partition ordering (induction hypothesis), every pair of distinct addresses in the sub-partition is comparable under T1. Per-allocator allocation order is consistent throughout: T9 supplies `allocated_before(a, b) ⟹ a < b` within each allocator's sibling stream, and the induction hypothesis carries this consistency through each `subtree(uⱼ)`.

**Total ordering.** The partition root `p` is itself an allocated address in `subtree(p)`, yet it belongs to no child's reach: every sibling base `s ∈ dom(c₁) ∪ dom(c₂)` satisfies `#s > #p` (TA5(d) gives child-base lengths `#p + 1` or `#p + 2`; T10a.1 preserves length under sibling increments), so no such `s` can be a prefix of `p`; hence `p ∉ reach(c₁) ∪ reach(c₂)`. For any allocated `a ≠ p` with `p ≼ a`, the relation is proper — `p ≺ a`, hence `#p < #a` — and T1 case (ii) gives `p < a`. Thus `p` precedes every other allocated address in the partition.

For the remaining pairs, every allocated address `a ≠ p` belongs to exactly one of `reach(c₁)` and `reach(c₂)` (when both exist; otherwise to whichever single child's reach is present), and within that, to the prefix-closure `subtree(u)` of exactly one sibling `u` in the corresponding child's stream. *Existence*: every such `a` was produced by an allocator descended from `p`, and the lineage from `p` to `a`'s producer first leaves `p` through one of the two child-spawning increments, landing in some sibling stream `dom(cᵢ)`; within that stream, `a` either equals some sibling `u ∈ dom(cᵢ)` or descends further from such a `u`, so `a ∈ subtree(u) ⊆ reach(cᵢ)`. *Uniqueness across reaches* (when both exist): `reach(c₁)` carries component `≥ 1` at position `#p + 1` while `reach(c₂)` carries component `0` there, so `reach(c₁) ∩ reach(c₂) = ∅`. *Uniqueness within a reach*: distinct siblings `u, u' ∈ dom(cᵢ)` have `#u = #u'` (T10a.1) and `u ≠ u'` (TA5(a)); if `s ∈ subtree(u) ∩ subtree(u')` existed, then `u ≼ s` gives `uⱼ = sⱼ` for `1 ≤ j ≤ #u` and `u' ≼ s` gives `u'ⱼ = sⱼ` for `1 ≤ j ≤ #u'`; with `#u = #u'`, `u` and `u'` agree componentwise at every position, whence T3 forces `u = u'`, a contradiction. Hence `subtree(u) ∩ subtree(u') = ∅`. Within that prefix-closure `subtree(u)`, the structural induction places `a` in exactly one sub-sub-partition.

For any two distinct addresses `a ≠ p` and `b ≠ p` within the partition: if they belong to different children's reaches, Cross-param ordering determines their comparison; if they belong to the same child's reach but to prefix-closures of different siblings `uᵢ, uⱼ ∈ dom(cₖ)` with `i < j`, then `uᵢ < uⱼ` (TA5(a)) and `uᵢ ⋠ uⱼ ∧ uⱼ ⋠ uᵢ`, so PrefixOrderingExtension gives that the `subtree(uᵢ)`-address precedes the `subtree(uⱼ)`-address; if both belong to `subtree(u)` for the same sibling `u`, structural induction gives their ordering. In every case the pair is comparable under T1, and the ordering is consistent with per-allocator allocation order — `p` precedes all its descendants by T1 case (ii) (`p ≺ a ⟹ p < a`), within each allocator's sibling stream by T9, across spawn parameters by T1 case (i), across sibling prefix-closures within a single reach by PrefixOrderingExtension, and within nested sub-partitions by structural induction. ∎

*Formal Contract:*
- *Preconditions:* A system conforming to T10a (allocator discipline); a partition with prefix `p ∈ T`; up to two child-spawning events from `p`, via `inc(p, k')` with `k' ∈ {1, 2}` as permitted by T10a, each establishing a child prefix whose sibling stream is produced by repeated `inc(·, 0)`.
- *Depends:*
  - T5 (ContiguousSubtrees) — `subtree(p)` is a contiguous T1-interval.
  - T10a (AllocatorDiscipline) — at most two children per `p` via `inc(p, k')` with `k' ∈ {1, 2}`; sibling streams by repeated `inc(·, 0)`.
  - T10a.1 — uniform length of siblings within a stream.
  - T10a.4 — T4-validity preservation, feeds TA5-SigValid.
  - TA5-SigValid (SigOnValidAddresses) — `sig(t) = #t` for valid addresses.
  - TA5 (HierarchicalIncrement) — (a) strict monotonicity of `inc`; (b) `inc(s, k')` with `k' > 0` preserves positions `1..#s`; (c) `inc(·, 0)` preserves length and acts at the significant position; (d) child-base characterisation for `k' ∈ {1, 2}`.
  - T1 (LexicographicOrder) — case (i) divergence-position comparison; case (ii) proper-prefix ordering.
  - T3 (CanonicalRepresentation) — equal-length componentwise agreement implies equality.
  - Prefix (PrefixRelation) — prefix definition and `p ≺ q ⟹ #p < #q`.
  - PrefixOrderingExtension — extends non-nesting prefix order to all descendants.
  - T9 (ForwardAllocation) — per-allocator allocation-order consistency.
- *Postconditions:* (1) For sibling sub-partition prefixes `tᵢ < tⱼ` (with `0 ≤ i < j`) within any single child allocator's stream, and any `a, b ∈ T` with `tᵢ ≼ a` and `tⱼ ≼ b`: `a < b`. (2) Within each sub-partition with prefix `tᵢ`, for any `a, b` allocated by the same allocator: `allocated_before(a, b) ⟹ a < b`. (3) When both param-1 and param-2 children are spawned from `p` (with `c₁ = inc(p, 1)` and `c₂ = inc(p, 2)`), let `reach(c) = ⋃_{s ∈ dom(c)} subtree(s)`. Every address in `reach(c₂)` precedes every address in `reach(c₁)`: every `a ∈ reach(c₁)` has `a_{#p+1} ≥ 1`, every `b ∈ reach(c₂)` has `b_{#p+1} = 0`, both reaches agree with `p` on positions `1..#p`, and T1 case (i) at position `#p + 1` gives `b < a`. Equivalently, for any `b` with `p ≼ b` and `b_{#p+1} = 0`, and any `a` with `p ≼ a` and `a_{#p+1} ≥ 1`: `b < a`.
- *Invariant:* For every reachable system state, the set of allocated addresses within any prefix-delimited partition is totally ordered by T1 consistently with per-allocator allocation order.

**AllocatedSet (AllocatedSet).** Defines `allocated(s)`, the set of addresses allocated in state s, as the union of realized per-allocator domains, and establishes the bridge between T10a's unindexed chain `dom(A)` and the state-indexed realized domain `domₛ(A)`.

Let Σ denote the system's transition vocabulary and let 𝒮 denote the state space of the allocation system. Each `op ∈ Σ` is a partial function `op : 𝒮 ⇀ 𝒮`. The predicate `op(s) defined` abbreviates `s ∈ dom(op)`; when it holds, `op(s) ∈ 𝒮` is the unique successor state. A state transition `s → s'` is exactly a pair `(s, op(s))` with `op ∈ Σ` and `s ∈ dom(op)`.

A *state* `s ∈ 𝒮` is a configuration of the allocator tree consisting of two components: a set `Act(s) ⊆ 𝒯` of *activated allocators* and, for each `A ∈ Act(s)`, a count `nₛ(A) ≥ 0` of sibling increments performed on A. For `A ∉ Act(s)` the count nₛ(A) is not defined — an allocator has no sibling count until it has been activated. We make activation a projection of the state by the definition

  activated(A, s) ≡ A ∈ Act(s),

so `activated : 𝒯 × 𝒮 → {⊤, ⊥}` is a total function of s alone; it reads a component of s and does not require any inductive reconstruction from the transition history. The *realized domain* of A at s is the finite set

  domₛ(A) = {t₀, t₁, …, t_{nₛ(A)}}    when activated(A, s),
  domₛ(A) = ∅                          when ¬activated(A, s),

where t₀ is A's base address and tᵢ₊₁ = inc(tᵢ, 0). The second clause stipulates that a non-activated allocator has realized no addresses yet; it also keeps `domₛ` total on 𝒯 × 𝒮, so the set-builder notation `{t₀, …, t_{nₛ(A)}}` — which would be ill-formed when `nₛ(A)` is undefined — is simply never invoked for non-activated A. Downstream claims that read `domₛ(A)` for an arbitrary A (the frame condition below, for instance) are therefore well-formed without a precondition on activation. The *allocated set* at s is

  allocated(s) = ⋃ { domₛ(A) : activated(A, s) },

a well-defined finite union because Act(s) is finite (it is populated one element per transition, see (T2) below) and each domₛ(A) is finite.

*Admissibility of Σ.* Having made activation a state component, what used to be an inductive definition of `activated` over transitions becomes an *admissibility requirement on Σ*: each `op ∈ Σ` must update the Act component exactly in accord with the base and transition clauses. We state these requirements directly on transition shapes so that the earlier inductive content is preserved without the circularity.

The *initial state* `s₀` is fixed by `Act(s₀) = {root}` and `nₛ₀(root) = 0`, so `allocated(s₀) = {t₀}` where t₀ is the root's base address.

Every admissible transition `s → s'` takes exactly one of three shapes, and each `op ∈ Σ` realizes one such shape:

  (T1) *Sibling increment of some A ∈ Act(s)*: `Act(s') = Act(s)`, `nₛ'(A) = nₛ(A) + 1`, and `nₛ'(B) = nₛ(B)` for every `B ∈ Act(s) ∖ {A}`. The step applies `inc(tₙₛ(A), 0)` to A's current frontier, extending A's realized chain by one element.

  (T2) *Child spawn of some A ∉ Act(s)*: the step is admissible in state s only when `parent(A) ∈ Act(s)` and `spawnPt(A) ∈ domₛ(parent(A))` — i.e., parent(A) is itself already activated, and spawnPt(A) is one of parent(A)'s already-realized siblings in s. The first conjunct ensures `domₛ(parent(A))` is well-defined (otherwise nₛ(parent(A)) is undefined); the second requires that the address from which A is spawned has actually been generated in s, since `inc(spawnPt(A), spawnParam(A))` cannot be applied to a tumbler that does not yet exist as a realized address. T10a fixes spawnPt(A) and spawnParam(A) uniquely as components of A's spawning triple, so the inc-operation's arguments are determined by A's identity alone — the precondition is therefore a *realization* requirement on spawnPt(A) in s, not a uniqueness requirement on the operation's arguments. We do *not* additionally require `spawnPt(A) = t_{nₛ(parent(A))}` (parent's current frontier): under T10a's allocator discipline, spawnPt(A) may be any element of parent(A)'s abstract chain, so once spawnPt(A) has been realized in parent(A), spawning A is admissible whether or not parent(A) has produced further siblings beyond it. Equivalently, by the realized-domain definition this precondition reads `spawnPt(A) = tᵢ for some i with 0 ≤ i ≤ nₛ(parent(A))`. Under the precondition, the step applies `inc(spawnPt(A), spawnParam(A))` with `spawnParam(A) ∈ {1, 2}` to spawnPt(A), yielding A's base address — the first element `t₀` of `dom(A)`. Then `Act(s') = Act(s) ∪ {A}`, `nₛ'(A) = 0`, and `nₛ'(B) = nₛ(B)` for every `B ∈ Act(s)`. The single `inc(·, k')` with `k' ∈ {1, 2}` admitted by T10a is exactly the operation that spawns A, so T10a's spawning discipline is what picks out this shape.

  (T3) *Non-allocating*: `Act(s') = Act(s)` and `nₛ'(B) = nₛ(B)` for every `B ∈ Act(s)` — every realized domain is unchanged.

Three consequences are immediate from the shape-based admissibility. (α) *Persistence of activation*: every admissible transition satisfies `Act(s) ⊆ Act(s')`, since (T1) and (T3) preserve Act and (T2) extends it by one element; equivalently, `activated(A, s) ⟹ activated(A, s')`. (β) *No spontaneous activation*: if `A ∉ Act(s)` and `s → s'` is not a (T2) step spawning A, then `A ∉ Act(s')`; activation is gained only by being the spawned allocator of a (T2) step. (γ) *Frame on non-allocating transitions*: if `s → s'` is a (T3) step, then `Act(s') = Act(s)` and `nₛ'(B) = nₛ(B)` for every `B ∈ Act(s)`, so for every `A ∈ 𝒯` we have `activated(A, s) ≡ activated(A, s')` and, where activation holds, `domₛ(A) = domₛ'(A)`; hence `allocated(s) = allocated(s')`. This frame is what licenses downstream reasoning to restrict attention to (T1) and (T2) when asking how `allocated` evolves — (T3) steps contribute nothing to that evolution by construction, not by convention. T10a's at-most-once constraint on `(t, k')` pairs additionally guarantees that no allocator's spawning inc-operation fires twice along any admissible trajectory, so activation, once acquired, is not re-acquired and the Act component is strictly monotone across any transition sequence.

Because activation is a projection of s, the activated set `Act(s) = {A ∈ 𝒯 : activated(A, s)}` is a function of the endpoint alone: any two admissible transition sequences from s₀ that terminate at the same state s necessarily agree on Act(s), since s is their common endpoint and carries Act as a component. Path-independence is thus not a separate theorem over α and β — it is a structural consequence of framing activation as a state projection rather than reconstructing it from transition history; α and β constrain how Σ may move *between* states but contribute nothing further at a shared endpoint, because at that endpoint there is nothing left to reconstruct. Hence `allocated(s) = ⋃ { domₛ(A) : activated(A, s) }` is well-defined on every state — reachable or not — without any appeal to the history that produced s.

*Domain embedding.* Since both `dom(A)` and `domₛ(A)` are generated by the same chain `tᵢ₊₁ = inc(tᵢ, 0)` from A's base address, `domₛ(A)` is the initial segment of length `nₛ(A) + 1` in T10a's enumeration of `dom(A)`:

  (i) *Inclusion:* for every reachable s and every activated A, `domₛ(A) ⊆ dom(A)`.

  (ii) *Initial-segment structure:* `domₛ(A) = {tᵢ : 0 ≤ i ≤ nₛ(A)}`; enumeration indices agree with those in `dom(A)`.

  (iii) *Reachable-state containment:* `dom(A) ⊇ ⋃ { domₛ(A) : s reachable from s₀ }`. The reverse inclusion is a liveness statement not furnished by this ASN.

T10a restricts sibling production to `inc(·, 0)`, so under (T1) `domₛ(A)` can only grow by appending `t_{nₛ(A)+1}` — no skipped index, no out-of-order element, no gap.

*Transfer of T9 to realized allocations.* If `a, b ∈ domₛ(A)` with `a = tᵢ, b = tⱼ` and `i < j ≤ nₛ(A)`, then by (i) both `a, b ∈ dom(A)`, and by (ii) their indices in T10a's enumeration are i, j. So `same_allocator(a, b)` (T10a) and `allocated_before(a, b)` (T9) hold for the pair, and T9's conclusion `a < b` applies. Any two addresses co-realized by a single allocator in s are ordered in the tumbler order by entry index.

*Formal Contract:*
- *Definitions:*
  - *State space:* 𝒮 is the state space of the allocation system; `s ∈ 𝒮` is a pair `(Act(s), nₛ)` where `Act(s) ⊆ 𝒯` is the set of activated allocators and `nₛ` assigns each `A ∈ Act(s)` a count `nₛ(A) ≥ 0` of sibling increments performed. For `A ∉ Act(s)`, nₛ(A) is not defined.
  - *Activation predicate:* `activated(A, s) ≡ A ∈ Act(s)` — a projection of the Act component, total on 𝒯 × 𝒮 and computed from s alone (no induction over transitions).
  - *Transition vocabulary:* Σ is the system's transition vocabulary; each `op ∈ Σ` is a partial function `op : 𝒮 ⇀ 𝒮`. The predicate `op(s) defined` abbreviates `s ∈ dom(op)`; when it holds, `op(s) ∈ 𝒮` is the unique successor state.
  - *State transition:* `s → s'` is the pair `(s, op(s))` with `op ∈ Σ` and `s ∈ dom(op)`.
  - *Realized domain:* domₛ(A) = {t₀, …, t_{nₛ(A)}} where tᵢ₊₁ = inc(tᵢ, 0), when activated(A, s); domₛ(A) = ∅ when ¬activated(A, s). The second clause makes domₛ total on 𝒯 × 𝒮 and keeps the definition well-formed when nₛ(A) is undefined (outside Act(s) it is never evaluated).
  - *Allocated set:* allocated(s) = ⋃ { domₛ(A) : activated(A, s) }.
- *Axiom (admissibility of Σ):* Every `op ∈ Σ` whose application yields `s → s'` realizes exactly one of three transition shapes:
  - *(T1) Sibling increment of `A ∈ Act(s)`:* Act(s') = Act(s); nₛ'(A) = nₛ(A) + 1; nₛ'(B) = nₛ(B) for every `B ∈ Act(s) ∖ {A}`. The step applies `inc(tₙₛ(A), 0)` to A's frontier.
  - *(T2) Child spawn of `A ∉ Act(s)`:* admissible in s only when `parent(A) ∈ Act(s)` and `spawnPt(A) ∈ domₛ(parent(A))` — equivalently, `spawnPt(A) = tᵢ for some i with 0 ≤ i ≤ nₛ(parent(A))`, i.e., spawnPt(A) is an already-realized sibling of parent(A) in s, not necessarily parent's current frontier; under this precondition the step applies `inc(spawnPt(A), spawnParam(A))` with `spawnParam(A) ∈ {1, 2}`, yielding A's base address `t₀ ∈ dom(A)`; Act(s') = Act(s) ∪ {A}; nₛ'(A) = 0; nₛ'(B) = nₛ(B) for every `B ∈ Act(s)`.
  - *(T3) Non-allocating:* Act(s') = Act(s); nₛ'(B) = nₛ(B) for every `B ∈ Act(s)`; every realized domain is unchanged.
- *Postconditions:*
  - *Initial state:* Act(s₀) = {root}, nₛ₀(root) = 0, and `allocated(s₀) = {t₀}` where t₀ is the root allocator's base address.
  - *Persistence of activation:* for every admissible transition `s → s'`, `Act(s) ⊆ Act(s')`, equivalently `activated(A, s) ⟹ activated(A, s')`.
  - *No spontaneous activation:* if `A ∉ Act(s)` and `s → s'` is not a (T2) step spawning A, then `A ∉ Act(s')`.
  - *No repeat activation:* along any admissible transition sequence, no allocator's (T2) spawn step occurs twice (by T10a's at-most-once constraint on `(t, k')` pairs).
  - *Path-independence of activation:* for any two admissible transition sequences from s₀ that terminate at the same state s, the activated set Act(s) is the same along both. This is structural — activation is a projection of s, so any two paths sharing an endpoint share Act(s) by construction — not a derived consequence of α and β.
  - *Inclusion (i):* for every reachable s and every activated A, `domₛ(A) ⊆ dom(A)`.
  - *Initial-segment structure (ii):* `domₛ(A) = {tᵢ : 0 ≤ i ≤ nₛ(A)}`, and the indices i agree with T10a's enumeration of `dom(A)` — the same `tᵢ₊₁ = inc(tᵢ, 0)` chain generates both, so no index is skipped, no element is out of order, no gap appears.
  - *Reachable-state containment (iii):* `dom(A) ⊇ ⋃ { domₛ(A) : s reachable from s₀ }`. The reverse inclusion is a liveness statement not furnished by this ASN.
  - *Transfer of T9 to realized allocations:* for every reachable s, every activated A, and every pair `a, b ∈ domₛ(A)` with `a = tᵢ, b = tⱼ` and `i < j ≤ nₛ(A)`: `same_allocator(a, b)` (T10a) and `allocated_before(a, b)` (T9) hold by (i) and (ii), and T9's forward-ordering conclusion `a < b` applies to the pair.
- *Frame:* for every non-allocation-affecting (i.e., (T3)) transition `s → s'` and every `A ∈ 𝒯`, `activated(A, s) ≡ activated(A, s')` and, where activation holds, `domₛ(A) = domₛ'(A)`; thus `allocated(s) = allocated(s')`.
- *Depends:*
  - T0 (CarrierSetDefinition) — the carrier T of tumblers and the component-projection / length primitives used to index each allocator's chain.
  - T0(a) (UnboundedComponentValues) — component values are unbounded at every position, underwriting the inexhaustibility of the sibling `inc(·,0)` chain.
  - T0(b) (UnboundedLength) — tumbler length is unbounded, so allocator nesting via deep increments is not capped.
  - T9 (ForwardAllocation) — `allocated_before` ordering and per-allocator forward-ordering conclusion.
  - T10a (AllocatorDiscipline) — allocator tree 𝒯 with root, spawning triples `(parent(A), spawnPt(A), spawnParam(A))` and the `k' ∈ {1, 2}` child-spawning rule (used by admissibility shape (T2)), the per-allocator chain `dom(A) = {tₙ : n ≥ 0}`, and the at-most-once constraint on `(t, k')` pairs (forbids double spawning, so (T2) cannot fire twice for the same A).


---

## 7. Tumbler arithmetic

Tumbler arithmetic supports span computation and position advancement. Addition and subtraction are defined position-by-position with carry/borrow handling and a closure discipline that keeps results in T. Order is preserved (TA1, TA1-strict); subtraction's order behavior is asymmetric (TA3, TA3-strict). The arithmetic admits partial inverses (TA4), associativity (TA-assoc), and left cancellation (TA-LC); right cancellation fails (TA-RC). ZPD records the zero-positional-divider behavior.

### Tumbler arithmetic

The system requires an operation that advances a position by a displacement — for computing span endpoints and shifting positions. This operation is tumbler addition (⊕), constructed here as TumblerAdd. It is not arithmetic on numbers but a position-advance operation in a hierarchical address space. Its inverse — tumbler subtraction (⊖), which recovers the displacement between two positions — is constructed below as TumblerSub.

A displacement `w` is a tumbler whose leading zeros say "stay at these hierarchical levels" and whose first nonzero component says "advance here." Components after the advance point describe the structure of the landing position within the target region.

### Definition of ⊕

Tumbler addition is a **position-advance operation**: given a start position `a` and a displacement `w`, compute where you land. The displacement encodes both the distance and the hierarchical level at which the advance occurs.

```
START:  1.0.3.0.2.0.1.777
  DIF:  0.0.0.0.0.0.0.300
        ──────────────────
AFTER:  1.0.3.0.2.0.1.1077
```

Reading the displacement `[0,0,0,0,0,0,0,300]`: seven leading zeros mean "same server, same account, same document, same subspace." Component 8 is 300: "advance 300 elements." No trailing components: the landing position has no further sub-structure.

A displacement that acts at a higher level:

```
START:  1.0.3.0.2.0.1.777
  DIF:  0.0.0.0.3.0.1.1
        ──────────────────
AFTER:  1.0.3.0.5.0.1.1
```

Reading `[0,0,0,0,3,0,1,1]`: four leading zeros mean "same server, same account." Component 5 is 3: "advance 3 documents." Trailing `[0,1,1]`: "land at element 1.1 in the target document." The start position's element field `[1,777]` is replaced by the displacement's trailing structure `[1,1]`.

**TumblerAdd (TumblerAdd).** Let `a = [a₁, ..., aₘ]` and `w = [w₁, ..., wₙ]` with `a, w ∈ T` and `Pos(w)`. By ActionPoint, `k = actionPoint(w)` satisfies `1 ≤ k ≤ n` and `wₖ ≥ 1`. Require `k ≤ m`.

```
         ⎧ aᵢ           if i < k        (copy from start)
rᵢ   =  ⎨ aₖ + wₖ      if i = k        (single-component advance)
         ⎩ wᵢ           if i > k        (copy from displacement)
```

The result `a ⊕ w = [r₁, ..., rₚ]` has length `p = (k - 1) + 1 + (n - k) = n = #w`, where `k - 1 ∈ ℕ` and `n - k ∈ ℕ` are well-defined by NAT-sub's conditional closure under `k ≥ 1` and `n ≥ k`, and the collapses `(k - 1) + 1 = k` and `k + (n - k) = n` are NAT-sub's right- and left-inverse characterisations. Since `n ≥ 1`, the result has at least one component. *Result-length identity:* **`#(a ⊕ w) = #w`**.

Each component of the result is a natural number: for `i < k`, `rᵢ = aᵢ ∈ ℕ` since `a ∈ T` and `k ≤ m`; at the action point, `rₖ = aₖ + wₖ ∈ ℕ` by NAT-closure; for `i > k`, `rᵢ = wᵢ ∈ ℕ`. The map `i ↦ rᵢ` therefore assigns a natural number to each `i ∈ {j ∈ ℕ : 1 ≤ j ≤ p}`, and `p = n ≥ 1`; T0's comprehension clause, instantiated at length `p` and component map `r`, supplies a tumbler in T whose length is `p` and whose `i`-th component is `rᵢ`. Therefore **`a ⊕ w ∈ T`**.

*Strict advancement.* From `wₖ ≥ 1`, NAT-addcompat's left order-compatibility gives `aₖ + wₖ ≥ aₖ + 1`, and its strict successor inequality gives `aₖ + 1 > aₖ`. NAT-order's reverse-companion definitions rewrite these as `aₖ + 1 ≤ aₖ + wₖ` and `aₖ < aₖ + 1`. The `≤`-defining clause unfolds the first into the disjunction `aₖ + 1 < aₖ + wₖ ∨ aₖ + 1 = aₖ + wₖ`. *Strict branch:* `<`-transitivity composes `aₖ < aₖ + 1` and `aₖ + 1 < aₖ + wₖ` into `aₖ < aₖ + wₖ`. *Equality branch:* indiscernibility of `=` substitutes `aₖ + 1 = aₖ + wₖ` into `aₖ < aₖ + 1` to deliver `aₖ < aₖ + wₖ`. Both branches yield `aₖ < aₖ + wₖ`, i.e., `aₖ + wₖ > aₖ`, hence `rₖ > aₖ`. For `1 ≤ i < k`, `rᵢ = aᵢ`. Since `k ≤ #a` and `k ≤ #(a ⊕ w) = n`, T1 case (i) at divergence position `k` yields **`a ⊕ w > a`**.

*Dominance over displacement.* Since `#(a ⊕ w) = #w`, the T1 comparison reduces to finding the first `i` where `rᵢ ≠ wᵢ`. For `i < k`, `rᵢ = aᵢ` and `wᵢ = 0`. Case split on `(∃j ∈ [1, k-1] : aⱼ > 0)`:

*Case some `aⱼ > 0` for `j < k`.* NAT-wellorder applied to `{j : 1 ≤ j < k ∧ aⱼ > 0}` supplies the least such `j`. For `1 ≤ i < j`: `aᵢ = 0` by minimality of `j`, `wᵢ = 0` by ActionPoint, `rᵢ = aᵢ`, so `rᵢ = wᵢ = 0`. At `j`: `wⱼ = 0` by ActionPoint, `rⱼ = aⱼ > 0`, so `rⱼ > wⱼ`. The bound `j ≤ #w` follows from `j < k ≤ #w` via NAT-order. T1 case (i) at `j` yields `r > w`.

*Case `aᵢ = 0` for all `i < k`.* Then `rₖ = aₖ + wₖ`. Sub-case split on `aₖ > 0 ∨ aₖ = 0` from NAT-zero + NAT-order:
- If `aₖ > 0`: NAT-addcompat's right order-compatibility lifts `0 ≤ aₖ` into `aₖ + wₖ ≥ 0 + wₖ`; NAT-closure's additive identity rewrites this as `aₖ + wₖ ≥ wₖ`; NAT-cancel's symmetric summand absorption `n + m = m ⟹ n = 0`, instantiated at `n = aₖ, m = wₖ`, rules out equality (which would force `aₖ = 0`), so NAT-order delivers `aₖ + wₖ > wₖ`, i.e., `rₖ > wₖ`. T1 case (i) at `k` yields `r > w`.
- If `aₖ = 0`: `rₖ = wₖ` (via NAT-closure's additive identity); combined with `rᵢ = 0 = wᵢ` for `i < k` and `rᵢ = wᵢ` for `i > k`, every component agrees and `#r = #w`, so `r = w` by T3.

The strict branches discharge `r > w` via T1 case (i); the equality branch discharges `r = w` via T3. Their disjunction `r > w ∨ r = w` is **`a ⊕ w ≥ w`** by T1's `≥` abbreviation `a ≥ b ≡ b < a ∨ b = a`. ∎

Three properties of this definition — characterizations of what ⊕ does rather than postconditions to discharge — require explicit statement.

**No carry propagation:** The sum `aₖ + wₖ` at the action point is a single natural-number addition. There is no carry into position `k - 1`. This is why the operation is fast — constant time regardless of tumbler length.

**Tail replacement, not tail addition:** Components after the action point come entirely from `w`. The start position's components at positions `k + 1, ..., m` are discarded. `a ⊕ w` does not add corresponding components pairwise — it replaces the start's sub-structure with the displacement's sub-structure below the action point.

**The many-to-one property:** Because trailing components of `a` are discarded, distinct start positions can produce the same result:

```
[1, 1] ⊕ [0, 2]       = [1, 3]
[1, 1, 5] ⊕ [0, 2]    = [1, 3]
[1, 1, 999] ⊕ [0, 2]  = [1, 3]
```

This is correct and intentional: advancing to "the beginning of the next chapter" lands at the same place regardless of where you were within the current chapter.

*Formal Contract:*
- *Preconditions:* a ∈ T, w ∈ T, Pos(w), actionPoint(w) ≤ #a
- *Definition:* k = actionPoint(w); rᵢ = aᵢ if i < k; rₖ = aₖ + wₖ; rᵢ = wᵢ if i > k
- *Depends:*
  - T0 (CarrierSetDefinition) — comprehension clause, instantiated at result-length `p ≥ 1` and the component map `i ↦ rᵢ` valued in ℕ, discharges `a ⊕ w ∈ T`; component projection supplies `aⱼ, aₖ ∈ ℕ` for dichotomy sites.
  - NAT-closure (NatArithmeticClosureAndIdentity) — closure of ℕ under addition at `rₖ = aₖ + wₖ`; additive identity `0 + wₖ = wₖ` in the dominance proof.
  - NAT-addcompat (NatAdditionOrderAndSuccessor) — left order-compatibility and strict successor inequality for strict advancement; right order-compatibility for dominance sub-case `aₖ > 0`.
  - NAT-cancel (NatAdditionCancellation) — summand absorption symmetric form `n + m = m ⟹ n = 0`, instantiated at `n = aₖ, m = wₖ`, rules out `aₖ + wₖ = wₖ` in the dominance sub-case `aₖ > 0`.
  - NAT-zero (NatZeroMinimum) — lower bound `0 ≤ n` at dichotomy sites.
  - NAT-order (NatStrictTotalOrder) — defining clause unfolds `≤` at dichotomy and strict-promotion sites; transitivity composes bounds.
  - NAT-wellorder (NatWellOrdering) — least element of `{j : 1 ≤ j < k ∧ aⱼ > 0}` in the divergence sub-case.
  - NAT-sub (NatPartialSubtraction) — conditional closure of `k - 1` and `n - k`; right-inverse `(m − n) + n = m` at `(k − 1) + 1 = k` and left-inverse `n + (m − n) = m` at `k + (n − k) = n` collapse the result-length identity.
  - ActionPoint (ActionPoint) — bounds `1 ≤ k ≤ #w`, zeros-below-action-point `wᵢ = 0` for `i < k`, and `wₖ ≥ 1`.
  - TA-Pos (PositiveTumbler) — the predicate `Pos(w)` in the precondition.
  - T1 (LexicographicOrder) — case (i) at the divergence position for the strict-advancement postcondition and for the strict branches of dominance; `≥` abbreviation (`a ≥ b ≡ b < a ∨ b = a`) merges the dominance proof's strict and equality branches to deliver `a ⊕ w ≥ w`.
  - T3 (CanonicalRepresentation, this ASN) — equality sub-case of dominance concludes `r = w` from component-wise agreement and equal length.
- *Forward References:*
  - TumblerSub (TumblerSub) — the inverse operation, constructed below in this ASN; TumblerAdd's correctness does not depend on it.
- *Postconditions:* a ⊕ w ∈ T, #(a ⊕ w) = #w, a ⊕ w > a (T1), a ⊕ w ≥ w (T1, T3)

### Tumbler subtraction

**TumblerSub (TumblerSub).** Given two tumblers `a` (minuend) and `w` (subtrahend), compute their component-wise difference at the first point of zero-padded divergence. NAT-order's trichotomy on `(#a, #w)` selects exactly one of: (α) `#a = #w` with `L = #a`; (β) `#a < #w` with `L = #w`; (γ) `#w < #a` with `L = #a`. All component references at indices in `{1, ..., L}` use ZPD's *padded projections* `â`, `ŵ` (`âᵢ = aᵢ` for `1 ≤ i ≤ #a` and `âᵢ = 0` for `#a < i ≤ L`; symmetrically for `ŵ`), so that the bare native symbols `aᵢ`, `wᵢ` retain their T0 meaning on the native domain only. When `â` and `ŵ` agree at every position, the result is the zero tumbler of length `L`: `a ⊖ w = [0, ..., 0]`. Otherwise, `zpd(a, w)` is defined (ZPD) — write `k = zpd(a, w)`. The result is:

```
         ⎧ 0             if i < k
rᵢ   =  ⎨ âₖ - ŵₖ      if i = k
         ⎩ âᵢ           if i > k
```

The result has length `L`.

**Precondition:** `a ≥ w` (T1). We prove that when `zpd(a, w)` is defined, this entails `âₖ > ŵₖ` at `k = zpd(a, w)` — stated on the padded projections so the inequality is well-typed regardless of whether `k` lies in the native domain of both operands. Since zpd is defined, `a` and `w` are not zero-padded-equal (ZPD): the negation of `(A i : 1 ≤ i ≤ L : âᵢ = ŵᵢ)` supplies an index `i` with `1 ≤ i ≤ L` and `âᵢ ≠ ŵᵢ`. T3's contrapositive `a ≠ b ⟺ #a ≠ #b ∨ (∃ j : 1 ≤ j ≤ #a : aⱼ ≠ bⱼ)` speaks of native components and lengths only, so the padded disagreement does not by itself license `a ≠ w`; we discharge `a ≠ w` by case analysis on whether `i` lies in the shared native domain. (A) `i ≤ #a ∧ i ≤ #w`: ZPD's padded-projection definition gives `âᵢ = aᵢ` and `ŵᵢ = wᵢ`, hence `aᵢ ≠ wᵢ`; T3's contrapositive instantiated at `(a, w)` with witness `j := i` (legal since `1 ≤ i ≤ #a`) fires its existential disjunct, yielding `a ≠ w`. (B) `i > #a ∨ i > #w` with `i ≤ L`. Sub-case B1 (`i > #a`): ZPD's padding clause gives `âᵢ = 0`, so `âᵢ ≠ ŵᵢ` forces `ŵᵢ ≠ 0`, ruling out the padding clause `ŵᵢ = 0` (which would apply for `i > #w`) and fixing `i ≤ #w`; combined with `i > #a`, this yields `#a < i ≤ #w`, hence `#a ≠ #w`. Sub-case B2 (`i > #w`) is the mirror image: `ŵᵢ = 0` and the disagreement force `i ≤ #a`, giving `#w < #a` and `#a ≠ #w`. In both sub-cases, T3's contrapositive instantiated at `(a, w)` fires its length disjunct, yielding `a ≠ w`. In either case (A) or (B), `a ≠ w`; combined with `a ≥ w`, this yields `w < a` (T1). Two Divergence cases arise for the pair `(w, a)` with `w ≠ a`:

  (i) Component divergence at position `k` with `k ≤ #w ∧ k ≤ #a` and `wₖ ≠ aₖ` (native projections, well-defined since `k` lies in both native domains). ZPD's Relationship-to-Divergence gives `zpd(a, w) = divergence(a, w) = k`. From `w < a` (T1), a witness `j` exists in one of T1's two cases for the pair `(w, a)`. T1 case (ii) is eliminated: it would require `j = #w + 1 ≤ #a` with `wᵢ = aᵢ` for `1 ≤ i < j`, i.e., for `1 ≤ i ≤ #w`; instantiating this prefix agreement at `i := k` — legal since `k ≤ #w` from Divergence case (i) — yields `wₖ = aₖ`, contradicting `wₖ ≠ aₖ`. So T1 case (i) holds: `j ≤ #w ∧ j ≤ #a`, `wⱼ < aⱼ`, and `wᵢ = aᵢ` for `1 ≤ i < j`. NAT-order's disjointness-of-`<`-and-`=` at `(wⱼ, aⱼ)` converts `wⱼ < aⱼ` into `wⱼ ≠ aⱼ`, so the position `j` satisfies Divergence case (i)'s conjunction `1 ≤ j ∧ j ≤ #w ∧ j ≤ #a ∧ wⱼ ≠ aⱼ ∧ (A i : 1 ≤ i < j : wᵢ = aᵢ)` for the pair `(w, a)`; Divergence's uniqueness clause for case (i) identifies `j = k`. Hence `wₖ < aₖ`, whence `aₖ > wₖ`. ZPD's padded projections coincide with native here (`âₖ = aₖ` from `k ≤ #a`, `ŵₖ = wₖ` from `k ≤ #w`), lifting the inequality to `âₖ > ŵₖ`.

  (ii) Prefix divergence splits via NAT-order's trichotomy on `(#w, #a)` into sub-case (ii-a) `#w < #a` with `wᵢ = aᵢ` for `1 ≤ i ≤ #w` (native projections on the shared native domain), and sub-case (ii-b) `#a < #w` with `wᵢ = aᵢ` for `1 ≤ i ≤ #a`. Sub-case (ii-b) is eliminated by exhibiting a T1 case (ii) witness for `a < w` and contradicting `w < a`. Set `k := #a + 1`. T1 case (ii) for the pair `(a, w)` requires `k = #a + 1 ≤ #w`; NAT-discrete's forward direction `m < n ⟹ m + 1 ≤ n` instantiated at `(m, n) := (#a, #w)` bridges sub-case (ii-b)'s `#a < #w` to `#a + 1 ≤ #w`, discharging this clause. The prefix-agreement clause `(A i : 1 ≤ i < k : aᵢ = wᵢ)` reduces at `k = #a + 1` to `aᵢ = wᵢ` for `1 ≤ i ≤ #a`, supplied by sub-case (ii-b)'s `wᵢ = aᵢ` for `1 ≤ i ≤ #a` via symmetry of `=`. Hence `k = #a + 1` witnesses `a < w` via T1(ii), contradicting `w < a` through T1's trichotomy disjointness clause `¬(a < b ∧ b < a)` at `(a, w)`. In sub-case (ii-a), `w` is a proper prefix of `a`, so `L = #a`. ZPD's padded projection sets `ŵᵢ = 0` for `#w < i ≤ L` (and `ŵᵢ = wᵢ = aᵢ = âᵢ` for `1 ≤ i ≤ #w` by the prefix agreement). Since zpd is defined, `â` and `ŵ` disagree somewhere (ZPD, contrapositive); the prefix agreement rules out positions `1 ≤ i ≤ #w`, so the disagreement lies at some `i > #w`. By ZPD's minimality, `k > #w`, whence `ŵₖ = 0` by zero-padding and `âₖ ≠ 0`. From NAT-zero's `0 ≤ âₖ` and NAT-order's `m ≤ n ⟺ m < n ∨ m = n`, the divergence `âₖ ≠ 0` leaves `0 < âₖ`; hence `âₖ > 0 = ŵₖ`.

In both cases `âₖ > ŵₖ` at `k = zpd(a, w)`. When zpd is undefined, the consequence is vacuous.  ∎

Each component of the result is a natural number: for `i < k`, `rᵢ = 0 ∈ ℕ` by NAT-zero; at the divergence point, `rₖ = âₖ − ŵₖ ∈ ℕ` by NAT-sub, whose precondition `âₖ ≥ ŵₖ` follows from `âₖ > ŵₖ` via NAT-order; for `i > k`, `rᵢ = âᵢ`, which is `aᵢ ∈ ℕ` (T0) when `i ≤ #a` and `0 ∈ ℕ` (NAT-zero) when `i > #a`, by ZPD's padded-projection definition. In the no-divergence case every component is `0 ∈ ℕ`. The length `L ≥ 1` since T0 gives `#a ≥ 1` and `#w ≥ 1`, and `L` is named by the trichotomy as one of `#a` or `#w`. Hence **`a ⊖ w ∈ T`** by T0.

When `zpd(a, w)` is defined — write `k = zpd(a, w)` — components before `k` are zero by construction. To discharge TA-Pos we exhibit `k` as an index with `¬(rₖ = 0)`. NAT-sub's right-inverse characterisation, at `(âₖ, ŵₖ)` with precondition `âₖ ≥ ŵₖ` already established above from `âₖ > ŵₖ` via NAT-order, yields `(âₖ − ŵₖ) + ŵₖ = âₖ` — that is, `rₖ + ŵₖ = âₖ`. Suppose, for contradiction, `rₖ = 0`: NAT-closure's left additive identity instantiated at `n := ŵₖ` rewrites the left-hand side via `0 + ŵₖ = ŵₖ`, giving `ŵₖ = âₖ`. But `âₖ > ŵₖ` unfolds through NAT-order's `>` definition `m > n ⟺ n < m` to `ŵₖ < âₖ`, and NAT-order's disjointness-of-`<`-and-`=` clause applied at `(ŵₖ, âₖ)` then forces `ŵₖ ≠ âₖ`, contradicting `ŵₖ = âₖ`. Hence `¬(rₖ = 0)`. ZPD's codomain places `k` in `{1, ..., L}`, and `#(a ⊖ w) = L` gives `1 ≤ k ≤ #(a ⊖ w)`, so `k` is a valid existential witness; whence **`Pos(a ⊖ w)`** (TA-Pos). ActionPoint names `actionPoint(a ⊖ w)` as the unique `m ∈ S := {i : 1 ≤ i ≤ #(a ⊖ w) ∧ rᵢ ≠ 0}` with `(A n ∈ S :: m ≤ n)`; to identify this minimum with `k` we discharge both membership and the least-element clause. Membership: `1 ≤ k ≤ #(a ⊖ w)` and `rₖ ≠ 0` just established jointly give `k ∈ S`. Least-element: take any `n ∈ S` and suppose for contradiction `n < k`. The Definition fixes `rᵢ = 0` for every `i` with `1 ≤ i < k`; instantiating at `i := n` yields `rₙ = 0`, contradicting `rₙ ≠ 0` from `n ∈ S`. Hence `¬(n < k)`, and NAT-order's at-least-one trichotomy at `(k, n)` gives `k < n ∨ k = n ∨ n < k`; the excluded disjunct drops out, and NAT-order's defining clause `k ≤ n ⟺ k < n ∨ k = n` folds the remainder to `k ≤ n`. Hence `(A n ∈ S :: k ≤ n)`, and ActionPoint's uniqueness clause names `k` as the action point: **`actionPoint(a ⊖ w) = k = zpd(a, w)`**.

When `zpd(a, w)` is undefined, the Definition fixes `a ⊖ w = [0, …, 0]` of length `L`, so every component satisfies `rᵢ = 0` for `1 ≤ i ≤ L`. Using the postcondition `#(a ⊖ w) = L` to retype the index range, the universal `(A i ∈ ℕ : 1 ≤ i ≤ #(a ⊖ w) : rᵢ = 0)` holds, discharging **`Zero(a ⊖ w)`** (TA-Pos). TA-Pos's complementarity `Pos(t) ⟺ ¬Zero(t)` then yields `¬Pos(a ⊖ w)`, so the previous paragraph's Pos witness and ActionPoint identification are inapplicable here; ActionPoint's `Pos(w)` precondition fails at `w := a ⊖ w`, leaving `actionPoint(a ⊖ w)` unspecified.

*Formal Contract:*
- *Preconditions:* a ∈ T, w ∈ T, a ≥ w (T1).
- *Depends:*
  - T0 (CarrierSetDefinition) — carrier membership `a ⊖ w ∈ T` and per-operand length bounds `#a ≥ 1`, `#w ≥ 1`.
  - T1 (LexicographicOrder) — precondition ordering `a ≥ w`; trichotomy derives `w < a`; T1 case (ii) is eliminated in Divergence case (i) (its prefix-agreement range `1 ≤ i ≤ #w` instantiated at `i := k` would force `wₖ = aₖ`, contradicting `wₖ ≠ aₖ`) and in Divergence case (ii) sub-case (ii-b) (it yields `a < w`, contradicting `w < a`); in Divergence case (i), T1 case (i)'s witness `j` satisfies `wⱼ < aⱼ` and, once identified with `k` via Divergence's uniqueness, supplies `wₖ < aₖ`.
  - T3 (CanonicalRepresentation) — contrapositive `a ≠ b ⟺ #a ≠ #b ∨ (∃ j : 1 ≤ j ≤ #a : aⱼ ≠ bⱼ)` instantiated at `(a, w)` discharges `a ≠ w` from the not-zero-padded-equal hypothesis by case analysis on the padded-disagreement index `i`: case (A) (`i ≤ #a ∧ i ≤ #w`) fires the existential disjunct via ZPD's padded-projection equality (`âᵢ = aᵢ`, `ŵᵢ = wᵢ` lift `âᵢ ≠ ŵᵢ` to `aᵢ ≠ wᵢ`); case (B) (`i` in a padding zone) fires the length disjunct via NAT-order's trichotomy forcing `#a ≠ #w`.
  - Divergence — case analysis on the pair `(w, a)`; uniqueness clause for case (i) identifies T1 case (i)'s witness position `j` with the divergence index `k`.
  - ZPD — defines `zpd(a, w)`; padded-projection equality clauses `âᵢ = aᵢ` (for `1 ≤ i ≤ #a`) and `ŵᵢ = wᵢ` (for `1 ≤ i ≤ #w`) used in case (A) of the precondition's `a ≠ w` derivation to lift padded disagreement to native; padding clauses `âᵢ = 0` (for `#a < i ≤ L`) and `ŵᵢ = 0` (for `#w < i ≤ L`) used in case (B) to force the disagreement index into the longer operand's native domain; Relationship-to-Divergence identifies `zpd = divergence` under case (i); case-split and minimality under case (ii).
  - TA-Pos (PositiveTumbler) — defines `Pos` and `Zero` for the two conditional postconditions; the `Zero(a ⊖ w)` derivation in the no-divergence branch instantiates `Zero`'s Definition `(A i ∈ ℕ : 1 ≤ i ≤ #t : tᵢ = 0)` at `t := a ⊖ w`, discharging the universal from the per-component zeros `rᵢ = 0` supplied by the Definition's `a ⊖ w = [0, …, 0]` clause; complementarity `Pos(t) ⟺ ¬Zero(t)` then rules out `Pos(a ⊖ w)` in this branch, vacating ActionPoint's `Pos(w)` precondition.
  - ActionPoint — characterises `actionPoint(a ⊖ w)` as the unique least element of `S := {i : 1 ≤ i ≤ #(a ⊖ w) ∧ rᵢ ≠ 0}`; membership `k ∈ S` (from `1 ≤ k ≤ #(a ⊖ w)` and `rₖ ≠ 0`) and the least-element clause `(A n ∈ S :: k ≤ n)` (from the Definition's `rᵢ = 0` for `i < k`) jointly identify this minimum with `k`, yielding `actionPoint(a ⊖ w) = zpd(a, w)`.
  - NAT-sub (NatPartialSubtraction) — conditional closure `âₖ − ŵₖ ∈ ℕ` under `âₖ ≥ ŵₖ`; right-inverse characterisation `(âₖ − ŵₖ) + ŵₖ = âₖ` under `âₖ ≥ ŵₖ`, supplying the sum rewritten in the Pos derivation (instantiated on ZPD's padded projections so the operands are well-defined when `k` exceeds either native domain).
  - NAT-zero (NatZeroMinimum) — `0 ∈ ℕ` for ZPD's padded-projection clauses, `rᵢ = 0` components, and the zero-tumbler branch; lower bound `0 ≤ âₖ`.
  - NAT-order (NatStrictTotalOrder) — trichotomy on `(#a, #w)` naming `L`, reused in case (B) of the precondition's `a ≠ w` derivation where `L ∈ {#a, #w}` together with a padding-zone disagreement index (`i > #a` forcing `L = #w` and `#a < #w`, or `i > #w` forcing `L = #a` and `#w < #a`) witnesses `#a ≠ #w`; defining clause `≤ ⟺ < ∨ =` at `(0, âₖ)`; conversion `>` to `≥` at `(âₖ, ŵₖ)` for NAT-sub; disjointness-of-`<`-and-`=` at `(wⱼ, aⱼ)` in Divergence case (i) (native indices `j ≤ #w ∧ j ≤ #a`) converts T1 case (i)'s `wⱼ < aⱼ` into `wⱼ ≠ aⱼ`, qualifying the witness `j` for Divergence case (i)'s conjunction (whose uniqueness then identifies `j` with `k`); the `>` definition `m > n ⟺ n < m` at `(âₖ, ŵₖ)` and disjointness-of-`<`-and-`=` at `(ŵₖ, âₖ)` jointly discharge the Pos-derivation contradiction `ŵₖ ≠ âₖ` from `âₖ > ŵₖ`; at-least-one trichotomy at `(k, n)` together with the defining clause `≤ ⟺ < ∨ =` at `(k, n)` discharges the least-element clause `(A n ∈ S :: k ≤ n)` from `¬(n < k)`, identifying `k` as `actionPoint(a ⊖ w)` within ActionPoint's uniqueness.
  - NAT-closure (NatArithmeticClosureAndIdentity) — posits `1 ∈ ℕ` and closes ℕ under `+`, and fixes `0 + n = n`. The left-identity clause is instantiated at `n := ŵₖ` to rewrite `0 + ŵₖ = ŵₖ` in the Pos derivation, bridging the supposition `rₖ = 0` to the contradiction `ŵₖ = âₖ`.
  - NAT-discrete (NatDiscreteness) — forward direction `m < n ⟹ m + 1 ≤ n` instantiated at `(m, n) := (#a, #w)`, used in Divergence case (ii) sub-case (ii-b) to bridge the sub-case's hypothesis `#a < #w` to the T1 case (ii) condition `#a + 1 ≤ #w`, completing the exhibition of the T1(ii) witness `k = #a + 1` that yields `a < w` (which then contradicts `w < a` via T1's trichotomy disjointness clause and eliminates the sub-case).
- *Definition:* NAT-order's trichotomy on `(#a, #w)` selects exactly one of: (α) `#a = #w`, `L = #a`; (β) `#a < #w`, `L = #w`; (γ) `#w < #a`, `L = #a`. a ⊖ w is computed by case analysis on k = zpd(a, w) (ZPD) using ZPD's padded projections `â`, `ŵ` on `{1, ..., L}` for every component reference at indices that may exceed the native domain: rᵢ = 0 for i < k, rₖ = âₖ − ŵₖ, rᵢ = âᵢ for i > k; when zpd(a, w) is undefined, a ⊖ w = [0, …, 0]; #(a ⊖ w) = L.
- *Postconditions:* a ⊖ w ∈ T, #(a ⊖ w) = L (the longer of `#a` and `#w`, named by NAT-order trichotomy per the Definition); when zpd(a, w) is defined: â_{zpd(a,w)} > ŵ_{zpd(a,w)} (the divergence-point inequality on ZPD's padded projections, well-typed regardless of whether zpd(a, w) lies in either operand's native domain), Pos(a ⊖ w) (TA-Pos), actionPoint(a ⊖ w) = zpd(a, w) (ActionPoint); when zpd(a, w) is undefined: Zero(a ⊖ w) (TA-Pos).

**TA0 (WellDefinedAddition).** `(A a, w ∈ T : Pos(w) ∧ actionPoint(w) ≤ #a : a ⊕ w ∈ T ∧ #(a ⊕ w) = #w)`.

TA0 exports TumblerAdd's first two postconditions as a single labelled well-definedness fact. The precondition's bound `actionPoint(w) ≤ #a` carries the non-strict relation `≤` on ℕ, grounded by NAT-order via the definition `m ≤ n ⟺ m < n ∨ m = n`.

*Proof.* Immediate from TumblerAdd's first two postconditions `a ⊕ w ∈ T` and `#(a ⊕ w) = #w` under the preconditions `a, w ∈ T`, `Pos(w)`, `actionPoint(w) ≤ #a`. ∎

*Formal Contract:*
- *Preconditions:* a ∈ T, w ∈ T, Pos(w), actionPoint(w) ≤ #a
- *Depends:*
  - TumblerAdd (TumblerAdd, this ASN) — supplies `a ⊕ w ∈ T` and `#(a ⊕ w) = #w` as postconditions.
  - T0 (CarrierSetDefinition, this ASN) — supplies carrier `T` and length operator `#`.
  - TA-Pos (PositiveTumbler, this ASN) — precondition `Pos(w)` ensures the action point exists.
  - ActionPoint (ActionPoint, this ASN) — defines `actionPoint(w)` used in the bound `actionPoint(w) ≤ #a`.
  - NAT-order (NatStrictTotalOrder) — supplies the non-strict relation `≤` on ℕ appearing in the precondition `actionPoint(w) ≤ #a`.
- *Postconditions:* a ⊕ w ∈ T, #(a ⊕ w) = #w

**TA1 (OrderPreservationUnderAddition).** `(A a, b, w : a < b ∧ Pos(w) ∧ actionPoint(w) ≤ #a ∧ actionPoint(w) ≤ #b : a ⊕ w ≤ b ⊕ w)`.

TA1 guarantees weak order preservation: positions in order before advancement remain in non-reversed order after.

*Proof.* Let `k = actionPoint(w)`. By TumblerAdd, for any `t ∈ T` with `k ≤ #t`, the result `t ⊕ w` is built in three regions: `(t ⊕ w)ᵢ = tᵢ` for `i < k`, `(t ⊕ w)ₖ = tₖ + wₖ`, and `(t ⊕ w)ᵢ = wᵢ` for `i > k`. By TA0, both `a ⊕ w` and `b ⊕ w` are well-defined members of `T` with length `#w`.

By T1, `a < b` gives two cases: (i) there exists `j` with `j ≤ #a ∧ j ≤ #b` and `aⱼ < bⱼ` and `aᵢ = bᵢ` for `i < j`, or (ii) `#a < #b` and `aᵢ = bᵢ` for `1 ≤ i ≤ #a`.

*Case (ii).* The precondition gives `k ≤ #a` directly. For `i < k`: `(a ⊕ w)ᵢ = aᵢ = bᵢ = (b ⊕ w)ᵢ`. At `i = k`: `aₖ = bₖ` gives `(a ⊕ w)ₖ = aₖ + wₖ = bₖ + wₖ = (b ⊕ w)ₖ`. For `i > k`: `(a ⊕ w)ᵢ = wᵢ = (b ⊕ w)ᵢ`. Lengths agree by TA0, so `a ⊕ w = b ⊕ w` by T3.

*Case (i).* Three sub-cases on `j` vs `k`.

*Sub-case `j < k`.* For `i < j`: `(a ⊕ w)ᵢ = aᵢ = bᵢ = (b ⊕ w)ᵢ`. At `j`: `(a ⊕ w)ⱼ = aⱼ < bⱼ = (b ⊕ w)ⱼ`. Position `j` witnesses T1 case (i): `a ⊕ w < b ⊕ w`.

*Sub-case `j = k`.* For `i < k`: `(a ⊕ w)ᵢ = aᵢ = bᵢ = (b ⊕ w)ᵢ`. At `k`: we must derive `aₖ + wₖ < bₖ + wₖ` from `aₖ < bₖ`. By NAT-order, `aₖ < bₖ` yields `aₖ ≤ bₖ`. By NAT-addcompat right order-compatibility with `m = wₖ`, `aₖ + wₖ ≤ bₖ + wₖ`. If `aₖ + wₖ = bₖ + wₖ`, then NAT-cancel right cancellation yields `aₖ = bₖ`, contradicting `aₖ < bₖ` by NAT-order irreflexivity. Hence `aₖ + wₖ < bₖ + wₖ` by NAT-order. Position `k` witnesses T1 case (i): `a ⊕ w < b ⊕ w`.

*Sub-case `j > k`.* Since `k < j`, `aₖ = bₖ`. For `i < k`: `(a ⊕ w)ᵢ = aᵢ = bᵢ = (b ⊕ w)ᵢ`. At `k`: `(a ⊕ w)ₖ = aₖ + wₖ = bₖ + wₖ = (b ⊕ w)ₖ`. For `i > k`: `(a ⊕ w)ᵢ = wᵢ = (b ⊕ w)ᵢ`. Lengths agree by TA0, so `a ⊕ w = b ⊕ w` by T3.

In every case, `a ⊕ w ≤ b ⊕ w`. ∎

*Formal Contract:*
- *Preconditions:* a ∈ T, b ∈ T, w ∈ T, a < b, Pos(w), actionPoint(w) ≤ #a, actionPoint(w) ≤ #b
- *Depends:*
  - T0 (CarrierSetDefinition) — carrier `T`, length `#·`, component projection `·ᵢ`.
  - T1 (LexicographicOrder) — case analysis on `a < b`; case (i) concludes strict ordering of results.
  - T3 (CanonicalRepresentation) — component-wise agreement with equal length yields equality.
  - TA0 (WellDefinedAddition) — `a ⊕ w`, `b ⊕ w ∈ T` with length `#w`.
  - TumblerAdd (TumblerAdd) — three-region piecewise structure of `⊕`.
  - TA-Pos (PositiveTumbler, this ASN) — supplies `Pos(w)`.
  - ActionPoint (ActionPoint, this ASN) — defines `actionPoint(·)` and yields `1 ≤ k ≤ #w`.
  - NAT-order (NatStrictTotalOrder) — weakening `<` to `≤`, irreflexivity, and reconstructing strict `<` from `≤` plus non-equality.
  - NAT-addcompat (NatAdditionOrderAndSuccessor) — right order-compatibility lifts `aₖ ≤ bₖ` to `aₖ + wₖ ≤ bₖ + wₖ`.
  - NAT-cancel (NatAdditionCancellation) — right cancellation rules out `aₖ + wₖ = bₖ + wₖ`.
- *Postconditions:* a ⊕ w ≤ b ⊕ w

Strict order preservation holds under a tighter condition. We first need a precise notion of where two tumblers first differ.

**TA1-strict (StrictOrderPreservation).** `(A a, b, w ∈ T : a < b ∧ Pos(w) ∧ actionPoint(w) ≤ #a ∧ actionPoint(w) ≤ #b ∧ actionPoint(w) ≥ divergence(a, b) : a ⊕ w < b ⊕ w)`.

Tumbler addition by `w` preserves strict order when the action point of `w` lies at or beyond the first disagreement between `a` and `b`. If the action point falls before divergence, both operands receive the same advance and copy the same tail, collapsing the order to equality (e.g. `a = [1, 3]`, `b = [1, 5]`, `w = [2]` with action point 1 gives `a ⊕ w = [3] = b ⊕ w`).

*Proof.* From `a < b` and T1 irreflexivity, `a ≠ b`, discharging Divergence's precondition. Let `j = divergence(a, b)` and let `k` be the action point of `w`. The preconditions give `k ≥ j`, `k ≤ #a`, `k ≤ #b`.

Rule out Divergence case (ii). NAT-order trichotomy at `(#a, #b)` yields `#a = #b`, `#a < #b`, or `#b < #a`. The first makes case (ii) inapplicable. Under `#a < #b`, case (ii-a) gives `j = #a + 1`, so `k ≥ #a + 1` with `k ≤ #a` gives `#a + 1 ≤ #a`. NAT-order's defining clause unfolds this to `#a + 1 < #a ∨ #a + 1 = #a`. NAT-addcompat gives `#a < #a + 1`; the first disjunct composes to `#a + 1 < #a + 1` by transitivity, the second by substitution. NAT-order irreflexivity refutes both. The `#b < #a` branch is symmetric at `n = #b`. So Divergence case (i) holds: `1 ≤ j`, `j ≤ #a`, `j ≤ #b`, `aⱼ ≠ bⱼ`, and `aᵢ = bᵢ` for all `1 ≤ i < j`.

Align the T1 witness with `j`. Foreclose T1 case (ii) for `a < b`: its agreement requirement at `i = j ≤ #a` would force `aⱼ = bⱼ`, contradicting `aⱼ ≠ bⱼ`. So T1 case (i) supplies some `k'` with `1 ≤ k' ≤ #a, #b`, `aₖ' < bₖ'`, and `aᵢ = bᵢ` for `1 ≤ i < k'`. NAT-order trichotomy at `(k', j)`: in `k' < j`, Divergence agreement at `i = k'` gives `aₖ' = bₖ'`; substituted into `aₖ' < bₖ'` this yields `aₖ' < aₖ'`, refuted by NAT-order irreflexivity. In `k' > j`, T1 agreement at `i = j` gives `aⱼ = bⱼ`, contradicting Divergence. At `k' = j`, T1 case (i) delivers `aⱼ < bⱼ`.

Recall TumblerAdd: for tumbler `x`, positive `w`, action point `k ≤ #x`, `(x ⊕ w)ᵢ = xᵢ` for `i < k`, `(x ⊕ w)ₖ = xₖ + wₖ`, `(x ⊕ w)ᵢ = wᵢ` for `i > k`. By TA0, `a ⊕ w, b ⊕ w ∈ T` and `#(a ⊕ w) = #w = #(b ⊕ w)`.

*Case 1: `k = j`.* For `i < k`, Divergence agreement gives `aᵢ = bᵢ`, so `(a ⊕ w)ᵢ = (b ⊕ w)ᵢ`. At `k = j`, `(a ⊕ w)ₖ = aₖ + wₖ` and `(b ⊕ w)ₖ = bₖ + wₖ`. Promote `aₖ < bₖ` to `aₖ + wₖ < bₖ + wₖ`: NAT-order's defining clause weakens to `aₖ ≤ bₖ`; NAT-addcompat's right order-compatibility lifts to `aₖ + wₖ ≤ bₖ + wₖ`; NAT-cancel refutes `aₖ + wₖ = bₖ + wₖ` (it would force `aₖ = bₖ`, contradicting `aₖ < bₖ` via irreflexivity); the defining clause then yields the strict inequality. ActionPoint gives `k ≤ #w`, so `k ≤ #(a ⊕ w)` and `k ≤ #(b ⊕ w)`. By T1 case (i), `a ⊕ w < b ⊕ w`.

*Case 2: `k > j`.* For `i < j`, Divergence agreement with TumblerAdd's prefix-copy rule gives `(a ⊕ w)ᵢ = aᵢ = bᵢ = (b ⊕ w)ᵢ`. At `j < k`, prefix-copy gives `(a ⊕ w)ⱼ = aⱼ < bⱼ = (b ⊕ w)ⱼ`. The case assumption `k > j` with ActionPoint's `k ≤ #w` gives `j < #w` (transitivity on the strict disjunct, substitution on the equality disjunct); weakened to `j ≤ #w` and rewritten under TA0 to `j ≤ #(a ⊕ w)` and `j ≤ #(b ⊕ w)`. By T1 case (i), `a ⊕ w < b ⊕ w`.

In both cases, `a ⊕ w < b ⊕ w`. ∎

*Formal Contract:*
- *Preconditions:* a ∈ T, b ∈ T, w ∈ T, a < b, Pos(w), actionPoint(w) ≤ #a, actionPoint(w) ≤ #b, actionPoint(w) ≥ divergence(a, b)
- *Depends:*
  - T0 (CarrierSetDefinition) — carrier `T`, length operator `#·`, component projection `·ᵢ` with components in ℕ.
  - T1 (LexicographicOrder) — irreflexivity; case (i) witness and agreement; case (ii) structure.
  - T3 (CanonicalRepresentation) — backs Divergence's exhaustiveness at the case-(ii) rule-out.
  - Divergence — supplies `j`, case (i) agreement and disagreement, case (ii) sub-case length structure.
  - TA-Pos (PositiveTumbler) — `Pos(w)` consumed by ActionPoint and TA0.
  - ActionPoint — fixes `k`; supplies `1 ≤ k ≤ #w`.
  - TA0 (WellDefinedAddition) — `a ⊕ w, b ⊕ w ∈ T`; length identity `#(a ⊕ w) = #w`.
  - TumblerAdd — constructive component-wise definition.
  - NAT-order (NatStrictTotalOrder) — trichotomy; defining clause `m ≤ n ⟺ m < n ∨ m = n`; transitivity of `<`; irreflexivity.
  - NAT-addcompat (NatAdditionOrderAndSuccessor) — strict successor `n < n + 1`; right order-compatibility `p ≤ n ⟹ p + m ≤ n + m`.
  - NAT-cancel (NatAdditionCancellation) — right cancellation `n + m = p + m ⟹ n = p`.
- *Postconditions:* a ⊕ w < b ⊕ w

### Subtraction for width computation

Let `⊖` denote tumbler subtraction: given two positions, compute the displacement between them.

**TA2 (WellDefinedSubtraction).** For tumblers `a, w ∈ T` where `a ≥ w`, `a ⊖ w` is a well-defined tumbler in `T`.

*Proof.* By TumblerSub, subtraction zero-pads both operands to length `L`, where `L = #a` if `#a ≥ #w` and `L = #w` otherwise (by NAT-order trichotomy on `(#a, #w)`), then scans for the first position at which the padded sequences disagree.

*Case 1: no divergence.* The padded sequences of `a` and `w` agree at every position. TumblerSub produces `[0, ..., 0]` of length `L`. Since `#a ≥ 1` and `#w ≥ 1` by T0, `L ≥ 1`. Each component is `0 ∈ ℕ` by NAT-zero. Hence the result is in T.

*Case 2: divergence at position `k`.* TumblerSub defines `r = a ⊖ w` componentwise on ZPD's padded projections `â`, `ŵ`: `rᵢ = 0` for `i < k`, `rₖ = âₖ - ŵₖ`, `rᵢ = âᵢ` for `i > k`, with `#r = L`.

*Pre-divergence* (`i < k`): `rᵢ = 0 ∈ ℕ` by NAT-zero.

*Divergence point* (`i = k`): We must establish `a ≠ w` before T1 can fire, and T3 speaks of native components and lengths only — a padded disagreement at `k` does not invoke T3 directly. We argue by reductio. Suppose `a = w`. T3, instantiated at `(a, w)`, then yields `#a = #w` and `aᵢ = wᵢ` for `1 ≤ i ≤ #a`. NAT-order's trichotomy on `(#a, #w)` selects the equality case, so `L = #a = #w` and the padded domain `[1, L]` coincides with both native domains. By ZPD's padded-projection definition, for every `i` with `1 ≤ i ≤ L`, `âᵢ = aᵢ` (since `i ≤ #a`) and `ŵᵢ = wᵢ` (since `i ≤ #w`); hence `âᵢ = aᵢ = wᵢ = ŵᵢ`, so the padded sequences agree everywhere on `[1, L]`, contradicting Case 2's hypothesis that ZPD identifies a padded divergence at some `k ≤ L`. Therefore `a ≠ w`, and combined with `a ≥ w` this gives `a > w` under T1.

- *Sub-case (i): T1 component divergence.* There exists a first position `j` with `j ≤ #a ∧ j ≤ #w`, `aⱼ > wⱼ`, and `aᵢ = wᵢ` for all `i < j` (native projections, well-defined on the shared native domain). By ZPD's minimality, `k = j`. At `k`, `aₖ > wₖ`; since `k ≤ #a ∧ k ≤ #w` the padded projections coincide with native (`âₖ = aₖ`, `ŵₖ = wₖ`), giving `âₖ > ŵₖ`, so `âₖ ≥ ŵₖ` by NAT-order, and NAT-sub yields `rₖ = âₖ - ŵₖ ∈ ℕ`.

- *Sub-case (ii): T1 prefix relationship.* `w` is a proper prefix of `a`: `#w < #a` and `aᵢ = wᵢ` for `i ≤ #w` (native). ZPD's padded projection `ŵ` extends `w` with zeros (NAT-zero) at positions `#w + 1` through `L = #a`. Some position `i > #w` has `âᵢ ≠ 0` (with `âᵢ = aᵢ` from `i ≤ #a`), else the padded sequences would agree. By ZPD's minimality, `k = min{i : #w < i ≤ L ∧ âᵢ ≠ 0}`. At `k`, `âₖ ≠ 0 = ŵₖ`. From NAT-zero's `0 ≤ âₖ` and NAT-order's `m ≤ n ⟺ m < n ∨ m = n`, the `âₖ = 0` disjunct is excluded, yielding `âₖ > 0 = ŵₖ`. Then `âₖ ≥ ŵₖ` by NAT-order, and NAT-sub yields `rₖ = âₖ - ŵₖ ∈ ℕ`.

*Tail* (`i > k`): `rᵢ = âᵢ`. If `i ≤ #a`, `âᵢ = aᵢ ∈ ℕ` by T0. If `i > #a`, `âᵢ = 0 ∈ ℕ` by NAT-zero.

The result has length `L ≥ 1` (since `#a ≥ 1` and `#w ≥ 1` by T0) with every component in ℕ, hence in T. ∎

*Formal Contract:*
- *Preconditions:* a ∈ T, w ∈ T, a ≥ w
- *Depends:*
  - TumblerSub (TumblerSub) — piecewise construction of `a ⊖ w`: zero-padding, divergence-based case split, componentwise definition, and result length `L`.
  - T0 (CarrierSetDefinition) — minimum-length `≥ 1`, component-typing in ℕ, and carrier-set membership criterion.
  - T1 (LexicographicOrder) — derives `a > w` from `a ≥ w ∧ a ≠ w`; supplies component-divergence and prefix cases at the divergence point.
  - T3 (CanonicalRepresentation) — `a = w` iff same length and components; used in a reductio at the divergence point: assuming `a = w` propagates equal lengths and native component equality, which under NAT-order's equality case on `(#a, #w)` extends via ZPD's padded-projection definition to padded equality on `[1, L]`, contradicting Case 2's padded divergence at `k`.
  - ZPD (ZeroPaddedDivergence) — minimality property identifying `k = zpd(a, w)` in both sub-cases.
  - NAT-sub (NatPartialSubtraction) — conditional-closure clause discharging `rₖ ∈ ℕ` once `âₖ ≥ ŵₖ` (instantiated on ZPD's padded projections so the operands are well-defined when `k > #w`).
  - NAT-zero (NatZeroMinimum) — supplies `0 ∈ ℕ` for literal zeros (pre-divergence components, ZPD's padded extension of `a` past `#a`, ZPD's padded extension of `w` past `#w`, and the zero tumbler of Case 1); lower bound `0 ≤ âₖ` for the `≠ 0 ⟹ > 0` step.
  - NAT-order (NatStrictTotalOrder) — trichotomy on `(#a, #w)` naming `L`; defining clause `m ≤ n ⟺ m < n ∨ m = n` used to convert strict inequalities into weak form for NAT-sub and to unfold `0 ≤ âₖ` in sub-case (ii).
- *Postconditions:* a ⊖ w ∈ T, #(a ⊖ w) = L where `L = #a` if `#a ≥ #w`, else `L = #w`.

**TA3 (OrderPreservationUnderSubtractionWeak).** `(A a, b, w : a < b ∧ a ≥ w ∧ b ≥ w : a ⊖ w ≤ b ⊖ w)`.

*Proof.* We show that for all `a, b, w ∈ T` with `a < b`, `a ≥ w`, `b ≥ w`, we have `a ⊖ w ≤ b ⊖ w`.

By TA2, `a ⊖ w` and `b ⊖ w` are well-formed tumblers in `T`. Recall TumblerSub: given `x ≥ w`, zero-pad both operands to `L_{x,w}` (the longer of `#x`, `#w`, dispatched by NAT-order's trichotomy on `(#x, #w)`) and scan for the first disagreement. If none exists, `x ⊖ w` is the zero tumbler of length `L_{x,w}`. Otherwise, let `d` be the first divergence; then `(x ⊖ w)ᵢ = 0` for `i < d`, `(x ⊖ w)_d = x_d - w_d`, and `(x ⊖ w)ᵢ = xᵢ` for `i > d`, with result length `L_{x,w}`.

Since `a < b`, T1 provides two cases: (i) there exists a first position `j` with `j ≤ #a ∧ j ≤ #b` where `aⱼ < bⱼ`, or (ii) `a` is a proper prefix of `b`.

**Case A: `a` is a proper prefix of `b`** (T1 case (ii)). Then `#a < #b` and `aᵢ = bᵢ` for all `i ≤ #a`.

*Sub-case A1: `a = w`.* NAT-order's trichotomy on `(#a, #w)` gives `L_{a,w} = #a`; `a ⊖ w` is the zero tumbler of that length. Since `a` is a proper prefix of `b` and `a = w`, `bᵢ = wᵢ` for all `i ≤ #w = #a`. If some `bᵢ` with `i > #w` is nonzero, `(b, w)` diverges beyond `#w`, making `b ⊖ w` positive; by TA-PosDom, `a ⊖ w < b ⊖ w`. Otherwise, the zero-padded sequences of `b` and `w` agree everywhere, and under `#w = #a < #b` NAT-order places `(#b, #w)` in sub-case (γ), giving `L_{b,w} = #b`; `b ⊖ w` is the zero tumbler of length `#b`. Both results are zero, agreeing on positions `1, ..., #a`; the strict length inequality `#a < #b` is converted by NAT-discrete into `#a + 1 ≤ #b` (with `#a + 1 ∈ ℕ` by NAT-closure), supplying T1 case (ii)'s witness. Thus `a ⊖ w < b ⊖ w` by T1 case (ii).

*Sub-case A2: `a > w` with divergence.* Let `dₐ = zpd(a, w)`; ZPD's codomain places `dₐ ≤ L_{a,w}`. TumblerSub's exported postcondition applied to `(a, w)` under `a ≥ w` gives `â_{dₐ} > ŵ_{dₐ}` on ZPD's padded projections. We claim `dₐ ≤ #a`: suppose for contradiction `dₐ > #a`; then `#a < dₐ ≤ L_{a,w}`, and ZPD's padding clause `âᵢ = 0` for `#a < i ≤ L_{a,w}` instantiated at `i := dₐ` gives `â_{dₐ} = 0`. Substituting into `â_{dₐ} > ŵ_{dₐ}` yields `0 > ŵ_{dₐ}`, i.e., `ŵ_{dₐ} < 0` by NAT-order's `>` definition `m > n ⟺ n < m`, contradicting NAT-zero's lower bound `0 ≤ ŵ_{dₐ}` via NAT-order's trichotomy. Hence `¬(dₐ > #a)`; NAT-order's trichotomy at `(dₐ, #a)` together with its defining clause `≤ ⟺ < ∨ =` yields `dₐ ≤ #a`. Since `#a < #b`, also `dₐ ≤ #b`. Case A's prefix agreement `bᵢ = aᵢ` for `i ≤ #a` lifts through ZPD's padded-projection equality on the native domain (`âᵢ = aᵢ` from `i ≤ #a`, `b̂ᵢ = bᵢ` from `i ≤ #a ≤ #b`) to give `âᵢ = b̂ᵢ` for `1 ≤ i ≤ #a`. Chaining at `i < dₐ` with ZPD's pre-divergence agreement `âᵢ = ŵᵢ` for `(a, w)` yields `b̂ᵢ = ŵᵢ` for `i < dₐ`; at `i = dₐ`, ZPD's first-disagreement `â_{dₐ} ≠ ŵ_{dₐ}` combined with `â_{dₐ} = b̂_{dₐ}` gives `b̂_{dₐ} ≠ ŵ_{dₐ}`. By ZPD's minimality, `d_b = dₐ`; write `d = dₐ = d_b`.

At positions `i < d`, TumblerSub's Definition gives `(a ⊖ w)ᵢ = (b ⊖ w)ᵢ = 0`. At position `d`: TumblerSub's Definition gives `(a ⊖ w)_d = â_d - ŵ_d` and `(b ⊖ w)_d = b̂_d - ŵ_d` — well-typed on ZPD's padded projections regardless of whether `d` exceeds `#w` in the prefix-divergence sub-case. Both differences are in ℕ by NAT-sub's conditional closure under `â_d ≥ ŵ_d` and `b̂_d ≥ ŵ_d`, supplied by TumblerSub's exported postconditions `â_d > ŵ_d` (applied to `(a, w)` under `a ≥ w`) and `b̂_d > ŵ_d` (applied to `(b, w)` under `b ≥ w`) via NAT-order. Equality of the two divergence-point components follows from `â_d = b̂_d` (just established). At positions `d < i ≤ #a`: TumblerSub's Definition gives `(a ⊖ w)ᵢ = âᵢ` and `(b ⊖ w)ᵢ = b̂ᵢ`; with `i ≤ #a ≤ #b`, ZPD's padded-projection equality lifts to native (`âᵢ = aᵢ`, `b̂ᵢ = bᵢ`), and Case A's prefix agreement gives `aᵢ = bᵢ`, hence `(a ⊖ w)ᵢ = (b ⊖ w)ᵢ`. The results agree on `1, ..., #a`.

Denote result lengths `L_{a,w}`, `L_{b,w}`. We establish `L_{a,w} ≤ L_{b,w}` by enumerating NAT-order's trichotomy on `(#a, #w)`. In (α) or (γ), `L_{a,w} = #a`; with `#a < #b`, `(#b, #w)` is in (γ), giving `L_{b,w} = #b > #a`. In (β) `#a < #w`, `L_{a,w} = #w`; NAT-order on `(#b, #w)` gives `L_{b,w} ∈ {#b, #w}` with `L_{b,w} ≥ #w = L_{a,w}`.

At positions `#a < i ≤ L_{a,w}` (only in sub-case (β), where `L_{a,w} = #w`): TumblerSub's Definition gives `(a ⊖ w)ᵢ = âᵢ`, and ZPD's padding clause for `â` at `i > #a` gives `âᵢ = 0`; likewise `(b ⊖ w)ᵢ = b̂ᵢ`, which equals `bᵢ` if `i ≤ #b` (ZPD's padded-projection equality) and `0` if `i > #b` (ZPD's padding clause) — in either case, NAT-zero's lower bound `0 ≤ b̂ᵢ` gives `âᵢ ≤ b̂ᵢ`, hence `(a ⊖ w)ᵢ ≤ (b ⊖ w)ᵢ`.

If a first disagreement exists at `p ∈ 1, ..., L_{a,w}`, then `p > #a` and `(a ⊖ w)_p = 0`, `(b ⊖ w)_p ≠ 0`. By NAT-zero's lower bound and NAT-order's defining clause, `(b ⊖ w)_p > 0`. Position `p` satisfies `p ≤ L_{a,w} ∧ p ≤ L_{b,w}`, so T1 case (i) yields `a ⊖ w < b ⊖ w`. If no disagreement exists, NAT-order's trichotomy at `(L_{a,w}, L_{b,w})` with `L_{a,w} ≤ L_{b,w}` fixes either `L_{a,w} < L_{b,w}` or `L_{a,w} = L_{b,w}`. In the strict case, NAT-discrete gives `L_{a,w} + 1 ≤ L_{b,w}` (with closure by NAT-closure), so `a ⊖ w` is a proper prefix of `b ⊖ w` by T1 case (ii). In the equal case, T3 yields `a ⊖ w = b ⊖ w`.

*Sub-case A3: `a > w` without divergence (zero-padded equality).* The only possibility is T1 case (ii): `w` is a proper prefix of `a` with `aᵢ = 0` for all `i > #w`. NAT-order on `(#a, #w)` is sub-case (γ), giving `L_{a,w} = #a`; `a ⊖ w` is the zero tumbler of that length. Since `#w < #a < #b`, NAT-order on `(#b, #w)` is sub-case (γ), giving `L_{b,w} = #b`. By TA-Pos's complementarity, `b ⊖ w` is either positive or a zero tumbler. If positive, `a ⊖ w < b ⊖ w` by TA-PosDom. If a zero tumbler, both results are zero; NAT-discrete converts `#a < #b` into `#a + 1 ≤ #b`, supplying T1 case (ii)'s witness. Thus `a ⊖ w < b ⊖ w`.

**Case B: Component divergence at `j`** (T1 case (i)). There exists a first position `j` with `j ≤ #a ∧ j ≤ #b`, `aⱼ < bⱼ`, and `aᵢ = bᵢ` for all `i < j`.

*Sub-case B1: `a` is zero-padded-equal to `w`.* TumblerSub's no-divergence branch fixes `a ⊖ w = [0, …, 0]` of length `L_{a,w}`, hence `Zero(a ⊖ w)` by TA-Pos's Definition. We show `(b, w)` is not zero-padded-equal, supplying TumblerSub's exported `Pos` postcondition for `b ⊖ w`. NAT-order's trichotomy on `(#a, #w)` places `L_{a,w}` in `{#a, #w}` with `L_{a,w} ≥ #a` in each branch ((β) supplies `#a < #w = L_{a,w}`); analogously, `L_{b,w} ≥ #b`. Case B's witness `j ≤ #a ∧ j ≤ #b ∧ aⱼ < bⱼ` therefore gives `j ≤ L_{a,w}` and `j ≤ L_{b,w}`. ZPD's padded-projection equality (legal at `j ≤ #a`) gives `âⱼ = aⱼ`; a's zero-padded-equality instantiated at `j ≤ L_{a,w}` yields `âⱼ = ŵⱼ`, hence `aⱼ = ŵⱼ`. NAT-order's trichotomy at `(j, #w)` splits into two cases. (i) `j ≤ #w`: ZPD's padded-projection equality at `j ≤ #w` gives `ŵⱼ = wⱼ`, so `aⱼ = wⱼ`; substituting into `aⱼ < bⱼ` yields `wⱼ < bⱼ`, and NAT-order's disjointness-of-`<`-and-`=` at `(wⱼ, bⱼ)` gives `wⱼ ≠ bⱼ`. ZPD's padded-projection equalities `b̂ⱼ = bⱼ` (from `j ≤ #b`) and `ŵⱼ = wⱼ` lift this to `b̂ⱼ ≠ ŵⱼ`. (ii) `j > #w`: ZPD's padding clause for `ŵ` in the `(a, w)` context (legal since `#w < j ≤ L_{a,w}`) gives `ŵⱼ = 0`, so `aⱼ = 0`; substituting into `aⱼ < bⱼ` yields `0 < bⱼ`, and NAT-order's disjointness-of-`<`-and-`=` at `(0, bⱼ)` gives `bⱼ ≠ 0`. ZPD's padded-projection equality `b̂ⱼ = bⱼ` (from `j ≤ #b`) together with ZPD's padding clause for `ŵ` in the `(b, w)` context (legal since `#w < j ≤ L_{b,w}`) gives `b̂ⱼ = bⱼ ≠ 0 = ŵⱼ`. In either case, `b̂ⱼ ≠ ŵⱼ` at `1 ≤ j ≤ L_{b,w}`, so `(b, w)` is not zero-padded-equal (ZPD's existence biconditional, contrapositive); hence `zpd(b, w)` is defined, and TumblerSub's exported `Pos` postcondition under `b ≥ w` gives `Pos(b ⊖ w)`. By TA-PosDom, `a ⊖ w < b ⊖ w`.

For the remaining sub-cases, `dₐ = zpd(a, w)` is well-defined, so TumblerSub's exported postcondition applied to `(a, w)` under `a ≥ w` gives `â_{dₐ} > ŵ_{dₐ}` (on ZPD's padded projections, since `dₐ` may exceed `#w` in the prefix-divergence sub-case); ZPD's codomain places `dₐ ≤ L_{a,w}`. We derive `dₐ ≤ #a` directly: suppose for contradiction `dₐ > #a`; then `#a < dₐ ≤ L_{a,w}`, and ZPD's padding clause `âᵢ = 0` for `#a < i ≤ L_{a,w}` instantiated at `i := dₐ` gives `â_{dₐ} = 0`. Substituting into `â_{dₐ} > ŵ_{dₐ}` yields `0 > ŵ_{dₐ}`, i.e., `ŵ_{dₐ} < 0` by NAT-order's `>` definition `m > n ⟺ n < m`, contradicting NAT-zero's lower bound `0 ≤ ŵ_{dₐ}` via NAT-order's trichotomy. Hence `¬(dₐ > #a)`; NAT-order's trichotomy at `(dₐ, #a)` together with its defining clause `≤ ⟺ < ∨ =` yields `dₐ ≤ #a`.

The zero-padded divergence `d_b = zpd(b, w)` is also well-defined: were `b` zero-padded-equal to `w`, ZPD's padded equality `(A i : 1 ≤ i ≤ L_{b,w} : b̂ᵢ = ŵᵢ)` would hold throughout `1..L_{b,w}`. NAT-order's trichotomy on `(#b, #w)` places `L_{b,w}` in `{#b, #w}` with `L_{b,w} ≥ #b` in each branch (in (β), `#b < #w = L_{b,w}`); Case B's witness `j ≤ #b` therefore gives `j ≤ L_{b,w}`, so the hypothesised equality at `j` yields `b̂ⱼ = ŵⱼ`. ZPD's padded-projection equality at `j ≤ #b` gives `b̂ⱼ = bⱼ`, hence `bⱼ = ŵⱼ`. NAT-order's trichotomy at `(j, #w)` splits into two cases. (i) `j ≤ #w`: ZPD's padded-projection equality at `j ≤ #w` gives `ŵⱼ = wⱼ`, so `bⱼ = wⱼ`; substituting into Case B's witness `aⱼ < bⱼ` yields `aⱼ < wⱼ`. For `i < j`, the hypothesised equality at `i ≤ L_{b,w}` (legal since `i < j ≤ L_{b,w}`) gives `b̂ᵢ = ŵᵢ`; ZPD's padded-projection equalities at `i < j ≤ #b` and `i < j ≤ #w` lift this to `bᵢ = wᵢ`, and Case B's pre-`j` agreement `aᵢ = bᵢ` chains to `aᵢ = wᵢ`. Thus `j ≤ #a ∧ j ≤ #w ∧ aⱼ < wⱼ` together with `aᵢ = wᵢ` for `i < j` is T1 case (i)'s witness for `a < w` — contradicting `a ≥ w` via T1's trichotomy clause `¬(a < w ∧ w ≤ a)`. (ii) `j > #w`: ZPD's padding clause for `ŵ` at `#w < j ≤ L_{b,w}` gives `ŵⱼ = 0`, so `bⱼ = 0`; substituting into Case B's witness `aⱼ < bⱼ` yields `aⱼ < 0`, contradicting NAT-zero's lower bound `0 ≤ aⱼ`. In either case the hypothesis is refuted, so `(b, w)` is not zero-padded-equal; ZPD's existence biconditional then makes `d_b = zpd(b, w)` well-defined.

By the symmetric direct argument for `(b, w)` with `b ≥ w` and `d_b` defined: TumblerSub's exported postcondition gives `b̂_{d_b} > ŵ_{d_b}` on ZPD's padded projections, and ZPD's codomain places `d_b ≤ L_{b,w}`. Suppose for contradiction `d_b > #b`; then `#b < d_b ≤ L_{b,w}`, and ZPD's padding clause `b̂ᵢ = 0` for `#b < i ≤ L_{b,w}` instantiated at `i := d_b` gives `b̂_{d_b} = 0`. Substituting into `b̂_{d_b} > ŵ_{d_b}` yields `0 > ŵ_{d_b}`, i.e., `ŵ_{d_b} < 0` by NAT-order's `>` definition, contradicting NAT-zero's lower bound `0 ≤ ŵ_{d_b}` via NAT-order's trichotomy. Hence `d_b ≤ #b` (NAT-order's trichotomy at `(d_b, #b)` with its defining clause `≤ ⟺ < ∨ =`).

NAT-order's trichotomy on `(dₐ, d_b)` partitions into three sub-cases.

*Sub-case B2: `dₐ = d_b = d`.* TumblerSub's exported postcondition applied to `(a, w)` and `(b, w)` gives `â_d > ŵ_d` and `b̂_d > ŵ_d`, hence `â_d, b̂_d ≥ ŵ_d` by NAT-order. The preamble's hypothesis-free `dₐ ≤ #a` and `d_b ≤ #b`, with `dₐ = d_b = d`, give `d ≤ #a ∧ d ≤ #b`, letting padded projections coincide with native at `d` and earlier (`â_d = a_d`, `b̂_d = b_d`, and `âᵢ = aᵢ`, `b̂ᵢ = bᵢ` for `i ≤ d`). For `i < d`, both results are zero. ZPD's pre-divergence agreements give `âᵢ = ŵᵢ = b̂ᵢ` for `i < d`, lifting to `aᵢ = bᵢ`; combined with Case B's witness `aⱼ < bⱼ`, this forces `j ≥ d`. If `j = d`: NAT-sub's strict monotonicity at `â_d < b̂_d` (from `a_d < b_d`) with both `≥ ŵ_d` yields `â_d - ŵ_d < b̂_d - ŵ_d`, so `(a ⊖ w)_d < (b ⊖ w)_d`; with both results zero on `i < d`, T1 case (i) gives `a ⊖ w < b ⊖ w`. If `j > d`: Case B's pre-`j` agreement gives `a_d = b_d`, so the divergence-point components `â_d - ŵ_d` and `b̂_d - ŵ_d` are identical; at `d < i < j`, with `i < j ≤ #a ∧ ≤ #b`, both copy matching minuend components (`âᵢ = aᵢ = bᵢ = b̂ᵢ`); at `j`, `(a ⊖ w)ⱼ = âⱼ = aⱼ < bⱼ = b̂ⱼ = (b ⊖ w)ⱼ`. By T1 case (i), `a ⊖ w < b ⊖ w`.

*Sub-case B3: `dₐ < d_b`.* ZPD's first-disagreement characterisation gives `â_{dₐ} ≠ ŵ_{dₐ}`; ZPD's pre-divergence agreement for `(b, w)` at `dₐ < d_b` gives `b̂_{dₐ} = ŵ_{dₐ}`; chaining, `â_{dₐ} ≠ b̂_{dₐ}`. The preamble's `dₐ ≤ #a` together with `dₐ < d_b ≤ #b` (NAT-order's transitivity composing `dₐ < d_b` with the preamble's `d_b ≤ #b`) give `dₐ ≤ #a ∧ dₐ ≤ #b`, letting padded projections coincide with native at `dₐ` and earlier; pre-divergence agreement for `(a, w)` chained through `ŵ` gives `âᵢ = b̂ᵢ` for `i < dₐ`, lifting to `aᵢ = bᵢ`, and `â_{dₐ} ≠ b̂_{dₐ}` lifts to `a_{dₐ} ≠ b_{dₐ}`. Case B's first-disagreement witness `aⱼ < bⱼ` then fixes `j = dₐ` with `a_{dₐ} < b_{dₐ}`, hence `â_{dₐ} < b̂_{dₐ} = ŵ_{dₐ}`. But TumblerSub's exported postcondition applied to `(a, w)` under `a ≥ w` gives `â_{dₐ} > ŵ_{dₐ}` — contradicting `â_{dₐ} < ŵ_{dₐ}`. This case is impossible.

*Sub-case B4: `dₐ > d_b`.* ZPD's pre-divergence agreement for `(a, w)` at `d_b < dₐ` gives `â_{d_b} = ŵ_{d_b}`; ZPD's first-disagreement characterisation for `(b, w)` gives `b̂_{d_b} ≠ ŵ_{d_b}`; chaining, `â_{d_b} ≠ b̂_{d_b}`. The preamble's `d_b ≤ #b` together with `d_b < dₐ ≤ #a` (NAT-order's transitivity composing `d_b < dₐ` with the preamble's `dₐ ≤ #a`) give `d_b ≤ #a ∧ d_b ≤ #b`, so padded projections coincide with native at `d_b` and earlier, giving `aᵢ = bᵢ` for `i < d_b` (chained through `ŵᵢ`) and `a_{d_b} ≠ b_{d_b}`. Case B's first-disagreement witness `aⱼ < bⱼ` fixes `j = d_b` with `a_{d_b} < b_{d_b}`. TumblerSub's exported postcondition applied to `(b, w)` under `b ≥ w` gives `b̂_{d_b} > ŵ_{d_b}`, so `(b ⊖ w)_{d_b} = b̂_{d_b} - ŵ_{d_b} > 0` by NAT-sub's strict positivity. Then `(a ⊖ w)_{d_b} = 0` since `d_b < dₐ` (Definition's `rᵢ = 0` for `i < k`), and at `i < d_b`, both results are zero. By T1 case (i), `a ⊖ w < b ⊖ w`.

In every case, `a ⊖ w ≤ b ⊖ w`. ∎

*Formal Contract:*
- *Preconditions:* a ∈ T, b ∈ T, w ∈ T, a < b, a ≥ w, b ≥ w
- *Depends:*
  - TA2 (WellDefinedSubtraction) — `a ⊖ w, b ⊖ w ∈ T`; result components in ℕ.
  - TumblerSub (TumblerSub) — component-wise subtraction definition: zero-padding, three-phase formula, length-pair dispatch naming `L_{x,w}`; exported postcondition that when `zpd(x, w)` is defined, `x̂_{zpd(x,w)} > ŵ_{zpd(x,w)}` holds on ZPD's padded projections — invoked in Sub-case A2 applied to `(a, w)` and `(b, w)` to supply `â_d > ŵ_d` and `b̂_d > ŵ_d` (well-typed regardless of whether `d` exceeds `#w` in the prefix-divergence sub-case) for NAT-sub's `≥ ŵ_d` precondition via NAT-order, in the preamble to Sub-cases B2–B4 to supply `â_{dₐ} > ŵ_{dₐ}`, in Sub-case B2 (the `j = d` branch) to discharge NAT-sub's `≥ ŵ_d` precondition for both operands via NAT-order, in Sub-case B3 to contradict `â_{dₐ} < ŵ_{dₐ}`, and in Sub-case B4 applied to `(b, w)` for the strict divergence-point inequality `b̂_{d_b} > ŵ_{d_b}`; conditional postcondition `Pos(x ⊖ w)` when `zpd(x, w)` is defined — used in Sub-cases A1, A3, and B1 to conclude `b ⊖ w` is positive from the existence of zero-padded divergence.
  - ZPD (ZeroPaddedDivergence) — existence biconditional, first-position characterisation, pre-zpd agreement; codomain `zpd(a, w) ∈ {1, ..., L}` and padding clause `âᵢ = 0` for `#a < i ≤ L` (with the symmetric `b̂` clause for the `(b, w)` case) used in Sub-case A2 and Case B's preamble to derive `dₐ ≤ #a` (resp. `d_b ≤ #b`) directly: the supposition `dₐ > #a` (resp. `d_b > #b`) with the codomain bound forces the padding-zone value `â_{dₐ} = 0` (resp. `b̂_{d_b} = 0`), substituting into TumblerSub's `â_{dₐ} > ŵ_{dₐ}` (resp. `b̂_{d_b} > ŵ_{d_b}`) yields `ŵ < 0`, contradicting NAT-zero's lower bound.
  - T1 (LexicographicOrder) — strict ordering `<` and derived `≤`; case (i) shared-position bound in conjunction form, supplying Case B's witness `j ≤ #a ∧ j ≤ #b ∧ aⱼ < bⱼ` and used in Case B's preamble sub-case (i) of the `(b, w)` not-zero-padded-equal proof to introduce `a < w` from witness `j` against `a ≥ w`; case (ii) prefix characterisation framing Case A and supplying the successor witness for the `a ⊖ w < b ⊖ w` length-comparisons in Sub-cases A1 and A3; trichotomy clause `¬(a < b ∧ b ≤ a)` discharges the `a < w ∧ a ≥ w` contradiction in Case B's preamble sub-case (i).
  - T3 (CanonicalRepresentation) — equality from component-wise agreement at equal length in Sub-case A2's `L_{a,w} = L_{b,w}` branch.
  - TA-Pos (PositiveTumbler) — `Pos(t)` and `Zero(t)` predicates for framing zero-tumbler and positive results of subtractions in Sub-cases A1, A3, B1.
  - TA-PosDom (PositiveDominatesZero) — a zero tumbler is strictly less than any positive tumbler; used in Sub-cases A1, A3, B1.
  - NAT-sub (NatPartialSubtraction) — conditional closure, strict monotonicity (B2's `j = d` branch), strict positivity (B4).
  - NAT-zero (NatZeroMinimum) — `0 ∈ ℕ` for padded components and literal-zero result components; lower bound at `(b ⊖ w)_p` in Sub-case A2's `≠ 0 ⟹ > 0` step; lower bound `0 ≤ aⱼ` in Case B's preamble sub-case (ii) to refute `aⱼ < 0`; lower bound `0 ≤ ŵ_{dₐ}` (resp. `0 ≤ ŵ_{d_b}`) in Sub-case A2 and Case B's preamble to refute `ŵ_{dₐ} < 0` (resp. `ŵ_{d_b} < 0`) obtained by substituting the padding-zone `â_{dₐ} = 0` (resp. `b̂_{d_b} = 0`) into TumblerSub's exported postcondition under the supposition `dₐ > #a` (resp. `d_b > #b`).
  - NAT-order (NatStrictTotalOrder) — trichotomy at `(#a, #w)`, `(#b, #w)`, `(L_{a,w}, L_{b,w})`, `(dₐ, d_b)`, `(j, #w)`, `(dₐ, #a)`, `(d_b, #b)` (the latter two close out the `dₐ ≤ #a` and `d_b ≤ #b` derivations in Sub-case A2 and Case B's preamble after `¬(dₐ > #a)` and `¬(d_b > #b)` are established); defining clause `m ≤ n ⟺ m < n ∨ m = n` for ≥/> conversions and the `≠ 0 ⟹ > 0` step; `>` definition `m > n ⟺ n < m` unfolding `0 > ŵ_{dₐ}` (resp. `0 > ŵ_{d_b}`) to `ŵ_{dₐ} < 0` (resp. `ŵ_{d_b} < 0`) in Sub-case A2 and Case B's preamble; disjointness-of-`<`-and-`=` at `(wⱼ, bⱼ)` and `(0, bⱼ)` in Sub-case B1; trichotomy disjointness composing the derived `ŵ < 0` against NAT-zero's `0 ≤ ŵ` to close out the `dₐ ≤ #a` and `d_b ≤ #b` arguments; transitivity composing length and divergence-position bounds.
  - NAT-discrete (NatDiscreteness) — forward direction `m < n ⟹ m + 1 ≤ n` supplying T1 case (ii)'s successor witness at `(#a, #b)` in A1 and A3, and at `(L_{a,w}, L_{b,w})` in A2.
  - NAT-closure (NatArithmeticClosureAndIdentity) — addition closure instantiated at `(n, 1)` with `1 ∈ ℕ` from the same axiom places `n + 1 ∈ ℕ` for the T1 case (ii) witnesses formed in A1, A2, A3.
- *Postconditions:* a ⊖ w ≤ b ⊖ w

**TA3-strict (OrderPreservationUnderSubtractionStrict).** `(A a, b, w : a < b ∧ a ≥ w ∧ b ≥ w ∧ #a = #b : a ⊖ w < b ⊖ w)`.

Subtracting a common lower bound from two equal-length tumblers preserves strict order.

*Proof.* Given `a, b, w ∈ T` with `a < b`, `a ≥ w`, `b ≥ w`, `#a = #b`, show `a ⊖ w < b ⊖ w`.

**The form of `a < b`.** Since `#a = #b`, T1 case (ii) (which requires `#a < #b`) is impossible. So `a < b` holds by case (i): there exists a least `j` with `1 ≤ j ≤ #a ∧ j ≤ #b` such that `aᵢ = bᵢ` for all `i < j` and `aⱼ < bⱼ`. Fix this `j`.

**Well-formedness and common length.** By TA2, `a ⊖ w, b ⊖ w ∈ T`. NAT-order's trichotomy on `(#a, #w)` selects one of (α) `#a = #w`, (β) `#a < #w`, (γ) `#w < #a`, naming `L_{a,w}`; with `#a = #b`, the trichotomy on `(#b, #w)` falls in the same sub-case, naming `L_{b,w} = L_{a,w}`. Write `L = L_{a,w} = L_{b,w}`; ZPD's padded projections `â`, `b̂`, `ŵ` are defined on `{1, ..., L}`. TumblerSub's length postcondition gives `#(a ⊖ w) = #(b ⊖ w) = L`. From the chosen sub-case, `#a ≤ L` and `#b ≤ L`, so the T1 witness satisfies `j ≤ L`.

Proceed by case analysis on the divergence structure of `(a, w)` and `(b, w)`.

**Case A: `a` is zero-padded-equal to `w`.** ZPD's no-divergence hypothesis gives `âᵢ = ŵᵢ` for all `1 ≤ i ≤ L`, and TumblerSub's no-divergence branch fixes `a ⊖ w = [0, …, 0]` of length `L`, so `(a ⊖ w)ᵢ = 0` for `1 ≤ i ≤ L`. We extract the divergence position of `(b, w)` from `j`, working entirely on padded projections so the argument is uniform across whether `j` lies in `w`'s native domain (zero-padded equality of `a` and `w` under `a ≥ w` permits `#a > #w`, e.g., `a = [3, 0]`, `w = [3]`, in which case `wᵢ` is undefined for `#w < i ≤ #a`). T1's pre-`j` agreement `aᵢ = bᵢ` for `i < j` (well-formed at `i < j ≤ #a = #b`) lifts via ZPD's padded-projection equalities (`âᵢ = aᵢ` from `i < j ≤ #a`, `b̂ᵢ = bᵢ` from `i < j ≤ #b`) to `âᵢ = b̂ᵢ` for `1 ≤ i < j`; chaining with the no-divergence hypothesis at `i < j ≤ L` (legal since `j ≤ L`) yields `b̂ᵢ = ŵᵢ` for `1 ≤ i < j`. At `i = j`: T1's witness `aⱼ < bⱼ` (well-formed at `j ≤ #a = #b`) lifts via padded-projection equalities (`âⱼ = aⱼ` from `j ≤ #a`, `b̂ⱼ = bⱼ` from `j ≤ #b`) to `âⱼ < b̂ⱼ`; the no-divergence hypothesis instantiated at `j ≤ L` gives `âⱼ = ŵⱼ`, hence `ŵⱼ < b̂ⱼ`, and NAT-order's disjointness-of-`<`-and-`=` at `(ŵⱼ, b̂ⱼ)` gives `b̂ⱼ ≠ ŵⱼ`. ZPD's minimality at `1 ≤ j ≤ L`, with `b̂ᵢ = ŵᵢ` for `i < j` and `b̂ⱼ ≠ ŵⱼ`, identifies `j = zpd(b, w)`. TumblerSub's exported postcondition under `b ≥ w` then gives `b̂ⱼ > ŵⱼ`. TumblerSub's Definition at `i = k = j` yields `(b ⊖ w)ⱼ = b̂ⱼ − ŵⱼ`, with NAT-sub's strict positivity at `b̂ⱼ > ŵⱼ` giving `b̂ⱼ − ŵⱼ ≥ 1`; the residual `≥ 1`-to-`> 0` step is closed by `0 < 1 ≤ b̂ⱼ − ŵⱼ ⟹ 0 < b̂ⱼ − ŵⱼ` — NAT-closure's Consequence supplies `0 < 1`, NAT-order's `≤`-definition unfolds `1 ≤ b̂ⱼ − ŵⱼ` to `1 < b̂ⱼ − ŵⱼ ∨ 1 = b̂ⱼ − ŵⱼ`, the `<` branch chains with `0 < 1` through NAT-order's `<`-transitivity at `(0, 1, b̂ⱼ − ŵⱼ)` and the `=` branch substitutes `1 = b̂ⱼ − ŵⱼ` into `0 < 1` via indiscernibility of `=`, both yielding `0 < b̂ⱼ − ŵⱼ`, equivalently `b̂ⱼ − ŵⱼ > 0` by NAT-order's `>` definition; for `i < j`, TumblerSub's pre-divergence rule gives `(b ⊖ w)ᵢ = 0`. Both results agree at `(a ⊖ w)ᵢ = 0 = (b ⊖ w)ᵢ` for `i < j`, and at `j ≤ L = #(a ⊖ w) = #(b ⊖ w)` we have `(a ⊖ w)ⱼ = 0 < b̂ⱼ − ŵⱼ = (b ⊖ w)ⱼ`. By T1 case (i), `a ⊖ w < b ⊖ w`.

**Setup for remaining cases.** Assume `a` is not zero-padded-equal to `w`. ZPD's existence biconditional makes `d_a = zpd(a, w)` well-defined with `1 ≤ d_a ≤ L`. TumblerSub's exported postcondition under `a ≥ w` gives `â_{d_a} > ŵ_{d_a}` on the padded projections — well-typed regardless of whether `d_a` exceeds `#w`. We bound `d_a ≤ #a`: suppose for contradiction `d_a > #a`; then `#a < d_a ≤ L`, and ZPD's padding clause `âᵢ = 0` for `#a < i ≤ L` instantiated at `i := d_a` gives `â_{d_a} = 0`. Substituting into `â_{d_a} > ŵ_{d_a}` yields `0 > ŵ_{d_a}`, i.e., `ŵ_{d_a} < 0` (NAT-order's `>` definition `m > n ⟺ n < m`), contradicting NAT-zero's lower bound `0 ≤ ŵ_{d_a}` via NAT-order's trichotomy. Hence `¬(d_a > #a)`; NAT-order's trichotomy at `(d_a, #a)` together with the defining clause `≤ ⟺ < ∨ =` yields `d_a ≤ #a`. With `#a = #b`, also `d_a ≤ #b`. ZPD's padded-projection equality therefore identifies padded with native at `d_a` and earlier: `â_{d_a} = a_{d_a}`, `b̂_{d_a} = b_{d_a}`, and `âᵢ = aᵢ`, `b̂ᵢ = bᵢ` for `1 ≤ i ≤ d_a`.

If `b` were zero-padded-equal to `w`, then `b̂ᵢ = ŵᵢ` for all `1 ≤ i ≤ L`. Instantiating at `i := d_a` (legal since `d_a ≤ L`) gives `b̂_{d_a} = ŵ_{d_a}`. ZPD's pre-divergence agreement for `(a, w)` gives `âᵢ = ŵᵢ` for `1 ≤ i < d_a`; chaining with `b̂ᵢ = ŵᵢ` yields `âᵢ = b̂ᵢ` for `1 ≤ i < d_a`. Lifting via padded-projection equality (legal since `i < d_a ≤ #a = #b`): `aᵢ = bᵢ` for `1 ≤ i < d_a`. At `d_a`: TumblerSub's `â_{d_a} > ŵ_{d_a} = b̂_{d_a}` lifts via padded-native equality to `a_{d_a} > b_{d_a}`. So the pair `(b, a)` satisfies T1 case (i) at witness `j' = d_a`, yielding `b < a`; this contradicts `a < b` via T1's trichotomy disjointness clause `¬(a < b ∧ b < a)`. Hence `b` is not zero-padded-equal to `w`, so `d_b = zpd(b, w)` is well-defined with `1 ≤ d_b ≤ L`, and TumblerSub's exported postcondition under `b ≥ w` gives `b̂_{d_b} > ŵ_{d_b}`. The same padding-zone contradiction (now substituting `b̂_{d_b} = 0` from the supposition `d_b > #b` into `b̂_{d_b} > ŵ_{d_b}` to clash with NAT-zero's lower bound) yields `d_b ≤ #b`, hence `d_b ≤ #a`.

By NAT-order trichotomy on `(d_a, d_b) ∈ ℕ × ℕ`, exactly one of `d_a = d_b`, `d_a < d_b`, `d_a > d_b` holds.

**Case 1: `d_a = d_b = d`.** Both `d ≤ #a` and `d ≤ #b`, so padded projections coincide with native at `d` and earlier (`â_d = a_d`, `b̂_d = b_d`, and `âᵢ = aᵢ`, `b̂ᵢ = bᵢ` for `1 ≤ i ≤ d`). TumblerSub's Definition gives `(a ⊖ w)ᵢ = (b ⊖ w)ᵢ = 0` for `i < d`. ZPD's pre-divergence agreements for `(a, w)` and `(b, w)` give `âᵢ = ŵᵢ` and `b̂ᵢ = ŵᵢ` for `i < d`; chaining and lifting yields `aᵢ = bᵢ` for `i < d`. T1's witness `aⱼ < bⱼ` together with `aᵢ = bᵢ` for `i < d` forces `j ≥ d`: had `j < d`, the just-established agreement instantiated at `i := j` would give `aⱼ = bⱼ`, conflicting with NAT-order's disjointness-of-`<`-and-`=` at `(aⱼ, bⱼ)` which converts `aⱼ < bⱼ` into `aⱼ ≠ bⱼ`.

*Subcase `j = d`:* TumblerSub's Definition at `i = k = d` gives `(a ⊖ w)_d = â_d − ŵ_d` and `(b ⊖ w)_d = b̂_d − ŵ_d`. TumblerSub's exported postconditions for `(a, w)` and `(b, w)` deliver `â_d > ŵ_d` and `b̂_d > ŵ_d`, hence `â_d ≥ ŵ_d` and `b̂_d ≥ ŵ_d` via NAT-order's defining clause `≤ ⟺ < ∨ =`; both differences therefore lie in ℕ by NAT-sub's conditional closure. From `a_d < b_d` (T1's witness at `j = d`) and padded-native equality `â_d = a_d`, `b̂_d = b_d`, we obtain `â_d < b̂_d`; NAT-sub's strict monotonicity at `(â_d, b̂_d, ŵ_d)` (with both operands `≥ ŵ_d`) yields `â_d − ŵ_d < b̂_d − ŵ_d`, i.e., `(a ⊖ w)_d < (b ⊖ w)_d`. The results agree at `(a ⊖ w)ᵢ = 0 = (b ⊖ w)ᵢ` for `i < d` and first disagree at `d ≤ L = #(a ⊖ w) = #(b ⊖ w)`. By T1 case (i), `a ⊖ w < b ⊖ w`.

*Subcase `j > d`:* T1's pre-`j` agreement instantiated at `i := d` (legal since `d < j`) gives `a_d = b_d`; with padded-native equality, `â_d = b̂_d`, so the divergence-point components `â_d − ŵ_d` and `b̂_d − ŵ_d` coincide and `(a ⊖ w)_d = (b ⊖ w)_d`. For `d < i < j`: TumblerSub's tail-copy gives `(a ⊖ w)ᵢ = âᵢ` and `(b ⊖ w)ᵢ = b̂ᵢ`; padded-native equality at `i < j ≤ #a = #b` gives `âᵢ = aᵢ` and `b̂ᵢ = bᵢ`, and T1's pre-`j` agreement gives `aᵢ = bᵢ`, so `(a ⊖ w)ᵢ = (b ⊖ w)ᵢ`. At `j`: tail-copy gives `(a ⊖ w)ⱼ = âⱼ = aⱼ` and `(b ⊖ w)ⱼ = b̂ⱼ = bⱼ` (legal at `j ≤ #a = #b`); T1's witness `aⱼ < bⱼ` yields `(a ⊖ w)ⱼ < (b ⊖ w)ⱼ`. Results agree before `j`, first disagree at `j ≤ L`. By T1 case (i), `a ⊖ w < b ⊖ w`.

**Case 2: `d_a < d_b`.** ZPD's first-disagreement clause for `(a, w)` gives `â_{d_a} ≠ ŵ_{d_a}`; ZPD's pre-divergence agreement for `(b, w)` (legal at `d_a < d_b`) gives `b̂_{d_a} = ŵ_{d_a}`. Chaining: `â_{d_a} ≠ b̂_{d_a}`. Padded-native equality at `d_a ≤ #a = #b` lifts to `a_{d_a} ≠ b_{d_a}`. ZPD's pre-divergence agreements for both pairs give `âᵢ = ŵᵢ = b̂ᵢ` for `i < d_a`; lifting via padded-native equality gives `aᵢ = bᵢ` for `i < d_a`. T1's first-disagreement witness `j` therefore satisfies `j = d_a` (it is the least position where `a` and `b` differ), and T1 case (i) yields `a_{d_a} < b_{d_a}`. Combined with `b_{d_a} = b̂_{d_a} = ŵ_{d_a}`: `a_{d_a} < ŵ_{d_a}`. Padded-native equality lifts to `â_{d_a} < ŵ_{d_a}`. But TumblerSub's exported postcondition gave `â_{d_a} > ŵ_{d_a}`, equivalent to `ŵ_{d_a} < â_{d_a}` (NAT-order's `>` definition); NAT-order's exactly-one-trichotomy clause `¬(x < y ∧ y < x)` at `(â_{d_a}, ŵ_{d_a})` rules out the conjunction. Impossible.

**Case 3: `d_a > d_b`.** ZPD's pre-divergence agreement for `(a, w)` (legal at `d_b < d_a`) gives `â_{d_b} = ŵ_{d_b}`; ZPD's first-disagreement clause for `(b, w)` gives `b̂_{d_b} ≠ ŵ_{d_b}`. Chaining: `â_{d_b} ≠ b̂_{d_b}`. Padded-native equality at `d_b ≤ #b = #a` lifts to `a_{d_b} ≠ b_{d_b}`. ZPD's pre-divergence agreements for both pairs give `âᵢ = ŵᵢ = b̂ᵢ` for `i < d_b`; lifting gives `aᵢ = bᵢ` for `i < d_b`. T1's first-disagreement witness `j` therefore satisfies `j = d_b`, with T1 case (i) yielding `a_{d_b} < b_{d_b}`.

For `a ⊖ w`: TumblerSub's Definition at `i = d_b < d_a` (the pre-divergence zero phase of `(a, w)`) gives `(a ⊖ w)_{d_b} = 0`. For `b ⊖ w`: TumblerSub's Definition at `i = k = d_b` gives `(b ⊖ w)_{d_b} = b̂_{d_b} − ŵ_{d_b}`, with NAT-sub's strict positivity at `b̂_{d_b} > ŵ_{d_b}` (TumblerSub's exported postcondition) yielding `b̂_{d_b} − ŵ_{d_b} ≥ 1`; the same `≥ 1`-to-`> 0` bridge `0 < 1 ≤ b̂_{d_b} − ŵ_{d_b} ⟹ 0 < b̂_{d_b} − ŵ_{d_b}` via NAT-closure's Consequence `0 < 1`, NAT-order's `≤`-definition splitting `1 ≤ b̂_{d_b} − ŵ_{d_b}` into `1 < b̂_{d_b} − ŵ_{d_b} ∨ 1 = b̂_{d_b} − ŵ_{d_b}`, NAT-order's `<`-transitivity at `(0, 1, b̂_{d_b} − ŵ_{d_b})` for the `<` branch, and indiscernibility of `=` substituting `1 = b̂_{d_b} − ŵ_{d_b}` into `0 < 1` for the `=` branch (as in Case A) lifts this to `b̂_{d_b} − ŵ_{d_b} > 0` (by NAT-order's `>` definition). For `i < d_b`: `(a ⊖ w)ᵢ = 0` (TumblerSub's pre-divergence zero phase, since `i < d_b < d_a`) and `(b ⊖ w)ᵢ = 0` (similarly, since `i < d_b`). First disagreement at `d_b ≤ L = #(a ⊖ w) = #(b ⊖ w)` with `0 < b̂_{d_b} − ŵ_{d_b}`. By T1 case (i), `a ⊖ w < b ⊖ w`.

In every case, `a ⊖ w < b ⊖ w`. ∎

*Formal Contract:*
- *Preconditions:* a ∈ T, b ∈ T, w ∈ T, a < b, a ≥ w, b ≥ w, #a = #b
- *Depends:*
  - T0 (CarrierSetDefinition) — carrier-set membership `a, b, w ∈ T`; length operator `#·`; native-domain component projection `·ᵢ ∈ ℕ` on `{1, ..., #·}`.
  - T1 (LexicographicOrder) — definition of `<`; ruling out case (ii) under `#a = #b`; first-divergence witness `j` with prefix agreement `aᵢ = bᵢ` for `i < j` and strict component inequality `aⱼ < bⱼ`; trichotomy disjointness clause `¬(a < b ∧ b < a)` discharging the contradiction in Setup that rules out `b` zero-padded-equal to `w`; case (i) producing `a ⊖ w < b ⊖ w` from each branch's first-disagreement witness.
  - TumblerSub (TumblerSub) — Definition of `x ⊖ w` on ZPD's padded projections (zero-padding, divergence discovery, three-region rule `r_i = 0` for `i < k`, `r_k = x̂_k − ŵ_k`, `r_i = x̂_i` for `i > k`); length postcondition `#(x ⊖ w) = L_{x,w}`; exported divergence-point inequality `x̂_{zpd(x,w)} > ŵ_{zpd(x,w)}` under `x ≥ w` — invoked in Case A applied to `(b, w)` after `j = zpd(b, w)` is identified, in Setup applied to `(a, w)` and `(b, w)` to supply `â_{d_a} > ŵ_{d_a}` and `b̂_{d_b} > ŵ_{d_b}` (well-typed regardless of whether the zpd index lies in either operand's native domain), in Case 1 Subcase `j = d` to discharge NAT-sub's `≥ ŵ_d` precondition for both operands via NAT-order, in Case 2 to contradict the lifted `â_{d_a} < ŵ_{d_a}`, and in Case 3 to supply NAT-sub's strict-positivity input `b̂_{d_b} > ŵ_{d_b}`.
  - ZPD (ZeroPaddedDivergence) — existence biconditional (`zpd(x, w)` defined iff `x` is not zero-padded-equal to `w`), establishing `d_a` and `d_b` defined; codomain `1 ≤ zpd ≤ L`; padded-projection equalities `âᵢ = aᵢ` for `1 ≤ i ≤ #a` and `b̂ᵢ = bᵢ` for `1 ≤ i ≤ #b` (symmetric clause `ŵᵢ = wᵢ` for `1 ≤ i ≤ #w`) lifting padded statements to native at indices in the native domain; padding clause `âᵢ = 0` for `#a < i ≤ L` (symmetric `b̂ᵢ = 0` clause) used in Setup to derive `d_a ≤ #a` and `d_b ≤ #b` directly: the supposition `d_a > #a` (resp. `d_b > #b`) with the codomain bound forces the padding-zone value `â_{d_a} = 0` (resp. `b̂_{d_b} = 0`), substituting into TumblerSub's `â_{d_a} > ŵ_{d_a}` (resp. `b̂_{d_b} > ŵ_{d_b}`) yields `ŵ < 0`, contradicting NAT-zero's lower bound; first-disagreement clause `âₖ ≠ ŵₖ` at `k = zpd(a, w)` (symmetric for `(b, w)`) supplying the divergence position's disagreement in Cases 2 and 3; pre-divergence agreement `âᵢ = ŵᵢ` for `1 ≤ i < zpd(a, w)` (symmetric for `(b, w)`) chained through `ŵ` to derive `aᵢ = bᵢ` on the pre-divergence range; minimality used in Case A to identify `j = zpd(b, w)` from the established `b̂ᵢ = ŵᵢ` for `i < j` and `b̂ⱼ ≠ ŵⱼ`.
  - TA2 (WellDefinedSubtraction) — `a ⊖ w, b ⊖ w ∈ T`.
  - NAT-sub (NatPartialSubtraction) — conditional closure of `â_d − ŵ_d`, `b̂_d − ŵ_d` in ℕ under `â_d, b̂_d ≥ ŵ_d` (Case 1 subcase `j = d`); strict monotonicity at `(â_d, b̂_d, ŵ_d)` deriving `â_d − ŵ_d < b̂_d − ŵ_d` from `â_d < b̂_d` with both `≥ ŵ_d` (Case 1 subcase `j = d`); strict positivity yielding `b̂_j − ŵ_j ≥ 1` from `b̂_j > ŵ_j` (Case A) and `b̂_{d_b} − ŵ_{d_b} ≥ 1` from `b̂_{d_b} > ŵ_{d_b}` (Case 3) — the residual `≥ 1`-to-`> 0` step is closed downstream by NAT-closure's Consequence `0 < 1` together with NAT-order's `≤`-definition and `<`-transitivity, not by NAT-sub itself. All NAT-sub invocations are stated on ZPD's padded projections so the operands lie in ℕ even when the divergence index exceeds either native domain.
  - NAT-zero (NatZeroMinimum) — `0 ∈ ℕ` for literal-zero result components and the zero-tumbler branch (Case A); padded operand values `âᵢ = 0` and `b̂ᵢ = 0` in the padding-zone derivations of Setup; lower bound `0 ≤ ŵ_{d_a}` (resp. `0 ≤ ŵ_{d_b}`) refuting `ŵ_{d_a} < 0` (resp. `ŵ_{d_b} < 0`) obtained by substituting the padding-zone `â_{d_a} = 0` (resp. `b̂_{d_b} = 0`) into TumblerSub's exported postcondition under the supposition `d_a > #a` (resp. `d_b > #b`).
  - NAT-order (NatStrictTotalOrder) — trichotomy at length pairs `(#a, #w)` and `(#b, #w)` selecting the same sub-case under `#a = #b`, hence naming `L = L_{a,w} = L_{b,w}`; trichotomy at index pair `(d_a, d_b)` for the three-way case split; trichotomy at `(d_a, #a)` and `(d_b, #b)` together with the defining clause `m ≤ n ⟺ m < n ∨ m = n` closing the `d_a ≤ #a` and `d_b ≤ #b` arguments after their `>` branches are refuted; trichotomy at `(#a, #a + 1)` together with the `≤`-defining clause refuting `#a + 1 ≤ #a` in *The form of `a < b`* — both branches `#a + 1 < #a` and `#a + 1 = #a` are excluded by trichotomy given NAT-addcompat's `#a < #a + 1`; `>` definition `m > n ⟺ n < m` unfolding `0 > ŵ_{d_a}` (resp. `0 > ŵ_{d_b}`) to `ŵ_{d_a} < 0` (resp. `ŵ_{d_b} < 0`) in Setup, unfolding TumblerSub's `â_{d_a} > ŵ_{d_a}` to `ŵ_{d_a} < â_{d_a}` in Case 2, and folding `0 < b̂_j − ŵ_j` to `b̂_j − ŵ_j > 0` (resp. `0 < b̂_{d_b} − ŵ_{d_b}` to `b̂_{d_b} − ŵ_{d_b} > 0`) at the conclusion of the `≥ 1`-to-`> 0` bridges in Cases A and 3; defining clause `≤ ⟺ < ∨ =` converting TumblerSub's strict `>` to NAT-sub's `≥` precondition (Case 1 subcase `j = d`), and splitting NAT-sub's strict-positivity output `1 ≤ b̂_j − ŵ_j` (Case A) and `1 ≤ b̂_{d_b} − ŵ_{d_b}` (Case 3) into a `<` branch and an `=` branch for the bridge to `> 0`; `<`-transitivity at `(0, 1, b̂_j − ŵ_j)` (Case A) and `(0, 1, b̂_{d_b} − ŵ_{d_b})` (Case 3) chaining NAT-closure's `0 < 1` with the `<` branch of the split to deliver `0 < b̂_j − ŵ_j` (resp. `0 < b̂_{d_b} − ŵ_{d_b}`); disjointness-of-`<`-and-`=` at `(ŵⱼ, b̂ⱼ)` (Case A, converting `ŵⱼ < b̂ⱼ` to `b̂ⱼ ≠ ŵⱼ` on ZPD's padded projections) and at `(aⱼ, bⱼ)` (Case 1, converting `aⱼ < bⱼ` to `aⱼ ≠ bⱼ` to refute `j < d`); exactly-one-trichotomy clause `¬(x < y ∧ y < x)` at `(â_{d_a}, ŵ_{d_a})` (Case 2) ruling out the conjunction of `â_{d_a} < ŵ_{d_a}` and `ŵ_{d_a} < â_{d_a}`.
  - NAT-closure (NatArithmeticClosureAndIdentity) — supplies the Consequence `0 < 1`, used in Cases A and 3 to bridge from NAT-sub's strict-positivity output `b̂_j − ŵ_j ≥ 1` (resp. `b̂_{d_b} − ŵ_{d_b} ≥ 1`) to the strict-positive form `b̂_j − ŵ_j > 0` (resp. `b̂_{d_b} − ŵ_{d_b} > 0`) required to apply T1 case (i): the bridge `0 < 1 ≤ b̂_j − ŵ_j ⟹ 0 < b̂_j − ŵ_j` combines NAT-closure's `0 < 1` with NAT-order's mixed `< ≤` transitivity (the `≤`-definition splits `1 ≤ b̂_j − ŵ_j` into `1 < b̂_j − ŵ_j ∨ 1 = b̂_j − ŵ_j`, the `<` branch closes by NAT-order's `<`-transitivity chained with `0 < 1`, the `=` branch closes by indiscernibility of `=` substituting into `0 < 1`), and analogously for `(0, 1, b̂_{d_b} − ŵ_{d_b})`.
  - NAT-addcompat (NatAdditionOrderAndSuccessor) — strict successor inequality `n < n + 1` at `n := #a`, used in *The form of `a < b`* to rule out T1 case (ii) under `#a = #b`: T1(ii)'s clause `k = #a + 1 ≤ #b` substitutes via `#a = #b` to `#a + 1 ≤ #a`, whose `≤`-expansion `#a + 1 < #a ∨ #a + 1 = #a` is excluded in both branches by NAT-order's trichotomy at `(#a, #a + 1)` given NAT-addcompat's `#a < #a + 1`, so case (ii) is impossible.
- *Postconditions:* a ⊖ w < b ⊖ w

Tumbler addition is not, in general, invertible by `⊖`. TumblerAdd builds `a ⊕ w` in three regions keyed on the action point `k` of `w`: positions `i < k` retain `aᵢ`, position `k` accumulates `aₖ + wₖ`, and positions `i > k` are supplied by `w`. Whatever content `a` carries past position `k` is overwritten by `w`'s tail and cannot be recovered. Even with `#a = k` ruling out that loss, the recovery `(a ⊕ w) ⊖ w = a` further requires that `a`'s prefix vanish (`aᵢ = 0` for `1 ≤ i < k`), so that the first divergence between `a ⊕ w` and `w` falls at position `k` rather than at some earlier nonzero entry of `a` that would mislead TumblerSub's divergence-keyed dispatch. Together with `Pos(w)` (so the action point exists, by TA-Pos) and `#w = k`, these are the structural conditions under which we can establish a partial inverse.

**TA4 (PartialInverse).** `(A a, w ∈ T : Pos(w) ∧ k = #a ∧ #w = k ∧ (A i : 1 ≤ i < k : aᵢ = 0) : (a ⊕ w) ⊖ w = a)`, where `k` is the action point of `w`.

*Proof.* Let `k` denote the action point of `w` (ActionPoint): the least position `i` with `wᵢ > 0`, so `wᵢ = 0` for `i < k` and `wₖ > 0`. `Pos(w)` guarantees `k` exists (TA-Pos).

**Step 1: structure of `r = a ⊕ w`.** By TumblerAdd (`k = #a` discharges TA0's precondition `k ≤ #a`), `r` is built in three regions: `rᵢ = aᵢ` for `i < k`; `rₖ = aₖ + wₖ`; `rᵢ = wᵢ` for `i > k`. The precondition `(A i : 1 ≤ i < k : aᵢ = 0)` gives `rᵢ = 0` for `i < k`. By TA0's result-length identity `#r = #w` and the precondition `#w = k`, `#r = k`, so positions `i > k` are empty. Hence `r = [0, ..., 0, aₖ + wₖ]` of length `k`.

**Step 2: computing `s = r ⊖ w`.** TumblerSub requires `r ≥ w` (T1); TumblerAdd's dominance postcondition discharges this. TumblerSub is keyed on `zpd(r, w)` (ZPD): the three-region rule (`sᵢ = 0` for `i < k`, `sₖ = rₖ − wₖ`, `sᵢ = rᵢ` for `i > k`) when `zpd` is defined, and the zero tumbler of length `L` when `zpd` is undefined. NAT-order's trichotomy on `(#r, #w)` names `L = max(#r, #w)`; with `#r = #w = k`, `L = k`. At every position `i < k`, `rᵢ = 0` and `wᵢ = 0`, so padded projections agree before position `k`.

Since `aₖ ∈ ℕ` (T0 component typing at `k = #a`), NAT-zero supplies `0 ≤ aₖ`, which NAT-order's defining clause `m ≤ n ⟺ m < n ∨ m = n` at `m = 0, n = aₖ` unfolds to `aₖ > 0 ∨ aₖ = 0`.

*Case 1: `aₖ > 0`.* NAT-addcompat's right order-compatibility (`p ≤ n ⟹ p + m ≤ n + m`, at `p = 0, n = aₖ, m = wₖ`) lifts `0 ≤ aₖ` to `0 + wₖ ≤ aₖ + wₖ`; NAT-closure's additive identity rewrites `0 + wₖ = wₖ`, giving `wₖ ≤ aₖ + wₖ`. NAT-cancel's symmetric summand absorption `n + m = m ⟹ n = 0` rules out the equality disjunct, which would force `aₖ = 0` and contradict `aₖ > 0` by NAT-order's irreflexivity. NAT-order's defining clause at `m = wₖ, n = aₖ + wₖ` then yields `aₖ + wₖ > wₖ`, i.e., `rₖ > wₖ`. Combined with pre-divergence agreement at `i < k`, ZPD's minimality identifies `k = zpd(r, w)`. TumblerSub produces `sᵢ = 0` for `i < k`, `sₖ = (aₖ + wₖ) − wₖ = aₖ` (NAT-sub right-telescoping), and nothing beyond (since `#r = k`). Hence `s = [0, ..., 0, aₖ]` of length `k`, which by T3 and the precondition `aᵢ = 0` for `i < k` equals `a`.

*Case 2: `aₖ = 0`.* Then `rₖ = aₖ + wₖ = 0 + wₖ = wₖ` (NAT-closure). Combined with `rᵢ = 0 = wᵢ` for `i < k` and `#r = k = #w`, T3 gives `r = w`. The padded projections agree throughout `{1, ..., k}`, so `zpd(r, w)` is undefined (ZPD case-split) and TumblerSub's no-divergence branch yields the zero tumbler of length `k`. By the precondition, this is `a`.

In both cases, `(a ⊕ w) ⊖ w = a`. ∎

*Formal Contract:*
- *Preconditions:* `a ∈ T`, `w ∈ T`, `Pos(w)`, `k = #a`, `#w = k`, `(A i : 1 ≤ i < k : aᵢ = 0)`, where `k` is the action point of `w`
- *Depends:*
  - TA-Pos (PositiveTumbler) — guarantees action point exists from `Pos(w)`
  - ActionPoint (ActionPoint) — defines `k` as least position with `wᵢ > 0`; `wᵢ = 0` for `i < k`
  - TumblerAdd (TumblerAdd) — three-region construction of `a ⊕ w`; dominance postcondition `r ≥ w`
  - TA0 (WellDefinedAddition) — applicability precondition `k ≤ #a`; result-length identity `#r = #w`
  - TumblerSub (TumblerSub) — three-region construction of `r ⊖ w`; no-divergence zero-tumbler branch
  - T0 (CarrierSetDefinition) — carrier `T`, length `#`, component typing `aᵢ ∈ ℕ`
  - T1 (LexicographicOrder) — `≥` comparison for TumblerSub's precondition
  - T3 (CanonicalRepresentation) — componentwise and length equality imply tumbler equality
  - ZPD (ZPD) — case-split (undefined when padded projections agree); minimality at first disagreement
  - NAT-closure (NatArithmeticClosureAndIdentity) — additive identity `0 + n = n`
  - NAT-addcompat (NatAdditionOrderAndSuccessor) — right order-compatibility `p ≤ n ⟹ p + m ≤ n + m`
  - NAT-cancel (NatAdditionCancellation) — symmetric summand absorption `n + m = m ⟹ n = 0`
  - NAT-zero (NatZeroMinimum) — lower bound `0 ≤ n` for `n ∈ ℕ`
  - NAT-order (NatStrictTotalOrder) — trichotomy on length pair; defining clause `≤ ⟺ < ∨ =`; irreflexivity
  - NAT-sub (NatPartialSubtraction) — right-telescoping `(m + n) − n = m`
- *Postconditions:* `(a ⊕ w) ⊖ w = a`

### What tumbler arithmetic is NOT

**The algebra is not a group.** No additive identity — the zero tumbler is a sentinel. No additive inverse — subtraction is defined only when `a ≥ w`. Not closed under subtraction.

**TA-assoc (AdditionAssociative).** Addition is associative where both compositions are defined: `(a ⊕ b) ⊕ c = a ⊕ (b ⊕ c)` whenever both sides are well-defined.

*Proof.* Write `k_b = actionPoint(b)`, `k_c = actionPoint(c)`. Recall TumblerAdd: for `x ⊕ w` with action point `k`, `(x ⊕ w)ᵢ = xᵢ` for `i < k`, `(x ⊕ w)_k = x_k + w_k`, `(x ⊕ w)ᵢ = wᵢ` for `i > k`, with `#(x ⊕ w) = #w`.

*Lengths.* By TA0: `#(a ⊕ b) = #b`, hence `#((a ⊕ b) ⊕ c) = #c`; and `#(b ⊕ c) = #c`. The outer right-side length `#(a ⊕ (b ⊕ c))` is deferred until `Pos(b ⊕ c)` and `actionPoint(b ⊕ c) ≤ #a` are established.

*Action point of `s = b ⊕ c`.* By TumblerAdd: `sᵢ = bᵢ` for `i < k_c`, `s_{k_c} = b_{k_c} + c_{k_c}`, `sᵢ = cᵢ` for `i > k_c`. NAT-order trichotomy at `k_b, k_c` gives three exhaustive sub-cases; in each we exhibit the least index at which `s` is nonzero and read `actionPoint(s)` off ActionPoint's least-witness clauses.

- `k_b < k_c`: prefix-copy gives `s_{k_b} = b_{k_b}` (since `k_b < k_c`). ActionPoint minimum-nonzero at `b` gives `b_{k_b} ≥ 1`; NAT-zero plus NAT-order's `m ≤ n ⟺ m < n ∨ m = n` lift this to `b_{k_b} > 0`. For `i` with `1 ≤ i < k_b`, `bᵢ = 0` (ActionPoint zeros-below at `b`); since `i < k_b < k_c`, prefix-copy gives `sᵢ = bᵢ = 0`. ActionPoint applied to `s` therefore yields `actionPoint(s) = k_b`.
- `k_b = k_c = k`: `s_k = b_k + c_k`. From `b_k ≥ 1`, `c_k ≥ 1` (ActionPoint minimum-nonzero at `b` and `c`), NAT-addcompat's left order-compatibility gives `b_k + c_k ≥ b_k + 1`; NAT-addcompat's strict successor gives `b_k + 1 > b_k`; NAT-order composes to `b_k + c_k > b_k > 0`. For `i` with `1 ≤ i < k`, `bᵢ = 0` (zeros-below at `b`), and prefix-copy (since `i < k = k_c`) gives `sᵢ = bᵢ = 0`. ActionPoint applied to `s` therefore yields `actionPoint(s) = k`.
- `k_b > k_c`: `b_{k_c} = 0` (ActionPoint zeros-below at `b`, since `k_c < k_b`), so `s_{k_c} = 0 + c_{k_c} = c_{k_c}` by NAT-closure's additive identity; `c_{k_c} ≥ 1` lifts to `c_{k_c} > 0` as above. For `i` with `1 ≤ i < k_c`, `cᵢ = 0` (zeros-below at `c`); since `i < k_c < k_b`, `bᵢ = 0` (zeros-below at `b`), and prefix-copy gives `sᵢ = bᵢ = 0`. ActionPoint applied to `s` therefore yields `actionPoint(s) = k_c`.

In each sub-case the witness index lies in `{1, …, #s}`: `1 ≤ k_b` and `1 ≤ k_c` from ActionPoint's first postcondition at `b` and `c`, and `k_c ≤ #c = #s`, with NAT-order transitivity covering sub-case 1 (where `k_b < k_c ≤ #s`), supplies the upper bound. This witnesses TA-Pos for `s`, so `Pos(s)`. The case-split also yields the unified description: `k_b ≤ k_c ⟹ actionPoint(s) = k_b` (sub-cases 1 and 2) and `k_c ≤ k_b ⟹ actionPoint(s) = k_c` (sub-cases 2 and 3).

*Domain conditions.* Left side requires `Pos(b)`, `k_b ≤ #a`, `Pos(c)`, `k_c ≤ #b` (TA0 on `a ⊕ b` and on `(a ⊕ b) ⊕ c`). Right side requires `Pos(c)`, `k_c ≤ #b`, `Pos(s)`, `actionPoint(s) ≤ #a` (TA0 on `b ⊕ c` and on `a ⊕ s`). The subsumption `k_b ≤ #a ⟹ actionPoint(s) ≤ #a` follows from the case-split: when `k_b ≤ k_c`, `actionPoint(s) = k_b ≤ #a`; when `k_c < k_b`, `actionPoint(s) = k_c < k_b ≤ #a` via NAT-order. The intersection of domains is the formal-contract preconditions.

*Right-side length.* With `Pos(s)` and `actionPoint(s) ≤ #a`, TA0 gives `#(a ⊕ s) = #s = #c`. Both sides have length `#c`.

*Case 1: `k_b < k_c`.* `actionPoint(s) = k_b`, `s_{k_b} = b_{k_b}`. Let `r = a ⊕ b`.

Left `(r ⊕ c)` has action point `k_c`: `aᵢ` for `i < k_b`; `r_{k_b} = a_{k_b} + b_{k_b}` at `k_b`; `rᵢ = bᵢ` for `k_b < i < k_c`; `r_{k_c} + c_{k_c} = b_{k_c} + c_{k_c}` at `k_c`; `cᵢ` for `i > k_c`.

Right `(a ⊕ s)` has action point `k_b`: `aᵢ` for `i < k_b`; `a_{k_b} + s_{k_b} = a_{k_b} + b_{k_b}` at `k_b`; `sᵢ = bᵢ` for `k_b < i < k_c`; `s_{k_c} = b_{k_c} + c_{k_c}` at `k_c`; `cᵢ` for `i > k_c`.

Every component agrees.

*Case 2: `k_b = k_c = k`.* `actionPoint(s) = k`, `s_k = b_k + c_k`. Let `r = a ⊕ b`.

Left `(r ⊕ c)_k = r_k + c_k = (a_k + b_k) + c_k`. Right `(a ⊕ s)_k = a_k + s_k = a_k + (b_k + c_k)`. Equal by NAT-addassoc. All other positions match directly.

*Case 3: `k_b > k_c`.* `actionPoint(s) = k_c`, `s_{k_c} = 0 + c_{k_c} = c_{k_c}`. Let `r = a ⊕ b`.

Left `(r ⊕ c)` has action point `k_c`: for `i < k_c < k_b`, `rᵢ = aᵢ`; at `k_c`, `r_{k_c} + c_{k_c} = a_{k_c} + c_{k_c}`; for `i > k_c`, `cᵢ`.

Right `(a ⊕ s)` has action point `k_c`: `aᵢ` for `i < k_c`; `a_{k_c} + s_{k_c} = a_{k_c} + c_{k_c}` at `k_c`; `sᵢ = cᵢ` for `i > k_c`.

Every component agrees. The shallower displacement `c` discards everything below its action point on both sides, so `b`'s contribution at and beyond `k_b` is invisible.

In all three cases both sides produce the same sequence of length `#c`, so `(a ⊕ b) ⊕ c = a ⊕ (b ⊕ c)` by T3. ∎

*Formal Contract:*
- *Preconditions:* `a, b, c ∈ T`, `Pos(b)`, `Pos(c)`, `k_b ≤ #a`, `k_c ≤ #b` (where `k_b = actionPoint(b)`, `k_c = actionPoint(c)`).
- *Depends:*
  - T0 (CarrierSetDefinition) — carrier `T` and length `#·` on finite ℕ-sequences.
  - TumblerAdd (TumblerAdd) — piecewise prefix-copy / advance / tail-copy definition of `⊕`.
  - TA0 (WellDefinedAddition) — preconditions `Pos(w)`, `actionPoint(w) ≤ #x`; result-length `#(x ⊕ w) = #w`.
  - TA-Pos (PositiveTumbler) — existential definition of `Pos(·)`; consumed to establish `Pos(b ⊕ c)`.
  - ActionPoint (ActionPoint) — definition `actionPoint(w) = min{i : wᵢ ≠ 0}`; bounds `1 ≤ actionPoint(w) ≤ #w`; zeros-below; minimum-nonzero `w_{actionPoint(w)} ≥ 1`.
  - T1 (LexicographicOrder) — supplies the `<` and `≥` on tumblers under which TumblerAdd's strict-advancement and dominance postconditions (`a ⊕ w > a`, `a ⊕ w ≥ w`) are stated; TumblerAdd's contract, consumed by this proof, is interpretable only with T1 in scope.
  - T3 (CanonicalRepresentation) — component-wise equality plus equal length implies tumbler equality.
  - NAT-addassoc (NatAdditionAssociative) — `(m + n) + p = m + (n + p)` on ℕ; used in Case 2.
  - NAT-addcompat (NatAdditionOrderAndSuccessor) — left order-compatibility and strict successor `n < n + 1`; used in sub-case `k_b = k_c`.
  - NAT-cancel (NatAdditionCancellation) — symmetric summand absorption `n + m = m ⟹ n = 0`, on which TumblerAdd's dominance sub-case `aₖ > 0` rests; required in scope for the consumed TumblerAdd contract.
  - NAT-closure (NatArithmeticClosureAndIdentity) — additive identity `0 + n = n` and closure under `+`.
  - NAT-discrete (NatDiscreteness) — forward direction `m < n ⟹ m + 1 ≤ n`, on which ActionPoint's minimum-nonzero clause `1 ≤ w_{actionPoint(w)}` rests; this proof invokes that clause directly when lifting `b_{k_b} ≥ 1` and `c_{k_c} ≥ 1`.
  - NAT-order (NatStrictTotalOrder) — trichotomy, transitivity, `m ≤ n ⟺ m < n ∨ m = n`.
  - NAT-sub (NatPartialSubtraction) — conditional closure of `k − 1` and `n − k` and the inverse collapses on which TumblerAdd's result-length identity `#(a ⊕ w) = #w` rests; that identity, exported through TA0, supplies the right-side length `#(a ⊕ s) = #c` here.
  - NAT-wellorder (NatWellOrdering) — least-element principle on which ActionPoint's existence-and-uniqueness construction of `actionPoint(w)` rests; this proof invokes ActionPoint's definition and bounds directly when computing `actionPoint(s)` for `s = b ⊕ c` per sub-case of NAT-order trichotomy on `(k_b, k_c)`.
  - NAT-zero (NatZeroMinimum) — lower bound `0 ≤ n`; used in `≥ 1 → > 0` lifts.
- *Postconditions:* `(a ⊕ b) ⊕ c = a ⊕ (b ⊕ c)`; `#((a ⊕ b) ⊕ c) = #(a ⊕ (b ⊕ c)) = #c`; `Pos(b ⊕ c)`; `k_b ≤ k_c ⟹ actionPoint(b ⊕ c) = k_b`; `k_c ≤ k_b ⟹ actionPoint(b ⊕ c) = k_c` (jointly characterizing `actionPoint(b ⊕ c)` by NAT-order trichotomy on `(k_b, k_c)`).

**Addition is not commutative.** The operands play asymmetric roles: the first is a *position*, the second a *displacement*. Gregory's `absadd` takes the prefix from the first argument and the suffix from the second.

**There is no multiplication or division.** Gregory's codebase analysis confirms: no `tumblermult`, no `tumblerdiv`. The arithmetic repertoire is add, subtract, increment, compare. Tumblers are addresses, not quantities.

**Tumbler differences are not counts.** Nelson: "A tumbler-span is not a conventional number, and it does not designate the number of bytes contained." The difference between two addresses specifies boundaries, not cardinality. Between sibling addresses 3 and 7, document 5 may have arbitrarily many descendants; their count is unknowable from the addresses alone.

### Cancellation properties of ⊕

TumblerAdd's constructive definition determines each component of the result from exactly one input. This makes the operation left-cancellative.

**TA-LC (LeftCancellation).** If a ⊕ x = a ⊕ y with both sides well-defined (TA0 satisfied for both), then x = y.

*Proof.* Let `k₁` be the action point of `x` and `k₂` the action point of `y`. Both exist because TA0 requires `Pos(x)` and `Pos(y)`, so each has at least one nonzero component. We eliminate both strict orderings.

**Case k₁ < k₂.** Every component of `y` before position `k₂` is zero, so `y_{k₁} = 0`. Position `k₁` falls in the prefix-copy region of `a ⊕ y`: `(a ⊕ y)_{k₁} = a_{k₁}`. In `a ⊕ x`, position `k₁` is the action point: `(a ⊕ x)_{k₁} = a_{k₁} + x_{k₁}`. From `a ⊕ x = a ⊕ y`, `a_{k₁} + x_{k₁} = a_{k₁}`, so by NAT-cancel (summand absorption, `m + n = m ⟹ n = 0`) with `m = a_{k₁}`, `n = x_{k₁}`, we get `x_{k₁} = 0`. But `k₁` is the action point of `x`, so `x_{k₁} > 0` — contradiction.

**Case k₂ < k₁.** Symmetric: `x_{k₂} = 0`, so `(a ⊕ x)_{k₂} = a_{k₂}` while `(a ⊕ y)_{k₂} = a_{k₂} + y_{k₂}`. By NAT-cancel, `y_{k₂} = 0`, contradicting `y_{k₂} > 0`.

By NAT-order's trichotomy, `k₁ = k₂`. Write `k` for this common action point.

**Positions i < k.** `xᵢ = 0 = yᵢ` by definition of action point.

**Position i = k.** `(a ⊕ x)_k = a_k + x_k` and `(a ⊕ y)_k = a_k + y_k`. From `a ⊕ x = a ⊕ y`, `a_k + x_k = a_k + y_k`, so `x_k = y_k` by NAT-cancel (left cancellation, `m + n = m + p ⟹ n = p`).

**Positions i > k.** Tail-copy region: `(a ⊕ x)_i = x_i` and `(a ⊕ y)_i = y_i`. From `a ⊕ x = a ⊕ y`, `x_i = y_i`.

**Length.** By T3, `#(a ⊕ x) = #(a ⊕ y)`. The result-length identity gives `#(a ⊕ w) = #w`, so `#x = #y`.

All components agree and `#x = #y`, so `x = y` by T3.  ∎

*Worked example.* Let a = [2, 5] and suppose a ⊕ x = a ⊕ y = [2, 8]. Suppose k_x = 1: then 2 + x₁ = 2 gives x₁ = 0, contradicting k_x = 1. So k_x = 2, and similarly k_y = 2. At position 2: 5 + x₂ = 8 gives x₂ = 3, and 5 + y₂ = 8 gives y₂ = 3. For i < k: x₁ = 0 = y₁. From `#(a ⊕ x) = #x`, #x = 2 = #y. By T3, x = y = [0, 3].

*Formal Contract:*
- *Preconditions:* a, x, y ∈ T; Pos(x); Pos(y); actionPoint(x) ≤ #a; actionPoint(y) ≤ #a; a ⊕ x = a ⊕ y
- *Depends:*
  - TumblerAdd (TumblerAdd) — prefix-copy, advance, tail-copy rules and result-length identity.
  - TA0 (WellDefinedAddition) — well-definedness of `a ⊕ x` and `a ⊕ y`.
  - TA-Pos (PositiveTumbler) — supplies `Pos(x)` and `Pos(y)` for action-point existence.
  - ActionPoint (ActionPoint) — action point as first nonzero component.
  - NAT-cancel (NatAdditionCancellation) — summand absorption and left cancellation on ℕ.
  - NAT-order (NatStrictTotalOrder) — trichotomy collapsing ruled-out orderings to equality.
  - T3 (CanonicalRepresentation) — component-wise and length agreement imply tumbler equality.
- *Postconditions:* x = y

**TA-MTO (ManyToOne).** For any displacement w with action point k and any tumblers a, b with #a ≥ k and #b ≥ k: a ⊕ w = b ⊕ w if and only if a_i = b_i for all 1 ≤ i ≤ k.

*Proof.* Let `w` be a displacement with action point `k`, and let `a, b ∈ T` with `#a ≥ k` and `#b ≥ k`. Both additions `a ⊕ w` and `b ⊕ w` are well-defined by TA0. TumblerAdd builds each result in three regions relative to `k`:

```
  (a ⊕ w)ᵢ = aᵢ         for 1 ≤ i < k     (prefix copy)
  (a ⊕ w)ₖ = aₖ + wₖ                       (advance)
  (a ⊕ w)ᵢ = wᵢ         for k < i ≤ #w     (tail copy)
```

and identically for `b ⊕ w`. TumblerAdd gives `#(a ⊕ w) = #w = #(b ⊕ w)`.

*(Forward.)* Assume `aᵢ = bᵢ` for all `1 ≤ i ≤ k`.

*Position i < k:* `(a ⊕ w)ᵢ = aᵢ = bᵢ = (b ⊕ w)ᵢ` by prefix-copy and the hypothesis.

*Position i = k:* `(a ⊕ w)ₖ = aₖ + wₖ = bₖ + wₖ = (b ⊕ w)ₖ` by advance and the hypothesis.

*Position i > k:* `(a ⊕ w)ᵢ = wᵢ = (b ⊕ w)ᵢ` by tail-copy.

All components agree and lengths are equal, so `a ⊕ w = b ⊕ w` by T3.

*(Converse.)* Assume `a ⊕ w = b ⊕ w`. By T3, `(a ⊕ w)ᵢ = (b ⊕ w)ᵢ` at every position.

*Position i < k:* prefix-copy gives `(a ⊕ w)ᵢ = aᵢ` and `(b ⊕ w)ᵢ = bᵢ`, so `aᵢ = bᵢ`.

*Position i = k:* advance gives `aₖ + wₖ = bₖ + wₖ`, hence `aₖ = bₖ` by NAT-cancel with `m = wₖ`. ∎

*Formal Contract:*
- *Preconditions:* w ∈ T, Pos(w), a ∈ T, b ∈ T, #a ≥ actionPoint(w), #b ≥ actionPoint(w)
- *Depends:*
  - TumblerAdd (TumblerAdd) — three-region constructive definition and result-length identity.
  - TA0 (WellDefinedAddition) — well-definedness of `a ⊕ w` and `b ⊕ w`.
  - TA-Pos (PositiveTumbler) — discharges `Pos(w)` for TA0 and ActionPoint.
  - ActionPoint (ActionPoint) — names `k` and licenses the three-region split.
  - T3 (CanonicalRepresentation) — position-wise-and-length characterisation of tumbler equality.
  - NAT-cancel (NatAdditionCancellation) — right cancellation on ℕ at position `k`.
- *Postconditions:* a ⊕ w = b ⊕ w ⟺ (A i : 1 ≤ i ≤ actionPoint(w) : aᵢ = bᵢ)

### Right cancellation and the many-to-one property

The converse — right cancellation — does not hold.

**TA-RC (RightCancellationFailure).** There exist tumblers a, b, w with a ≠ b and a ⊕ w = b ⊕ w (both sides well-defined).

*Proof.* We exhibit three specific tumblers and verify the claim by direct computation.

Let `a = [1, 3, 5]`, `b = [1, 3, 7]`, and `w = [0, 2, 4]`. Each is a length-3 nonempty finite sequence over ℕ; T0's comprehension clause, instantiated at `p = 3` and the component maps `r_a(1)=1, r_a(2)=3, r_a(3)=5`, `r_b(1)=1, r_b(2)=3, r_b(3)=7`, and `r_w(1)=0, r_w(2)=2, r_w(3)=4`, supplies witness tumblers in `T` with these lengths and components, establishing `a, b, w ∈ T`. The third components differ (`5 ≠ 7`), so `a ≠ b` by T3.

The displacement `w` has action point `k = 2`, since `w₁ = 0` and `w₂ = 2 > 0`. TA0 requires `actionPoint(w) ≤ #a` and `actionPoint(w) ≤ #b`; both reduce to `2 ≤ 3`, which holds.

We compute `a ⊕ w` by TumblerAdd with action point `k = 2`:

- Position `i = 1` (`i < k`): prefix copy gives `(a ⊕ w)₁ = a₁ = 1`.
- Position `i = 2` (`i = k`): advance gives `(a ⊕ w)₂ = a₂ + w₂ = 3 + 2 = 5`.
- Position `i = 3` (`i > k`): tail copy gives `(a ⊕ w)₃ = w₃ = 4`.

So `a ⊕ w = [1, 5, 4]`.

We compute `b ⊕ w` by the same three rules:

- Position `i = 1` (`i < k`): prefix copy gives `(b ⊕ w)₁ = b₁ = 1`.
- Position `i = 2` (`i = k`): advance gives `(b ⊕ w)₂ = b₂ + w₂ = 3 + 2 = 5`.
- Position `i = 3` (`i > k`): tail copy gives `(b ⊕ w)₃ = w₃ = 4`.

So `b ⊕ w = [1, 5, 4]`.

Both results are `[1, 5, 4]`, hence `a ⊕ w = b ⊕ w`. The tail-copy rule discards components of the start after position `k`, so the difference between `a₃ = 5` and `b₃ = 7` is erased.

We have exhibited `a ≠ b` with `a ⊕ w = b ⊕ w`, both sides well-defined: right cancellation fails.  ∎

*Formal Contract:*
- *Depends:*
  - T0 (CarrierSetDefinition) — comprehension clause, instantiated at length `p = 3` with the component maps for `a = [1,3,5]`, `b = [1,3,7]`, and `w = [0,2,4]` respectively, establishes `a, b, w ∈ T` — the carrier-set membership presupposed by every condition cited below.
  - T3 (CanonicalRepresentation) — inequality from a single component disagreement.
  - TA0 (WellDefinedAddition) — action-point bound for well-definedness.
  - TA-Pos (PositiveTumbler) — positivity of `w` licensing the action point.
  - ActionPoint (ActionPoint) — minimum-position formula fixing `k = 2`.
  - TumblerAdd (TumblerAdd) — three-region rule computing each side.
- *Postconditions:* ∃ a, b, w ∈ T : Pos(w) ∧ actionPoint(w) ≤ #a ∧ actionPoint(w) ≤ #b ∧ a ≠ b ∧ a ⊕ w = b ⊕ w

**TA-strict (StrictIncrease).** `(A a, w ∈ T : Pos(w) ∧ actionPoint(w) ≤ #a : a ⊕ w > a)`.

TA-strict exports TumblerAdd's ordering postcondition as a single labelled fact so downstream users (chiefly T12 span well-definedness) can cite one corollary rather than TumblerAdd's full postcondition list.

*Proof.* Immediate from TumblerAdd's ordering-guarantee postcondition `a ⊕ w > a (T1)` under the preconditions `a, w ∈ T`, `Pos(w)`, `actionPoint(w) ≤ #a`, which are exactly TA-strict's hypotheses. ∎

*Formal Contract:*
- *Preconditions:* `a ∈ T`, `w ∈ T`, `Pos(w)`, `actionPoint(w) ≤ #a`
- *Depends:*
  - TumblerAdd (TumblerAdd) — ordering-guarantee postcondition `a ⊕ w > a (T1)` re-exported unchanged.
  - T0 (CarrierSetDefinition) — carrier `T` and length operator `#` in the quantifier range and precondition.
  - TA-Pos (PositiveTumbler) — precondition `Pos(w)`.
  - ActionPoint (ActionPoint) — precondition `actionPoint(w) ≤ #a`.
  - TA0 (WellDefinedAddition) — membership `a ⊕ w ∈ T` so T1's ordering applies to the left-hand side.
  - T1 (LexicographicOrder) — meaning of the strict ordering `>`.
- *Forward References:*
  - T12 (SpanWellDefinedness) — downstream user of this corollary; cites TA-strict for span well-definedness rather than TumblerAdd's full postcondition list.
- *Postconditions:* `a ⊕ w > a`

**ZPD (ZeroPaddedDivergence).** For tumblers `a, w ∈ T`, the *zero-padded divergence* `zpd(a, w)` is defined on the zero-padded extensions of both operands to a common length `L`, selected by NAT-order's trichotomy on `(#a, #w)`: (α) `#a = #w`, `L = #a`; (β) `#a < #w`, `L = #w`; (γ) `#w < #a`, `L = #a`. The *padded projections* `â`, `ŵ` on `{1, ..., L}` are given by `âᵢ = aᵢ` for `1 ≤ i ≤ #a` and `âᵢ = 0` for `#a < i ≤ L`, and symmetrically `ŵᵢ = wᵢ` for `1 ≤ i ≤ #w` and `ŵᵢ = 0` for `#w < i ≤ L`. If `(A i : 1 ≤ i ≤ L : âᵢ = ŵᵢ)`, then `zpd(a, w)` is *undefined* and we say `a` and `w` are *zero-padded-equal*. Otherwise, `zpd(a, w)` is the least `k` with `1 ≤ k ≤ L` such that `âₖ ≠ ŵₖ`.

The function is partial: undefined precisely when `â` and `ŵ` agree everywhere on `{1, ..., L}`, as when one operand is a proper prefix of the other with all trailing components zero (e.g., `a = [3, 0]`, `w = [3]` give `â = ŵ = [3, 0]`). Equal tumblers are trivially zero-padded-equal.

**Relationship to Divergence.** When `a ≠ w`, formal Divergence and `zpd` may disagree. In Divergence case (i) — component divergence at shared position `k` with `k ≤ #a ∧ k ≤ #w` — the padded projections coincide with the native projections through `1, ..., k`, so `zpd(a, w) = divergence(a, w) = k`. In Divergence case (ii) — proper prefix, falling in sub-case (β) or (γ) — Divergence reports `#a + 1` (β) or `#w + 1` (γ), while `zpd` scans the padded components of the shorter operand (all zero) against the longer operand's native components: if the longer operand has a nonzero component past the shorter's last position, `zpd(a, w)` is the least index `k` satisfying `#a < k ≤ #w ∧ ŵₖ ≠ âₖ` in sub-case (β) (and symmetrically `#w < k ≤ #a ∧ âₖ ≠ ŵₖ` in sub-case (γ)). The construction yields only the strict bound `#a < k` (resp. `#w < k`), one position weaker than the postcondition's required `#a + 1 ≤ k` (resp. `#w + 1 ≤ k`); NAT-discrete's forward direction `m < n ⟹ m + 1 ≤ n`, instantiated at `(#a, k)` (resp. `(#w, k)`), bridges that gap, yielding `zpd(a, w) ≥ divergence(a, w)`. If all such trailing components are zero, `zpd(a, w)` is undefined.

*Formal Contract:*
- *Domain:* a ∈ T, w ∈ T
- *Definition:* NAT-order trichotomy on `(#a, #w)` selects (α) `#a = #w`, `L = #a`; (β) `#a < #w`, `L = #w`; (γ) `#w < #a`, `L = #a`. Padded projections `â`, `ŵ` on `{1, ..., L}`: `âᵢ = aᵢ` for `1 ≤ i ≤ #a`, `âᵢ = 0` for `#a < i ≤ L`; `ŵᵢ = wᵢ` for `1 ≤ i ≤ #w`, `ŵᵢ = 0` for `#w < i ≤ L`. If `(A i : 1 ≤ i ≤ L : âᵢ = ŵᵢ)`, `zpd(a, w)` is undefined. Otherwise, `zpd(a, w) = min {k : 1 ≤ k ≤ L ∧ âₖ ≠ ŵₖ}`.
- *Depends:*
  - T0 (CarrierSetDefinition) — `a, w ∈ T`, lengths `#a`, `#w`, native-domain component projections `aᵢ`, `wᵢ`, ℕ-valuation of native components.
  - NAT-zero (NatZeroMinimum) — supplies `0 ∈ ℕ` for the padding clauses `âᵢ = 0`, `ŵᵢ = 0`.
  - NAT-order (NatStrictTotalOrder) — trichotomy on `(#a, #w)` selects `L` and dispatches the shared-position bound `k ≤ #a ∧ k ≤ #w` and sub-case boundaries `#a + 1`, `#w + 1`.
  - NAT-wellorder (NatWellOrdering) — least-element principle for `min {k : 1 ≤ k ≤ L ∧ âₖ ≠ ŵₖ}`.
  - NAT-closure (NatArithmeticClosureAndIdentity) — addition closure instantiated at `(#a, 1)` and `(#w, 1)`, with `1 ∈ ℕ` from the same axiom, places `#a + 1` and `#w + 1` in ℕ in the postcondition.
  - NAT-discrete (NatDiscreteness) — forward direction `m < n ⟹ m + 1 ≤ n`, instantiated at `(#a, k)` in sub-case (β) and at `(#w, k)` in sub-case (γ), bridges the construction's strict bound `#a < k` (resp. `#w < k`) on the least disagreement position to the postcondition's `#a + 1 ≤ k` (resp. `#w + 1 ≤ k`), grounding `zpd(a, w) ≥ divergence(a, w)` against the NAT-* axioms.
  - Divergence (Divergence) — two-case structure (component divergence; prefix divergence) and domain restriction `a ≠ b` consumed by the Relationship-to-Divergence postcondition.
- *Codomain:* When defined, `zpd(a, w) ∈ {1, ..., L}`, with `L = #a` in sub-cases (α), (γ) and `L = #w` in sub-case (β).
- *Partiality:* `zpd(a, w)` is undefined iff `a` and `w` are zero-padded-equal.
- *Postconditions (Symmetry):* `zpd(a, w)` is defined iff `zpd(w, a)` is defined, and when defined, `zpd(a, w) = zpd(w, a)`. Sub-case (α) is self-symmetric; sub-cases (β) and (γ) swap under exchange, yielding the same `L`; the disagreement predicate is symmetric.
- *Postconditions (Relationship to Divergence):* For `a ≠ w`: in Divergence case (i) with divergence at `k` satisfying `k ≤ #a ∧ k ≤ #w`, `zpd(a, w) = divergence(a, w)`. In Divergence case (ii), under sub-case (β) or (γ): if the longer operand has a nonzero component beyond the shorter's last position, `zpd(a, w)` is defined and `zpd(a, w) ≥ divergence(a, w)`; if all such components are zero, `zpd(a, w)` is undefined.


---

## 8. Increment and positivity

The increment operation TA5 advances a tumbler by a single allocator step. Positivity (TA-Pos) characterizes tumblers eligible for allocation; TA-PosDom and TA-dom track the domains over which arithmetic and increment are defined. TA5a, TA5-SIG, and TA5-SigValid record the signature checks and well-formedness invariants the increment relies on. TA6 establishes the zero-tumbler boundary.

### Increment for allocation

A separate operation, distinct from the shifting arithmetic, handles address allocation. When the system allocates a new address, it takes the highest existing address in a partition and produces the next one.

The *last significant position* `sig(t)` of a tumbler — defined in TA5-SIG — identifies the rightmost nonzero component, or `#t` when all components are zero. For valid addresses, `sig(t) = #t` (TA5-SigValid), so `inc(t, 0)` on a valid address increments the last component of the last field.

**TA5 (HierarchicalIncrement).** For tumbler `t ∈ T` and level `k ≥ 0`, there exists an operation `inc(t, k)` producing tumbler `t'` such that:

  (a) `t' > t` (strictly greater under T1),

  (b) when `k = 0`: `t'` agrees with `t` at every position other than `sig(t)`; when `k > 0`: `t'` agrees with `t` on all original positions,

  (c) when `k = 0` (*sibling*): `#t' = #t` and `t'_{sig(t)} = t_{sig(t)} + 1`,

  (d) when `k > 0` (*child*): `#t' = #t + k`, the `k - 1` intermediate positions `#t + 1, ..., #t + k - 1` are set to `0` (field separators), and the final position `#t + k` is set to `1` (the first child).

*Proof.* Let `t = t₁. ... .tₘ` where `m = #t`, and let `k ≥ 0`.

**Construction.** When `k = 0` (*sibling increment*): set `t'ᵢ = tᵢ` for all `i ≠ sig(t)`, and `t'_{sig(t)} = t_{sig(t)} + 1`. Then `#t' = m`.

When `k > 0` (*child creation*): set `t'ᵢ = tᵢ` for `1 ≤ i ≤ m`, set `t'ᵢ = 0` for `m + 1 ≤ i ≤ m + k - 1`, and set `t'_{m+k} = 1`. Then `#t' = m + k`.

In both cases `t'` is a finite sequence of natural numbers with length ≥ 1, so `t' ∈ T` by T0.

**Verification of (b).** For `k = 0`: by construction `t'ᵢ = tᵢ` for all `i ≠ sig(t)`. For `k > 0`: by construction `t'ᵢ = tᵢ` for all `1 ≤ i ≤ m`.

**Verification of (c).** When `k = 0`: `#t' = m = #t`, and `t'_{sig(t)} = t_{sig(t)} + 1` by construction.

**Verification of (d).** When `k > 0`: `#t' = m + k = #t + k`. Positions `m + 1` through `m + k - 1` are `0` (empty range when `k = 1`). Position `m + k` is `1`.

**Verification of (a).**

*Case `k = 0`.* Let `j = sig(t)`. By (b), `t'ᵢ = tᵢ` for all `i ≠ j`, so the tumblers agree on positions `1 ≤ i < j`. At position `j`, `t'_j = t_j + 1 > t_j` by NAT-addcompat's strict successor inequality. Since `j = sig(t) ≤ m = #t = #t'`, both tumblers have a component at `j`. T1 case (i) yields `t < t'`.

*Case `k > 0`.* By (b), the tumblers agree on positions `1 ≤ i ≤ m`. T1 case (ii) requires `#t + 1 ≤ #t'`. NAT-discrete (instantiated at `m = 0`, `n = k`) discharges its strict antecedent against the case hypothesis `0 < k` and yields `0 + 1 ≤ k`; NAT-closure's left-identity clause `0 + n = n` (instantiated at `n = 1`) rewrites `0 + 1` to `1`, so `1 ≤ k`. NAT-addcompat's order-compatibility of addition (instantiated at `m = #t`, `p = 1`, `n = k`) lifts `1 ≤ k` to `#t + 1 ≤ #t + k = #t'`. T1 case (ii) yields `t < t'`. ∎

*Formal Contract:*
- *Preconditions:* `t ∈ T`, `k ≥ 0`.
- *Definition:* `inc(t, k)`: when `k = 0`, modify position `sig(t)` (TA5-SIG) to `t_{sig(t)} + 1`; when `k > 0`, extend by `k` positions with `k - 1` zeros and final `1`.
- *Depends:*
  - T0 (CarrierSetDefinition) — characterisation of `T` as finite ℕ-sequences of length ≥ 1; discharges `t' ∈ T`.
  - NAT-closure (NatArithmeticClosureAndIdentity) — addition closure instantiated at `(t_{sig(t)}, 1)` gives `t_{sig(t)} + 1 ∈ ℕ`, and at `(0, 1)` gives `0 + 1 ∈ ℕ`, with `1 ∈ ℕ` from the same axiom; the left-identity clause `0 + n = n` instantiated at `n = 1` rewrites NAT-discrete's consequent `0 + 1 ≤ k` to `1 ≤ k` in Case `k > 0`.
  - NAT-addcompat (NatAdditionOrderAndSuccessor) — strict successor inequality `n < n + 1` for Case `k = 0`; left order-compatibility `1 ≤ k ⟹ #t + 1 ≤ #t + k` for Case `k > 0`.
  - NAT-zero (NatZeroMinimum) — `0 ∈ ℕ` supplies both the literal value of the `k − 1` field separators and the legal `m`-value for instantiating NAT-discrete at `m = 0`.
  - NAT-discrete (NatDiscreteness) — instantiated at `m = 0`, `n = k`; the strict antecedent `0 < k` is the case hypothesis itself, so the axiom yields `0 + 1 ≤ k`, which NAT-closure's left identity rewrites to `1 ≤ k`.
  - T1 (LexicographicOrder) — case (i) at divergence position `sig(t)` for `k = 0`; case (ii) with proper-prefix `#t + 1 ≤ #t'` for `k > 0`.
  - TA5-SIG (LastSignificantPosition) — resolves `sig(t)` in the definition and postconditions (b), (c).
- *Forward References:*
  - TA5-SigValid (SigOnValidAddresses) — refines TA5 to T4-valid inputs, establishing `sig(t) = #t`; TA5 names it to explain the valid-address consequence of `inc(t, 0)`.
  - TA5a (IncrementPreservesT4) — elaborates TA5 by establishing the precise T4-preservation conditions for `inc(t, k)`; TA5 names it as the downstream analysis site.
  - T4 (HierarchicalParsing) — named in the prose as the validity predicate that TA5-SigValid requires and TA5a analyzes; TA5's own proof does not invoke T4.
- *Postconditions:* `t' ∈ T`. (a) `t' > t` under T1. (b) When `k = 0`: `(A i : 1 ≤ i ≤ #t ∧ i ≠ sig(t) : t'ᵢ = tᵢ)`. When `k > 0`: `(A i : 1 ≤ i ≤ #t : t'ᵢ = tᵢ)`. (c) When `k = 0`: `#t' = #t`, `t'_{sig(t)} = t_{sig(t)} + 1`. (d) When `k > 0`: `#t' = #t + k`, positions `#t + 1 ... #t + k - 1` are `0`, position `#t + k` is `1`.

`inc(t, 0)` does not produce the immediate successor of `t` in the total order. It produces the smallest same-length tumbler that agrees with `t` on positions `1, ..., sig(t) − 1` and has a strictly larger component at position `sig(t)`. When `sig(t) = #t` (which holds for valid addresses by TA5-SigValid), this is the next peer at the same hierarchical depth. When `sig(t) < #t`, same-length tumblers lie between `t` and `inc(t, 0)` — for example, `(2, 0, 1)` lies between `(2, 0, 0)` and `inc((2, 0, 0), 0) = (3, 0, 0)`. The gap between `t` and `inc(t, 0)` contains the entire subtree of `t`: all tumblers `t.x₁. ... .xₘ`. The true immediate successor in the total order is `t.0` by T1 case (ii).

For `k > 0`, `inc(t, k)` likewise does not produce the immediate successor: for `k = 1` the result is `t.1`; for `k = 2` the result is `t.0.1`. In both cases `t.0` lies strictly between `t` and the result. For address allocation this is harmless: allocation advances the counter past all existing addresses.

The conditions under which `inc` preserves T4 are established in TA5a: `inc(t, k)` preserves T4 iff `k ∈ {0, 1}`, or `k = 2` with `zeros(t) ≤ 2`; for `k ≥ 3`, `inc(t, k)` violates T4 by introducing adjacent zero separators.

| Label | Statement | Status |
|-------|-----------|--------|
| TA5 | `inc(t, k)` produces `t' > t` with same-length structure for `k = 0` (sibling) and extended structure for `k > 0` (child) | proved (this property) |
| TA5-SIG | `sig(t)` is the rightmost nonzero component position of `t`, or `#t` when all components are zero | definition (separate property) |
| TA5-SigValid | For every valid address satisfying T4, `sig(t) = #t` | proved (separate property) |
| TA5a | `inc(t, k)` preserves T4 iff `k ∈ {0, 1}`, or `k = 2 ∧ zeros(t) ≤ 2`; violated for `k ≥ 3` | proved (separate property) |

**TA5a (IncrementPreservesT4).** The operation `inc(t, k)` on a T4-valid address `t` preserves T4 iff `k ∈ {0, 1}`, or `k = 2` with `zeros(t) ≤ 2`. For `k ≥ 3`, T4 is violated.

*Proof.* Let `t` satisfy T4, `t' = inc(t, k)`. T4 requires: (i) `zeros(t) ≤ 3`, (ii) no two zeros adjacent, (iii) `t₁ ≠ 0`, (iv) `t_{#t} ≠ 0`.

*Case `k = 0`.* By TA5(c), `#t' = #t` and `t'_{sig(t)} = t_{sig(t)} + 1`; by TA5(b), `t'` agrees with `t` at every position `≠ sig(t)`. By TA5-SigValid, `sig(t) = #t`. By NAT-closure, `t_{sig(t)} + 1 ∈ ℕ`; by NAT-zero, NAT-addcompat, and NAT-order, `t_{sig(t)} + 1 > t_{sig(t)} ≥ 0`, so `t_{sig(t)} + 1 ≠ 0` — NAT-addcompat's strict successor inequality `t_{sig(t)} + 1 > t_{sig(t)}` chains via NAT-order's transitivity with NAT-zero's lower bound `t_{sig(t)} ≥ 0` to give `t_{sig(t)} + 1 > 0`, and NAT-order's irreflexivity (equivalently, the exactly-one trichotomy clause `¬(m < n ∧ m = n)` derived from it) lifts `> 0` to `≠ 0`. The zero-index set of `t'` is `{i : 1 ≤ i ≤ #t' ∧ t'ᵢ = 0} = {i : 1 ≤ i ≤ #t ∧ t'ᵢ = 0}` (using `#t' = #t`); at every `i ≠ sig(t)`, `t'ᵢ = tᵢ` by TA5(b), and at `i = sig(t)`, T4(iv)'s `t_{#t} ≠ 0` together with TA5-SigValid's `sig(t) = #t` gives `t_{sig(t)} ≠ 0`, excluding position `sig(t)` from the original zero-index set, while TA5(c)'s `t'_{sig(t)} = t_{sig(t)} + 1` combined with the just-derived `t_{sig(t)} + 1 ≠ 0` gives `t'_{sig(t)} ≠ 0`, excluding it from the primed; position `sig(t)` lies outside both the original and the primed zero-index subsets. The two subsets coincide as sets: `{i : 1 ≤ i ≤ #t ∧ t'ᵢ = 0} = {i : 1 ≤ i ≤ #t ∧ tᵢ = 0}`. Both subsets lie inside `{1, …, #t}`; by NAT-card's well-definedness of `|·|` as a total function on subsets of that initial segment, equal subsets carry equal cardinalities, so `zeros(t') = zeros(t)`. For T4(i) on `t'`, the established `zeros(t') = zeros(t)` together with T4(i) on `t` (`zeros(t) ≤ 3`) gives `zeros(t') ≤ 3`. For T4(ii), we split each `i` with `1 ≤ i < #t'` (equivalently `1 ≤ i < #t` by TA5(c)'s `#t' = #t`) on whether `sig(t) ∈ {i, i + 1}`. TA5-SigValid's `sig(t) = #t` combined with the index bound `i < #t` rules out the sub-case `i = sig(t)` (which would force `i = #t`, contradicting `i < #t`), leaving two non-vacuous sub-cases on T4-valid `t`. When `sig(t) ∉ {i, i + 1}`, TA5(b)'s agreement at positions `≠ sig(t)` instantiated at `i` and `i + 1` gives `t'ᵢ = tᵢ` and `t'ᵢ₊₁ = tᵢ₊₁`, and T4(ii) on `t` at index `i` (legal since `1 ≤ i < #t`) gives `¬(tᵢ = 0 ∧ tᵢ₊₁ = 0)`, hence `¬(t'ᵢ = 0 ∧ t'ᵢ₊₁ = 0)`. When `i + 1 = sig(t) = #t` (forcing `i = #t − 1`, hence `#t ≥ 2`), the NAT-closure/NAT-zero/NAT-addcompat/NAT-order chain above at position `sig(t) = i + 1` gives `t'ᵢ₊₁ = t'_{sig(t)} = t_{sig(t)} + 1 ≠ 0`, falsifying the conjunct `t'ᵢ₊₁ = 0` and hence the conjunction. For T4(iv), TA5(c)'s `#t' = #t` and TA5-SigValid's `sig(t) = #t` identify `t'_{#t'} = t'_{#t} = t'_{sig(t)}`; combining TA5(c)'s `t'_{sig(t)} = t_{sig(t)} + 1` with the already-established `t_{sig(t)} + 1 ≠ 0` (from the NAT-closure/NAT-zero/NAT-addcompat/NAT-order chain above) gives `t'_{#t'} ≠ 0`. For T4(iii), we split on `sig(t)`: when `sig(t) = 1`, position `1 = sig(t)` places `t'₁ = t'_{sig(t)} = t_{sig(t)} + 1` at the site of the NAT-closure/NAT-zero/NAT-addcompat/NAT-order chain above, so reusing that chain at position `1` gives `t'₁ ≠ 0`; when `sig(t) ≠ 1`, TA5(b)'s agreement at every position `≠ sig(t)` instantiated at position `1` gives `t'₁ = t₁`, and T4(iii) on `t` gives `t₁ ≠ 0`, hence `t'₁ ≠ 0`. T4 preserved unconditionally.

*Case `k = 1`.* By TA5(d), `#t' = #t + 1` and `t'_{#t+1} = 1`; by TA5(b), `t'` agrees with `t` on original positions. The zero-index set of `t'` is `{i : 1 ≤ i ≤ #t + 1 ∧ t'ᵢ = 0}`; for `1 ≤ i ≤ #t` we have `t'ᵢ = tᵢ` by TA5(b), and at the new boundary `t'_{#t+1} = 1 ≠ 0` excludes index `#t + 1`, so the set equals `{i : 1 ≤ i ≤ #t ∧ tᵢ = 0}`. Both subsets lie inside `{1, …, #t + 1}`; by NAT-card's well-definedness on subsets of that initial segment, equal subsets carry equal cardinalities, so `zeros(t') = zeros(t)`. For T4(i) on `t'`, the established `zeros(t') = zeros(t)` together with T4(i) on `t` (`zeros(t) ≤ 3`) gives `zeros(t') ≤ 3`. For T4(ii) on `t'`, the index range `1 ≤ i < #t' = #t + 1`, equivalently `1 ≤ i ≤ #t`, splits into the interior `1 ≤ i < #t` and the new boundary `i = #t`: in the interior, TA5(b)'s original-position agreement at positions `i` and `i + 1` (both in `{1, …, #t}` since `i + 1 ≤ #t`) gives `t'ᵢ = tᵢ` and `t'ᵢ₊₁ = tᵢ₊₁`, and T4(ii) on `t` at index `i` (legal since `1 ≤ i < #t`) gives `¬(tᵢ = 0 ∧ tᵢ₊₁ = 0)`, hence `¬(t'ᵢ = 0 ∧ t'ᵢ₊₁ = 0)`; at the new boundary `i = #t`, the pair `(t'_{#t}, t'_{#t+1}) = (t_{#t}, 1)` — TA5(b) at `#t` (with `1 ≤ #t` by T0) gives the left entry, TA5(d)'s `t'_{#t+1} = 1` gives the right — and T4(iv) on `t`'s `t_{#t} ≠ 0` falsifies the left conjunct, while equivalently `1 ≠ 0` falsifies the right; either falsifies the conjunction. For T4(iv) on `t'`, TA5(d)'s `#t' = #t + 1` and `t'_{#t+1} = 1` give `t'_{#t'} = 1 ≠ 0`. For T4(iii), TA5(b)'s original-position agreement `(A i : 1 ≤ i ≤ #t : t'ᵢ = tᵢ)` instantiated at `i = 1` — legal since `1 ≤ #t` by T0 — gives `t'₁ = t₁`, and T4(iii) on `t` gives `t₁ ≠ 0`, hence `t'₁ ≠ 0`. T4 preserved unconditionally.

*Case `k = 2`.* By TA5(d), `#t' = #t + 2`, `t'_{#t+1} = 0`, `t'_{#t+2} = 1`; by TA5(b), original positions agree. Let `S = {i : 1 ≤ i ≤ #t ∧ tᵢ = 0}` (with `|S| = zeros(t)` by definition) and `S' = {i : 1 ≤ i ≤ #t + 2 ∧ t'ᵢ = 0}`. For `1 ≤ i ≤ #t` original-position agreement gives `t'ᵢ = tᵢ`; `t'_{#t+1} = 0` admits index `#t + 1`; `t'_{#t+2} = 1 ≠ 0` excludes index `#t + 2`. Hence `S' = S ∪ {#t + 1}`; since `S ⊆ {1, …, #t}` and `#t + 1 > #t` by NAT-addcompat's strict successor inequality, `#t + 1 ∉ S` and the union is disjoint. By NAT-card, `S` admits a unique strictly increasing enumeration `s₁ < … < s_{|S|}` with each `s_j ≤ #t < #t + 1`; appending `#t + 1` (which strictly exceeds `s_{|S|}` by the same bound) yields a strictly increasing enumeration of `S'` of length `|S| + 1`. By NAT-card's enumeration characterisation applied at `n = #t + 2` (so `S' ⊆ {1, …, #t + 2}`), `|S'| = |S| + 1`, so `zeros(t') = zeros(t) + 1`. For T4(i) on `t'`, the established `zeros(t') = zeros(t) + 1` together with T4(i) on `t` (`zeros(t) ≤ 3`) gives `zeros(t') ≤ 3` iff `zeros(t) + 1 ≤ 3`, equivalently `zeros(t) ≤ 2`. For T4(ii) on `t'`, the index range `1 ≤ i < #t' = #t + 2`, equivalently `1 ≤ i ≤ #t + 1`, splits into the interior `1 ≤ i < #t`, the original-to-appended boundary `i = #t`, and the appended-zero-adjacency index `i = #t + 1`: in the interior, TA5(b)'s original-position agreement at positions `i` and `i + 1` (both in `{1, …, #t}` since `i + 1 ≤ #t`) gives `t'ᵢ = tᵢ` and `t'ᵢ₊₁ = tᵢ₊₁`, and T4(ii) on `t` at index `i` (legal since `1 ≤ i < #t`) gives `¬(tᵢ = 0 ∧ tᵢ₊₁ = 0)`, hence `¬(t'ᵢ = 0 ∧ t'ᵢ₊₁ = 0)`; at the boundary `i = #t`, the pair `(t'_{#t}, t'_{#t+1}) = (t_{#t}, 0)` — TA5(b) at `#t` (with `1 ≤ #t` by T0) gives the left entry, TA5(d)'s `t'_{#t+1} = 0` gives the right — and T4(iv) on `t`'s `t_{#t} ≠ 0` falsifies the left conjunct, hence the conjunction; at the new index `i = #t + 1`, the pair `(t'_{#t+1}, t'_{#t+2}) = (0, 1)` by TA5(d) at both positions, and `1 ≠ 0` falsifies the right conjunct, hence the conjunction. For T4(iv) on `t'`, TA5(d)'s `#t' = #t + 2` and `t'_{#t+2} = 1` give `t'_{#t'} = 1 ≠ 0`. For T4(iii), TA5(b)'s original-position agreement `(A i : 1 ≤ i ≤ #t : t'ᵢ = tᵢ)` instantiated at `i = 1` — legal since `1 ≤ #t` by T0 — gives `t'₁ = t₁`, and T4(iii) on `t` gives `t₁ ≠ 0`, hence `t'₁ ≠ 0`. T4 preserved iff `zeros(t) ≤ 2`.

*Case `k ≥ 3`.* By TA5(d), positions `#t + 1` through `#t + k - 1` are zero. NAT-sub's conditional closure at `k ≥ 1` (implied by `k ≥ 3`) places `k − 1 ∈ ℕ`. To sharpen `k ≥ 3` to `k − 1 ≥ 2`, NAT-order's `≤` definition unfolds `3 ≤ k` to `3 < k ∨ 3 = k`, splitting the hypothesis into two sub-branches. In the sub-branch `k = 3`, NAT-sub's right telescoping (unconditional) at `(m, n) = (2, 1)` gives `(2 + 1) − 1 = 2`, i.e., `3 − 1 = 2`, so `k − 1 = 2`. In the sub-branch `3 < k`, NAT-sub's strict monotonicity at `(m, n, p) = (3, k, 1)` — with `3 ≥ 1` and `k ≥ 1` (the latter from `k ≥ 3`) — yields `3 − 1 < k − 1`, and right telescoping at `(2, 1)` rewrites the left side to `2`, so `2 < k − 1`; NAT-order's `≤` definition then lifts `2 < k − 1` to `2 ≤ k − 1`, i.e., `k − 1 ≥ 2`. In either sub-branch `k − 1 ≥ 2`, so positions `#t + 1` and `#t + 2` lie within `{#t + 1, …, #t + k − 1}` and carry zero; that is, `t'_{#t+1} = t'_{#t+2} = 0`. Suppose for contradiction that T4 holds on `t'`. T4(ii) on `t'` is `(A i : 1 ≤ i < #t' : ¬(t'ᵢ = 0 ∧ t'ᵢ₊₁ = 0))`; with `#t' = #t + k` by TA5(d), the index `i = #t + 1` is legal — `1 ≤ #t + 1` follows from T0's `1 ≤ #t` and NAT-addcompat's strict successor inequality `#t < #t + 1` by NAT-order's transitivity, and `#t + 1 < #t + k` follows from the chain `#t + 1 < #t + 2 ≤ #t + k`: NAT-addcompat's strict successor inequality at `n = #t + 1` together with NAT-addassoc's `(#t + 1) + 1 = #t + (1 + 1) = #t + 2` gives `#t + 1 < #t + 2`, and NAT-addcompat's left order compatibility at `2 ≤ k` (a consequence of `3 ≤ k` chained with the numeral `2 < 3` from NAT-addcompat's strict successor at `n = 2` via NAT-order's transitivity and `≤`-definition) gives `#t + 2 ≤ #t + k`. T4(ii) instantiated at `i = #t + 1` — with successor index `(#t + 1) + 1 = #t + 2` by the same NAT-addassoc/numeral identification — yields `¬(t'_{#t+1} = 0 ∧ t'_{#t+2} = 0)`, which directly contradicts the established `t'_{#t+1} = t'_{#t+2} = 0`. The supposition that T4 holds on `t'` is inconsistent. Witness: `inc([1], 3) = [1, 0, 0, 1]`. T4 violated. ∎

*Formal Contract:*
- *Precondition:* `t` satisfies T4; `k ≥ 0`.
- *Depends:*
  - T4 (HierarchicalParsing) — the four positional clauses being checked; cardinality bound `zeros(·) ≤ 3` (i) used on `t` (`zeros(t) ≤ 3`) and lifted to `t'` (`zeros(t') ≤ 3`) via the established `zeros(t') = zeros(t)` at cases `k = 0` and `k = 1`, and (at case `k = 2`) used to read off the iff threshold from `zeros(t') = zeros(t) + 1 ≤ 3`, i.e., `zeros(t) ≤ 2`; boundary clause `t_{#t} ≠ 0` (iv) used at case `k = 0` (via TA5-SigValid's `sig(t) = #t`) to give `t_{sig(t)} ≠ 0`, which excludes position `sig(t)` from the original zero-index set in the zero-index-set equality argument (the primed exclusion at the same position is supplied independently by TA5(c)'s `t'_{sig(t)} = t_{sig(t)} + 1` and the NAT chain `t_{sig(t)} + 1 ≠ 0`), and at cases `k = 1` and `k = 2` to falsify the left conjunct of T4(ii) on `t'` at the boundary index `i = #t`; left-boundary clause `t₁ ≠ 0` (iii) on `t` transferred to `t'₁ ≠ 0` in cases `k = 1, 2` (via TA5(b) at position `1`) and in the `sig(t) ≠ 1` sub-case of `k = 0` (same route), with the `sig(t) = 1` sub-case of `k = 0` deriving `t'₁ ≠ 0` from the NAT chain at position `1`; the no-adjacent-zeros clause T4(ii) on `t`, instantiated at index `i` with `1 ≤ i < #t`, is transferred to `t'` in the `sig(t) ∉ {i, i + 1}` sub-case of `k = 0` and in the interior branch `1 ≤ i < #t` of cases `k = 1` and `k = 2`, via TA5(b) agreement at `i` and `i + 1`; the same clause T4(ii), instantiated at `i = #t + 1` on `t'`, is the directly violated clause at `k ≥ 3`.
  - T0 (CarrierSetDefinition) — fixes carrier ℕ so every `tᵢ ∈ ℕ`; supplies `1 ≤ #t` (each tumbler has at least one component), used at four sites: in the `sig(t) ≠ 1` sub-case of case `k = 0` and in cases `k = 1` and `k = 2`, to discharge the legality of the `i = 1` instantiation of TA5(b)'s original-position agreement `(A i : 1 ≤ i ≤ #t : t'ᵢ = tᵢ)` for the T4(iii) transfer `t'₁ = t₁`; and at case `k ≥ 3`, to discharge the lower bound `1 ≤ #t + 1` for the T4(ii) instantiation index.
  - NAT-zero (NatZeroMinimum) — lower bound `0 ≤ n` on ℕ.
  - NAT-closure (NatArithmeticClosureAndIdentity) — addition closure instantiated at `(t_{sig(t)}, 1)` with `1 ∈ ℕ` from the same axiom places `t_{sig(t)} + 1 ∈ ℕ` at case `k = 0`. At case `k ≥ 3`, closure is consumed at the manipulated sums so the cited NAT-addcompat strict-successor and left-order-compatibility instantiations and the NAT-addassoc identification stay within signature: closure at `(#t, 1)` places `#t + 1 ∈ ℕ`, typing NAT-addcompat's strict-successor conclusion at `n = #t` (`#t < #t + 1`) as a comparison between ℕ-elements, supporting T0's `1 ≤ #t` chained via NAT-order's transitivity with that successor to give `1 ≤ #t + 1` between ℕ-elements, and admitting NAT-addcompat's strict-successor instantiation at `n = #t + 1`; closure at `(#t, 2)` places `#t + 2 ∈ ℕ`, typing the strict-successor inequality `#t + 1 < #t + 2` and NAT-addcompat's left-order-compatibility conclusion `#t + 2 ≤ #t + k` as comparisons between ℕ-elements; closure at `(#t, k)` places `#t + k ∈ ℕ`, matching TA5(d)'s `#t' = #t + k` so the chain `#t + 1 < #t + 2 ≤ #t + k = #t'` stays within ℕ; closure at `(#t + 1, 1)` places `(#t + 1) + 1 ∈ ℕ` and closure at `(1, 1)` places `1 + 1 ∈ ℕ`, so NAT-addassoc's identification `(#t + 1) + 1 = #t + (1 + 1) = #t + 2` chains through ℕ-elements at every term.
  - NAT-addcompat (NatAdditionOrderAndSuccessor) — strict successor inequality `n < n + 1` at case `k = 0`; at case `k ≥ 3`, strict successor at `n = #t` lifts T0's `1 ≤ #t` to `1 ≤ #t + 1`, strict successor at `n = #t + 1` and `n = 2` participate in the chain `#t + 1 < #t + 2` (via NAT-addassoc) and `2 < 3 ≤ k` respectively, and left order compatibility `(A m, n, p ∈ ℕ : p ≤ n : m + p ≤ m + n)` at `(m, p, n) = (#t, 2, k)` lifts `2 ≤ k` to `#t + 2 ≤ #t + k`.
  - NAT-addassoc (NatAdditionAssociative) — at case `k ≥ 3`, identifies `(#t + 1) + 1 = #t + (1 + 1) = #t + 2` so that NAT-addcompat's strict successor inequality at `n = #t + 1` reads as `#t + 1 < #t + 2`; the same identification supplies the successor index `(#t + 1) + 1 = #t + 2` for the T4(ii) instantiation at `i = #t + 1`, against which `t'_{#t+2} = 0` is matched.
  - NAT-order (NatStrictTotalOrder) — at case `k = 0`, transitivity chains NAT-addcompat's strict successor inequality `t_{sig(t)} + 1 > t_{sig(t)}` with NAT-zero's lower bound `t_{sig(t)} ≥ 0` to give `t_{sig(t)} + 1 > 0`, and irreflexivity (equivalently, the exactly-one trichotomy clause `¬(m < n ∧ m = n)` derived from irreflexivity, which routes `> 0` to `≠ 0`) lifts `t_{sig(t)} + 1 > 0` to `t_{sig(t)} + 1 ≠ 0`; the resulting `≠ 0` conclusion is consumed at four sites within the case — the zero-index set equality's primed exclusion at position `sig(t)` (combining with TA5(c)'s `t'_{sig(t)} = t_{sig(t)} + 1` to give `t'_{sig(t)} ≠ 0`), T4(ii)'s `i + 1 = sig(t) = #t` sub-branch (combining with TA5(c)'s `t'_{sig(t)} = t_{sig(t)} + 1` at position `i + 1` to falsify `t'ᵢ₊₁ = 0`), T4(iv)'s discharge (combining with TA5(c)'s `t'_{sig(t)} = t_{sig(t)} + 1` and TA5-SigValid's `sig(t) = #t` to give `t'_{#t'} ≠ 0`), and T4(iii)'s `sig(t) = 1` sub-case (where reusing the chain at position `1` gives `t'₁ ≠ 0`). At case `k ≥ 3`, at-least-one trichotomy (via the `≤` definition unfolding `3 ≤ k` to `3 < k ∨ 3 = k`) splits `k ≥ 3` into the sub-branches `k = 3` and `3 < k`; the same `≤` definition lifts `2 < k − 1` to `2 ≤ k − 1` (i.e., `k − 1 ≥ 2`) in the `3 < k` sub-branch, and lifts `2 < 3` to `2 ≤ 3` (chained with `3 ≤ k` via transitivity to give `2 ≤ k`); transitivity additionally chains `1 ≤ #t < #t + 1` (giving `1 ≤ #t + 1`) and `#t + 1 < #t + 2 ≤ #t + k = #t'` (giving `#t + 1 < #t'`).
  - NAT-sub (NatPartialSubtraction) — conditional closure at `k ≥ 1` places `k − 1 ∈ ℕ`; right telescoping at `(m, n) = (2, 1)` gives `3 − 1 = 2` (used directly in sub-branch `k = 3` and to rewrite the left side of the strict-monotonicity conclusion in sub-branch `3 < k`); strict monotonicity at `(m, n, p) = (3, k, 1)` gives `3 − 1 < k − 1` in sub-branch `3 < k`; together these derive `k − 1 ≥ 2` at case `k ≥ 3`.
  - NAT-card (NatFiniteSetCardinality) — well-definedness of `|·|` as a total function on subsets of every initial segment `{1, …, n} ⊆ ℕ` lifts set-equality of zero-index subsets to cardinality equality at cases `k = 0` (subsets of `{1, …, #t}`) and `k = 1` (subsets of `{1, …, #t + 1}`); the enumeration characterisation, applied at `n = #t + 2`, lifts the disjoint extension `S' = S ∪ {#t + 1}` (with `#t + 1` strictly greater than every element of `S`) to `|S'| = |S| + 1` at case `k = 2`.
  - TA5 (HierarchicalIncrement) — TA5(b) agreement clauses; TA5(c) for `k = 0`; TA5(d) for `k ≥ 1`.
  - TA5-SigValid (SigOnValidAddresses) — `sig(t) = #t` on T4-valid `t` at case `k = 0`.
- *Guarantee:* `inc(t, k)` satisfies T4 iff `k ∈ {0, 1}`, or `k = 2 ∧ zeros(t) ≤ 2`.
- *Failure:* The Guarantee's iff yields two failure regions on the precondition domain (`t` satisfies T4, so `zeros(t) ∈ {0, 1, 2, 3}` by T4(i); `k ∈ ℕ`): (a) `k ≥ 3`, and (b) `k = 2 ∧ zeros(t) = 3`. In mode (a), T4(ii) on `t'` is the directly violated conjunct: by TA5(d) and the established `k − 1 ≥ 2`, the appended separator zeros at positions `#t + 1` and `#t + 2` are adjacent indices of `t'` carrying zero, so T4(ii) instantiated at `i = #t + 1` fails on `t'`. In mode (b), T4(i) on `t'` is the directly violated conjunct: by Case `k = 2` of the proof, `zeros(t') = zeros(t) + 1`, so the precondition `zeros(t) = 3` (admitted by T4(i) on `t`) yields `zeros(t') = 4`, exceeding the bound `zeros(·) ≤ 3` required by T4(i).

**TA5-SIG (LastSignificantPosition).** We define the *last significant position* of a tumbler `t ∈ T`, written `sig(t)`.

When `t` has at least one nonzero component — that is, `(E i : 1 ≤ i ≤ #t : tᵢ ≠ 0)` — we set `sig(t)` to the rightmost index at which `t` is nonzero. Let `S = {i : 1 ≤ i ≤ #t ∧ tᵢ ≠ 0}`; the existence hypothesis makes `S` nonempty, and every `i ∈ S` is bounded above by `#t`.

The maximum of a bounded nonempty ℕ-subset is not delivered directly by NAT-wellorder, which states only the *least-element* principle; ℕ has no greatest element, so the principle does not dualize unconditionally, and greatest elements are guaranteed only on subsets bounded above. We derive `max(S)` from the least-element principle with `#t` as the explicit boundedness witness. Form the upper-bound set `U = {u ∈ ℕ : (A i ∈ S :: i ≤ u)}`; every `i ∈ S` satisfies `i ≤ #t`, so `#t ∈ U` and `U ≠ ∅`. NAT-wellorder applied to `U` delivers a least upper bound `m`. We claim `m ∈ S`. Suppose otherwise: every `i ∈ S` satisfies `i ≤ m` (since `m ∈ U`) and `i ≠ m` (since `m ∉ S`), so NAT-order's `≤`-defining clause `i ≤ m ⟺ i < m ∨ i = m` forces `i < m`, and NAT-discrete's forward direction then gives `i + 1 ≤ m` for every `i ∈ S`. Fixing any `i₀ ∈ S` — `S ≠ ∅` supplies such a witness — we have `1 ≤ i₀` (since `S ⊆ {1, …, #t}`), and NAT-addcompat's strict successor inequality supplies `i₀ < i₀ + 1`. The chain `1 ≤ i₀ < i₀ + 1 ≤ m` carries two weak bounds, and NAT-order's `≤`-defining clause `p ≤ q ⟺ p < q ∨ p = q` splits each into a `<`-or-`=` disjunction, producing the four sub-cases `(1 < i₀ ∨ 1 = i₀) × (i₀ + 1 < m ∨ i₀ + 1 = m)`. In `1 < i₀ ∧ i₀ + 1 < m`, NAT-order's transitivity of `<` composes `1 < i₀`, `i₀ < i₀ + 1`, `i₀ + 1 < m` into `1 < m`. In `1 < i₀ ∧ i₀ + 1 = m`, transitivity composes `1 < i₀` with `i₀ < i₀ + 1` into `1 < i₀ + 1`, and substituting `m` for `i₀ + 1` yields `1 < m`. In `1 = i₀ ∧ i₀ + 1 < m`, transitivity composes `i₀ < i₀ + 1` with `i₀ + 1 < m` into `i₀ < m`, and substituting `1` for `i₀` yields `1 < m`. In `1 = i₀ ∧ i₀ + 1 = m`, the strict segment `i₀ < i₀ + 1` rewrites by both substitutions to `1 < m` directly. All four sub-cases close on `1 < m`, hence `m ≥ 1`. NAT-sub's conditional closure at `m ≥ 1` supplies `m − 1 ∈ ℕ`. The value `m − 1` is strictly below `m`: NAT-sub's right-inverse gives `(m − 1) + 1 = m`, and NAT-addcompat's `(m − 1) < (m − 1) + 1` rewrites via that identity to `m − 1 < m`. And `m − 1` bounds `S`: each `i ∈ S` satisfies `i + 1 ≤ m`, which splits via NAT-order's `≤`-defining clause into `i + 1 = m` (then NAT-sub's right telescoping `(i + 1) − 1 = i` gives `i = m − 1`) or `i + 1 < m` (then NAT-sub's strict monotonicity at `p = 1` requires both `i + 1 ≥ 1` and `m ≥ 1`; `m ≥ 1` is available from the chain `1 ≤ i₀ < i₀ + 1 ≤ m` established above, and `i + 1 ≥ 1` is obtained for the running `i ∈ S` by chaining `1 ≤ i` (since `S ⊆ {1, …, #t}`) with NAT-addcompat's strict successor inequality `i < i + 1` — the weak bound `1 ≤ i` dispatched into `<`-or-`=` cases by NAT-order's `≤`-defining clause and the strict segment composed by NAT-order's transitivity of `<` — yielding `1 < i + 1`, hence `1 ≤ i + 1` by the `≤`-defining clause; strict monotonicity then gives `(i + 1) − 1 < m − 1`, i.e., `i < m − 1`); in both cases `i ≤ m − 1`. So `m − 1 ∈ U` with `m − 1 < m`, contradicting minimality of `m` in `U`. Therefore `m ∈ S`. This least element `m` of `U` is moreover uniquely determined: if `m' ∈ U` also satisfies `(A n ∈ U :: m' ≤ n)`, instantiating `m'`'s lower-bound clause at `n := m` (using `m ∈ U`) gives `m' ≤ m`, and instantiating `m`'s lower-bound clause at `n := m'` (using `m' ∈ U`) gives `m ≤ m'`. NAT-order's `≤`-defining clause unfolds the conjunction `m ≤ m' ∧ m' ≤ m` into four sub-cases, and NAT-order's exactly-one trichotomy at `(m, m')` excludes the three sub-cases involving a strict inequality — `m < m' ∧ m' < m` by the mutual-exclusion clause `¬(m < m' ∧ m' < m)`; `m = m' ∧ m' < m` by `¬(m = m' ∧ m' < m)` directly; `m < m' ∧ m' = m` by `¬(m < m' ∧ m = m')` after symmetrizing `m' = m` to `m = m'`. The surviving sub-case `m = m' ∧ m' = m` yields `m = m'`. So `m` is the unique least element of `U`; since `m ∈ S` and every `i ∈ S` satisfies `i ≤ m` (from `m ∈ U`), `m` satisfies the maximum predicate on `S`, and we set `sig(t) = m = max(S)`.

When every component of `t` is zero — that is, `(A i : 1 ≤ i ≤ #t : tᵢ = 0)` — we set `sig(t) = #t`.

In both cases `1 ≤ sig(t) ≤ #t`, since `#t ≥ 1` for every `t ∈ T`.

*Formal Contract:*
- *Preconditions:* `t ∈ T` (any tumbler with `#t ≥ 1`).
- *Definition:* `sig(t) = max({i : 1 ≤ i ≤ #t ∧ tᵢ ≠ 0})` when `(E i : 1 ≤ i ≤ #t : tᵢ ≠ 0)`; `sig(t) = #t` when `(A i : 1 ≤ i ≤ #t : tᵢ = 0)`.
- *Depends:*
  - T0 (CarrierSetDefinition) — supplies `t ∈ T` as finite ℕ-sequences with `#t ≥ 1`, component projection `tᵢ`, and the length `#t`.
  - NAT-zero (NatZeroMinimum) — supplies `0 ∈ ℕ` for the literal `0` appearing in the set-comprehension condition `tᵢ ≠ 0` of the nonzero-case definition `sig(t) = max({i : 1 ≤ i ≤ #t ∧ tᵢ ≠ 0})` and in the all-zero condition `(A i : 1 ≤ i ≤ #t : tᵢ = 0)` of the all-zero-case definition.
  - NAT-closure (NatArithmeticClosureAndIdentity) — supplies `1 ∈ ℕ` and closure of ℕ under addition.
  - NAT-wellorder (NatWellOrdering) — supplies the least-element principle.
  - NAT-order (NatStrictTotalOrder) — supplies the `≤`-defining clause `p ≤ q ⟺ p < q ∨ p = q`, transitivity of `<`, and the exactly-one trichotomy mutual-exclusion clauses `¬(m < n ∧ n < m)`, `¬(m < n ∧ m = n)`, `¬(m = n ∧ n < m)` — used to derive antisymmetry of `≤` from `m ≤ m' ∧ m' ≤ m`, hence uniqueness of the least element of `U`.
  - NAT-discrete (NatDiscreteness) — supplies the forward direction `i < m ⟹ i + 1 ≤ m`.
  - NAT-sub (NatPartialSubtraction) — supplies conditional closure `m ≥ 1 ⟹ m − 1 ∈ ℕ`, the right-inverse `(m − 1) + 1 = m`, the right-telescoping clause `(i + 1) − 1 = i`, and strict monotonicity at `p = 1`.
  - NAT-addcompat (NatAdditionOrderAndSuccessor) — supplies the strict successor inequality `(A n ∈ ℕ :: n < n + 1)`.
- *Postconditions:* `1 ≤ sig(t) ≤ #t`.

**TA5-SigValid (SigOnValidAddresses).** For every valid address `t` satisfying T4, `sig(t) = #t`.

*Proof.* Let `t` be a valid address satisfying T4. T4 gives `t_{#t} ≠ 0`. T0 fixes the carrier as ℕ, so `t_{#t} ∈ ℕ`. NAT-zero supplies `0 < t_{#t} ∨ 0 = t_{#t}`; T4's `t_{#t} ≠ 0` excludes the equality branch, leaving `0 < t_{#t}`.

Since `t_{#t} > 0`, by TA5-SIG, `sig(t) = max(S)` where `S = {i : 1 ≤ i ≤ #t ∧ tᵢ ≠ 0}`; the range predicate `1 ≤ i ≤ #t` reads through NAT-order's `≤` definition. The index `#t` satisfies `1 ≤ #t ≤ #t` — the left bound by T0's `#t ≥ 1` lifted through the same definition, the right bound by reflexivity of `=` — and `t_{#t} ≠ 0` by T4, so `#t ∈ S` and `sig(t) ≥ #t`. TA5-SIG's postcondition gives `sig(t) ≤ #t`. Combining the two through antisymmetry of `≤` — supplied by NAT-order via exactly-one trichotomy, which eliminates the three disjoint-pair cases `m < n ∧ n < m`, `m < n ∧ m = n`, and `m = n ∧ n < m` from the four-way distribution of the conjoined disjunctions — yields `sig(t) = #t`. ∎

*Formal Contract:*
- *Preconditions:* `t` satisfies T4.
- *Depends:*
  - T4 (HierarchicalParsing) — supplies `t_{#t} ≠ 0`.
  - T0 (CarrierSetDefinition) — fixes carrier as ℕ, giving `t_{#t} ∈ ℕ`, and supplies `#t ≥ 1` for every `t ∈ T`.
  - NAT-zero (NatZeroMinimum) — supplies the disjunction `0 < t_{#t} ∨ 0 = t_{#t}`; T4's `t_{#t} ≠ 0` eliminates the equality branch, yielding `0 < t_{#t}`.
  - NAT-order (NatStrictTotalOrder) — supplies the `≤`-defining clause `m ≤ n ⟺ m < n ∨ m = n`, used (a) to interpret TA5-SIG's range predicate `1 ≤ i ≤ #t` and the postcondition `sig(t) ≤ #t`, (b) to witness `1 ≤ #t ≤ #t` (hence `#t ∈ S`); supplies antisymmetry of `≤` — derived from the exactly-one trichotomy clauses `¬(m < n ∧ n < m)`, `¬(m < n ∧ m = n)`, `¬(m = n ∧ n < m)` — to combine `sig(t) ≥ #t` and `sig(t) ≤ #t` into `sig(t) = #t`.
  - TA5-SIG (LastSignificantPosition) — unfolds `sig(t)` as the maximum-position formula when `t_{#t} > 0` and supplies the range postcondition `sig(t) ≤ #t`.
- *Postconditions:* `sig(t) = #t`.

**TA6 (ZeroTumblers).** No zero tumbler is a valid address.

  `(A t ∈ T : Zero(t) ⟹ t is not a valid address)`

*Proof (from T0, T4, TA-Pos).* Let `t ∈ T` with `Zero(t)`. Unpacking `Zero(t)` via TA-Pos gives `tᵢ = 0` for all `1 ≤ i ≤ #t`. From T0, `#t ≥ 1`, so `t₁` is defined and equals `0`. This violates T4's requirement `t₁ ≠ 0`, so `t` is not a valid address. ∎

*Formal Contract:*
- *Depends:*
  - T0 (CarrierSetDefinition) — `#t ≥ 1` and components in ℕ.
  - T4 (HierarchicalParsing) — boundary clause `t₁ ≠ 0`.
  - TA-Pos (PositiveTumbler) — definition of `Zero(t)`.
- *Forward References:*
  - TA-PosDom (PositiveDominatesZero) — uses zero tumblers as the dominated class in its ordering result; TA6 sentinels are the context for that pairing.
- *Postcondition:* `(A t ∈ T : Zero(t) ⟹ t is not a valid address)`.

Zero tumblers thus exist in `T` but lie outside the address-valid subset; paired with TA-PosDom's ordering result they act as sentinels — uninitialized markers, unbounded span endpoints, and lower bounds.

### Zero tumblers and positivity

**TA-Pos (PositiveTumbler).** A tumbler `t ∈ T` is *positive*, written `Pos(t)`, iff `(E i ∈ ℕ : 1 ≤ i ≤ #t : ¬(tᵢ = 0))`. A tumbler `t ∈ T` is a *zero tumbler*, written `Zero(t)`, iff `(A i ∈ ℕ : 1 ≤ i ≤ #t : tᵢ = 0)`.

The two predicates are complementary: `(A t ∈ T :: Pos(t) ⟺ ¬Zero(t))`. This equivalence rests on logic alone: the matrix of the `Pos` clause is the negation of the matrix of the `Zero` clause, and by the DeMorgan duality of bounded quantifiers, `(E i ∈ ℕ : 1 ≤ i ≤ #t : ¬(tᵢ = 0)) ⟺ ¬(A i ∈ ℕ : 1 ≤ i ≤ #t : tᵢ = 0)`.

Reading the Definition against T0 gives the content of this partition: T0's clause `(A a ∈ T :: 1 ≤ #a)` guarantees that every `t ∈ T` has at least one index in range, so `Pos(t)` demands a nonzero component (the existential is not vacuous) and `Zero(t)` forces every component to equal `0` (the universal is not vacuous).

The set of zero tumblers is written **Z** = {t ∈ T : Zero(t)}.

*Formal Contract:*
- *Definition:* `(A t ∈ T :: Pos(t) ⟺ (E i ∈ ℕ : 1 ≤ i ≤ #t : ¬(tᵢ = 0)))`; `(A t ∈ T :: Zero(t) ⟺ (A i ∈ ℕ : 1 ≤ i ≤ #t : tᵢ = 0))`; **Z** = {t ∈ T : Zero(t)}.
- *Consequence:* `(A t ∈ T :: Pos(t) ⟺ ¬Zero(t))`.
- *Depends:*
  - T0 (CarrierSetDefinition) — carrier `T`, length `#t`, component projection `tᵢ`, and the nonemptiness clause `(A a ∈ T :: 1 ≤ #a)` cited in prose to unpack the Definition's quantifier ranges.
  - NAT-carrier (NatCarrierSet) — supplies `ℕ` as the underlying set appearing in the bounded existential `(E i ∈ ℕ : 1 ≤ i ≤ #t : ¬(tᵢ = 0))` of the `Pos` clause and the bounded universal `(A i ∈ ℕ : 1 ≤ i ≤ #t : tᵢ = 0)` of the `Zero` clause, over which the index variable `i` ranges before being further restricted by the carrier-side clause `i ∈ ℕ` and the term-side range `1 ≤ i ≤ #t`.
  - NAT-zero (NatZeroMinimum) — supplies `0 ∈ ℕ` for the literal appearing in `tᵢ = 0`.
  - NAT-order (NatStrictTotalOrder) — supplies `≤` on ℕ for the bounded-quantifier range `1 ≤ i ≤ #t`.
  - NAT-closure (NatArithmeticClosureAndIdentity) — supplies `1 ∈ ℕ` for the numeral bounding that range.

**TA-PosDom (PositiveDominatesZero).** `(A t ∈ T, z ∈ T : Pos(t) ∧ Zero(z) :: z < t)` — every positive tumbler is strictly greater under T1 than every zero tumbler of any length.

*Proof.* Let `t ∈ T` with `Pos(t)` and `z ∈ T` with `Zero(z)`; we show `z < t`. Before the case analysis we extract a witnessing index `k` from `Pos(t)` directly. TA-Pos unpacks `Pos(t)` to the existential `(E i ∈ ℕ : 1 ≤ i ≤ #t : ¬(tᵢ = 0))`, so the set `S = {i : 1 ≤ i ≤ #t ∧ tᵢ ≠ 0}` is nonempty; T0's commitment that the index domain `{1, …, #t}` is a subset of ℕ gives `S ⊆ ℕ`. NAT-wellorder then supplies some `k ∈ S` with `(A n ∈ S :: k ≤ n)`. Membership `k ∈ S` yields (i) `1 ≤ k ≤ #t` together with `tₖ ≠ 0`. Minimality yields (ii) `tᵢ = 0` for all `1 ≤ i < k`: such an `i` lies in `{1, …, #t}`, and if `tᵢ ≠ 0` it would sit in `S` below `k`, contradicting `(A n ∈ S :: k ≤ n)`. For (iii) `0 < tₖ`: T0 places `tₖ ∈ ℕ`; instantiating NAT-zero's disjunction `(A n ∈ ℕ :: 0 < n ∨ 0 = n)` at `n = tₖ` and excluding the equality branch via `tₖ ≠ 0` leaves `0 < tₖ`. Unpacking `Zero(z)` gives `zᵢ = 0` for all `1 ≤ i ≤ #z`. Distinguish two cases by the relationship between `#z` and `k`.

*Case `#z ≥ k`.* For `1 ≤ i < k`, `zᵢ = 0` (from `Zero(z)`, since `i < k ≤ #z`) and `tᵢ = 0` (by (ii)), so `zᵢ = tᵢ`. The case hypothesis gives `k ≤ #z`, and (i) gives `k ≤ #t`. At `i = k`: `zₖ = 0` (from `Zero(z)`), and (iii) supplies `0 < tₖ`, so `zₖ < tₖ`. By T1 case (i) with witness `k`, `z < t`.

*Case `#z < k`.* T1 case (ii)'s schema, instantiated at witness `#z + 1`, demands agreement on `(A i : 1 ≤ i < #z + 1 :: zᵢ = tᵢ)`; we discharge this obligation directly over that range. Fix `i` with `1 ≤ i < #z + 1`. NAT-order's trichotomy at `(i, #z)` partitions into `i < #z ∨ i = #z ∨ #z < i`; the third disjunct is excluded, since NAT-discrete at `m = #z, n = i` would then yield `#z + 1 ≤ i`, contradicting `i < #z + 1`. The remaining two disjuncts together give `i ≤ #z` via the `≤`-defining clause `m ≤ n ⟺ m < n ∨ m = n`. Composing `i ≤ #z` with the case hypothesis `#z < k` by NAT-order's `≤`/`<` composition gives `i < k`, so `tᵢ = 0` (by (ii)). And `1 ≤ i ≤ #z` places `i` in `Zero(z)`'s range, so `zᵢ = 0`. Hence `zᵢ = tᵢ`, discharging the agreement. From `#z < k` and (i)'s `k ≤ #t`, NAT-order's `<`/`≤` composition yields `#z < #t`. NAT-discrete (with NAT-order) gives `m < n ⟹ m + 1 ≤ n` for `m, n ∈ ℕ`; at `m = #z, n = #t` this yields `#z + 1 ≤ #t`. T1's schema also requires its witness to satisfy the top-level bound `1 ≤ #z + 1`: T0 supplies `1 ≤ #z` from the nonemptiness of `z ∈ T`, NAT-addcompat's strict successor inequality gives `#z < #z + 1`, and NAT-order's `<`/`≤` composition of `1 ≤ #z` with `#z < #z + 1` yields `1 < #z + 1`, hence `1 ≤ #z + 1` via the `≤`-defining clause `m ≤ n ⟺ m < n ∨ m = n`. By T1 case (ii) with witness `#z + 1`, `z < t`. ∎

*Formal Contract:*
- *Preconditions:* `t ∈ T`, `Pos(t)`; `z ∈ T`, `Zero(z)`.
- *Depends:*
  - T0 (CarrierSetDefinition) — carrier `T`, length `#·`, component projection; commitment that the index domain `{1, …, #t}` is a subset of ℕ (used to place `S ⊆ ℕ`) and that each `tᵢ ∈ ℕ`.
  - TA-Pos (PositiveTumbler) — `Pos` and `Zero` predicate definitions; unpacks `Pos(t)` to the existential whose witnesses populate `S`.
  - NAT-wellorder (NatWellOrdering) — least-element principle applied to `S` to supply the minimal index `k`.
  - NAT-zero (NatZeroMinimum) — disjunction axiom `(A n ∈ ℕ :: 0 < n ∨ 0 = n)` instantiated at `n = tₖ` to derive `0 < tₖ` from `tₖ ≠ 0`.
  - NAT-discrete (NatDiscreteness) — forward form `m < n ⟹ m + 1 ≤ n`, used at `m = #z, n = #t` to obtain `#z + 1 ≤ #t`, and at `m = #z, n = i` in Case `#z < k` to exclude the `#z < i` branch of trichotomy when discharging T1(ii)'s agreement obligation.
  - NAT-addcompat (NatAdditionOrderAndSuccessor) — strict successor inequality `#z < #z + 1`, used with NAT-order's `<`/`≤` composition to discharge T1's top-level schema bound `1 ≤ #z + 1` for the witness `#z + 1` in Case `#z < k`.
  - NAT-order (NatStrictTotalOrder) — `<`/`≤` transitivity and irreflexivity used both in the least-element witness and in the case analyses, trichotomy at `(i, #z)` used in Case `#z < k` to reduce a generic `i` with `1 ≤ i < #z + 1` to `i ≤ #z` so that T1(ii)'s agreement schema can be discharged on its native range, and the `≤`-defining clause `m ≤ n ⟺ m < n ∨ m = n` used to compose strict with non-strict bounds (including the discharge of `1 ≤ #z + 1` and the assembly of `i ≤ #z` from the surviving trichotomy disjuncts).
  - T1 (LexicographicOrder) — case (i) in `#z ≥ k`, case (ii) in `#z < k`.
- *Postconditions:* `(A t ∈ T, z ∈ T : Pos(t) ∧ Zero(z) :: z < t)`.

**TA-dom (DisplacementDominance).** `(A a, w ∈ T : Pos(w) ∧ actionPoint(w) ≤ #a : a ⊕ w ≥ w)`.

TA-dom exports TumblerAdd's fourth postcondition — `a ⊕ w ≥ w (T1, T3)` — as a single labelled corollary for downstream use.

*Proof.* Immediate from TumblerAdd's *dominance guarantee* postcondition `a ⊕ w ≥ w (T1, T3)` under the preconditions `a, w ∈ T`, `Pos(w)`, `actionPoint(w) ≤ #a`, which are exactly TA-dom's hypotheses. ∎

*Formal Contract:*
- *Preconditions:* `a ∈ T`, `w ∈ T`, `Pos(w)`, `k ≤ #a` where `k` is the action point of `w`
- *Depends:*
  - TumblerAdd — sole arithmetic source; exports `a ⊕ w ≥ w (T1, T3)` as its fourth postcondition.
  - TA-Pos (PositiveTumbler) — licenses `Pos(w)` precondition and the existence of the action point.
  - ActionPoint — licenses `actionPoint(w) ≤ #a` precondition.
  - TA0 (WellDefinedAddition) — supplies `a ⊕ w ∈ T` (so T1's ordering applies on the left) and `#(a ⊕ w) = #w` (consumed by T3 in the equality case).
  - T1 (LexicographicOrder) — meaning of `≥` via `a ≥ b ⟺ b ≤ a` and `a ≤ b ⟺ a < b ∨ a = b`.
  - T3 (CanonicalRepresentation) — equality-from-component-agreement-and-equal-length, used when `aᵢ = 0` for all `i ≤ k`.
- *Postconditions:* `a ⊕ w ≥ w`


---

## 9. Subspace closure

TA7a establishes that arithmetic operations applied within a subspace produce results in the same subspace — the subspace is closed under permitted operations. The decomposition TA7a.1, TA7a.2, TA7a.3 separates closure under addition, subtraction, and increment respectively.

### Subspace closure

When arithmetic advances a position within one element subspace, the result must remain in that subspace. We state this as a pair of closure theorems for `⊕` and `⊖` whose preconditions are tight enough to keep every component of the result strictly positive, so that no component collapses to a zero that would either exit the subspace into the zero-padded residue `T \ S` or collapse the whole result to the zero tumbler `Z`. The case-analytic residues — length overflow (TA7a.1), interior divergence (TA7a.2), and self-subtraction to `Z` (TA7a.3) — are relocated to sub-claims whose preconditions are the complementary fragments of the theorem's precondition lattice.

**TA7a (SubspaceClosure).** A position in a subspace with identifier `N` and ordinal `o = [o₁, ..., oₘ]` (where `m ≥ 1`) is represented as the tumbler `o` for arithmetic purposes, with `N` held as structural context. Define **S** = {o ∈ T : #o ≥ 1 ∧ (A i : 1 ≤ i ≤ #o : oᵢ > 0)}. An element-local displacement is a positive tumbler `w` with action point `k = actionPoint(w)` satisfying `1 ≤ k ≤ m`. Then:

  `(A o ∈ S, w ∈ T : Pos(w) ∧ k ≤ #o ∧ (A i : k ≤ i ≤ #w : wᵢ > 0) ⟹ o ⊕ w ∈ S)`

  `(A o ∈ S, w ∈ T : Pos(w) ∧ o ≥ w ∧ k ≤ #o ∧ #w ≤ #o ∧ o₁ > w₁ ⟹ o ⊖ w ∈ S)`

The tail-positivity precondition on `w` in the `⊕`-conjunct keeps the trailing components of the result — which TumblerAdd copies verbatim from `w` at positions `i > k` — strictly positive; dropping it admits a displacement whose interior zero survives into the result and exits `S`. In the `⊖`-conjunct, `k ≤ #o` enforces the element-local restriction on `w` stated above (parallel to the `⊕`-conjunct's bound); `#w ≤ #o` forecloses the length-overflow escape characterised by TA7a.1; and `o₁ > w₁` forces divergence at position 1, keeping `r₁ > 0` (against the leading-zero escape characterised by TA7a.2) and the tail `rᵢ = oᵢ > 0` drawn from `o ∈ S` (against the collapse to `Z` characterised by TA7a.3). When `k ≥ 2`, ActionPoint gives `w₁ = 0`, so `o ∈ S` supplies `o₁ > 0 = w₁` automatically; the `o₁ > w₁` precondition only imposes a genuine restriction at `k = 1`, where it rules out the `o₁ = w₁` cases that TA7a.2 and TA7a.3 address.

The subspace identifier is not an operand; it determines which positions are subject to the shift but never enters the arithmetic.

*Proof.* Let `o = [o₁, ..., oₘ]` with `o ∈ S`, and let `w` be positive with action point `k`.

**Conjunct 1** (`⊕`-closure in `S`). From `o, w ∈ T`, `Pos(w)`, and `k ≤ #o`, TA0 gives `r := o ⊕ w ∈ T` with `#r = #w`. By TumblerAdd's three-region componentwise formula, `rᵢ = oᵢ` for `1 ≤ i < k`; `rₖ = oₖ + wₖ`; `rᵢ = wᵢ` for `k < i ≤ #w`. We show each region is positive.

*Pre-action* (`1 ≤ i < k`): `i < k ≤ #o = m` places `i` in the range of `S`'s universal clause on `o`, giving `rᵢ = oᵢ > 0`.

*Action point* (`i = k`): `rₖ = oₖ + wₖ > 0` by NAT-addcompat's left order-compatibility (at `m := oₖ, n := wₖ, p := 1`) lifting `wₖ ≥ 1` — supplied by ActionPoint's minimum-value clause — to `oₖ + wₖ ≥ oₖ + 1`; NAT-addcompat's strict successor gives `oₖ + 1 > oₖ`; NAT-order's `≤` defining clause together with transitivity of `<` compose these into `oₖ + wₖ > oₖ`; chaining with `oₖ > 0` (from `o ∈ S`) via transitivity yields `oₖ + wₖ > 0`.

*Tail* (`k < i ≤ #w`): `rᵢ = wᵢ > 0` by the tail-positivity precondition `(A i : k ≤ i ≤ #w : wᵢ > 0)` restricted to its upper sub-range.

Every index in `[1, #r] = [1, #w]` carries a positive component; with `#r = #w ≥ 1` from T0, we conclude `r ∈ S`. For single-component ordinals, `[x] ⊕ [n] = [x + n] ∈ S`.

Example: `[1, 3, 2] ⊕ [0, 2, 7] = [1, 5, 7]` (action point `k = 2`, tail positive).

**Conjunct 2** (`⊖`-closure in `S`). From `o, w ∈ T` and `o ≥ w`, TA2 gives `r := o ⊖ w ∈ T`. The length precondition `#w ≤ #o` selects — via NAT-order's trichotomy on `(#o, #w)` — either sub-case (α) `#o = #w` with `L = #o` or sub-case (γ) `#w < #o` with `L = #o`; in either `L = #o = m`. Since `o₁ > w₁` gives `o₁ ≠ w₁`, the zero-padded sequences disagree at position 1, and by ZPD's minimality `zpd(o, w) = 1`. TumblerSub's componentwise formula then gives `r₁ = o₁ − w₁`, `rᵢ = oᵢ` (zero-padded) for `1 < i ≤ L = m`, and `#r = L = m`.

*Divergence point* (`i = 1`): NAT-sub's strict-positivity clause `(A m, n ∈ ℕ : m > n : m − n ≥ 1)` at `(o₁, w₁)` lifts `o₁ > w₁` directly to `r₁ = o₁ − w₁ ≥ 1 > 0`.

*Tail* (`1 < i ≤ m`): the position lies within `1 < i ≤ m = #o`, so no zero-padding applies and `rᵢ = oᵢ`; `oᵢ > 0` by `o ∈ S`.

Every index in `[1, #r] = [1, m]` carries a positive component; with `#r = m ≥ 1`, we conclude `r ∈ S`. For single-component ordinals (`m = 1`, `#w = 1`), `[x] ⊖ [n] = [x − n] ∈ S` when `x > n`. ∎

The restriction to element-local displacements is necessary: an unrestricted displacement whose action point falls at the subspace-identifier position could produce an address in a different subspace.

*Formal Contract:*
- *Preconditions:* For `⊕`: `o ∈ S`, `w ∈ T`, `Pos(w)`, `actionPoint(w) ≤ #o`, `(A i : actionPoint(w) ≤ i ≤ #w : wᵢ > 0)`. For `⊖`: `o ∈ S`, `w ∈ T`, `Pos(w)`, `o ≥ w`, `actionPoint(w) ≤ #o`, `#w ≤ #o`, `o₁ > w₁`.
- *Depends:*
  - T0 (CarrierSetDefinition) — supplies carrier `T`, length operator `#`, ℕ-typed components, and the length-minimum `#t ≥ 1` underlying `#r ≥ 1` in both conjuncts; grounds the **S** definition.
  - T1 (LexicographicOrder) — defines the ordering relation `≥` used in the `⊖`-precondition and consumed by TA2.
  - TA-Pos (PositiveTumbler) — the precondition `Pos(w)` licenses action-point existence; supplies the **Z** definition referenced in the narrative and in the sub-claim TA7a.3.
  - ActionPoint (ActionPoint) — defines `k = actionPoint(w)` as the least non-zero position of `w` and supplies the minimum-value clause `w_k ≥ 1` used in the Conjunct 1 action-point positivity chain; the prefix-zero characterisation justifies the narrative remark that `k ≥ 2 ⟹ w₁ = 0`.
  - TumblerAdd (TumblerAdd) — three-region componentwise construction of `r = o ⊕ w` used in Conjunct 1 (pre-action copy from `o`, action-point sum `oₖ + wₖ`, tail copy from `w`).
  - TumblerSub (TumblerSub) — zero-padding under NAT-order trichotomy, ZPD-based divergence dispatch, and componentwise formula used in Conjunct 2; the divergence-at-1 branch is the one selected by `o₁ > w₁`.
  - ZPD (ZeroPaddedDivergence) — minimality clause `zpd(a, w) = min {k : 1 ≤ k ≤ L ∧ âₖ ≠ ŵₖ}` fixes `zpd(o, w) = 1` in Conjunct 2 from the position-1 disagreement `o₁ ≠ w₁` (itself supplied by `o₁ > w₁`); this divergence index is the dispatch key consumed by TumblerSub's componentwise formula at the divergence point.
  - TA0 (WellDefinedAddition) — delivers `o ⊕ w ∈ T` and `#(o ⊕ w) = #w` from the `⊕`-preconditions; the S-strengthening in Conjunct 1 rests on this T-closure.
  - TA2 (WellDefinedSubtraction) — delivers `o ⊖ w ∈ T` from the `⊖`-preconditions; the S-strengthening in Conjunct 2 rests on this T-closure.
  - NAT-addcompat (NatAdditionOrderAndSuccessor) — left order-compatibility and strict successor jointly establishing `oₖ + wₖ > oₖ` at the action point of `⊕`.
  - NAT-order (NatStrictTotalOrder) — trichotomy on `(#o, #w)` names `L` in the TumblerSub dispatch; the `≤` defining clause and transitivity of `<` compose the strict-through-addition chain in Conjunct 1.
  - NAT-sub (NatPartialSubtraction) — strict-positivity clause `m > n ⟹ m − n ≥ 1` discharges `r₁ > 0` at the divergence point of Conjunct 2.
  - NAT-closure (NatArithmeticClosureAndIdentity) — supplies `1 ∈ ℕ` for the numerals in quantifier bounds and in `wₖ ≥ 1`; additive identity required in scope for the consumed contracts of TumblerAdd, TumblerSub, TA-Pos, and ActionPoint.
  - NAT-zero (NatZeroMinimum) — supplies `0 ∈ ℕ` for the literal `0` in the **S** positivity clause `oᵢ > 0` and for the zero-padding semantics of TumblerSub consumed in Conjunct 2.
- *Forward References:*
  - TA7a.1 (SubspaceLengthResidue) — handles the complementary length-overflow residue case (`#w > #o`) relocated from TA7a's precondition lattice
  - TA7a.2 (SubspaceDivergenceResidue) — handles the complementary leading-zero residue case (`o₁ = w₁`) relocated from TA7a's precondition lattice
  - TA7a.3 (SubspaceZeroResidue) — handles the complementary self-subtraction residue case (collapse to Z) relocated from TA7a's precondition lattice
- *Postconditions:* `o ⊕ w ∈ S` with `#(o ⊕ w) = #w`; `o ⊖ w ∈ S` with `#(o ⊖ w) = #o`.
- *Frame:* The subspace identifier `N` is not an operand and is never modified.
- *Definition:* **S** = {o ∈ T : #o ≥ 1 ∧ (A i : 1 ≤ i ≤ #o : oᵢ > 0)}.

**TA7a.1 (SubspaceLengthResidue).** When the subtrahend is longer than the minuend, the subspace-closure guarantee of TA7a fails and the residue lies in `T \ S` with trailing zeros beyond the minuend's length.

  `(A o ∈ S, w ∈ T : Pos(w) ∧ o ≥ w ∧ #w > #o ⟹ o ⊖ w ∈ T \ S)`

*Proof.* Let `o ∈ S` and `w ∈ T` with `Pos(w)`, `o ≥ w`, and `#w > #o`. By TA2, `r := o ⊖ w ∈ T`. NAT-order's trichotomy on `(#o, #w)` selects sub-case (β) of TumblerSub: `L = #w > #o`, and the minuend is zero-padded so that `oᵢ = 0` for `#o < i ≤ #w`.

We first show that the zero-padded sequences disagree. If they agreed everywhere, then in particular `oᵢ = wᵢ` for `1 ≤ i ≤ #o`, and for `#o < i ≤ #w`, `wᵢ = oᵢ (padded) = 0`. Then by T3 the pair `(o, w)` satisfies `o ≠ w` via the length clause `#o < #w`, and T1's prefix-relationship case (ii) applied to the agreement `oᵢ = wᵢ` for `i ≤ #o` — `o` a proper prefix of `w` — yields `o < w`, contradicting `o ≥ w`. Hence the zero-padded sequences disagree, `zpd(o, w)` is defined; write `d = zpd(o, w)`.

Next we locate `d` within `o`'s positions. Suppose `d > #o`. Then by ZPD's minimality, the padded sequences agree for `1 ≤ i ≤ #o`, i.e., `oᵢ = wᵢ` there; for `#o < i < d`, padded agreement means `0 = wᵢ`, i.e., `wᵢ = 0`; at `i = d`, disagreement means `0 = o_d (padded) ≠ w_d`, so `w_d ≠ 0`. But then `o` is a proper prefix of `w` — `oᵢ = wᵢ` on `[1, #o]` and `#o < #w` — so T1's prefix case (ii) again yields `o < w`, contradicting `o ≥ w`. Therefore `d ≤ #o`.

By TumblerSub's componentwise formula: `rᵢ = 0` for `i < d`; `r_d = o_d − w_d`; `rᵢ = oᵢ` (zero-padded) for `d < i ≤ L = #w`. At position `#w` (which satisfies `d < #w` since `d ≤ #o < #w`), `r_{#w} = o_{#w}` (padded). Since `#w > #o`, the padding gives `o_{#w} = 0`, so `r_{#w} = 0`. The index `#w = #r` lies in `[1, #r]`, and its component is `0`, violating the universal positivity clause of **S**; hence `r ∉ S`. Combined with `r ∈ T` from TA2, `r ∈ T \ S`. ∎

Example: `[5, 3] ⊖ [5, 3, 4]` — padding `o` to `[5, 3, 0]`, divergence at position 3 (`0 ≠ 4`) is excluded by `o ≥ w`; take instead `[5, 4] ⊖ [5, 3, 4]`, padding to `[5, 4, 0]`, divergence at position 2 (`4 > 3`), giving `r = [0, 1, 0]` (since `r_2 = 4 − 3 = 1`, `r_3 = o_3 (padded) = 0`). `#r = 3`, `r_3 = 0`, so `r ∈ T \ S`.

*Formal Contract:*
- *Preconditions:* `o ∈ S`, `w ∈ T`, `Pos(w)`, `o ≥ w`, `#w > #o`.
- *Depends:*
  - TA7a (SubspaceClosure) — parent claim defining **S** and establishing the complementary in-S branch whose precondition `#w ≤ #o` this sub-claim negates.
  - T0 (CarrierSetDefinition) — carrier `T`, length `#`, ℕ-typed components.
  - T1 (LexicographicOrder) — prefix-relationship case (ii) rules out `d > #o` and also the padded-sequences-agree-everywhere case, both by deriving `o < w` against `o ≥ w`.
  - T3 (CanonicalRepresentation) — length clause `#o ≠ #w ⟹ o ≠ w` supports the disagreement argument.
  - TA-Pos (PositiveTumbler) — `Pos(w)` precondition; **S** complement referenced in the postcondition.
  - TA2 (WellDefinedSubtraction) — delivers `o ⊖ w ∈ T`.
  - TumblerSub (TumblerSub) — zero-padding under NAT-order trichotomy, ZPD-based dispatch, and componentwise formula — in particular `rᵢ = oᵢ` (zero-padded) for `i > d` which places `r_{#w} = 0`.
  - ZPD (ZeroPaddedDivergence) — minimality of `zpd(o, w)`.
  - NAT-order (NatStrictTotalOrder) — trichotomy on `(#o, #w)` selects sub-case (β) with `L = #w`.
  - NAT-zero (NatZeroMinimum) — supplies `0 ∈ ℕ` for the padding positions `#o < i ≤ #w`.
- *Postcondition:* `o ⊖ w ∈ T \ S`, with `r_{#w} = 0` witnessing the escape from **S**.

**TA7a.2 (SubspaceDivergenceResidue).** When the action point is at position 1 and the leading components coincide with a strict disagreement later, the subspace-closure guarantee of TA7a fails and the residue acquires a leading zero, placing it in `T \ S`.

  `(A o ∈ S, w ∈ T : Pos(w) ∧ o ≥ w ∧ #w ≤ #o ∧ actionPoint(w) = 1 ∧ o₁ = w₁ ∧ o ≠ w ⟹ o ⊖ w ∈ T \ S)`

*Proof.* Let `o ∈ S`, `w ∈ T` with `Pos(w)`, `o ≥ w`, `#w ≤ #o`, `k := actionPoint(w) = 1`, `o₁ = w₁`, and `o ≠ w`. By TA2, `r := o ⊖ w ∈ T`. NAT-order's trichotomy on `(#o, #w)` with `#w ≤ #o` selects sub-case (α) `#o = #w` with `L = #o` or sub-case (γ) `#w < #o` with `L = #o`; in either `L = #o`.

We establish that `zpd(o, w)` is defined by case-splitting on the trichotomy outcome. The bare disagreement `o ≠ w` does not suffice — ZPD's partiality clause is explicit that `o ≠ w` is compatible with `zpd(o, w)` undefined (the documented counterexample `[3, 0]` versus `[3]`). The argument must consume the sub-case structure that the trichotomy already supplied.

*Sub-case (α)* (`#o = #w`, `L = #o`). When the lengths agree there is no padding to traverse: ZPD's defining clauses give `ôᵢ = oᵢ` for `1 ≤ i ≤ #o` and `ŵᵢ = wᵢ` for `1 ≤ i ≤ #w = #o`, so on `[1, L]` the padded projections coincide with the native sequences. Suppose for contradiction that `zpd(o, w)` is undefined; ZPD's partiality clause then forces `(A i : 1 ≤ i ≤ L : ôᵢ = ŵᵢ)`, i.e. `(A i : 1 ≤ i ≤ #o : oᵢ = wᵢ)`. Conjoined with `#o = #w`, T3's forward direction at `(o, w)` yields `o = w`, contradicting the precondition `o ≠ w`. Hence `zpd(o, w)` is defined.

*Sub-case (γ)* (`#w < #o`, `L = #o`). Here the strict inequality leaves at least one position past `#w` within `[1, L]`; pick `i := #o`, which satisfies `#w < i ≤ L = #o`. ZPD's padding clause for `ŵ` gives `ŵᵢ = 0` (the position is past `#w`), and ZPD's native clause for `ô` gives `ôᵢ = oᵢ` (the position is within `#o`). Since `o ∈ S`, the universal positivity clause from **S**'s definition delivers `oᵢ > 0`, so `ôᵢ = oᵢ > 0 = ŵᵢ` and `ôᵢ ≠ ŵᵢ`. The disagreement at this index forecloses ZPD's universal-agreement antecedent, so `zpd(o, w)` is defined.

In either sub-case `zpd(o, w)` is defined; write `d = zpd(o, w)`. The padded projections agree at position 1 — `ô₁ = o₁ = w₁ = ŵ₁` — so the disagreement cannot be at position 1, and by ZPD's minimality `d > 1`. By TumblerSub's componentwise formula, `rᵢ = 0` for `1 ≤ i < d`. In particular `r₁ = 0`.

The index `1` lies in `[1, #r]` (since `#r = L = #o ≥ 1` by T0), and `r₁ = 0` violates the universal positivity clause of **S**; hence `r ∉ S`. Combined with `r ∈ T` from TA2, `r ∈ T \ S`. ∎

Example: `[5, 3] ⊖ [5, 1] = [0, 2]` — `k = 1`, `o₁ = w₁ = 5`, divergence at `d = 2` (`3 ≠ 1`), giving `r₁ = 0` (pre-divergence zero), `r₂ = 3 − 1 = 2` (divergence point). `r = [0, 2] ∈ T \ S`, consistent with the predicted residue.

*Formal Contract:*
- *Preconditions:* `o ∈ S`, `w ∈ T`, `Pos(w)`, `o ≥ w`, `#w ≤ #o`, `actionPoint(w) = 1`, `o₁ = w₁`, `o ≠ w`.
- *Depends:*
  - TA7a (SubspaceClosure) — parent claim defining **S** and establishing the complementary in-S branch whose precondition `o₁ > w₁` this sub-claim negates under `o ≠ w`.
  - T0 (CarrierSetDefinition) — carrier `T`, length `#`, `#r ≥ 1`.
  - TA-Pos (PositiveTumbler) — `Pos(w)` precondition; **S** definition whose universal positivity clause is violated at index 1.
  - ActionPoint (ActionPoint) — defines `k = actionPoint(w)`; the precondition `k = 1` is consumed only to characterise the scenario, not inside the proof (the divergence location `d > 1` follows from `o₁ = w₁ ∧ o ≠ w` without invoking `k`).
  - TA2 (WellDefinedSubtraction) — delivers `o ⊖ w ∈ T`.
  - T3 (CanonicalRepresentation) — forward direction `(#a = #b ∧ (A i : 1 ≤ i ≤ #a : aᵢ = bᵢ)) ⟹ a = b` instantiated at `(o, w)` in sub-case (α): the contradiction `o = w` against the precondition `o ≠ w` is what forces `zpd(o, w)` defined when the lengths agree.
  - TumblerSub (TumblerSub) — zero-padding under NAT-order trichotomy, ZPD-based dispatch, and the pre-divergence-zero clause `rᵢ = 0` for `i < d` which places `r₁ = 0`.
  - ZPD (ZeroPaddedDivergence) — partiality clause used both ways: in sub-case (α), the universal-agreement antecedent contradicts T3 plus `o ≠ w`; in sub-case (γ), the padding clause `ŵᵢ = 0` for `#w < i ≤ L` against `ôᵢ = oᵢ > 0` (from `o ∈ S`) breaks universal agreement at `i = #o`. Together these establish `zpd(o, w)` defined; minimality then places `d > 1` given agreement at position 1.
  - NAT-order (NatStrictTotalOrder) — trichotomy on `(#o, #w)` with `#w ≤ #o` places `L = #o`.
  - NAT-zero (NatZeroMinimum) — supplies `0 ∈ ℕ` for `r₁ = 0`.
- *Postcondition:* `o ⊖ w ∈ T \ S`, with `r₁ = 0` witnessing the escape from **S**.

**TA7a.3 (SubspaceZeroResidue).** When the minuend and subtrahend coincide, subtraction collapses the residue to the zero tumbler: `o ⊖ o ∈ Z`.

  `(A o ∈ S : o ⊖ o ∈ Z)`

*Proof.* Let `o ∈ S`. Then `o ∈ T` and `o ≥ o` by the reflexivity of T1's ordering, so TA2 gives `r := o ⊖ o ∈ T`. NAT-order's trichotomy on `(#o, #o)` selects sub-case (α) `#o = #o` with `L = #o`; no zero-padding is required.

The zero-padded sequences of `o` and `o` agree at every position; hence `zpd(o, o)` is undefined and TumblerSub's no-divergence branch produces the zero tumbler `[0, ..., 0]` of length `L = #o`. Every component of `r` equals `0 ∈ ℕ` (NAT-zero), so the universal clause of TA-Pos's `Zero` predicate, `(A i : 1 ≤ i ≤ #r : rᵢ = 0)`, is satisfied. Therefore `Zero(r)` holds, placing `r ∈ Z` by TA-Pos's **Z** definition.

As a sentinel, `r` is not a valid address (TA6) and serves as a lower bound relative to every positive tumbler (TA-PosDom); its appearance as the self-subtraction residue marks the "no-displacement" fixed point of `⊖`. ∎

Example: `[1, 2] ⊖ [1, 2] = [0, 0] ∈ Z`.

*Formal Contract:*
- *Preconditions:* `o ∈ S`.
- *Depends:*
  - TA7a (SubspaceClosure) — parent claim defining **S** and establishing the complementary in-S branch whose precondition `o₁ > w₁` this sub-claim negates via `o = w` (which forces `o₁ = w₁`).
  - T0 (CarrierSetDefinition) — carrier `T` and length `#`.
  - T1 (LexicographicOrder) — reflexivity of `≥` delivering `o ≥ o`.
  - TA-Pos (PositiveTumbler) — `Zero` predicate and **Z** definition.
  - TA2 (WellDefinedSubtraction) — delivers `o ⊖ o ∈ T`.
  - TumblerSub (TumblerSub) — no-divergence branch producing the zero tumbler of length `L`.
  - TA6 (ZeroTumblers) — invalidity of zero tumblers as addresses.
  - TA-PosDom (PositiveDominatesZero) — lower-bound status of the zero-tumbler residue relative to every positive tumbler.
  - NAT-order (NatStrictTotalOrder) — trichotomy on `(#o, #o)` names `L = #o`.
  - NAT-zero (NatZeroMinimum) — supplies `0 ∈ ℕ` for every component of the zero tumbler.
- *Postcondition:* `o ⊖ o ∈ Z`, with every component zero.


---

## 10. Spans

A *span* is a contiguous range of tumbler addresses, identified by a pair of endpoints or by a single anchor and a displacement. T12 establishes that span computation is well-defined and respects subspace structure.

### Spans

By **Definition (Span)**, a span denotes a contiguous range of tumblers from a start address up to but not including the displaced endpoint. The form of `ℓ` depends on the hierarchical level at which the span operates, because the action point of `ℓ` must match the level of the start address `s`.

Nelson makes spans self-describing at every hierarchical level: "A digit of 'one' may be used to designate all of a given version, all versions of a given document, all works of a given author, all documents in a given project, all documents on a given server — or the entire docuverse." The "1-position convention" exploits T5: because subtrees are contiguous, a span whose start is a high-level prefix and whose length reaches to the next sibling captures exactly that subtree's content.

A span's *content* may be empty — the range populated by nothing at present — yet the span itself remains a valid address-set: "A span that contains nothing today may at a later time contain a million documents." Throughout this document, *span* denotes the address-set `span(s, ℓ) = {t ∈ T : s ≤ t < s ⊕ ℓ}` fixed by Definition (Span), and *a span's content* denotes the documents populating that range at a given moment.

**T12 (SpanWellDefinedness).** For any `(s, ℓ)` satisfying the preconditions of Definition (Span), the set `span(s, ℓ)` has three properties: its upper bound `s ⊕ ℓ` exists in `T`, the set is non-empty (with `s` always a member), and it is order-convex under T1.

*Proof.* Let `(s, ℓ)` satisfy the preconditions of Definition (Span): `s ∈ T`, `ℓ ∈ T`, `Pos(ℓ)`, and the action point `k` of `ℓ` satisfies `k ≤ #s`. Write `S = span(s, ℓ) = {t ∈ T : s ≤ t < s ⊕ ℓ}`.

*(a) Endpoint existence.* The preconditions supply `s ∈ T`, `ℓ ∈ T`, `Pos(ℓ)`, and `k ≤ #s` — precisely the four preconditions of TA0 under `(a, w) := (s, ℓ)` — so TA0 gives `s ⊕ ℓ ∈ T`. The set `S` is well-defined.

*(b) Non-emptiness.* We show `s ∈ S`. First, `s ≤ s` by reflexivity of `≤` (from T1: `a ≤ b` iff `a < b ∨ a = b`). Second, the same preconditions match TA-strict under `(a, w) := (s, ℓ)`, so `s ⊕ ℓ > s`, i.e., `s < s ⊕ ℓ`. Both conditions hold, so `s ∈ S`.

*(c) Contiguity.* We show `S` is order-convex: for `a, c ∈ S` and `b ∈ T` with `a ≤ b ≤ c`, we have `b ∈ S`. By T1, `<` is a strict total order on `T` with transitivity from T1(c). Transitivity of `≤` follows by case analysis on `< ∨ =`: the (<,<) case composes via T1(c); the (<,=) and (=,<) cases substitute equality; the (=,=) case chains equalities.

From `a ∈ S`, `s ≤ a`; with `a ≤ b`, transitivity of `≤` gives `s ≤ b`.

From `c ∈ S`, `c < s ⊕ ℓ`. If `b = c`, then `b < s ⊕ ℓ` immediately; if `b < c`, then T1(c) with `c < s ⊕ ℓ` gives `b < s ⊕ ℓ`.

Together, `s ≤ b` and `b < s ⊕ ℓ`, so `b ∈ S`. ∎

We reserve T5 for the distinct claim that *prefix-defined* sets are contiguous — a non-trivial property of the lexicographic order.

*Formal Contract:*
- *Preconditions:* `(s, ℓ)` satisfies the preconditions of Definition (Span) — equivalently, `s ∈ T`, `ℓ ∈ T`, `Pos(ℓ)`, and `actionPoint(ℓ) ≤ #s`.
- *Depends:*
  - Span (Span) — fixes the symbol `span(s, ℓ) = {t ∈ T : s ≤ t < s ⊕ ℓ}` and the preconditions on `(s, ℓ)`.
  - T0 (CarrierSetDefinition) — supplies the carrier `T` and length operator `#`.
  - T1 (LexicographicOrder) — supplies reflexivity of `≤`, transitivity of `<` via T1(c), and the `< ∨ =` decomposition.
  - TA0 (WellDefinedAddition) — supplies `s ⊕ ℓ ∈ T` from the four preconditions.
  - TA-strict (StrictIncrease) — supplies `s ⊕ ℓ > s` from the four preconditions.
- *Forward References:*
  - T5 (PrefixContiguity) — named as the downstream claim establishing contiguity for prefix-defined sets, a distinct property deferred from T12
- *Postconditions:* (a) `s ⊕ ℓ ∈ T`. (b) `s ∈ span(s, ℓ)`. (c) `span(s, ℓ)` is order-convex under T1: for all `a, c ∈ span(s, ℓ)` and `b ∈ T`, `a ≤ b ≤ c` implies `b ∈ span(s, ℓ)`.

**Span (Span).** A *span* is the address-set `span(s, ℓ) = {t ∈ T : s ≤ t < s ⊕ ℓ}` determined by a pair `(s, ℓ)` where `s ∈ T` is a start address and `ℓ ∈ T` is a length — a positive tumbler used as a displacement whose action point satisfies `actionPoint(ℓ) ≤ #s`.

*Formal Contract:*
- *Preconditions:* `s ∈ T`, `ℓ ∈ T`, `Pos(ℓ)`, `actionPoint(ℓ) ≤ #s`
- *Definition:* `span(s, ℓ) = {t ∈ T : s ≤ t < s ⊕ ℓ}`
- *Depends:*
  - T0 (CarrierSetDefinition) — supplies the carrier `T` and length operator `#`.
  - TA-Pos (PositiveTumbler) — supplies the positivity predicate `Pos(·)`.
  - ActionPoint (ActionPoint) — supplies the action-point function `actionPoint(·)`.
  - TumblerAdd (TumblerAdd) — supplies the operator `⊕`.
  - TA0 (WellDefinedAddition) — licenses `s ⊕ ℓ ∈ T` under the four preconditions via the instantiation `(a, w) := (s, ℓ)`.
  - T1 (LexicographicOrder) — supplies the strict order `<` and the non-strict `≤` bracketing the defining set.


---

## 11. Shifts

A *shift* translates a tumbler by a fixed displacement, preserving order (TS1) and structural identity (TS2). Shifts compose (TS3), increase strictly under positive amounts (TS4), and the shift amount itself is monotone (TS5). OrdinalShift names the operator.

**TS1 (ShiftOrderPreservation).**

`(A v₁, v₂ ∈ T, n ∈ ℕ : n ≥ 1 ∧ #v₁ = #v₂ ∧ v₁ < v₂ : shift(v₁, n) < shift(v₂, n))`

*Proof.* Fix v₁, v₂ ∈ T with #v₁ = #v₂, v₁ < v₂, and n ≥ 1, and let m abbreviate #v₁. By OrdinalShift, shift(v₁, n) = v₁ ⊕ δ(n, m) and shift(v₂, n) = v₂ ⊕ δ(n, m), so it suffices to show v₁ ⊕ δ(n, m) < v₂ ⊕ δ(n, m). We discharge TA1-strict's eight preconditions with a = v₁, b = v₂, w = δ(n, m):

(i) v₁ ∈ T — hypothesis.

(ii) v₂ ∈ T — hypothesis.

(iii) δ(n, m) ∈ T — OrdinalDisplacement postcondition.

(iv) v₁ < v₂ — hypothesis.

(v) Pos(δ(n, m)) — OrdinalDisplacement postcondition.

(vi) actionPoint(δ(n, m)) ≤ #v₁ — actionPoint(δ(n, m)) = m (OrdinalDisplacement) and #v₁ = m, so m ≤ m.

(vii) actionPoint(δ(n, m)) ≤ #v₂ — similarly, #v₂ = m by hypothesis #v₁ = #v₂, so m ≤ m.

(viii) actionPoint(δ(n, m)) ≥ divergence(v₁, v₂) — from v₁ < v₂, T1 irreflexivity gives v₁ ≠ v₂. Since #v₁ = #v₂, Divergence case (ii) is excluded and case (i) applies, supplying k with 1 ≤ k ≤ #v₁, k ≤ #v₂, (v₁)ₖ ≠ (v₂)ₖ, and prior-position agreement, with divergence(v₁, v₂) = k. Then divergence(v₁, v₂) = k ≤ #v₁ = m.

By TA1-strict: v₁ ⊕ δ(n, m) < v₂ ⊕ δ(n, m), that is, shift(v₁, n) < shift(v₂, n). ∎

*Formal Contract:*
- *Preconditions:* v₁ ∈ T, v₂ ∈ T, n ∈ ℕ, n ≥ 1, #v₁ = #v₂, v₁ < v₂
- *Depends:*
  - OrdinalShift (OrdinalShift) — unfolds shift(v, n) = v ⊕ δ(n, #v).
  - OrdinalDisplacement (OrdinalDisplacement) — supplies δ(n, m) ∈ T, Pos(δ(n, m)), and actionPoint(δ(n, m)) = m.
  - Divergence (Divergence) — case (i) supplies the index k with 1 ≤ k ≤ #v₁, k ≤ #v₂, and divergence(v₁, v₂) = k; case (ii) is excluded by #v₁ = #v₂.
  - T3 (CanonicalRepresentation) — underwrites Divergence's exhaustiveness (used to rule out the residual configuration at the case-(ii)-exclusion step).
  - TA1-strict (StrictOrderPreservation) — load-bearing lemma: a < b with the eight preconditions yields a ⊕ w < b ⊕ w.
  - T0 (CarrierSetDefinition) — carrier T, length operator #·, component projection ·ᵢ.
  - T1 (LexicographicOrder) — the relation < on T, and irreflexivity used to derive v₁ ≠ v₂ from v₁ < v₂.
  - TA-Pos (PositiveTumbler) — definition of Pos(·).
  - ActionPoint (ActionPoint) — definition of actionPoint(·).
  - NAT-order (NatStrictTotalOrder) — ≤ on ℕ used in the length-bound and divergence-bound comparisons.
  - NAT-wellorder (NatWellOrdering) — least-element principle underwriting Divergence case (i)'s well-defined index k.
- *Postconditions:* shift(v₁, n) < shift(v₂, n)

**TS2 (ShiftInjectivity).**

`(A v₁, v₂ ∈ T, n ∈ ℕ : n ≥ 1 ∧ #v₁ = #v₂ : shift(v₁, n) = shift(v₂, n) ⟹ v₁ = v₂)`

*Proof.* Fix v₁, v₂ ∈ T with #v₁ = #v₂, and fix n ≥ 1. Let m = #v₁ = #v₂. Assume shift(v₁, n) = shift(v₂, n). By T0, m ≥ 1.

Applying OrdinalShift at v = v₁ and at v = v₂ (preconditions `v ∈ T, n ∈ ℕ, n ≥ 1` transfer from hypothesis), the assumption rewrites as

v₁ ⊕ δ(n, m) = v₂ ⊕ δ(n, m).

Applying OrdinalDisplacement at (n, m): `n ∈ ℕ` and `n ≥ 1` transfer from hypothesis; `m ∈ ℕ` and `m ≥ 1` from T0's length typing and length axiom at v₁ ∈ T. Its postconditions give `δ(n, m) ∈ T`, `Pos(δ(n, m))`, and `actionPoint(δ(n, m)) = m`.

Apply TA-MTO with w = δ(n, m), a = v₁, b = v₂. Verifying its six preconditions:

(i) δ(n, m) ∈ T — OrdinalDisplacement.

(ii) Pos(δ(n, m)) — OrdinalDisplacement.

(iii) v₁ ∈ T — hypothesis.

(iv) v₂ ∈ T — hypothesis.

(v) #v₁ ≥ actionPoint(δ(n, m)) — reduces to m ≥ m via `actionPoint(δ(n, m)) = m` and `#v₁ = m`.

(vi) #v₂ ≥ actionPoint(δ(n, m)) — reduces to m ≥ m via `actionPoint(δ(n, m)) = m` and `#v₂ = m`.

TA-MTO's converse yields v₁ᵢ = v₂ᵢ for all 1 ≤ i ≤ m. Since #v₁ = #v₂ = m and all m components agree, T3 gives v₁ = v₂. ∎

*Formal Contract:*
- *Preconditions:* v₁ ∈ T, v₂ ∈ T, n ∈ ℕ, n ≥ 1, #v₁ = #v₂
- *Depends:*
  - T0 (CarrierSetDefinition) — length typing `#·: T → ℕ` and length axiom `#a ≥ 1 for a ∈ T`.
  - OrdinalShift (OrdinalShift) — rewrites `shift(v, n) = v ⊕ δ(n, m)`.
  - OrdinalDisplacement (OrdinalDisplacement) — exports `δ(n, m) ∈ T`, `Pos(δ(n, m))`, `actionPoint(δ(n, m)) = m`.
  - TA-Pos (PositiveTumbler) — defines the predicate `Pos(·)`.
  - ActionPoint (ActionPoint) — defines the operator `actionPoint(·)`.
  - TA-MTO (ManyToOne) — load-bearing lemma; converse yields component-wise agreement.
  - T3 (CanonicalRepresentation) — component-wise plus length agreement implies equality.
- *Postconditions:* shift(v₁, n) = shift(v₂, n) ⟹ v₁ = v₂

**TS3 (ShiftComposition).**

`(A v, n₁, n₂, m : v ∈ T ∧ n₁ ∈ ℕ ∧ n₂ ∈ ℕ ∧ n₁ ≥ 1 ∧ n₂ ≥ 1 ∧ #v = m : shift(shift(v, n₁), n₂) = shift(v, n₁ + n₂))`

The binder's `#v = m` fixes `m` as the length of `v`; with `v ∈ T`, T0 gives `m ∈ ℕ` and `m ≥ 1`.

*Proof.* Fix `v ∈ T`, `n₁, n₂ ∈ ℕ` with `n₁, n₂ ≥ 1`, and let `m = #v`.

**Left side.** By OrdinalShift, `shift(v, n₁) = v ⊕ δ(n₁, m)` with `actionPoint(δ(n₁, m)) = m ≤ m = #v`. Let `u = v ⊕ δ(n₁, m)`. By TumblerAdd with `k = m`:

- For `1 ≤ i < m`: `uᵢ = vᵢ`.
- At `i = m`: `uₘ = vₘ + n₁`.
- `#u = #δ(n₁, m) = m` by TA0's length postcondition.

By TA0's carrier postcondition, `u ∈ T`. By OrdinalShift, `shift(u, n₂) = u ⊕ δ(n₂, m)` with `actionPoint(δ(n₂, m)) = m ≤ m = #u`. Let `L = u ⊕ δ(n₂, m)`. By TumblerAdd with `k = m`:

- For `1 ≤ i < m`: `Lᵢ = uᵢ = vᵢ`.
- At `i = m`: `Lₘ = uₘ + n₂ = (vₘ + n₁) + n₂`.
- `#L = m`.

**Right side.** By NAT-closure, `n₁ + n₂ ∈ ℕ`. We derive `n₁ + n₂ ≥ 1` via the chain `n₁ + n₂ ≥ 1 + n₂ ≥ 1 + 1 ≥ 1`: the first step applies NAT-addcompat right order-compatibility to `1 ≤ n₁`; the second applies NAT-addcompat left order-compatibility to `1 ≤ n₂`; the third unfolds NAT-addcompat's strict successor inequality `1 < 1 + 1` through NAT-order's defining clause `m ≤ n ⟺ m < n ∨ m = n`. By OrdinalShift, `shift(v, n₁ + n₂) = v ⊕ δ(n₁ + n₂, m)` with `actionPoint(δ(n₁ + n₂, m)) = m ≤ m = #v`. Let `R = v ⊕ δ(n₁ + n₂, m)`. By TumblerAdd with `k = m`:

- For `1 ≤ i < m`: `Rᵢ = vᵢ`.
- At `i = m`: `Rₘ = vₘ + (n₁ + n₂)`.
- `#R = m`.

**Comparison.** `#L = m = #R`. For `1 ≤ i < m`: `Lᵢ = vᵢ = Rᵢ`. At `i = m`: by T0, `vₘ ∈ ℕ`; by NAT-addassoc at `(vₘ, n₁, n₂)`, `(vₘ + n₁) + n₂ = vₘ + (n₁ + n₂)`, so `Lₘ = Rₘ`. By T3, `L = R`. ∎

*Formal Contract:*
- *Preconditions:* v ∈ T, n₁ ∈ ℕ, n₂ ∈ ℕ, n₁ ≥ 1, n₂ ≥ 1, #v = m
- *Depends:*
  - OrdinalShift (OrdinalShift) — unfolds `shift(·, n) = · ⊕ δ(n, m)` at each of three shift sites.
  - OrdinalDisplacement (OrdinalDisplacement) — fixes `δ(n, m) = [0, ..., 0, n]` with `actionPoint = m`, and exports `Pos(δ(n, m))` and `δ(n, m) ∈ T`.
  - T0 (CarrierSetDefinition) — length operator typing `#·: T → ℕ` and length axiom `#a ≥ 1` supply `m ∈ ℕ` and `m ≥ 1`; carrier characterisation places `vₘ ∈ ℕ`.
  - TA-Pos (PositiveTumbler) — defines `Pos(·)` consumed at TA0's third precondition.
  - ActionPoint (ActionPoint) — defines `actionPoint(·)` consumed at TA0's fourth precondition.
  - NAT-closure (NatArithmeticClosureAndIdentity) — addition-closure supplies `n₁ + n₂ ∈ ℕ`.
  - NAT-addcompat (NatAdditionOrderAndSuccessor) — left/right order compatibility and strict successor inequality supply the chain `n₁ + n₂ ≥ 1 + n₂ ≥ 1 + 1 ≥ 1`.
  - NAT-order (NatStrictTotalOrder) — defining clause `m ≤ n ⟺ m < n ∨ m = n` and transitivity of `<` compose the chain into `n₁ + n₂ ≥ 1`.
  - TA0 (WellDefinedAddition) — discharges each `⊕`'s action-point precondition, supplies result-length `#(a ⊕ w) = #w`, and supplies `u ∈ T` for the second shift.
  - TumblerAdd (TumblerAdd) — three-region rule producing `uᵢ`, `Lᵢ`, `Rᵢ`.
  - NAT-addassoc (NatAdditionAssociative) — `(vₘ + n₁) + n₂ = vₘ + (n₁ + n₂)` at the comparison step.
  - T3 (CanonicalRepresentation) — component-wise and length agreement implies tumbler equality.
- *Postconditions:* shift(shift(v, n₁), n₂) = shift(v, n₁ + n₂)
- *Frame:* #shift(shift(v, n₁), n₂) = #v = m

**TS4 (ShiftStrictIncrease).**

`(A v, n, m : v ∈ T ∧ n ∈ ℕ ∧ n ≥ 1 ∧ #v = m : shift(v, n) > v)`

The dummy `m` abbreviates `#v`: the range predicate `#v = m` binds `m` as the length of `v`, with `m ∈ ℕ` from T0's length typing `#·: T → ℕ` and `m ≥ 1` from T0's length axiom.

*Proof.* Fix v ∈ T, n ∈ ℕ with n ≥ 1, and let m = #v. By OrdinalShift, shift(v, n) = v ⊕ δ(n, m); we must show v ⊕ δ(n, m) > v.

Apply TA-strict with a = v and w = δ(n, m). Four preconditions:

*First: v ∈ T.* Directly from TS4's own precondition, under the identity substitution a ↦ v.

*Second: δ(n, m) ∈ T.* From OrdinalDisplacement's exported postcondition `δ(n, m) ∈ T`, under the substitution w ↦ δ(n, m).

*Third: Pos(δ(n, m)).* From OrdinalDisplacement's exported postcondition `Pos(δ(n, m))`.

*Fourth: actionPoint(δ(n, m)) ≤ #v.* From OrdinalDisplacement's exported postcondition `actionPoint(δ(n, m)) = m`. Since #v = m, we have m ≤ m.

By TA-strict: v ⊕ δ(n, m) > v, that is, shift(v, n) > v. ∎

*Formal Contract:*
- *Preconditions:* v ∈ T, n ∈ ℕ, n ≥ 1, #v = m
- *Depends:*
  - OrdinalShift (OrdinalShift) — unfolds `shift(v, n) = v ⊕ δ(n, m)`. Preconditions `v ∈ T`, `n ∈ ℕ`, `n ≥ 1` discharged from TS4's own preconditions under identity substitution.
  - OrdinalDisplacement (OrdinalDisplacement) — supplies exported postconditions `δ(n, m) ∈ T`, `Pos(δ(n, m))`, and `actionPoint(δ(n, m)) = m` at TA-strict's membership, positivity, and action-point precondition checks respectively.
  - TA-strict (StrictIncrease) — the load-bearing lemma: converts `Pos(w)` and `actionPoint(w) ≤ #a` into `a ⊕ w > a`.
  - T0 (CarrierSetDefinition) — length operator typing `#·: T → ℕ` supplies `m ∈ ℕ`; length axiom `#a ≥ 1 for all a ∈ T` supplies `m ≥ 1`. Both feed OrdinalDisplacement's `m ∈ ℕ` and `m ≥ 1` preconditions.
  - TA-Pos (PositiveTumbler) — defines the predicate `Pos(t) ⟺ (E i : 1 ≤ i ≤ #t : tᵢ ≠ 0)` consumed at TA-strict's first precondition.
  - ActionPoint (ActionPoint) — defines `actionPoint(w) = min({i : 1 ≤ i ≤ #w ∧ wᵢ ≠ 0})` consumed at TA-strict's second precondition.
- *Postconditions:* shift(v, n) > v

**TS5 (ShiftAmountMonotonicity).**

`(A v, n₁, n₂, m : v ∈ T ∧ n₁ ∈ ℕ ∧ n₂ ∈ ℕ ∧ n₁ ≥ 1 ∧ n₂ > n₁ ∧ #v = m : shift(v, n₁) < shift(v, n₂))`

Shifting a tumbler by a larger amount produces a strictly greater result.

*Proof.* Fix v ∈ T with m = #v, and n₁, n₂ ∈ ℕ with n₁ ≥ 1 and n₂ > n₁.

Define d = n₂ − n₁. By NAT-sub's conditional closure at `m = n₂, n = n₁` (using n₂ ≥ n₁ via NAT-order from n₂ > n₁), d ∈ ℕ. By NAT-sub's strict positivity at the same instantiation, d ≥ 1. By NAT-sub's left-inverse characterisation, n₁ + d = n₂.

Invoke TS3 (ShiftComposition) at u = v, a = n₁, b = d: shift(shift(v, n₁), d) = shift(v, n₁ + d) = shift(v, n₂).

Let u = shift(v, n₁). By OrdinalShift at v, n₁: u ∈ T and #u = m. Invoke TS4 (ShiftStrictIncrease) at u, n = d: shift(u, d) > u.

Substituting: shift(v, n₂) = shift(u, d) > u = shift(v, n₁), that is, shift(v, n₂) > shift(v, n₁). T1 (LexicographicOrder) defines the strict total order `<` on T, and the companion relation `>` on T abbreviates the converse — `a > b ⟺ b < a` — so the conclusion rewrites to shift(v, n₁) < shift(v, n₂). ∎

*Worked example.* Let v = [2, 3, 7] (m = 3), n₁ = 4, n₂ = 7. Then shift(v, 4) = [2, 3, 11] and shift(v, 7) = [2, 3, 14]. By T1's lexicographic ordering, [2, 3, 11] < [2, 3, 14]. ✓

*Formal Contract:*
- *Preconditions:* v ∈ T, n₁ ∈ ℕ, n₂ ∈ ℕ, n₁ ≥ 1, n₂ > n₁, #v = m
- *Depends:*
  - TS3 (ShiftComposition) — rewrites shift(v, n₂) as shift(shift(v, n₁), d).
  - TS4 (ShiftStrictIncrease) — yields shift(u, d) > u for u = shift(v, n₁).
  - OrdinalShift — supplies u ∈ T and #u = m for u = shift(v, n₁).
  - NAT-sub (NatPartialSubtraction) — conditional closure, strict positivity, and left-inverse characterisation applied to d = n₂ − n₁.
  - NAT-order (NatStrictTotalOrder) — converts n₂ > n₁ to n₂ ≥ n₁ for NAT-sub's weak-order preconditions.
  - T0 (CarrierSetDefinition) — length operator typing #·: T → ℕ and length axiom #a ≥ 1, licensing m = #v ∈ ℕ with m ≥ 1.
  - T1 (LexicographicOrder) — establishes the strict total order `<` on T and grounds the companion relation `>` as its converse (`a > b ⟺ b < a`), licensing the rewrite from `shift(v, n₂) > shift(v, n₁)` to `shift(v, n₁) < shift(v, n₂)` at the proof's conclusion and the comparison `[2, 3, 11] < [2, 3, 14]` in the worked example.
- *Postconditions:* shift(v, n₁) < shift(v, n₂)

**OrdinalShift (OrdinalShift).** For a tumbler v ∈ T of length m = #v and natural number n ≥ 1:

`shift(v, n) = v ⊕ δ(n, m) where m = #v`

*Derivation.* Discharge TA0's four preconditions. (i) v ∈ T by assumption. (ii) δ(n, m) ∈ T by OrdinalDisplacement's postcondition. (iii) Pos(δ(n, m)) by OrdinalDisplacement's postcondition. (iv) actionPoint(δ(n, m)) = m = #v by OrdinalDisplacement's postcondition, so actionPoint(δ(n, m)) ≤ #v.

OrdinalDisplacement's own preconditions discharge as: n ∈ ℕ and n ≥ 1 transfer from OrdinalShift's preconditions, with NAT-carrier supplying `ℕ` as the underlying set in which the membership `n ∈ ℕ` is asserted; m ∈ ℕ from T0's length typing `#·: T → ℕ` at v ∈ T, the codomain `ℕ` again grounded by NAT-carrier; m ≥ 1 from T0's length axiom `#a ≥ 1` at a = v.

By TA0, shift(v, n) = v ⊕ δ(n, m) ∈ T. By TumblerAdd: shift(v, n)ᵢ = vᵢ for i < m, and shift(v, n)ₘ = vₘ + n. TA0's postcondition `#(a ⊕ w) = #w` yields `#shift(v, n) = #δ(n, m)`; OrdinalDisplacement's `#δ(n, m) = m` and the binding m = #v complete `#shift(v, n) = #v`.

Component lower bound `shift(v, n)ₘ = vₘ + n ≥ 1`. T0 places vₘ ∈ ℕ. NAT-zero gives `0 ≤ vₘ`. NAT-addcompat right order-compatibility lifts to `vₘ + n ≥ 0 + n`. NAT-closure's additive identity rewrites to `vₘ + n ≥ n`. NAT-order composes `vₘ + n ≥ n` with precondition `n ≥ 1` into `vₘ + n ≥ 1` via its defining clause and transitivity of `<`. ∎

*Formal Contract:*
- *Preconditions:* v ∈ T, n ∈ ℕ, n ≥ 1
- *Definition:* shift(v, n) = v ⊕ δ(n, m) where m = #v
- *Depends:*
  - OrdinalDisplacement (OrdinalDisplacement) — constructs δ(n, m); supplies postconditions `δ(n, m) ∈ T`, `Pos(δ(n, m))`, `actionPoint(δ(n, m)) = m`, `#δ(n, m) = m`.
  - T0 (CarrierSetDefinition) — length operator typing `#·: T → ℕ` and length axiom `#a ≥ 1`; carrier characterisation places vₘ ∈ ℕ.
  - NAT-carrier (NatCarrierSet) — supplies `ℕ` as the underlying set for the Precondition membership clause `n ∈ ℕ`, and as the codomain of T0's length operator `#·: T → ℕ` instantiated at v to type m = #v ∈ ℕ — the depth argument passed to OrdinalDisplacement.
  - TA-Pos (PositiveTumbler) — defines the predicate `Pos(·)` consumed at TA0 precondition (iii).
  - ActionPoint (ActionPoint) — defines `actionPoint(·)` consumed at TA0 precondition (iv).
  - TA0 (WellDefinedAddition) — postconditions `a ⊕ w ∈ T` and `#(a ⊕ w) = #w`.
  - TumblerAdd (TumblerAdd) — piecewise component rule: prefix copy for i < m, advance `vₘ + n` at position m.
  - NAT-zero (NatZeroMinimum) — `(∀ n ∈ ℕ :: 0 ≤ n)` supplies `0 ≤ vₘ`.
  - NAT-addcompat (NatAdditionOrderAndSuccessor) — right order-compatibility lifts `0 ≤ vₘ` to `vₘ + n ≥ 0 + n`.
  - NAT-closure (NatArithmeticClosureAndIdentity) — additive identity `0 + n = n`.
  - NAT-order (NatStrictTotalOrder) — defining clause `m ≤ n ⟺ m < n ∨ m = n` and transitivity of `<` compose `vₘ + n ≥ n` with `n ≥ 1` into `vₘ + n ≥ 1`.
- *Postconditions:* shift(v, n) ∈ T, #shift(v, n) = #v, shift(v, n)ᵢ = vᵢ for i < #v, shift(v, n)_{#v} = v_{#v} + n ≥ 1


---

## 12. Displacements

A *displacement* records the gap between two tumblers, suitable for transporting a position across a chain of allocations. D0, D1, D2 establish well-definedness, round-trip identity, and uniqueness. OrdinalDisplacement names the operator.

### Displacement identities

Given two positions a and b on the tumbler line, we establish when b ⊖ a yields a displacement w such that a ⊕ w recovers b.

From TumblerAdd, a ⊕ w acts at the action point k of w: it copies a₁..aₖ₋₁, advances aₖ by wₖ, and replaces the tail with w's tail. So if a ⊕ w = b, then a and b agree on components 1..k−1 and diverge at k, with bₖ = aₖ + wₖ and bᵢ = wᵢ for i > k. Reading off the width:

  wᵢ = 0  for i < k,    wₖ = bₖ − aₖ,    wᵢ = bᵢ  for i > k

where k = divergence(a, b). The component formulas match TumblerSub's definition of b ⊖ a. Lengths coincide when #a ≤ #b; when #a > #b, TumblerSub extends the result with trailing zeros to length #a, and by T3 the extended tumbler is distinct from the original. We write w = b ⊖ a and call it the *displacement from a to b*. The displacement is well-defined when:

**D0 (DisplacementWellDefined).** a < b, and the divergence k of a and b satisfies k ≤ #a.

*Proof.* Let `k = divergence(a, b)`. We show D0's hypotheses eliminate Divergence case (ii).

Sub-case (ii-a): `#a < #b` with `k = #a + 1`. Substituting into `k ≤ #a` yields `#a + 1 ≤ #a`; against NAT-addcompat's `#a < #a + 1`, NAT-order's trichotomy at `(#a, #a + 1)` refutes this.

Sub-case (ii-b): `#b < #a` with `k = #b + 1` and `b` a proper prefix of `a`; by T1 case (ii), `b < a`, contradicting `a < b`.

We are therefore in case (i): `k ≤ #a ∧ k ≤ #b`, with `aᵢ = bᵢ` for `i < k` and `aₖ ≠ bₖ`. Since `a < b`, T1 case (i) gives `aₖ < bₖ`.

**Well-definedness of the subtraction.** Since `a < b` entails `b ≥ a`, `w = b ⊖ a ∈ T` by TA2. Its length is `#w = L` per TumblerSub's length-pair dispatch at `(#b, #a)`: `L = #b` in sub-cases (α) `#b = #a` and (γ) `#a < #b`; `L = #a` in sub-case (β) `#b < #a`. Both `a` and `b` have actual components at positions `1, ..., k`, so the zero-padded extensions agree through position `k − 1` and disagree at `k`, whence `zpd(b, a) = divergence(b, a) = divergence(a, b) = k` (ZPD case (i); Divergence symmetry). TumblerSub yields:

  `wᵢ = 0` for `i < k`, `wₖ = bₖ − aₖ`, `wᵢ = bᵢ` for `i > k`

with `#w = L`. From `bₖ > aₖ` and NAT-order's definition of `≤` from `<`, `bₖ ≥ aₖ`, so `wₖ = bₖ − aₖ ∈ ℕ` by NAT-sub, and `wₖ ≥ 1` by NAT-sub's strict-positivity clause.

**Positivity.** TumblerSub's conditional postcondition gives `Pos(w)`.

**Action point.** TumblerSub's conditional postcondition gives `actionPoint(w) = zpd(b, a) = k`.

**Well-definedness of the addition.** TA0 requires `Pos(w)` and `actionPoint(w) ≤ #a`. Both hold, so `a ⊕ w ∈ T`.

**Round-trip boundary.** By TumblerAdd, `#(a ⊕ w) = #w = L`. When `#a > #b`, sub-case (β) gives `L = #a > #b`, whence `a ⊕ w ≠ b` by T3. Round-trip faithfulness requires `#a ≤ #b`, under which `L = #b` and component-by-component recovery succeeds (D1). ∎

*Formal Contract:*
- *Preconditions:* a ∈ T, b ∈ T, a < b, divergence(a, b) ≤ #a
- *Depends:*
  - Divergence (Divergence) — case structure and symmetry; case (i) gives shared-bound conjunction.
  - T1 (LexicographicOrder) — case (i) gives `aₖ < bₖ`; case (ii) gives `b < a` for the prefix sub-case.
  - TA2 (WellDefinedSubtraction) — `b ⊖ a ∈ T` from `b ≥ a`.
  - TumblerSub (TumblerSub) — component formulas, length-pair dispatch at `(#b, #a)`, and conditional postcondition (positivity, action point).
  - ZPD (ZPD) — `zpd(b, a) = divergence(b, a)` in case (i).
  - T3 (CanonicalRepresentation) — distinct lengths imply distinct tumblers.
  - TA-Pos (PositiveTumbler) — defines `Pos`.
  - ActionPoint (ActionPoint) — defines `actionPoint`.
  - TA0 (WellDefinedAddition) — `a ⊕ w ∈ T` from `Pos(w)` and `actionPoint(w) ≤ #a`.
  - TumblerAdd (TumblerAdd) — result-length identity `#(a ⊕ w) = #w`.
  - NAT-sub (NatPartialSubtraction) — conditional closure for `wₖ = bₖ − aₖ ∈ ℕ`; strict positivity for `wₖ ≥ 1`.
  - NAT-order (NatStrictTotalOrder) — trichotomy at `(#a, #a + 1)` for the sub-case (ii-a) refutation; definition of `≤` from `<` to convert `bₖ > aₖ` to `bₖ ≥ aₖ`.
  - NAT-addcompat (NatAdditionOrderAndSuccessor) — strict successor inequality `#a < #a + 1`.
- *Forward References:*
  - D1 (RoundTripRecovery) — proves the component-by-component recovery that this claim navigates to under the #a ≤ #b condition
- *Postconditions:* b ⊖ a ∈ T, Pos(b ⊖ a), actionPoint(b ⊖ a) = divergence(a, b), #(b ⊖ a) = L (per TumblerSub's length-pair dispatch at `(#b, #a)`), a ⊕ (b ⊖ a) ∈ T, #a > #b → a ⊕ (b ⊖ a) ≠ b

**D1 (DisplacementRoundTrip).** For tumblers a, b ∈ T with a < b, divergence(a, b) ≤ #a, and #a ≤ #b:

  a ⊕ (b ⊖ a) = b

*Proof.* Let k = divergence(a, b). The preconditions give k ≤ #a and #a ≤ #b.

We eliminate Divergence case (ii). Sub-case (ii-a) requires k = #a + 1, contradicting k ≤ #a via NAT-addcompat (#a < #a + 1) and NAT-order trichotomy. Sub-case (ii-b) requires #b < #a, contradicting #a ≤ #b by NAT-order trichotomy. The case-hypothesis #a ≠ #b excludes the equality disjunct. We are in case (i): aᵢ = bᵢ for 1 ≤ i < k, k ≤ #a ∧ k ≤ #b, and aₖ ≠ bₖ.

To direct the inequality at position k, we apply T1 to a < b. T1 supplies a witness j ≥ 1 with aᵢ = bᵢ for 1 ≤ i < j, satisfying either (i) j ≤ #a ∧ j ≤ #b ∧ aⱼ < bⱼ, or (ii) j = #a + 1 ≤ #b. T1 case (ii) is eliminated for the pair (a, b): it would make a a proper prefix of b, instantiating Divergence sub-case (ii-a) and forcing divergence(a, b) = #a + 1 — contradicting k = divergence(a, b) ≤ #a via NAT-addcompat (#a < #a + 1) and NAT-order trichotomy, exactly as the Divergence (ii-a) elimination already established. So T1 case (i) holds: j ≤ #a, j ≤ #b, aⱼ < bⱼ, and aᵢ = bᵢ for 1 ≤ i < j. NAT-order's exactly-one trichotomy at (aⱼ, bⱼ), via the disjointness clause ¬(aⱼ < bⱼ ∧ aⱼ = bⱼ), converts aⱼ < bⱼ to aⱼ ≠ bⱼ. Position j satisfies Divergence case (i)'s conjunction `1 ≤ j ∧ j ≤ #a ∧ j ≤ #b ∧ aⱼ ≠ bⱼ ∧ (A i : 1 ≤ i < j : aᵢ = bᵢ)` for the pair (a, b); Divergence's uniqueness clause for case (i) identifies j = k, yielding aₖ < bₖ.

We discharge TumblerSub's precondition b ≥ a before invoking it. From a < b, T1's ≤ abbreviation (a ≤ b ≡ a < b ∨ a = b) delivers a ≤ b by ∨-introduction; T1's ≥ abbreviation (b ≥ a ≡ a ≤ b) rewrites this as b ≥ a.

Define w = b ⊖ a. By the ZPD–Divergence relationship in case (i), zpd(b, a) = divergence(b, a); Divergence's symmetry gives divergence(b, a) = divergence(a, b) = k, so zpd(b, a) = k. TumblerSub yields:

  wᵢ = 0           for i < k
  wₖ = bₖ − aₖ     (∈ ℕ by NAT-sub closure, since bₖ ≥ aₖ via NAT-order from bₖ > aₖ)
  wᵢ = bᵢ          for i > k

For #w, TumblerSub's length-pair dispatch at (#b, #a) gives sub-case (α) #b = #a ⇒ L = #b, (β) #b < #a ⇒ L = #a, (γ) #a < #b ⇒ L = #b. The precondition #a ≤ #b forecloses (β) by NAT-order trichotomy. Both (α) and (γ) give #w = #b.

Three properties of w:
1. w ∈ T: from b ∈ T, a ∈ T, b ≥ a, by TumblerSub.
2. Pos(w): wₖ ≥ 1 by NAT-sub strict positivity (precondition bₖ > aₖ).
3. actionPoint(w) = k: TumblerSub's conditional postcondition gives actionPoint(w) = zpd(b, a) = k.

Since k ≤ #a, TA0's precondition is satisfied.

Compute a ⊕ w by TumblerAdd:

*Positions i < k:* (a ⊕ w)ᵢ = aᵢ = bᵢ (Divergence agreement).

*Position i = k:* (a ⊕ w)ₖ = aₖ + wₖ = aₖ + (bₖ − aₖ) = bₖ (NAT-sub left-inverse).

*Positions i > k:* (a ⊕ w)ᵢ = wᵢ = bᵢ.

By TumblerAdd's result-length identity, #(a ⊕ w) = #w = #b. Component-wise equality with matching lengths gives a ⊕ w = b by T3.  ∎

*Formal Contract:*
- *Preconditions:* a ∈ T, b ∈ T, a < b, divergence(a, b) ≤ #a, #a ≤ #b
- *Depends:*
  - Divergence (Divergence) — case (i) supplies aᵢ = bᵢ for 1 ≤ i < k, shared-bound k ≤ #a ∧ k ≤ #b, and aₖ ≠ bₖ; sub-case (ii-a) instantiated by a-proper-prefix-of-b rules out T1 case (ii) for (a, b) by forcing divergence(a, b) = #a + 1 against k ≤ #a; uniqueness clause for case (i) identifies T1 case (i)'s witness j with k, lifting aⱼ < bⱼ to aₖ < bₖ; symmetry bridges divergence(a, b) = divergence(b, a).
  - T1 (LexicographicOrder) — supplies a witness j for a < b in one of two cases; case (ii) is eliminated for the pair (a, b) (it would make a a proper prefix of b, instantiating Divergence sub-case (ii-a) and contradicting k ≤ #a), so case (i) holds with aⱼ < bⱼ at j ≤ #a ∧ j ≤ #b and aᵢ = bᵢ for 1 ≤ i < j — Divergence's uniqueness then identifies j = k, yielding aₖ < bₖ; discharges TumblerSub's precondition b ≥ a from a < b via the ≤ abbreviation (a ≤ b ≡ a < b ∨ a = b) and the ≥ abbreviation (b ≥ a ≡ a ≤ b).
  - ZPD (ZPD) — identifies zpd(b, a) = divergence(b, a) in case (i).
  - TumblerSub (TumblerSub) — component formulas for w = b ⊖ a, w ∈ T, length-pair dispatch, and conditional postcondition actionPoint(w) = zpd(b, a).
  - TA-Pos (PositiveTumbler) — defines Pos(w).
  - ActionPoint (ActionPoint) — minimum-formula underlying TumblerSub's action-point identification.
  - TA0 (WellDefinedAddition) — establishes a ⊕ w ∈ T from Pos(w) and actionPoint(w) ≤ #a.
  - TumblerAdd (TumblerAdd) — constructive component definition and result-length identity #(a ⊕ w) = #w.
  - T3 (CanonicalRepresentation) — concludes a ⊕ w = b from component-wise equality and matching length.
  - NAT-sub (NatPartialSubtraction) — conditional closure for wₖ ∈ ℕ; strict positivity for wₖ ≥ 1; left-inverse for aₖ + (bₖ − aₖ) = bₖ.
  - NAT-addcompat (NatAdditionOrderAndSuccessor) — strict successor inequality #a < #a + 1 used in Divergence sub-case (ii-a) elimination and again in T1 case (ii) elimination for the pair (a, b).
  - NAT-order (NatStrictTotalOrder) — trichotomy at (#a, #a+1) for Divergence sub-case (ii-a) and for T1 case (ii) elimination at (a, b); at (#a, #b) for Divergence sub-case (ii-b) and TumblerSub sub-case (β); exactly-one trichotomy's disjointness clause ¬(aⱼ < bⱼ ∧ aⱼ = bⱼ) at (aⱼ, bⱼ) converts T1 case (i)'s aⱼ < bⱼ into aⱼ ≠ bⱼ to qualify j for Divergence case (i)'s conjunction; <-to-≤ weakening of bₖ > aₖ.
- *Postconditions:* a ⊕ (b ⊖ a) = b

**D2 (DisplacementUnique).** Under D1's preconditions (a < b, divergence(a, b) ≤ #a, #a ≤ #b), for any w ∈ T with Pos(w) and actionPoint(w) ≤ #a such that a ⊕ w = b, we have w = b ⊖ a.

*Proof.* Any w carrying a to b must equal b ⊖ a. We produce a second witness for the equation, then apply left cancellation.

**Step 1: a second witness.** By D1, a ⊕ (b ⊖ a) = b. So both w and b ⊖ a, added to a, yield b.

**Step 2: establishing TA-LC's preconditions.** Both additions must satisfy TA0.

For w: Pos(w) and actionPoint(w) ≤ #a are given, so a ⊕ w is well-defined and equals b. TumblerAdd's result-length identity yields #w = #(a ⊕ w) = #b.

For b ⊖ a: let k = divergence(a, b). Divergence case (ii) is eliminated: sub-case (ii-a) gives k = #a + 1, contradicting k ≤ #a via NAT-addcompat's #a < #a + 1 and NAT-order's trichotomy; sub-case (ii-b) gives #b < #a, contradicting #a ≤ #b via NAT-order's trichotomy; the #a = #b situation is excluded by case (ii)'s hypothesis #a ≠ #b. We are in case (i): k ≤ #a ∧ k ≤ #b, with aᵢ = bᵢ for i < k and aₖ < bₖ (by T1 at the divergence point). By ZPD and Divergence's symmetry, zpd(b, a) = divergence(b, a) = divergence(a, b) = k. The precondition a < b yields b ≥ a via T1's strict-to-weak weakening, discharging TumblerSub's first precondition. TumblerSub then gives b ⊖ a ∈ T; component formulas (b ⊖ a)ᵢ = 0 for i < k and (b ⊖ a)ₖ = bₖ − aₖ; and length-pair dispatch at (#b, #a), under #a ≤ #b, gives #(b ⊖ a) = #b. By NAT-sub, (b ⊖ a)ₖ ∈ ℕ and (b ⊖ a)ₖ ≥ 1, so Pos(b ⊖ a). TumblerSub's conditional postcondition gives actionPoint(b ⊖ a) = zpd(b, a) = k ≤ #a. TA0's preconditions are satisfied.

**Step 3: cancellation.** From a ⊕ w = b and a ⊕ (b ⊖ a) = b:

  a ⊕ w = a ⊕ (b ⊖ a)

By TA-LC, w = b ⊖ a.  ∎

D1 and D2 together characterize the displacement: D1 says b ⊖ a recovers b, D2 says nothing else does. When a = b, the degenerate case is handled separately since b ⊖ a is the zero tumbler and TA0 requires Pos(w).

*Worked example.* Let a = [1, 2, 3] and b = [1, 5, 1], so #a = #b = 3.

*D0 check.* divergence(a, b) = 2, since a₁ = b₁ = 1 and a₂ = 2 ≠ 5 = b₂. k = 2 ≤ #a = 3.

*Displacement.* By TumblerSub, w = b ⊖ a: w₁ = 0, w₂ = 5 − 2 = 3, w₃ = 1. So w = [0, 3, 1].

*Round-trip.* actionPoint(w) = 2. By TumblerAdd, a ⊕ [0, 3, 1]: position 1 copies a₁ = 1, position 2 computes 2 + 3 = 5, position 3 copies w₃ = 1. Result: [1, 5, 1] = b.  ✓

*Uniqueness check.* Any w' with a ⊕ w' = b satisfies w' = b ⊖ a = [0, 3, 1] = w by D2.

For #a < #b: let a' = [1, 2], b = [1, 5, 1]. #a' = 2 < 3 = #b, divergence is 2, k = 2 ≤ #a' = 2. TumblerSub gives w = [0, 3, 1] of length 3, and a' ⊕ [0, 3, 1] = [1, 5, 1] = b.

*Formal Contract:*
- *Preconditions:* a ∈ T, b ∈ T, w ∈ T, a < b, divergence(a, b) ≤ #a, #a ≤ #b, Pos(w), actionPoint(w) ≤ #a, a ⊕ w = b
- *Depends:*
  - D1 (DisplacementRoundTrip) — supplies the second witness a ⊕ (b ⊖ a) = b.
  - T1 (LexicographicOrder) — gives bₖ > aₖ at the divergence point; strict-to-weak weakening a < b ⇒ b ≥ a.
  - Divergence — case analysis eliminating case (ii); symmetry divergence(a, b) = divergence(b, a).
  - ZPD — zpd(b, a) = divergence(b, a), bridging to k.
  - TumblerSub — carrier membership b ⊖ a ∈ T, component formulas at k, action-point identification, length-pair dispatch at (#b, #a).
  - TumblerAdd — result-length identity #(a ⊕ w) = #w pinning #w = #b.
  - ActionPoint — defining minimum-formula underlying actionPoint(b ⊖ a) = k.
  - TA-Pos (PositiveTumbler) — positivity predicate Pos(·).
  - TA0 (WellDefinedAddition) — well-definedness precondition for both additions.
  - TA-LC (LeftCancellation) — cancellation rule yielding w = b ⊖ a.
  - NAT-sub (NatPartialSubtraction) — conditional closure and strict positivity for (b ⊖ a)ₖ = bₖ − aₖ.
  - NAT-addcompat (NatAdditionOrderAndSuccessor) — strict successor inequality #a < #a + 1 for sub-case (ii-a).
  - NAT-order (NatStrictTotalOrder) — trichotomy at (#a, #a + 1), (#a, #b), and (aₖ, bₖ).
- *Forward References:*
  - D0 (DisplacementWellDefined) — named in the worked example as the precondition checkpoint; D2 re-derives its conclusions independently.
- *Postconditions:* w = b ⊖ a

### Ordinal displacement and shift

**OrdinalDisplacement (OrdinalDisplacement).** For natural number n ≥ 1 and depth m ≥ 1, the *ordinal displacement* δ(n, m) is the tumbler [0, 0, ..., 0, n] of length m — zero at positions 1 through m − 1, and n at position m. Its action point is m.

δ(n, m) is a finite sequence of length m ≥ 1 over ℕ, so δ(n, m) ∈ T by T0. Component typing: the m-th component is n, with `n ∈ ℕ` from the precondition; positions 1..m−1 are 0, with `0 ∈ ℕ` from NAT-zero's first axiom clause `0 ∈ ℕ`.

The length postcondition `#δ(n, m) = m` holds by construction from the Definition clause.

Promote `n ≥ 1` to `n ≠ 0`: NAT-closure exports `0 < 1` as a *Consequence* — derived from its successor-positivity clause `(A n ∈ ℕ :: 0 < n + 1)` instantiated at `n := 0` composed with its left-identity clause `(A n ∈ ℕ :: 0 + n = n)` instantiated at `n := 1` via substitutivity of `=`. NAT-order's `m ≤ n ⟺ m < n ∨ m = n` unfolds `n ≥ 1` to `1 < n ∨ 1 = n`. In the first disjunct, transitivity of `<` composes `0 < 1` with `1 < n` to yield `0 < n`; in the second, substitution of `n = 1` into `0 < 1` yields `0 < n`. NAT-order's exactly-one trichotomy exports the conjunct `¬(m < n ∧ m = n)`; instantiated at `(m, n) := (0, n)` it gives `¬(0 < n ∧ 0 = n)`. With `0 < n` in hand, the propositional step `¬(A ∧ B) ∧ A ⟹ ¬B` yields `¬(0 = n)`, i.e., `0 ≠ n`; by symmetry of `=`, `n ≠ 0`.

Since δ(n, m)ₘ = n and `n ≠ 0`, the m-th component is nonzero, whence Pos(δ(n, m)) by TA-Pos. By ActionPoint, actionPoint(δ(n, m)) = min({i : 1 ≤ i ≤ m ∧ δ(n, m)ᵢ ≠ 0}); since δ(n, m)ᵢ = 0 for 1 ≤ i < m and δ(n, m)ₘ = n ≠ 0, this set equals {m}, whose minimum is m. ∎

When the depth is determined by context (typically m = #v for the tumbler being shifted), we write δₙ.

*Formal Contract:*
- *Preconditions:* n ∈ ℕ, m ∈ ℕ, n ≥ 1, m ≥ 1
- *Definition:* δ(n, m) = [0, 0, …, 0, n] of length m
- *Depends:*
  - T0 (CarrierSetDefinition) — carrier-set criterion for `δ(n, m) ∈ T`; length operator `#·: T → ℕ` for `#δ(n, m) = m`.
  - NAT-carrier (NatCarrierSet) — supplies `ℕ` as the underlying set appearing in the Precondition membership clauses `n ∈ ℕ` and `m ∈ ℕ`, and as the codomain typing the components of δ(n, m) (the m-th component `n` drawn from the precondition and the leading zeros at positions 1..m−1 drawn from NAT-zero's `0 ∈ ℕ`), discharging T0's commitment that a tumbler's components be ℕ-valued.
  - NAT-zero (NatZeroMinimum) — supplies `0 ∈ ℕ` for the m − 1 leading zero components.
  - NAT-order (NatStrictTotalOrder) — `≤`/`<` unfolding, transitivity of `<`, and the `¬(m < n ∧ m = n)` conjunct of the exactly-one trichotomy, used in `n ≥ 1 ⟹ n ≠ 0`.
  - NAT-closure (NatArithmeticClosureAndIdentity) — supplies the *Consequence* `0 < 1` (derived from its successor-positivity and left-identity clauses) that anchors the `n ≥ 1 ⟹ n ≠ 0` promotion.
  - TA-Pos (PositiveTumbler) — positivity predicate witnessed at i = m.
  - ActionPoint (ActionPoint) — minimum-position formula evaluated against δ's component pattern.
- *Postconditions:* δ(n, m) ∈ T, #δ(n, m) = m, Pos(δ(n, m)), actionPoint(δ(n, m)) = m


---

## 13. Adjacency and global properties

Divergence identifies the first position at which two tumblers differ; PrefixOrderingExtension lifts the prefix relation through extensions; ReverseInverse captures the inverse pairing of forward and backward operations. GlobalUniqueness establishes that every reachable state assigns each tumbler at most one ownership — the foundation on which the ownership predicate of ASN-0042 rests.

**Divergence (Divergence).** For tumblers `a, b ∈ T` with `a ≠ b`, the *divergence* `divergence(a, b)` is defined by two cases reflecting the two ways distinct finite sequences over ℕ can fail to coincide: at a shared position by component mismatch, or by one being a proper prefix of the other.

  (i) If there exists `k` with `1 ≤ k ∧ k ≤ #a ∧ k ≤ #b` and `aₖ ≠ bₖ`, then `divergence(a, b)` is the least such `k` — equivalently, the unique `k` satisfying `1 ≤ k ∧ k ≤ #a ∧ k ≤ #b ∧ aₖ ≠ bₖ ∧ (A i : 1 ≤ i < k : aᵢ = bᵢ)`, the universal conjunct restating minimality — component divergence at a shared position.

  (ii) If `#a ≠ #b ∧ (A i : 1 ≤ i ≤ #a ∧ i ≤ #b : aᵢ = bᵢ)` — equivalently, lengths differ and case (i) does not apply — then NAT-order's trichotomy applied to `(#a, #b)` rules out the `#a = #b` branch and splits on which length is shorter. In sub-case (ii-a), `#a < #b`. To see that `i ≤ #a` entails `i ≤ #b`, unfold `i ≤ #a` against NAT-order's definition `x ≤ y ⟺ x < y ∨ x = y` into two branches: in the strict branch `i < #a`, NAT-order's `<`-transitivity at `(i, #a, #b)` with `#a < #b` gives `i < #b`; in the equality branch `i = #a`, indiscernibility of `=` substitutes `i = #a` into `#a < #b` to yield `i < #b`. Either way `i < #b`, hence `i ≤ #b` by the same definition. The range `1 ≤ i ≤ #a ∧ i ≤ #b` therefore reduces to `1 ≤ i ≤ #a`, yielding `(A i : 1 ≤ i ≤ #a : aᵢ = bᵢ)`, whence `divergence(a, b) = #a + 1`. In sub-case (ii-b), `#b < #a`. To see that `i ≤ #b` entails `i ≤ #a`, unfold `i ≤ #b` similarly: in the strict branch `i < #b`, `<`-transitivity at `(i, #b, #a)` with `#b < #a` gives `i < #a`; in the equality branch `i = #b`, indiscernibility of `=` substitutes `i = #b` into `#b < #a` to yield `i < #a`. Either way `i < #a`, hence `i ≤ #a` by the definition. The range `1 ≤ i ≤ #a ∧ i ≤ #b` therefore reduces to `1 ≤ i ≤ #b`, yielding `(A i : 1 ≤ i ≤ #b : aᵢ = bᵢ)`, whence `divergence(a, b) = #b + 1`. In either sub-case the divergence lies one position past the shorter tumbler's last component — prefix divergence, where one tumbler is a proper prefix of the other.

Exactly one case applies for any `a ≠ b`. Mutual exclusivity: if case (i) holds, some `aₖ ≠ bₖ` with `k ≤ #a ∧ k ≤ #b` falsifies case (ii)'s universal agreement at shared positions. Exhaustiveness: if neither case applies, all shared components agree and `#a = #b`, so by T3, `a = b`, contradicting `a ≠ b`.

The function is symmetric: `divergence(a, b) = divergence(b, a)`. In case (i), the qualifying conjunction is invariant under operand swap — `1 ≤ k` mentions neither operand, `k ≤ #a ∧ k ≤ #b` by `∧`-commutativity, `aₖ ≠ bₖ` by `≠`-symmetry, `(A i : 1 ≤ i < k : aᵢ = bᵢ)` by `=`-symmetry — so the same `k` witnesses case (i) under swap. In case (ii), swapping `(a, b)` exchanges sub-cases (ii-a) and (ii-b); both select one-plus the shorter tumbler's length.

*Formal Contract:*
- *Preconditions:* a ∈ T, b ∈ T, a ≠ b
- *Definition:* (i) if `(∃ k : 1 ≤ k ∧ k ≤ #a ∧ k ≤ #b : aₖ ≠ bₖ)`, then `divergence(a, b)` is the least `k` satisfying `1 ≤ k ∧ k ≤ #a ∧ k ≤ #b ∧ aₖ ≠ bₖ ∧ (A i : 1 ≤ i < k : aᵢ = bᵢ)` (equivalently, the unique such `k`, the universal conjunct being the minimality condition restated); (ii) if `#a ≠ #b ∧ (A i : 1 ≤ i ≤ #a ∧ i ≤ #b : aᵢ = bᵢ)`, then `divergence(a, b) = #a + 1` when `#a < #b` (sub-case (ii-a)) and `divergence(a, b) = #b + 1` when `#b < #a` (sub-case (ii-b)).
- *Depends:*
  - T0 (CarrierSetDefinition) — supplies `a, b ∈ T`, lengths `#a, #b`, and component projections `aₖ, bₖ, aᵢ, bᵢ` as ℕ-valued, making component (in)equalities well-formed.
  - T3 (CanonicalRepresentation) — exhaustiveness: if neither case applies, all shared components agree and `#a = #b`, so `a = b`, contradicting `a ≠ b`.
  - NAT-order (NatStrictTotalOrder) — trichotomy at length pair `(#a, #b)` splits case (ii) into sub-cases (ii-a)/(ii-b); the definition `x ≤ y ⟺ x < y ∨ x = y` and `<`-transitivity together discharge the mixed `≤`-`<` chain showing `i ≤ #a ⇒ i ≤ #b` under `#a < #b` (and the symmetric chain under `#b < #a`) by case-splitting on the unfolded `≤` and applying `<`-transitivity in the strict branch and `=`-substitution in the equality branch.
  - NAT-wellorder (NatWellOrdering) — existence of a least element in the nonempty subset `{k ∈ ℕ : 1 ≤ k ∧ k ≤ #a ∧ k ≤ #b ∧ aₖ ≠ bₖ}` grounds case (i)'s designating description, so "the least such `k`" is non-vacuous.
  - NAT-closure (NatArithmeticClosureAndIdentity) — addition closure instantiated at `(#a, 1)` and `(#b, 1)`, with `1 ∈ ℕ` from the same axiom, well-types case (ii)'s values `#a + 1` and `#b + 1` as ℕ.
- *Postconditions:* `divergence(a, b) ∈ ℕ`; exactly one of case (i) or case (ii) applies; in case (ii), `divergence(a, b) = #a + 1` in sub-case (ii-a) and `divergence(a, b) = #b + 1` in sub-case (ii-b); `divergence(a, b) = divergence(b, a)` for all `a ≠ b`.

**PrefixOrderingExtension (PrefixOrderingExtension).** Let `p₁, p₂ ∈ T` be tumblers such that `p₁ < p₂` and neither is a prefix of the other (`p₁ ⋠ p₂ ∧ p₂ ⋠ p₁`). Then for every `a` extending `p₁` (`p₁ ≼ a`) and every `b` extending `p₂` (`p₂ ≼ b`), `a < b`.

*Proof.* Let `p₁ = p₁₁. ... .p₁ₘ` and `p₂ = p₂₁. ... .p₂ₙ`. By T1, `p₁ < p₂` gives a least position `k ≥ 1` with `(A i : 1 ≤ i < k : p₁ᵢ = p₂ᵢ)` and one of two cases. Case (ii) would require `p₁ ≼ p₂`, contradicting non-nesting. So case (i) applies:

  (H1) `(A i : 1 ≤ i < k : p₁ᵢ = p₂ᵢ)`.

  (H2) `k ≤ min(m, n)` and `p₁ₖ < p₂ₖ`.

Let `a, b ∈ T` with `p₁ ≼ a` and `p₂ ≼ b`. By Prefix, `#a ≥ m` and `aᵢ = p₁ᵢ` for `1 ≤ i ≤ m`; `#b ≥ n` and `bᵢ = p₂ᵢ` for `1 ≤ i ≤ n`. Since `k ≤ m` and `k ≤ n`, we have `aₖ = p₁ₖ` and `bₖ = p₂ₖ`.

For `i` with `1 ≤ i < k`: `aᵢ = p₁ᵢ = p₂ᵢ = bᵢ` by Prefix, H1, and Prefix. At position `k`: `aₖ = p₁ₖ < p₂ₖ = bₖ` by H2. Since `k ≤ min(#a, #b)`, T1 case (i) yields `a < b`. ∎

*Formal Contract:*
- *Preconditions:* `p₁, p₂ ∈ T` with `p₁ < p₂` and `p₁ ⋠ p₂ ∧ p₂ ⋠ p₁`; `a, b ∈ T` with `p₁ ≼ a` and `p₂ ≼ b`.
- *Depends:*
  - T1 (LexicographicOrder) — supplies divergence position `k` with `p₁ₖ < p₂ₖ`; re-applied to conclude `a < b`.
  - Prefix (PrefixRelation) — transfers component equality and length bounds from `p₁, p₂` onto `a, b`.
- *Postconditions:* `a < b` under T1.

**ReverseInverse (ReverseInverse).** `(A a, w : a ≥ w ∧ Pos(w) ∧ k = #a ∧ #w = k ∧ (A i : 1 ≤ i < k : aᵢ = 0) : (a ⊖ w) ⊕ w = a)`, where `k` is the action point of `w`.

*Proof.* Let `k` denote the action point of `w`, so `wᵢ = 0` for `i < k`.

**Step 1: structure of `y = a ⊖ w`.** TumblerSub zero-pads operands to common length `L` via NAT-order's trichotomy on `(#a, #w)`. The preconditions `k = #a` and `#w = k` give `#a = #w = k`, placing the pair in the equal-length sub-case with `L = k` and empty padding region. For `i < k`, both `aᵢ = 0` (precondition) and `wᵢ = 0` (action point), so operands agree before position `k`.

NAT-order's trichotomy at `(aₖ, wₖ)` gives three outcomes. If `aₖ < wₖ`, then T1 case (i) at position `k` yields `a < w`, contradicting `a ≥ w`. Two cases remain:

- If `aₖ = wₖ`: `a` and `w` agree everywhere, and TumblerSub's no-divergence branch produces the zero tumbler of length `k`.
- If `aₖ > wₖ`: ZPD's case-split identifies `zpd(a, w)` as defined; pre-`k` agreement together with ZPD's minimality fixes `k = zpd(a, w)`. TumblerSub's three-region rule produces `yᵢ = 0` for `i < k`, `yₖ = aₖ - wₖ > 0` (by NAT-sub's conditional closure and strict-positivity clauses), and no components beyond `k`.

Record:
- (Y1) `#y = k`
- (Y2) `yᵢ = 0` for `1 ≤ i < k`
- (Y3a) equality branch `aₖ = wₖ`: `yₖ = 0`
- (Y3b) divergence branch `aₖ > wₖ`: `yₖ = aₖ - wₖ > 0`

**Step 2: TA4 applies to `y` and `w`.** TA4's six preconditions hold: `y ∈ T` (TumblerSub carrier-membership), `w ∈ T`, `Pos(w)`, `k = #y` (Y1), `#w = k`, and `(A i : 1 ≤ i < k : yᵢ = 0)` (Y2). TA4 yields:

`(y ⊕ w) ⊖ w = y`  — (†)

**Step 3: `y ⊕ w = a` by contradiction via TA3-strict.** Assume `y ⊕ w ≠ a`.

*Carrier membership of `y ⊕ w`.* TumblerAdd's preconditions at `(y, w)`: `y ∈ T` (Step 2), `w ∈ T`, `Pos(w)`, and `actionPoint(w) ≤ #y` (from `actionPoint(w) = k = #y` via NAT-order's defining clause). TumblerAdd yields `y ⊕ w ∈ T`.

*Equal length.* `#(y ⊕ w) = #w = k = #a` by TumblerAdd's result-length identity.

*`y ⊕ w > w`.* By TumblerAdd, for `i < k`: `(y ⊕ w)ᵢ = yᵢ = 0 = wᵢ`. At `k`: `(y ⊕ w)ₖ = yₖ + wₖ`. We show `yₖ > 0`. Suppose `yₖ = 0`. In the divergence branch, Y3b gives `yₖ > 0`, contradicting the hypothetical via NAT-order's irreflexivity at `n = 0`. So we are in the equality branch: `y` is the zero tumbler of length `k`, and `aₖ = wₖ`. With pre-`k` agreement and `#a = #w = k`, T3 gives `a = w`. Then `(y ⊕ w)ₖ = 0 + wₖ = wₖ` (NAT-closure's additive identity), so `y ⊕ w = w = a`, contradicting `y ⊕ w ≠ a`. Hence `yₖ > 0`.

Promote to `yₖ + wₖ > wₖ`: NAT-order's defining clause weakens `yₖ > 0` to `0 ≤ yₖ`; NAT-addcompat's right order-compatibility lifts this to `yₖ + wₖ ≥ 0 + wₖ`; NAT-closure rewrites to `yₖ + wₖ ≥ wₖ`; NAT-cancel's summand absorption rules out the equality disjunct (which would force `yₖ = 0`); NAT-order's defining clause returns `yₖ + wₖ > wₖ`. T1 case (i) at position `k` gives `y ⊕ w > w`.

*Trichotomy contradiction.* By T1, since `y ⊕ w ≠ a`, either `y ⊕ w > a` or `y ⊕ w < a`.

*Case `y ⊕ w > a`:* TA3-strict with `a := a, b := y ⊕ w` yields `a ⊖ w < (y ⊕ w) ⊖ w`. Left side is `y` by definition; right side is `y` by (†). So `y < y`, contradicting T1's irreflexivity.

*Case `y ⊕ w < a`:* TA3-strict with `a := y ⊕ w, b := a` yields `(y ⊕ w) ⊖ w < a ⊖ w`. Left is `y` by (†); right is `y` by definition. Again `y < y`, contradicting irreflexivity.

Both cases impossible, so `y ⊕ w = a`. Therefore `(a ⊖ w) ⊕ w = a`. ∎

*Formal Contract:*
- *Preconditions:* `a ∈ T`, `w ∈ T`, `a ≥ w`, `Pos(w)`, `k = #a`, `#w = k`, `(A i : 1 ≤ i < k : aᵢ = 0)`, where `k` is the action point of `w`
- *Depends:*
  - TumblerSub — piecewise definition for structure of `y = a ⊖ w`; carrier-membership postcondition `a ⊖ w ∈ T`.
  - TumblerAdd — prefix-copy/advance rule for components of `y ⊕ w`; result-length identity `#(a ⊕ w) = #w`; carrier-membership postcondition `a ⊕ w ∈ T`.
  - TA-Pos (PositiveTumbler) — precondition `Pos(w)`.
  - ActionPoint — action-point function; `wᵢ = 0` for `i < actionPoint(w)`.
  - TA4 (PartialInverse) — yields `(y ⊕ w) ⊖ w = y`.
  - T1 (LexicographicOrder) — case (i) at divergence position `k`; trichotomy on `(y ⊕ w, a)`; irreflexivity.
  - T3 (CanonicalRepresentation) — yields `a = w` in the equality branch.
  - ZPD (ZeroPaddedDivergence) — case-split and minimality clauses keying TumblerSub's branches.
  - TA3-strict (OrderPreservationUnderSubtractionStrict) — applied at both trichotomy cases.
  - T0 (CarrierSetDefinition) — carrier `T`, length `#`, component projection with typing `aᵢ ∈ ℕ`.
  - NAT-sub — conditional closure and strict positivity for `aₖ - wₖ`.
  - NAT-addcompat — right order-compatibility for the strict-promotion chain.
  - NAT-closure — additive identity `0 + wₖ = wₖ`.
  - NAT-cancel — summand absorption ruling out `yₖ + wₖ = wₖ`.
  - NAT-zero — `0 ∈ ℕ` for the zero-valued components and inequalities.
  - NAT-order — trichotomy on length and component pairs; defining clause `m ≤ n ⟺ m < n ∨ m = n`; irreflexivity at `n = 0`.
- *Postconditions:* `(a ⊖ w) ⊕ w = a`

**GlobalUniqueness (GlobalUniqueness).** No two distinct allocations, anywhere in the system, at any time, produce the same address.

*Proof.* For any two addresses `a` and `b` produced by distinct allocation events, we show `a ≠ b` by strong induction on allocator tree depth.

An *allocation event* is either the initialization of the root allocator — establishing its base address `t₀` satisfying T4 — or an invocation of `inc(t, k)`. Each allocator `A` with base address `t₀` has *domain* `dom(A) = {tₙ : n ≥ 0}` where `tₙ₊₁ = inc(tₙ, 0)`. When a parent executes `inc(t, k')` with `k' > 0`, the result `c₀ = inc(t, k')` becomes the base of a new child allocator and is assigned to that child's domain. The *producing allocator* of an address is the allocator to which the generating event assigns it: root initialization assigns `t₀` to root; `inc(t, 0)` assigns the output to the executing allocator; `inc(t, k')` with `k' > 0` assigns the output to the newly created child.

For a non-root allocator `A` spawned by `c₀ = inc(t, k')` with `k' > 0`, the *domain prefix* of `A` is the parent domain element `t`. The root has no domain prefix.

Define *depth* as the number of child-spawning steps from the root: root has depth 0, a child of a depth-*d* allocator has depth *d* + 1. The inductive claim `U(d)`: every pair of distinct allocation events whose producing allocators both have depth ≤ *d* yields distinct outputs.

*Base case* (`d = 0`): the root is the sole depth-0 allocator; every pair of distinct events at depth 0 shares the root as producing allocator, so Case 1 gives `a ≠ b`.

*Inductive step*: assume `U(d)`; prove `U(d + 1)`. Pairs with both depths ≤ *d* follow from the hypothesis. For pairs at maximum depth *d* + 1, the five cases below apply.

*Case 1: Same producing allocator.* Both `a` and `b` belong to `dom(A)`. The sequence `t₀, inc(t₀, 0), inc(inc(t₀, 0), 0), ...` is the stream over which T9 is proved. Since the events are distinct, WLOG `allocated_before(a, b)`; by T9, `a < b`; by T1 irreflexivity, `a ≠ b`.

*Case 2: Root vs non-root.* `a ∈ dom(root)`, `b ∈ dom(A)` for non-root `A`. By T10a.1, every root output has length `γ = #t₀`. By T10a.3, a descendant at depth `d ≥ 1` produces outputs of length `≥ γ + 1`. Hence `#a ≠ #b`, and by T3, `a ≠ b`.

*Case 3: Non-root allocators with non-nesting domain prefixes.* `A₁` and `A₂` non-root with prefixes `p₁`, `p₂` satisfying `p₁ ⋠ p₂ ∧ p₂ ⋠ p₁`.

Every output of a non-root allocator extends its domain prefix. Let `A` have prefix `t` and base `c₀ = inc(t, k')` with `k' > 0`. By TA5(b), `c₀` agrees with `t` on positions `1 ≤ i ≤ #t`; by TA5(d), `#c₀ = #t + k' > #t`; so `t ≼ c₀`. Each `cₙ₊₁ = inc(cₙ, 0)` modifies only position `sig(cₙ) = #cₙ` (TA5(c), TA5-SigValid, T10a.4). Since `#cₙ = #t + k'` (T10a.1), the modified position exceeds `#t`, so positions `1, …, #t` are unchanged across siblings; `t ≼ cₙ` for every output of `A`.

Let `a ∈ dom(A₁)`, `b ∈ dom(A₂)`. Then `p₁ ≼ a` and `p₂ ≼ b`. T10 applies: locate `k` with `p₁ₖ ≠ p₂ₖ`, transfer to `aₖ ≠ bₖ`, conclude `a ≠ b` via T3.

*Case 4: Nesting prefixes, different zero counts.* Suppose `a = b`. By T3, `aᵢ = bᵢ` at every position, so `zeros(a) = zeros(b)`, contradicting `zeros(a) ≠ zeros(b)`. Therefore `a ≠ b`.

*Case 5: Nesting prefixes, same zero count.* Two non-root allocators with `p₁ ≼ p₂`, `p₁ ≠ p₂`. We show length separation excludes collision.

Let the parent have base `t₀` with `#t₀ = γ`. By T10a, the parent produces siblings via `inc(·, 0)`; by TA5(c), every parent sibling output has length `γ`. To spawn a child, the parent performs `inc(t, k')` with `k' > 0`, producing `c₀ = inc(t, k')` with `#c₀ = γ + k'` (TA5(d)). The child produces its siblings by `inc(·, 0)`, so all child outputs have length `γ + k' ≥ γ + 1`. For any parent output `a` and child output `b`, `#a ≠ #b`, so by T3, `a ≠ b`.

For the general nesting-prefix pair: let `A₁`, `A₂` be non-root with prefixes `p₁ ≼ p₂`, `p₁ ≠ p₂`, spawned with `k'ᵢ ∈ {1, 2}`, producing outputs of uniform length `#pᵢ + k'ᵢ`. Suppose `#p₁ + k'₁ = #p₂ + k'₂`. Since `p₁ ≺ p₂`, Prefix's postcondition gives `#p₁ < #p₂`.

By NAT-order trichotomy on `(k'₁, k'₂)`:
- *Sub-case `k'₁ = k'₂`*: NAT-cancel yields `#p₁ = #p₂`, contradicting `#p₁ < #p₂`.
- *Sub-case `k'₁ < k'₂`*: NAT-addcompat (left) lifts `k'₁ ≤ k'₂` to `#p₁ + k'₁ ≤ #p₁ + k'₂`; NAT-addcompat (right) lifts `#p₁ ≤ #p₂` to `#p₁ + k'₂ ≤ #p₂ + k'₂`, sharpened to strict by NAT-cancel ruling out `#p₁ + k'₂ = #p₂ + k'₂`. NAT-order transitivity gives `#p₁ + k'₁ < #p₂ + k'₂`, contradicting the assumed equality by NAT-order irreflexivity.
- *Remaining case `k'₁ > k'₂`*: with values in `{1, 2}`, `(k'₁, k'₂) = (2, 1)`, so `#p₁ + 2 = #p₂ + 1`. Rewriting `2 = 1 + 1` and applying NAT-addassoc gives `(#p₁ + 1) + 1 = #p₂ + 1`; NAT-cancel yields `#p₂ = #p₁ + 1`.

So `p₂` extends `p₁` by one position. By T10a.4, `p₂` is T4-valid; by T4 clause (iv), `p₂[#p₂] ≠ 0`. Hence `zeros(p₂) = zeros(p₁)`. With `k'₁ = 2`, TA5(d) gives `zeros(c₀(A₁)) = zeros(p₁) + 1`; with `k'₂ = 1`, `zeros(c₀(A₂)) = zeros(p₂) = zeros(p₁)`. T10a.8 lifts each base zero count to every sibling. Therefore `zeros(a) ≠ zeros(b)` for every `a ∈ dom(A₁)`, `b ∈ dom(A₂)` — routing the pair to Case 4 and contradicting Case 5's same-zero-count assumption.

Every pair in Case 5 thus satisfies `#a ≠ #b`; by T3, `a ≠ b`.

*Exhaustiveness.* Every pair of distinct allocation events has well-defined producing allocators. Same producing allocator: Case 1. Different, one is root: Case 2. Both non-root, non-nesting prefixes: Case 3. Both non-root, `p₁ = p₂`: let `Pᵢ = parent(Aᵢ)`, so `pᵢ ∈ dom(Pᵢ)` (the domain prefix of `Aᵢ` is by construction an output of its parent). T10a.6 gives `dom(P₁) ∩ dom(P₂) = ∅` for distinct allocators; the shared value `p₁ = p₂` therefore forces `P₁ = P₂`: same parent, same domain element `t = p₁ = p₂`, parameters `k'₁, k'₂ ∈ {1, 2}`. T10a's per-parent uniqueness — at most one child-spawning event per `(t, k')` — excludes `k'₁ = k'₂` (else `A₁ = A₂` by T10a's identity criterion, contradicting distinctness), so `{k'₁, k'₂} = {1, 2}`; the TA5(d)/T10a.8 argument of Case 5 gives different zero counts, routing to Case 4. Both non-root, strict nesting: Case 4 or Case 5 by zero count.

By induction, `U(d)` holds for all `d ≥ 0`; since every allocator has finite depth, GlobalUniqueness follows. ∎

*Corollary (Domain Disjointness).* For distinct allocators `A₁ ≠ A₂`, `dom(A₁) ∩ dom(A₂) = ∅`. A shared address would have been produced by two distinct allocation events yielding the same value, contradicting GlobalUniqueness. Each address value belongs to at most one allocator's domain, inducing a well-defined *owning allocator* per address value.

*Critical dependence on T10a.* Case 5 depends on T10a's constraint that sibling allocations use `k = 0`. If a parent could use `k > 0` for siblings, its outputs would have varying lengths, potentially matching a child's length. T10a's necessity proof shows `inc(t₁, 1)` produces a sibling that is a proper prefix of the next, violating T10's non-nesting precondition.

*Formal Contract:*
- *Preconditions:* `a, b ∈ T` produced by distinct allocation events — root initialization or `inc(t, k)` — within a system conforming to T10a. Each address has a producing allocator assigned by the event taxonomy: root base to root; `inc(t, 0)` output to the executing allocator; `inc(t, k')` with `k' > 0` output to the newly created child. The domain prefix of a non-root allocator `A` spawned by `c₀ = inc(t, k')` is `t`; every `a ∈ dom(A)` satisfies `t ≼ a`.
- *Depends:*
  - AllocatedSet (AllocatedSet) — allocation-event taxonomy grounding distinctness.
  - T9 (ForwardAllocation) — `allocated_before(a, b) ⟹ a < b`.
  - T1 (LexicographicOrder) — irreflexivity of `<`.
  - T10 (PartitionIndependence) — distinctness from non-nesting prefixes.
  - T10a (AllocatorDiscipline) — `inc(·, 0)`-only siblings; `k' ∈ {1, 2}`; per-parent uniqueness.
  - T10a.1 (UniformSiblingLength) — every sibling shares the allocator's base length.
  - T10a.3 (LengthSeparation) — descendants at depth `d ≥ 1` have length `≥ γ + d`.
  - T10a.4 (T4Preservation) — every domain prefix is T4-valid.
  - T10a.6 (DomainDisjointness) — for distinct allocators `X ≠ Y`, `dom(X) ∩ dom(Y) = ∅`. Consumed in exhaustiveness's `p₁ = p₂` routing: from the parents' domains containing the shared value, T10a.6 forces `P₁ = P₂` without invoking the inductive hypothesis.
  - T10a.8 (UniformSiblingZeroCount) — base zero count lifts to all siblings.
  - T3 (CanonicalRepresentation) — tumbler equality requires position-wise agreement.
  - T4 (HierarchicalParsing) — clause (iv) `t_{#t} ≠ 0` on T4-valid addresses.
  - TA5 (HierarchicalIncrement) — (b) agreement on `1 ≤ i ≤ #t`; (c) `#inc(t, 0) = #t` with single-position modification; (d) `#inc(t, k') = #t + k'` and zero-separator bookkeeping.
  - TA5-SigValid (TA5-SigValid) — `sig(cₙ) = #cₙ` for T4-valid `cₙ`.
  - Prefix (PrefixRelation) — ≼ definition and `p ≺ q ⟹ #p < #q`.
  - NAT-addcompat (NatAdditionOrderAndSuccessor) — left and right order compatibility.
  - NAT-cancel (NatAdditionCancellation) — right cancellation `n + m = p + m ⟹ n = p`.
  - NAT-order (NatStrictTotalOrder) — trichotomy, `≤` definition, transitivity, irreflexivity.
  - NAT-addassoc (NatAdditionAssociative) — `(m + n) + p = m + (n + p)`. Consumed in Case 5's sub-case `k'₁ > k'₂` (with `(k'₁, k'₂) = (2, 1)`): instantiated at `(m, n, p) = (#p₁, 1, 1)` to regroup `#p₁ + (1 + 1) = (#p₁ + 1) + 1`, which (combined with T4's *Numerals* definition `2 := 1 + 1`) identifies `#p₁ + 2 = (#p₁ + 1) + 1`, putting the equation `#p₁ + 2 = #p₂ + 1` into the form `(#p₁ + 1) + 1 = #p₂ + 1` so that NAT-cancel can fire on the trailing `+ 1` to yield `#p₂ = #p₁ + 1`.
- *Invariant:* For every pair of addresses `a, b` arising from distinct allocation events in any reachable system state: `a ≠ b`.
- *Postconditions:* (1) Domain Disjointness — for distinct `A₁ ≠ A₂`, `dom(A₁) ∩ dom(A₂) = ∅`. (2) Well-defined owning allocator — each address value belongs to at most one allocator's domain.
- *Proof structure:* Strong induction on allocator tree depth *d*. Claim `U(d)`: all pairs at depth ≤ *d* produce distinct outputs. Base (`d = 0`): sole root, Case 1. Step: Cases 1–5 are self-contained; the `p₁ = p₂` routing invokes T10a.6 (domain disjointness on the parent pair) to establish shared parentage, then applies T10a's per-parent uniqueness.

