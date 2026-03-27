# ASN-0034: Tumbler Algebra

*2026-03-13, revised 2026-03-19, 2026-03-21, 2026-03-25, 2026-03-26, 2026-03-26, 2026-03-26*

We wish to understand what algebraic structure the Xanadu addressing system must possess. The system assigns every entity a permanent address — a *tumbler* — and requires these addresses to support comparison, containment testing, arithmetic for span computation and position advancement, and coordination-free allocation across a global network. We seek the minimal set of abstract properties that any correct implementation must provide, deriving each from design requirements rather than from any particular representation.

The approach is: state what the system must guarantee, then discover what properties of the address algebra are necessary and sufficient for those guarantees. We begin with the carrier set and work outward.

Nelson conceived this system as "the tumbler line" — a flat linearization of a hierarchical tree, yielding a total order on all addresses. Gregory implemented it as fixed-width sign-magnitude arithmetic over 16-digit mantissas. Between these two accounts we find the abstract algebra: what must hold for any correct implementation, regardless of representation.


## The carrier set

A tumbler is a finite sequence of non-negative integers. We write `t = d₁.d₂. ... .dₙ` where each `dᵢ ∈ ℕ` and `n ≥ 1`. The set of all tumblers is **T**. Nelson describes each component as a "digit" with "no upper limit" — the term is misleading, since each "digit" is an arbitrary-precision natural number, not a single decimal digit. The variable-length encoding ("humber") ensures small values are compact and large values expand as needed.

This gives us our first property:

**T0 (Carrier-set definition).** `T = {d₁.d₂. ... .dₙ : each dᵢ ∈ ℕ, n ≥ 1}`. This is an axiom: we posit the carrier set by definition, not by derivation. The natural numbers ℕ are taken with their standard properties, including closure under successor and addition.

*Formal Contract:*
- *Axiom:* T is the set of all finite sequences over ℕ with length ≥ 1; ℕ is closed under successor and addition.

**T0(a) (Unbounded component values).** `(A t ∈ T, i : 1 ≤ i ≤ #t : (A M ∈ ℕ :: (E t' ∈ T :: t' agrees with t except t'.dᵢ > M)))`.

In words: for every tumbler and every component position, there exists a tumbler whose value at that position exceeds any given bound. The address space within any subtree is inexhaustible.

*Proof.* We establish the universal claim by exhibiting, for arbitrary `t`, `i`, and `M`, a witness `t'` with the required properties.

Let `t = d₁.d₂. ... .dₙ` be an arbitrary member of T, let `i` satisfy `1 ≤ i ≤ n`, and let `M ∈ ℕ` be an arbitrary bound. Define

> `t' = d₁. ... .dᵢ₋₁.(M + 1).dᵢ₊₁. ... .dₙ`

— the sequence obtained from `t` by replacing its `i`-th component with `M + 1` and leaving all other components unchanged. We must verify three things.

*(i)* `t' ∈ T`. The sequence `t'` has length `n ≥ 1`, and each of its components is a natural number: for `j ≠ i`, the component `dⱼ ∈ ℕ` by hypothesis on `t`; for `j = i`, the component is `M + 1`, which belongs to ℕ since ℕ is closed under successor. Since T is the set of all finite sequences over ℕ with length ≥ 1, we have `t' ∈ T`.

*(ii)* `t'` agrees with `t` at every position `j ≠ i`. This holds by construction: the components at positions `j ≠ i` are identical to those of `t`.

*(iii)* `t'.dᵢ > M`. By construction `t'.dᵢ = M + 1`, and `M + 1 > M` for all `M ∈ ℕ`.

Since `t`, `i`, and `M` were arbitrary, the universal claim holds. ∎

*Formal Contract:*
- *Preconditions:* `t ∈ T`, `1 ≤ i ≤ #t`, `M ∈ ℕ`.
- *Postconditions:* There exists `t' ∈ T` such that `t'.dⱼ = t.dⱼ` for all `j ≠ i` and `t'.dᵢ > M`.
- *Frame:* `#t' = #t`; all components at positions `j ≠ i` are identical to those of `t`.
- *Axiom:* T is the set of all finite sequences over ℕ with length ≥ 1; ℕ is closed under successor.

**T0(b) (Unbounded length).** `(A n ∈ ℕ : n ≥ 1 : (E t ∈ T :: #t ≥ n))`.

In words: there is no maximum tumbler length — for every bound, a tumbler of at least that length exists in T. The hierarchy has unlimited nesting depth. T0(b) follows from T's definition as the set of all finite sequences over ℕ — for any `n`, the constant sequence `[1, 1, ..., 1]` of length `n` is a member. We state it explicitly because it carries independent architectural weight: T0(a) ensures siblings within a level are inexhaustible, while T0(b) ensures levels themselves are inexhaustible.

*Proof.* We establish the universal claim by exhibiting, for arbitrary `n ≥ 1`, a witness `t ∈ T` with `#t ≥ n`.

Let `n ∈ ℕ` with `n ≥ 1` be arbitrary. Define

> `t = 1.1. ... .1` (n components)

— the constant sequence of `n` ones, that is, `t = d₁.d₂. ... .dₙ` with `dᵢ = 1` for all `1 ≤ i ≤ n`. We must verify two things.

*(i)* `t ∈ T`. The sequence `t` has length `n ≥ 1`, and each of its components is a natural number: `dᵢ = 1 ∈ ℕ` for all `1 ≤ i ≤ n`. Since T is the set of all finite sequences over ℕ with length ≥ 1, we have `t ∈ T`.

*(ii)* `#t ≥ n`. By construction `t` has exactly `n` components, so `#t = n`, and `n ≥ n` holds.

Since `n` was arbitrary, the universal claim holds. ∎

*Formal Contract:*
- *Preconditions:* `n ∈ ℕ`, `n ≥ 1`.
- *Postconditions:* There exists `t ∈ T` such that `#t ≥ n`.
- *Axiom:* T is the set of all finite sequences over ℕ with length ≥ 1; there is no upper bound on the length of a finite sequence.

T0 is what separates the tumbler design from fixed-width addressing. Nelson: "New items may be continually inserted in tumbler-space while the other addresses remain valid." The word "continually" carries the weight — it means the process of creating new addresses never terminates. Between any two sibling addresses, the forking mechanism can always create children: "One digit can become several by a forking or branching process. This consists of creating successive new digits to the right." Each daughter can have daughters without limit, and each digit is itself unbounded.

The address space is unbounded in two dimensions: T0(a) ensures each component is unbounded (unlimited siblings at any level) and T0(b) ensures the number of components is unbounded (unlimited nesting depth). Together they make the address space infinite in both dimensions, which Nelson calls "finite but unlimited" — at any moment finitely many addresses exist, but there is no bound on how many can be created: "A span that contains nothing today may at a later time contain a million documents."

We observe that Gregory's implementation uses a fixed 16-digit mantissa of 32-bit unsigned integers, giving a large but finite representable range. When the allocation primitive `tumblerincrement` would exceed this range structurally (requiring a 17th digit), it detects the overflow and terminates fatally. The general addition routine `tumbleradd` silently wraps on digit-value overflow. Both behaviors violate T0. The abstract specification demands unbounded components; a correct implementation must either provide them or demonstrate that the reachable state space never exercises the bound. The comment `NPLACES 16 /* increased from 11 to support deeper version chains */` records that the original bound of 11 was concretely hit in practice — version chains deeper than 3–4 levels caused fatal crashes.


## The total order

We require a total order on T. Nelson describes the "tumbler line" as a single linear sequence: "In a sense the tumbler line is like the real line, i.e., the line of integers and all the numbers in between." The system maps a hierarchical tree — servers containing accounts containing documents containing elements — onto this flat line via depth-first traversal. The traversal inherently produces a total order: for any two nodes in a tree, depth-first traversal visits one before the other. The ordering rule is lexicographic:

**T1 (Lexicographic order).** For tumblers `a = a₁. ... .aₘ` and `b = b₁. ... .bₙ`, define `a < b` iff there exists `k ≥ 1` such that `(A i : 1 ≤ i < k : aᵢ = bᵢ)` and either:

  (i) `k ≤ min(m, n)` and `aₖ < bₖ`, or

  (ii) `k = m + 1 ≤ n` (that is, `a` is a proper prefix of `b`).

The prefix convention — a prefix is less than any proper extension — is what makes depth-first traversal work. The server address `2` is less than every address within server `2`'s subtree, because every such address extends the prefix `2` with further components. This means server `2`'s subtree begins immediately after `2` in the order and extends until some address whose first component exceeds `2`.

*Dependencies:*
- **T0(a) (Carrier-set definition):** T is the set of all finite sequences over ℕ with length ≥ 1.
- **T3 (Canonical representation):** `a = b ⟺ #a = #b ∧ (A i : 1 ≤ i ≤ #a : aᵢ = bᵢ)`.

*Proof.* We show that `<` as defined is a strict total order on T by establishing irreflexivity, trichotomy, and transitivity. The argument relies on the corresponding properties of `<` on ℕ and on T3 (canonical representation).

*(a) Irreflexivity.* We must show: `(A a ∈ T :: ¬(a < a))`.

Suppose `a < a` for some `a ∈ T` with `#a = m`. Then there exists `k ≥ 1` with `aᵢ = aᵢ` for all `1 ≤ i < k` (vacuously satisfied) and either (i) `k ≤ m` and `aₖ < aₖ`, or (ii) `k = m + 1 ≤ m`. Case (i) requires `aₖ < aₖ`, violating irreflexivity of `<` on ℕ. Case (ii) requires `m + 1 ≤ m`, which is false. Both cases produce contradictions, so no witness `k` exists and `¬(a < a)`.

*(b) Trichotomy.* We must show: `(A a, b ∈ T :: exactly one of a < b, a = b, b < a)`.

Let `a, b ∈ T` with `#a = m` and `#b = n`. Define the *first divergence position* `k` as the least positive integer at which `a` and `b` disagree — either because `aₖ ≠ bₖ` at some `k ≤ min(m, n)`, or because one tumbler is exhausted at position `k = min(m, n) + 1` while the other continues. Three cases are exhaustive.

*Case 1: no divergence exists.* Then `m = n` and `aᵢ = bᵢ` for all `1 ≤ i ≤ m`, so `a = b` by T3. By part (a), `¬(a < a)` and `¬(a > a)`, giving equality as the unique outcome.

*Case 2: `k ≤ min(m, n)` and `aₖ ≠ bₖ`.* Since `aᵢ = bᵢ` for all `i < k` but `aₖ ≠ bₖ`, we have `a ≠ b`. By trichotomy on ℕ, exactly one of `aₖ < bₖ` or `bₖ < aₖ` holds. If `aₖ < bₖ`, then `k` witnesses `a < b` via T1 case (i); if `bₖ < aₖ`, then `k` witnesses `b < a` via T1 case (i). We confirm that no witness establishes the reverse. Any witness `k'` for the opposite ordering requires `aᵢ = bᵢ` for all `i < k'`. If `k' > k`, this fails at position `k` where `aₖ ≠ bₖ`. If `k' = k`, case (i) requires the opposite inequality at position `k`, contradicting ℕ-trichotomy, and case (ii) requires `k = n + 1` (or `k = m + 1`), contradicting `k ≤ min(m, n) ≤ n` (respectively `≤ m`). If `k' < k`, the minimality of `k` gives `a_{k'} = b_{k'}`, so case (i) fails on equal components and case (ii) requires `k' = n + 1` (or `m + 1`), but `k' < k ≤ min(m, n)` gives `k' < n` and `k' < m`, contradicting both. No witness exists; exactly one ordering holds.

*Case 3: `k = min(m, n) + 1` — all shared positions agree but `m ≠ n`.* Since `aᵢ = bᵢ` for all `1 ≤ i ≤ min(m, n)` but `m ≠ n`, we have `a ≠ b` by T3 (distinct lengths). If `m < n`, then `k = m + 1 ≤ n`, so `a` is a proper prefix of `b` and `k` witnesses `a < b` via T1 case (ii). No witness for `b < a` exists: case (i) would require `bⱼ < aⱼ` at some position `j ≤ min(m, n)`, but all such positions have equal components; case (ii) would require `b` to be a proper prefix of `a`, i.e., `n < m`, contradicting `m < n`. If `m > n`, then `k = n + 1 ≤ m`, so `b` is a proper prefix of `a` and `k` witnesses `b < a` via T1 case (ii). No witness for `a < b` exists: case (i) would require `aⱼ < bⱼ` at some position `j ≤ min(m, n)`, but all such positions have equal components; case (ii) would require `m + 1 ≤ n`, contradicting `m > n`.

These three cases partition all pairs in `T × T`, and in each case exactly one of the three relations holds.

*(c) Transitivity.* We must show: `(A a, b, c ∈ T : a < b ∧ b < c : a < c)`.

Let `k₁` witness `a < b` and `k₂` witness `b < c`, with `#a = m`, `#b = n`, `#c = p`. For all `i < min(k₁, k₂)`, the agreement conditions of the two hypotheses give `aᵢ = bᵢ` (since `i < k₁`) and `bᵢ = cᵢ` (since `i < k₂`), hence `aᵢ = cᵢ` by transitivity of equality. We produce a witness for `a < c` by case analysis on the relationship between `k₁` and `k₂`.

*Case k₁ < k₂.* Position `k₁` lies in the agreement range of `b < c`, so `bₖ₁ = cₖ₁`. If `a < b` via case (i): `aₖ₁ < bₖ₁` with `k₁ ≤ min(m, n)`, and since `bₖ₁ = cₖ₁` we have `aₖ₁ < cₖ₁`; the existence of `cₖ₁` gives `k₁ ≤ p`, so `k₁ ≤ min(m, p)`, and position `k₁` witnesses `a < c` via T1 case (i). If `a < b` via case (ii): `k₁ = m + 1 ≤ n`, and since `bₖ₁ = cₖ₁` the component `cₖ₁` exists, giving `p ≥ k₁ = m + 1`; thus `a` is a proper prefix of `c` and `k₁` witnesses `a < c` via T1 case (ii).

*Case k₂ < k₁.* Position `k₂` lies in the agreement range of `a < b`, so `aₖ₂ = bₖ₂`. We first show `b < c` must be via case (i). If `b < c` were via case (ii), then `k₂ = n + 1`. But `a < b` requires `k₁ ≤ n` — in case (i), `k₁ ≤ min(m, n) ≤ n`; in case (ii), `k₁ = m + 1 ≤ n` — so `k₂ = n + 1 > n ≥ k₁`, contradicting `k₂ < k₁`. Therefore `b < c` is via case (i): `bₖ₂ < cₖ₂` with `k₂ ≤ min(n, p)`. Since `k₂ < k₁` and `a` has components at all positions below `k₁`, we have `k₂ ≤ m`, giving `aₖ₂ = bₖ₂ < cₖ₂` with `k₂ ≤ min(m, p)`. Position `k₂` witnesses `a < c` via T1 case (i).

*Case k₁ = k₂ = k.* Both divergences occur at position `k`, and we have `aᵢ = cᵢ` for all `i < k`. The two-case structure of T1 gives four combinations for the pair of witnesses; we show that exactly two are realizable.

*Sub-case (i, i):* `aₖ < bₖ` with `k ≤ min(m, n)` and `bₖ < cₖ` with `k ≤ min(n, p)`. Transitivity of `<` on ℕ gives `aₖ < cₖ`. Since `k ≤ m` and `k ≤ p`, we have `k ≤ min(m, p)`, and position `k` witnesses `a < c` via T1 case (i).

*Sub-case (ii, i):* `k = m + 1 ≤ n` and `bₖ < cₖ` with `k ≤ min(n, p)`. The bound `k ≤ p` gives `m + 1 = k ≤ p`, so `a` is a proper prefix of `c` and position `k` witnesses `a < c` via T1 case (ii).

*Sub-case (i, ii):* `aₖ < bₖ` with `k ≤ min(m, n)` requires `k ≤ n`, while `k = n + 1 ≤ p` requires `k > n`. The conjunction `k ≤ n` and `k > n` is a contradiction; this sub-case cannot arise.

*Sub-case (ii, ii):* `k = m + 1 ≤ n` and `k = n + 1 ≤ p`. Then `m + 1 = n + 1`, hence `m = n`. But the first condition requires `m + 1 ≤ n`, i.e., `m < n`, contradicting `m = n`. This sub-case cannot arise.

In every realizable combination, a witness for `a < c` under T1 is produced. ∎

*Formal Contract:*
- *Definition:* `a < b` iff `∃ k ≥ 1` with `(A i : 1 ≤ i < k : aᵢ = bᵢ)` and either (i) `k ≤ min(m,n) ∧ aₖ < bₖ`, or (ii) `k = m+1 ≤ n`.
- *Postconditions:* (a) Irreflexivity — `(A a ∈ T :: ¬(a < a))`. (b) Trichotomy — `(A a,b ∈ T :: exactly one of a < b, a = b, b < a)`. (c) Transitivity — `(A a,b,c ∈ T : a < b ∧ b < c : a < c)`.

Nelson's assertion that the tumbler line is total — that two addresses are never incomparable — is architecturally load-bearing. Spans are defined as contiguous regions on the tumbler line: "A span in the tumbler line, represented by two tumblers, refers to a subtree of the entire docuverse." If two addresses were incomparable, the interval between them would be undefined, and the entire machinery of span-sets, link endsets, and content reference would collapse.

Nelson requires that comparison be self-contained — no index consultation needed:

**T2 (Intrinsic comparison).** The order relation T1 is computable from the two tumblers alone, without consulting any external data structure. The comparison examines at most `min(#a, #b)` component pairs.

*Dependencies:*
- **T1 (Lexicographic order):** Defines `a < b` via witness position `k` with agreement below and either component divergence or prefix exhaustion at `k`.
- **T3 (Canonical representation):** Tumbler equality is sequence equality — same length and same components at every position.

*Proof.* We establish two claims: (1) the ordering among `a` and `b` under T1 is decidable from the components and lengths of the two tumblers alone, with no external data, and (2) the number of component pairs examined is at most `min(#a, #b)`.

Let `a = a₁. ... .aₘ` and `b = b₁. ... .bₙ`. The definition of `<` in T1 requires a witness position `k ≥ 1` satisfying `(A i : 1 ≤ i < k : aᵢ = bᵢ)` and either (i) `k ≤ min(m, n) ∧ aₖ < bₖ`, or (ii) `k = m + 1 ≤ n`. We construct a deterministic procedure that decides the ordering by scanning positions `i = 1, 2, ...` and examining the pair `(aᵢ, bᵢ)` at each, then count the pairs examined and inventory the data consulted.

*Case 1: divergence at some position `k ≤ min(m, n)`.* The scan finds a position `k` where `aₖ ≠ bₖ`, having verified `aᵢ = bᵢ` for all `1 ≤ i < k`. Exactly `k` component pairs are examined. Since `k ≤ min(m, n)`, the bound `k ≤ min(#a, #b)` holds. By trichotomy on ℕ, exactly one of `aₖ < bₖ` or `bₖ < aₖ` holds. If `aₖ < bₖ`, then `k` witnesses `a < b` via T1 case (i), since `k ≤ min(m, n)` and the agreement condition holds for all `i < k`. If `bₖ < aₖ`, then `k` witnesses `b < a` via T1 case (i) by the same reasoning with roles exchanged. The values consulted are `a₁, ..., aₖ` and `b₁, ..., bₖ` — all components of the input tumblers.

*Case 2: no divergence within the shared range.* The scan exhausts all `min(m, n)` positions with `aᵢ = bᵢ` at every position `1 ≤ i ≤ min(m, n)`. Exactly `min(m, n)` component pairs are examined, satisfying the bound. Three sub-cases determine the ordering:

- If `m < n`: position `k = m + 1` satisfies `k ≤ n` and the agreement condition `aᵢ = bᵢ` for all `1 ≤ i < k = m + 1`, i.e., for all `1 ≤ i ≤ m`. So `k` witnesses `a < b` via T1 case (ii).
- If `n < m`: position `k = n + 1` satisfies `k ≤ m` and the agreement condition for all `1 ≤ i ≤ n`. So `k` witnesses `b < a` via T1 case (ii).
- If `m = n`: the tumblers have the same length and agree at every position, so `a = b` by T3.

The sub-case decision consults only the lengths `m = #a` and `n = #b`, both intrinsic to the tumblers.

These two cases are exhaustive: either some position in `{1, ..., min(m, n)}` has `aₖ ≠ bₖ`, or none does.

*Claim (2).* In Case 1, exactly `k ≤ min(m, n) = min(#a, #b)` pairs are examined. In Case 2, exactly `min(m, n) = min(#a, #b)` pairs are examined. In both cases the count is at most `min(#a, #b)`.

*Claim (1).* We inventory every value the procedure consults: the components `aᵢ` and `bᵢ` at each scanned position (extracted from `a` and `b` by index), and the lengths `m` and `n` (properties of the sequences themselves). The definition of `<` in T1 is expressed entirely in terms of these values. No tree structure, no index, no auxiliary mapping, and no external state participates in the decision. The comparison is a pure function of its two tumbler arguments. ∎

The importance of T2 is operational: span containment tests, link search, and index traversal all reduce to tumbler comparison. If comparison required a lookup, these operations would depend on auxiliary state, and the system's decentralization guarantee would collapse — one could not determine whether an address falls within a span without access to the index that manages that span.

Gregory's implementation confirms T2. The comparison function `tumblercmp` delegates to `abscmp`, which performs a purely positional comparison: exponent first (a proxy for the number of leading zeros), then lexicographic mantissa slot-by-slot. No tree structure, no index, no external state is consulted.

*Formal Contract:*
- *Preconditions:* `a, b ∈ T` — two well-formed tumblers (finite sequences over ℕ with `#a ≥ 1` and `#b ≥ 1`, per T0).
- *Postconditions:* (a) The ordering among `a` and `b` under T1 is determined. (b) At most `min(#a, #b)` component pairs are examined. (c) The only values consulted are `{aᵢ : 1 ≤ i ≤ #a}`, `{bᵢ : 1 ≤ i ≤ #b}`, `#a`, and `#b`.
- *Frame:* No external data structure is read or modified — the comparison is a pure function of the two tumblers.


## Canonical form

Equality of tumblers must mean component-wise identity. There must be no representation in which two distinct sequences of components denote the same abstract tumbler:

**T3 (Canonical representation).** `(A a, b ∈ T : a₁ = b₁ ∧ ... ∧ aₙ = bₙ ∧ #a = #b ≡ a = b)`.

If two tumblers have the same length and the same components at every position, they are the same tumbler. Conversely, if they differ in any component or in length, they are distinct. No normalization, no trailing-zero ambiguity, no exponent variation can create aliases.

Address identity is load-bearing. If two representations could denote the same tumbler, equality tests might give false negatives, span containment checks might fail for addresses that should match, and the system might allocate a "new" address that is actually an alias for an existing one. Gregory's implementation achieves T3 through a normalization routine (`tumblerjustify`) that shifts leading zeros out of the mantissa and adjusts the exponent. When T3 is violated — when an unnormalized tumbler with a leading zero reaches the comparison function — `iszerotumbler` checks only the first mantissa slot and misclassifies the tumbler as zero. Two logically positive tumblers with different values both compare as EQUAL to each other and to the genuine zero tumbler, breaking transitivity of the total order. T3, maintained by normalization after every arithmetic operation, prevents this corruption.

*Dependencies:*
- **T0(a) (Carrier-set definition):** T is the set of all finite sequences over ℕ with length ≥ 1. A tumbler *is* its component sequence; no quotient, equivalence relation, or normalization map is imposed on T beyond sequence identity.

*Proof.* T3 asserts that tumbler equality coincides with extensional sequence equality. We derive this from T0(a)'s characterisation of the carrier set: T is the set of all finite sequences over ℕ with length ≥ 1, and a tumbler *is* its component sequence. There is no separate abstract value that a sequence "represents," no quotient by an equivalence relation, no normalization map whose image is the "true" tumbler. The biconditional to establish is `#a = #b ∧ (A i : 1 ≤ i ≤ #a : aᵢ = bᵢ) ≡ a = b`. We verify both directions.

*Forward direction.* Let `a, b ∈ T` and suppose `#a = #b = n` and `aᵢ = bᵢ` for all `1 ≤ i ≤ n`. We must show `a = b`. By T0(a), `a` and `b` are finite sequences over ℕ. Two finite sequences over the same domain are equal when they have the same length and agree at every index — this is the extensional definition of sequence equality. The hypotheses supply both conditions: `#a = #b = n` and `aᵢ = bᵢ` for every `i` in `{1, ..., n}`. Therefore `a = b`.

*Reverse direction.* Let `a, b ∈ T` and suppose `a = b`. We must show `#a = #b` and `aᵢ = bᵢ` for all `1 ≤ i ≤ #a`. By Leibniz's law (the indiscernibility of identicals), every property of `a` is a property of `b`. The length function `#·` is well-defined on T, so `#a = #b`. The component projection `·ᵢ` at each position `i` with `1 ≤ i ≤ #a` is well-defined on T, so `aᵢ = bᵢ`. Both conclusions follow from applying well-defined functions to equal arguments.

The force of T3 as a design commitment is the decision that no additional identification is imposed on T — the algebra does not quotient by trailing zeros (so `[1, 2]` and `[1, 2, 0]` are distinct tumblers), does not identify sequences that differ only in exponent representation (an implementation concern, not an abstract one), and does not collapse addresses that happen to denote the same logical entity under some external interpretation. The abstract tumbler *is* the sequence, nothing more and nothing less. ∎

*Formal Contract:*
- *Postconditions:* Tumbler equality is sequence equality: `a = b ⟺ #a = #b ∧ (A i : 1 ≤ i ≤ #a : aᵢ = bᵢ)`.
- *Frame:* No quotient, normalization, or external identification is imposed on T. Trailing zeros are significant: `[1, 2] ≠ [1, 2, 0]`.


## Hierarchical structure

Tumblers encode a containment hierarchy. Nelson uses zero-valued components as structural delimiters:

> "There are four major fields, each expandable indefinitely, with three major dividers between them. These fields are Server, User, Document and Contents."

> "A tumbler address may have at most three zero digits... These are interpreted as the major dividers, and have lexical significance as punctuation."

We formalize this. Define a *field separator* as a component with value zero. An address tumbler has the form:

`t = N₁. ... .Nₐ . 0 . U₁. ... .Uᵦ . 0 . D₁. ... .Dᵧ . 0 . E₁. ... .Eδ`

where each `Nᵢ, Uⱼ, Dₖ, Eₗ > 0`. The four fields are:

- **Node field** `N₁. ... .Nₐ`: identifies the server. "The server address always begins with the digit 1, since all other servers are descended from it."
- **User field** `U₁. ... .Uᵦ`: identifies the account. "Typically, the user will have no control over the node address he, she or it is assigned; but once assigned a User account, the user will have full control over its subdivision forevermore."
- **Document field** `D₁. ... .Dᵧ`: identifies the document and version. Nelson notes the boundary between base document and version is not syntactically marked — "the version, or subdocument number is only an accidental extension of the document number, and strictly implies no specific relationship of derivation."
- **Element field** `E₁. ... .Eδ`: identifies the content element. The first component distinguishes the *subspace*: 1 for text content, 2 for links.

Not every tumbler need have all four fields. A tumbler with zero zeros addresses a node. One zero: a user account. Two zeros: a document. Three zeros: an element. The count of zero-valued components determines the specificity level.

**T4 (Hierarchical parsing).** Every tumbler `t ∈ T` used as an address contains at most three zero-valued components, appearing in order as field separators, every non-separator component is strictly positive, and every field present in the address has at least one component. Formally, if `t = N₁. ... .Nₐ . 0 . U₁. ... .Uᵦ . 0 . D₁. ... .Dᵧ . 0 . E₁. ... .Eδ`, then `(A i : 1 ≤ i ≤ α : Nᵢ > 0)`, `(A j : 1 ≤ j ≤ β : Uⱼ > 0)`, `(A k : 1 ≤ k ≤ γ : Dₖ > 0)`, `(A l : 1 ≤ l ≤ δ : Eₗ > 0)`, and `α ≥ 1`, `β ≥ 1` when present, `γ ≥ 1` when present, `δ ≥ 1` when present. We call this the *positive-component constraint*: every component of every field is strictly positive. The non-empty field constraint — each present field has at least one component — is equivalent to three syntactic conditions on the raw tumbler: no two zeros are adjacent, the tumbler does not begin with zero, and the tumbler does not end with zero. These conditions ensure that every zero genuinely separates two non-empty fields. Without the non-empty field constraint, a tumbler like `[1, 0, 0, 3]` would have `zeros = 2`, classifying it as a document address with an empty user field — the positive-component constraint holds vacuously on the empty field, but the parse is degenerate. The function `fields(t)` that extracts the node, user, document, and element fields is well-defined and computable from `t` alone. Define `zeros(t) = #{i : 1 ≤ i ≤ #t ∧ tᵢ = 0}`. The count of zero-valued components uniquely determines the hierarchical level:

  - `zeros(t) = 0`: `t` is a node address (node field only),
  - `zeros(t) = 1`: `t` is a user address (node and user fields),
  - `zeros(t) = 2`: `t` is a document address (node, user, and document fields),
  - `zeros(t) = 3`: `t` is an element address (all four fields).

This correspondence is injective on levels: each level produces addresses with exactly one zero count, and each zero count corresponds to exactly one level. The correspondence depends on the positive-component constraint — zero components serve exclusively as field separators *because* no field component is zero. Without the positivity constraint, a tumbler like `[1, 0, 0, 3]` would have two zero-valued components but ambiguous parse: the second zero could be a separator or a zero-valued component within the user field. Since field components are strictly positive, zeros appear only as separators, the number of separators determines the number of fields, and the parse is unique.

A subtlety deserves emphasis: the hierarchy is *convention layered over flat arithmetic*, not enforcement by the algebra. Gregory's analysis reveals that the comparison, addition, subtraction, and increment operations treat every mantissa slot identically. There is no `isparent`, `isancestor`, or `ischild` primitive in the arithmetic layer. The algebra operates on flat sequences of non-negative integers; the hierarchical interpretation is projected onto those sequences by the allocation machinery and the field-parsing function `fields(t)`. This is a deliberate design choice. The arithmetic layer is kept flat so that comparison and span computation are simple, uniform operations with no parsing of semantic structure.

Hierarchy is constructed by the allocation machinery, not by the algebra. The `.0.` separator is produced when the allocation `depth` parameter equals 2 — creating a child at a *different hierarchical type* than its parent (e.g., an ACCOUNT creating a DOCUMENT). When creating a same-type child (DOCUMENT creating DOCUMENT = versioning), `depth = 1`, and no zero separator is introduced. Gregory confirms: there was even a bug where the first document under an account failed to receive its `.0.` separator — the convention had to be explicitly constructed by the allocator, not enforced by any algebraic invariant.

*Dependencies:*
- **T3 (Canonical representation):** `a = b ⟺ #a = #b ∧ (A i : 1 ≤ i ≤ #a : aᵢ = bᵢ)`. Used to establish that the component values of `t` are determinate — `tᵢ` is well-defined for each position — so that scanning for zeros is unambiguous.

**Verification of T4.** T4 is an axiom: it constrains which tumblers the system admits as valid addresses. We verify three consequences that follow from these constraints. The argument uses only T3 (canonical representation) and the T4 constraints themselves; no other properties are required.

*(a) Syntactic equivalence of the non-empty field constraint.* We prove that the non-empty field constraint — each present field has at least one component — is equivalent to three syntactic conditions on the raw tumbler: (i) no two zeros are adjacent, (ii) `t₁ ≠ 0`, (iii) `t_{#t} ≠ 0`.

*Forward.* Assume every present field has at least one component, and that the positive-component constraint holds (every field component is strictly positive). We derive each syntactic condition separately.

*Condition (ii): `t₁ ≠ 0`.* The first component `t₁` belongs to the node field. The node field is always present with `α ≥ 1` components, so `t₁ = N₁`. By the positive-component constraint, `N₁ > 0`, hence `t₁ ≠ 0`.

*Condition (iii): `t_{#t} ≠ 0`.* The last component `t_{#t}` belongs to the last present field — the node field if `zeros(t) = 0`, the user field if `zeros(t) = 1`, the document field if `zeros(t) = 2`, or the element field if `zeros(t) = 3`. In each case, that field has at least one component by the non-empty field constraint, and its last component is strictly positive by the positive-component constraint. Hence `t_{#t} > 0`, so `t_{#t} ≠ 0`.

*Condition (i): no adjacent zeros.* Suppose for contradiction that `tᵢ = 0` and `tᵢ₊₁ = 0` for some position `i` with `1 ≤ i < #t`. Under T4, every zero-valued component is a field separator. Two consecutive separators at positions `i` and `i + 1` would bound a field segment containing zero components — an empty field. This contradicts the non-empty field constraint. Hence no two zeros are adjacent.

*Reverse.* Assume (i), (ii), and (iii) hold. We must show that every present field has at least one component. The fields of `t` are the maximal contiguous sub-sequences between consecutive separator zeros — the first field runs from position 1 to the first zero minus one, interior fields run between consecutive zeros, and the last field runs from the last zero plus one to position `#t`. We verify non-emptiness for each kind of field.

*First field (node).* By (ii), `t₁ ≠ 0`, so position 1 is not a separator. If `zeros(t) = 0`, the node field spans all of `t` and has `#t ≥ 1` components. If `zeros(t) ≥ 1`, let `j₁` be the position of the first zero. Then `j₁ ≥ 2` (since `t₁ ≠ 0`), and the node field occupies positions `1` through `j₁ - 1` — a segment of `j₁ - 1 ≥ 1` components.

*Last field.* By (iii), `t_{#t} ≠ 0`, so position `#t` is not a separator. If `zeros(t) = 0`, this is the node field, already handled. If `zeros(t) ≥ 1`, let `j_s` be the position of the last zero. Then `j_s ≤ #t - 1` (since `t_{#t} ≠ 0`), and the last field occupies positions `j_s + 1` through `#t` — a segment of `#t - j_s ≥ 1` components.

*Interior fields.* Consider two consecutive separator zeros at positions `j` and `j'` with `j < j'` and no separator between them. By (i), no two zeros are adjacent, so `j' ≥ j + 2`. The segment from position `j + 1` to position `j' - 1` therefore contains at least one position: `j' - 1 ≥ j + 1`. Every position in this segment lies strictly between consecutive separators and is therefore a field component, not a separator. The interior field has at least one component.

All fields have at least one component.

*(b) Unique parse.* We prove that under the T4 constraints, `fields(t)` — the decomposition of `t` into node, user, document, and element fields — is well-defined and uniquely determined by `t` alone.

The argument turns on a single observation: the positive-component constraint makes the separator positions exactly recoverable. A position `i` satisfies `tᵢ = 0` if and only if `i` is a field separator. The forward direction: every separator has value 0 by the definition of the field decomposition — separators are the zero-valued components that delimit fields. The reverse direction: if `tᵢ = 0`, then `i` must be a separator, because no field component can be zero (every field component is strictly positive by the positive-component constraint). Therefore `{i : 1 ≤ i ≤ #t ∧ tᵢ = 0}` is exactly the set of separator positions — computable by a single scan of `t`.

Given the separator positions, the fields are the maximal contiguous sub-sequences between them: the node field runs from position 1 to the first separator minus one, the user field from the first separator plus one to the second separator minus one, and so on. By part (a), each sub-sequence is non-empty. The separator positions are uniquely determined by `t` — by T3, the component values are determinate, so the set `{i : tᵢ = 0}` is determinate — and the field boundaries follow uniquely. Two distinct decompositions would require two distinct sets of separator positions, but there is only one such set. Therefore `fields(t)` is well-defined and unique.

*(c) Level determination.* We prove that `zeros(t)` uniquely determines the hierarchical level, and the mapping is a bijection on `{0, 1, 2, 3}`.

Define `zeros(t) = #{i : 1 ≤ i ≤ #t ∧ tᵢ = 0}`. By T4, valid address tumblers have at most three zero-valued components, so `zeros(t) ∈ {0, 1, 2, 3}`. By part (b), every zero in `t` is a field separator and every separator is a zero. Therefore `zeros(t)` counts exactly the number of field separators, and the number of fields present equals `zeros(t) + 1`.

The mapping from zero count to hierarchical level is defined by the number of fields:

  - `zeros(t) = 0` → 1 field (node only) → node address,
  - `zeros(t) = 1` → 2 fields (node, user) → user address,
  - `zeros(t) = 2` → 3 fields (node, user, document) → document address,
  - `zeros(t) = 3` → 4 fields (node, user, document, element) → element address.

Injectivity: the function `z ↦ z + 1` is injective on ℕ, so distinct zero counts produce distinct field counts, hence distinct levels. If `zeros(a) ≠ zeros(b)`, then `a` and `b` belong to different hierarchical levels. Surjectivity: each of the four levels is realized — `zeros(t) = 0, 1, 2, 3` are all values permitted by T4, and each corresponds to exactly one level. The mapping is therefore bijective on `{0, 1, 2, 3}`.

We note the essential role of the positive-component constraint in this result. Without it, a tumbler `[1, 0, 0, 3]` would have `zeros(t) = 2`, classifying it as a document address with three fields: `[1]`, `[]`, `[3]`. But the second zero is ambiguous — it could be a separator (giving an empty user field) or a zero-valued component within the user field (giving two fields: `[1]`, `[0, 3]`). The positive-component constraint eliminates the second interpretation: no field component can be zero, so every zero is unambiguously a separator, and the parse is unique. ∎

*Formal Contract:*
- *Axiom:* Valid address tumblers satisfy `zeros(t) ≤ 3`, `(A i : 1 ≤ i ≤ #t ∧ tᵢ ≠ 0 : tᵢ > 0)`, no adjacent zeros, `t₁ ≠ 0`, `t_{#t} ≠ 0`.
- *Definition:* `zeros(t) = #{i : 1 ≤ i ≤ #t ∧ tᵢ = 0}`; `fields(t)` decomposes `t` into node, user, document, and element fields by partitioning at the zero-valued separator positions.
- *Postconditions:* (a) The non-empty field constraint is equivalent to three syntactic conditions: no adjacent zeros, `t₁ ≠ 0`, `t_{#t} ≠ 0`. (b) `fields(t)` is well-defined and uniquely determined by `t` alone. (c) `zeros(t)` determines the hierarchical level bijectively on `{0, 1, 2, 3}`.


## Contiguous subtrees

T4, combined with the total order T1, gives us the property that makes spans work:

**T5 (Contiguous subtrees).** For any tumbler prefix `p`, the set `{t ∈ T : p ≼ t}` (where `≼` denotes "is a prefix of") forms a contiguous interval under T1:

  `[p ≼ a ∧ p ≼ c ∧ a ≤ b ≤ c ⟹ p ≼ b]`

*Dependencies:*
- **T1 (Lexicographic order):** Defines `<` on T. Case (i): first divergence `k ≤ min(#a, #b)` with `aₖ < bₖ`. Case (ii): `a` is a proper prefix of `b`. Used to derive contradictions from ordering violations.
- **T3 (Canonical representation):** `a = b ⟺ #a = #b ∧ (A i : 1 ≤ i ≤ #a : aᵢ = bᵢ)`. Distinct lengths entail distinct tumblers. Used in Case 2 to force strict inequality.

*Proof.* We must show that the set of all tumblers sharing a common prefix is contiguous under the lexicographic order T1 — no tumbler from outside the subtree can interleave between two members.

Let `p` be a tumbler prefix with `#p ≥ 1`, let `a, b, c ∈ T` with `p ≼ a`, `p ≼ c`, and `a ≤ b ≤ c` under T1. We must show `p ≼ b`.

Since `p ≼ a`, the tumbler `a` agrees with `p` on its first `#p` components: `(A i : 1 ≤ i ≤ #p : aᵢ = pᵢ)`, and `#a ≥ #p`. Likewise `p ≼ c` gives `(A i : 1 ≤ i ≤ #p : cᵢ = pᵢ)` and `#c ≥ #p`. We proceed by case analysis on the length of `b`.

*Case 1: `#b ≥ #p`.* We show that `b` agrees with `p` at every position `1 ≤ i ≤ #p`, which is exactly `p ≼ b`.

Suppose, for contradiction, that `b` diverges from `p` at some position. Let `k` be the least index in `{1, ..., #p}` with `bₖ ≠ pₖ`, so `bᵢ = pᵢ` for all `1 ≤ i < k`. Since `bₖ ≠ pₖ`, exactly one of `bₖ < pₖ` or `bₖ > pₖ` holds.

*Subcase 1a: `bₖ < pₖ`.* Since `p ≼ a`, we have `aₖ = pₖ`, so `bₖ < aₖ`. For all `i < k`, we established `bᵢ = pᵢ`, and since `p ≼ a` gives `aᵢ = pᵢ`, we have `aᵢ = bᵢ` for all `i < k`. Position `k` is therefore the first divergence between `a` and `b`, with `bₖ < aₖ`, and `k ≤ #p ≤ min(#a, #b)`. By T1 case (i), `b < a`. This contradicts `a ≤ b`.

*Subcase 1b: `bₖ > pₖ`.* Since `p ≼ c`, we have `cₖ = pₖ`, so `bₖ > cₖ`. For all `i < k`, `bᵢ = pᵢ = cᵢ`, so `b` and `c` agree on all positions before `k`, and `k ≤ #p ≤ min(#b, #c)`. By T1 case (i), `c < b`. This contradicts `b ≤ c`.

Both subcases yield contradictions, so no divergence position `k` exists. Therefore `bᵢ = pᵢ` for all `1 ≤ i ≤ #p`, which gives `p ≼ b`.

*Case 2: `#b < #p`.* We derive a contradiction, showing this case is impossible — no tumbler shorter than `p` can lie between two tumblers that extend `p`.

From `p ≼ a` we have `#a ≥ #p > #b`, so `a` is strictly longer than `b`. We examine the hypothesis `a ≤ b`. Since `#a > #b`, `a` cannot equal `b` (by T3, distinct lengths imply distinct tumblers), and `a` cannot be a proper prefix of `b` (since `#a > #b`). Therefore `a ≤ b` requires `a < b`, which by T1 requires a witness `k ≥ 1` with `aᵢ = bᵢ` for all `i < k` and either: (i) `k ≤ min(#a, #b) = #b` and `aₖ < bₖ`, or (ii) `k = #a + 1 ≤ #b`. Case (ii) requires `#a + 1 ≤ #b`, that is `#a < #b`, contradicting `#a > #b`. So case (i) must hold: there exists `k ≤ #b` with `aᵢ = bᵢ` for all `1 ≤ i < k` and `aₖ < bₖ`.

Since `k ≤ #b < #p ≤ #a`, position `k` lies within the prefix `p`, so `aₖ = pₖ` (from `p ≼ a`). Therefore `bₖ > aₖ = pₖ`. Likewise, since `k < #p ≤ #c`, we have `cₖ = pₖ` (from `p ≼ c`), so `bₖ > pₖ = cₖ`.

Now we compare `b` and `c` at position `k`. For all `i < k`: the witness condition gives `bᵢ = aᵢ`, and `p ≼ a` with `i < k < #p` gives `aᵢ = pᵢ`, and `p ≼ c` with `i < #p` gives `cᵢ = pᵢ`, so `bᵢ = cᵢ`. At position `k`, we have `bₖ > cₖ`, and `k ≤ #b` and `k < #p ≤ #c`, so `k ≤ min(#b, #c)`. By T1 case (i), `c < b`. This contradicts `b ≤ c`.

Since Case 2 is impossible, Case 1 is the only possibility, and we have established `p ≼ b` in all cases. ∎

*Formal Contract:*
- *Definition:* `p ≼ t ⟺ #t ≥ #p ∧ (A i : 1 ≤ i ≤ #p : tᵢ = pᵢ)` — the tumbler `t` extends the prefix `p`.
- *Preconditions:* `a, b, c ∈ T`; `p` is a tumbler prefix with `#p ≥ 1`; `p ≼ a`; `p ≼ c`; `a ≤ b ≤ c` under the lexicographic order T1.
- *Postconditions:* `p ≼ b` — the tumbler `b` extends the prefix `p`, and therefore belongs to the same subtree as `a` and `c`.

This is Nelson's key insight: "The first point of a span may designate a server, an account, a document or an element; so may the last point. There is no choice as to what lies between; this is implicit in the choice of first and last point." T5 is what makes this true. A span between two endpoints under the same prefix captures exactly the addresses under that prefix between those endpoints — no addresses from unrelated subtrees can interleave.

Because the hierarchy is projected onto a flat line (T1), containment in the tree corresponds to contiguity on the line. Nelson: "A span may be visualized as a zone hanging down from the tumbler line — what is called in computer parlance a depth-first spanning tree." Every subtree maps to a contiguous range, and every contiguous range within a subtree stays within the subtree.


## Decidable containment

The total order T1 determines *sequence* (which address comes first). But the system also needs *containment* — does address `a` belong to account `b`? Is document `d₁` under the same server as document `d₂`? These are not ordering questions; they are prefix questions.

**T6 (Decidable containment).** For any two tumblers `a, b ∈ T`, the following are decidable from the addresses alone:

  (a) Whether `a` and `b` share the same node field.

  (b) Whether `a` and `b` share the same node and user fields.

  (c) Whether `a` and `b` share the same node, user, and document-lineage fields.

  (d) Whether the document field of `a` is a prefix of the document field of `b` (structural subordination within a document family).

*Dependencies:*
- **T3 (Canonical representation):** `a = b ⟺ #a = #b ∧ (A i : 1 ≤ i ≤ #a : aᵢ = bᵢ)`. Two finite sequences are equal iff they have the same length and agree componentwise. Used to establish that equality of finite sequences of natural numbers is decidable in finitely many steps.
- **T4 (Hierarchical parsing):** Valid address tumblers have at most three zero-valued components, every non-separator component is strictly positive, no adjacent zeros, no leading or trailing zero. (a) Non-empty field constraint. (b) `fields(t)` is well-defined and uniquely determined by `t` alone. (c) `zeros(t)` determines hierarchical level bijectively on `{0, 1, 2, 3}`. Used for field extraction and field-presence determination.

*Proof.* We show that each of (a)–(d) admits a terminating decision procedure whose only inputs are the tumbler representations of `a` and `b`. The argument rests on three preliminary facts, which we establish first and then apply to each case.

*Fact 1 (field extraction terminates and is unique).* By T4(b), the function `fields(t)` decomposes a tumbler into its node, user, document, and element fields by locating all zero-valued components. The positive-component constraint (T4) guarantees that zero-valued components are exactly the field separators — no field component can be zero, so every zero is unambiguously a separator. Since `t` is a finite sequence, extraction terminates: scan `t` once, record the positions of zero-valued components, and partition the remaining components into the corresponding fields. The result is uniquely determined by `t` alone (T4(b)). Write `N(t)`, `U(t)`, `D(t)`, `E(t)` for the node, user, document, and element fields of `t` respectively. Each is a finite (possibly absent) sequence of strictly positive natural numbers.

*Fact 2 (field presence is decidable).* Define `zeros(t) = #{i : 1 ≤ i ≤ #t ∧ tᵢ = 0}`. By T4(c), this count is computable from `t` alone — a single finite scan — and determines field presence: every tumbler has a node field (T4 requires `α ≥ 1`); a user field is present iff `zeros(t) ≥ 1`; a document field is present iff `zeros(t) ≥ 2`; an element field is present iff `zeros(t) = 3`. Each presence check reduces to comparing a non-negative integer against a constant, which is decidable.

*Fact 3 (finite-sequence equality is decidable).* Two finite sequences of natural numbers `S = (s₁, ..., sₘ)` and `R = (r₁, ..., rₙ)` are equal iff `m = n` and `(A i : 1 ≤ i ≤ m : sᵢ = rᵢ)` — this is T3 applied to the subsequences. The check requires one length comparison and at most `m` equality tests on natural numbers, each decidable. The procedure terminates in at most `m + 1` steps. We call this *componentwise comparison* and use it in every case below.

With these three facts established, each case proceeds by extraction (Fact 1), presence check where needed (Fact 2), and componentwise comparison (Fact 3).

*(a) Same node field.* Extract `N(a)` and `N(b)` via `fields` (Fact 1). Every tumbler has a node field — T4 requires `α ≥ 1`, and Fact 2 confirms that no presence check is needed. Apply componentwise comparison (Fact 3): check `#N(a) = #N(b)` and, if so, verify `(A i : 1 ≤ i ≤ #N(a) : N(a)ᵢ = N(b)ᵢ)`. This requires at most `#N(a) + 1` comparisons, each decidable. The procedure terminates and returns *yes* iff the node fields are identical.

*(b) Same node and user fields.* Extract `N(a), U(a)` and `N(b), U(b)` via `fields` (Fact 1). Both `a` and `b` must possess user fields — that is, `zeros(a) ≥ 1` and `zeros(b) ≥ 1` — which is decidable by Fact 2. If either tumbler lacks a user field, the answer is *no*: two tumblers cannot share a field that one does not possess. When both are present, apply componentwise comparison (Fact 3) to each pair in turn: first `N(a) = N(b)`, checking `#N(a) = #N(b)` and `(A i : 1 ≤ i ≤ #N(a) : N(a)ᵢ = N(b)ᵢ)`; then `U(a) = U(b)`, checking `#U(a) = #U(b)` and `(A j : 1 ≤ j ≤ #U(a) : U(a)ⱼ = U(b)ⱼ)`. The procedure terminates and returns *yes* iff both pairs are identical.

*(c) Same node, user, and document-lineage fields.* Extract `N(a), U(a), D(a)` and `N(b), U(b), D(b)` via `fields` (Fact 1). Both must possess document fields — `zeros(a) ≥ 2` and `zeros(b) ≥ 2` — decidable by Fact 2. If either lacks a document field, the answer is *no*. When both are present, apply componentwise comparison (Fact 3) to each of the three pairs: `N(a) = N(b)`, `U(a) = U(b)`, `D(a) = D(b)`. The total number of comparisons is bounded by `#N(a) + #U(a) + #D(a) + 3` — the sum of the field lengths plus three length checks — all finite. The procedure terminates and returns *yes* iff all three pairs are identical.

*(d) Document-field prefix.* Extract `D(a) = (d₁ᵃ, ..., dᵧₐᵃ)` and `D(b) = (d₁ᵇ, ..., dᵧᵦᵇ)` via `fields` (Fact 1). Both must possess document fields — decidable by Fact 2, as in (c). If either lacks a document field, the answer is *no*. The sequence `D(a)` is a prefix of `D(b)` iff two conditions hold: `γₐ ≤ γᵦ` (the prefix is no longer than the candidate) and `(A k : 1 ≤ k ≤ γₐ : dₖᵃ = dₖᵇ)` (componentwise agreement up to the prefix length). Check the length condition first — one comparison of natural numbers; if it fails, return *no*. Otherwise verify componentwise agreement up to position `γₐ` — at most `γₐ` comparisons, each decidable. The procedure terminates in at most `γₐ + 1` steps and returns a boolean.

In every case the procedure examines only the finite sequence of components in `a` and `b`, performs finitely many equality or ordering tests on natural numbers, and terminates. No mapping tables, version graphs, or system state are consulted — the tumbler representation alone suffices. ∎

*Formal Contract:*
- *Preconditions:* `a, b ∈ T` are valid tumblers satisfying T4 (positive-component constraint, at most three zeros, no adjacent zeros, no leading or trailing zero).
- *Definition:* `N(t)`, `U(t)`, `D(t)`, `E(t)` are the node, user, document, and element fields of `t`, extracted by `fields(t)` (T4(b)). Componentwise comparison of two finite sequences `S, R` checks `#S = #R ∧ (A i : 1 ≤ i ≤ #S : Sᵢ = Rᵢ)`. Prefix comparison of `S` against `R` checks `#S ≤ #R ∧ (A i : 1 ≤ i ≤ #S : Sᵢ = Rᵢ)`.
- *Postconditions:* (a) Same-node-field query terminates and returns a boolean, requiring at most `#N(a) + 1` comparisons. (b) Same-node-and-user query terminates and returns a boolean; returns *no* if either tumbler lacks a user field. (c) Same-node-user-document query terminates and returns a boolean; returns *no* if either tumbler lacks a document field. (d) Document-field prefix query terminates and returns a boolean in at most `γₐ + 1` steps; returns *no* if either tumbler lacks a document field. All decisions use only the tumbler representations of `a` and `b`.

T6 is a corollary: it follows immediately from T4 — we extract the relevant fields and compare. We state it separately because the decidability claim is load-bearing for decentralized operation, but it introduces no independent content beyond T4.

We must note what T6(d) does NOT capture. The document field records the *allocation hierarchy* — who baptised which sub-number — not the *derivation history*. Version `5.3` was allocated under document `5`, but this tells us nothing about which version's content was copied to create `5.3`. Nelson: "the version, or subdocument number is only an accidental extension of the document number, and strictly implies no specific relationship of derivation." Formal version-derivation requires the version graph, not just the address.

Nelson confirms that shared prefix means shared containing scope: "The owner of a given item controls the allocation of the numbers under it." The prefix IS the path from root to common ancestor. But he cautions: "Tumblers do not affect the user-level structure of the documents; they only provide a mapping mechanism, and impose no categorization and no structure on the contents of a document." Shared prefix guarantees containment and ownership, never semantic categorization.

Gregory's implementation confirms the distinction between ordering and containment. The codebase provides both `tumblercmp` (total order comparison) and `tumbleraccounteq` (prefix-matching predicate with zero-as-wildcard semantics). The latter truncates the candidate to the length of the parent and checks for exact match — this is the operational realization of T6, and it is a genuinely different algorithm from the ordering comparison.


## Subspace disjointness

Within a document's element space, the first component after the third zero delimiter identifies the *subspace*: 1 for text, 2 for links. Nelson also mentions that the link subspace "could be further subdivided." The critical property is permanent separation:

**T7 (Subspace disjointness).** The subspace identifier (the first component of the element field) permanently separates the address space into disjoint regions. No tumbler in subspace `s₁` can equal or be confused with a tumbler in subspace `s₂ ≠ s₁`.

  `(A a, b ∈ T : a.E₁ ≠ b.E₁ ⟹ a ≠ b)`

*Dependencies:*
- **T3 (Canonical representation):** `a = b ⟺ #a = #b ∧ (A i : 1 ≤ i ≤ #a : aᵢ = bᵢ)`. Contrapositively: tumblers that differ in length or at any component are distinct. Used in every case to conclude `a ≠ b`.
- **T4 (Hierarchical parsing):** (b) `fields(t)` is well-defined and uniquely determined by `t` alone. (c) `zeros(t) = 3` iff `t` is an element-level address. The positive-component constraint: every non-separator component is strictly positive, so every zero in `t` is unambiguously a field separator. Used to locate `E₁` and to distinguish separators from field components.

*Proof.* We must show that two element-level tumblers whose first element-field components differ are distinct tumblers: given `a, b ∈ T` with `a.E₁ ≠ b.E₁`, we establish `a ≠ b`.

The hypothesis that `a` and `b` each possess an element field means each has exactly three zero-valued separator components — by T4(c), `zeros(a) = zeros(b) = 3`. By T4's positive-component constraint, every non-separator component is strictly positive, so every zero in either tumbler is unambiguously a field separator. By T4(b), the field decomposition of each tumbler is uniquely determined.

Write the field lengths of `a` as `(α, β, γ, δ)`: the node field has `α` components, the user field `β`, the document field `γ`, the element field `δ`, with each field length at least 1 by T4's non-empty field constraint. The three separators occupy positions `α + 1`, `α + β + 2`, and `α + β + γ + 3` in the raw component sequence. The first element-field component `a.E₁` therefore sits at position `pₐ = α + β + γ + 4`. Analogously, write the field lengths of `b` as `(α', β', γ', δ')`, so `b.E₁` sits at position `p_b = α' + β' + γ' + 4`.

We proceed by case analysis on whether the element fields begin at the same position.

*Case 1* (`pₐ = p_b`). Both tumblers have their first element-field component at the same position `p = pₐ = p_b`. By hypothesis `a[p] = a.E₁ ≠ b.E₁ = b[p]`, so the tumblers differ at position `p`. By T3 (contrapositively: tumblers that disagree at any position are distinct), `a ≠ b`.

*Case 2* (`pₐ ≠ p_b`). The element fields begin at different positions, so the prefix-length triples `(α, β, γ)` and `(α', β', γ')` differ in at least one coordinate. We consider two sub-cases.

*Sub-case 2a* (`#a ≠ #b`). The tumblers have different total lengths. By T3 (contrapositively: distinct lengths entail distinct tumblers), `a ≠ b`.

*Sub-case 2b* (`#a = #b`). The tumblers have equal total length, call it `n`, but their element fields begin at different positions. We show the separator positions of `a` and `b` must disagree.

The separator positions of `a` are `Sₐ = {α + 1,  α + β + 2,  α + β + γ + 3}` and those of `b` are `S_b = {α' + 1,  α' + β' + 2,  α' + β' + γ' + 3}`. Suppose for contradiction that `Sₐ = S_b`. Since the elements of each set are strictly increasing (each field length is at least 1), matching them in order gives three equations. From the first: `α + 1 = α' + 1`, so `α = α'`. Substituting into the second: `α + β + 2 = α + β' + 2`, so `β = β'`. Substituting into the third: `α + β + γ + 3 = α + β + γ' + 3`, so `γ = γ'`. But then `pₐ = α + β + γ + 4 = α' + β' + γ' + 4 = p_b`, contradicting the case hypothesis `pₐ ≠ p_b`. Therefore `Sₐ ≠ S_b`.

Since `Sₐ ≠ S_b`, there exists a position `j` with `1 ≤ j ≤ n` that is a separator in one tumbler but not the other. In the tumbler where `j` is a separator, the value at position `j` is `0`. In the other tumbler, position `j` falls within a field, so its value is strictly positive by T4's positive-component constraint. Hence `a[j] = 0 ≠ b[j] > 0` (or vice versa), and by T3, `a ≠ b`.

All cases yield `a ≠ b`. ∎

*Formal Contract:*
- *Preconditions:* `a, b ∈ T` with `zeros(a) = zeros(b) = 3` (both are element-level addresses with well-formed field structure per T4).
- *Postconditions:* `a.E₁ ≠ b.E₁ ⟹ a ≠ b`.

We state T7 explicitly because it is load-bearing for the guarantee that operations within one content type do not interfere with another. T7 is the structural basis — arithmetic within subspace 1 cannot produce addresses in subspace 2, because the subspace identifier is part of the address, not metadata.

The ordering T1 places all text addresses (subspace 1) before all link addresses (subspace 2) within the same document, because `1 < 2` at the subspace position. This is a consequence, not an assumption — it falls out of the lexicographic order.


## Allocation permanence

The most consequential property of the address system is that once an address is allocated, it persists forever:

**T8 (Allocation permanence).** If tumbler `a ∈ T` has been allocated at any point in the system's history, then for all subsequent states, `a` remains in the set of allocated addresses. No operation removes an allocated address from the address space. The set of allocated addresses is monotonically non-decreasing.

*Dependencies:*
- **T10a (Allocation mechanism):** Each allocator advances its frontier by `inc(·, 0)`, producing an address strictly greater than the previous, and inserts it into the allocated set. This is the sole mechanism by which the allocated set grows.
- **TA5 (Hierarchical increment):** (a) `inc(t, 0)` produces `t' > t` under T1. Used to establish that each newly allocated address is fresh.
- **TumblerAdd (Constructive definition of ⊕), TumblerSub (Constructive definition of ⊖):** Pure functions on component sequences: each accepts tumbler arguments, computes a new component sequence, and returns a tumbler value. Neither operation consults or modifies the allocated set.
- **T1 (Lexicographic order), T2 (Decidable comparison), T4 (Hierarchical parsing):** Read-only operations that inspect tumbler values without modifying any system state.

*Proof.* We must show that the set of allocated addresses grows monotonically — that for every state transition `s → s'`, `allocated(s) ⊆ allocated(s')`. The strategy is exhaustive case analysis over the operations the system defines, followed by induction on transition sequences.

Let `s` be any reachable state and `s'` the state after one operation. Every operation the system defines falls into exactly one of three classes; we treat each in turn.

*Case 1: Read-only operations.* The ordering test (T1), the decidable comparison procedure (T2), and hierarchical parsing (T4) each inspect the component values of one or two tumblers and return a result. None of these operations consults or modifies the allocated set — they are pure queries on tumbler values. Therefore `allocated(s') = allocated(s)`, and the inclusion `allocated(s) ⊆ allocated(s')` holds as an equality.

*Case 2: Pure arithmetic.* The operations `⊕` (tumbler addition), `⊖` (tumbler subtraction), and `inc` (hierarchical increment) are pure functions on `T`. Their constructive definitions (TumblerAdd, TumblerSub, TA5 respectively) each accept tumbler arguments, compute on the component sequences of their operands, and return a tumbler value; none of these constructions consults or modifies the allocated set. Therefore `allocated(s') = allocated(s)`, and the inclusion holds as an equality.

*Case 3: Allocation.* T10a defines the sole allocation mechanism. An allocator with current frontier address `t` computes `t' = inc(t, 0)`. By TA5(a), `t' > t` — the new address is strictly greater than the frontier, so in particular `t' ∉ allocated(s)` (since `t` was the frontier, all previously allocated addresses in this allocator's stream satisfy `a ≤ t < t'`). The allocator then inserts `t'` into the allocated set: `allocated(s') = allocated(s) ∪ {t'}`. Since `allocated(s) ⊆ allocated(s) ∪ {t'} = allocated(s')`, the inclusion holds.

These three cases are exhaustive — every operation the system defines belongs to one of them. Critically, the system specification defines no inverse operation: no "deallocate", "free", or "reclaim" that would remove an address from the allocated set. The absence of any removal operation is a deliberate design axiom, not a derived property.

We have established that every single-step transition satisfies `allocated(s) ⊆ allocated(s')`. The extension to arbitrary transition sequences follows by induction on the number of transitions `n`. For `n = 0` the claim is trivial (`allocated(s₀) ⊆ allocated(s₀)`). Given `allocated(s₀) ⊆ allocated(sₙ)` for some `n ≥ 0`, and the single-step inclusion `allocated(sₙ) ⊆ allocated(sₙ₊₁)`, transitivity of `⊆` yields `allocated(s₀) ⊆ allocated(sₙ₊₁)`. Therefore `allocated(s₀) ⊆ allocated(sₙ)` for all reachable states `sₙ`. ∎

*Formal Contract:*
- *Invariant:* For every state transition `s → s'`, `allocated(s) ⊆ allocated(s')`.
- *Axiom:* The system defines no operation that removes an element from the allocated set. This is a design constraint, not a derived property.
- *Frame:* Read-only operations (T1, T2, T4) and pure arithmetic (⊕, ⊖, inc) preserve the allocated set exactly: `allocated(s') = allocated(s)`.

Nelson: "any address of any document in an ever-growing network may be specified by a permanent tumbler address." The guarantee is about the address itself — its persistence, its permanent occupancy of its position on the tumbler line.

Even addresses that have no stored content are irrevocably claimed. Nelson calls these "ghost elements": "While servers, accounts and documents logically occupy positions on the developing tumbler line, no specific element need be stored in tumbler-space to correspond to them. Hence we may call them ghost elements." A ghost element occupies a position on the tumbler line, and that position cannot be reclaimed.

T8 is required for link stability (links reference addresses, which must remain valid), for transclusion identity (transcluded content maintains its address), and for attribution (the address encodes the originating server, user, and document, and this attribution cannot be revised). What a given address *maps to* — whether content, and what content — is a property of the mapping layer, not the algebra.


## Monotonic allocation

T8 tells us that addresses, once allocated, are permanent. We now ask: in what order are new addresses assigned?

**T9 (Forward allocation).** T10a below defines the allocation mechanism: each allocator advances by `inc(·, 0)`, incrementing by exactly 1 at the last significant position. Since `inc` produces a strictly greater tumbler at each step (TA5(a)), it follows that within each allocator's sequential stream, new addresses are strictly monotonically increasing:

  `(A a, b : same_allocator(a, b) ∧ allocated_before(a, b) : a < b)`

Nelson's design is explicitly sequential: "successive new digits to the right ... 2.1, 2.2, 2.3, 2.4 are successive items being placed under 2." The word "successive" carries the weight: 2.2 follows 2.1, never precedes it. Under T10a, no gaps arise within a single allocator's sibling stream — each address is exactly one increment beyond the previous.

Positions on the tumbler line that have been allocated but have no stored content are what Nelson calls "ghost elements" (T8 above). Ghosts are about absent content, not absent addresses — every allocated position is permanently claimed whether or not anything is stored there.

But the tumbler line as a whole does NOT grow monotonically by creation time. Nelson: "Starting from a given tumbler address, it may only be possible arithmetically to get to some places in the Docuverse — those notationally after that address." When a parent address forks a child, the child is *inserted* between the parent and the parent's next sibling on the tumbler line. Address `2.1.1` may be created long after `2.2`, but it sits between them: `2.1 < 2.1.1 < 2.2`. The depth-first linearization means children always precede the parent's next sibling, regardless of creation order. T9 holds per-allocator, not globally.

We observe that T9 is scoped to a *single allocator's sequential stream*, not to arbitrary partitions. A server-level subtree spans multiple independent allocators (one per user). Those allocators operate concurrently — T10 below guarantees they need no coordination. If user A (prefix `1.0.1`) allocates at wall-clock time `t₂` and user B (prefix `1.0.2`) allocates at time `t₁ < t₂`, neither T9 nor any other property requires that A's address exceed B's. T9 applies within each user's allocation stream independently.

A consequence of T8 and T9 together: the set of allocated addresses is a *growing set* in the lattice-theoretic sense — it can only increase, and new elements always appear at the frontier of each allocator's domain.

*Dependencies:*
- **T10a (Allocator discipline):** Each allocator produces its sibling outputs exclusively by repeated application of `inc(·, 0)`. This is the mechanism under proof: the sequence `t₀, t₁, t₂, ...` with `tₙ₊₁ = inc(tₙ, 0)` is the allocator's entire sibling stream.
- **TA5 (Hierarchical increment):** (a) `inc(t, 0)` produces `t' > t` under T1. Supplies the strict increase at each step that drives the induction.
- **T1 (Lexicographic order):** (c) Transitivity: `a < b ∧ b < c ⟹ a < c`. Chains consecutive strict increases across multiple steps.

*Proof.* We must show that within a single allocator's sequential stream, if address `a` was allocated before address `b`, then `a < b` under the tumbler order T1.

By T10a, each allocator produces its sibling outputs exclusively by repeated application of `inc(·, 0)`. Let the allocator's base address be `t₀` and its successive outputs be `t₁, t₂, t₃, ...` where `tₙ₊₁ = inc(tₙ, 0)` for all `n ≥ 0`. The predicate `same_allocator(a, b)` holds exactly when both `a` and `b` appear in this sequence, and `allocated_before(a, b)` holds exactly when `a = tᵢ` and `b = tⱼ` with `i < j`. We must show `tᵢ < tⱼ`.

We proceed by induction on the gap `d = j - i ≥ 1`.

*Base case* (`d = 1`). Here `tⱼ = inc(tᵢ, 0)`. By TA5(a), `inc(tᵢ, 0) > tᵢ`, so `tᵢ < tⱼ`.

*Inductive step* (from `d` to `d + 1`, assuming the result holds for gap `d`). We must show `tᵢ < tⱼ` when `j - i = d + 1`. Since `d ≥ 1`, the index `j - 1` satisfies `i < j - 1 < j` with gap `(j - 1) - i = d`. By the inductive hypothesis, `tᵢ < tⱼ₋₁`. By TA5(a), `tⱼ = inc(tⱼ₋₁, 0) > tⱼ₋₁`, so `tⱼ₋₁ < tⱼ`. By transitivity of the strict order (T1(c)), `tᵢ < tⱼ`.

This completes the induction. For any addresses `a, b` with `same_allocator(a, b) ∧ allocated_before(a, b)`, we have `a < b`.

We note the scope of this result. T9 holds per-allocator, not globally. The tumbler line as a whole does not grow monotonically by creation time: when a parent forks a child via `inc(·, k')` with `k' > 0` (T10a), the child is inserted between the parent and the parent's next sibling — address `2.1.1` may be created long after `2.2`, yet `2.1 < 2.1.1 < 2.2` by T1 case (ii). The depth-first linearization places children before the parent's next sibling regardless of creation order. ∎

*Formal Contract:*
- *Preconditions:* `a, b ∈ T` with `same_allocator(a, b) ∧ allocated_before(a, b)` — both addresses produced by the same allocator's sibling stream, `a` allocated before `b`.
- *Postconditions:* `a < b` under the tumbler order T1.


## Coordination-free uniqueness

The tumbler hierarchy exists so that independent actors can allocate addresses without communicating:

**T10 (Partition independence).** The address space is partitioned by prefix into ownership domains. Two allocators with distinct, non-nesting prefixes can allocate simultaneously, and the resulting addresses are guaranteed distinct.

Formally: let `p₁` and `p₂` be prefixes such that neither is a prefix of the other (`p₁ ⋠ p₂ ∧ p₂ ⋠ p₁`). Then for any tumbler `a` with prefix `p₁` and any tumbler `b` with prefix `p₂`, `a ≠ b`.

*Dependencies:*
- **T3 (Canonical representation):** `a = b ⟺ #a = #b ∧ (A i : 1 ≤ i ≤ #a : aᵢ = bᵢ)`. Used contrapositively: tumblers that differ at any component are distinct.
- **Prefix relation (from T1):** `p ≼ a` means `#p ≤ #a` and `aᵢ = pᵢ` for all `1 ≤ i ≤ #p`. Negation `p ⋠ a` means it is not the case that `p ≼ a`.

*Proof.* We must show: given prefixes `p₁ = p₁₁. ... .p₁ₘ` and `p₂ = p₂₁. ... .p₂ₙ` satisfying `p₁ ⋠ p₂ ∧ p₂ ⋠ p₁`, and tumblers `a` with `p₁ ≼ a` and `b` with `p₂ ≼ b`, that `a ≠ b`.

We first establish that the non-nesting prefixes must diverge at some component position within their common range `ℓ = min(m, n)`. The proof splits into two cases on the relative lengths of the prefixes.

*Case 1: `m ≤ n`.* The prefix relation `p₁ ≼ p₂` requires `#p₁ ≤ #p₂` and `p₂ᵢ = p₁ᵢ` for all `1 ≤ i ≤ m`. Since `m ≤ n`, the length condition holds; the hypothesis `p₁ ⋠ p₂` therefore means the componentwise condition fails. There exists some `j` with `1 ≤ j ≤ m` such that `p₁ⱼ ≠ p₂ⱼ`. (If no such `j` existed, `p₂` would agree with `p₁` on all `m` positions, making `p₁ ≼ p₂` — contradicting `p₁ ⋠ p₂`.) Since `m ≤ n`, we have `j ≤ m = ℓ`, so the divergence occurs within the common range.

*Case 2: `m > n`.* The prefix relation `p₂ ≼ p₁` requires `#p₂ ≤ #p₁` and `p₁ᵢ = p₂ᵢ` for all `1 ≤ i ≤ n`. Since `n < m`, the length condition holds; the hypothesis `p₂ ⋠ p₁` therefore means the componentwise condition fails. There exists some `j` with `1 ≤ j ≤ n` such that `p₂ⱼ ≠ p₁ⱼ`. (If no such `j` existed, `p₁` would agree with `p₂` on all `n` positions, making `p₂ ≼ p₁` — contradicting `p₂ ⋠ p₁`.) Since `n < m`, we have `j ≤ n = ℓ`, so the divergence occurs within the common range.

In both cases, let `k` be the *least* such divergence position: `k = min{j : 1 ≤ j ≤ ℓ ∧ p₁ⱼ ≠ p₂ⱼ}`. By construction, `p₁ᵢ = p₂ᵢ` for all `1 ≤ i < k`, and `p₁ₖ ≠ p₂ₖ`, with `k ≤ ℓ = min(m, n)`.

We now transfer this divergence to `a` and `b`. Since `p₁ ≼ a`, the prefix relation gives `aᵢ = p₁ᵢ` for all `1 ≤ i ≤ m`. Since `k ≤ m` (from `k ≤ min(m, n) ≤ m`), this yields `aₖ = p₁ₖ`. Since `p₂ ≼ b`, the prefix relation gives `bᵢ = p₂ᵢ` for all `1 ≤ i ≤ n`. Since `k ≤ n` (from `k ≤ min(m, n) ≤ n`), this yields `bₖ = p₂ₖ`. Combining: `aₖ = p₁ₖ ≠ p₂ₖ = bₖ`. The tumblers `a` and `b` differ at position `k`, so by the contrapositive of T3 — tumblers that differ at any component are distinct — `a ≠ b`. ∎

*Formal Contract:*
- *Preconditions:* `p₁, p₂ ∈ T` with `p₁ ⋠ p₂ ∧ p₂ ⋠ p₁`; `a, b ∈ T` with `p₁ ≼ a` and `p₂ ≼ b`.
- *Postconditions:* `a ≠ b`.

The proof is elementary, but the property is architecturally profound. Nelson: "The owner of a given item controls the allocation of the numbers under it." No central allocator is needed. No coordination protocol is needed. The address structure itself makes collision impossible.

Nelson: "Whoever owns a specific node, account, document or version may in turn designate (respectively) new nodes, accounts, documents and versions, by forking their integers. We often call this the 'baptism' of new numbers." Baptism is the mechanism by which ownership domains are established — the owner of a number creates sub-numbers beneath it, and those sub-numbers belong exclusively to the owner.

**T10a (Allocator discipline).** Each allocator produces its sibling outputs exclusively by repeated application of `inc(·, 0)` — shallow increment at the last significant position. To spawn a child allocator, the parent performs one `inc(·, k')` with `k' > 0` to establish the child's prefix, then delegates further allocation to the child. The parent's own sibling stream resumes with `inc(·, 0)`.

*Dependencies:*
- **TA5 (Hierarchical increment):** (a) `inc(t, k)` produces `t' > t` under T1. (b) `t'` agrees with `t` on all components before the increment point. (c) When `k = 0`: `#t' = #t`, and `t'` differs from `t` only at `sig(t)`, where `t'_{sig(t)} = t_{sig(t)} + 1`. (d) When `k > 0`: `#t' = #t + k`, with `k - 1` zero field separators and final component `1`.
- **T1 (Lexicographic order):** `a < b` iff there exists `k ≥ 1` with `aᵢ = bᵢ` for all `i < k`, and either (i) `k ≤ min(#a, #b)` and `aₖ < bₖ`, or (ii) `k = #a + 1 ≤ #b` (proper prefix). Irreflexivity: `¬(a < a)`.
- **T3 (Canonical representation):** `a = b ⟺ #a = #b ∧ (A i : 1 ≤ i ≤ #a : aᵢ = bᵢ)`. Contrapositively: tumblers of different lengths are distinct.
- **T10 (Partition independence):** For non-nesting prefixes `p₁ ⋠ p₂ ∧ p₂ ⋠ p₁`, any tumbler extending `p₁` is distinct from any tumbler extending `p₂`.
- **Prefix relation (from T1):** `p ≼ a` means `#p ≤ #a` and `aᵢ = pᵢ` for all `1 ≤ i ≤ #p`. A proper prefix `p ≺ a` requires `p ≼ a` with `p ≠ a`, entailing `#p < #a`.

*Justification.* T10a is a design axiom: it constrains allocator behavior rather than following from prior properties. Without it, an allocator could intermix shallow and deep increments, producing outputs of varying lengths whose prefix relationships would be uncontrolled. We justify the constraint by establishing three consequences on which the coordination-free uniqueness guarantees depend, then proving that the constraint is necessary — that relaxing it permits nesting violations that collapse T10's partition independence.

**Consequence 1: Uniform sibling length.** We prove: `(A n ≥ 0 : #tₙ = #t₀)`, where `tₙ₊₁ = inc(tₙ, 0)` is the sibling sequence of an allocator with base address `t₀`.

*Base case* (`n = 0`). `#t₀ = #t₀` holds by reflexivity of equality.

*Inductive step.* Assume `#tₙ = #t₀` for some `n ≥ 0`. By TA5(c), `inc(t, 0)` preserves length: `#inc(t, 0) = #t`. Instantiating with `t := tₙ`:

  `#tₙ₊₁ = #inc(tₙ, 0) = #tₙ`

By the inductive hypothesis, `#tₙ = #t₀`, so `#tₙ₊₁ = #t₀`. The induction closes.

Every sibling output of a single allocator has the same length as its base address. ∎ (Consequence 1)

**Consequence 2: Non-nesting sibling prefixes.** We prove: for distinct siblings `tᵢ` and `tⱼ` (with `i < j`) from the same allocator, `tᵢ ⋠ tⱼ ∧ tⱼ ⋠ tᵢ`.

*Step 1: Distinctness.* By TA5(a), each application of `inc(·, 0)` produces a strictly greater tumbler: `tₙ₊₁ = inc(tₙ, 0) > tₙ`. By induction on the index gap, the sibling sequence is strictly increasing: `t₀ < t₁ < t₂ < ...`. Since `i < j`, we have `tᵢ < tⱼ`, and by T1 irreflexivity, `tᵢ ≠ tⱼ`.

*Step 2: Equal length.* By Consequence 1, `#tᵢ = #t₀` and `#tⱼ = #t₀`, so `#tᵢ = #tⱼ`.

*Step 3: Non-nesting.* Suppose for contradiction that `tᵢ ≼ tⱼ`. Since `tᵢ ≠ tⱼ` (Step 1), this is a proper prefix: `tᵢ ≺ tⱼ`, which requires `#tᵢ < #tⱼ`. But `#tᵢ = #tⱼ` (Step 2) — contradiction. Therefore `tᵢ ⋠ tⱼ`. Now suppose for contradiction that `tⱼ ≼ tᵢ`. Since `tⱼ ≠ tᵢ` (Step 1), this is a proper prefix: `tⱼ ≺ tᵢ`, which requires `#tⱼ < #tᵢ`. But `#tᵢ = #tⱼ` (Step 2) — contradiction. Therefore `tⱼ ⋠ tᵢ`.

Combining: `tᵢ ⋠ tⱼ ∧ tⱼ ⋠ tᵢ`. The sibling prefixes are non-nesting, satisfying the precondition of T10. ∎ (Consequence 2)

**Consequence 3: Length separation between parent and child domains.** We prove: every child output has length strictly greater than every parent sibling output.

Let a parent allocator have base address `t₀` with sibling length `γ = #t₀`. When the parent spawns a child via `inc(t, k')` with `k' > 0` — where `t` is one of the parent's siblings — the child's base address `c₀` has length `#c₀ = #t + k'` by TA5(d). Since `t` is a parent sibling, `#t = γ` by Consequence 1, so `#c₀ = γ + k'`.

The child allocator produces its own siblings by `inc(·, 0)` (T10a). By Consequence 1 applied to the child's sequence, all child outputs have uniform length `γ + k'`. Since `k' ≥ 1`, every child output has length at least `γ + 1 > γ` — strictly longer than any parent sibling. By the contrapositive of T3, tumblers of different lengths are distinct: no child output can equal any parent sibling.

The separation is additive across nesting levels. Each child-spawning step adds at least one component (TA5(d) with `k' ≥ 1`), so a descendant `d` levels deep produces outputs of length at least `γ + d`. Outputs at different depths cannot collide, since they differ in length and T3 applies. ∎ (Consequence 3)

**Necessity.** We show that relaxing the `k = 0` restriction for siblings permits nesting, violating the precondition of T10.

Suppose an allocator produces `t₁ = inc(t₀, 0)` followed by `t₂ = inc(t₁, 1)`, treating both as sibling outputs. By TA5(c), `#t₁ = #t₀`. By TA5(d), `#t₂ = #t₁ + 1 = #t₀ + 1`, so `#t₁ < #t₂`.

We show `t₁ ≼ t₂`. The child construction TA5(d) for `inc(t₁, 1)` copies all components of `t₁` into positions `1, ..., #t₁` of `t₂`: for all `i` with `1 ≤ i ≤ #t₁`, `t₂ᵢ = t₁ᵢ`. Since `#t₁ < #t₂`, we have both `#t₁ ≤ #t₂` and component-wise agreement at every position of `t₁`. By definition of the prefix relation, `t₁ ≼ t₂`. Since `t₁ ≠ t₂` (they differ in length), this is a proper prefix: `t₁ ≺ t₂`.

The siblings nest. This violates the non-nesting precondition of T10 — any address extending `t₂` also extends `t₁`, so T10 cannot distinguish the two domains. The partition independence guarantee collapses.

The constraint to `k = 0` for siblings is therefore both sufficient (Consequences 1–3) and necessary (its absence permits nesting). ∎

*Formal Contract:*
- *Axiom:* Allocators produce sibling outputs exclusively by `inc(·, 0)`; child-spawning uses exactly one `inc(·, k')` with `k' > 0`.
- *Postconditions:* (a) Uniform sibling length — `(A tᵢ, tⱼ : same_allocator(tᵢ, tⱼ) ∧ sibling(tᵢ) ∧ sibling(tⱼ) : #tᵢ = #tⱼ)`. (b) Non-nesting sibling prefixes — `(A tᵢ, tⱼ : same_allocator(tᵢ, tⱼ) ∧ sibling(tᵢ) ∧ sibling(tⱼ) ∧ tᵢ ≠ tⱼ : tᵢ ⋠ tⱼ ∧ tⱼ ⋠ tᵢ)`. (c) Length separation — child outputs have length strictly greater than parent sibling outputs: `(A t_parent, t_child : sibling(t_parent) ∧ spawned_by(t_child, t_parent) : #t_child > #t_parent)`.

We first establish a lemma that converts ordering of prefixes into ordering of all addresses under those prefixes.

**PrefixOrderingExtension (Prefix ordering extension).** Let `p₁, p₂ ∈ T` be tumblers such that `p₁ < p₂` and neither is a prefix of the other (`p₁ ⋠ p₂ ∧ p₂ ⋠ p₁`). Then for every `a` extending `p₁` (`p₁ ≼ a`) and every `b` extending `p₂` (`p₂ ≼ b`), `a < b`.

*Dependencies:*
- **T1 (Lexicographic order):** `a < b` iff there exists least `k ≥ 1` with `(A i : 1 ≤ i < k : aᵢ = bᵢ)` and either (i) `k ≤ min(#a, #b)` with `aₖ < bₖ`, or (ii) `k = #a + 1 ≤ #b` (proper prefix).
- **Prefix relation (from T1):** `p ≼ a` means `#p ≤ #a` and `aᵢ = pᵢ` for all `1 ≤ i ≤ #p`.

*Proof.* We must show: `(A a, b ∈ T : p₁ ≼ a ∧ p₂ ≼ b : a < b)`, given that `p₁ < p₂` and `p₁ ⋠ p₂ ∧ p₂ ⋠ p₁`.

**Extracting the divergence point.** Let `p₁ = p₁₁. ... .p₁ₘ` and `p₂ = p₂₁. ... .p₂ₙ`. The hypothesis `p₁ < p₂` means, by T1, that there exists a least position `k ≥ 1` such that `(A i : 1 ≤ i < k : p₁ᵢ = p₂ᵢ)` and one of two cases holds. Case (ii) requires `p₁` to be a proper prefix of `p₂`, i.e., `k = m + 1 ≤ n`, which gives `#p₁ ≤ #p₂` and `p₂ᵢ = p₁ᵢ` for all `1 ≤ i ≤ m` — that is, `p₁ ≼ p₂`, contradicting the hypothesis `p₁ ⋠ p₂`. Therefore case (i) applies: `k ≤ min(m, n)` and `p₁ₖ < p₂ₖ`. We record:

  (H1) `(A i : 1 ≤ i < k : p₁ᵢ = p₂ᵢ)` — the prefixes agree before position `k`.

  (H2) `k ≤ min(m, n)` and `p₁ₖ < p₂ₖ` — the prefixes diverge at position `k`.

**Transferring the divergence to extensions.** Let `a` and `b` be arbitrary tumblers with `p₁ ≼ a` and `p₂ ≼ b`.

From `p₁ ≼ a`: by the prefix relation, `#a ≥ m` and `aᵢ = p₁ᵢ` for all `1 ≤ i ≤ m`. Since `k ≤ m` (from H2, as `k ≤ min(m, n) ≤ m`), position `k` falls within the prefix, so `aₖ = p₁ₖ`.

From `p₂ ≼ b`: by the prefix relation, `#b ≥ n` and `bᵢ = p₂ᵢ` for all `1 ≤ i ≤ n`. Since `k ≤ n` (from H2, as `k ≤ min(m, n) ≤ n`), position `k` falls within the prefix, so `bₖ = p₂ₖ`.

**Establishing `a < b` via T1 case (i).** We verify the two conditions required by T1 case (i).

*Agreement before position `k`:* for each `i` with `1 ≤ i < k`, we have `aᵢ = p₁ᵢ` (from `p₁ ≼ a`, since `i < k ≤ m`) and `p₁ᵢ = p₂ᵢ` (from H1) and `p₂ᵢ = bᵢ` (from `p₂ ≼ b`, since `i < k ≤ n`), giving `aᵢ = bᵢ`.

*Strict inequality at position `k`:* `aₖ = p₁ₖ < p₂ₖ = bₖ`, combining the prefix transfers with H2.

*Witness validity:* `k ≤ min(#a, #b)`, since `k ≤ m ≤ #a` and `k ≤ n ≤ #b`.

These three facts together satisfy T1 case (i), giving `a < b`.

Since `a` and `b` were arbitrary tumblers extending `p₁` and `p₂` respectively, the result holds universally: `(A a, b ∈ T : p₁ ≼ a ∧ p₂ ≼ b : a < b)`. ∎

*Formal Contract:*
- *Preconditions:* `p₁, p₂ ∈ T` with `p₁ < p₂` (T1) and `p₁ ⋠ p₂ ∧ p₂ ⋠ p₁` (non-nesting); `a, b ∈ T` with `p₁ ≼ a` and `p₂ ≼ b`.
- *Postconditions:* `a < b` under T1.

**PartitionMonotonicity (Partition monotonicity).** Within any prefix-delimited partition of the address space, the set of allocated addresses is totally ordered by T1, and this order is consistent with the allocation order of any single allocator within that partition. Moreover, for any two sibling sub-partitions with non-nesting prefixes `p₁ < p₂`, every address extending `p₁` precedes every address extending `p₂` under T1 — the per-allocator ordering extends to a cross-allocator ordering determined by the prefix structure.

*Dependencies:*
- **T1 (Lexicographic order):** `a < b` iff there exists least `k ≥ 1` with `(A i : 1 ≤ i < k : aᵢ = bᵢ)` and either (i) `k ≤ min(#a, #b)` with `aₖ < bₖ`, or (ii) `k = #a + 1 ≤ #b` (proper prefix). The relation is a strict total order on `T`.
- **T5 (Contiguous subtrees):** For any tumbler prefix `p`, the set `{t ∈ T : p ≼ t}` forms a contiguous interval under T1: `[p ≼ a ∧ p ≼ c ∧ a ≤ b ≤ c ⟹ p ≼ b]`.
- **T9 (Forward allocation):** `(A a, b : same_allocator(a, b) ∧ allocated_before(a, b) : a < b)`.
- **T10a (Allocator discipline):** Each allocator produces sibling outputs exclusively by `inc(·, 0)`. To spawn a child, it performs one `inc(·, k')` with `k' > 0`.
- **TA5 (Hierarchical increment):** (a) `inc(t, k) > t`; (c) when `k = 0`: `#inc(t, 0) = #t`, differing from `t` only at position `sig(t)` where the component increases by 1; (d) when `k > 0`: `#inc(t, k) = #t + k`.
- **PrefixOrderingExtension:** For `p₁, p₂ ∈ T` with `p₁ < p₂` and `p₁ ⋠ p₂ ∧ p₂ ⋠ p₁`, every `a` extending `p₁` and every `b` extending `p₂` satisfy `a < b`.
- **Prefix relation (from T1):** `p ≼ a` means `#p ≤ #a` and `aᵢ = pᵢ` for all `1 ≤ i ≤ #p`. A proper prefix `p ≺ a` requires `p ≼ a` with `p ≠ a`, entailing `#p < #a`.

*Proof.* We must show two things: (i) for sibling sub-partition prefixes `tᵢ < tⱼ` produced by a single allocator within a prefix-delimited partition, every address extending `tᵢ` precedes every address extending `tⱼ` under T1; and (ii) within each sub-partition, allocation order coincides with address order. Together these yield a total ordering on all allocated addresses in the partition, consistent with both per-allocator allocation order and the prefix structure.

**Partition structure.** Consider a partition with prefix `p`. Every allocated address `a` in this partition satisfies `p ≼ a`, placing it in the set `{t ∈ T : p ≼ t}`. By T5, this set forms a contiguous interval under T1: if `p ≼ a`, `p ≼ c`, and `a ≤ b ≤ c`, then `p ≼ b`. No address from outside the partition can interleave between two addresses inside it.

**Sub-partition construction.** Within the partition, the parent allocator spawns a child allocator according to T10a. The child's base address `t₀` is produced by `inc(s, k)` with `k > 0`, where `s` is a parent sibling extending `p`; by TA5(d), `#t₀ = #s + k`. The child allocator then produces its sibling outputs by repeated application of `inc(·, 0)` (T10a): `t₁ = inc(t₀, 0)`, `t₂ = inc(t₁, 0)`, and so on. Each `tᵢ` serves as the prefix for a distinct sub-partition within the parent partition.

**Sibling prefixes are non-nesting.** We establish that for distinct indices `i ≠ j`: `tᵢ ⋠ tⱼ ∧ tⱼ ⋠ tᵢ`. The argument proceeds through three facts.

*Uniform length.* By TA5(c), `inc(t, 0)` preserves length: `#inc(t, 0) = #t`. Applying this inductively from `t₀` — `#t₁ = #inc(t₀, 0) = #t₀`, and for each `n ≥ 0`, `#tₙ₊₁ = #inc(tₙ, 0) = #tₙ` — we obtain `#tₙ = #t₀` for all `n ≥ 0`. Every sibling prefix has the same length.

*Distinctness.* By TA5(a), each application of `inc(·, 0)` produces a strictly greater tumbler under T1, so the sibling prefix sequence is strictly increasing: `t₀ < t₁ < t₂ < ...`. In particular, `tᵢ ≠ tⱼ` for all `i ≠ j`.

*Non-nesting.* A proper prefix relationship `q ≺ r` requires `#q < #r`, since T1 case (ii) defines `q < r` when `q` is a proper prefix of `r`, which demands `k = #q + 1 ≤ #r`, hence `#q < #r`. Since `#tᵢ = #tⱼ` (uniform length), we have `¬(#tᵢ < #tⱼ)` and `¬(#tⱼ < #tᵢ)`, so neither can be a proper prefix of the other: `tᵢ ⊀ tⱼ` and `tⱼ ⊀ tᵢ`. The prefix relation `tᵢ ≼ tⱼ` means either `tᵢ = tⱼ` or `tᵢ ≺ tⱼ`; we have excluded `tᵢ = tⱼ` (distinctness) and `tᵢ ≺ tⱼ` (equal length precludes proper prefix), so `tᵢ ⋠ tⱼ`. For the reverse: `tⱼ ≼ tᵢ` means either `tⱼ = tᵢ` or `tⱼ ≺ tᵢ`; we have excluded `tⱼ = tᵢ` (distinctness, since `tᵢ ≠ tⱼ` entails `tⱼ ≠ tᵢ`) and `tⱼ ≺ tᵢ` (equal length, since `#tⱼ = #tᵢ` precludes `#tⱼ < #tᵢ`), so `tⱼ ⋠ tᵢ`.

**Cross-partition ordering.** Take two sibling sub-partition prefixes `tᵢ` and `tⱼ` with `i < j`. From the strict monotonicity of the sibling sequence we have `tᵢ < tⱼ`, and we have just established `tᵢ ⋠ tⱼ ∧ tⱼ ⋠ tᵢ`. These are precisely the preconditions of PrefixOrderingExtension: for every address `a` with `tᵢ ≼ a` and every address `b` with `tⱼ ≼ b`, we conclude `a < b`. The prefix ordering of sub-partitions determines the address ordering across them.

**Intra-partition ordering.** Within any single sub-partition, all addresses are produced by one allocator's sequential stream of `inc(·, 0)` applications (T10a). By TA5(a), each step produces a strictly greater tumbler, so by T9, `allocated_before(a, b)` implies `a < b`. Allocation order within each sub-partition coincides with address order.

**Total ordering.** Every address in the partition belongs to exactly one sub-partition — the sub-partition whose prefix it extends. For any two distinct allocated addresses `a` and `b` within the partition, exactly one of three cases holds.

*Case 1: Same sub-partition.* Both `a` and `b` extend the same prefix `tᵢ`. Since they are produced by the same allocator's sequential stream, one was allocated before the other. By T9, `allocated_before(a, b) ⟹ a < b` (or `allocated_before(b, a) ⟹ b < a`). In either case, `a` and `b` are comparable under T1, and the ordering is consistent with allocation order.

*Case 2: `a` in earlier sub-partition.* Address `a` extends `tᵢ` and `b` extends `tⱼ` with `i < j`. Since the sibling sequence is strictly increasing, `tᵢ < tⱼ`, and since sibling prefixes are non-nesting, PrefixOrderingExtension gives `a < b`.

*Case 3: `a` in later sub-partition.* Address `a` extends `tᵢ` and `b` extends `tⱼ` with `i > j`. Since `j < i`, the sibling sequence gives `tⱼ < tᵢ`, and since sibling prefixes are non-nesting, PrefixOrderingExtension gives `b < a`.

In every case, `a` and `b` are comparable under T1. The ordering is consistent with allocation order within each allocator (Case 1, via T9) and with prefix structure across allocators (Cases 2–3, via PrefixOrderingExtension). ∎

*Formal Contract:*
- *Preconditions:* A system conforming to T10a (allocator discipline); a partition with prefix `p ∈ T`; sub-partition prefixes `t₀, t₁, ...` produced by `inc(·, 0)` from an initial child prefix `t₀ = inc(s, k)` with `k > 0` and `p ≼ s`.
- *Postconditions:* (1) For sibling sub-partition prefixes `tᵢ < tⱼ` (with `i < j`) and any `a, b ∈ T` with `tᵢ ≼ a` and `tⱼ ≼ b`: `a < b`. (2) Within each sub-partition with prefix `tᵢ`: `allocated_before(a, b) ⟹ a < b`.
- *Invariant:* For every reachable system state, the set of allocated addresses within any prefix-delimited partition is totally ordered by T1 consistently with per-allocator allocation order.

**GlobalUniqueness (Global uniqueness).** No two distinct allocations, anywhere in the system, at any time, produce the same address.

*Dependencies:*
- **T1 (Lexicographic order):** `a < b` iff there exists `k ≥ 1` with `aᵢ = bᵢ` for all `i < k`, and either (i) `k ≤ min(#a, #b)` and `aₖ < bₖ`, or (ii) `k = #a + 1 ≤ #b` (proper prefix). Part (a): irreflexivity — `¬(a < a)`.
- **T3 (Canonical representation):** `a = b ⟺ #a = #b ∧ (A i : 1 ≤ i ≤ #a : aᵢ = bᵢ)`. Contrapositive: `#a ≠ #b ⟹ a ≠ b`.
- **T4 (Hierarchical parsing):** The zero count `zeros(t)` — the number of zero-valued field-separator components — uniquely determines the hierarchical level. The correspondence is injective: distinct levels entail distinct zero counts.
- **T9 (Forward allocation):** `(A a, b : same_allocator(a, b) ∧ allocated_before(a, b) : a < b)`.
- **T10 (Partition independence):** For prefixes `p₁, p₂` with `p₁ ⋠ p₂ ∧ p₂ ⋠ p₁`, every `a` extending `p₁` and every `b` extending `p₂` satisfy `a ≠ b`.
- **T10a (Allocator discipline):** Each allocator produces sibling outputs exclusively by `inc(·, 0)`. To spawn a child, it performs one `inc(·, k')` with `k' > 0`.
- **TA5 (Hierarchical increment):** (a) `inc(t, k) > t`; (c) when `k = 0`: `#inc(t, 0) = #t`; (d) when `k > 0`: `#inc(t, k) = #t + k`.

*Proof.* We must show: for any two addresses `a` and `b` produced by distinct allocation events — whether by the same allocator, different allocators at the same level, or allocators at different levels of the hierarchy — `a ≠ b`.

The argument partitions all pairs of distinct allocation events into four exhaustive, mutually exclusive cases based on the relationship between the allocators that produced them: same allocator (Case 1), different allocators with non-nesting prefixes (Case 2), different allocators with nesting prefixes and different zero counts (Case 3), and different allocators with nesting prefixes and the same zero count (Case 4).

*Case 1: Same allocator.* Both `a` and `b` are produced by the same allocator's sequential stream. Since the allocation events are distinct, one was allocated before the other; without loss of generality, `allocated_before(a, b)`. By T9, within a single allocator's stream, `allocated_before(a, b)` implies `a < b`. Since `a < b`, irreflexivity of the strict order (T1, part (a)) gives `a ≠ b`.

*Case 2: Different allocators with non-nesting prefixes.* The two allocators have prefixes `p₁` and `p₂` such that neither is a prefix of the other: `p₁ ⋠ p₂ ∧ p₂ ⋠ p₁`. This arises whenever the allocators are siblings — two users under the same node, two documents under the same user, or any two sub-partitions whose prefixes diverge at some component. By T10, for any tumbler `a` extending `p₁` and any tumbler `b` extending `p₂`, `a ≠ b`. The proof of T10 locates a position `k` where `p₁ₖ ≠ p₂ₖ`, transfers this divergence to `aₖ ≠ bₖ`, and concludes via the T3 contrapositive.

*Case 3: Different allocators with nesting prefixes and different zero counts.* One allocator's prefix nests within the other's, and the two allocators produce addresses at different hierarchical levels. By T4, the zero count `zeros(t)` uniquely determines the hierarchical level: the correspondence is injective, so allocators at different levels produce addresses with `zeros(a) ≠ zeros(b)`.

We show `a ≠ b` by contradiction. Suppose `a = b`. By T3, this requires `#a = #b` and `aᵢ = bᵢ` at every position `1 ≤ i ≤ #a`. If the components are identical at every position, then `{i : aᵢ = 0} = {i : bᵢ = 0}`, giving `zeros(a) = zeros(b)` — contradicting the hypothesis that the allocators operate at different hierarchical levels. Therefore `a ≠ b`.

*Case 4: Different allocators with nesting prefixes and the same zero count.* A parent and a descendant allocator both produce addresses at the same hierarchical level (same zero count). We show that length separation makes collision impossible.

Let the parent allocator have base address `t₀` with `#t₀ = γ`. By T10a, the parent produces its sibling outputs exclusively by repeated application of `inc(·, 0)`. By TA5(c), `inc(t, 0)` preserves length: `#inc(t, 0) = #t`. Applying this inductively — as established in T10a Consequence 1 — every parent sibling output has uniform length `γ`.

To spawn a child allocator, the parent performs one `inc(t, k')` with `k' > 0` for some parent sibling `t` with `#t = γ`. By TA5(d), the child's base address `c₀ = inc(t, k')` has length `#c₀ = γ + k'`. Since `k' ≥ 1`, we have `#c₀ ≥ γ + 1`. The child allocator then produces its own siblings by `inc(·, 0)` (T10a), and by TA5(c) applied inductively, all child sibling outputs have uniform length `γ + k'`.

We establish `a ≠ b` by length separation. Every parent sibling has length `γ`; every child sibling has length `γ + k'` with `k' ≥ 1`, so `γ + k' > γ`. If `a` is a parent output and `b` is a child output (or vice versa), then `#a ≠ #b`, and by the T3 contrapositive, `a ≠ b`.

One pair requires separate treatment: the parent's child-spawning output `c₀ = inc(t, k')` has length `γ + k'` — the same length as the child's sibling outputs. However, `c₀` is the child's base address, not a child sibling output. The child's first sibling is `inc(c₀, 0)`, which satisfies `inc(c₀, 0) > c₀` by TA5(a). By T9, every subsequent child sibling strictly exceeds its predecessor, and therefore strictly exceeds `c₀`. No child sibling equals its own base address; each strictly exceeds it. And `c₀` itself is the parent's output, not a child sibling output, so no double-counting occurs.

The length separation extends inductively across nesting levels. Each child-spawning step via `inc(·, k')` with `k' ≥ 1` adds at least one component (TA5(d)). A descendant `d` nesting levels below the parent produces outputs of length at least `γ + d > γ`. Allocators at different nesting depths produce outputs of different lengths, so they cannot collide by the T3 contrapositive. Allocators at the same depth but on different branches have non-nesting prefixes and are handled by Case 2.

*Exhaustiveness.* Every pair of distinct allocation events falls into exactly one case. If both events belong to the same allocator: Case 1. If the allocators differ: their prefixes either nest or do not. If non-nesting: Case 2. If nesting: the addresses either have different zero counts (Case 3) or the same zero count (Case 4).

*Critical dependence on T10a.* The argument in Case 4 depends on T10a's constraint that sibling allocations use `k = 0`. If a parent allocator could use `k > 0` for siblings, its outputs would have varying lengths — each deep increment extends the tumbler by TA5(d). Some parent output could then match the length of a child output, collapsing the length separation. T10a's necessity proof demonstrates this failure mode explicitly: `inc(t₁, 1)` produces a sibling that is a proper prefix of the next, violating the non-nesting precondition of T10. ∎

This theorem is the foundation of the addressing architecture. Every subsequent guarantee — link stability, transclusion identity, royalty tracing — depends on the uniqueness of addresses. And uniqueness is achieved without any distributed consensus, simply by the structure of the names.

*Formal Contract:*
- *Preconditions:* `a, b ∈ T` produced by distinct allocation events within a system conforming to T10a (allocator discipline).
- *Invariant:* For every pair of addresses `a, b` produced by distinct allocation events in any reachable system state: `a ≠ b`.


## Tumbler arithmetic

We now turn to the arithmetic operations. The system requires operations that advance a position by a displacement (for computing span endpoints and shifting positions) and that recover the displacement between two positions (for computing span widths). These operations — tumbler addition and subtraction — are not arithmetic on numbers but position-advance operations in a hierarchical address space.

A displacement `w` is a tumbler whose leading zeros say "stay at these hierarchical levels" and whose first nonzero component says "advance here." Components after the advance point describe the structure of the landing position within the target region.

### Addition for position advancement

Let `⊕` denote tumbler addition: given a start position `a` and a displacement `w`, compute the advanced position.

We require a notion of where a displacement "acts." For a positive displacement `w = [w₁, w₂, ..., wₙ]`, define the *action point* as `k = min({i : 1 ≤ i ≤ n ∧ wᵢ ≠ 0})` — the position of the first nonzero component. The leading zeros say "stay at these hierarchical levels"; the first nonzero component says "advance here."

**TA0 (Well-defined addition).** For tumblers `a, w ∈ T` where `w > 0` and the action point `k` of `w` satisfies `k ≤ #a`, the result `a ⊕ w` is a well-defined tumbler in `T`.

The precondition `k ≤ #a` is essential: the constructive definition copies components `a₁, ..., aₖ₋₁` from the start position and adds `wₖ` to `aₖ`, so position `k` must exist within `a`. A displacement whose action point exceeds `#a` — one with more leading zeros than `a` has components — would attempt to "stay at" hierarchical levels that the start position does not have, and the operation is undefined.

*Dependencies:*
- **T0 (Carrier-set definition):** T is the set of all finite sequences over ℕ with length ≥ 1; ℕ is closed under addition.
- **TumblerAdd (Constructive definition):** `(a ⊕ w)ᵢ = aᵢ` for `i < k`, `(a ⊕ w)ₖ = aₖ + wₖ`, `(a ⊕ w)ᵢ = wᵢ` for `i > k`; result length `#(a ⊕ w) = #w`.

*Proof.* We show that under the stated preconditions, the constructive rule for `⊕` produces a member of `T` — a finite sequence of natural numbers with length ≥ 1 — and that its length equals `#w`.

Let `a = [a₁, ..., aₘ]` and `w = [w₁, ..., wₙ]`. The action point `k = min({i : 1 ≤ i ≤ n ∧ wᵢ ≠ 0})` — the position of the first nonzero component of `w` — exists because `w > 0` guarantees at least one nonzero component. The precondition requires `k ≤ m`.

The constructive definition (TumblerAdd) builds `r = a ⊕ w = [r₁, ..., rₙ]` by three rules: `rᵢ = aᵢ` for `1 ≤ i < k` (copy from start), `rₖ = aₖ + wₖ` (single-component advance), and `rᵢ = wᵢ` for `k < i ≤ n` (copy from displacement). We must establish two things: that `r ∈ T`, and that `#r = n = #w`.

**Length.** The result has `(k − 1)` prefix components, one action-point component, and `(n − k)` tail components, for a total of `(k − 1) + 1 + (n − k) = n`. Since `w ∈ T` requires `n ≥ 1` by the carrier-set definition, the result has at least one component. So `#r = n = #w`.

**Components.** We verify `rᵢ ∈ ℕ` for each of the three regions.

*(i) Prefix, `1 ≤ i < k`.* Each `rᵢ = aᵢ` by TumblerAdd's prefix-copy rule. The precondition `k ≤ m` ensures position `i < k ≤ m` exists within `a`, and since `a ∈ T`, each `aᵢ ∈ ℕ` by the carrier-set definition. So `rᵢ ∈ ℕ`.

*(ii) Action point, `i = k`.* `rₖ = aₖ + wₖ` by TumblerAdd's advance rule. We have `aₖ ∈ ℕ` (since `k ≤ m` and `a ∈ T`) and `wₖ ∈ ℕ` (since `k ≤ n` and `w ∈ T`). The natural numbers are closed under addition, so `aₖ + wₖ ∈ ℕ`.

*(iii) Tail, `k < i ≤ n`.* Each `rᵢ = wᵢ` by TumblerAdd's tail-copy rule. Since `w ∈ T`, each `wᵢ ∈ ℕ` by the carrier-set definition. So `rᵢ ∈ ℕ`.

The result `r` is a finite sequence of natural numbers with length `n ≥ 1` — a member of `T` by the carrier-set definition, with `#r = #w`. ∎

*Formal Contract:*
- *Preconditions:* `a ∈ T`, `w ∈ T`, `w > 0`, `actionPoint(w) ≤ #a`
- *Postconditions:* `a ⊕ w ∈ T`, `#(a ⊕ w) = #w`

**TA1 (Order preservation under addition).** `(A a, b, w : a < b ∧ w > 0 ∧ k ≤ min(#a, #b) : a ⊕ w ≤ b ⊕ w)`, where `k` is the action point of `w`.

TA1 guarantees weak (`≤`) order preservation: if two positions were ordered before advancement by the same displacement, they remain non-reversed after. The precondition `k ≤ min(#a, #b)` ensures both additions are well-defined per TA0.

*Dependencies:*
- **TA0 (Well-defined addition):** `a ⊕ w ∈ T` when `w > 0` and `actionPoint(w) ≤ #a`; result length `#(a ⊕ w) = #w`.
- **TumblerAdd (Constructive definition):** `(x ⊕ w)ᵢ = xᵢ` for `i < k`, `(x ⊕ w)ₖ = xₖ + wₖ`, `(x ⊕ w)ᵢ = wᵢ` for `i > k`, where `k = actionPoint(w)`.
- **T1 (Lexicographic order):** `a < b` iff `∃ k ≥ 1` with agreement before `k` and either (i) `k ≤ min(#a, #b)` and `aₖ < bₖ`, or (ii) `k = #a + 1 ≤ #b`.
- **T3 (Canonical representation):** `a = b ⟺ #a = #b ∧ (A i : 1 ≤ i ≤ #a : aᵢ = bᵢ)`.

*Proof.* We must show: for all `a, b, w ∈ T` with `a < b`, `w > 0`, and action point `k ≤ min(#a, #b)`, the advanced positions satisfy `a ⊕ w ≤ b ⊕ w`.

Let `k` be the action point of `w`. Since `k ≤ min(#a, #b)`, the precondition of TA0 is satisfied for both `a` and `b`, so `a ⊕ w` and `b ⊕ w` are well-defined members of T, each with length `#w`. TumblerAdd builds each result in three regions relative to `k`: for `i < k`, `(x ⊕ w)ᵢ = xᵢ` (prefix copy); at `i = k`, `(x ⊕ w)ₖ = xₖ + wₖ` (advance); for `i > k`, `(x ⊕ w)ᵢ = wᵢ` (tail from displacement).

Since `a < b`, T1 provides exactly two cases: either (i) there exists a least position `j` with `j ≤ min(#a, #b)` where `aⱼ < bⱼ` and `aᵢ = bᵢ` for all `i < j`, or (ii) `a` is a proper prefix of `b` — that is, `#a < #b` and `aᵢ = bᵢ` for all `1 ≤ i ≤ #a`.

*Case (ii): `a` is a proper prefix of `b`.* Here `min(#a, #b) = #a`, so `k ≤ #a`, and the prefix condition gives `aᵢ = bᵢ` for all `1 ≤ i ≤ #a`. Since `k ≤ #a`, the action point falls within the range of agreement, and TumblerAdd consults only positions `1, ..., k` from `a` and `b`. We verify component-wise equality. For `i < k`: TumblerAdd's prefix-copy rule gives `(a ⊕ w)ᵢ = aᵢ = bᵢ = (b ⊕ w)ᵢ`, where the middle equality holds because `i < k ≤ #a` places `i` within the prefix range. At `i = k`: TumblerAdd's advance rule gives `(a ⊕ w)ₖ = aₖ + wₖ = bₖ + wₖ = (b ⊕ w)ₖ`, since `aₖ = bₖ` (as `k ≤ #a`). For `i > k`: TumblerAdd's tail-copy rule gives `(a ⊕ w)ᵢ = wᵢ = (b ⊕ w)ᵢ`. Both results have length `#w` by TA0 and every component agrees, so `a ⊕ w = b ⊕ w` by T3. Equality satisfies `≤`.

*Case (i): component divergence at position `j`.* Here `j ≤ min(#a, #b)`, `aⱼ < bⱼ`, and `aᵢ = bᵢ` for all `i < j`. Three sub-cases arise from the relationship between the first divergence `j` and the action point `k`.

*Sub-case `j < k`.* Position `j` lies in TumblerAdd's prefix-copy region, so `(a ⊕ w)ⱼ = aⱼ` and `(b ⊕ w)ⱼ = bⱼ`, giving `(a ⊕ w)ⱼ = aⱼ < bⱼ = (b ⊕ w)ⱼ`. For all `i < j`: since `i < j < k`, both positions fall in the prefix-copy region, and the agreement condition `aᵢ = bᵢ` gives `(a ⊕ w)ᵢ = aᵢ = bᵢ = (b ⊕ w)ᵢ`. Since `j < k ≤ #w` and both results have length `#w` by TA0, position `j` is shared by both results and satisfies `j ≤ min(#(a ⊕ w), #(b ⊕ w))`. Position `j` witnesses T1 case (i) for `a ⊕ w < b ⊕ w`, and strict inequality satisfies `≤`.

*Sub-case `j = k`.* For all `i < k = j`: both positions fall in the prefix-copy region, and the agreement condition gives `(a ⊕ w)ᵢ = aᵢ = bᵢ = (b ⊕ w)ᵢ`. At position `k`: TumblerAdd's advance rule gives `(a ⊕ w)ₖ = aₖ + wₖ` and `(b ⊕ w)ₖ = bₖ + wₖ`. Since `aₖ < bₖ` (the divergence at `j = k`) and addition of a fixed natural number preserves strict inequality on ℕ — if `x < y` then `x + c < y + c` for all `c ∈ ℕ` — we have `aₖ + wₖ < bₖ + wₖ`. Since `k ≤ #w` and both results have length `#w` by TA0, position `k` satisfies `k ≤ min(#(a ⊕ w), #(b ⊕ w))`. Position `k` witnesses T1 case (i) for `a ⊕ w < b ⊕ w`, and strict inequality satisfies `≤`.

*Sub-case `j > k`.* Since `k < j` and `aᵢ = bᵢ` for all `i < j`, in particular `aₖ = bₖ` (because `k < j`). We verify component-wise equality of the two results. For `i < k`: both positions fall in the prefix-copy region, and `i < k < j` gives `aᵢ = bᵢ`, so `(a ⊕ w)ᵢ = aᵢ = bᵢ = (b ⊕ w)ᵢ`. At `i = k`: TumblerAdd's advance rule gives `(a ⊕ w)ₖ = aₖ + wₖ = bₖ + wₖ = (b ⊕ w)ₖ`, since `aₖ = bₖ`. For `i > k`: TumblerAdd's tail-copy rule gives `(a ⊕ w)ᵢ = wᵢ = (b ⊕ w)ᵢ`. Both results have length `#w` by TA0 and every component agrees, so `a ⊕ w = b ⊕ w` by T3. Equality satisfies `≤`.

In every case and sub-case, `a ⊕ w ≤ b ⊕ w`. ∎

*Formal Contract:*
- *Preconditions:* `a ∈ T`, `b ∈ T`, `w ∈ T`, `a < b`, `w > 0`, `actionPoint(w) ≤ min(#a, #b)`
- *Postconditions:* `a ⊕ w ≤ b ⊕ w`

Strict order preservation holds under a tighter condition. We first need a precise notion of where two tumblers first differ.

**Definition (Divergence).** For tumblers `a, b ∈ T` with `a ≠ b`, the *divergence* `divergence(a, b)` is defined by two cases corresponding to the two cases of T1:

  (i) If there exists `k ≤ min(#a, #b)` such that `aₖ ≠ bₖ` and `(A i : 1 ≤ i < k : aᵢ = bᵢ)`, then `divergence(a, b) = k` — component divergence at a shared position.

  (ii) If `(A i : 1 ≤ i ≤ min(#a, #b) : aᵢ = bᵢ)` and `#a ≠ #b`, then `divergence(a, b) = min(#a, #b) + 1` — prefix divergence, where one tumbler is a proper prefix of the other.

Exactly one case applies for any `a ≠ b`. In case (i), `a` and `b` differ at a component both possess. In case (ii), they agree on all shared positions but one is longer — the divergence lies "just past" the shorter tumbler's last component.

For prefix-related pairs, `divergence(a, b) = min(#a, #b) + 1 > min(#a, #b)`. Since TA0 requires `k ≤ min(#a, #b)`, the condition `k ≥ divergence(a, b)` in TA1-strict below is unsatisfiable for prefix-related operands. This is correct: when `a` is a proper prefix of `b` (or vice versa), Case 1 of the verification below shows that addition erases the divergence, producing equality rather than strict inequality. TA1-strict makes no claim about prefix-related pairs — TA1 (weak) covers them, guaranteeing non-reversal.

*Formal Contract:*
- *Preconditions:* a ∈ T, b ∈ T, a ≠ b
- *Definition:* divergence(a, b) = k, where (i) if ∃ i with 1 ≤ i ≤ min(#a, #b) and aᵢ ≠ bᵢ, then k = min({i : 1 ≤ i ≤ min(#a, #b) ∧ aᵢ ≠ bᵢ}); (ii) if (A i : 1 ≤ i ≤ min(#a, #b) : aᵢ = bᵢ) and #a ≠ #b, then k = min(#a, #b) + 1

**TA1-strict (Strict order preservation).** `(A a, b, w : a < b ∧ w > 0 ∧ k ≤ min(#a, #b) ∧ k ≥ divergence(a, b) : a ⊕ w < b ⊕ w)`, where `k` is the action point of `w`.

When the action point falls before the divergence — `k < divergence(a, b)` — both operands agree at position `k`, both get the same `wₖ` added, and both copy the same tail from `w` afterward. The original divergence is erased and the results are equal. For example, `a = [1, 3]`, `b = [1, 5]` (diverge at position 2), `w = [2]` (action point at position 1): `a ⊕ w = [3] = b ⊕ w`. Order degrades to equality, never reversal.

*Dependencies:*
- **TA0 (Well-defined addition):** `a ⊕ w ∈ T` when `w > 0` and `actionPoint(w) ≤ #a`; result length `#(a ⊕ w) = #w`.
- **TumblerAdd (Constructive definition):** `(x ⊕ w)ᵢ = xᵢ` for `i < k`, `(x ⊕ w)ₖ = xₖ + wₖ`, `(x ⊕ w)ᵢ = wᵢ` for `i > k`, where `k = actionPoint(w)`.
- **T1 (Lexicographic order):** `a < b` iff `∃ k ≥ 1` with agreement before `k` and either (i) `k ≤ min(#a, #b)` and `aₖ < bₖ`, or (ii) `k = #a + 1 ≤ #b`.
- **Divergence definition:** For `a ≠ b`, `divergence(a, b)` is the least `k` where they differ; in case (i) `k ≤ min(#a, #b)` with `aₖ ≠ bₖ` and `aᵢ = bᵢ` for `i < k`; in case (ii) `k = min(#a, #b) + 1`.

*Proof.* We show that tumbler addition by `w` preserves the strict inequality `a < b` whenever the action point of `w` falls at or beyond the first disagreement between `a` and `b`.

Let `j = divergence(a, b)` and let `k` be the action point of `w`. The precondition `a < b` gives `a ≠ b` by T1 irreflexivity, so `divergence(a, b)` is well-defined. The remaining preconditions give `k ≥ j` and `k ≤ min(#a, #b)`. From these bounds, `j ≤ min(#a, #b)`, which rules out Divergence case (ii) — that case requires `j = min(#a, #b) + 1 > min(#a, #b)` — and places us in case (i): position `j` is shared by both tumblers, `aⱼ ≠ bⱼ`, and `aᵢ = bᵢ` for all `i < j`. Since `a < b` and `j` is the least position where `a` and `b` differ, the T1 witness for the ordering must be `j`; case (i) of T1 then gives `aⱼ < bⱼ`.

By TA0, both `a ⊕ w` and `b ⊕ w` are well-defined members of T with length `#w`, since `k ≤ min(#a, #b)` ensures the action point falls within both operands. TumblerAdd's constructive definition builds each result in three regions relative to `k`: `(x ⊕ w)ᵢ = xᵢ` for `i < k` (prefix copy), `(x ⊕ w)ₖ = xₖ + wₖ` (single-component advance), and `(x ⊕ w)ᵢ = wᵢ` for `i > k` (tail from displacement). Two cases arise from the relationship between `k` and `j`.

*Case 1: `k = j`.* For `i < k`: since `i < j = k`, the Divergence case (i) agreement condition gives `aᵢ = bᵢ`, and TumblerAdd's prefix-copy rule gives `(a ⊕ w)ᵢ = aᵢ = bᵢ = (b ⊕ w)ᵢ`. At position `k = j`: TumblerAdd's advance rule gives `(a ⊕ w)ₖ = aₖ + wₖ` and `(b ⊕ w)ₖ = bₖ + wₖ`. Since `aₖ < bₖ` (established above) and natural-number addition preserves strict inequality — `x < y` implies `x + c < y + c` for all `c ∈ ℕ` — we have `aₖ + wₖ < bₖ + wₖ`. The results agree on all positions before `k` and satisfy `(a ⊕ w)ₖ < (b ⊕ w)ₖ` at position `k`. Since `k ≤ #w = #(a ⊕ w) = #(b ⊕ w)`, position `k` is shared by both results, and T1 case (i) gives `a ⊕ w < b ⊕ w`.

*Case 2: `k > j`.* For all positions `i < k`: TumblerAdd's prefix-copy rule gives `(a ⊕ w)ᵢ = aᵢ` and `(b ⊕ w)ᵢ = bᵢ`. Since `j < k`, position `j` lies in this prefix-copy region, so `(a ⊕ w)ⱼ = aⱼ < bⱼ = (b ⊕ w)ⱼ` — the divergence inequality is preserved by prefix copy. For all `i < j`: the Divergence case (i) agreement condition gives `aᵢ = bᵢ`, so `(a ⊕ w)ᵢ = aᵢ = bᵢ = (b ⊕ w)ᵢ`. The results agree on all positions before `j` and satisfy `(a ⊕ w)ⱼ < (b ⊕ w)ⱼ` at position `j`. Since `j ≤ k ≤ #w = #(a ⊕ w) = #(b ⊕ w)`, position `j` is shared by both results, and T1 case (i) gives `a ⊕ w < b ⊕ w`.

In both cases, `a ⊕ w < b ⊕ w`. ∎

*Formal Contract:*
- *Preconditions:* a ∈ T, b ∈ T, w ∈ T, a < b, w > 0, actionPoint(w) ≤ min(#a, #b), actionPoint(w) ≥ divergence(a, b)
- *Postconditions:* a ⊕ w < b ⊕ w

But TA1 alone does not guarantee that addition *advances* a position. It preserves relative order between two positions but is silent about the relationship between `a` and `a ⊕ w`. We need:

**TA-strict (Strict increase).** `(A a ∈ T, w > 0 : a ⊕ w > a)` (where `a ⊕ w` is well-defined, i.e., `k ≤ #a` per TA0).

Without TA-strict, the axioms admit a degenerate model in which `a ⊕ w = a` for all `a, w`. This no-op model satisfies TA0 (result is in T), TA1 (if `a < b` then `a < b` — the consequent is unchanged), and TA4 (`(a ⊕ w) ⊖ w = a ⊖ w = a` if subtraction is equally degenerate). Every axiom is satisfied, yet spans are empty — the interval `[s, s ⊕ ℓ)` collapses to `[s, s)`. TA-strict excludes this model and ensures that advancing by a positive displacement moves forward. T12 (span well-definedness) depends on this directly.

*Dependencies:*
- **T0(a) (Carrier-set definition):** T is the set of all finite sequences over ℕ with length ≥ 1.
- **T1 (Lexicographic order):** `a < b` iff there exists `k ≥ 1` with `aᵢ = bᵢ` for all `i < k` and either (i) `k ≤ min(#a, #b)` and `aₖ < bₖ`, or (ii) `k = #a + 1 ≤ #b`.
- **TA0 (Well-defined addition):** For `a, w ∈ T` with `w > 0` and action point `k ≤ #a`, `a ⊕ w ∈ T` with `#(a ⊕ w) = #w`.
- **TumblerAdd (Constructive definition):** `(a ⊕ w)ᵢ = aᵢ` for `i < k`, `(a ⊕ w)ₖ = aₖ + wₖ`, `(a ⊕ w)ᵢ = wᵢ` for `i > k`; result length `#(a ⊕ w) = #w`.

*Proof.* We show that for all `a ∈ T` and `w > 0` with action point `k ≤ #a`, the result `r = a ⊕ w` satisfies `r > a` under the lexicographic order T1.

Let `a = [a₁, ..., aₘ]` and `w = [w₁, ..., wₙ]` with `w > 0`. The action point `k = min({i : 1 ≤ i ≤ n ∧ wᵢ ≠ 0})` exists because `w > 0` ensures at least one nonzero component, and the TA0 precondition gives `k ≤ m`. Write `r = a ⊕ w`. By TA0, `r ∈ T` with `#r = n`, so both `a` and `r` are members of T and the T1 comparison is well-defined.

The TumblerAdd construction defines `r` in three regions: `rᵢ = aᵢ` for `1 ≤ i < k` (prefix copy), `rₖ = aₖ + wₖ` (single-component advance), and `rᵢ = wᵢ` for `k < i ≤ n` (tail copy). We produce a witness for `a < r` under T1 case (i) at position `k`.

*Agreement before position `k`.* For every `i` with `1 ≤ i < k`, `rᵢ = aᵢ` by TumblerAdd's prefix-copy rule — the construction reproduces the start position exactly through position `k − 1`. This establishes the T1 prefix-agreement condition `(A i : 1 ≤ i < k : aᵢ = rᵢ)`.

*Strict increase at position `k`.* By definition of action point, `wₖ > 0`. Since `aₖ ∈ ℕ` (because `k ≤ m` and `a ∈ T`) and `wₖ ∈ ℕ` with `wₖ > 0`, the sum `aₖ + wₖ > aₖ` — adding a positive natural number to a non-negative one yields a strictly larger result. Therefore `rₖ = aₖ + wₖ > aₖ`, i.e., `aₖ < rₖ`.

*Applicability of T1 case (i).* Position `k` must satisfy `k ≤ min(#a, #r)`. We have `k ≤ m = #a` by the TA0 precondition, and `k ≤ n = #r` because `k` is a valid index into `w` and `#r = #w = n` by TA0. So `k ≤ min(#a, #r)`.

We now have a witness for T1 case (i) at position `k`: `aᵢ = rᵢ` for all `i < k`, and `aₖ < rₖ`, with `k ≤ min(#a, #r)`. By T1, `a < r`, i.e., `a < a ⊕ w`, which is equivalently `a ⊕ w > a`. ∎

*Formal Contract:*
- *Preconditions:* `a ∈ T`, `w ∈ T`, `w > 0`, `k ≤ #a` where `k` is the action point of `w`
- *Postconditions:* `a ⊕ w > a`

### Subtraction for width computation

Let `⊖` denote tumbler subtraction: given two positions, compute the displacement between them.

**TA2 (Well-defined subtraction).** For tumblers `a, w ∈ T` where `a ≥ w`, `a ⊖ w` is a well-defined tumbler in `T`.

*Dependencies:*
- **T0(a) (Carrier-set definition):** T is the set of all finite sequences over ℕ with length ≥ 1.
- **T1 (Lexicographic order):** The total order on T, defining `a < b` by first divergence position.
- **T3 (Canonical representation):** `a = b ⟺ #a = #b ∧ (A i : 1 ≤ i ≤ #a : aᵢ = bᵢ)`.
- **TumblerSub (Constructive definition):** Zero-pad both operands to length `p = max(#a, #w)`. If the padded sequences agree everywhere, the result is the zero tumbler of length `p`. Otherwise, let `k` be the first position where they disagree; then `rᵢ = 0` for `i < k`, `rₖ = aₖ - wₖ`, `rᵢ = aᵢ` for `i > k` (all under zero-padding), with `#r = p`.

*Proof.* We show that for all `a, w ∈ T` with `a ≥ w`, the construction TumblerSub produces a member of T — a finite sequence of non-negative integers with at least one component — and that `#(a ⊖ w) = max(#a, #w)`.

Let `a ∈ T` and `w ∈ T` with `a ≥ w`. Write `p = max(#a, #w)`. TumblerSub zero-pads both operands to length `p` and scans for the first position at which the padded sequences disagree. Two cases exhaust the possibilities.

*Case 1: no divergence (zero-padded equality).* The padded sequences of `a` and `w` agree at every position. TumblerSub produces the zero tumbler `r = [0, ..., 0]` of length `p`. Since `#a ≥ 1` and `#w ≥ 1` (both are members of T by T0(a)), `p ≥ 1`. Each component is `0 ∈ ℕ`. The result is a finite sequence over ℕ with length ≥ 1 — a member of T by T0(a), with `#r = p = max(#a, #w)`.

*Case 2: divergence at position `k`.* The padded sequences agree at all positions `i < k` and first disagree at `k`. TumblerSub defines the result `r = a ⊖ w` componentwise: `rᵢ = 0` for `i < k`, `rₖ = aₖ - wₖ`, and `rᵢ = aᵢ` for `i > k` (all under zero-padding), with `#r = p`. We verify that every component belongs to ℕ, treating the three regions in turn.

*Pre-divergence* (`i < k`): `rᵢ = 0 ∈ ℕ` by construction.

*Divergence point* (`i = k`): We must show `aₖ ≥ wₖ` (zero-padded values) so that `rₖ = aₖ - wₖ` is a well-defined member of ℕ. The padded sequences disagree at `k`, so the operands are not zero-padded-equal. We claim `a ≠ w` as tumblers: if `a = w`, then T3 gives `#a = #w` and `aᵢ = wᵢ` for all `1 ≤ i ≤ #a`, so the padded sequences — identical to the originals through position `#a = #w` and both zero beyond — agree everywhere, contradicting the divergence at `k`. Therefore `a ≠ w`, and since `a ≥ w` by hypothesis, `a > w` under T1. We show the T1 witness for `a > w` coincides with the padded divergence `k` and yields `aₖ > wₖ`.

*Sub-case (i): T1 case (i) — component divergence.* There exists a least `j ≤ min(#a, #w)` with `aⱼ > wⱼ` and `aᵢ = wᵢ` for all `i < j`. Since `j ≤ min(#a, #w)`, both values are original components, so zero-padding does not alter them. The padded sequences agree before `j` and disagree at `j`, making `j` the first padded divergence: `k = j`. At position `k`, `aₖ > wₖ`, so `rₖ = aₖ - wₖ ∈ ℕ`.

*Sub-case (ii): T1 case (ii) — prefix relationship.* Here `w` is a proper prefix of `a`: `#w < #a` and `aᵢ = wᵢ` for all `i ≤ #w`. Zero-padding extends `w` with zeros at positions `#w + 1` through `p = #a`. The padded sequences agree at all positions `i ≤ #w`. The divergence `k` falls at the first position `i > #w` where `aᵢ > 0` — such a position must exist, for if `aᵢ = 0` at every `i > #w`, the padded sequences would agree everywhere, contradicting the case hypothesis. At position `k`, `aₖ > 0 = wₖ` (the zero-padded value), so `rₖ = aₖ - 0 = aₖ ∈ ℕ`.

*Tail* (`i > k`): `rᵢ = aᵢ` (zero-padded). If `i ≤ #a`, then `aᵢ` is a component of `a ∈ T`, hence `aᵢ ∈ ℕ` by T0(a). If `i > #a`, then the zero-padded value is `0 ∈ ℕ`.

The result `r` has length `p = max(#a, #w) ≥ 1` with every component in ℕ — a member of T by T0(a), with `#r = p = max(#a, #w)`.

In both cases, `a ⊖ w ∈ T` with `#(a ⊖ w) = max(#a, #w)`. ∎

*Formal Contract:*
- *Preconditions:* `a ∈ T`, `w ∈ T`, `a ≥ w`
- *Postconditions:* `a ⊖ w ∈ T`, `#(a ⊖ w) = max(#a, #w)`

**TA3 (Order preservation under subtraction, weak).** `(A a, b, w : a < b ∧ a ≥ w ∧ b ≥ w : a ⊖ w ≤ b ⊖ w)`.

*Dependencies:*
- **T1 (Lexicographic order):** `a < b` iff there exists `k ≥ 1` with `aᵢ = bᵢ` for all `i < k`, and either (i) `k ≤ min(#a, #b)` and `aₖ < bₖ`, or (ii) `k = #a + 1 ≤ #b` (proper prefix).
- **TA2 (Well-defined subtraction):** For `a ≥ w`, `a ⊖ w ∈ T` with `#(a ⊖ w) = max(#a, #w)`.
- **TA6 (Zero tumblers):** Every zero tumbler is less than every positive tumbler under T1.
- **TumblerSub (Constructive definition):** Zero-pad both operands to length `p = max(#a, #w)`. If the padded sequences agree everywhere, the result is the zero tumbler of length `p`. Otherwise, let `d` be the first divergence; then `rᵢ = 0` for `i < d`, `r_d = a_d - w_d`, `rᵢ = aᵢ` for `i > d` (all under zero-padding), with `#r = p`.

*Proof.* We show that for all `a, b, w ∈ T` with `a < b`, `a ≥ w`, and `b ≥ w`, subtracting the common lower bound preserves the ordering: `a ⊖ w ≤ b ⊖ w`.

**Preliminaries.** By TA2, since `a ≥ w` and `b ≥ w`, both `a ⊖ w` and `b ⊖ w` are well-formed members of T, so the comparison under T1 is well-defined. We recall TumblerSub for self-containment: given `x ≥ w`, zero-pad both to length `max(#x, #w)` and find the first position `d` where the padded sequences disagree. If no such position exists (`x` is *zero-padded-equal* to `w`), the result is the zero tumbler of length `max(#x, #w)`. Otherwise: `(x ⊖ w)ᵢ = 0` for `i < d`, `(x ⊖ w)_d = x_d - w_d`, and `(x ⊖ w)ᵢ = xᵢ` for `i > d` (under zero-padding), with `#(x ⊖ w) = max(#x, #w)`.

Since `a < b`, T1 provides two exhaustive forms: (i) there exists a first position `j ≤ min(#a, #b)` with `aⱼ < bⱼ`, or (ii) `a` is a proper prefix of `b` — `#a < #b` and `aᵢ = bᵢ` for all `i ≤ #a`. We treat each in turn, partitioning further by the divergence structure of the operands against `w`.

**Case A: `a` is a proper prefix of `b`** (T1 case (ii)). Then `#a < #b` and `aᵢ = bᵢ` for all `i ≤ #a`.

*Sub-case A1: `a = w`.* Since the operands are identical, `a ⊖ w` is the zero tumbler of length `#a`. Since `a = w` and `a` is a proper prefix of `b`, we have `bᵢ = wᵢ` for all `i ≤ #w = #a`. If some `bᵢ > 0` for `i > #w`, then `(b, w)` diverges beyond `#w`, making `b ⊖ w` a positive tumbler; by TA6 the zero tumbler `a ⊖ w` is strictly less. If `bᵢ = 0` for all `i > #w`, the padded sequences agree everywhere, so `b ⊖ w` is the zero tumbler of length `max(#b, #w) = #b`. Both results are zero tumblers with `#(a ⊖ w) = #a < #b = #(b ⊖ w)`, so `a ⊖ w` is a proper prefix of `b ⊖ w`, giving `a ⊖ w < b ⊖ w` by T1 case (ii).

*Sub-case A2: `a > w` with divergence.* Let `dₐ` be the first position where the zero-padded sequences of `a` and `w` disagree. We show `dₐ ≤ #a`. If `a > w` by T1 case (i), the witness satisfies `dₐ ≤ min(#a, #w) ≤ #a`. If by T1 case (ii), `w` is a proper prefix of `a` and `dₐ` is the first `i > #w` with `aᵢ > 0`, so `dₐ ≤ #a`.

Since `bᵢ = aᵢ` for all `i ≤ #a` and `dₐ ≤ #a`, the zero-padded comparison of `b` against `w` agrees with that of `a` against `w` at every position through `dₐ`. The pair `(b, w)` therefore diverges at the same position: write `d = dₐ = d_b`.

Apply TumblerSub to both pairs. At positions `i < d`: both results are `0`. At position `d`: both yield `a_d - w_d = b_d - w_d`, since `a_d = b_d` (as `d ≤ #a`). At positions `d < i ≤ #a`: both are in the tail-copy phase, yielding `aᵢ = bᵢ`. The two results agree on all positions `1` through `#a`.

Beyond position `#a`, the zero-padded value of `a` is `0` everywhere, so `(a ⊖ w)_i = 0` for all `i > #a` within the result. Meanwhile `(b ⊖ w)_i ∈ ℕ`, so `0 ≤ (b ⊖ w)_i` at every shared position. Write `L_a = #(a ⊖ w) = max(#a, #w)` and `L_b = #(b ⊖ w) = max(#b, #w)`; since `#b > #a`, we have `L_b ≥ L_a`. Three exhaustive sub-sub-cases complete the comparison. If the results first disagree at some position `p > #a` with `(a ⊖ w)_p = 0 < (b ⊖ w)_p`, T1 case (i) gives `a ⊖ w < b ⊖ w`. If the results agree on all positions `1, ..., L_a` and `L_a < L_b`, then `a ⊖ w` is a proper prefix of `b ⊖ w`, giving `a ⊖ w < b ⊖ w` by T1 case (ii). If the results agree on all positions and `L_a = L_b`, then `a ⊖ w = b ⊖ w` and `≤` holds.

*Sub-case A3: `a > w` without divergence (zero-padded equality).* Since `a > w` yet the padded sequences agree everywhere, the ordering must come from T1 case (ii): `w` is a proper prefix of `a` with `aᵢ = 0` for all `i > #w` (otherwise a divergence would exist). The subtraction `a ⊖ w` yields the zero tumbler of length `#a`.

Since `a` is a proper prefix of `b`, `bᵢ = aᵢ = wᵢ` for all `i ≤ #a`. The result `b ⊖ w` has length `max(#b, #w) = #b > #a`. If `b ⊖ w` has any positive component, TA6 gives `a ⊖ w < b ⊖ w` (since `a ⊖ w` is a zero tumbler). If `b ⊖ w` is also a zero tumbler, then `#(a ⊖ w) = #a < #b = #(b ⊖ w)`, making `a ⊖ w` a proper prefix of `b ⊖ w`, so `a ⊖ w < b ⊖ w` by T1 case (ii).

In all sub-cases of Case A, `a ⊖ w ≤ b ⊖ w`.

**Case B: Component divergence at `j`** (T1 case (i)). There exists a first position `j ≤ min(#a, #b)` with `aⱼ < bⱼ` and `aᵢ = bᵢ` for all `i < j`.

*Sub-case B1: `a` is zero-padded-equal to `w`.* Then `a ⊖ w` is the zero tumbler of length `max(#a, #w)`. Zero-padded equality gives `wⱼ = aⱼ`, so `bⱼ > aⱼ = wⱼ`, and the pair `(b, w)` diverges at or before `j`. This makes `b ⊖ w` a positive tumbler. By TA6, `a ⊖ w < b ⊖ w`.

For the remaining sub-cases, `a` is not zero-padded-equal to `w`, so `dₐ = divergence(a, w)` is well-defined. We show that `d_b = divergence(b, w)` also exists: if `b` were zero-padded-equal to `w`, then `a_{dₐ} > w_{dₐ} = b_{dₐ}` (from `a ≥ w` at the divergence), while `aᵢ = wᵢ = bᵢ` for all `i < dₐ`, giving `a > b` by T1 — contradicting `a < b`. So `d_b` is well-defined.

*Sub-case B2: `dₐ = d_b = d`.* Both operands diverge from `w` at position `d`. At positions `i < d`, both results are `0`. Since `a` and `b` both agree with `w` before `d`, they agree with each other there, so the first `a`-vs-`b` disagreement satisfies `j ≥ d`.

If `j = d`: `(a ⊖ w)_d = a_d - w_d` and `(b ⊖ w)_d = b_d - w_d`. Since `a_d < b_d` (from `j = d`), subtracting the same `w_d` preserves the strict inequality: `a_d - w_d < b_d - w_d`. All prior positions are `0 = 0`. By T1 case (i), `a ⊖ w < b ⊖ w`.

If `j > d`: `a_d = b_d` (since `d < j`), so both results agree at `d`. At positions `d < i < j`, both are in the tail-copy phase: `(a ⊖ w)_i = a_i` and `(b ⊖ w)_i = b_i`, with `a_i = b_i` since `i < j`. At position `j`, both remain in tail-copy: `(a ⊖ w)_j = a_j < b_j = (b ⊖ w)_j`. The first disagreement between the results is at `j`. By T1 case (i), `a ⊖ w < b ⊖ w`.

*Sub-case B3: `dₐ < d_b`.* At position `dₐ`, the padded value of `a` disagrees with `w` but `b`'s padded value agrees with `w`. Since `a` and `b` both agree with `w` before `dₐ`, the first disagreement between `a` and `b` is at `dₐ`, so `j = dₐ`. This gives `a_{dₐ} < b_{dₐ} = w_{dₐ}`. But `a ≥ w` and the first padded divergence of `(a, w)` is at `dₐ`, so `a_{dₐ} ≥ w_{dₐ}` — contradiction. This case is impossible.

*Sub-case B4: `dₐ > d_b`.* At position `d_b`, the padded value of `b` disagrees with `w` but `a`'s padded value agrees with `w`. Since both agree with `w` before `d_b`, the first `a`-vs-`b` disagreement is at `d_b`, giving `j = d_b` with `a_{d_b} = w_{d_b} < b_{d_b}` — the strict inequality holds because `b ≥ w` and `d_b` is the first divergence of `(b, w)`, requiring `b_{d_b} > w_{d_b}`.

For `a ⊖ w`: position `d_b` falls before `dₐ`, in the pre-divergence zero phase, so `(a ⊖ w)_{d_b} = 0`. For `b ⊖ w`: `d_b` is the divergence point, so `(b ⊖ w)_{d_b} = b_{d_b} - w_{d_b} > 0`. At all positions `i < d_b`, both results are `0`. The first disagreement is at `d_b` with `0 < b_{d_b} - w_{d_b}`. By T1 case (i), `a ⊖ w < b ⊖ w`.

In every case, `a ⊖ w ≤ b ⊖ w`. ∎

*Formal Contract:*
- *Preconditions:* a ∈ T, b ∈ T, w ∈ T, a < b, a ≥ w, b ≥ w
- *Postconditions:* a ⊖ w ≤ b ⊖ w

**TA3-strict (Order preservation under subtraction, strict).** `(A a, b, w : a < b ∧ a ≥ w ∧ b ≥ w ∧ #a = #b : a ⊖ w < b ⊖ w)`.

We prove that subtracting a common lower bound from two equal-length tumblers preserves strict order: if `a` precedes `b`, both dominate `w`, and `#a = #b`, then `a ⊖ w` strictly precedes `b ⊖ w`.

*Proof.* We are given `a, b, w ∈ T` with `a < b`, `a ≥ w`, `b ≥ w`, and `#a = #b`. We must show `a ⊖ w < b ⊖ w`.

**Preliminaries.** We recall the definitions on which the argument depends. T1 defines `a < b` by: there exists a least `k ≥ 1` with `aᵢ = bᵢ` for all `i < k`, and either (i) `k ≤ min(#a, #b)` with `aₖ < bₖ`, or (ii) `k = #a + 1 ≤ #b` (`a` a proper prefix of `b`). TumblerSub defines `x ⊖ w` (for `x ≥ w`) by zero-padding both operands to length `max(#x, #w)` and scanning for the first position where the padded sequences disagree. If no disagreement exists (*zero-padded equality*), the result is the zero tumbler of length `max(#x, #w)`. If divergence occurs at position `d`, the result `r` satisfies: `rᵢ = 0` for `i < d`, `r_d = x_d - w_d`, and `rᵢ = xᵢ` for `i > d`, with `#r = max(#x, #w)`.

**The form of `a < b`.** Since `#a = #b`, T1 case (ii) is impossible — it requires `#a < #b`. So `a < b` holds by case (i): there exists a least `j` with `1 ≤ j ≤ #a` such that `aᵢ = bᵢ` for all `i < j` and `aⱼ < bⱼ`. We fix this `j` throughout.

**Well-formedness.** By TA2, both `a ⊖ w` and `b ⊖ w` are well-defined members of `T`.

We proceed by exhaustive case analysis on the divergence structure of the pairs `(a, w)` and `(b, w)` under zero-padding.

**Case A: `a` is zero-padded-equal to `w`.** By TumblerSub, `a ⊖ w` is the zero tumbler of length `max(#a, #w)`. For `i < j`: `b_i = a_i` (from T1) and `a_i = w_i` (zero-padded equality), so `b_i = w_i`. At position `j`: `w_j = a_j` (zero-padded equality) and `b_j > a_j` (from `a < b`), giving `b_j > w_j`. So `(b, w)` diverges at position `j`, and TumblerSub yields `(b ⊖ w)_j = b_j - w_j > 0`. Since `a ⊖ w` is a zero tumbler and `b ⊖ w` has a positive component, TA6 gives `a ⊖ w < b ⊖ w`.

**Setup for remaining cases.** Since `a` is not zero-padded-equal to `w`, the divergence `d_a = div(a, w)` is well-defined. Since `a ≥ w` and `a` is not zero-padded-equal to `w`, we have `a > w`, and T1 at the first zero-padded divergence gives `a_{d_a} > w_{d_a}`. We verify that `d_b = div(b, w)` also exists: if `b` were zero-padded-equal to `w`, then `b_{d_a} = w_{d_a} < a_{d_a}`, and since `b_i = w_i = a_i` for `i < d_a`, T1 gives `a > b` — contradicting `a < b`. So `d_b` is well-defined, with `b_{d_b} > w_{d_b}` by the same reasoning from `b > w`.

**Case 1: `d_a = d_b = d`.** Both pairs diverge from `w` at position `d`. By TumblerSub, `(a ⊖ w)_i = 0` and `(b ⊖ w)_i = 0` for all `i < d`. Since `a` and `b` both agree with `w` before `d`, they agree with each other, so `j ≥ d`.

*Subcase `j = d`:* `(a ⊖ w)_d = a_d - w_d` and `(b ⊖ w)_d = b_d - w_d`. From `j = d`: `a_d < b_d`. Since `a_d > w_d` and `b_d > w_d` (established in setup), both differences are positive and `a_d - w_d < b_d - w_d`. The results agree before `d` (both zero) and first disagree at `d`. By T1 case (i), `a ⊖ w < b ⊖ w`.

*Subcase `j > d`:* `a_d = b_d` (since `j > d`), so `(a ⊖ w)_d = a_d - w_d = b_d - w_d = (b ⊖ w)_d`. For `d < i < j`: both results are in TumblerSub's tail-copy phase, giving `(a ⊖ w)_i = a_i` and `(b ⊖ w)_i = b_i`; since `a_i = b_i` (`i < j`), the results agree. At position `j`: `(a ⊖ w)_j = a_j` and `(b ⊖ w)_j = b_j` (still tail-copy), with `a_j < b_j`. The results first disagree at `j`. By T1 case (i), `a ⊖ w < b ⊖ w`.

**Case 2: `d_a < d_b`.** At position `d_a`: `a_{d_a} ≠ w_{d_a}` but `b_{d_a} = w_{d_a}` (since `d_a < d_b`). Both agree with `w` — hence with each other — before `d_a`, and disagree at `d_a` (since `a_{d_a} ≠ w_{d_a} = b_{d_a}`), so `j = d_a`. From `a < b` by T1: `a_{d_a} < b_{d_a} = w_{d_a}`. But `a_{d_a} > w_{d_a}` (from setup) — contradiction. This case is impossible.

**Case 3: `d_a > d_b`.** At position `d_b`: `b_{d_b} ≠ w_{d_b}` but `a_{d_b} = w_{d_b}` (since `d_b < d_a`). Both agree with `w` — hence with each other — before `d_b`, and disagree at `d_b` (since `b_{d_b} ≠ w_{d_b} = a_{d_b}`), so `j = d_b`. From `a < b`: `a_{d_b} < b_{d_b}`, i.e., `w_{d_b} < b_{d_b}` — consistent with `b_{d_b} > w_{d_b}`.

For `a ⊖ w`: position `d_b` falls before `d_a`, placing it in the pre-divergence zero phase, so `(a ⊖ w)_{d_b} = 0`. For `b ⊖ w`: `d_b` is the divergence point, so `(b ⊖ w)_{d_b} = b_{d_b} - w_{d_b} > 0`. At all positions `i < d_b`, both results are zero (pre-divergence for both). The first disagreement is at `d_b` with `0 < b_{d_b} - w_{d_b}`. By T1 case (i), `a ⊖ w < b ⊖ w`.

In every case, `a ⊖ w < b ⊖ w` is established. ∎

*Formal Contract:*
- *Preconditions:* a ∈ T, b ∈ T, w ∈ T, a < b, a ≥ w, b ≥ w, #a = #b
- *Postconditions:* a ⊖ w < b ⊖ w

### Partial inverse

**TA4 (Partial inverse).** `(A a, w : w > 0 ∧ k = #a ∧ #w = k ∧ (A i : 1 ≤ i < k : aᵢ = 0) : (a ⊕ w) ⊖ w = a)`, where `k` is the action point of `w`.

The precondition has three parts. First, `k = #a` — the action point falls at the last component of `a`. This is necessary because addition replaces `a`'s trailing structure below the action point with `w`'s trailing structure (tail replacement, defined below). When `k < #a`, components `aₖ₊₁, ..., a_{#a}` are discarded by addition and cannot be recovered by subtraction. Concretely: `[1, 5] ⊕ [1, 3] = [2, 3]` (action point 1, position 2 replaced by `w`'s trailing `3`), then `[2, 3] ⊖ [1, 3] = [1, 3] ≠ [1, 5]`.

Second, `#w = k` — the displacement has no trailing components beyond the action point. When `#w > k`, the result acquires trailing components from `w` that were not present in `a`. The trailing `7` from `w` persists through subtraction: `[0, 5] ⊕ [0, 3, 7] = [0, 8, 7]`, then `[0, 8, 7] ⊖ [0, 3, 7]` yields `[0, 5, 7] ≠ [0, 5]`.

Third, `(A i : 1 ≤ i < k : aᵢ = 0)` — all components of `a` before the action point are zero. This ensures the subtraction's divergence-discovery mechanism finds the action point at the right position. If `a` has a nonzero component at some position `j < k`, then the result of addition has `rⱼ = aⱼ ≠ 0`, and the subtraction's divergence falls at `j`, not at `k`. Concretely: `[5, 3] ⊕ [0, 7] = [5, 10]`, then `[5, 10] ⊖ [0, 7]`: divergence at position 1, producing `[5, 10] ≠ [5, 3]`.

When all three conditions hold, recovery is exact. The restriction is not a deficiency but a precise statement of when the operations are inverses.

*Dependencies:*
- **TA0 (Well-defined addition):** `a ⊕ w ∈ T` when `w > 0` and `actionPoint(w) ≤ #a`; result length `#(a ⊕ w) = #w`.
- **TA2 (Well-defined subtraction):** For `a ≥ w`, `a ⊖ w ∈ T` with `#(a ⊖ w) = max(#a, #w)`.
- **TumblerAdd (Constructive definition):** `(a ⊕ w)ᵢ = aᵢ` for `i < k`, `(a ⊕ w)ₖ = aₖ + wₖ`, `(a ⊕ w)ᵢ = wᵢ` for `i > k`, where `k = actionPoint(w)`.
- **TumblerSub (Constructive definition):** Zero-pad both operands to length `p = max(#a, #w)`. If the padded sequences agree everywhere, the result is the zero tumbler of length `p`. Otherwise, let `k` be the first divergence; then `rᵢ = 0` for `i < k`, `rₖ = aₖ - wₖ`, `rᵢ = aᵢ` for `i > k`, with `#r = p`.
- **T1 (Lexicographic order):** `a < b` iff `∃ k ≥ 1` with agreement before `k` and either (i) `k ≤ min(#a, #b)` and `aₖ < bₖ`, or (ii) `k = #a + 1 ≤ #b`.
- **T3 (Canonical representation):** `a = b ⟺ #a = #b ∧ (A i : 1 ≤ i ≤ #a : aᵢ = bᵢ)`.

*Proof.* We show that under the stated preconditions, `(a ⊕ w) ⊖ w = a`. Throughout, `k` denotes the action point of `w` — the least position `i` with `wᵢ > 0` — so by definition `wᵢ = 0` for all `i < k` and `wₖ > 0`.

**Step 1: the structure of `r = a ⊕ w`.** The precondition `k = #a` gives `k ≤ #a`, so by TA0 the sum `r = a ⊕ w` is well-defined with `#r = #w`. By TumblerAdd, `r` is built in three regions relative to the action point `k`:

*Prefix (`i < k`):* `rᵢ = aᵢ`. The precondition `(A i : 1 ≤ i < k : aᵢ = 0)` gives `rᵢ = 0`.

*Action point (`i = k`):* `rₖ = aₖ + wₖ`. Since `wₖ > 0` (definition of action point), `rₖ ≥ wₖ > 0`.

*Tail (`i > k`):* The precondition `#w = k` gives `#r = k`, so there are no positions beyond `k` — the tail-copy region is empty. The precondition `k = #a` ensures no components of `a` beyond position `k` are lost to tail replacement.

Therefore `r = [0, ..., 0, aₖ + wₖ]` — a tumbler of length `k` with zeros at all positions before `k`.

**Step 2: `r ≥ w`, so subtraction is well-defined.** Applying TumblerSub requires `r ≥ w` (TA2). Since `#r = k = #w`, no zero-padding is needed and T1 comparison proceeds on original components. At every position `i < k`, `rᵢ = 0 = wᵢ` (the former by Step 1, the latter by definition of action point). At position `k`, `rₖ = aₖ + wₖ ≥ wₖ`. If `aₖ > 0`, then `rₖ > wₖ`, and position `k` is the first divergence with `rₖ > wₖ`, so `r > w` by T1. If `aₖ = 0`, then `rₖ = wₖ`, and since `#r = #w = k` with all components equal, `r = w` by T3. Either way, `r ≥ w`.

**Step 3: computing `s = r ⊖ w`.** By Step 2 and TA2, the difference `s = r ⊖ w` is well-defined with `#s = max(#r, #w) = k`. TumblerSub zero-pads both operands to length `max(#r, #w) = k`; since both already have length `k`, no padding is needed. At each position `i < k`, `rᵢ = 0 = wᵢ` (Step 1 and definition of action point), so no divergence occurs before position `k`.

Two cases arise at position `k`, exhausting all possibilities for `aₖ ∈ ℕ`.

*Case 1: `aₖ > 0`.* Then `rₖ = aₖ + wₖ > wₖ` (since `aₖ > 0`), so `rₖ ≠ wₖ` and the first divergence is at position `k`. TumblerSub produces: `sᵢ = 0` for `i < k` (zeroing pre-divergence positions), `sₖ = rₖ - wₖ = (aₖ + wₖ) - wₖ = aₖ` (reversing the advance), and `sᵢ = rᵢ` for `i > k` (tail copy from the longer operand). Since `#r = k`, there are no positions beyond `k`, so the tail-copy region contributes nothing. The result `s` has length `k` with `sᵢ = 0` for all `i < k` and `sₖ = aₖ`. The original `a` has `#a = k` with `aᵢ = 0` for `i < k` (precondition) and `aₖ = aₖ`. Every component of `s` equals the corresponding component of `a`, and both have length `k`, so `s = a` by T3.

*Case 2: `aₖ = 0`.* Every component of `a` is zero: `aᵢ = 0` for `i < k` by precondition, and `aₖ = 0` by the case hypothesis, so `a` is the zero tumbler of length `k`. The addition gives `rₖ = 0 + wₖ = wₖ`. Combined with `rᵢ = 0 = wᵢ` for all `i < k` and `#r = k = #w`, every component of `r` equals the corresponding component of `w` at equal length, so `r = w` by T3. Now `s = r ⊖ w = w ⊖ w`: the operands agree at every position, so TumblerSub finds no divergence and produces the zero tumbler of length `max(#w, #w) = k`. This zero tumbler has the same length as `a` and every component equals zero — matching `a` component-by-component — so `s = a` by T3.

In both cases, `(a ⊕ w) ⊖ w = a`. ∎

*Formal Contract:*
- *Preconditions:* `a ∈ T`, `w ∈ T`, `w > 0`, `k = #a`, `#w = k`, `(A i : 1 ≤ i < k : aᵢ = 0)`, where `k` is the action point of `w`
- *Postconditions:* `(a ⊕ w) ⊖ w = a`

Gregory's analysis confirms that `⊕` and `⊖` are NOT inverses in general. The implementation's `absadd` is asymmetric: the first argument supplies the high-level prefix, the second supplies the low-level suffix. When `d = a ⊖ b` strips a common prefix (reducing the exponent), `b ⊕ d` puts the difference in the wrong operand position — `absadd`'s else branch discards the first argument entirely and returns the second. The operand-order asymmetry causes total information loss even before any digit overflow.

The reverse direction is equally necessary:

**ReverseInverse (Reverse inverse).** `(A a, w : a ≥ w ∧ w > 0 ∧ k = #a ∧ #w = k ∧ (A i : 1 ≤ i < k : aᵢ = 0) : (a ⊖ w) ⊕ w = a)`, where `k` is the action point of `w`.

We prove that subtraction followed by addition recovers the original tumbler, the reverse direction of TA4. Where TA4 shows `(a ⊕ w) ⊖ w = a`, this property shows `(a ⊖ w) ⊕ w = a` — together they establish that `⊕` and `⊖` are mutual inverses under the stated constraints.

*Dependencies:*
- **TA2 (Well-defined subtraction):** For `a ≥ w`, `a ⊖ w ∈ T` with `#(a ⊖ w) = max(#a, #w)`.
- **TA3-strict (Order preservation, strict):** `(A a, b, w : a < b ∧ a ≥ w ∧ b ≥ w ∧ #a = #b : a ⊖ w < b ⊖ w)`.
- **TA4 (Partial inverse):** `(A a, w : w > 0 ∧ k = #a ∧ #w = k ∧ (A i : 1 ≤ i < k : aᵢ = 0) : (a ⊕ w) ⊖ w = a)`.
- **TumblerAdd (Constructive definition):** `(a ⊕ w)ᵢ = aᵢ` for `i < k`, `(a ⊕ w)ₖ = aₖ + wₖ`, `(a ⊕ w)ᵢ = wᵢ` for `i > k`; result length `#(a ⊕ w) = #w`.
- **TumblerSub (Constructive definition):** Zero-pad to `max(#a, #w)`, scan for first divergence `d`; `rᵢ = 0` for `i < d`, `r_d = a_d - w_d`, `rᵢ = aᵢ` for `i > d`. If no divergence, result is zero tumbler of length `max(#a, #w)`.
- **T1 (Lexicographic order):** Strict total order; irreflexivity (`¬(a < a)`), trichotomy (`a < b ∨ a = b ∨ b < a`).
- **T3 (Canonical representation):** `a = b ⟺ #a = #b ∧ (A i : 1 ≤ i ≤ #a : aᵢ = bᵢ)`.

*Proof.* We show that `(a ⊖ w) ⊕ w = a`. Throughout, `k` denotes the action point of `w` — the least position with `wₖ > 0` — so by definition `wᵢ = 0` for all `i < k` and `wₖ > 0`.

**Step 1: the structure of `y = a ⊖ w`.** Since `a ≥ w` (given), the difference `y = a ⊖ w` is well-defined by TA2 with `#y = max(#a, #w)`. Since `#a = k = #w` (given), `#y = k` and no zero-padding is needed. TumblerSub scans for the first divergence between `a` and `w`. At each position `i < k`: `aᵢ = 0` (by the zero-prefix precondition) and `wᵢ = 0` (by definition of action point), so the operands agree before position `k`.

Two cases arise at position `k`, exhausting all possibilities since `a ≥ w`.

*Case `aₖ = wₖ`:* The operands agree at every position — there are no positions beyond `k` since both have length `k` — and TumblerSub finds no divergence, producing the zero tumbler of length `k`.

*Case `aₖ > wₖ`:* This is the only alternative, since `a ≥ w` with equal-length tumblers that agree before `k` requires `aₖ ≥ wₖ` by T1. Position `k` is the first divergence, and TumblerSub produces `yᵢ = 0` for `i < k`, `yₖ = aₖ - wₖ > 0`, and no components beyond `k` (since `max(#a, #w) = k`).

In either case, `y` has three properties:

- (Y1) `#y = k`
- (Y2) `yᵢ = 0` for all `1 ≤ i < k`
- (Y3) `yₖ = aₖ - wₖ`

**Step 2: TA4 applies to `y` and `w`.** TA4 requires four preconditions: `w > 0` (given), `k = #y` (by Y1), `#w = k` (given), and `(A i : 1 ≤ i < k : yᵢ = 0)` (by Y2). All four hold, so TA4 yields:

`(y ⊕ w) ⊖ w = y`  — (†)

This is the key fact: whatever `y ⊕ w` turns out to be, subtracting `w` from it recovers `y`.

**Step 3: `y ⊕ w = a`.** We prove this by contradiction. Assume `y ⊕ w ≠ a`. We will show that both `y ⊕ w > a` and `y ⊕ w < a` lead to `y < y`, contradicting irreflexivity (T1). This requires establishing the preconditions of TA3-strict for each case.

*Equal length.* By the result-length identity (TumblerAdd), `#(y ⊕ w) = #w = k = #a`.

*`a ≥ w`.* Given as a precondition.

*`y ⊕ w ≥ w`.* By TumblerAdd, for `i < k`: `(y ⊕ w)ᵢ = yᵢ = 0 = wᵢ` (using Y2 and the definition of action point). At position `k`: `(y ⊕ w)ₖ = yₖ + wₖ`. Since `#(y ⊕ w) = k = #w`, there are no positions beyond `k`, so the two tumblers agree at all positions except possibly `k`.

We show `y ⊕ w > w` or `y ⊕ w = w = a`. If `yₖ = 0`, then by Y3, `aₖ = wₖ`. Combined with `aᵢ = wᵢ = 0` for all `i < k` and `#a = #w = k`, this gives `a = w` by T3. Then `y = a ⊖ w = w ⊖ w`, which is the zero tumbler of length `k`, and `(y ⊕ w)ₖ = 0 + wₖ = wₖ` with zeros before `k`, so `y ⊕ w = w = a` by T3 — contradicting our assumption. Therefore `yₖ > 0`, giving `(y ⊕ w)ₖ = yₖ + wₖ > wₖ`. The two tumblers agree before `k` and first differ at `k` with `(y ⊕ w)ₖ > wₖ`, so `y ⊕ w > w` by T1.

*Deriving the contradiction.* By T1 (trichotomy), since `y ⊕ w ≠ a`, exactly one of `y ⊕ w > a` or `y ⊕ w < a` holds.

*Case `y ⊕ w > a`:* We have `a < y ⊕ w`, both `a ≥ w` and `y ⊕ w > w` (hence `y ⊕ w ≥ w`), and `#a = #(y ⊕ w)`. These are precisely the preconditions of TA3-strict, which gives `a ⊖ w < (y ⊕ w) ⊖ w`. The left side is `y` by definition of `y`. The right side is `y` by (†). This yields `y < y`, contradicting irreflexivity of `<` (T1).

*Case `y ⊕ w < a`:* We have `y ⊕ w < a`, both `y ⊕ w > w` (hence `y ⊕ w ≥ w`) and `a ≥ w`, and `#(y ⊕ w) = #a`. TA3-strict gives `(y ⊕ w) ⊖ w < a ⊖ w`. The left side is `y` by (†). The right side is `y` by definition. This yields `y < y`, again contradicting irreflexivity.

Both cases are impossible, so the assumption `y ⊕ w ≠ a` is false. Therefore `(a ⊖ w) ⊕ w = a`. ∎

*Formal Contract:*
- *Preconditions:* `a ∈ T`, `w ∈ T`, `a ≥ w`, `w > 0`, `k = #a`, `#w = k`, `(A i : 1 ≤ i < k : aᵢ = 0)`, where `k` is the action point of `w`
- *Postconditions:* `(a ⊖ w) ⊕ w = a`


### Constructive definition of ⊕ and ⊖

The axiomatic properties above state what `⊕` and `⊖` must satisfy. We now give a constructive definition that shows how they work. Tumbler addition is not arithmetic addition — it is a **position-advance operation**: given a start position `a` and a displacement `w`, compute where you land. The displacement encodes both the distance and the hierarchical level at which the advance occurs.

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

**Definition (TumblerAdd).** Let `a = [a₁, ..., aₘ]` and `w = [w₁, ..., wₙ]` with `w > 0`. With action point `k`:

```
         ⎧ aᵢ           if i < k        (copy from start)
rᵢ   =  ⎨ aₖ + wₖ      if i = k        (single-component advance)
         ⎩ wᵢ           if i > k        (copy from displacement)
```

The result `a ⊕ w = [r₁, ..., rₚ]` has length `p = max(k - 1, 0) + (n - k + 1)`. Since `w > 0` implies `k ≥ 1`, this simplifies to `p = (k - 1) + (n - k + 1) = n = #w`. We record this as the *result-length identity*: **`#(a ⊕ w) = #w`** — the length of the sum is determined entirely by the displacement, not the start position. This identity is load-bearing: the reverse inverse proof and the TA4 verification both depend on knowing the result length.

**Precondition:** `k ≤ m` — the displacement's action point must fall within the start position's length.

Three properties of this definition require explicit statement:

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
- *Preconditions:* `a ∈ T`, `w ∈ T`, `w > 0`, `actionPoint(w) ≤ #a`
- *Definition:* `(a ⊕ w)ᵢ = aᵢ` for `i < k`, `(a ⊕ w)ₖ = aₖ + wₖ`, `(a ⊕ w)ᵢ = wᵢ` for `i > k`, where `k = actionPoint(w)`
- *Postconditions:* `#(a ⊕ w) = #w`

**Definition (TumblerSub).** Given an end position `a` and a displacement `w`, recover the start position. When the operands have different lengths, we conceptually zero-pad the shorter to the length of the longer before scanning for divergence. When the zero-padded sequences agree at every position (no divergence exists), the result is the zero tumbler of length `max(#a, #w)`: `a ⊖ w = [0, ..., 0]`. Otherwise, let `k` be the first position where `a` and `w` differ (treating missing components as zero):

```
         ⎧ 0             if i < k        (these levels matched — zero them)
rᵢ   =  ⎨ aₖ - wₖ      if i = k        (reverse the advance)
         ⎩ aᵢ           if i > k        (copy from end position)
```

The result has length `max(#a, #w)`.

**Precondition:** `a ≥ w` — when `a ≠ w`, at the divergence point (after zero-padding) `aₖ ≥ wₖ`.

*Formal Contract:*
- *Preconditions:* `a ∈ T`, `w ∈ T`, `a ≥ w`
- *Definition:* Zero-pad both operands to length `max(#a, #w)`. If the padded sequences agree at every position, `a ⊖ w = [0, ..., 0]` of length `max(#a, #w)`. Otherwise, let `k` be the first divergence position: `(a ⊖ w)ᵢ = 0` for `i < k`, `(a ⊖ w)ₖ = aₖ - wₖ`, `(a ⊖ w)ᵢ = aᵢ` for `i > k`, with `#(a ⊖ w) = max(#a, #w)`.


### Verification of TA1 and TA1-strict

**Claim:** (TA1, weak form). If `a < b`, `w > 0`, and `k ≤ min(#a, #b)`, then `a ⊕ w ≤ b ⊕ w`.

**Claim:** (TA1-strict). If additionally `k ≥ divergence(a, b)`, then `a ⊕ w < b ⊕ w`.

*Proof.* Let `j = divergence(a, b)`. In case (i) of the Divergence definition, `aⱼ < bⱼ`; in case (ii), `j = min(#a, #b) + 1` exceeds both tumblers' shared positions and the ordering `a < b` follows from the prefix rule. Three cases arise.

*Case 1: `k < j`.* Both `a` and `b` agree at position `k` (since `k < j`), so `(a ⊕ w)ₖ = aₖ + wₖ = bₖ + wₖ = (b ⊕ w)ₖ`. At positions after `k`, both results copy from `w`, giving identical tails. So `a ⊕ w = b ⊕ w`. The weak form (`≤`) holds. The strict form does not — the original divergence is erased by tail replacement.

*Case 2: `k = j`.* At position `k`, `(a ⊕ w)ₖ = aₖ + wₖ < bₖ + wₖ = (b ⊕ w)ₖ` (since `aₖ < bₖ` and natural-number addition preserves strict inequality). Positions before `k` agree. So `a ⊕ w < b ⊕ w` strictly.

*Case 3: `k > j`.* For `i < k`, the constructive definition gives `(a ⊕ w)ᵢ = aᵢ` and `(b ⊕ w)ᵢ = bᵢ`. Since `j < k`, the divergence at position `j` is preserved: `(a ⊕ w)ⱼ = aⱼ < bⱼ = (b ⊕ w)ⱼ`. So `a ⊕ w < b ⊕ w` strictly. ∎

In all three cases, `a ⊕ w ≤ b ⊕ w`. Strict inequality holds in Cases 2 and 3, i.e., whenever `k ≥ j = divergence(a, b)`.


### Verification of TA3

The subtraction algorithm differs structurally from addition — it zeros positions before the divergence point and copies the tail from the minuend, whereas addition copies the tail from the displacement. We must verify TA3 directly.

**Claim:** (TA3, weak form). If `a < b`, `a ≥ w`, and `b ≥ w`, then `a ⊖ w ≤ b ⊖ w`.

*Proof.* By TA2, since `a ≥ w` and `b ≥ w`, both `a ⊖ w` and `b ⊖ w` are well-formed tumblers in `T`, making the order comparisons below well-defined. We first handle the case where `a < b` by the prefix rule (T1 case (ii)), then the component-divergence cases.

We derive from T1 alone an observation used in several cases below: every zero tumbler `z` is strictly less than every positive tumbler `p`. Let `j` be the least position with `pⱼ > 0`; for all `i < j`, `zᵢ = 0 = pᵢ`. If `j ≤ #z`, then `zⱼ = 0 < pⱼ` and T1 case (i) gives `z < p`. If `j > #z`, then `z` agrees with `p` at every shared position and `#z < j ≤ #p`, so T1 case (ii) gives `z < p`. We cite this as **(†)**.

*Case 0: `a` is a proper prefix of `b`.* Then `#a < #b` and `aᵢ = bᵢ` for all `i ≤ #a`.

We first handle the sub-case `a = w`. Then `a ⊖ w = [0, ..., 0]` (the zero tumbler of length `max(#a, #w) = #w = #a`). Since `b > a = w` and `a` is a proper prefix of `b`, we have `bᵢ = wᵢ` for all `i ≤ #w`. Two sub-sub-cases arise. If `b ⊖ w` is a positive tumbler — some component of `b` beyond `#w` is nonzero — then by (†), `a ⊖ w < b ⊖ w`. If `b ⊖ w` is itself a zero tumbler — all components of `b` beyond `#w` are zero, so zero-padded `w` equals `b` — then `b ⊖ w = [0, ..., 0]` of length `max(#b, #w) = #b`. Both results are zero tumblers, but `#(a ⊖ w) = #a < #b = #(b ⊖ w)` (since `a` is a proper prefix of `b`). The shorter zero tumbler is a proper prefix of the longer, so `a ⊖ w < b ⊖ w` by T1 case (ii). In either sub-sub-case, `a ⊖ w ≤ b ⊖ w`. The sub-case is resolved.

For `a > w`: two sub-cases arise depending on the structure of the divergence between `a` and `w` (after zero-padding).

*Sub-case `a > w` with divergence.* If `a > w` by T1 case (i), the divergence `dₐ` is at a shared position `≤ min(#a, #w) ≤ #a`. If `a > w` by T1 case (ii), `w` is a proper prefix of `a`; after zero-padding `w` to length `#a`, we compare: if at least one component `aᵢ > 0` for `i > #w`, the divergence falls at the smallest such `i`, satisfying `#w < dₐ ≤ #a`. In either T1 case, `dₐ ≤ #a`. Since `bᵢ = aᵢ` for all `i ≤ #a` and `dₐ ≤ #a`, the comparison of `b` (zero-padded) against `w` (zero-padded) agrees with that of `a` at all positions up to `dₐ`. So `d_b = dₐ = d`.

Now apply the subtraction formula to both. At positions `i < d`: both results are zero. At position `d`: both compute `a_d - w_d = b_d - w_d`, since `a_d = b_d` for `d ≤ #a`. At positions `d < i ≤ #a`: both copy from the minuend, giving `aᵢ = bᵢ`. The two results agree on all positions `1, ..., #a`.

Beyond position `#a`, the results may differ. The result `a ⊖ w` has length `max(#a, #w)`. At positions `#a < i ≤ max(#a, #w)` (present only when `#w > #a`): `(a ⊖ w)ᵢ = 0` (from `a`'s zero padding). For `(b ⊖ w)ᵢ`: when `i ≤ #b`, the value is `bᵢ` (copied in the tail phase since `i > d`); when `i > #b`, the value is `0` (from `b`'s zero padding). In either case `(a ⊖ w)ᵢ ≤ (b ⊖ w)ᵢ`. The result `b ⊖ w` has length `max(#b, #w) ≥ max(#a, #w)` (since `#b > #a`). If `max(#b, #w) > max(#a, #w)`, the extra positions come from `b`'s components beyond `max(#a, #w)` when `#b > #w` (copied from the minuend), or are zero when `#w > #b` (from `b`'s zero padding). Now `a ⊖ w` is no longer than `b ⊖ w`, and they agree on positions `1, ..., #a`. We compare lexicographically. If no disagreement exists on positions `1, ..., max(#a, #w)`, then `a ⊖ w` is a prefix of `b ⊖ w` (since `#(a ⊖ w) ≤ #(b ⊖ w)`), giving `a ⊖ w ≤ b ⊖ w` by T1 case (ii). If a first disagreement exists at some position `j > #a`, then `(a ⊖ w)ⱼ = 0 ≤ (b ⊖ w)ⱼ` (where `(b ⊖ w)ⱼ = bⱼ` when `j ≤ #b`, or `0` when `j > #b`). If the disagreement is strict (`(a ⊖ w)ⱼ = 0 < (b ⊖ w)ⱼ`), we have `a ⊖ w < b ⊖ w` by T1 case (i). If `(b ⊖ w)ⱼ = 0` at all positions `#a < j ≤ max(#a, #w)`, then `a ⊖ w` and `b ⊖ w` agree through position `max(#a, #w)`, and `a ⊖ w` is a prefix of the longer `b ⊖ w`, giving `a ⊖ w ≤ b ⊖ w` by T1 case (ii). In either case, `a ⊖ w ≤ b ⊖ w`.

*Sub-case `a > w` without divergence (zero-padded equality).* If `a > w` by T1 case (ii) and `aᵢ = 0` for all `i > #w`, then after zero-padding `w` to length `#a`, the padded sequences are identical — no divergence exists. The subtraction `a ⊖ w` yields the zero tumbler of length `max(#a, #w) = #a`. For `b ⊖ w`: since `b > a > w` and `#b > #a ≥ #w`, `b` agrees with `w` (hence with `a`) on positions `1, ..., #a`. Beyond `#a`, `b` has components that `a` lacks. The result `b ⊖ w` has length `max(#b, #w) = #b > #a`. The zero tumbler `a ⊖ w` of length `#a` is a proper prefix of the zero tumbler of length `#b` (if `b ⊖ w` is all zeros), giving `a ⊖ w < b ⊖ w` by T1 case (ii). If `b ⊖ w` has any positive component, then `a ⊖ w` (all zeros) is less than `b ⊖ w` by (†). In either case, `a ⊖ w ≤ b ⊖ w`. The sub-case is resolved.

*Case 0a: `a < b` by component divergence and `a` zero-padded-equal to `w`.* There exists `j ≤ min(#a, #b)` with `aⱼ < bⱼ`. Since `a` and `w` agree at every position under zero-padding, `a ⊖ w` is the zero tumbler of length `max(#a, #w)`. At position `j`, `wⱼ = aⱼ` (from zero-padded equality), so `bⱼ > aⱼ = wⱼ`. The pair `(b, w)` diverges at or before `j`, making `b ⊖ w` positive. By (†), `a ⊖ w < b ⊖ w`.

For the remaining cases, `a < b` by T1 case (i) and `a` is not zero-padded-equal to `w`, so `dₐ = divergence(a, w)` is well-defined. We show that `d_b = divergence(b, w)` also exists: if `b` were zero-padded-equal to `w`, then at position `dₐ`, `a_{dₐ} > w_{dₐ}` (from `a ≥ w` at the first padded divergence) and `w_{dₐ} = b_{dₐ}` (from `b`'s zero-padded equality with `w`), giving `a_{dₐ} > b_{dₐ}`. At all positions `i < dₐ`, `aᵢ = wᵢ = bᵢ`. By T1 case (i), `a > b` — contradicting `a < b`. So `b` is not zero-padded-equal to `w` and `d_b` is well-defined.

*Case 1: `dₐ = d_b = d`.* For `i < d`, both results are zero. At position `d`, we need `j ≥ d` (since `a` and `b` agree with `w` before `d`). If `j = d`: `a_d - w_d < b_d - w_d`, so `a ⊖ w < b ⊖ w`. If `j > d`: `a_d = b_d`, so both results agree at `d`; at positions `d < i < j`, both copy from their respective minuends which agree; at position `j`, `aⱼ < bⱼ`. So `a ⊖ w < b ⊖ w`.

*Case 2: `dₐ < d_b`.* At position `dₐ`: `a_{dₐ} ≠ w_{dₐ}` but `b_{dₐ} = w_{dₐ}`. Since `a < b` and they agree with `w` before `dₐ`, we have `j = dₐ` with `a_{dₐ} < b_{dₐ} = w_{dₐ}`. But `a ≥ w` requires `a_{dₐ} ≥ w_{dₐ}` at the divergence — contradiction. This case is impossible under the preconditions.

*Case 3: `dₐ > d_b`.* At position `d_b`: `b_{d_b} ≠ w_{d_b}` but `a_{d_b} = w_{d_b}`. So `j = d_b` with `a_{d_b} = w_{d_b} < b_{d_b}`. The result `(a ⊖ w)_{d_b} = 0` and `(b ⊖ w)_{d_b} = b_{d_b} - w_{d_b} > 0`. So `a ⊖ w < b ⊖ w`. ∎

*Formal Contract:*
- *Preconditions:* a ∈ T, b ∈ T, w ∈ T, a < b, a ≥ w, b ≥ w
- *Postconditions:* a ⊖ w ≤ b ⊖ w

**Claim:** (TA3-strict). If `a < b`, `a ≥ w`, `b ≥ w`, and `#a = #b`, then `a ⊖ w < b ⊖ w`.

*Proof.* The equal-length precondition eliminates Case 0 entirely — two tumblers of the same length cannot be in a prefix relationship unless equal, and `a < b` rules out equality. Cases 0a and 1–3 remain, all of which produce strict inequality. ∎

*Formal Contract:*
- *Preconditions:* a ∈ T, b ∈ T, w ∈ T, a < b, a ≥ w, b ≥ w, #a = #b
- *Postconditions:* a ⊖ w < b ⊖ w


### Verification of TA4

**Claim.** `(a ⊕ w) ⊖ w = a` under the full precondition: `k = #a`, `#w = k`, `(A i : 1 ≤ i < k : aᵢ = 0)`.

*Proof.* Let `k` be the action point of `w`. Since `k = #a`, the addition `a ⊕ w` produces a result `r` with: `rᵢ = aᵢ = 0` for `i < k` (by the zero-prefix condition), `rₖ = aₖ + wₖ`, and `rᵢ = wᵢ` for `i > k`. Crucially, there are no components of `a` beyond position `k` — the tail replacement discards nothing. By the result-length identity, `#r = #w = k`, so `r = [0, ..., 0, aₖ + wₖ]`.

Now subtract `w` from `r`. The subtraction scans for the first divergence between `r` and `w`. For `i < k`: `rᵢ = 0 = wᵢ` (both are zero — `aᵢ` by the zero-prefix precondition, `wᵢ` by definition of action point). Two sub-cases arise at position `k`.

*Sub-case (i): `aₖ > 0`.* Then `rₖ = aₖ + wₖ > wₖ`, and the first divergence is at position `k`. The subtraction produces: positions `i < k` get zero, position `k` gets `rₖ - wₖ = aₖ`, and positions `i > k` copy from `r`, giving `rᵢ = wᵢ`. Since `k = #a` and `#w = k`, there are no trailing components. The result is `[0, ..., 0, aₖ] = a`. For valid addresses, T4's positive-component constraint guarantees `aₖ > 0`, so this sub-case always applies in the address context.

*Sub-case (ii): `aₖ = 0`.* Then `a` is a zero tumbler. The addition gives `rₖ = wₖ`. Since `#r = #w` (result-length identity) and `#w = k` (precondition), we have `r = w`. The subtraction `w ⊖ w` yields the zero tumbler of length `k`, which is `a`. ∎

*Formal Contract:*
- *Preconditions:* `a ∈ T`, `w ∈ T`, `w > 0`, `k = #a`, `#w = k`, `(A i : 1 ≤ i < k : aᵢ = 0)`, where `k` is the action point of `w`
- *Postconditions:* `(a ⊕ w) ⊖ w = a`


### Cancellation properties of ⊕

TumblerAdd's constructive definition determines each component of the result from exactly one input. This makes the operation left-cancellative.

**TA-LC (LeftCancellation).** If a ⊕ x = a ⊕ y with both sides well-defined (TA0 satisfied for both), then x = y.

*Proof.* We shall derive `x = y` from the hypothesis `a ⊕ x = a ⊕ y`, where both additions satisfy TA0. The argument has two stages: first we prove that `x` and `y` share the same action point, then we establish component-wise and length equality.

Let `k₁ = actionPoint(x)` and `k₂ = actionPoint(y)`. Both are well-defined: TA0 requires `x > 0` and `y > 0`, so each displacement has at least one nonzero component, and the action point — defined as the index of the first such component — exists. We must show `k₁ = k₂`. We do so by eliminating both strict orderings.

**Case k₁ < k₂.** The action point `k₂` is the first nonzero component of `y`, so every component of `y` before position `k₂` is zero; in particular, since `k₁ < k₂`, we have `y_{k₁} = 0`. In the addition `a ⊕ y`, position `k₁` therefore falls strictly before the action point of `y`, so TumblerAdd's prefix-copy rule (Definition TumblerAdd, case `i < k`) gives `(a ⊕ y)_{k₁} = a_{k₁}`. In the addition `a ⊕ x`, position `k₁` is the action point of `x` itself, so TumblerAdd's advance rule (case `i = k`) gives `(a ⊕ x)_{k₁} = a_{k₁} + x_{k₁}`. The hypothesis `a ⊕ x = a ⊕ y` yields, at position `k₁`:

&emsp; `a_{k₁} + x_{k₁} = a_{k₁}`

hence `x_{k₁} = 0`. But `k₁ = actionPoint(x)` means `x_{k₁} > 0` by definition — contradiction.

**Case k₂ < k₁.** The action point `k₁` is the first nonzero component of `x`, so every component of `x` before position `k₁` is zero; in particular, since `k₂ < k₁`, we have `x_{k₂} = 0`. In the addition `a ⊕ x`, position `k₂` falls strictly before the action point of `x`, so TumblerAdd's prefix-copy rule gives `(a ⊕ x)_{k₂} = a_{k₂}`. In the addition `a ⊕ y`, position `k₂` is the action point of `y` itself, so TumblerAdd's advance rule gives `(a ⊕ y)_{k₂} = a_{k₂} + y_{k₂}`. The hypothesis `a ⊕ x = a ⊕ y` yields, at position `k₂`:

&emsp; `a_{k₂} = a_{k₂} + y_{k₂}`

hence `y_{k₂} = 0`. But `k₂ = actionPoint(y)` means `y_{k₂} > 0` by definition — contradiction.

Both strict orderings lead to contradiction, so `k₁ = k₂`. Write `k` for this common action point. It remains to show that `x` and `y` agree at every component and have the same length.

**Positions i < k.** Both `x` and `y` have action point `k`, so by definition every component before position `k` is zero: `xᵢ = 0` and `yᵢ = 0`. Hence `xᵢ = yᵢ = 0`.

**Position i = k.** TumblerAdd's advance rule gives `(a ⊕ x)_k = a_k + x_k` and `(a ⊕ y)_k = a_k + y_k`. The hypothesis `a ⊕ x = a ⊕ y` yields `a_k + x_k = a_k + y_k`, hence `x_k = y_k` by cancellation in ℕ.

**Positions i > k.** TumblerAdd's tail-copy rule (case `i > k`) gives `(a ⊕ x)_i = x_i` and `(a ⊕ y)_i = y_i`. The hypothesis `a ⊕ x = a ⊕ y` yields `x_i = y_i` directly.

**Length.** The result-length identity (Definition TumblerAdd) states `#(a ⊕ w) = #w` for any well-defined addition. Applying it to both sides of `a ⊕ x = a ⊕ y`: `#x = #(a ⊕ x)` and `#y = #(a ⊕ y)`. Since `a ⊕ x = a ⊕ y`, T3 (CanonicalRepresentation) gives `#(a ⊕ x) = #(a ⊕ y)`, hence `#x = #y`.

We have established `xᵢ = yᵢ` for every position `i` from `1` to `max(#x, #y)`, and `#x = #y`. By T3 (CanonicalRepresentation), `x = y`.  ∎

TumblerAdd is *left-cancellative*: the start position can be "divided out" from equal results, recovering the displacement uniquely. This follows from TumblerAdd's constructive definition — each component of the result is determined by exactly one input, so equality of results propagates back to equality of inputs.

*Worked example.* Let `a = [2, 5]` and suppose `a ⊕ x = a ⊕ y = [2, 8]`. We recover `x` and `y` uniquely. First, the action points must agree. Suppose `k_x = 1`: TumblerAdd's advance rule gives `(a ⊕ x)₁ = a₁ + x₁ = 2 + x₁ = 2`, so `x₁ = 0`, contradicting `k_x = 1` being the first nonzero component. So `k_x ≠ 1`. The result-length identity gives `#x = #(a ⊕ x) = 2`, so `k_x = 2`. By the same argument applied to `y`, `k_y = 2`. At position `k = 2`: `a₂ + x₂ = 5 + x₂ = 8` gives `x₂ = 3`, and `a₂ + y₂ = 5 + y₂ = 8` gives `y₂ = 3`. For `i < k`: `x₁ = 0 = y₁` (both zero before the action point). Since `#x = 2 = #y`, T3 gives `x = y = [0, 3]`.

*Formal Contract:*
- *Preconditions:* a, x, y ∈ T; x > 0; y > 0; actionPoint(x) ≤ #a; actionPoint(y) ≤ #a; a ⊕ x = a ⊕ y
- *Postconditions:* x = y


### Right cancellation and the many-to-one property

The converse — right cancellation — does not hold. TumblerAdd's many-to-one property (noted informally in the definition of TumblerAdd above) means distinct starts can produce the same result under the same displacement.

**TA-RC (RightCancellationFailure).** There exist tumblers a, b, w with a ≠ b and a ⊕ w = b ⊕ w (both sides well-defined).

*Dependencies:*
- **TA0 (Well-defined addition):** For `a, w ∈ T` with `w > 0` and action point `k ≤ #a`, `a ⊕ w ∈ T` with `#(a ⊕ w) = #w`.
- **TumblerAdd (Constructive definition):** `(a ⊕ w)ᵢ = aᵢ` for `i < k`, `(a ⊕ w)ₖ = aₖ + wₖ`, `(a ⊕ w)ᵢ = wᵢ` for `i > k`; result length `#(a ⊕ w) = #w`.
- **T3 (Canonical representation):** `a = b ⟺ #a = #b ∧ (A i : 1 ≤ i ≤ #a : aᵢ = bᵢ)`.

*Proof.* We exhibit three specific tumblers and verify the claim by direct computation. Three obligations must be discharged: that the witnesses are distinct, that both additions are well-defined, and that the results are equal.

Let `a = [1, 3, 5]`, `b = [1, 3, 7]`, and `w = [0, 2, 4]`.

**Distinctness.** The third components differ: `a₃ = 5` and `b₃ = 7`, so `a₃ ≠ b₃`. Since `#a = 3 = #b` but not all components agree, the contrapositive of T3 gives `a ≠ b`.

**Well-definedness.** The displacement `w = [0, 2, 4]` has action point `k = 2`, since `w₁ = 0` and `w₂ = 2 > 0` — position 2 is the first nonzero component. For `a ⊕ w`, TA0 requires `actionPoint(w) ≤ #a`, i.e. `2 ≤ 3`, which holds. For `b ⊕ w`, TA0 requires `actionPoint(w) ≤ #b`, i.e. `2 ≤ 3`, which likewise holds. Both additions are well-defined.

**Computation of a ⊕ w.** We expand by TumblerAdd's constructive definition with action point `k = 2`:

- Position `i = 1` (`i < k`): prefix copy gives `(a ⊕ w)₁ = a₁ = 1`.
- Position `i = 2` (`i = k`): advance gives `(a ⊕ w)₂ = a₂ + w₂ = 3 + 2 = 5`.
- Position `i = 3` (`i > k`): tail copy gives `(a ⊕ w)₃ = w₃ = 4`.

The result-length identity gives `#(a ⊕ w) = #w = 3`, so `a ⊕ w = [1, 5, 4]`.

**Computation of b ⊕ w.** We expand by the same three rules with the same action point `k = 2`:

- Position `i = 1` (`i < k`): prefix copy gives `(b ⊕ w)₁ = b₁ = 1`.
- Position `i = 2` (`i = k`): advance gives `(b ⊕ w)₂ = b₂ + w₂ = 3 + 2 = 5`.
- Position `i = 3` (`i > k`): tail copy gives `(b ⊕ w)₃ = w₃ = 4`.

The result-length identity gives `#(b ⊕ w) = #w = 3`, so `b ⊕ w = [1, 5, 4]`.

**Equality of results.** Both results are `[1, 5, 4]`. Since `#(a ⊕ w) = 3 = #(b ⊕ w)` and all three components agree, T3 gives `a ⊕ w = b ⊕ w`.

The mechanism that produces this equality is TumblerAdd's tail-copy rule: for positions `i > k`, the result component `(a ⊕ w)ᵢ = wᵢ` depends only on `w`, not on the start. The components `a₃ = 5` and `b₃ = 7` both lie after the action point `k = 2`, so neither contributes to the result — the displacement's tail replaces them entirely.

We have exhibited `a ≠ b` with `a ⊕ w = b ⊕ w`, both sides well-defined: right cancellation fails.  ∎

*Formal Contract:*
- *Postconditions:* `∃ a, b, w ∈ T : w > 0 ∧ actionPoint(w) ≤ #a ∧ actionPoint(w) ≤ #b ∧ a ≠ b ∧ a ⊕ w = b ⊕ w`

The mechanism is TumblerAdd's tail replacement: components of the start position after the action point are discarded and replaced by the displacement's tail. Any two starts that agree on components 1..k and differ only on components after k will produce the same result under any displacement with action point k. Formally:

**TA-MTO (ManyToOne).** For any displacement w with action point k and any tumblers a, b with #a ≥ k and #b ≥ k: a ⊕ w = b ⊕ w if and only if a_i = b_i for all 1 ≤ i ≤ k.

*Dependencies:*
- **TA0 (Well-defined addition):** For `a, w ∈ T` with `w > 0` and action point `k ≤ #a`, `a ⊕ w ∈ T` with `#(a ⊕ w) = #w`. Used to establish that both additions `a ⊕ w` and `b ⊕ w` are well-defined.
- **TumblerAdd (Constructive definition):** `(a ⊕ w)ᵢ = aᵢ` for `i < k`, `(a ⊕ w)ₖ = aₖ + wₖ`, `(a ⊕ w)ᵢ = wᵢ` for `i > k`; result length `#(a ⊕ w) = #w`. Used to expand both sums componentwise and to establish that the result length is independent of the start position.
- **T3 (Canonical representation):** `a = b ⟺ #a = #b ∧ (A i : 1 ≤ i ≤ #a : aᵢ = bᵢ)`. Used in the forward direction to conclude equality from componentwise agreement, and contrapositively in the converse to extract componentwise agreement from equality.

*Proof.* We show that for all `w ∈ T` with `w > 0` and action point `k`, and all `a, b ∈ T` with `#a ≥ k` and `#b ≥ k`, the equivalence `a ⊕ w = b ⊕ w ⟺ (A i : 1 ≤ i ≤ k : aᵢ = bᵢ)` holds. The argument proceeds by establishing each direction separately.

Both additions `a ⊕ w` and `b ⊕ w` are well-defined by TA0, since the action point `k` satisfies `k ≤ #a` and `k ≤ #b`. TumblerAdd's constructive definition builds each result in three regions relative to `k`:

```
  (a ⊕ w)ᵢ = aᵢ         for 1 ≤ i < k     (prefix copy)
  (a ⊕ w)ₖ = aₖ + wₖ                       (single-component advance)
  (a ⊕ w)ᵢ = wᵢ         for k < i ≤ #w     (tail copy)
```

and identically for `b ⊕ w` with `bᵢ` replacing `aᵢ`. The result-length identity (TumblerAdd) gives `#(a ⊕ w) = #w = #(b ⊕ w)`.

*(Forward: agreement implies equal results.)* Assume `aᵢ = bᵢ` for all `1 ≤ i ≤ k`. We show `(a ⊕ w)ᵢ = (b ⊕ w)ᵢ` at every position `i` from `1` to `#w`, which together with `#(a ⊕ w) = #(b ⊕ w) = #w` yields `a ⊕ w = b ⊕ w` by T3.

*Position i < k:* `(a ⊕ w)ᵢ = aᵢ = bᵢ = (b ⊕ w)ᵢ`. The first and third equalities are TumblerAdd's prefix-copy rule applied to `a` and `b` respectively; the middle equality is the hypothesis `aᵢ = bᵢ`.

*Position i = k:* `(a ⊕ w)ₖ = aₖ + wₖ = bₖ + wₖ = (b ⊕ w)ₖ`. The first and third equalities are TumblerAdd's advance rule; the middle step substitutes the hypothesis `aₖ = bₖ`.

*Position i > k:* `(a ⊕ w)ᵢ = wᵢ = (b ⊕ w)ᵢ`. Both equalities are TumblerAdd's tail-copy rule — neither `a` nor `b` contributes to positions beyond the action point.

All `#w` components agree and the lengths are equal, so `a ⊕ w = b ⊕ w` by T3.

*(Converse: equal results implies agreement.)* Assume `a ⊕ w = b ⊕ w`. By T3, this entails `(a ⊕ w)ᵢ = (b ⊕ w)ᵢ` at every position `1 ≤ i ≤ #w`. We extract `aᵢ = bᵢ` for each `1 ≤ i ≤ k`.

*Position i < k:* TumblerAdd's prefix-copy rule gives `(a ⊕ w)ᵢ = aᵢ` and `(b ⊕ w)ᵢ = bᵢ`. From `(a ⊕ w)ᵢ = (b ⊕ w)ᵢ` we obtain `aᵢ = bᵢ`.

*Position i = k:* TumblerAdd's advance rule gives `(a ⊕ w)ₖ = aₖ + wₖ` and `(b ⊕ w)ₖ = bₖ + wₖ`. From `(a ⊕ w)ₖ = (b ⊕ w)ₖ` we obtain `aₖ + wₖ = bₖ + wₖ`, hence `aₖ = bₖ` by cancellation in ℕ.

*Positions i > k* impose no constraint on `a` or `b`: TumblerAdd's tail-copy rule gives `(a ⊕ w)ᵢ = wᵢ = (b ⊕ w)ᵢ` regardless of `aᵢ` and `bᵢ`, since these components are drawn entirely from `w`. This is the structural source of the many-to-one property — distinct tumblers that agree on the first `k` components but differ below `k` are mapped to the same result. ∎

This gives a precise characterization of the equivalence classes: *a and b produce the same result under w if and only if they agree on the first k components, where k is the action point of w.*

*Formal Contract:*
- *Preconditions:* `w ∈ T`, `w > 0`, `a ∈ T`, `b ∈ T`, `#a ≥ actionPoint(w)`, `#b ≥ actionPoint(w)`
- *Postconditions:* `a ⊕ w = b ⊕ w ⟺ (A i : 1 ≤ i ≤ actionPoint(w) : aᵢ = bᵢ)`


### Displacement identities

Given two positions a and b on the tumbler line, a natural question is whether b ⊖ a yields a displacement w such that a ⊕ w faithfully recovers b. We establish the well-definedness condition for such displacement recovery and the round-trip identity that guarantees faithfulness.

From TumblerAdd, a ⊕ w acts at the action point k of w: it copies a₁..aₖ₋₁, advances aₖ by wₖ, and replaces the tail with w's tail. So if a ⊕ w = b, then a and b agree on components 1..k−1 and diverge at k, with bₖ = aₖ + wₖ and bᵢ = wᵢ for i > k. Reading off the width:

  wᵢ = 0  for i < k,    wₖ = bₖ − aₖ,    wᵢ = bᵢ  for i > k

where k = divergence(a, b). This is exactly the formula for b ⊖ a from TumblerSub. We write w = b ⊖ a and call it the *displacement from a to b*. The displacement is well-defined when:

**D0 (DisplacementWellDefined).** a < b, and the divergence k of a and b satisfies k ≤ #a.

*Proof.* We show that under the hypotheses `a, b ∈ T`, `a < b`, and `divergence(a, b) ≤ #a`, the displacement `w = b ⊖ a` is a well-defined positive tumbler whose action point equals `divergence(a, b)`, and the addition `a ⊕ w` is well-defined. We also identify the boundary condition for round-trip faithfulness.

Let `k = divergence(a, b)`. The hypothesis `k ≤ #a` eliminates Divergence case (ii), which would require `k = min(#a, #b) + 1 ≥ #a + 1 > #a`. We are therefore in case (i): `k ≤ min(#a, #b)`, with `aᵢ = bᵢ` for all `i < k` and `aₖ ≠ bₖ`. Since `a < b`, T1 case (i) gives the direction: `aₖ < bₖ`.

When `a` is a proper prefix of `b`, the Divergence definition gives case (ii) with `k = #a + 1 > #a`, violating D0's hypothesis. No displacement exists for prefix-related pairs — the subtraction is defined but the round-trip addition is not, because the action point would exceed `#a`.

**Well-definedness of the subtraction.** Since `a < b` entails `b ≥ a`, the subtraction `w = b ⊖ a` is a well-defined tumbler in T by TA2. We now compute `w` explicitly. By TumblerSub, zero-pad both operands to length `max(#b, #a)` and scan for the first position at which the padded sequences disagree. Since `bᵢ = aᵢ` for all `i < k` (from Divergence case (i)) and `bₖ ≠ aₖ`, the first divergence between minuend `b` and subtrahend `a` is at position `k`. TumblerSub yields:

  `wᵢ = 0` for `i < k`, `wₖ = bₖ − aₖ`, `wᵢ = bᵢ` for `i > k`

with `#w = max(#b, #a)`. The component `wₖ = bₖ − aₖ` is well-defined and non-negative because `bₖ > aₖ` (established above).

**Positivity.** The displacement `w` is positive: `wₖ = bₖ − aₖ ≥ 1` since `aₖ < bₖ` and both are natural numbers. All components before position `k` are zero, so `w` is not the zero tumbler.

**Action point.** The action point of `w` is `k`: every component `wᵢ = 0` for `i < k`, and `wₖ > 0`, so `k` is the first positive component of `w`.

**Well-definedness of the addition.** TA0 requires `w > 0` (established) and `actionPoint(w) ≤ #a`. The action point is `k`, and the hypothesis gives `k ≤ #a`, so TA0 is satisfied. The addition `a ⊕ w` is a well-defined tumbler in T.

**Round-trip boundary.** The displacement has length `#w = max(#a, #b)`. By the result-length identity (TumblerAdd), `#(a ⊕ w) = #w`. When `#a > #b`, this gives `#(a ⊕ w) = #a > #b`, so `a ⊕ w ≠ b` by T3 (CanonicalRepresentation) — the round-trip fails on length alone. Round-trip faithfulness requires the additional condition `#a ≤ #b`, under which `#w = #b` and the component-by-component recovery succeeds (D1). ∎

*Formal Contract:*
- *Preconditions:* a ∈ T, b ∈ T, a < b, divergence(a, b) ≤ #a
- *Postconditions:* b ⊖ a ∈ T, b ⊖ a > 0, actionPoint(b ⊖ a) = divergence(a, b), a ⊕ (b ⊖ a) ∈ T

**D1 (DisplacementRoundTrip).** For tumblers a, b ∈ T with a < b, divergence(a, b) ≤ #a, and #a ≤ #b:

  a ⊕ (b ⊖ a) = b

*Dependencies:*
- **D0 (DisplacementWellDefined):** Under `a < b` and `divergence(a, b) ≤ #a`: the displacement `w = b ⊖ a` is a well-defined positive tumbler with `actionPoint(w) = divergence(a, b)`, and `a ⊕ w ∈ T`.
- **TumblerSub (Constructive definition):** Zero-pad both operands to length `max(#b, #a)`. Let `k` be the first divergence; `(b ⊖ a)ᵢ = 0` for `i < k`, `(b ⊖ a)ₖ = bₖ - aₖ`, `(b ⊖ a)ᵢ = bᵢ` for `i > k`; result length `#(b ⊖ a) = max(#b, #a)`.
- **TumblerAdd (Constructive definition):** `(a ⊕ w)ᵢ = aᵢ` for `i < k`, `(a ⊕ w)ₖ = aₖ + wₖ`, `(a ⊕ w)ᵢ = wᵢ` for `i > k`, where `k = actionPoint(w)`; result length `#(a ⊕ w) = #w`.
- **Divergence definition:** For `a ≠ b`, `divergence(a, b)` is the least `k` where they differ; in case (i) `k ≤ min(#a, #b)` with `aₖ ≠ bₖ` and `aᵢ = bᵢ` for `i < k`; in case (ii) `k = min(#a, #b) + 1`.
- **T1 (Lexicographic order):** `a < b` iff `∃ k ≥ 1` with agreement before `k` and either (i) `k ≤ min(#a, #b)` and `aₖ < bₖ`, or (ii) `k = #a + 1 ≤ #b`.
- **T3 (Canonical representation):** `a = b ⟺ #a = #b ∧ (A i : 1 ≤ i ≤ #a : aᵢ = bᵢ)`.

*Proof.* We show that the displacement from a to b, when added back to a, recovers b — both component by component and in length.

Let k = divergence(a, b). The preconditions give k ≤ #a and #a ≤ #b, so k ≤ #a = min(#a, #b). This eliminates Divergence case (ii), which requires k = min(#a, #b) + 1 = #a + 1 > #a, contradicting k ≤ #a. We are in case (i): aᵢ = bᵢ for all i < k, and aₖ ≠ bₖ at position k ≤ min(#a, #b). Since a < b, the T1 witness for the ordering is position k — case (i) of T1 gives the direction: aₖ < bₖ.

**The displacement.** Define w = b ⊖ a. By D0, the subtraction is well-defined under a < b and k ≤ #a, yielding a positive tumbler with actionPoint(w) = k. We compute w explicitly via TumblerSub. Zero-pad both operands to length max(#b, #a) = #b (since #a ≤ #b). The first divergence in the padded sequences is at position k — positions i < k have bᵢ = aᵢ (from Divergence case (i)), and position k has bₖ ≠ aₖ — so TumblerSub yields:

  wᵢ = 0           for i < k
  wₖ = bₖ − aₖ     (well-defined since bₖ > aₖ)
  wᵢ = bᵢ          for i > k

with #w = max(#b, #a) = #b.

**The addition.** By D0, the addition a ⊕ w is well-defined: w > 0 and actionPoint(w) = k ≤ #a satisfy the preconditions of TumblerAdd. The constructive definition builds a ⊕ w in three regions determined by the action point k:

*Positions i < k (prefix copy):* (a ⊕ w)ᵢ = aᵢ. By the Divergence case (i) agreement condition, aᵢ = bᵢ for all i < k. Therefore (a ⊕ w)ᵢ = bᵢ.

*Position i = k (advance):* (a ⊕ w)ₖ = aₖ + wₖ = aₖ + (bₖ − aₖ) = bₖ. The cancellation is exact: bₖ > aₖ ensures bₖ − aₖ ∈ ℕ, and aₖ + (bₖ − aₖ) = bₖ by arithmetic on natural numbers.

*Positions i > k (tail from displacement):* (a ⊕ w)ᵢ = wᵢ = bᵢ. TumblerSub placed bᵢ into wᵢ at these positions; TumblerAdd copies wᵢ into the result.

**Length.** By the result-length identity of TumblerAdd, #(a ⊕ w) = #w = #b.

**Conclusion.** Every component of a ⊕ w equals the corresponding component of b — (a ⊕ w)ᵢ = bᵢ for all 1 ≤ i ≤ #b — and #(a ⊕ w) = #b. By T3 (CanonicalRepresentation), a ⊕ w = b.  ∎

*Formal Contract:*
- *Preconditions:* a ∈ T, b ∈ T, a < b, divergence(a, b) ≤ #a, #a ≤ #b
- *Postconditions:* a ⊕ (b ⊖ a) = b

**D2 (DisplacementUnique).** Under D1's preconditions (a < b, divergence(a, b) ≤ #a, #a ≤ #b), if a ⊕ w = b then w = b ⊖ a.

*Dependencies:*
- **D0 (DisplacementWellDefined):** Under `a < b` and `divergence(a, b) ≤ #a`: the displacement `b ⊖ a` is a well-defined positive tumbler with `actionPoint(b ⊖ a) = divergence(a, b)`, and `a ⊕ (b ⊖ a) ∈ T`.
- **D1 (DisplacementRoundTrip):** Under `a < b`, `divergence(a, b) ≤ #a`, `#a ≤ #b`: `a ⊕ (b ⊖ a) = b`.
- **TA0 (Well-defined addition):** For tumblers `a, w ∈ T` where `w > 0` and `actionPoint(w) ≤ #a`, the result `a ⊕ w` is a well-defined tumbler in `T`.
- **TA-LC (LeftCancellation):** If `a ⊕ x = a ⊕ y` with both sides well-defined (TA0 satisfied for both), then `x = y`.

*Proof.* We show that any displacement w satisfying a ⊕ w = b must equal the canonical displacement b ⊖ a. The argument proceeds in three steps: construct a second witness for the same equation, verify that both additions satisfy TA0, and apply left cancellation.

**Step 1 (a second witness).** The preconditions a < b, divergence(a, b) ≤ #a, and #a ≤ #b are exactly those of D1 (DisplacementRoundTrip), which gives a ⊕ (b ⊖ a) = b. Combined with the hypothesis a ⊕ w = b, we have two equations sharing the same base and result:

  a ⊕ w = b
  a ⊕ (b ⊖ a) = b

**Step 2 (TA0 verification).** To apply TA-LC, both additions must satisfy TA0 — that is, both displacements must be positive with action points at most #a. We verify each in turn.

*For w:* The hypothesis asserts a ⊕ w = b. TumblerAdd is a partial operation, defined only when TA0 holds: w > 0 and actionPoint(w) ≤ #a. The well-definedness of a ⊕ w therefore entails both conditions. TA0 is satisfied for w.

*For b ⊖ a:* By D0 (DisplacementWellDefined), under a < b and divergence(a, b) ≤ #a, the displacement b ⊖ a is a well-defined positive tumbler with actionPoint(b ⊖ a) = divergence(a, b). The precondition divergence(a, b) ≤ #a gives actionPoint(b ⊖ a) ≤ #a directly. Both conditions of TA0 — positivity and the action-point bound — are satisfied for b ⊖ a.

**Step 3 (cancellation).** From the hypothesis and Step 1:

  a ⊕ w = a ⊕ (b ⊖ a)

Both additions satisfy TA0 (Step 2). TA-LC (LeftCancellation) states that a ⊕ x = a ⊕ y, with both sides well-defined, implies x = y. We conclude w = b ⊖ a.  ∎

D1 and D2 together characterize the displacement completely: D1 says b ⊖ a recovers b, D2 says nothing else does.

When a = b, no displacement is needed; the degenerate case is handled separately since b ⊖ a produces the zero tumbler and a ⊕ (b ⊖ a) is not well-formed (TA0 requires w > 0). D0 ensures the displacement is well-defined; D1 ensures the round-trip is faithful when additionally #a ≤ #b.

*Worked example.* Consider a = [1, 2, 3] and b = [1, 5, 1]. We have #a = #b = 3.

*D0 check.* divergence(a, b) = 2, since a₁ = b₁ = 1 and a₂ = 2 ≠ 5 = b₂. The condition k = 2 ≤ #a = 3 is satisfied.

*Displacement.* By TumblerSub, w = b ⊖ a: w₁ = 0 (i < k), w₂ = 5 − 2 = 3 (i = k), w₃ = 1 (i > k, from b). So w = [0, 3, 1].

*Round-trip.* The action point of w is 2. By TumblerAdd, a ⊕ [0, 3, 1]: position 1 copies a₁ = 1, position 2 computes 2 + 3 = 5, position 3 copies w₃ = 1. Result: [1, 5, 1] = b.  ✓

*Uniqueness check.* Suppose some other w' also satisfies a ⊕ w' = b = [1, 5, 1]. By D2, w' = b ⊖ a = [0, 3, 1] = w. There is no alternative displacement.

The generalization to #a < #b can be seen with a' = [1, 2] and the same b = [1, 5, 1]. Here #a' = 2 < 3 = #b, the divergence is still 2 (a'₂ = 2 ≠ 5 = b₂), and k = 2 ≤ #a' = 2 satisfies D0. TumblerSub (zero-padding a' to length 3) gives the same w = [0, 3, 1] of length 3. The round-trip a' ⊕ [0, 3, 1] produces [1, 5, 1] = b — the result has length #w = 3 = #b, matching the target.

*Formal Contract:*
- *Preconditions:* a ∈ T, b ∈ T, w ∈ T, a < b, divergence(a, b) ≤ #a, #a ≤ #b, a ⊕ w = b
- *Postconditions:* w = b ⊖ a


### Ordinal displacement and shift

**Definition (OrdinalDisplacement).** For natural number n ≥ 1 and depth m ≥ 1, the *ordinal displacement* δ(n, m) is the tumbler [0, 0, ..., 0, n] of length m — zero at positions 1 through m − 1, and n at position m. Its action point is m.

When the depth is determined by context (typically m = #v for the tumbler being shifted), we write δₙ.

*Formal Contract:*
- *Preconditions:* n ≥ 1, m ≥ 1
- *Definition:* δ(n, m) = [0, ..., 0, n] of length m, action point m

**Definition (OrdinalShift).** For a tumbler v of length m and natural number n ≥ 1:

`shift(v, n) = v ⊕ δ(n, m)`

By OrdinalDisplacement, δ(n, m) = [0, ..., 0, n] of length m with action point m; since n ≥ 1, the m-th component is nonzero, so δ(n, m) > 0. The preconditions of TA0 are therefore satisfied: δ(n, m) > 0, and the action point k = m = #v gives k ≤ #v. By TumblerAdd: shift(v, n)ᵢ = vᵢ for i < m, and shift(v, n)ₘ = vₘ + n. The shift advances the deepest component by exactly n, leaving all higher-level components unchanged.

Additionally, shift preserves structural properties. When m ≥ 2, the action point of δₙ leaves position 1 unchanged — shift(v, n)₁ = v₁. When m = 1, shift([S], n) = [S + n] changes the first component. Furthermore, #shift(v, n) = #δₙ = m = #v by the result-length identity of TumblerAdd. The shift preserves tumbler depth, and — since n ≥ 1 — component positivity: shift(v, n)ₘ = vₘ + n ≥ 1 unconditionally for all vₘ ≥ 0.

*Formal Contract:*
- *Preconditions:* v ∈ T, n ≥ 1
- *Definition:* shift(v, n) = v ⊕ δ(n, #v)
- *Postconditions:* shift(v, n)ᵢ = vᵢ for i < #v, shift(v, n) at position #v = v at position #v + n, #shift(v, n) = #v, shift(v, n) at position #v ≥ 1

**TS1 (ShiftOrderPreservation).**

`(A v₁, v₂, n : n ≥ 1 ∧ #v₁ = #v₂ = m ∧ v₁ < v₂ : shift(v₁, n) < shift(v₂, n))`

*Dependencies:*
- **OrdinalShift (Definition):** `shift(v, n) = v ⊕ δ(n, #v)`. Reduces the shift to tumbler addition with an ordinal displacement.
- **OrdinalDisplacement (Definition):** `δ(n, m) = [0, ..., 0, n]` of length `m`, with action point `m`. Supplies the displacement structure and its action point.
- **TA1-strict (Strict order preservation):** For `a < b`, `w > 0`, action point `k ≤ min(#a, #b)`, `k ≥ divergence(a, b)`: `a ⊕ w < b ⊕ w`. The workhorse — once its four preconditions are verified, the conclusion follows.
- **Divergence (Definition):** For `a ≠ b` with `#a = #b = m`, `divergence(a, b) = min({j : 1 ≤ j ≤ m ∧ aⱼ ≠ bⱼ})`. Supplies the bound `divergence(v₁, v₂) ≤ m` needed in precondition (iv).

*Proof.* We show that shifting two equal-length tumblers by the same positive amount preserves their strict ordering. The shift advances the deepest component of each operand by the same value, so the relative difference at the divergence point is untouched.

Fix `v₁, v₂ ∈ T` with `#v₁ = #v₂ = m` and `v₁ < v₂`, and fix `n ≥ 1`. By OrdinalShift, `shift(v₁, n) = v₁ ⊕ δ(n, m)` and `shift(v₂, n) = v₂ ⊕ δ(n, m)`, so the obligation reduces to showing `v₁ ⊕ δ(n, m) < v₂ ⊕ δ(n, m)`. We discharge this by verifying the four preconditions of TA1-strict with `a = v₁`, `b = v₂`, `w = δ(n, m)`, and `k = actionPoint(δ(n, m)) = m`:

(i) `v₁ < v₂` — given directly.

(ii) `δ(n, m) > 0` — by OrdinalDisplacement, `δ(n, m) = [0, ..., 0, n]` with `n ≥ 1`, so its `m`-th component is positive and the displacement exceeds the zero tumbler of length `m`.

(iii) `k ≤ min(#v₁, #v₂)` — the action point `k = m` (OrdinalDisplacement), and `min(#v₁, #v₂) = min(m, m) = m`, so `m ≤ m` holds.

(iv) `k ≥ divergence(v₁, v₂)` — since `#v₁ = #v₂ = m`, Divergence case (ii) (prefix divergence) is excluded: it requires `#v₁ ≠ #v₂`. Since `v₁ < v₂` implies `v₁ ≠ v₂`, case (i) applies: `divergence(v₁, v₂) = min({j : 1 ≤ j ≤ m ∧ v₁ⱼ ≠ v₂ⱼ})`, which satisfies `divergence(v₁, v₂) ≤ m`. The required `k = m ≥ divergence(v₁, v₂)` follows.

All four preconditions hold. TA1-strict yields `v₁ ⊕ δ(n, m) < v₂ ⊕ δ(n, m)`, that is, `shift(v₁, n) < shift(v₂, n)`. ∎

*Formal Contract:*
- *Preconditions:* v₁ ∈ T, v₂ ∈ T, n ≥ 1, #v₁ = #v₂ = m, v₁ < v₂
- *Postconditions:* shift(v₁, n) < shift(v₂, n)

**TS2 (ShiftInjectivity).**

`(A v₁, v₂, n : n ≥ 1 ∧ #v₁ = #v₂ = m : shift(v₁, n) = shift(v₂, n) ⟹ v₁ = v₂)`

*Dependencies:*
- **OrdinalShift (Definition):** `shift(v, n) = v ⊕ δ(n, #v)`. Reduces the shift to tumbler addition with an ordinal displacement.
- **OrdinalDisplacement (Definition):** `δ(n, m) = [0, ..., 0, n]` of length `m`, with action point `m`. Supplies the displacement structure and its action point.
- **TA-MTO (ManyToOne):** For `w > 0` with action point `k`, and `#a ≥ k`, `#b ≥ k`: `a ⊕ w = b ⊕ w ⟺ aᵢ = bᵢ` for all `1 ≤ i ≤ k`. The forward direction extracts componentwise agreement from equal sums.
- **T3 (Canonical representation):** `a = b ⟺ #a = #b ∧ (A i : 1 ≤ i ≤ #a : aᵢ = bᵢ)`. Assembles componentwise agreement into tumbler equality.

*Proof.* We show that the ordinal shift is injective: if two equal-length tumblers produce the same result under the same shift, they must be identical. The argument reduces the shift to tumbler addition, applies the cancellation property of TA-MTO, and recovers full equality from componentwise agreement.

Fix `v₁, v₂ ∈ T` with `#v₁ = #v₂ = m`, and fix `n ≥ 1`. Assume `shift(v₁, n) = shift(v₂, n)`. By OrdinalShift, `shift(v₁, n) = v₁ ⊕ δ(n, m)` and `shift(v₂, n) = v₂ ⊕ δ(n, m)`, so the assumption becomes `v₁ ⊕ δ(n, m) = v₂ ⊕ δ(n, m)`.

We apply TA-MTO with `w = δ(n, m)`, `a = v₁`, `b = v₂`, and verify its preconditions:

(i) `δ(n, m) > 0` — by OrdinalDisplacement, `δ(n, m) = [0, ..., 0, n]` with `n ≥ 1`, so its `m`-th component is positive and the displacement exceeds the zero tumbler of length `m`.

(ii) `#v₁ ≥ actionPoint(δ(n, m))` and `#v₂ ≥ actionPoint(δ(n, m))` — the action point of `δ(n, m)` is `m` (OrdinalDisplacement), and `#v₁ = #v₂ = m`, so `m ≥ m` holds for both.

All preconditions are satisfied. TA-MTO's forward direction yields: `v₁ ⊕ δ(n, m) = v₂ ⊕ δ(n, m)` implies `v₁ᵢ = v₂ᵢ` for all `1 ≤ i ≤ actionPoint(δ(n, m)) = m`. We therefore have `v₁ᵢ = v₂ᵢ` for every position `1 ≤ i ≤ m`.

Since `#v₁ = #v₂ = m` and `v₁ᵢ = v₂ᵢ` at every position `1 ≤ i ≤ m`, T3 (CanonicalRepresentation) gives `v₁ = v₂`. ∎

*Formal Contract:*
- *Preconditions:* v₁ ∈ T, v₂ ∈ T, n ≥ 1, #v₁ = #v₂ = m
- *Postconditions:* shift(v₁, n) = shift(v₂, n) ⟹ v₁ = v₂

**TS3 (ShiftComposition).**

`(A v, n₁, n₂ : n₁ ≥ 1 ∧ n₂ ≥ 1 ∧ #v = m : shift(shift(v, n₁), n₂) = shift(v, n₁ + n₂))`

*Dependencies:*
- **OrdinalShift (Definition):** `shift(v, n) = v ⊕ δ(n, #v)`. Reduces the shift to tumbler addition with an ordinal displacement.
- **OrdinalDisplacement (Definition):** `δ(n, m) = [0, ..., 0, n]` of length `m`, with action point `m`. Supplies the displacement structure and its action point.
- **TA0 (Well-defined addition):** For `a, w ∈ T` with `w > 0` and action point `k ≤ #a`, `a ⊕ w ∈ T` with `#(a ⊕ w) = #w`. Supplies the precondition check and the result-length identity.
- **TumblerAdd (Constructive definition):** `(a ⊕ w)ᵢ = aᵢ` for `i < k`, `(a ⊕ w)ₖ = aₖ + wₖ`, `(a ⊕ w)ᵢ = wᵢ` for `i > k`, where `k = actionPoint(w)`. The three-region rule expanded for each addition.
- **T3 (Canonical representation):** `a = b ⟺ #a = #b ∧ (A i : 1 ≤ i ≤ #a : aᵢ = bᵢ)`. Assembles componentwise agreement and equal length into tumbler equality.

*Proof.* We show that composing two ordinal shifts reduces to a single shift whose amount is the sum: shifting by `n₁` then `n₂` yields the same tumbler as shifting by `n₁ + n₂`.

Fix `v ∈ T` with `#v = m`, and fix `n₁ ≥ 1`, `n₂ ≥ 1`. We compute each side of the equation `shift(shift(v, n₁), n₂) = shift(v, n₁ + n₂)` by expanding OrdinalShift and TumblerAdd, then show the results agree at every component.

**Left side.** By OrdinalShift, `shift(v, n₁) = v ⊕ δ(n₁, m)`, where `δ(n₁, m) = [0, ..., 0, n₁]` has action point `m` (OrdinalDisplacement). The precondition of TA0 is satisfied: `k = m ≤ m = #v`. Let `u = v ⊕ δ(n₁, m)`. By TumblerAdd with action point `k = m`:

- For `1 ≤ i < m`: `uᵢ = vᵢ` (prefix copy — all `m − 1` higher-level components are preserved).
- At `i = m`: `uₘ = vₘ + n₁` (single-component advance).
- No positions `i > m` exist, since `#u = #δ(n₁, m) = m` by the result-length identity (TA0).

Now we apply the second shift. By OrdinalShift, `shift(u, n₂) = u ⊕ δ(n₂, m)`, where `δ(n₂, m)` has action point `m` (OrdinalDisplacement). The precondition of TA0 is satisfied: `k = m ≤ m = #u`. Let `L = u ⊕ δ(n₂, m)` denote the left side. By TumblerAdd with action point `k = m`:

- For `1 ≤ i < m`: `Lᵢ = uᵢ = vᵢ` (prefix copy, substituting the values of `u` established above).
- At `i = m`: `Lₘ = uₘ + n₂ = (vₘ + n₁) + n₂` (advance, substituting `uₘ = vₘ + n₁`).
- Length: `#L = #δ(n₂, m) = m` by the result-length identity (TA0).

**Right side.** Since `n₁ ≥ 1` and `n₂ ≥ 1`, their sum `n₁ + n₂ ≥ 2 ≥ 1`, so `δ(n₁ + n₂, m)` is a well-formed ordinal displacement with action point `m` (OrdinalDisplacement). By OrdinalShift, `shift(v, n₁ + n₂) = v ⊕ δ(n₁ + n₂, m)`. The precondition of TA0 is satisfied: `k = m ≤ m = #v`. Let `R = v ⊕ δ(n₁ + n₂, m)` denote the right side. By TumblerAdd with action point `k = m`:

- For `1 ≤ i < m`: `Rᵢ = vᵢ` (prefix copy).
- At `i = m`: `Rₘ = vₘ + (n₁ + n₂)` (single-component advance).
- Length: `#R = #δ(n₁ + n₂, m) = m` by the result-length identity (TA0).

**Comparison.** Both sides have length `m`: `#L = m = #R`. We verify componentwise equality:

- For `1 ≤ i < m`: `Lᵢ = vᵢ = Rᵢ` — both sides copied the prefix from `v`.
- At `i = m`: `Lₘ = (vₘ + n₁) + n₂` and `Rₘ = vₘ + (n₁ + n₂)`. These are equal by the associativity of addition in ℕ: `(vₘ + n₁) + n₂ = vₘ + (n₁ + n₂)`.

Every component agrees and both tumblers have the same length. By T3 (CanonicalRepresentation): `L = R`, that is, `shift(shift(v, n₁), n₂) = shift(v, n₁ + n₂)`. ∎

*Formal Contract:*
- *Preconditions:* v ∈ T, n₁ ≥ 1, n₂ ≥ 1, #v = m
- *Postconditions:* shift(shift(v, n₁), n₂) = shift(v, n₁ + n₂)
- *Frame:* #shift(shift(v, n₁), n₂) = #v = m (shift preserves tumbler length)

**TS4 (ShiftStrictIncrease).**

`(A v, n : n ≥ 1 ∧ #v = m : shift(v, n) > v)`

*Dependencies:*
- **OrdinalShift (Definition):** `shift(v, n) = v ⊕ δ(n, #v)`. Reduces the shift to tumbler addition with an ordinal displacement.
- **OrdinalDisplacement (Definition):** `δ(n, m) = [0, ..., 0, n]` of length `m`, with action point `m`. Supplies the displacement structure and its action point.
- **TA-strict (Strict increase):** For `a ∈ T` and `w > 0` with action point `k ≤ #a`: `a ⊕ w > a`. Guarantees that adding a positive displacement advances a tumbler forward.

*Proof.* We show that shifting a tumbler by a positive ordinal amount produces a result strictly greater than the original. The argument reduces the shift to tumbler addition and then invokes the strict-increase axiom.

Fix `v ∈ T` with `#v = m`, and fix `n ≥ 1`. By OrdinalShift, `shift(v, n) = v ⊕ δ(n, m)`, so the obligation reduces to showing `v ⊕ δ(n, m) > v`. We discharge this by applying TA-strict with `a = v` and `w = δ(n, m)`. TA-strict requires two preconditions: `w > 0`, and `actionPoint(w) ≤ #a`. We verify each in turn.

*First precondition: `δ(n, m) > 0`.* By OrdinalDisplacement, `δ(n, m) = [0, ..., 0, n]` of length `m`, with `n` at position `m`. Since `n ≥ 1`, component `m` is positive, so `δ(n, m)` is not the zero tumbler — that is, `δ(n, m) > 0`.

*Second precondition: `actionPoint(δ(n, m)) ≤ #v`.* By OrdinalDisplacement, the action point of `δ(n, m)` is `m` — position `m` is the first nonzero component, since positions 1 through `m − 1` are zero and position `m` is `n ≥ 1`. Since `#v = m`, the required `m ≤ m` holds.

Both preconditions are satisfied. TA-strict yields `v ⊕ δ(n, m) > v`, that is, `shift(v, n) > v`. ∎

*Formal Contract:*
- *Preconditions:* v ∈ T, n ≥ 1, #v = m
- *Postconditions:* shift(v, n) > v

**TS5 (ShiftAmountMonotonicity).**

`(A v, n₁, n₂ : n₁ ≥ 1 ∧ n₂ > n₁ ∧ #v = m : shift(v, n₁) < shift(v, n₂))`

*Dependencies:*
- **TS3 (ShiftComposition):** `shift(shift(v, n₁), n₂) = shift(v, n₁ + n₂)` for `n₁ ≥ 1`, `n₂ ≥ 1`, `#v = m`. Decomposes a larger shift into a composition of two smaller shifts.
- **TS4 (ShiftStrictIncrease):** `shift(v, n) > v` for `n ≥ 1`, `#v = m`. Guarantees that any positive shift advances a tumbler strictly forward.
- **TA0 (Well-defined addition):** For `a, w ∈ T` with `w > 0` and action point `k ≤ #a`, `a ⊕ w ∈ T` with `#(a ⊕ w) = #w`. Supplies the result-length identity needed to confirm that shift preserves tumbler length.

*Proof.* We show that shifting a tumbler by a larger amount produces a strictly greater result. The argument decomposes the larger shift into the smaller shift followed by an additional positive shift, then applies strict increase to the remainder.

Fix `v ∈ T` with `#v = m`, and fix `n₁ ≥ 1` and `n₂ > n₁`. We must prove `shift(v, n₁) < shift(v, n₂)`.

Define `d = n₂ − n₁`. Since `n₂ > n₁` and both are natural numbers, `d ≥ 1`. Since `n₁ ≥ 1`, the decomposition `n₂ = n₁ + d` holds with both summands positive.

We invoke TS3 (ShiftComposition) with tumbler `v`, first shift `n₁`, second shift `d`. The preconditions are `n₁ ≥ 1` (given), `d ≥ 1` (established above), and `#v = m` (given), all satisfied. Therefore `shift(shift(v, n₁), d) = shift(v, n₁ + d) = shift(v, n₂)`. This expresses the larger shift as a composition: first shift by `n₁`, then shift the result by `d`.

Let `u = shift(v, n₁)`. We need `#u = m` to invoke TS4 on `u`. By the definition of shift, `u = v ⊕ δ(n₁, m)`, and by TA0 (result-length identity), `#u = #δ(n₁, m) = m`. So `u ∈ T` with `#u = m`. The composition identity gives `shift(v, n₂) = shift(u, d)`.

We invoke TS4 (ShiftStrictIncrease) with tumbler `u` and shift amount `d`. The preconditions are `d ≥ 1` (established above) and `#u = m` (just confirmed), both satisfied. Therefore `shift(u, d) > u`.

Substituting: `shift(v, n₂) = shift(u, d) > u = shift(v, n₁)`, that is, `shift(v, n₁) < shift(v, n₂)`. ∎

*Formal Contract:*
- *Preconditions:* v ∈ T, n₁ ≥ 1, n₂ > n₁, #v = m
- *Postconditions:* shift(v, n₁) < shift(v, n₂)


## Increment for allocation

A separate operation, distinct from the shifting arithmetic, handles address allocation. When the system allocates a new address, it takes the highest existing address in a partition and produces the next one. This is not addition of a width; it is advancement of a counter at a specified hierarchical level.

We define the *last significant position* of a tumbler `t`. When `t` has at least one nonzero component, `sig(t) = max({i : 1 ≤ i ≤ #t ∧ tᵢ ≠ 0})` — the position of the last nonzero component. When every component is zero, `sig(t) = #t`.

For valid addresses, `sig(t)` falls within the last populated field. This is a consequence of T4's positive-component constraint: every field component is strictly positive, so the last component of the last field is nonzero, and `sig(t) = #t`. Therefore `inc(t, 0)` on a valid address increments the last component of the last field, modifying only within that field and preserving the hierarchical structure.

**TA5 (Hierarchical increment).** For tumbler `t ∈ T` and level `k ≥ 0`, there exists an operation `inc(t, k)` producing tumbler `t'` such that:

  (a) `t' > t` (strictly greater under T1),

  (b) `t'` agrees with `t` on all components before the increment point,

  (c) when `k = 0` (*sibling*): `#t' = #t`, and `t'` differs from `t` only at position `sig(t)`, where `t'_{sig(t)} = t_{sig(t)} + 1`,

  (d) when `k > 0` (*child*): `#t' = #t + k`, the `k - 1` intermediate positions `#t + 1, ..., #t + k - 1` are set to `0` (field separators), and the final position `#t + k` is set to `1` (the first child).

*Dependencies:*
- **T1 (Lexicographic order):** `a < b` iff there exists `k ≥ 1` with `aᵢ = bᵢ` for all `i < k`, and either (i) `k ≤ min(#a, #b)` and `aₖ < bₖ`, or (ii) `k = #a + 1 ≤ #b` (proper prefix).
- **sig(t):** The last significant position of `t`. When `t` has at least one nonzero component, `sig(t) = max({i : 1 ≤ i ≤ #t ∧ tᵢ ≠ 0})`; when every component of `t` is zero, `sig(t) = #t`.

*Proof.* We must show that for every `t ∈ T` and `k ≥ 0`, there exists a tumbler `t' = inc(t, k) ∈ T` satisfying postconditions (a)–(d). We proceed by construction, then verify each postcondition.

**Construction.** Let `t = t₁. ... .tₘ` where `m = #t`, and let `k ≥ 0`. We define `t' = inc(t, k)` by cases.

When `k = 0` (*sibling increment*): set `t'ᵢ = tᵢ` for all `i ≠ sig(t)`, and `t'_{sig(t)} = t_{sig(t)} + 1`. The result has the same length `#t' = m`, since we modify one component in place. Since each component remains a natural number — the unmodified ones by hypothesis on `t`, the modified one because ℕ is closed under successor — and the length `m ≥ 1` is preserved, we have `t' ∈ T`.

When `k > 0` (*child creation*): set `t'ᵢ = tᵢ` for `1 ≤ i ≤ m`, set `t'ᵢ = 0` for `m + 1 ≤ i ≤ m + k - 1` (the `k - 1` field separators), and set `t'_{m+k} = 1` (the first child). The result has length `#t' = m + k ≥ 1 + 1 = 2`, since `m ≥ 1` and `k ≥ 1`. Every component is a natural number — the first `m` by hypothesis, the intermediates are `0 ∈ ℕ`, the final is `1 ∈ ℕ` — so `t' ∈ T`.

**Verification of (b)** (agreement before the increment point). For `k = 0`: the construction modifies only position `sig(t)`, leaving every position `i` with `1 ≤ i < sig(t)` unchanged: `t'ᵢ = tᵢ`. For `k > 0`: the first `m` components of `t'` are copied verbatim from `t`, so `t'ᵢ = tᵢ` for all `1 ≤ i ≤ m`. Since all original positions of `t` precede the extension, `t'` agrees with `t` on every original position.

**Verification of (c)** (sibling structure, `k = 0`). The length is preserved: `#t' = m = #t`, since we replaced one component without extending or shortening the sequence. The only modified position is `sig(t)`, where `t'_{sig(t)} = t_{sig(t)} + 1` by construction. For every position `i ≠ sig(t)`, we have `t'ᵢ = tᵢ` by construction — the modification is confined to a single component.

**Verification of (d)** (child structure, `k > 0`). The length is `#t' = m + k = #t + k` by construction. The `k - 1` positions from `m + 1` through `m + k - 1` are each set to `0` (field separators); when `k = 1` this range is empty, which is correct — descending one level requires no separator. The final position `m + k` is set to `1` (the first child in the new level).

**Verification of (a)** (`t' > t`). We must establish `t < t'` under the lexicographic order T1. The two cases require different clauses of the order.

*Case `k = 0`.* Let `j = sig(t)`. We claim `j` is the divergence position: for all `1 ≤ i < j`, part (b) gives `t'ᵢ = tᵢ`, so the tumblers agree below `j`. At position `j` itself, `t'_j = t_j + 1 > t_j`, since `n + 1 > n` for every `n ∈ ℕ`. We need `j ≤ min(#t, #t')` to apply T1 case (i). We have `j = sig(t) ≤ m = #t` by definition of `sig`, and `#t' = m` by part (c), so `j ≤ min(m, m) = m`. T1 case (i) applies with divergence position `j`: the agreement on `1, ..., j - 1` and the strict inequality `t_j < t'_j` yield `t < t'`.

*Case `k > 0`.* By part (b), `t'ᵢ = tᵢ` for all `1 ≤ i ≤ m` — the tumblers agree at every position of `t`. Since `#t' = m + k > m = #t`, the tumbler `t'` extends beyond `t`. We verify T1 case (ii): setting `k_{\text{wit}} = m + 1 = #t + 1`, we need `k_{\text{wit}} ≤ #t'`. Indeed `m + 1 ≤ m + k` because `k ≥ 1`. The first `m` components agree and `t` has no component at position `m + 1`, so `t` is a proper prefix of `t'`. T1 case (ii) gives `t < t'`. ∎

*Formal Contract:*
- *Definition:* `inc(t, k)` for `t ∈ T`, `k ≥ 0`: when `k = 0`, produce the sequence that agrees with `t` everywhere except at position `sig(t)`, where the value is `t_{sig(t)} + 1`; when `k > 0`, extend `t` by `k` positions — `k - 1` zeros followed by `1`.
- *Preconditions:* `t ∈ T`, `k ∈ ℕ` with `k ≥ 0`.
- *Postconditions:* (a) `t' > t` under T1. (b) `(A i : 1 ≤ i < sig(t) : t'ᵢ = tᵢ)` when `k = 0`; `(A i : 1 ≤ i ≤ #t : t'ᵢ = tᵢ)` when `k > 0`. (c) When `k = 0`: `#t' = #t`, and `t'` differs from `t` only at position `sig(t)`, where `t'_{sig(t)} = t_{sig(t)} + 1`. (d) When `k > 0`: `#t' = #t + k`, `(A i : #t + 1 ≤ i ≤ #t + k - 1 : t'ᵢ = 0)`, and `t'_{#t+k} = 1`.
- *Frame:* When `k = 0`: all positions except `sig(t)` are unchanged, and length is preserved. When `k > 0`: all original positions `1, ..., #t` are unchanged.

Gregory's analysis reveals a critical distinction: `inc(t, 0)` does NOT produce the immediate successor of `t` in the total order. It produces the *next peer* at the same hierarchical depth — the smallest tumbler with the same length that is strictly greater than `t`. The gap between `t` and `inc(t, 0)` contains the entire subtree of `t`: all tumblers of the form `t.x₁. ... .xₘ` for any `m ≥ 1` and any `x₁ ≥ 0`. The true immediate successor in the total order is `t.0` — the zero-extension — by the prefix convention (T1 case (ii)). For any `k > 0`, `inc(t, k)` does NOT produce the immediate successor of `t` in the total order. For `k = 1` the result is `t.1`; for `k = 2` the result is `t.0.1`. In both cases, `t.0` (the true immediate successor) lies strictly between `t` and the result. The gap between `t` and `inc(t, k)` contains `t`'s entire subtree of zero-extensions. For address allocation, the distinction is harmless: allocation cares about advancing the counter past all existing addresses, not about visiting every point in the total order.

**TA5 preserves T4 when `k ≤ 2` and `zeros(t) + k - 1 ≤ 3`.** Two constraints must hold simultaneously: the zero-count bound and a structural constraint against adjacent zeros.

For `k = 0`: no zeros are added — `zeros(t') = zeros(t)`, and no new adjacencies are introduced. T4 is preserved unconditionally.

For `k = 1`: one component is appended (the child value `1`), with no new zero separators — `zeros(t') = zeros(t)`. Since the appended component is positive and the last component of `t` is positive (by T4), no adjacent zeros are created. T4 is preserved when `zeros(t) ≤ 3`.

For `k = 2`: one zero separator and one child value `1` are appended, giving `zeros(t') = zeros(t) + 1`. The appended sequence is `[0, 1]` — the zero is flanked by the last component of `t` (positive, by T4's non-empty field constraint) and the new child `1`, so no adjacent zeros are created. T4 is preserved when `zeros(t) ≤ 2`.

For `k ≥ 3`: the appended sequence `[0, 0, ..., 0, 1]` contains `k - 1 ≥ 2` zeros, of which at least two are adjacent. This violates T4's non-empty field constraint — the adjacent zeros create an empty field. Consider `inc([1], 3)` producing `[1, 0, 0, 1]`: zero count is 2 (≤ 3), but positions 2 and 3 are adjacent zeros, parsing as node `[1]`, separator, *empty user field*, separator, document `[1]`. The empty field violates T4 regardless of the zero count. So T4 is violated for all `k ≥ 3`.

The effective constraints are: `k = 0` (always valid), `k = 1` (when `zeros(t) ≤ 3`), `k = 2` (when `zeros(t) ≤ 2`). The hierarchy enforces this naturally: each `inc(·, k)` with `k > 0` introduces one new hierarchical level, and the address format has exactly four fields with three separators, so at most three new separators can be introduced from a node address (the three `inc(·, 2)` steps from node to element level, with `zeros(t) = 0, 1, 2` respectively before each step, each satisfying `zeros(t) ≤ 2`).


## Zero tumblers and positivity

Under T3, the tumblers `[0]`, `[0, 0]`, `[0, 0, 0]`, etc., are *distinct* elements of T — they have different lengths. Under T1, they form a chain: `[0] < [0, 0] < [0, 0, 0] < ...` by the prefix rule. There is no single "zero tumbler"; there are infinitely many all-zero tumblers.

**Definition (PositiveTumbler).** A tumbler `t ∈ T` is *positive*, written `t > 0`, iff at least one of its components is nonzero: `(E i : 1 ≤ i ≤ #t : tᵢ ≠ 0)`. A tumbler is a *zero tumbler* iff every component is zero: `(A i : 1 ≤ i ≤ #t : tᵢ = 0)`.

Every positive tumbler is greater than every zero tumbler under T1 — if `t` has a nonzero component at position `k`, then at position `k` either the zero tumbler has a smaller component (0 < tₖ) or has run out of components, either way placing it below `t`. The condition `w > 0` in TA0 and TA4 excludes all all-zero displacements regardless of length.

**TA6 (Zero tumblers).** No zero tumbler is a valid address — no all-zero tumbler designates content. Every zero tumbler is less than every positive tumbler under T1.

  `(A t ∈ T : (A i : 1 ≤ i ≤ #t : tᵢ = 0) ⟹ t is not a valid address)`

  `(A s, t ∈ T : (A i : 1 ≤ i ≤ #s : sᵢ = 0) ∧ (E j : 1 ≤ j ≤ #t : tⱼ > 0) ⟹ s < t)`

*Dependencies:*
- **T1 (Lexicographic order):** `a < b` iff there exists `k ≥ 1` with `aᵢ = bᵢ` for all `i < k`, and either (i) `k ≤ min(#a, #b)` and `aₖ < bₖ`, or (ii) `k = #a + 1 ≤ #b` (proper prefix).
- **T4 (Hierarchical parsing):** Every valid address satisfies the positive-component constraint — every field component is strictly positive. In particular, the first component belongs to the node field, which has at least one component, so `t₁ > 0` for every valid address.

*Proof.* We prove the two conjuncts separately.

**Conjunct 1** (invalidity): Let `t` be a zero tumbler, so `tᵢ = 0` for all `1 ≤ i ≤ #t`. In particular `t₁ = 0`. By T4, every valid address satisfies `t₁ > 0`. Since `t₁ = 0`, the tumbler `t` violates T4 and is therefore not a valid address.

**Conjunct 2** (ordering): Let `s` be a zero tumbler of length `m`, so `sᵢ = 0` for all `1 ≤ i ≤ m`. Let `t` be a tumbler of length `n` with at least one positive component — there exists `j` with `1 ≤ j ≤ n` and `tⱼ > 0`. We must show `s < t`.

Define `k = min({i : 1 ≤ i ≤ n : tᵢ > 0})` — the position of the first positive component in `t`. This minimum exists because `t` has at least one positive component. By minimality of `k`, we have `tᵢ = 0` for all `1 ≤ i < k`, and `tₖ > 0`. Since `k` is a position in `t`, we have `k ≤ n`.

*Case 1* (`k ≤ m`): For all positions `1 ≤ i < k`, `sᵢ = 0` (since `s` is a zero tumbler) and `tᵢ = 0` (by minimality of `k`), so `sᵢ = tᵢ`. At position `k`, `sₖ = 0 < tₖ` (since `tₖ > 0`). Since `k ≤ m` and `k ≤ n`, we have `k ≤ min(m, n)`, so this divergence falls within the shared length. T1 case (i) applies with witness `k`, giving `s < t`.

*Case 2* (`k > m`): For all positions `1 ≤ i ≤ m`, we have `i ≤ m < k`, so `tᵢ = 0` (by minimality of `k`) and `sᵢ = 0` (since `s` is a zero tumbler), giving `sᵢ = tᵢ`. The tumblers agree at every position of `s`. Since `m < k ≤ n`, we have `m < n`, so `m + 1 ≤ n`. T1 case (ii) applies with witness `m + 1`: the first `m` components agree and `m + 1 ≤ n`, so `s` is a proper prefix of `t`. Hence `s < t`. ∎

*Formal Contract:*
- *Postconditions:* (a) `(A t ∈ T : (A i : 1 ≤ i ≤ #t : tᵢ = 0) ⟹ t is not a valid address)`. (b) `(A s, t ∈ T : (A i : 1 ≤ i ≤ #s : sᵢ = 0) ∧ (E j : 1 ≤ j ≤ #t : tⱼ > 0) ⟹ s < t)`.

Zero tumblers serve as *sentinels*: they mark uninitialized values, denote "unbounded" when used as span endpoints, and act as lower bounds.


## Subspace closure

When arithmetic advances a position within one element subspace, the result must remain in that subspace. Text positions must not cross into link space, and vice versa.

An element-local position within subspace `S` has two components: the subspace identifier `N` and the ordinal `x`. A natural first attempt at an element-local displacement is `w = [0, n]` — action point `k = 2`, preserving the subspace identifier and advancing the ordinal. Addition works: `[N, x] ⊕ [0, n] = [N, x + n]`, preserving the subspace. But subtraction exposes a subtlety: `[N, x] ⊖ [0, n]` finds the first divergence at position 1 (where `N ≠ 0`), not at position 2 where the intended action lies. The subtraction produces `[N - 0, x] = [N, x]` — a no-op. The abstract `⊖` cannot shift a position backward by a displacement that disagrees with the position at the subspace identifier.

Gregory's implementation reveals the resolution. The operands passed to the arithmetic during shifts are not full element-local positions; they are *within-subspace ordinals* — the second component alone. The subspace identifier is not an operand to the shift; it is structural context that determines *which* positions are subject to the shift. The arithmetic receives ordinals, not full positions.

**TA7a (Subspace closure).** The canonical representation for shift arithmetic is the *ordinal-only* formulation: a position in a subspace with identifier `N` and ordinal `o = [o₁, ..., oₘ]` (where `m ≥ 1`) is represented as the tumbler `o` for arithmetic purposes, with `N` held as structural context. Define **S** = {o ∈ T : #o ≥ 1 ∧ (A i : 1 ≤ i ≤ #o : oᵢ > 0)} — ordinals with all positive components, matching T4's positive-component constraint on element fields. An element-local displacement is a positive tumbler `w` with action point `k` satisfying `1 ≤ k ≤ m`. In this formulation:

  `(A o ∈ S, w > 0 : k ≤ #o ⟹ o ⊕ w ∈ T)`

  `(A o ∈ S, w > 0 : o ≥ w ⟹ o ⊖ w ∈ T)`

Both claims assert closure in T: arithmetic on ordinals, with the subspace identifier held as structural context, produces results that remain in T. The subspace identifier is not an operand — it determines *which* positions are subject to the shift, but never enters the arithmetic. This design ensures that no shift can escape the subspace.

The ordinal-only formulation is not arbitrary. The natural 2-component formulation `[N, x]` fails for subtraction: `[N, x] ⊖ [0, n]` finds the divergence at position 1 (where `N > 0 = 0`), producing `[N, x]` — a no-op rather than a genuine shift. Stripping the subspace identifier from the operands avoids this degeneracy.

*Dependencies:*
- **TA0 (Well-defined addition):** For `a, w ∈ T` with `w > 0` and action point `k ≤ #a`, `a ⊕ w ∈ T` with `#(a ⊕ w) = #w`. Supplies T-membership and the result-length identity for Conjunct 1.
- **TA2 (Well-defined subtraction):** For `a, w ∈ T` with `a ≥ w`, `a ⊖ w ∈ T` with `#(a ⊖ w) = max(#a, #w)`. Supplies T-membership and the result-length identity for Conjunct 2.
- **TumblerAdd (Constructive definition):** `(a ⊕ w)ᵢ = aᵢ` for `i < k`, `(a ⊕ w)ₖ = aₖ + wₖ`, `(a ⊕ w)ᵢ = wᵢ` for `i > k`, where `k = actionPoint(w)`. Used to determine which components of `o ⊕ w` are positive (S-membership analysis).
- **TumblerSub (Constructive definition):** Zero-pad both operands to length `max(#a, #w)`, find the first divergence `d`; `rᵢ = 0` for `i < d`, `r_d = a_d - w_d`, `rᵢ = aᵢ` for `i > d`. If no divergence, the result is the zero tumbler of length `max(#a, #w)`. Used in the case analysis of S-membership under subtraction.
- **T1 (Lexicographic order):** At the first divergence position `d` with `d ≤ min(#a, #b)`, `a > b` requires `a_d > b_d`. Used to establish `o_d > w_d` in the subtraction case analysis.
- **TA6 (Zero sentinel):** The zero tumbler `[0, ..., 0]` is a member of T. Referenced for the boundary case where subtraction yields a zero tumbler.

*Proof.* We prove each conjunct of TA7a — that the stated operations preserve membership in T — then analyze the finer question of S-membership: whether the results retain all positive components.

Let `o = [o₁, ..., oₘ]` with `o ∈ S`, so `m ≥ 1` and every `oᵢ > 0`. Let `w` be a positive tumbler with action point `k = min({i : 1 ≤ i ≤ #w ∧ wᵢ ≠ 0})`.

**Conjunct 1** (`⊕`-closure in T). The precondition gives `o ∈ T` (since `S ⊆ T` by definition), `w ∈ T`, `w > 0`, and `k ≤ #o = m`. These are exactly the preconditions of TA0. By TA0, `o ⊕ w ∈ T`, with `#(o ⊕ w) = #w`. The subspace identifier, held as structural context outside the operands, is untouched.

We now establish when the stronger conclusion `o ⊕ w ∈ S` holds. By TumblerAdd, the result `r = o ⊕ w` is built in three regions relative to the action point `k`: `rᵢ = oᵢ` for `1 ≤ i < k` (prefix from start), `rₖ = oₖ + wₖ` (advance), and `rᵢ = wᵢ` for `k < i ≤ #w` (tail from displacement). In the prefix region, each `rᵢ = oᵢ > 0` because `o ∈ S`. At the action point, `rₖ = oₖ + wₖ > 0` because `oₖ > 0` (from `o ∈ S`) and `wₖ > 0` (by definition of action point). In the tail region, each `rᵢ = wᵢ` — copied verbatim from the displacement. The result is in S precisely when every tail component `wᵢ` (for `i > k`) is also positive. For single-component ordinals — the common case — this question does not arise: `[x] ⊕ [n] = [x + n]`, which is unconditionally in S since `x > 0` and `n > 0`.

For example, spanning from ordinal `[1, 3, 2]` to `[1, 5, 7]` requires displacement `[0, 2, 7]` (action point `k = 2`). TumblerAdd produces `[1, 3 + 2, 7] = [1, 5, 7]` — position 1 of the ordinal is copied from the start, preserving the ordinal prefix.

**Conjunct 2** (`⊖`-closure in T). The precondition gives `o ∈ T` (since `S ⊆ T`), `w ∈ T`, and `o ≥ w`. These are exactly the preconditions of TA2. By TA2, `o ⊖ w ∈ T`, with `#(o ⊖ w) = max(m, #w)`. The subspace identifier is again untouched.

The S-membership question for `⊖` is more delicate. We perform exhaustive case analysis on the action point `k` of `w` and the divergence position `d` of TumblerSub. Recall TumblerSub's constructive rule: zero-pad both operands to length `max(m, #w)`, find the divergence position `d` (the first position where the padded sequences differ), then set `rᵢ = 0` for `i < d`, `r_d = o_d - w_d`, and `rᵢ = oᵢ` for `i > d`.

*Preliminary: when `#w > m`.* TumblerSub produces a result of length `max(m, #w) = #w > m`. The zero-padded minuend has `oᵢ = 0` at positions `m + 1` through `#w`, so the result inherits zeros at those trailing positions and lies in T \ S. The result nonetheless lies in T, confirming the closure claim. The remaining cases assume `#w ≤ m`, giving result length `m`.

*Case `k ≥ 2`:* The displacement has `wᵢ = 0` for all `i < k`, so in particular `w₁ = 0`. Since `o ∈ S`, `o₁ > 0`, and therefore `o₁ ≠ w₁`. The divergence falls at `d = 1`. TumblerSub produces: `r₁ = o₁ - 0 = o₁ > 0`, and `rᵢ = oᵢ > 0` for `1 < i ≤ m` (copied from the minuend since `i > d = 1`). Every component of the result equals the corresponding component of `o`, so the result is `o` itself — the subtraction is a no-op. The result is trivially in S. This is the vacuous closure: TumblerSub discovers the mismatch at the ordinal's first positive component rather than at the displacement's intended action point.

*Case `k = 1`, divergence `d = 1`:* The displacement has `w₁ > 0`, and `o₁ ≠ w₁`. Since `o ≥ w` and the first divergence is at position 1, T1 requires `o₁ > w₁`. TumblerSub produces: `r₁ = o₁ - w₁ > 0` (since `o₁ > w₁ ≥ 1` gives `o₁ - w₁ ≥ 1`), and `rᵢ = oᵢ > 0` for `1 < i ≤ m` (copied from the minuend). All components are positive; the result is in S.

*Case `k = 1`, divergence `d > 1`:* The displacement has `w₁ > 0`, and `o₁ = w₁` — the operands agree at position 1, with divergence at some later `d > 1`. TumblerSub zeros all positions before `d`: `rᵢ = 0` for `1 ≤ i < d`. In particular `r₁ = 0`, so the result has a zero first component and is not in S. Counterexample: `o = [5, 3]`, `w = [5, 1]` (action point `k = 1`, divergence `d = 2`). TumblerSub yields `r = [0, 3 - 1] = [0, 2]`. We have `[0, 2] ∈ T` (confirming the T-closure claim) but `[0, 2] ∉ S ∪ Z`. This case arises when `o` and `w` share a leading prefix — the subtraction produces a displacement-like tumbler with leading zeros rather than a valid ordinal position.

For single-component ordinals, the `d > 1` case cannot arise (there is only one position), and `⊖` gives closure in S ∪ Z: `[x] ⊖ [n]` yields `[x - n] ∈ S` when `x > n`, or `[0] ∈ Z` when `x = n` (a zero sentinel by TA6).

In every case, the result lies in T. The subspace identifier, held as structural context outside the operands, is never modified by either operation. TA7a holds. ∎

The restriction to element-local displacements is necessary. An unrestricted displacement whose action point falls at the subspace-identifier position could produce an address in a different subspace — TA7a cannot hold for arbitrary `w`.

*Formal Contract:*
- *Preconditions:* For `⊕`: `o ∈ S`, `w ∈ T`, `w > 0`, `actionPoint(w) ≤ #o`. For `⊖`: `o ∈ S`, `w ∈ T`, `o ≥ w`.
- *Postconditions:* `o ⊕ w ∈ T`. `o ⊖ w ∈ T`. For `⊕`, the result is in S when all tail components of `w` (after the action point) are positive.
- *Frame:* The subspace identifier `N`, held as structural context, is not an operand and is never modified by either operation.
- *Definition:* **S** = {o ∈ T : #o ≥ 1 ∧ (A i : 1 ≤ i ≤ #o : oᵢ > 0)} — ordinals with all positive components, matching T4's positive-component constraint on element fields.


## What tumbler arithmetic is NOT

We must state explicitly what the tumbler algebra does not guarantee. These negative results constrain what an implementer may assume.

**The algebra is not a group.** There is no additive identity — the zero tumbler is a sentinel, not a neutral element for addition. There is no additive inverse for every element — subtraction is only defined when `a ≥ w`. The algebra is not closed under subtraction in general.

**TA-assoc (AdditionAssociative).** Addition is associative where both compositions are defined: `(a ⊕ b) ⊕ c = a ⊕ (b ⊕ c)` whenever both sides are well-defined. Three cases exhaust the possibilities. Let `k_b` and `k_c` be the action points of `b` and `c` respectively. When `k_b < k_c`: both sides produce `aᵢ` for `i < k_b`, `aₖ_b + bₖ_b` at `k_b`, `bᵢ` for `k_b < i < k_c`, `bₖ_c + cₖ_c` at `k_c`, and `cᵢ` beyond — identical. When `k_b = k_c = k`: both sides produce `aₖ + bₖ + cₖ` at `k` (natural-number addition is associative) and `cᵢ` beyond — identical. When `k_b > k_c`: both sides produce `aₖ_c + cₖ_c` at `k_c` and `cᵢ` beyond — identical (the deeper displacement `b` is overwritten by the shallower `c` in both cases). The domain conditions are asymmetric — the left side requires `k_b ≤ #a`, while the right requires only `min(k_b, k_c) ≤ #a` — but on the intersection, the values agree.

The design does not depend on associativity. Shifts are applied as single operations in practice, never composed from multiple smaller shifts. An implementation with finite representations may break associativity through overflow at the action-point component, but the abstract algebra carries no such limitation.

*Dependencies:*
- **TA0 (Well-defined addition):** For `a, w ∈ T` with `w > 0` and action point `k ≤ #a`, `a ⊕ w ∈ T` with `#(a ⊕ w) = #w`. Supplies the result-length identity and domain conditions.
- **TumblerAdd (Constructive definition):** `(x ⊕ w)ᵢ = xᵢ` for `i < k`, `(x ⊕ w)ₖ = xₖ + wₖ`, `(x ⊕ w)ᵢ = wᵢ` for `i > k`, where `k = actionPoint(w)`. The three-region rule expanded throughout.
- **T3 (Canonical representation):** `a = b ⟺ #a = #b ∧ (A i : 1 ≤ i ≤ #a : aᵢ = bᵢ)`. Used in the forward direction to conclude equality from length agreement and componentwise agreement.

*Proof.* We show that for all `a, b, c ∈ T` with `b > 0`, `c > 0`, whenever both `(a ⊕ b) ⊕ c` and `a ⊕ (b ⊕ c)` are well-defined, every component of the left side equals the corresponding component of the right side.

Throughout, write `k_b` for the action point of `b` and `k_c` for the action point of `c`. Recall TumblerAdd's constructive definition: for `x ⊕ w` with `w` having action point `k`, the result has `(x ⊕ w)ᵢ = xᵢ` for `i < k` (prefix copy), `(x ⊕ w)ₖ = xₖ + wₖ` (advance), and `(x ⊕ w)ᵢ = wᵢ` for `i > k` (tail copy), with `#(x ⊕ w) = #w` (the result-length identity from TA0).

*Lengths.* By the result-length identity, `#(a ⊕ b) = #b`. Applying it again: `#((a ⊕ b) ⊕ c) = #c`. For the right side, `#(b ⊕ c) = #c`, and `#(a ⊕ (b ⊕ c)) = #(b ⊕ c) = #c`. Both sides have length `#c`.

*Action point of `s = b ⊕ c`.* We must determine `actionPoint(s)` to expand the right side `a ⊕ s`. By TumblerAdd on `b ⊕ c`: `sᵢ = bᵢ` for `i < k_c`, `s_{k_c} = b_{k_c} + c_{k_c}`, and `sᵢ = cᵢ` for `i > k_c`. The action point of `s` is the first position with a nonzero component. For `i < min(k_b, k_c)`, we have `i < k_b` (so `bᵢ = 0` by definition of action point) and `i < k_c` (so `sᵢ = bᵢ = 0` by the prefix-copy rule). At position `min(k_b, k_c)` three sub-cases arise. If `k_b < k_c`: `s_{k_b} = b_{k_b} > 0`, since `k_b` is the action point of `b` and `k_b < k_c` places it in the prefix-copy region. If `k_b = k_c`: `s_{k_b} = b_{k_b} + c_{k_b} > 0`, since both summands are positive action-point values. If `k_b > k_c`: `s_{k_c} = b_{k_c} + c_{k_c} = 0 + c_{k_c} = c_{k_c} > 0`, since `k_c < k_b` gives `b_{k_c} = 0`. In every sub-case the first nonzero component of `s` occurs at position `min(k_b, k_c)`, establishing `actionPoint(s) = min(k_b, k_c)`.

*Domain conditions.* The left side `(a ⊕ b) ⊕ c` requires two well-defined additions: `a ⊕ b` requires `k_b ≤ #a` (TA0), and `(a ⊕ b) ⊕ c` requires `k_c ≤ #(a ⊕ b) = #b` (TA0 applied to the intermediate result). The right side `a ⊕ (b ⊕ c)` requires `b ⊕ c` with `k_c ≤ #b` (TA0), and `a ⊕ s` with `actionPoint(s) = min(k_b, k_c) ≤ #a` (TA0). The domains are asymmetric: the left requires `k_b ≤ #a`, the right requires only `min(k_b, k_c) ≤ #a`. But since `k_b ≤ #a` implies `min(k_b, k_c) ≤ #a`, the left-side conditions subsume the right-side conditions. The intersection of both domains is therefore `k_b ≤ #a` and `k_c ≤ #b`. We assume these hold and show the values agree by exhaustive case analysis on the relationship between `k_b` and `k_c`.

*Case 1: `k_b < k_c`.* The action point of `s` is `k_b`, with `s_{k_b} = b_{k_b}` (from the prefix-copy region of `b ⊕ c`, since `k_b < k_c`).

Let `r = a ⊕ b`. By TumblerAdd: `rᵢ = aᵢ` for `i < k_b`, `r_{k_b} = a_{k_b} + b_{k_b}`, and `rᵢ = bᵢ` for `i > k_b`.

*Left side* `(r ⊕ c)` with action point `k_c`: for `i < k_b` we have `i < k_c`, so `(r ⊕ c)ᵢ = rᵢ = aᵢ`. At `i = k_b < k_c`: position `k_b` falls in the prefix-copy region of `r ⊕ c`, so `(r ⊕ c)_{k_b} = r_{k_b} = a_{k_b} + b_{k_b}`. For `k_b < i < k_c`: `(r ⊕ c)ᵢ = rᵢ = bᵢ` (prefix-copy from `r ⊕ c` since `i < k_c`, and tail-copy from `a ⊕ b` since `i > k_b`). At `i = k_c`: `(r ⊕ c)_{k_c} = r_{k_c} + c_{k_c} = b_{k_c} + c_{k_c}`, since `k_c > k_b` gives `r_{k_c} = b_{k_c}` by the tail-copy rule of `a ⊕ b`. For `i > k_c`: `(r ⊕ c)ᵢ = cᵢ`.

*Right side* `(a ⊕ s)` with action point `k_b`: for `i < k_b`, `(a ⊕ s)ᵢ = aᵢ`. At `i = k_b`: `(a ⊕ s)_{k_b} = a_{k_b} + s_{k_b} = a_{k_b} + b_{k_b}`. For `i > k_b`: `(a ⊕ s)ᵢ = sᵢ` by the tail-copy rule. Expanding `sᵢ` via TumblerAdd on `b ⊕ c`: for `k_b < i < k_c`, `sᵢ = bᵢ` (prefix-copy, since `i < k_c`); at `i = k_c`, `s_{k_c} = b_{k_c} + c_{k_c}` (advance); for `i > k_c`, `sᵢ = cᵢ` (tail-copy).

Comparing position by position: `aᵢ = aᵢ` for `i < k_b`; `a_{k_b} + b_{k_b} = a_{k_b} + b_{k_b}` at `k_b`; `bᵢ = bᵢ` for `k_b < i < k_c`; `b_{k_c} + c_{k_c} = b_{k_c} + c_{k_c}` at `k_c`; `cᵢ = cᵢ` for `i > k_c`. Every component agrees.

*Case 2: `k_b = k_c = k`.* The action point of `s` is `k`, with `s_k = b_k + c_k`.

Let `r = a ⊕ b`: `rᵢ = aᵢ` for `i < k`, `r_k = a_k + b_k`, `rᵢ = bᵢ` for `i > k`. The left side `(r ⊕ c)` has action point `k`: for `i < k`, `(r ⊕ c)ᵢ = rᵢ = aᵢ`; at `k`, `(r ⊕ c)_k = r_k + c_k = (a_k + b_k) + c_k`; for `i > k`, `(r ⊕ c)ᵢ = cᵢ`. The right side `(a ⊕ s)` has action point `k`: for `i < k`, `(a ⊕ s)ᵢ = aᵢ`; at `k`, `(a ⊕ s)_k = a_k + s_k = a_k + (b_k + c_k)`; for `i > k`, `(a ⊕ s)ᵢ = sᵢ = cᵢ`.

At position `k`, the left gives `(a_k + b_k) + c_k` and the right gives `a_k + (b_k + c_k)`. These are equal by associativity of addition on ℕ. All other positions agree by direct comparison.

*Case 3: `k_b > k_c`.* The action point of `s` is `k_c`, with `s_{k_c} = b_{k_c} + c_{k_c} = 0 + c_{k_c} = c_{k_c}` (since `k_c < k_b` gives `b_{k_c} = 0`).

Let `r = a ⊕ b`: `rᵢ = aᵢ` for `i < k_b`, `r_{k_b} = a_{k_b} + b_{k_b}`, `rᵢ = bᵢ` for `i > k_b`. The left side `(r ⊕ c)` has action point `k_c`. Since `k_c < k_b`: for `i < k_c` we have `i < k_b`, so `(r ⊕ c)ᵢ = rᵢ = aᵢ` (both prefix-copy rules apply). At `i = k_c < k_b`: `r_{k_c} = a_{k_c}` (position `k_c` falls in the prefix-copy region of `a ⊕ b`), so `(r ⊕ c)_{k_c} = r_{k_c} + c_{k_c} = a_{k_c} + c_{k_c}`. For `i > k_c`: `(r ⊕ c)ᵢ = cᵢ`. The components of `r` at and beyond `k_b` — where `b`'s contribution appears — are entirely overwritten by `c`'s tail, since `k_c < k_b`.

The right side `(a ⊕ s)` has action point `k_c`: for `i < k_c`, `(a ⊕ s)ᵢ = aᵢ`; at `k_c`, `(a ⊕ s)_{k_c} = a_{k_c} + s_{k_c} = a_{k_c} + c_{k_c}`; for `i > k_c`, `(a ⊕ s)ᵢ = sᵢ = cᵢ` (since `sᵢ = cᵢ` for `i > k_c` by the tail-copy rule of `b ⊕ c`).

Comparing: `aᵢ = aᵢ` for `i < k_c`; `a_{k_c} + c_{k_c} = a_{k_c} + c_{k_c}` at `k_c`; `cᵢ = cᵢ` for `i > k_c`. Every component agrees. The displacement `b` is entirely overwritten — TumblerAdd's tail-replacement semantics means the shallower displacement `c` discards everything below its action point on both sides, rendering `b`'s deeper contribution invisible in the final result.

In all three cases, both sides produce the same sequence of length `#c`, so `(a ⊕ b) ⊕ c = a ⊕ (b ⊕ c)` by T3 (CanonicalRepresentation). ∎

*Formal Contract:*
- *Preconditions:* `a ∈ T`, `b ∈ T`, `c ∈ T`, `b > 0`, `c > 0`, `k_b ≤ #a`, `k_c ≤ #b` (where `k_b = actionPoint(b)`, `k_c = actionPoint(c)`; these left-side conditions subsume the right-side conditions since `k_b ≤ #a` implies `min(k_b, k_c) ≤ #a`)
- *Postconditions:* `(a ⊕ b) ⊕ c = a ⊕ (b ⊕ c)`; `#((a ⊕ b) ⊕ c) = #(a ⊕ (b ⊕ c)) = #c`; `actionPoint(b ⊕ c) = min(k_b, k_c)`

**Addition is not commutative.** We do NOT require `a ⊕ b = b ⊕ a`. The operands play asymmetric roles: the first is a *position*, the second is a *displacement*. Swapping them is semantically meaningless. Gregory's `absadd` confirms: the first argument supplies the prefix, the second the suffix — the reverse call gives a different (and typically wrong) result.

**There is no multiplication or division.** Gregory's analysis of the complete codebase confirms: no `tumblermult`, no `tumblerdiv`, no scaling operation of any kind. The arithmetic repertoire is: add, subtract, increment, compare. Tumblers are *addresses*, not quantities. You don't multiply two file paths or divide an address by three.

**Tumbler differences are not counts.** Nelson is emphatic: "A tumbler-span is not a conventional number, and it does not designate the number of bytes contained. It does not designate a number of anything." The difference between two addresses specifies *boundaries*, not *cardinality*. What lies between those boundaries depends on the actual population of the tree, which is dynamic and unpredictable. Between sibling addresses 3 and 7, document 5 might have arbitrarily many descendants — the span from 3 to 7 encompasses all of them, and their count is unknowable from the addresses alone. The arithmetic is an *addressing calculus*, not a *counting calculus*.

The absence of algebraic structure beyond a monotone shift is not a deficiency. It is the *minimum* that addressing requires. An ordered set with an order-preserving shift and an allocation increment is sufficient. Anything more would be unused machinery and unverified obligation.


## Spans

A span is a pair `(s, ℓ)` where `s ∈ T` is a start address and `ℓ ∈ T` is a length (a positive tumbler used as a displacement), denoting the contiguous range from `s` up to but not including `s ⊕ ℓ`. The form of `ℓ` depends on the hierarchical level at which the span operates, because the action point of `ℓ` must match the level of the start address `s`.

Nelson makes spans self-describing at every hierarchical level: "A digit of 'one' may be used to designate all of a given version, all versions of a given document, all works of a given author, all documents in a given project, all documents on a given server — or the entire docuverse." The "1-position convention" exploits T5: because subtrees are contiguous, a span whose start is a high-level prefix and whose length reaches to the next sibling captures exactly that subtree's content.

And a span may be empty — populated by nothing at present — yet valid: "A span that contains nothing today may at a later time contain a million documents." The range is determined by the endpoints; what is actually stored within that range is a question about the current state of the system, not about the tumbler algebra.

**T12 (Span well-definedness).** A span `(s, ℓ)` is well-formed when `ℓ > 0` and the action point `k` of `ℓ` satisfies `k ≤ #s` (the TA0 precondition for `s ⊕ ℓ`). Equivalently, the number of leading zeros in `ℓ` must be strictly less than `#s`. A well-formed span denotes the set `{t ∈ T : s ≤ t < s ⊕ ℓ}`. This set is contiguous under T1 — there is no tumbler between two members that is not itself a member.

*Proof.* We establish three properties of the set `S = {t ∈ T : s ≤ t < s ⊕ ℓ}`, given `s ∈ T`, `ℓ ∈ T`, `ℓ > 0`, and action point `k` of `ℓ` satisfying `k ≤ #s`.

We first record an equivalence stated in the theorem. The action point `k` is the position of the first nonzero component of `ℓ`, so `ℓ` has exactly `k − 1` leading zeros. The condition `k ≤ #s` therefore holds precisely when the number of leading zeros in `ℓ` is strictly less than `#s`; the two formulations express the same arithmetic constraint.

*(a) Endpoint existence.* The preconditions give `ℓ > 0` and `k ≤ #s`. These are exactly the preconditions of TA0 (positive displacement whose action point does not exceed the base length), so TA0 guarantees `s ⊕ ℓ ∈ T`. The set `S` is well-defined — its upper bound exists in `T`.

*(b) Non-emptiness.* We show `s ∈ S` by verifying both defining conditions. First, `s ≤ s` holds by the definition of `≤` from T1: `a ≤ b` iff `a < b ∨ a = b`, and the second disjunct is satisfied. Second, TA-strict — whose preconditions `ℓ > 0` and `k ≤ #s` are given — yields `s ⊕ ℓ > s`, i.e., `s < s ⊕ ℓ`. Both conditions hold, so `s ∈ S`.

*(c) Contiguity.* We show `S` is order-convex: for any `a, c ∈ S` and `b ∈ T` with `a ≤ b ≤ c`, the tumbler `b` belongs to `S`.

The argument requires transitivity of `≤`, which we derive from T1. By T1, `<` is a strict total order on `T`; in particular, T1(c) gives transitivity of `<`. Since `≤` is defined as `x ≤ y` iff `x < y ∨ x = y`, suppose `x ≤ y` and `y ≤ z`. Expanding both disjunctions yields four cases: (i) `x < y` and `y < z` — T1(c) gives `x < z`, hence `x ≤ z`; (ii) `x < y` and `y = z` — substitution gives `x < z`, hence `x ≤ z`; (iii) `x = y` and `y < z` — substitution gives `x < z`, hence `x ≤ z`; (iv) `x = y` and `y = z` — then `x = z`, hence `x ≤ z`. In every case, `x ≤ z`.

Now we verify the two membership conditions for `b`. From `a ∈ S` we have `s ≤ a`. Combined with `a ≤ b`, transitivity of `≤` gives `s ≤ b` — the first defining condition of `S`.

From `c ∈ S` we have `c < s ⊕ ℓ`. Since `b ≤ c`, either `b = c` — in which case `b < s ⊕ ℓ` by substitution — or `b < c`, in which case transitivity of `<` (T1(c)) with `c < s ⊕ ℓ` gives `b < s ⊕ ℓ`. Either way, `b < s ⊕ ℓ` — the second defining condition of `S`.

Both conditions hold, so `b ∈ S`. The set `S` is order-convex: no tumbler lying between two members falls outside it. ∎

We reserve T5 for the distinct claim that *prefix-defined* sets are contiguous — a non-trivial property of the lexicographic order.

*Formal Contract:*
- *Preconditions:* `s ∈ T`, `ℓ ∈ T`, `ℓ > 0`, `actionPoint(ℓ) ≤ #s`
- *Definition:* `span(s, ℓ) = {t ∈ T : s ≤ t < s ⊕ ℓ}`
- *Postconditions:* (a) `s ⊕ ℓ ∈ T` (endpoint exists, by TA0). (b) `s ∈ span(s, ℓ)` (non-empty, by TA-strict). (c) `span(s, ℓ)` is order-convex under T1 (for all `a, c ∈ span(s, ℓ)` and `b ∈ T`, `a ≤ b ≤ c` implies `b ∈ span(s, ℓ)`).


## Order structure: adjacency and interpolation

We have stated the abstract properties. We now ask: what is the order-theoretic structure of T under T1?

T is *not* dense. Every tumbler `t` and its zero-extension `t.0` form an adjacent pair: `t < t.0` by the prefix rule (T1 case ii), and no tumbler lies strictly between them. For suppose `t < x < t.0`. Since `t` is a prefix of `t.0`, T5 requires that `x` also extend prefix `t` — so `x = t.x₁. ... .xₖ` for some `k ≥ 1`. The smallest such extension is `t.0` (since `x₁ ≥ 0` and if `x₁ = 0` then `x ≥ t.0`), giving `x ≥ t.0`, a contradiction. Every tumbler has an immediate successor: its zero-extension. The ordering resembles a tree's depth-first traversal order, which has adjacent pairs at every branch point.

What T0 does provide is *interpolation between non-prefix-related tumblers*. Between any two tumblers that differ at a shared position — that is, neither is a prefix of the other — there exist arbitrarily many intermediate tumblers. Between `1.3` and `1.5`, we can place `1.4`, `1.3.1`, `1.3.2`, and so on — T0 guarantees we never exhaust the space of intermediate values. This is the property that makes allocation work: within a single hierarchical level, there is always room for the next sibling.

Nelson describes the whole system as designed for this inexhaustibility: "the docuverse is ... finite but unlimited." At any moment the tree has finitely many nodes. But it can always grow. The address space between any two non-adjacent addresses can absorb unlimited new content.

Gregory's implementation further restricts the representable values to a fixed 16-digit mantissa of 32-bit unsigned integers, introducing additional adjacencies beyond those inherent in the abstract order. At the maximum mantissa depth (16 components), tumblers differing by 1 in their last component are adjacent even in the abstract order. But the implementation also makes tumblers adjacent when they would have required a 17th component to interpolate between — the `strongsub` exponent guard and the `tumblerincrement` overflow check are the two points where this limitation surfaces explicitly. A correct implementation must demonstrate that allocation never drives the system into a region where this additional adjacency matters.


## Worked example

We instantiate the algebra on a concrete scenario. Server 1, user 3, document 2, text subspace. The document contains five characters at element addresses:

  `a₁ = 1.0.3.0.2.0.1.1`, `a₂ = 1.0.3.0.2.0.1.2`, `a₃ = 1.0.3.0.2.0.1.3`, `a₄ = 1.0.3.0.2.0.1.4`, `a₅ = 1.0.3.0.2.0.1.5`

**T4 (Hierarchical parsing).** Take `a₃ = 1.0.3.0.2.0.1.3`. The three zeros at positions 2, 4, 6 are the field separators. Node field: `[1]`. User field: `[3]`. Document field: `[2]`. Element field: `[1, 3]`. The first component of the element field is `1`, placing this address in the text subspace. Every non-separator component is strictly positive, confirming T4.

**T1 (Ordering).** We verify `a₁ < a₂ < a₃ < a₄ < a₅`. All five share the prefix `1.0.3.0.2.0.1` and diverge at position 8, where the values are `1, 2, 3, 4, 5` respectively. Lexicographic comparison at the divergence point confirms the order.

**T5 (Contiguous subtrees).** The prefix `p = 1.0.3.0.2` identifies all content in document 2. Any tumbler `b` with `a₁ ≤ b ≤ a₅` must share this prefix. If `b` diverged from `p` at some position `k ≤ 5`, then `bₖ ≠ pₖ`, but `a₁` and `a₅` agree with `p` at position `k`, so `bₖ < pₖ` would violate `a₁ ≤ b` and `bₖ > pₖ` would violate `b ≤ a₅`. So `b` extends prefix `p` — it belongs to document 2.

**T6 (Decidable containment).** Do `a₃` and `a₅` belong to the same account? Extract user fields: both `[3]` under node `[1]`. Yes. Are they in the same document? Document fields: both `[2]`. Yes. Is `a₃` in the same document family as an address in document `2.1` (a version)? The document field `[2]` is a prefix of `[2, 1]`, so T6(d) confirms structural subordination.

**T7 (Subspace disjointness).** The document also contains a link at `ℓ₁ = 1.0.3.0.2.0.2.1`. Element field: `[2, 1]` — first component is `2`, placing this in the link subspace. By T7, `ℓ₁ ≠ aᵢ` for all `i` — the subspace identifiers differ.

**T9 (Forward allocation).** The five text addresses were allocated by a single allocator (user 3's element allocator within document 2, text subspace). Each address exceeds its predecessor: `a₁ < a₂ < a₃ < a₄ < a₅`. No gap-filling occurred.

**TA5 (Increment).** Allocating the sixth character: `inc(a₅, 0)`. Position `sig(a₅) = 8` (the last nonzero component). TA5(c): `a₆ = 1.0.3.0.2.0.1.6`. This preserves `#a₆ = #a₅ = 8` and differs only at position 8: `6 = 5 + 1`. By TA5(a), `a₆ > a₅`.

**T12 (Span computation).** The addresses `a₂` through `a₄` form a natural span — three consecutive elements. We construct `(s, ℓ)` with `s = a₂ = 1.0.3.0.2.0.1.2`. An element-level displacement must have action point `k = 8`: `ℓ = [0, 0, 0, 0, 0, 0, 0, 3]`. By the constructive definition of `⊕`: positions 1–7 copy from `s` (giving `1.0.3.0.2.0.1`), position 8 advances: `2 + 3 = 5`. So `s ⊕ ℓ = 1.0.3.0.2.0.1.5 = a₅`. The span denotes the range `{t ∈ T : a₂ ≤ t < a₅}`. This range is infinite — between any two consecutive allocated addresses lie arbitrarily many unallocated tumblers (e.g., `a₂.0`, `a₂.1`, etc.). Among the five allocated addresses, the span covers `{a₂, a₃, a₄}`. A single-component length `[3]` would give the wrong result: action point `k = 1`, and `a₂ ⊕ [3] = [4]` — a node-level address. The action point of the span length must match the hierarchical level of the start address.

**TA7a (Subspace closure).** Consider advancing text position ordinal `[3]` by displacement `[2]`: `[3] ⊕ [2] = [5]`. The result is a single-component ordinal — it remains within the text subspace. The subspace identifier `1` is held as context, unchanged. Subtracting: `[5] ⊖ [2] = [3]`. Recovery is exact (TA4 applies: `k = 1 = #a = #w`, zero-prefix condition vacuously satisfied).

**TA1 (Order preservation under addition).** We have `a₂ < a₃` (divergence at position 8: `2 < 3`). Apply displacement `ℓ = [0,0,0,0,0,0,0,3]` (action point `k = 8`). Compute: `a₂ ⊕ ℓ`: positions 1–7 copy from `a₂` giving `1.0.3.0.2.0.1`, position 8 advances `2 + 3 = 5`. Result: `1.0.3.0.2.0.1.5`. `a₃ ⊕ ℓ`: positions 1–7 copy from `a₃` giving `1.0.3.0.2.0.1`, position 8 advances `3 + 3 = 6`. Result: `1.0.3.0.2.0.1.6`. Comparing: `1.0.3.0.2.0.1.5 < 1.0.3.0.2.0.1.6` — divergence at position 8, `5 < 6`. TA1 (weak) is confirmed. Since `k = 8 = divergence(a₂, a₃)`, TA1-strict predicts strict inequality — and we see `a₂ ⊕ ℓ < a₃ ⊕ ℓ` strictly, as claimed.

**TA4 (Partial inverse — full addresses).** Does the round-trip `(a₂ ⊕ ℓ) ⊖ ℓ = a₂` hold? We have `a₂ ⊕ ℓ = [1,0,3,0,2,0,1,5]`. Subtracting `ℓ = [0,0,0,0,0,0,0,3]`: scan for divergence — position 1: `1 ≠ 0`. Divergence at `d = 1`. Result: position 1 gets `1 - 0 = 1`, positions 2–8 copy from minuend: `0,3,0,2,0,1,5`. So `(a₂ ⊕ ℓ) ⊖ ℓ = [1,0,3,0,2,0,1,5] = a₂ ⊕ ℓ ≠ a₂`. The subtraction is a no-op — it finds the divergence at the node field (position 1), not at the action point. The round-trip fails. Checking TA4's preconditions: `k = 8`, `#a₂ = 8`, so `k = #a₂` ✓. `#ℓ = 8 = k` ✓. But `(A i : 1 ≤ i < 8 : (a₂)ᵢ = 0)`? Position 1 has `(a₂)₁ = 1 ≠ 0` ✗. The zero-prefix condition fails — `a₂` has nonzero components before the action point, so TA4's preconditions are not met and the theorem makes no claim. Contrast with the ordinal-only case above: `[5] ⊖ [2] = [3]`, `[3] ⊕ [2] = [5]`. Here `k = 1 = #[3] = #[2]` and the zero-prefix condition is vacuous. All preconditions hold and round-trip succeeds. The restrictive preconditions exist precisely to exclude cases like the full-address round-trip where the subtraction algorithm's divergence-discovery mechanism is misled by nonzero prefix components.


## Formal summary

We collect the structure. The tumbler algebra is a tuple `(T, <, ⊕, ⊖, inc, fields, Z)` where `Z = {t ∈ T : (A i : 1 ≤ i ≤ #t : tᵢ = 0)}` is the set of zero tumblers:

- `T` is the carrier set of finite sequences of non-negative integers, with unbounded component values (T0(a)) and unbounded length (T0(b))
- `<` is the lexicographic total order on `T` (T1), intrinsically computable (T2), with canonical representation (T3)
- The hierarchical parsing function `fields` extracts four-level containment (T4), yielding contiguous subtrees (T5); decidable containment (T6, corollary of T4) and element subspace disjointness (T7, corollary of T3, T4) follow
- `T8` establishes allocation permanence — once allocated, an address is never removed from the set of allocated addresses
- `T9–T10` establish forward allocation and partition independence; `T10a` constrains each allocator to use `inc(·, 0)` for sibling outputs, reserving `k > 0` exclusively for child-spawning
- `⊕` and `⊖` are order-preserving operations on T (TA0–TA3, with TA0 requiring `k ≤ #a`), with weak order preservation universally (TA1 `≤`, TA3 `≤`) and strict preservation under tighter conditions (TA1-strict when `k ≤ min(#a, #b) ∧ k ≥ divergence(a,b)`, TA3-strict when `#a = #b`); strict increase (TA-strict); partially inverse when `k = #a`, `#w = k`, and all components of `a` before `k` are zero (TA4)
- `inc` is hierarchical increment for allocation (TA5)
- Zero tumblers (all components zero, any length) are sentinels, not valid addresses (TA6); positivity is defined as having at least one nonzero component
- `TA7a` confines element-local shifts to their subspace (algebraic closure)
- Spans are self-describing contiguous ranges (T12)
- D0–D2 characterize displacement recovery: D0 is the well-definedness precondition, D1 is the round-trip identity a ⊕ (b ⊖ a) = b, D2 is uniqueness (corollary of D1, TA-LC)
- OrdinalDisplacement and OrdinalShift define the shift apparatus — ordinal displacement δ(n, m) and shift(v, n) = v ⊕ δ(n, #v); TS1–TS5 establish that shift preserves order (TS1), is injective (TS2), composes additively (TS3), strictly increases (TS4), and is monotone in amount (TS5)

Each property is required by at least one system guarantee:

| Property | Required by |
|----------|-------------|
| T0(a), T0(b) | Unbounded growth of docuverse |
| T1, T2 | Span containment, link search, index traversal |
| T3 | Address identity, uniqueness, total order consistency |
| T4, T5 | Hierarchical queries, self-describing spans |
| T6 *(corollary of T4)* | Decidable containment |
| T7 *(corollary of T3, T4)* | Subspace isolation |
| T8 | Link stability, transclusion identity, attribution |
| T9 | Per-allocator monotonicity; partition monotonicity derived from T9 + T10 + T1 |
| T10, T10a | Decentralized allocation, global uniqueness |
| T12 | Content reference by span |
| TA0–TA4, TA-strict | Span computation, position advancement, span non-emptiness (T12) |
| TA5 | Address allocation |
| TA6 | Sentinel and lower bound |
| TA7a | Subspace isolation (algebraic closure) |
| TA-LC, TA-RC, TA-MTO *(lemmas)* | Cancellation characterization of ⊕; TA-MTO equivalence classes constrain span-endpoint recovery |
| D0 | Displacement recovery precondition |
| D1 | Displacement round-trip: span-endpoint recovery from start + displacement |
| D2 *(corollary of D1, TA-LC)* | Displacement uniqueness |
| OrdinalDisplacement, OrdinalShift | Element-level position advancement (Istream allocation, V-enfilade traversal) |
| TS1–TS5 *(lemmas/corollaries)* | Order-safe shifting: TS1 order preservation for sorted-sequence maintenance, TS2 injectivity for address uniqueness under shift, TS3 composition for multi-step allocation, TS4–TS5 monotonicity for forward progress |

Removing any independent property breaks a system-level guarantee. T6 and T7 are derived (corollaries of T4, T3 respectively) and are stated for emphasis, not as independent axioms. TA-LC, TA-RC, and TA-MTO are structural lemmas derived from TumblerAdd's constructive definition and T3 — they characterize cancellation asymmetry and the many-to-one equivalence classes of `⊕`, but introduce no independent content beyond the definition.


## Properties Introduced

| Label | Statement | Status |
|-------|-----------|--------|
| T0 | Carrier-set definition: T is the set of all finite sequences over ℕ with length ≥ 1 | axiom |
| T0(a) | Every component value of a tumbler is unbounded — no maximum value exists | introduced |
| T0(b) | Tumblers of arbitrary length exist in T — the hierarchy has unlimited nesting depth | introduced |
| T1 | Tumblers are totally ordered by lexicographic comparison, with the prefix-less-than convention | introduced |
| T2 | Tumbler comparison is computable from the two addresses alone, examining at most min(#a, #b) components | introduced |
| T3 | Each tumbler has exactly one canonical representation; component-wise identity is both necessary and sufficient for equality | from T0(a) |
| T4 | An address tumbler has at most three zero-valued components as field separators, every field component is strictly positive, and every present field has at least one component (no adjacent zeros, no leading/trailing zero) | introduced |
| T5 | The set of tumblers sharing a prefix forms a contiguous interval under T1 | introduced |
| T6 | Containment (same node, same account, same document family, structural subordination) is decidable from addresses alone | corollary of T4 |
| T7 | Subspaces (text, links) within a document's element field are permanently disjoint | corollary of T3, T4 |
| T8 | Once allocated, an address is never removed from the address space; the set of allocated addresses is monotonically non-decreasing | introduced |
| T9 | Within a single allocator's sequential stream, new addresses are strictly monotonically increasing; gaps are permanent | lemma (from T10a, TA5) |
| T10 | Allocators with non-nesting prefixes produce distinct addresses without coordination | introduced |
| T10a | Each allocator uses inc(·, 0) for siblings and inc(·, k>0) only for child-spawning; this constrains sibling outputs to uniform length | introduced |
| PrefixOrderingExtension | p₁ < p₂ with neither a prefix of the other implies a < b for every a with p₁ ≼ a and every b with p₂ ≼ b | lemma (from T1) |
| PartitionMonotonicity | Per-allocator ordering extends cross-allocator; for non-nesting sibling prefixes p₁ < p₂, every address extending p₁ precedes every address extending p₂ | theorem from PrefixOrderingExtension, T1, T3, T5, T9, T10a, TA5 |
| GlobalUniqueness | No two distinct allocation events anywhere in the system at any time produce the same address | theorem from T3, T4, T9, T10, T10a, TA5 |
| T12 | A span (s, ℓ) is well-formed when ℓ > 0 and action point k of ℓ satisfies k ≤ #s; it denotes the contiguous interval {t : s ≤ t < s ⊕ ℓ}, non-empty by TA-strict | from T1, TA0, TA-strict |
| TA0 | Tumbler addition a ⊕ w is well-defined when w > 0 and the action point k satisfies k ≤ #a | introduced |
| TA1 | Addition preserves the total order (weak): a < b ⟹ a ⊕ w ≤ b ⊕ w | introduced |
| Divergence | Divergence point of two unequal tumblers: first position k where aₖ ≠ bₖ (component), or min(#a, #b) + 1 (prefix) | from T1 |
| TA1-strict | Addition preserves the total order (strict) when k ≤ min(#a, #b) ∧ k ≥ divergence(a, b) | from Divergence, TumblerAdd |
| TA-strict | Adding a positive displacement strictly advances: a ⊕ w > a | from TumblerAdd, T1 |
| TA2 | Tumbler subtraction a ⊖ w is well-defined when a ≥ w | from TumblerSub, T1 |
| TA3 | Subtraction preserves the total order (weak): a < b ⟹ a ⊖ w ≤ b ⊖ w when both are defined | from TA2, T1, TA6, TumblerSub |
| TA3-strict | Subtraction preserves the total order (strict) when additionally #a = #b | introduced |
| TA4 | Addition and subtraction are partial inverses: (a ⊕ w) ⊖ w = a when k = #a, #w = k, and all components of a before k are zero | from TumblerAdd, TumblerSub |
| ReverseInverse | (a ⊖ w) ⊕ w = a when k = #a, #w = k, a ≥ w > 0, and all components of a before k are zero | corollary of TA3-strict, TA4, TumblerAdd, TumblerSub |
| TumblerAdd | a ⊕ w: copy aᵢ for i < k, advance aₖ by wₖ at action point k, replace tail with wᵢ for i > k; result length = #w | introduced |
| TumblerSub | a ⊖ w: zero positions before divergence k, compute aₖ − wₖ at divergence point, copy aᵢ for i > k; result length = max(#a, #w) | from Divergence, T1 |
| TA5 | Hierarchical increment inc(t, k) produces t' > t: k=0 advances at sig(t), k>0 extends by k positions with separators and first child | introduced |
| TA6 | Every all-zero tumbler (any length) is less than every positive tumbler and is not a valid address | from T1, T4 |
| PositiveTumbler | t > 0 iff at least one component is nonzero; zero tumbler iff all components are zero | introduced |
| TA7a | Ordinal-only shift arithmetic: both ⊕ and ⊖ on ordinals produce results in T with the subspace identifier (held as context) unchanged | introduced |
| TA-assoc | Addition is associative where both compositions are defined: (a ⊕ b) ⊕ c = a ⊕ (b ⊕ c) | theorem from TumblerAdd, T3 |
| TA-LC | a ⊕ x = a ⊕ y ⟹ x = y (left cancellation) | lemma (from TumblerAdd, T3) |
| TA-RC | Right cancellation fails: ∃ a ≠ b with a ⊕ w = b ⊕ w | lemma (from TumblerAdd, T3) |
| TA-MTO | a agrees with b on components 1..k ⟺ a ⊕ w = b ⊕ w for displacement w with action point k | lemma (from TumblerAdd, T3) |
| D0 | Displacement well-definedness: a < b and divergence(a, b) ≤ #a ensures positive displacement with TA0 satisfied | from T3, TA0, TumblerAdd, TumblerSub |
| D1 | Displacement round-trip: for a < b with divergence(a, b) ≤ #a and #a ≤ #b, a ⊕ (b ⊖ a) = b | lemma (from TumblerAdd, TumblerSub, T3, Divergence) |
| D2 | Displacement uniqueness: under D1's preconditions, if a ⊕ w = b then w = b ⊖ a | corollary of D1, TA-LC |
| OrdinalDisplacement | δ(n, m) = [0, ..., 0, n] of length m, action point m | introduced |
| OrdinalShift | shift(v, n) = v ⊕ δ(n, #v) | introduced |
| TS1 | shift preserves strict order: v₁ < v₂ ⟹ shift(v₁, n) < shift(v₂, n) | lemma (from TA1-strict) |
| TS2 | shift is injective: shift(v₁, n) = shift(v₂, n) ⟹ v₁ = v₂ | lemma (from TA-MTO, T3) |
| TS3 | shift composes additively: shift(shift(v, n₁), n₂) = shift(v, n₁ + n₂) | lemma (from TumblerAdd, T3) |
| TS4 | shift strictly increases: shift(v, n) > v | corollary of TA-strict |
| TS5 | shift is monotone in amount: n₁ < n₂ ⟹ shift(v, n₁) < shift(v, n₂) | corollary of TS3, TS4 |


## Open Questions

What constraints must an implementation's representable range satisfy to ensure that no reachable allocation state exceeds the representation — can these constraints be stated as a finite-model property of the abstract algebra?

Must allocation counter durability across crashes be a global-history property or only a per-session property, and what recovery mechanism restores monotonicity after a crash that loses the counter state?

What minimal auxiliary structure must the system maintain to reconstruct version-derivation history, given that it is not decidable from addresses alone (T6(d))?

What must the system guarantee about the zero tumbler's interaction with span arithmetic — if a span endpoint is the zero sentinel, how must containment and intersection operations behave?

Does left cancellation extend to a ⊕ x ≤ a ⊕ y ⟹ x ≤ y (left cancellation for the order)? This would strengthen TA1-strict.

The equivalence-class characterization (TA-MTO converse) suggests that TumblerAdd at action point k is a projection that discards information below level k. Does this projection have useful algebraic properties (idempotence, composition)?

