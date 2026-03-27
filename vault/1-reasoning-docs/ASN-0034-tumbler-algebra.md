# ASN-0034: Tumbler Algebra

*2026-03-13, revised 2026-03-19, 2026-03-21, 2026-03-25, 2026-03-26, 2026-03-26, 2026-03-26*

We wish to understand what algebraic structure the Xanadu addressing system must possess. The system assigns every entity a permanent address — a *tumbler* — and requires these addresses to support comparison, containment testing, arithmetic for span computation and position advancement, and coordination-free allocation across a global network. We seek the minimal set of abstract properties that any correct implementation must provide, deriving each from design requirements rather than from any particular representation.

The approach is: state what the system must guarantee, then discover what properties of the address algebra are necessary and sufficient for those guarantees. We begin with the carrier set and work outward.

Nelson conceived this system as "the tumbler line" — a flat linearization of a hierarchical tree, yielding a total order on all addresses. Gregory implemented it as fixed-width sign-magnitude arithmetic over 16-digit mantissas. Between these two accounts we find the abstract algebra: what must hold for any correct implementation, regardless of representation.


## The carrier set

A tumbler is a finite sequence of non-negative integers. We write `t = d₁.d₂. ... .dₙ` where each `dᵢ ∈ ℕ` and `n ≥ 1`. The set of all tumblers is **T**. Nelson describes each component as a "digit" with "no upper limit" — the term is misleading, since each "digit" is an arbitrary-precision natural number, not a single decimal digit. The variable-length encoding ("humber") ensures small values are compact and large values expand as needed.

This gives us our first property:

**T0(a) (Unbounded component values).** `(A t ∈ T, i : 1 ≤ i ≤ #t : (A M ∈ ℕ :: (E t' ∈ T :: t' agrees with t except t'.dᵢ > M)))`.

In words: for every tumbler and every component position, there exists a tumbler whose value at that position exceeds any given bound. The address space within any subtree is inexhaustible.

**T0(b) (Unbounded length).** `(A n ∈ ℕ : n ≥ 1 : (E t ∈ T :: #t ≥ n))`.

In words: there is no maximum tumbler length — for every bound, a tumbler of at least that length exists in T. The hierarchy has unlimited nesting depth. T0(b) follows from T's definition as the set of all finite sequences over ℕ — for any `n`, the constant sequence `[1, 1, ..., 1]` of length `n` is a member. We state it explicitly because it carries independent architectural weight: T0(a) ensures siblings within a level are inexhaustible, while T0(b) ensures levels themselves are inexhaustible.

T0 is what separates the tumbler design from fixed-width addressing. Nelson: "New items may be continually inserted in tumbler-space while the other addresses remain valid." The word "continually" carries the weight — it means the process of creating new addresses never terminates. Between any two sibling addresses, the forking mechanism can always create children: "One digit can become several by a forking or branching process. This consists of creating successive new digits to the right." Each daughter can have daughters without limit, and each digit is itself unbounded.

The address space is unbounded in two dimensions: T0(a) ensures each component is unbounded (unlimited siblings at any level) and T0(b) ensures the number of components is unbounded (unlimited nesting depth). Together they make the address space infinite in both dimensions, which Nelson calls "finite but unlimited" — at any moment finitely many addresses exist, but there is no bound on how many can be created: "A span that contains nothing today may at a later time contain a million documents."

We observe that Gregory's implementation uses a fixed 16-digit mantissa of 32-bit unsigned integers, giving a large but finite representable range. When the allocation primitive `tumblerincrement` would exceed this range structurally (requiring a 17th digit), it detects the overflow and terminates fatally. The general addition routine `tumbleradd` silently wraps on digit-value overflow. Both behaviors violate T0. The abstract specification demands unbounded components; a correct implementation must either provide them or demonstrate that the reachable state space never exercises the bound. The comment `NPLACES 16 /* increased from 11 to support deeper version chains */` records that the original bound of 11 was concretely hit in practice — version chains deeper than 3–4 levels caused fatal crashes.


## The total order

We require a total order on T. Nelson describes the "tumbler line" as a single linear sequence: "In a sense the tumbler line is like the real line, i.e., the line of integers and all the numbers in between." The system maps a hierarchical tree — servers containing accounts containing documents containing elements — onto this flat line via depth-first traversal. The traversal inherently produces a total order: for any two nodes in a tree, depth-first traversal visits one before the other. The ordering rule is lexicographic:

**T1 (Lexicographic order).** For tumblers `a = a₁. ... .aₘ` and `b = b₁. ... .bₙ`, define `a < b` iff there exists `k ≥ 1` such that `(A i : 1 ≤ i < k : aᵢ = bᵢ)` and either:

  (i) `k ≤ min(m, n)` and `aₖ < bₖ`, or

  (ii) `k = m + 1 ≤ n` (that is, `a` is a proper prefix of `b`).

The prefix convention — a prefix is less than any proper extension — is what makes depth-first traversal work. The server address `2` is less than every address within server `2`'s subtree, because every such address extends the prefix `2` with further components. This means server `2`'s subtree begins immediately after `2` in the order and extends until some address whose first component exceeds `2`.

*Proof.* We show that `<` as defined above is a strict total order on T by establishing irreflexivity, trichotomy, and transitivity.

*(a) Irreflexivity.* For any `a ∈ T`, we show `¬(a < a)`. Suppose `a < a`. Then there exists `k ≥ 1` with `aᵢ = aᵢ` for all `i < k` and either (i) `aₖ < aₖ`, contradicting irreflexivity of `<` on ℕ, or (ii) `k = #a + 1 ≤ #a`, which is impossible. No such `k` exists.

*(b) Trichotomy.* For any `a, b ∈ T`, exactly one of `a < b`, `a = b`, `a > b` holds. Let `k` be the smallest positive integer at which `a` and `b` first disagree — either because `aₖ ≠ bₖ` at some `k ≤ min(#a, #b)`, or because one tumbler is exhausted at `k = min(#a, #b) + 1` while the other continues.

If no such `k` exists — `#a = #b` and `aᵢ = bᵢ` for all `1 ≤ i ≤ #a` — then `a = b` by T3, and neither `a < b` nor `a > b` by part (a).

If `k ≤ min(#a, #b)` and `aₖ ≠ bₖ`, then by trichotomy on ℕ exactly one of `aₖ < bₖ` or `bₖ < aₖ` holds. The first gives `a < b` via T1 case (i) with witness `k`; the second gives `b < a` via T1 case (i) with witness `k`.

If `k = min(#a, #b) + 1` — all shared positions agree but `#a ≠ #b` — then: if `#a < #b`, we have `k = #a + 1 ≤ #b`, so `a` is a proper prefix of `b`, giving `a < b` via T1 case (ii); if `#a > #b`, we have `k = #b + 1 ≤ #a`, so `b` is a proper prefix of `a`, giving `b < a` via T1 case (ii).

These cases are exhaustive and mutually exclusive. In each, the first divergence position determines a unique outcome, and no alternative witness can override it — any valid witness `k'` for the reverse relation would satisfy `k' ≥ k`, and at position `k` the comparison is already determined.

*(c) Transitivity.* For `a, b, c ∈ T` with `a < b` and `b < c`, we show `a < c`. Let `k₁` be the divergence position witnessing `a < b` and `k₂` the divergence position witnessing `b < c`. For all `i < min(k₁, k₂)`, we have `aᵢ = bᵢ` (from `a < b`, since `i < k₁`) and `bᵢ = cᵢ` (from `b < c`, since `i < k₂`), so `aᵢ = cᵢ`. Three cases arise.

*Case k₁ < k₂.* Position `k₁` falls in the agreement range of `b < c`, so `bₖ₁ = cₖ₁`. If `a < b` via case (i): `aₖ₁ < bₖ₁ = cₖ₁`, and since `k₁ ≤ #a` and `k₁ ≤ #c` (the latter because `cₖ₁` exists), position `k₁` witnesses `a < c` via T1 case (i). If `a < b` via case (ii): `k₁ = #a + 1 ≤ #b`, and since `bₖ₁ = cₖ₁` implies `#c ≥ k₁ = #a + 1`, `a` is a proper prefix of `c`, so `k₁` witnesses `a < c` via T1 case (ii).

*Case k₂ < k₁.* Position `k₂` falls in the agreement range of `a < b`, so `aₖ₂ = bₖ₂`. We observe that `b < c` via case (ii) would give `k₂ = #b + 1`, but `a < b` requires `k₁ ≤ #b` (in case (i), `k₁ ≤ min(#a, #b) ≤ #b`; in case (ii), `k₁ = #a + 1 ≤ #b`), so `k₂ = #b + 1 > #b ≥ k₁`, contradicting `k₂ < k₁`. Therefore `b < c` is via case (i): `bₖ₂ < cₖ₂` with `k₂ ≤ min(#b, #c)`. Since `k₂ < k₁` and `a` has a component at every position below `k₁`, we have `k₂ ≤ #a`, giving `aₖ₂ = bₖ₂ < cₖ₂` with `k₂ ≤ min(#a, #c)`. Position `k₂` witnesses `a < c` via T1 case (i).

*Case k₁ = k₂ = k.* Both divergences occur at the same position. We have `aᵢ = cᵢ` for all `i < k`. Three sub-cases arise from the two-case structure of T1.

*Sub-case (i, i):* `aₖ < bₖ` and `bₖ < cₖ`, both with `k ≤ min(#a, #b)` and `k ≤ min(#b, #c)`. By transitivity of `<` on ℕ, `aₖ < cₖ`, and `k ≤ min(#a, #c)`. Position `k` witnesses `a < c` via T1 case (i).

*Sub-case (ii, i):* `k = #a + 1 ≤ #b` and `bₖ < cₖ` with `k ≤ min(#b, #c)`. Since `k ≤ #c`, we have `#a + 1 = k ≤ #c`, so `a` is a proper prefix of `c`. Position `k` witnesses `a < c` via T1 case (ii).

*Sub-case (i, ii):* `aₖ < bₖ` with `k ≤ min(#a, #b)` and `k = #b + 1 ≤ #c`. But case (i) requires `k ≤ #b` while case (ii) gives `k = #b + 1`, a contradiction. This sub-case cannot arise.

(The remaining combination — both via case (ii) — requires `k = #a + 1 ≤ #b` and `k = #b + 1 ≤ #c`, giving `#a + 1 = #b + 1`, hence `#a = #b`. But case (ii) for `a < b` requires `#a + 1 ≤ #b`, i.e., `#a < #b`. Contradiction. This sub-case also cannot arise.)

In every realizable case, a witness for `a < c` under T1 is produced. ∎

*Formal Contract:*
- *Definition:* `a < b` iff `∃ k ≥ 1` with `(A i : 1 ≤ i < k : aᵢ = bᵢ)` and either (i) `k ≤ min(m,n) ∧ aₖ < bₖ`, or (ii) `k = m+1 ≤ n`.
- *Postconditions:* (a) Trichotomy — `(A a,b ∈ T :: exactly one of a < b, a = b, a > b)`. (b) Transitivity — `(A a,b,c ∈ T : a < b ∧ b < c : a < c)`. (c) Irreflexivity — `(A a ∈ T :: ¬(a < a))`.

Nelson's assertion that the tumbler line is total — that two addresses are never incomparable — is architecturally load-bearing. Spans are defined as contiguous regions on the tumbler line: "A span in the tumbler line, represented by two tumblers, refers to a subtree of the entire docuverse." If two addresses were incomparable, the interval between them would be undefined, and the entire machinery of span-sets, link endsets, and content reference would collapse.

Nelson requires that comparison be self-contained — no index consultation needed:

**T2 (Intrinsic comparison).** The order relation T1 is computable from the two tumblers alone, without consulting any external data structure. The comparison examines at most `min(#a, #b)` component pairs.

*Proof.* The definition of T1 determines `a < b` by scanning component pairs `(aᵢ, bᵢ)` at successive positions `i = 1, 2, ...` until either (i) a divergence `aₖ ≠ bₖ` is found at some `k ≤ min(m, n)`, or (ii) all `min(m, n)` positions are exhausted without divergence, in which case the shorter tumbler is a proper prefix of the longer. In case (i), exactly `k ≤ min(m, n)` component pairs are examined. In case (ii), exactly `min(m, n)` component pairs are examined, and the result is then determined by comparing the lengths `m` and `n`. In both cases, at most `min(m, n)` component pairs are compared, and the only values consulted are the components `aᵢ`, `bᵢ` and the lengths `m`, `n` — all intrinsic to the two tumblers. No external data structure participates in the decision. ∎

The importance of T2 is operational: span containment tests, link search, and index traversal all reduce to tumbler comparison. If comparison required a lookup, these operations would depend on auxiliary state, and the system's decentralization guarantee would collapse — one could not determine whether an address falls within a span without access to the index that manages that span.

Gregory's implementation confirms T2. The comparison function `tumblercmp` delegates to `abscmp`, which performs a purely positional comparison: exponent first (a proxy for the number of leading zeros), then lexicographic mantissa slot-by-slot. No tree structure, no index, no external state is consulted.


## Canonical form

Equality of tumblers must mean component-wise identity. There must be no representation in which two distinct sequences of components denote the same abstract tumbler:

**T3 (Canonical representation).** `(A a, b ∈ T : a₁ = b₁ ∧ ... ∧ aₙ = bₙ ∧ #a = #b ≡ a = b)`.

If two tumblers have the same length and the same components at every position, they are the same tumbler. Conversely, if they differ in any component or in length, they are distinct. No normalization, no trailing-zero ambiguity, no exponent variation can create aliases.

Gregory's implementation achieves T3 through a normalization routine (`tumblerjustify`) that shifts leading zeros out of the mantissa and adjusts the exponent. After justification, the first mantissa element is nonzero (unless the tumbler is the zero tumbler), creating a unique representation for each value. A validation routine enforces the invariant — one branch labels the failure `"fucked up non-normalized"`; the frustration testifies to the difficulty.

Gregory's analysis reveals precisely what happens when T3 is violated. The comparison function begins with zero-detection: `iszerotumbler` checks only the first mantissa slot. An unnormalized tumbler with a leading zero and a nonzero digit buried at a later position is *misclassified as zero* — it never reaches the magnitude comparison logic. Two such tumblers representing different positive values compare as EQUAL to each other and to the genuine zero tumbler, producing ordering contradictions. Suppose `T₁` has `mantissa = [0, 0, 5, ...]` (logically positive) and `T₂` has `mantissa = [0, 7, ...]` (logically positive with different value). Both are misclassified as zero: `tumblercmp(T₁, T₂) = EQUAL` and `tumblercmp(T₁, 0) = EQUAL`, yet after normalization `T₁ ≠ T₂`. Transitivity of the total order is broken. T3 — maintained by normalization after every arithmetic operation — prevents this corruption.

T3 matters because address identity is load-bearing. If two representations could denote the same tumbler, equality tests might give false negatives, span containment checks might fail for addresses that should match, and the system might allocate a "new" address that is actually an alias for an existing one.

*Justification.* T3 is not derived from other properties; it holds by the definition of the carrier set. T is defined as the set of all finite sequences over ℕ. A tumbler *is* its component sequence — there is no separate abstract value that a sequence "represents," no quotient by an equivalence relation, no normalization map whose image is the "true" tumbler. The biconditional has two directions.

*Forward direction.* Suppose `#a = #b = n` and `aᵢ = bᵢ` for all `1 ≤ i ≤ n`. Then `a` and `b` are finite sequences of the same length with identical entries at every position. By the extensional definition of sequence equality, `a = b`.

*Reverse direction.* Suppose `a = b`. By Leibniz's law, every property of `a` is a property of `b`. In particular, `#a = #b` (they have the same length) and for each `i` with `1 ≤ i ≤ #a`, `aᵢ = bᵢ` (they have the same component at every position).

Both directions are immediate from what it means for two finite sequences to be equal. The force of T3 as a design commitment is the decision that no additional identification is imposed on T — the algebra does not quotient by trailing zeros (so `[1, 2]` and `[1, 2, 0]` are distinct tumblers), does not identify sequences that differ only in exponent representation (an implementation concern, not an abstract one), and does not collapse addresses that happen to denote the same logical entity under some external interpretation. The abstract tumbler *is* the sequence, nothing more and nothing less. ∎

*Formal Contract:*
- *Axiom:* Tumbler equality is sequence equality: `a = b ⟺ #a = #b ∧ (A i : 1 ≤ i ≤ #a : aᵢ = bᵢ)`. No quotient, normalization, or external identification is imposed on T.


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

**Verification of T4.** We verify three consequences of the T4 constraints.

*(a) Syntactic equivalence of the non-empty field constraint.* The non-empty field constraint — each present field has at least one component — is equivalent to three syntactic conditions on the raw tumbler: (i) no two zeros are adjacent, (ii) `t₁ ≠ 0`, (iii) `t_{#t} ≠ 0`. Forward: if every field has at least one positive component, then between any two separator zeros there is at least one positive component (ruling out adjacent zeros), the first component belongs to the node field which is non-empty (ruling out a leading zero), and the last component belongs to the last present field which is non-empty (ruling out a trailing zero). Reverse: if (i)–(iii) hold, then every zero is flanked on both sides by non-zero components, so every inter-separator segment is non-empty.

*(b) Unique parse.* Under the positive-component constraint, a position `i` satisfies `tᵢ = 0` if and only if `i` is a field separator — no field component can be zero, so zeros appear exclusively as separators. The separator positions are therefore uniquely determined by `t`. The fields are the maximal contiguous sub-sequences between consecutive separators (or between the endpoints of `t` and the nearest separator). By part (a), each such sub-sequence is non-empty. Therefore `fields(t)` — the decomposition into node, user, document, and element fields — is well-defined and uniquely determined by `t` alone.

*(c) Level determination.* Define `zeros(t) = #{i : 1 ≤ i ≤ #t ∧ tᵢ = 0}`. T4 constrains `zeros(t) ∈ {0, 1, 2, 3}`. By part (b), every zero is a separator and every separator is a zero, so `zeros(t)` equals the number of field boundaries. The number of fields present is `zeros(t) + 1`. The mapping from zero count to hierarchical level — 0 ↦ node, 1 ↦ user, 2 ↦ document, 3 ↦ element — is injective: distinct zero counts yield distinct levels, and the four levels exhaust the range `{0, 1, 2, 3}`. Without the positive-component constraint this fails: a tumbler `[1, 0, 0, 3]` would have `zeros(t) = 2` but an ambiguous parse, since the second zero could be a separator or a field component. T4 eliminates this ambiguity. ∎

*Formal Contract:*
- *Axiom:* Valid address tumblers satisfy `zeros(t) ≤ 3`, `(A i : 1 ≤ i ≤ #t ∧ tᵢ ≠ 0 : tᵢ > 0)`, no adjacent zeros, `t₁ ≠ 0`, `t_{#t} ≠ 0`.
- *Postconditions:* (a) `fields(t)` is well-defined and unique. (b) `zeros(t)` determines the hierarchical level bijectively on `{0, 1, 2, 3}`.


## Contiguous subtrees

T4, combined with the total order T1, gives us the property that makes spans work:

**T5 (Contiguous subtrees).** For any tumbler prefix `p`, the set `{t ∈ T : p ≼ t}` (where `≼` denotes "is a prefix of") forms a contiguous interval under T1:

  `[p ≼ a ∧ p ≼ c ∧ a ≤ b ≤ c ⟹ p ≼ b]`

*Proof.* From T1, if `p ≼ a` then `a` agrees with `p` on the first `#p` components. If `a ≤ b ≤ c` and both `a` and `c` share prefix `p`, then `b` must also share prefix `p`. We consider two cases.

*Case 1: `#b ≥ #p`.* If `b` diverged from `p` at some position `k ≤ #p`, then either `bₖ < pₖ` (contradicting `a ≤ b` since `aₖ = pₖ`) or `bₖ > pₖ` (contradicting `b ≤ c` since `cₖ = pₖ`). So `b` agrees with `p` on all `#p` positions, hence `p ≼ b`.

*Case 2: `#b < #p`.* Since `p ≼ a`, we have `#a ≥ #p > #b`, so `b` is shorter than `a`. By T1, `a ≤ b` requires a first divergence point `j ≤ #b` where `aⱼ < bⱼ` (since `a` cannot be a prefix of the shorter `b`). But `aⱼ = pⱼ` (because `j ≤ #b < #p` and `a` shares prefix `p`), so `bⱼ > pⱼ = cⱼ`. This contradicts `b ≤ c`, since `b` exceeds `c` at position `j` and they agree on all prior positions. ∎

This is Nelson's key insight: "The first point of a span may designate a server, an account, a document or an element; so may the last point. There is no choice as to what lies between; this is implicit in the choice of first and last point." T5 is what makes this true. A span between two endpoints under the same prefix captures exactly the addresses under that prefix between those endpoints — no addresses from unrelated subtrees can interleave.

Because the hierarchy is projected onto a flat line (T1), containment in the tree corresponds to contiguity on the line. Nelson: "A span may be visualized as a zone hanging down from the tumbler line — what is called in computer parlance a depth-first spanning tree." Every subtree maps to a contiguous range, and every contiguous range within a subtree stays within the subtree.


## Decidable containment

The total order T1 determines *sequence* (which address comes first). But the system also needs *containment* — does address `a` belong to account `b`? Is document `d₁` under the same server as document `d₂`? These are not ordering questions; they are prefix questions.

**T6 (Decidable containment).** For any two tumblers `a, b ∈ T`, the following are decidable from the addresses alone:

  (a) Whether `a` and `b` share the same node field.

  (b) Whether `a` and `b` share the same node and user fields.

  (c) Whether `a` and `b` share the same node, user, and document-lineage fields.

  (d) Whether the document field of `a` is a prefix of the document field of `b` (structural subordination within a document family).

T6 is a corollary: it follows immediately from T4 — we extract the relevant fields and compare. We state it separately because the decidability claim is load-bearing for decentralized operation, but it introduces no independent content beyond T4.

We must note what T6(d) does NOT capture. The document field records the *allocation hierarchy* — who baptised which sub-number — not the *derivation history*. Version `5.3` was allocated under document `5`, but this tells us nothing about which version's content was copied to create `5.3`. Nelson: "the version, or subdocument number is only an accidental extension of the document number, and strictly implies no specific relationship of derivation." Formal version-derivation requires the version graph, not just the address.

Nelson confirms that shared prefix means shared containing scope: "The owner of a given item controls the allocation of the numbers under it." The prefix IS the path from root to common ancestor. But he cautions: "Tumblers do not affect the user-level structure of the documents; they only provide a mapping mechanism, and impose no categorization and no structure on the contents of a document." Shared prefix guarantees containment and ownership, never semantic categorization.

Gregory's implementation confirms the distinction between ordering and containment. The codebase provides both `tumblercmp` (total order comparison) and `tumbleraccounteq` (prefix-matching predicate with zero-as-wildcard semantics). The latter truncates the candidate to the length of the parent and checks for exact match — this is the operational realization of T6, and it is a genuinely different algorithm from the ordering comparison.


## Subspace disjointness

Within a document's element space, the first component after the third zero delimiter identifies the *subspace*: 1 for text, 2 for links. Nelson also mentions that the link subspace "could be further subdivided." The critical property is permanent separation:

**T7 (Subspace disjointness).** The subspace identifier (the first component of the element field) permanently separates the address space into disjoint regions. No tumbler in subspace `s₁` can equal or be confused with a tumbler in subspace `s₂ ≠ s₁`.

  `(A a, b ∈ T : a.E₁ ≠ b.E₁ ⟹ a ≠ b)`

*Proof (corollary of T3, T4).* Both `a` and `b` have element fields, so `zeros(a) = zeros(b) = 3` (T4). Write their field lengths as `(α, β, γ, δ)` and `(α', β', γ', δ')`, so that `E₁` sits at position `pₐ = α + β + γ + 4` in `a` and `pᵦ = α' + β' + γ' + 4` in `b`.

*Case 1* (`pₐ = pᵦ`): The tumblers have `a[pₐ] = Eₐ₁ ≠ Eᵦ₁ = b[pₐ]`, so `a ≠ b` by T3.

*Case 2* (`pₐ ≠ pᵦ`): If `#a ≠ #b`, then `a ≠ b` by T3 (distinct lengths). If `#a = #b`, the zero-position sets of `a` — at `α + 1`, `α + β + 2`, `α + β + γ + 3` — and of `b` — at `α' + 1`, `α' + β' + 2`, `α' + β' + γ' + 3` — cannot all coincide: matching the first gives `α = α'`, then the second gives `β = β'`, then the third gives `γ = γ'`, whence `pₐ = pᵦ`, contradicting the case hypothesis. So there exists a position `j` that is a separator in one tumbler but not the other. At `j`, one tumbler has value 0 and the other has a field component, which is strictly positive by T4's positive-component constraint. They differ at `j`, giving `a ≠ b` by T3. ∎

We state T7 explicitly because it is load-bearing for the guarantee that operations within one content type do not interfere with another. T7 is the structural basis — arithmetic within subspace 1 cannot produce addresses in subspace 2, because the subspace identifier is part of the address, not metadata.

The ordering T1 places all text addresses (subspace 1) before all link addresses (subspace 2) within the same document, because `1 < 2` at the subspace position. This is a consequence, not an assumption — it falls out of the lexicographic order.


## Allocation permanence

The most consequential property of the address system is that once an address is allocated, it persists forever:

**T8 (Allocation permanence).** If tumbler `a ∈ T` has been allocated at any point in the system's history, then for all subsequent states, `a` remains in the set of allocated addresses. No operation removes an allocated address from the address space. The set of allocated addresses is monotonically non-decreasing.

*Proof.* T8 holds by construction from the system's state-transition design. We must show that for every state transition s → s', `allocated(s) ⊆ allocated(s')`. The system defines three classes of operation on tumblers: comparison and parsing (T1, T2, T4), which are read-only; arithmetic (⊕, ⊖, inc), which are pure functions on T that compute new tumbler values without mutating allocation state; and allocation, which is the sole operation that modifies the allocated set. T10a below constrains allocation to a single mechanism: each allocator advances its frontier via `inc` (TA5), producing a new address strictly greater than the previous, and adds it to the allocated set. Allocation is strictly additive — it inserts a new element and removes nothing. The system specification defines no inverse operation: no "deallocate", "free", or "reclaim" that would remove an address from the allocated set. Since every state transition either leaves the allocated set unchanged (read-only and arithmetic operations) or strictly grows it (allocation), `allocated(s) ⊆ allocated(s')` holds for every transition. By induction over transition sequences, the invariant holds for all reachable states. ∎

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


## Coordination-free uniqueness

The tumbler hierarchy exists so that independent actors can allocate addresses without communicating:

**T10 (Partition independence).** The address space is partitioned by prefix into ownership domains. Two allocators with distinct, non-nesting prefixes can allocate simultaneously, and the resulting addresses are guaranteed distinct.

Formally: let `p₁` and `p₂` be prefixes such that neither is a prefix of the other (`p₁ ⋠ p₂ ∧ p₂ ⋠ p₁`). Then for any tumbler `a` with prefix `p₁` and any tumbler `b` with prefix `p₂`, `a ≠ b`.

This follows from the definition: if `a` has prefix `p₁` and `b` has prefix `p₂`, and the prefixes diverge at some position `k` with `p₁ₖ ≠ p₂ₖ`, then `aₖ = p₁ₖ ≠ p₂ₖ = bₖ`, so `a ≠ b`. The proof is elementary, but the property is architecturally profound. Nelson: "The owner of a given item controls the allocation of the numbers under it." No central allocator is needed. No coordination protocol is needed. The address structure itself makes collision impossible.

Nelson: "Whoever owns a specific node, account, document or version may in turn designate (respectively) new nodes, accounts, documents and versions, by forking their integers. We often call this the 'baptism' of new numbers." Baptism is the mechanism by which ownership domains are established — the owner of a number creates sub-numbers beneath it, and those sub-numbers belong exclusively to the owner.

**T10a (Allocator discipline).** Each allocator produces its sibling outputs exclusively by repeated application of `inc(·, 0)` — shallow increment at the last significant position. To spawn a child allocator, the parent performs one `inc(·, k')` with `k' > 0` to establish the child's prefix, then delegates further allocation to the child. The parent's own sibling stream resumes with `inc(·, 0)`.

T10a constrains what would otherwise be an unregulated choice. Without it, an allocator could intermix shallow and deep increments, generating outputs of varying lengths. The constraint to `k = 0` for siblings is essential: since `inc(·, 0)` preserves length (TA5(c) below), all sibling outputs from a single allocator have the same length. This uniform-length property is what the partition monotonicity and global uniqueness proofs depend on. If an allocator used `k > 0` for siblings, successive outputs would have increasing lengths and each output would extend the previous — making successive siblings nest rather than stand disjoint. This nesting would break the non-nesting premise required by the Prefix Ordering Extension lemma below.

The `k > 0` operation is reserved exclusively for child-spawning: a single deep increment that establishes a new prefix at a deeper level, from which a new allocator continues with its own `inc(·, 0)` stream.

We first establish a lemma that converts ordering of prefixes into ordering of all addresses under those prefixes.

**PrefixOrderingExtension (Prefix ordering extension).** Let `p₁, p₂ ∈ T` be tumblers such that `p₁ < p₂` and neither is a prefix of the other (`p₁ ⋠ p₂ ∧ p₂ ⋠ p₁`). Then for every `a` extending `p₁` (`p₁ ≼ a`) and every `b` extending `p₂` (`p₂ ≼ b`), `a < b`.

*Proof.* Since `p₁ < p₂` and neither is a prefix of the other, T1 case (i) applies: there exists a position `k ≤ min(#p₁, #p₂)` such that `p₁` and `p₂` agree on positions `1, ..., k-1` and `p₁ₖ < p₂ₖ`. (Case (ii) is excluded because `p₁` is not a proper prefix of `p₂`.) Now `a` extends `p₁`, so `aᵢ = p₁ᵢ` for all `i ≤ #p₁`; in particular `aₖ = p₁ₖ`. Similarly `bₖ = p₂ₖ`. On positions `1, ..., k-1`, `aᵢ = p₁ᵢ = p₂ᵢ = bᵢ`. At position `k`, `aₖ = p₁ₖ < p₂ₖ = bₖ`. So `a < b` by T1 case (i). ∎

**PartitionMonotonicity (Partition monotonicity).** Within any prefix-delimited partition of the address space, the set of allocated addresses is totally ordered by T1, and this order is consistent with the allocation order of any single allocator within that partition. Moreover, for any two sibling sub-partitions with non-nesting prefixes `p₁ < p₂`, every address extending `p₁` precedes every address extending `p₂` under T1 — the per-allocator ordering extends to a cross-allocator ordering determined by the prefix structure.

*Proof.* Consider a partition with prefix `p`. Every allocated address in this partition has prefix `p`, hence lies in the contiguous interval guaranteed by T5. Within the partition, addresses belong to sub-partitions owned by distinct allocators. These sub-partitions have prefixes that are siblings — they share the parent prefix `p` but diverge at the component that distinguishes one allocator from another.

We claim that sibling prefixes are non-nesting. The first sub-partition prefix `t₀` is produced by `inc(parent, k)` with `k > 0`, giving `#t₀ = #parent + k` (by TA5(d)). By T10a, subsequent sibling prefixes are produced by `inc(·, 0)`: `t₁ = inc(t₀, 0)`, `t₂ = inc(t₁, 0)`, and so on. By TA5(c), `inc(t, 0)` preserves the length of `t`: `#inc(t, 0) = #t`. So all sibling prefixes have the same length `#t₀`. Two tumblers of the same length cannot stand in a prefix relationship unless they are equal (a proper prefix is strictly shorter). Since they differ at position `sig(t)` (TA5(c) increments that component), they are unequal, hence non-nesting.

Each allocator's output is monotonic (T9). The sub-partitions are ordered by their prefixes under T1. The prefix ordering extension lemma gives `a < b` for every address `a` under an earlier prefix and every address `b` under a later prefix. Within each sub-partition, allocation order matches address order by T9. ∎

**GlobalUniqueness (Global uniqueness).** No two distinct allocations, anywhere in the system, at any time, produce the same address.

*Proof.* Consider allocations producing addresses `a` and `b` by distinct allocation events. Four cases arise.

*Case 1: Same allocator.* Both addresses are produced by the same allocator's sequential stream. T9 guarantees `a ≠ b` because allocation is strictly monotonic.

*Case 2: Different allocators at the same hierarchical level.* The allocators have prefixes `p₁` and `p₂` that are siblings — neither is a prefix of the other. T10 gives `a ≠ b` directly.

*Case 3: Different allocators with nesting prefixes and different zero counts.* One allocator's prefix nests within another's. But these allocators produce addresses with different zero counts: the node allocator produces addresses with `zeros = 1` (user-level), while the element allocator produces addresses with `zeros = 3`. By T4, different zero counts imply different field structure. If `#a ≠ #b`, then `a ≠ b` by T3 directly. If `#a = #b`, then `zeros(a) ≠ zeros(b)` means there exists a position where one is zero and the other nonzero — by T3, `a ≠ b`.

*Case 4: Different allocators with nesting prefixes and the same zero count.* This arises when a parent and child allocator both produce addresses at the same hierarchical level. By T10a, the parent allocator uses `inc(·, 0)` for all its sibling allocations. Its first output has some length `γ₁`; since `inc(·, 0)` preserves length (TA5(c)), all subsequent parent siblings have length `γ₁`. The child allocator's prefix was established by `inc(parent_output, k')` with `k' > 0`, giving prefix length `γ₁ + k'` (by TA5(d)). The child then uses `inc(·, 0)` for its own siblings — all its outputs have the uniform length `γ₁ + k'`. Since `k' ≥ 1`, the child's outputs are strictly longer than the parent's: `γ₁ + k' > γ₁`. By T3, `a ≠ b`. One pair requires separate treatment: the parent's child-spawning output that established the child's prefix has the same length as the child's sibling outputs (both `γ₁ + k'`). However, this output IS the child's base address, and every child sibling output is strictly greater than its base (by TA5(a)), hence distinct. The length separation is additive across nesting levels — each `inc(·, k')` with `k' ≥ 1` adds at least one component, so a descendant `d` nesting levels below has output length at least `γ₁ + d > γ₁`. Allocators at different branches that are not ancestors of each other have non-nesting prefixes and are handled by Case 2.

The argument depends critically on T10a's constraint that sibling allocations use `k = 0`. If a parent allocator could use `k > 0` for siblings, its outputs would have increasing lengths, and some parent output could match the length of a child output, collapsing the length separation. ∎

This theorem is the foundation of the addressing architecture. Every subsequent guarantee — link stability, transclusion identity, royalty tracing — depends on the uniqueness of addresses. And uniqueness is achieved without any distributed consensus, simply by the structure of the names.


## Tumbler arithmetic

We now turn to the arithmetic operations. The system requires operations that advance a position by a displacement (for computing span endpoints and shifting positions) and that recover the displacement between two positions (for computing span widths). These operations — tumbler addition and subtraction — are not arithmetic on numbers but position-advance operations in a hierarchical address space.

A displacement `w` is a tumbler whose leading zeros say "stay at these hierarchical levels" and whose first nonzero component says "advance here." Components after the advance point describe the structure of the landing position within the target region.

### Addition for position advancement

Let `⊕` denote tumbler addition: given a start position `a` and a displacement `w`, compute the advanced position.

We require a notion of where a displacement "acts." For a positive displacement `w = [w₁, w₂, ..., wₙ]`, define the *action point* as `k = min({i : 1 ≤ i ≤ n ∧ wᵢ ≠ 0})` — the position of the first nonzero component. The leading zeros say "stay at these hierarchical levels"; the first nonzero component says "advance here."

**TA0 (Well-defined addition).** For tumblers `a, w ∈ T` where `w > 0` and the action point `k` of `w` satisfies `k ≤ #a`, the result `a ⊕ w` is a well-defined tumbler in `T`.

The precondition `k ≤ #a` is essential: the constructive definition copies components `a₁, ..., aₖ₋₁` from the start position and adds `wₖ` to `aₖ`, so position `k` must exist within `a`. A displacement whose action point exceeds `#a` — one with more leading zeros than `a` has components — would attempt to "stay at" hierarchical levels that the start position does not have, and the operation is undefined.

**Verification of TA0.** By the constructive definition (below), `a ⊕ w = [r₁, ..., r_{#w}]` where: `rᵢ = aᵢ` for `i < k`, `rₖ = aₖ + wₖ`, and `rᵢ = wᵢ` for `i > k`. The result has length `#w`, which is finite and at least 1 since `w ∈ T`. Each prefix component `rᵢ = aᵢ ∈ ℕ` (inherited from `a ∈ T`); the action-point component `rₖ = aₖ + wₖ ∈ ℕ` (ℕ is closed under addition); each tail component `rᵢ = wᵢ ∈ ℕ` (inherited from `w ∈ T`). The result is a finite sequence of non-negative integers with at least one component — a member of `T`.

*Formal Contract:*
- *Preconditions:* a ∈ T, w ∈ T, w > 0, actionPoint(w) ≤ #a
- *Postconditions:* a ⊕ w ∈ T, #(a ⊕ w) = #w

**TA1 (Order preservation under addition).** `(A a, b, w : a < b ∧ w > 0 ∧ k ≤ min(#a, #b) : a ⊕ w ≤ b ⊕ w)`, where `k` is the action point of `w`.

TA1 guarantees weak (`≤`) order preservation universally — if two positions were in order before advancement, they remain in non-reversed order after. The precondition `k ≤ min(#a, #b)` inherits from TA0: both operations must be well-defined.

**Verification of TA1.** Let `k` be the action point of `w`. By the constructive definition (below), for both `a ⊕ w` and `b ⊕ w`: positions before `k` copy from the start, position `k` adds `wₖ`, and positions after `k` copy from `w`. Since `a < b`, by T1 either (i) there exists a first position `j ≤ min(#a, #b)` where `aⱼ < bⱼ`, or (ii) `a` is a proper prefix of `b`. In case (ii), `aᵢ = bᵢ` for all `i ≤ #a`, and since `k ≤ min(#a, #b) = #a`, both additions agree on every position: `a ⊕ w = b ⊕ w`, satisfying `≤`. In case (i), three sub-cases arise based on the relationship between `j` and `k`:

*Sub-case j < k:* Position `j` falls in the prefix-copy phase. `(a ⊕ w)ⱼ = aⱼ < bⱼ = (b ⊕ w)ⱼ`, with agreement on all prior positions. By T1 case (i), `a ⊕ w < b ⊕ w`.

*Sub-case j = k:* At position `k`, `(a ⊕ w)ₖ = aₖ + wₖ < bₖ + wₖ = (b ⊕ w)ₖ` since `aₖ < bₖ` and natural-number addition preserves strict inequality. Positions before `k` agree. By T1 case (i), `a ⊕ w < b ⊕ w`.

*Sub-case j > k:* Since `k < j`, `aₖ = bₖ`, so `(a ⊕ w)ₖ = aₖ + wₖ = bₖ + wₖ = (b ⊕ w)ₖ`. For `i < k`, `(a ⊕ w)ᵢ = aᵢ = bᵢ = (b ⊕ w)ᵢ`. For `i > k`, both results copy from `w`: `(a ⊕ w)ᵢ = wᵢ = (b ⊕ w)ᵢ`. The results are identical: `a ⊕ w = b ⊕ w`, satisfying `≤`.

In all cases, `a ⊕ w ≤ b ⊕ w`. ∎

*Formal Contract:*
- *Preconditions:* a ∈ T, b ∈ T, w ∈ T, a < b, w > 0, actionPoint(w) ≤ min(#a, #b)
- *Postconditions:* a ⊕ w ≤ b ⊕ w

Strict order preservation holds under a tighter condition. We first need a precise notion of where two tumblers first differ.

**Definition (Divergence).** For tumblers `a, b ∈ T` with `a ≠ b`, the *divergence* `divergence(a, b)` is defined by two cases corresponding to the two cases of T1:

  (i) If there exists `k ≤ min(#a, #b)` such that `aₖ ≠ bₖ` and `(A i : 1 ≤ i < k : aᵢ = bᵢ)`, then `divergence(a, b) = k` — component divergence at a shared position.

  (ii) If `(A i : 1 ≤ i ≤ min(#a, #b) : aᵢ = bᵢ)` and `#a ≠ #b`, then `divergence(a, b) = min(#a, #b) + 1` — prefix divergence, where one tumbler is a proper prefix of the other.

Exactly one case applies for any `a ≠ b`. In case (i), `a` and `b` differ at a component both possess. In case (ii), they agree on all shared positions but one is longer — the divergence lies "just past" the shorter tumbler's last component.

For prefix-related pairs, `divergence(a, b) = min(#a, #b) + 1 > min(#a, #b)`. Since TA0 requires `k ≤ min(#a, #b)`, the condition `k ≥ divergence(a, b)` in TA1-strict below is unsatisfiable for prefix-related operands. This is correct: when `a` is a proper prefix of `b` (or vice versa), Case 1 of the verification below shows that addition erases the divergence, producing equality rather than strict inequality. TA1-strict makes no claim about prefix-related pairs — TA1 (weak) covers them, guaranteeing non-reversal.

**TA1-strict (Strict order preservation).** `(A a, b, w : a < b ∧ w > 0 ∧ k ≤ min(#a, #b) ∧ k ≥ divergence(a, b) : a ⊕ w < b ⊕ w)`, where `k` is the action point of `w`.

When the action point falls before the divergence — `k < divergence(a, b)` — both operands agree at position `k`, both get the same `wₖ` added, and both copy the same tail from `w` afterward. The original divergence is erased and the results are equal. For example, `a = [1, 3]`, `b = [1, 5]` (diverge at position 2), `w = [2]` (action point at position 1): `a ⊕ w = [3] = b ⊕ w`. Order degrades to equality, never reversal.

*Proof.* Let `j = divergence(a, b)` and let `k` be the action point of `w`. The preconditions give `k ≤ min(#a, #b)` and `k ≥ j`. Since `j ≤ k ≤ min(#a, #b)`, the Divergence definition places us in case (i): `j` is a shared position with `aⱼ < bⱼ` (from `a < b`) and `aᵢ = bᵢ` for all `i < j`. The condition `k ≥ j` excludes the divergence-erasing regime — the action point acts at or beyond the first disagreement. Two cases arise.

*Case 1: `k = j`.* By TumblerAdd, for `i < k`: `(a ⊕ w)ᵢ = aᵢ = bᵢ = (b ⊕ w)ᵢ`, since `i < j = k` implies `aᵢ = bᵢ` (agreement before the divergence). At position `k`: `(a ⊕ w)ₖ = aₖ + wₖ` and `(b ⊕ w)ₖ = bₖ + wₖ`. Since `aₖ < bₖ` (divergence at `j = k`) and natural-number addition preserves strict inequality, `aₖ + wₖ < bₖ + wₖ`. The results agree on all positions before `k` and diverge strictly at `k`. By T1 case (i), `a ⊕ w < b ⊕ w`.

*Case 2: `k > j`.* By TumblerAdd, for `i < k`: `(a ⊕ w)ᵢ = aᵢ` and `(b ⊕ w)ᵢ = bᵢ` (prefix-copy phase). Since `j < k`, position `j` falls in this phase: `(a ⊕ w)ⱼ = aⱼ < bⱼ = (b ⊕ w)ⱼ`. For `i < j`: `(a ⊕ w)ᵢ = aᵢ = bᵢ = (b ⊕ w)ᵢ` (agreement before the divergence). The original divergence at position `j` is preserved intact in the results. By T1 case (i), `a ⊕ w < b ⊕ w`.

In both cases, `a ⊕ w < b ⊕ w`. ∎

*Formal Contract:*
- *Preconditions:* a ∈ T, b ∈ T, w ∈ T, a < b, w > 0, actionPoint(w) ≤ min(#a, #b), actionPoint(w) ≥ divergence(a, b)
- *Postconditions:* a ⊕ w < b ⊕ w

But TA1 alone does not guarantee that addition *advances* a position. It preserves relative order between two positions but is silent about the relationship between `a` and `a ⊕ w`. We need:

**TA-strict (Strict increase).** `(A a ∈ T, w > 0 : a ⊕ w > a)` (where `a ⊕ w` is well-defined, i.e., `k ≤ #a` per TA0).

Without TA-strict, the axioms admit a degenerate model in which `a ⊕ w = a` for all `a, w`. This no-op model satisfies TA0 (result is in T), TA1 (if `a < b` then `a < b` — the consequent is unchanged), and TA4 (`(a ⊕ w) ⊖ w = a ⊖ w = a` if subtraction is equally degenerate). Every axiom is satisfied, yet spans are empty — the interval `[s, s ⊕ ℓ)` collapses to `[s, s)`. TA-strict excludes this model and ensures that advancing by a positive displacement moves forward. T12 (span well-definedness) depends on this directly.

**Verification of TA-strict.** Let `k` be the action point of `w`. By the constructive definition (below), `(a ⊕ w)ᵢ = aᵢ` for `i < k`, and `(a ⊕ w)ₖ = aₖ + wₖ`. Since `k` is the action point, `wₖ > 0`, so `aₖ + wₖ > aₖ`. Positions `1` through `k - 1` agree; position `k` is strictly larger. By T1 case (i), `a ⊕ w > a`.

### Subtraction for width computation

Let `⊖` denote tumbler subtraction: given two positions, compute the displacement between them.

**TA2 (Well-defined subtraction).** For tumblers `a, w ∈ T` where `a ≥ w`, `a ⊖ w` is a well-defined tumbler in `T`.

**Verification of TA2.** By TumblerSub, two cases arise. If the zero-padded sequences of `a` and `w` agree at every position, the result is the zero tumbler of length `max(#a, #w)` — a member of `T`. Otherwise, let `k` be the first divergence position (after zero-padding). The result `a ⊖ w = [r₁, ..., r_p]` has length `p = max(#a, #w)`, which is finite and at least 1. Each pre-divergence component `rᵢ = 0 ∈ ℕ`. At the divergence point: `a ≥ w` ensures `aₖ > wₖ` — if `a > w` by T1 case (i), the divergence falls at `k ≤ min(#a, #w)` with `aₖ > wₖ` directly; if `a > w` by T1 case (ii), `w` is a proper prefix of `a`, so `k > #w` and `wₖ = 0` (zero-padded), with `aₖ > 0` (otherwise no divergence at `k`). In either case, `rₖ = aₖ - wₖ ∈ ℕ`. Each tail component `rᵢ = aᵢ ∈ ℕ` (inherited from `a ∈ T`, or `0` when `i > #a`). The result is a finite sequence of non-negative integers with at least one component — a member of `T`.

*Formal Contract:*
- *Preconditions:* a ∈ T, w ∈ T, a ≥ w
- *Postconditions:* a ⊖ w ∈ T

**TA3 (Order preservation under subtraction, weak).** `(A a, b, w : a < b ∧ a ≥ w ∧ b ≥ w : a ⊖ w ≤ b ⊖ w)`.

The subtraction algorithm differs structurally from addition — it zeros positions before the divergence point and copies the tail from the minuend, whereas addition copies the tail from the displacement. We verify TA3 directly by case analysis.

**Verification of TA3.** By TA2, since `a ≥ w` and `b ≥ w`, both `a ⊖ w` and `b ⊖ w` are well-formed tumblers in `T`, making the order comparison well-defined. By TumblerSub, for any `x ≥ w`: if the zero-padded sequences of `x` and `w` agree everywhere, `x ⊖ w` is the zero tumbler of length `max(#x, #w)`; otherwise, let `d_x` be the first divergence position (under zero-padding), and the result has zeros at positions before `d_x`, value `x_{d_x} - w_{d_x}` at position `d_x`, and `xᵢ` copied for positions after `d_x`, with length `max(#x, #w)`. We say `x` is *zero-padded-equal* to `w` when no such divergence exists.

Since `a < b`, by T1 either (i) there exists a first position `j ≤ min(#a, #b)` where `aⱼ < bⱼ`, or (ii) `j = #a + 1 ≤ #b` — `a` is a proper prefix of `b`. We organize the case analysis around these two forms of `a < b` and the divergence structure of the operands against `w`.

*Case 0: `a` is a proper prefix of `b`* (T1 case (ii)). Then `#a < #b` and `aᵢ = bᵢ` for all `i ≤ #a`.

*Sub-case `a = w`.* Then `a ⊖ w = [0, ..., 0]` (the zero tumbler of length `max(#a, #w) = #a`). Since `b > a = w` and `a` is a proper prefix of `b`, we have `bᵢ = wᵢ` for all `i ≤ #w = #a`. If some component of `b` beyond `#w` is nonzero, then `b ⊖ w` is a positive tumbler, and by TA6 the zero tumbler `a ⊖ w` is strictly less. If all components of `b` beyond `#w` are zero (so zero-padded `w` equals `b`), then `b ⊖ w = [0, ..., 0]` of length `max(#b, #w) = #b`. Both results are zero tumblers, but `#(a ⊖ w) = #a < #b = #(b ⊖ w)`, so `a ⊖ w` is a proper prefix of `b ⊖ w`, giving `a ⊖ w < b ⊖ w` by T1 case (ii).

*Sub-case `a > w` with divergence.* Let `dₐ = divergence(a, w)` under zero-padding. If `a > w` by T1 case (i), `dₐ ≤ min(#a, #w) ≤ #a`. If `a > w` by T1 case (ii), `w` is a proper prefix of `a` and `dₐ` falls at the smallest `i > #w` with `aᵢ > 0`, so `dₐ ≤ #a`. Since `bᵢ = aᵢ` for all `i ≤ #a` and `dₐ ≤ #a`, the comparison of `b` against `w` (under zero-padding) agrees with that of `a` at all positions up to `dₐ`. So `d_b = dₐ = d`.

Apply the subtraction formula to both. At positions `i < d`: both results are zero. At position `d`: both compute `a_d - w_d = b_d - w_d` (since `a_d = b_d` for `d ≤ #a`). At positions `d < i ≤ #a`: both copy from their respective minuends, giving `aᵢ = bᵢ`. The two results agree on positions `1, ..., #a`.

Beyond position `#a`, the results may differ. The result `a ⊖ w` has length `max(#a, #w)`. At positions `#a < i ≤ max(#a, #w)` (present only when `#w > #a`): `(a ⊖ w)ᵢ = 0` (from `a`'s zero-padding). For `(b ⊖ w)ᵢ`: when `i ≤ #b`, the value is `bᵢ` (copied from the minuend since `i > d`); when `i > #b`, the value is `0` (from `b`'s zero-padding). In either case `(a ⊖ w)ᵢ ≤ (b ⊖ w)ᵢ`. The result `b ⊖ w` has length `max(#b, #w) ≥ max(#a, #w)` (since `#b > #a`). Now `a ⊖ w` is no longer than `b ⊖ w`, and they agree on positions `1, ..., #a`. If no disagreement exists on positions `1, ..., max(#a, #w)`, then `a ⊖ w` is a prefix of `b ⊖ w`, giving `a ⊖ w ≤ b ⊖ w` by T1 case (ii). If a first disagreement exists at position `p > #a`, then `(a ⊖ w)_p = 0 ≤ (b ⊖ w)_p`. If the disagreement is strict, `a ⊖ w < b ⊖ w` by T1 case (i). If `(b ⊖ w)_p = 0` at all such positions, then `a ⊖ w` is a prefix of `b ⊖ w`, giving `a ⊖ w ≤ b ⊖ w` by T1 case (ii).

*Sub-case `a > w` without divergence (zero-padded equality).* If `a > w` by T1 case (ii) and `aᵢ = 0` for all `i > #w`, then after zero-padding, the sequences are identical. The subtraction `a ⊖ w` yields the zero tumbler of length `#a`. Since `b > a > w` and `#b > #a ≥ #w`, `b` agrees with `w` (hence with `a`) on positions `1, ..., #a`. The result `b ⊖ w` has length `max(#b, #w) = #b > #a`. If `b ⊖ w` has any positive component, then `a ⊖ w` (all zeros) is less by TA6. If `b ⊖ w` is also a zero tumbler, its length `#b > #a = #(a ⊖ w)`, so the shorter is a proper prefix of the longer, giving `a ⊖ w < b ⊖ w` by T1 case (ii).

In all sub-cases of Case 0, `a ⊖ w ≤ b ⊖ w`.

*Case 0a: Component divergence with `a` zero-padded-equal to `w`.* Here `a < b` by T1 case (i): there exists `j ≤ min(#a, #b)` with `aⱼ < bⱼ`. Since the zero-padded sequences of `a` and `w` agree everywhere, `a ⊖ w` is the zero tumbler of length `max(#a, #w)`. At position `j`, `wⱼ = aⱼ` (from zero-padded equality), so `bⱼ > aⱼ = wⱼ`. The pair `(b, w)` diverges at or before `j`, making `b ⊖ w` positive. By TA6, `a ⊖ w < b ⊖ w`.

For the remaining cases, `a < b` by T1 case (i) and `a` is not zero-padded-equal to `w`, so `dₐ = divergence(a, w)` under zero-padding is well-defined. Let `d_b = divergence(b, w)` under zero-padding, and let `j` be the first position where `aⱼ < bⱼ`.

*Case 1: `dₐ = d_b = d`.* Both operands diverge from `w` at the same position. For `i < d`, both results are zero. Since `a` and `b` agree with `w` before `d`, and `aⱼ < bⱼ`, we have `j ≥ d`. If `j = d`: `a_d - w_d < b_d - w_d` (since `a_d < b_d`), so `a ⊖ w < b ⊖ w` by T1 case (i). If `j > d`: `a_d = b_d`, so both results agree at position `d`; at positions `d < i < j`, both copy from their respective minuends which agree (`aᵢ = bᵢ`); at position `j`, `(a ⊖ w)ⱼ = aⱼ < bⱼ = (b ⊖ w)ⱼ` (both in the tail-copy phase since `j > d`). By T1 case (i), `a ⊖ w < b ⊖ w`.

*Case 2: `dₐ < d_b`.* At position `dₐ`, `a_{dₐ} ≠ w_{dₐ}` but `b_{dₐ} = w_{dₐ}`. Since `a` and `b` agree with `w` at all positions before `dₐ`, the first disagreement between `a` and `b` is at `dₐ`, giving `j = dₐ` with `a_{dₐ} < b_{dₐ} = w_{dₐ}`. But `a ≥ w` requires `a_{dₐ} ≥ w_{dₐ}` at the divergence — contradiction. This case is impossible under the preconditions.

*Case 3: `dₐ > d_b`.* At position `d_b`, `b_{d_b} ≠ w_{d_b}` but `a_{d_b} = w_{d_b}`. So `j = d_b` with `a_{d_b} = w_{d_b} < b_{d_b}` (since `a < b` and the first disagreement is at `d_b`; `b ≥ w` ensures `b_{d_b} > w_{d_b}` at this divergence). The result `(a ⊖ w)_{d_b} = 0` (position `d_b < dₐ` falls in the pre-divergence zero phase for `a ⊖ w`). The result `(b ⊖ w)_{d_b} = b_{d_b} - w_{d_b} > 0`. At all positions `i < d_b`, both results are zero. By T1 case (i), `a ⊖ w < b ⊖ w`.

In every case, `a ⊖ w ≤ b ⊖ w`. ∎

*Formal Contract:*
- *Preconditions:* a ∈ T, b ∈ T, w ∈ T, a < b, a ≥ w, b ≥ w
- *Postconditions:* a ⊖ w ≤ b ⊖ w

**TA3-strict (Order preservation under subtraction, strict).** `(A a, b, w : a < b ∧ a ≥ w ∧ b ≥ w ∧ #a = #b : a ⊖ w < b ⊖ w)`.

**Verification of TA3-strict.** The equal-length precondition eliminates Case 0 of the TA3 proof entirely — two tumblers of the same length cannot be in a prefix relationship unless equal, and `a < b` rules out equality. Cases 0a and 1–3 remain, all of which produce strict inequality (`a ⊖ w < b ⊖ w`). ∎

*Formal Contract:*
- *Preconditions:* a ∈ T, b ∈ T, w ∈ T, a < b, a ≥ w, b ≥ w, #a = #b
- *Postconditions:* a ⊖ w < b ⊖ w

### Partial inverse

**TA4 (Partial inverse).** `(A a, w : w > 0 ∧ k = #a ∧ #w = k ∧ (A i : 1 ≤ i < k : aᵢ = 0) : (a ⊕ w) ⊖ w = a)`, where `k` is the action point of `w`.

The precondition has three parts. First, `k = #a` — the action point falls at the last component of `a`. This is necessary because addition replaces `a`'s trailing structure below the action point with `w`'s trailing structure (tail replacement, defined below). When `k < #a`, components `aₖ₊₁, ..., a_{#a}` are discarded by addition and cannot be recovered by subtraction. Concretely: `[1, 5] ⊕ [1, 3] = [2, 3]` (action point 1, position 2 replaced by `w`'s trailing `3`), then `[2, 3] ⊖ [1, 3] = [1, 3] ≠ [1, 5]`.

Second, `#w = k` — the displacement has no trailing components beyond the action point. When `#w > k`, the result acquires trailing components from `w` that were not present in `a`. The trailing `7` from `w` persists through subtraction: `[0, 5] ⊕ [0, 3, 7] = [0, 8, 7]`, then `[0, 8, 7] ⊖ [0, 3, 7]` yields `[0, 5, 7] ≠ [0, 5]`.

Third, `(A i : 1 ≤ i < k : aᵢ = 0)` — all components of `a` before the action point are zero. This ensures the subtraction's divergence-discovery mechanism finds the action point at the right position. If `a` has a nonzero component at some position `j < k`, then the result of addition has `rⱼ = aⱼ ≠ 0`, and the subtraction's divergence falls at `j`, not at `k`. Concretely: `[5, 3] ⊕ [0, 7] = [5, 10]`, then `[5, 10] ⊖ [0, 7]`: divergence at position 1, producing `[5, 10] ≠ [5, 3]`.

When all three conditions hold, recovery is exact. The restriction is not a deficiency but a precise statement of when the operations are inverses.

*Proof.* Let `k` denote the action point of `w`. We compute `r = a ⊕ w` using TumblerAdd and then verify that `r ⊖ w = a` using TumblerSub.

**Computing `r = a ⊕ w`.** By TumblerAdd, each component of `r` is: `rᵢ = aᵢ` for `i < k`, `rₖ = aₖ + wₖ`, and `rᵢ = wᵢ` for `i > k`. The zero-prefix precondition gives `aᵢ = 0` for all `i < k`, so `rᵢ = 0` for `i < k`. The precondition `k = #a` ensures there are no components of `a` beyond position `k` — tail replacement discards nothing. By the result-length identity (`#(a ⊕ w) = #w`), `#r = #w = k` (the second step uses `#w = k`). Therefore `r = [0, ..., 0, aₖ + wₖ]` — a `k`-component tumbler with zeros at all positions before `k`.

**Computing `r ⊖ w`.** By TumblerSub, subtraction scans `r` and `w` for the first divergence. Since `#r = #w = k`, no zero-padding is needed. For positions `i < k`: `rᵢ = 0` (established above) and `wᵢ = 0` (by definition of action point — all positions before `k` are zero in `w`). So `rᵢ = wᵢ = 0` at every position before `k`, and no divergence occurs before position `k`.

At position `k`, two cases arise.

*Case 1: `aₖ > 0`.* Then `rₖ = aₖ + wₖ > wₖ`, so `rₖ ≠ wₖ` and the first divergence is at position `k`. TumblerSub produces: `sᵢ = 0` for `i < k`, `sₖ = rₖ - wₖ = (aₖ + wₖ) - wₖ = aₖ`, and `sᵢ = rᵢ` for `i > k`. Since `#r = k`, there are no positions beyond `k`. The result is `s = [0, ..., 0, aₖ]` of length `k = #a`. The zero-prefix precondition gives `aᵢ = 0` for `i < k` and the last component is `aₖ`, so `s = a`.

*Case 2: `aₖ = 0`.* Then `a` is the zero tumbler of length `k`. The addition gives `rₖ = 0 + wₖ = wₖ`, so `r = [0, ..., 0, wₖ]`. Since `wᵢ = 0` for `i < k` and `#w = k`, this means `r = w`. The subtraction `r ⊖ w = w ⊖ w`: the sequences agree at every position (no divergence exists), so TumblerSub yields the zero tumbler of length `max(#w, #w) = k`. This zero tumbler of length `k` is exactly `a`.

In both cases, `(a ⊕ w) ⊖ w = a`. ∎

*Formal Contract:*
- *Preconditions:* `a ∈ T`, `w ∈ T`, `w > 0`, `k = #a`, `#w = k`, `(A i : 1 ≤ i < k : aᵢ = 0)`, where `k` is the action point of `w`
- *Postconditions:* `(a ⊕ w) ⊖ w = a`

Gregory's analysis confirms that `⊕` and `⊖` are NOT inverses in general. The implementation's `absadd` is asymmetric: the first argument supplies the high-level prefix, the second supplies the low-level suffix. When `d = a ⊖ b` strips a common prefix (reducing the exponent), `b ⊕ d` puts the difference in the wrong operand position — `absadd`'s else branch discards the first argument entirely and returns the second. The operand-order asymmetry causes total information loss even before any digit overflow.

The reverse direction is equally necessary:

**ReverseInverse (Reverse inverse).** `(A a, w : a ≥ w ∧ w > 0 ∧ k = #a ∧ #w = k ∧ (A i : 1 ≤ i < k : aᵢ = 0) : (a ⊖ w) ⊕ w = a)`, where `k` is the action point of `w`.

*Proof.* Let `y = a ⊖ w`. We verify the prerequisites for applying TA4 to `y`. Under the precondition `(A i : 1 ≤ i < k : aᵢ = 0)`, we have `aᵢ = wᵢ = 0` for all `i < k`, so the divergence falls at position `k`. The result `y` has: positions `i < k` zero, position `k` equal to `aₖ - wₖ`, and no components beyond `k` (since `k = #a`). So `#y = k`, `yᵢ = 0` for `i < k`, and `#w = k`. All preconditions for TA4 hold. By TA4, `(y ⊕ w) ⊖ w = y`. Suppose `y ⊕ w ≠ a`. We wish to apply TA3-strict, which requires three preconditions beyond strict ordering: `y ⊕ w ≥ w`, `a ≥ w`, and `#(y ⊕ w) = #a`. The equal-length condition holds: `#(y ⊕ w) = #w = k = #a` (the first step by the result-length identity; `#w = k` and `k = #a` are given). The condition `a ≥ w` is given. We verify `y ⊕ w ≥ w`: since `y ⊕ w ≠ a` and `yₖ = aₖ - wₖ`, we have `yₖ > 0` (if `yₖ = 0` then `aₖ = wₖ`, and since `yᵢ = wᵢ = 0` for `i < k` and `#y = k = #w`, we would have `y = [0,...,0]` and `y ⊕ w = w`; but `a ≥ w` and `aₖ = wₖ` with agreement on all prior positions gives `a = w` when `#a = #w = k`, so `y ⊕ w = w = a`, contradicting our assumption). So `yₖ > 0`, giving `(y ⊕ w)ₖ = yₖ + wₖ > wₖ` with agreement on positions before `k`, hence `y ⊕ w > w`. Now apply TA3-strict. If `y ⊕ w > a`, then `(y ⊕ w) ⊖ w > a ⊖ w = y`, giving `y > y`, a contradiction. If `y ⊕ w < a`, then `(y ⊕ w) ⊖ w < a ⊖ w`, giving `y < y`, a contradiction. So `(a ⊖ w) ⊕ w = a`. ∎


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

**Definition (TumblerSub).** Given an end position `a` and a displacement `w`, recover the start position. When the operands have different lengths, we conceptually zero-pad the shorter to the length of the longer before scanning for divergence. When the zero-padded sequences agree at every position (no divergence exists), the result is the zero tumbler of length `max(#a, #w)`: `a ⊖ w = [0, ..., 0]`. Otherwise, let `k` be the first position where `a` and `w` differ (treating missing components as zero):

```
         ⎧ 0             if i < k        (these levels matched — zero them)
rᵢ   =  ⎨ aₖ - wₖ      if i = k        (reverse the advance)
         ⎩ aᵢ           if i > k        (copy from end position)
```

The result has length `max(#a, #w)`.

**Precondition:** `a ≥ w` — when `a ≠ w`, at the divergence point (after zero-padding) `aₖ ≥ wₖ`.


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

*Case 0: `a` is a proper prefix of `b`.* Then `#a < #b` and `aᵢ = bᵢ` for all `i ≤ #a`.

We first handle the sub-case `a = w`. Then `a ⊖ w = [0, ..., 0]` (the zero tumbler of length `max(#a, #w) = #w = #a`). Since `b > a = w` and `a` is a proper prefix of `b`, we have `bᵢ = wᵢ` for all `i ≤ #w`. Two sub-sub-cases arise. If `b ⊖ w` is a positive tumbler — some component of `b` beyond `#w` is nonzero — then every zero tumbler is less than every positive tumbler (TA6), so `a ⊖ w < b ⊖ w`. If `b ⊖ w` is itself a zero tumbler — all components of `b` beyond `#w` are zero, so zero-padded `w` equals `b` — then `b ⊖ w = [0, ..., 0]` of length `max(#b, #w) = #b`. Both results are zero tumblers, but `#(a ⊖ w) = #a < #b = #(b ⊖ w)` (since `a` is a proper prefix of `b`). The shorter zero tumbler is a proper prefix of the longer, so `a ⊖ w < b ⊖ w` by T1 case (ii). In either sub-sub-case, `a ⊖ w ≤ b ⊖ w`. The sub-case is resolved.

For `a > w`: two sub-cases arise depending on the structure of the divergence between `a` and `w` (after zero-padding).

*Sub-case `a > w` with divergence.* If `a > w` by T1 case (i), the divergence `dₐ` is at a shared position `≤ min(#a, #w) ≤ #a`. If `a > w` by T1 case (ii), `w` is a proper prefix of `a`; after zero-padding `w` to length `#a`, we compare: if at least one component `aᵢ > 0` for `i > #w`, the divergence falls at the smallest such `i`, satisfying `#w < dₐ ≤ #a`. In either T1 case, `dₐ ≤ #a`. Since `bᵢ = aᵢ` for all `i ≤ #a` and `dₐ ≤ #a`, the comparison of `b` (zero-padded) against `w` (zero-padded) agrees with that of `a` at all positions up to `dₐ`. So `d_b = dₐ = d`.

Now apply the subtraction formula to both. At positions `i < d`: both results are zero. At position `d`: both compute `a_d - w_d = b_d - w_d`, since `a_d = b_d` for `d ≤ #a`. At positions `d < i ≤ #a`: both copy from the minuend, giving `aᵢ = bᵢ`. The two results agree on all positions `1, ..., #a`.

Beyond position `#a`, the results may differ. The result `a ⊖ w` has length `max(#a, #w)`. At positions `#a < i ≤ max(#a, #w)` (present only when `#w > #a`): `(a ⊖ w)ᵢ = 0` (from `a`'s zero padding). For `(b ⊖ w)ᵢ`: when `i ≤ #b`, the value is `bᵢ` (copied in the tail phase since `i > d`); when `i > #b`, the value is `0` (from `b`'s zero padding). In either case `(a ⊖ w)ᵢ ≤ (b ⊖ w)ᵢ`. The result `b ⊖ w` has length `max(#b, #w) ≥ max(#a, #w)` (since `#b > #a`). If `max(#b, #w) > max(#a, #w)`, the extra positions come from `b`'s components beyond `max(#a, #w)` when `#b > #w` (copied from the minuend), or are zero when `#w > #b` (from `b`'s zero padding). Now `a ⊖ w` is no longer than `b ⊖ w`, and they agree on positions `1, ..., #a`. We compare lexicographically. If no disagreement exists on positions `1, ..., max(#a, #w)`, then `a ⊖ w` is a prefix of `b ⊖ w` (since `#(a ⊖ w) ≤ #(b ⊖ w)`), giving `a ⊖ w ≤ b ⊖ w` by T1 case (ii). If a first disagreement exists at some position `j > #a`, then `(a ⊖ w)ⱼ = 0 ≤ (b ⊖ w)ⱼ` (where `(b ⊖ w)ⱼ = bⱼ` when `j ≤ #b`, or `0` when `j > #b`). If the disagreement is strict (`(a ⊖ w)ⱼ = 0 < (b ⊖ w)ⱼ`), we have `a ⊖ w < b ⊖ w` by T1 case (i). If `(b ⊖ w)ⱼ = 0` at all positions `#a < j ≤ max(#a, #w)`, then `a ⊖ w` and `b ⊖ w` agree through position `max(#a, #w)`, and `a ⊖ w` is a prefix of the longer `b ⊖ w`, giving `a ⊖ w ≤ b ⊖ w` by T1 case (ii). In either case, `a ⊖ w ≤ b ⊖ w`.

*Sub-case `a > w` without divergence (zero-padded equality).* If `a > w` by T1 case (ii) and `aᵢ = 0` for all `i > #w`, then after zero-padding `w` to length `#a`, the padded sequences are identical — no divergence exists. The subtraction `a ⊖ w` yields the zero tumbler of length `max(#a, #w) = #a`. For `b ⊖ w`: since `b > a > w` and `#b > #a ≥ #w`, `b` agrees with `w` (hence with `a`) on positions `1, ..., #a`. Beyond `#a`, `b` has components that `a` lacks. The result `b ⊖ w` has length `max(#b, #w) = #b > #a`. The zero tumbler `a ⊖ w` of length `#a` is a proper prefix of the zero tumbler of length `#b` (if `b ⊖ w` is all zeros), giving `a ⊖ w < b ⊖ w` by T1 case (ii). If `b ⊖ w` has any positive component, then `a ⊖ w` (all zeros) is less than `b ⊖ w` by TA6. In either case, `a ⊖ w ≤ b ⊖ w`. The sub-case is resolved.

*Case 0a: `a < b` by component divergence and `a` zero-padded-equal to `w`.* There exists `j ≤ min(#a, #b)` with `aⱼ < bⱼ`. Since `a` and `w` agree at every position under zero-padding, `a ⊖ w` is the zero tumbler of length `max(#a, #w)`. At position `j`, `wⱼ = aⱼ` (from zero-padded equality), so `bⱼ > aⱼ = wⱼ`. The pair `(b, w)` diverges at or before `j`, making `b ⊖ w` positive. By TA6, `a ⊖ w < b ⊖ w`.

For the remaining cases, `a < b` by T1 case (i) and `a` is not zero-padded-equal to `w`, so `dₐ = divergence(a, w)` is well-defined. Let `d_b = divergence(b, w)` (under zero-padding).

*Case 1: `dₐ = d_b = d`.* For `i < d`, both results are zero. At position `d`, we need `j ≥ d` (since `a` and `b` agree with `w` before `d`). If `j = d`: `a_d - w_d < b_d - w_d`, so `a ⊖ w < b ⊖ w`. If `j > d`: `a_d = b_d`, so both results agree at `d`; at positions `d < i < j`, both copy from their respective minuends which agree; at position `j`, `aⱼ < bⱼ`. So `a ⊖ w < b ⊖ w`.

*Case 2: `dₐ < d_b`.* At position `dₐ`: `a_{dₐ} ≠ w_{dₐ}` but `b_{dₐ} = w_{dₐ}`. Since `a < b` and they agree with `w` before `dₐ`, we have `j = dₐ` with `a_{dₐ} < b_{dₐ} = w_{dₐ}`. But `a ≥ w` requires `a_{dₐ} ≥ w_{dₐ}` at the divergence — contradiction. This case is impossible under the preconditions.

*Case 3: `dₐ > d_b`.* At position `d_b`: `b_{d_b} ≠ w_{d_b}` but `a_{d_b} = w_{d_b}`. So `j = d_b` with `a_{d_b} = w_{d_b} < b_{d_b}`. The result `(a ⊖ w)_{d_b} = 0` and `(b ⊖ w)_{d_b} = b_{d_b} - w_{d_b} > 0`. So `a ⊖ w < b ⊖ w`. ∎

**Claim:** (TA3-strict). If `a < b`, `a ≥ w`, `b ≥ w`, and `#a = #b`, then `a ⊖ w < b ⊖ w`.

*Proof.* The equal-length precondition eliminates Case 0 entirely — two tumblers of the same length cannot be in a prefix relationship unless equal, and `a < b` rules out equality. Cases 0a and 1–3 remain, all of which produce strict inequality. ∎

*Formal Contract:*
- *Preconditions:* a ∈ T, b ∈ T, w ∈ T, a < b, a ≥ w, b ≥ w
- *Postconditions:* a ⊖ w ≤ b ⊖ w


### Verification of TA4

**Claim.** `(a ⊕ w) ⊖ w = a` under the full precondition: `k = #a`, `#w = k`, `(A i : 1 ≤ i < k : aᵢ = 0)`.

*Proof.* Let `k` be the action point of `w`. Since `k = #a`, the addition `a ⊕ w` produces a result `r` with: `rᵢ = aᵢ = 0` for `i < k` (by the zero-prefix condition), `rₖ = aₖ + wₖ`, and `rᵢ = wᵢ` for `i > k`. Crucially, there are no components of `a` beyond position `k` — the tail replacement discards nothing. By the result-length identity, `#r = #w = k`, so `r = [0, ..., 0, aₖ + wₖ]`.

Now subtract `w` from `r`. The subtraction scans for the first divergence between `r` and `w`. For `i < k`: `rᵢ = 0 = wᵢ` (both are zero — `aᵢ` by the zero-prefix precondition, `wᵢ` by definition of action point). Two sub-cases arise at position `k`.

*Sub-case (i): `aₖ > 0`.* Then `rₖ = aₖ + wₖ > wₖ`, and the first divergence is at position `k`. The subtraction produces: positions `i < k` get zero, position `k` gets `rₖ - wₖ = aₖ`, and positions `i > k` copy from `r`, giving `rᵢ = wᵢ`. Since `k = #a` and `#w = k`, there are no trailing components. The result is `[0, ..., 0, aₖ] = a`. For valid addresses, T4's positive-component constraint guarantees `aₖ > 0`, so this sub-case always applies in the address context.

*Sub-case (ii): `aₖ = 0`.* Then `a` is a zero tumbler. The addition gives `rₖ = wₖ`. Since `#r = #w` (result-length identity) and `#w = k` (precondition), we have `r = w`. The subtraction `w ⊖ w` yields the zero tumbler of length `k`, which is `a`. ∎


### Cancellation properties of ⊕

TumblerAdd's constructive definition determines each component of the result from exactly one input. This makes the operation left-cancellative.

**TA-LC (LeftCancellation).** If a ⊕ x = a ⊕ y with both sides well-defined (TA0 satisfied for both), then x = y.

*Proof.* Let k₁ and k₂ be the action points of x and y. If k₁ < k₂, then (a ⊕ x)_{k₁} = a_{k₁} + x_{k₁} while (a ⊕ y)_{k₁} = a_{k₁} (position k₁ falls in the "copy from start" range of y). Equality gives x_{k₁} = 0, contradicting k₁ being the action point of x. Symmetrically k₂ < k₁ is impossible. So k₁ = k₂ = k.

At position k: a_k + x_k = a_k + y_k gives x_k = y_k. For i > k: x_i = (a ⊕ x)_i = (a ⊕ y)_i = y_i. For i < k: x_i = 0 = y_i. It remains to establish #x = #y. By T3, a ⊕ x = a ⊕ y implies #(a ⊕ x) = #(a ⊕ y). From TumblerAdd's result-length formula, #(a ⊕ w) = max(k − 1, 0) + (#w − k + 1) for any w with action point k. Since both x and y share the same action point k, we get #x = #y. By T3 (same length, same components), x = y.  ∎

TumblerAdd is *left-cancellative*: the start position can be "divided out" from equal results, recovering the displacement uniquely. This is a direct consequence of TumblerAdd's constructive definition — each component of the result is determined by exactly one input, so equality of results propagates back to equality of inputs.

*Worked example.* Let a = [2, 5] and suppose a ⊕ x = a ⊕ y = [2, 8]. We recover x and y uniquely. First, the action points must agree: if k_x = 1, then (a ⊕ x)₁ = a₁ + x₁ = 2 + x₁ = 2, giving x₁ = 0, which contradicts k_x = 1. So k_x = 2, and by the same argument k_y = 2. At position k = 2: a₂ + x₂ = 5 + x₂ = 8 gives x₂ = 3, and a₂ + y₂ = 5 + y₂ = 8 gives y₂ = 3. For i < k: x₁ = 0 = y₁. From the result-length formula with k = 2: #(a ⊕ x) = max(1, 0) + (#x − 1) = #x, so #x = 2 = #y. By T3, x = y = [0, 3].


### Right cancellation and the many-to-one property

The converse — right cancellation — does not hold. TumblerAdd's many-to-one property (noted informally in the definition of TumblerAdd above) means distinct starts can produce the same result under the same displacement.

**TA-RC (RightCancellationFailure).** There exist tumblers a, b, w with a ≠ b and a ⊕ w = b ⊕ w (both sides well-defined).

*Proof by example.* Let a = [1, 3, 5], b = [1, 3, 7], and w = [0, 2, 4] (action point k = 2). Then:

  a ⊕ w = [1, 3 + 2, 4] = [1, 5, 4]
  b ⊕ w = [1, 3 + 2, 4] = [1, 5, 4]  (component 3 of b is discarded — tail replacement)

So a ⊕ w = b ⊕ w = [1, 5, 4] despite a ≠ b — the difference at position 3 is erased by tail replacement.  ∎

The mechanism is TumblerAdd's tail replacement: components of the start position after the action point are discarded and replaced by the displacement's tail. Any two starts that agree on components 1..k and differ only on components after k will produce the same result under any displacement with action point k. Formally:

**TA-MTO (ManyToOne).** For any displacement w with action point k and any tumblers a, b with #a ≥ k and #b ≥ k: a ⊕ w = b ⊕ w if and only if a_i = b_i for all 1 ≤ i ≤ k.

*Proof (forward).* Assume a_i = b_i for all 1 ≤ i ≤ k. From TumblerAdd's definition: for i < k, (a ⊕ w)_i = a_i = b_i = (b ⊕ w)_i. At i = k, (a ⊕ w)_k = a_k + w_k = b_k + w_k = (b ⊕ w)_k. For i > k, (a ⊕ w)_i = w_i = (b ⊕ w)_i. The results have the same length (max(k − 1, 0) + (#w − k + 1) depends only on k and #w). By T3, a ⊕ w = b ⊕ w.  ∎

*Proof (converse).* Suppose a ⊕ w = b ⊕ w. Let k be the action point of w. We must show a_i = b_i for all 1 ≤ i ≤ k.

(a) For i < k: position i falls in the "copy from start" region of TumblerAdd, so (a ⊕ w)_i = a_i and (b ⊕ w)_i = b_i. From a ⊕ w = b ⊕ w we get a_i = b_i.

(b) At i = k: (a ⊕ w)_k = a_k + w_k and (b ⊕ w)_k = b_k + w_k. Equality gives a_k + w_k = b_k + w_k, hence a_k = b_k by cancellation in ℕ.

Components after k are unconstrained: for i > k, (a ⊕ w)_i = w_i = (b ⊕ w)_i regardless of a_i and b_i.  ∎

This gives a precise characterization of the equivalence classes: *a and b produce the same result under w if and only if they agree on the first k components, where k is the action point of w.*


### Displacement identities

Given two positions a and b on the tumbler line, a natural question is whether b ⊖ a yields a displacement w such that a ⊕ w faithfully recovers b. We establish the well-definedness condition for such displacement recovery and the round-trip identity that guarantees faithfulness.

From TumblerAdd, a ⊕ w acts at the action point k of w: it copies a₁..aₖ₋₁, advances aₖ by wₖ, and replaces the tail with w's tail. So if a ⊕ w = b, then a and b agree on components 1..k−1 and diverge at k, with bₖ = aₖ + wₖ and bᵢ = wᵢ for i > k. Reading off the width:

  wᵢ = 0  for i < k,    wₖ = bₖ − aₖ,    wᵢ = bᵢ  for i > k

where k = divergence(a, b). This is exactly the formula for b ⊖ a from TumblerSub. We write w = b ⊖ a and call it the *displacement from a to b*. The displacement is well-defined when:

**D0 (DisplacementWellDefined).** a < b, and the divergence k of a and b satisfies k ≤ #a.

D0 ensures the displacement b ⊖ a is a well-defined positive tumbler, and that a ⊕ (b ⊖ a) is defined (TA0 satisfied, since the displacement is positive and its action point k ≤ #a). Round-trip faithfulness additionally requires #a ≤ #b. The displacement w = b ⊖ a has length max(#a, #b), and the result a ⊕ w has length #w (by the result-length identity from TumblerAdd). When #a > #b, #w = #a > #b, so the result cannot equal b (by T3). When #a ≤ #b, #w = #b, giving the correct result length; combined with the component-by-component argument at the action point (k ≤ #a for arithmetic, #w = #b for length), this establishes a ⊕ w = b (D1 below).

When a is a proper prefix of b (divergence type (ii)), the divergence is #a + 1, exceeding #a, and D0 is not satisfied — no valid displacement exists.

*Proof.* Let `k = divergence(a, b)`. Since `a < b` with `k ≤ #a`, the Divergence definition places us in case (i): `k ≤ min(#a, #b)`, `aₖ < bₖ`, and `aᵢ = bᵢ` for all `i < k`. (Case (ii) — `a` a proper prefix of `b` — gives `k = #a + 1 > #a`, violating D0's hypothesis, so it does not arise.)

Since `a < b` entails `b ≥ a`, the subtraction `w = b ⊖ a` is a well-defined tumbler in `T` by TA2. By TumblerSub, the first divergence between `b` and `a` (minuend and subtrahend) is at position `k` — they agree at all prior positions since `bᵢ = aᵢ` for `i < k`, and `bₖ ≠ aₖ` by definition of `k`. The subtraction yields: `wᵢ = 0` for `i < k`, `wₖ = bₖ − aₖ`, and `wᵢ = bᵢ` for `i > k`, with `#w = max(#b, #a)`.

The displacement is positive: `wₖ = bₖ − aₖ > 0` since `aₖ < bₖ`. The action point of `w` is `k`, since every component before position `k` is zero and `wₖ > 0`. The hypothesis `k ≤ #a` satisfies TA0's precondition, so the addition `a ⊕ w` is a well-defined tumbler in `T`.

Finally, the displacement length `#w = max(#a, #b)` determines the result length: by the result-length identity (TumblerAdd), `#(a ⊕ w) = #w`. When `#a > #b`, this gives `#(a ⊕ w) = #a > #b`, so `a ⊕ w ≠ b` by T3 — the round-trip fails on length alone. Round-trip faithfulness requires the additional condition `#a ≤ #b`, under which `#w = #b` and the component-by-component recovery succeeds (D1).  ∎

*Formal Contract:*
- *Preconditions:* a ∈ T, b ∈ T, a < b, divergence(a, b) ≤ #a
- *Postconditions:* b ⊖ a ∈ T, b ⊖ a > 0, actionPoint(b ⊖ a) = divergence(a, b), a ⊕ (b ⊖ a) ∈ T

**D1 (DisplacementRoundTrip).** For tumblers a, b ∈ T with a < b, divergence(a, b) ≤ #a, and #a ≤ #b:

  a ⊕ (b ⊖ a) = b

*Proof.* Let k = divergence(a, b). By hypothesis k ≤ #a ≤ #b, so this is type (i) divergence with aₖ < bₖ. Define w = b ⊖ a by TumblerSub: wᵢ = 0 for i < k, wₖ = bₖ − aₖ, wᵢ = bᵢ for i > k. The result has length max(#a, #b) = #b. Now w > 0 since wₖ > 0, and the action point of w is k ≤ #a, so TA0 is satisfied. Applying TumblerAdd: (a ⊕ w)ᵢ = aᵢ = bᵢ for i < k (before divergence), (a ⊕ w)ₖ = aₖ + (bₖ − aₖ) = bₖ, and (a ⊕ w)ᵢ = wᵢ = bᵢ for i > k. The result has length #w = #b; every component matches b, so a ⊕ w = b by T3.  ∎

**D2 (DisplacementUnique).** Under D1's preconditions (a < b, divergence(a, b) ≤ #a, #a ≤ #b), if a ⊕ w = b then w = b ⊖ a.

*Proof.* By D1, a ⊕ (b ⊖ a) = b. So a ⊕ w = a ⊕ (b ⊖ a), and by TA-LC, w = b ⊖ a.  ∎

D1 and D2 together characterize the displacement completely: D1 says b ⊖ a recovers b, D2 says nothing else does.

When a = b, no displacement is needed; the degenerate case is handled separately since b ⊖ a produces the zero tumbler and a ⊕ (b ⊖ a) is not well-formed (TA0 requires w > 0). D0 ensures the displacement is well-defined; D1 ensures the round-trip is faithful when additionally #a ≤ #b.

*Worked example.* Consider a = [1, 2, 3] and b = [1, 5, 1]. We have #a = #b = 3.

*D0 check.* divergence(a, b) = 2, since a₁ = b₁ = 1 and a₂ = 2 ≠ 5 = b₂. The condition k = 2 ≤ #a = 3 is satisfied.

*Displacement.* By TumblerSub, w = b ⊖ a: w₁ = 0 (i < k), w₂ = 5 − 2 = 3 (i = k), w₃ = 1 (i > k, from b). So w = [0, 3, 1].

*Round-trip.* The action point of w is 2. By TumblerAdd, a ⊕ [0, 3, 1]: position 1 copies a₁ = 1, position 2 computes 2 + 3 = 5, position 3 copies w₃ = 1. Result: [1, 5, 1] = b.  ✓

The generalization to #a < #b can be seen with a' = [1, 2] and the same b = [1, 5, 1]. Here #a' = 2 < 3 = #b, the divergence is still 2 (a'₂ = 2 ≠ 5 = b₂), and k = 2 ≤ #a' = 2 satisfies D0. TumblerSub (zero-padding a' to length 3) gives the same w = [0, 3, 1] of length 3. The round-trip a' ⊕ [0, 3, 1] produces [1, 5, 1] = b — the result has length #w = 3 = #b, matching the target.


### Ordinal displacement and shift

**Definition (OrdinalDisplacement).** For natural number n ≥ 1 and depth m ≥ 1, the *ordinal displacement* δ(n, m) is the tumbler [0, 0, ..., 0, n] of length m — zero at positions 1 through m − 1, and n at position m. Its action point is m.

When the depth is determined by context (typically m = #v for the tumbler being shifted), we write δₙ.

**Definition (OrdinalShift).** For a tumbler v of length m and natural number n ≥ 1:

`shift(v, n) = v ⊕ δ(n, m)`

TA0 is satisfied: the action point of δ(n, m) is m = #v, so k ≤ #v holds trivially. By TumblerAdd: shift(v, n)ᵢ = vᵢ for i < m, and shift(v, n)ₘ = vₘ + n. The shift advances the deepest component by exactly n, leaving all higher-level components unchanged.

Additionally, shift preserves structural properties. When m ≥ 2, the action point of δₙ leaves position 1 unchanged — shift(v, n)₁ = v₁. When m = 1, shift([S], n) = [S + n] changes the first component. Furthermore, #shift(v, n) = #δₙ = m = #v by the result-length identity of TumblerAdd. The shift preserves tumbler depth, and — since n ≥ 1 — component positivity: shift(v, n)ₘ = vₘ + n ≥ 1 unconditionally for all vₘ ≥ 0.

**TS1 (ShiftOrderPreservation).**

`(A v₁, v₂, n : n ≥ 1 ∧ #v₁ = #v₂ = m ∧ v₁ < v₂ : shift(v₁, n) < shift(v₂, n))`

*Derivation.* Fix n ≥ 1. Since #v₁ = #v₂ = m and v₁ ≠ v₂, the divergence point satisfies divergence(v₁, v₂) ≤ m. The action point of δₙ is m ≥ divergence(v₁, v₂). By TA1-strict: v₁ ⊕ δₙ < v₂ ⊕ δₙ. ∎

**TS2 (ShiftInjectivity).**

`(A v₁, v₂, n : n ≥ 1 ∧ #v₁ = #v₂ = m : shift(v₁, n) = shift(v₂, n) ⟹ v₁ = v₂)`

*Derivation.* Fix n ≥ 1. By TA-MTO: v₁ ⊕ δₙ = v₂ ⊕ δₙ iff (A i : 1 ≤ i ≤ m : v₁ᵢ = v₂ᵢ). The action point of δₙ is m, and agreement at positions 1..m for tumblers of length m means v₁ = v₂ by T3 (CanonicalRepresentation). ∎

**TS3 (ShiftComposition).**

`(A v, n₁, n₂ : n₁ ≥ 1 ∧ n₂ ≥ 1 ∧ #v = m : shift(shift(v, n₁), n₂) = shift(v, n₁ + n₂))`

*Derivation.* We expand both sides component-wise using TumblerAdd's constructive definition.

Left side: let u = shift(v, n₁) = v ⊕ δ(n₁, m). By TumblerAdd, uᵢ = vᵢ for i < m, uₘ = vₘ + n₁, and #u = m. Now shift(u, n₂) = u ⊕ δ(n₂, m). By TumblerAdd, the result has components uᵢ = vᵢ for i < m, and uₘ + n₂ = vₘ + n₁ + n₂ at position m. Length is m.

Right side: shift(v, n₁ + n₂) = v ⊕ δ(n₁ + n₂, m). By TumblerAdd, components are vᵢ for i < m, and vₘ + (n₁ + n₂) at position m. Length is m.

Both sides have length m and agree at every component (natural-number addition is associative: vₘ + n₁ + n₂ = vₘ + (n₁ + n₂)). By T3: they are equal. ∎

**TS4 (ShiftStrictIncrease).**

`(A v, n : n ≥ 1 ∧ #v = m : shift(v, n) > v)`

*Derivation.* δ(n, m) > 0 since its m-th component is n ≥ 1. By TA-strict: v ⊕ δ(n, m) > v. ∎

**TS5 (ShiftAmountMonotonicity).**

`(A v, n₁, n₂ : n₁ ≥ 1 ∧ n₂ > n₁ ∧ #v = m : shift(v, n₁) < shift(v, n₂))`

*Derivation.* Write n₂ = n₁ + (n₂ − n₁) where n₂ − n₁ ≥ 1. By TS3: shift(v, n₂) = shift(shift(v, n₁), n₂ − n₁). By TS4: shift(shift(v, n₁), n₂ − n₁) > shift(v, n₁). ∎

*Worked example.* Let v = [2, 3, 7] (m = 3) and n = 4. Then δ(4, 3) = [0, 0, 4] with action point 3. TA0: k = 3 ≤ 3 = #v. By TumblerAdd: shift(v, 4) = [2, 3, 7 + 4] = [2, 3, 11].

For TS1: take v₁ = [2, 3, 5] < v₂ = [2, 3, 9] with n = 4. Then shift(v₁, 4) = [2, 3, 9] < [2, 3, 13] = shift(v₂, 4). ✓

For TS3: shift(shift([2, 3, 7], 4), 3) = shift([2, 3, 11], 3) = [2, 3, 14] = shift([2, 3, 7], 7). ✓


## Increment for allocation

A separate operation, distinct from the shifting arithmetic, handles address allocation. When the system allocates a new address, it takes the highest existing address in a partition and produces the next one. This is not addition of a width; it is advancement of a counter at a specified hierarchical level.

We define the *last significant position* of a tumbler `t`. When `t` has at least one nonzero component, `sig(t) = max({i : 1 ≤ i ≤ #t ∧ tᵢ ≠ 0})` — the position of the last nonzero component. When every component is zero, `sig(t) = #t`.

For valid addresses, `sig(t)` falls within the last populated field. This is a consequence of T4's positive-component constraint: every field component is strictly positive, so the last component of the last field is nonzero, and `sig(t) = #t`. Therefore `inc(t, 0)` on a valid address increments the last component of the last field, modifying only within that field and preserving the hierarchical structure.

**TA5 (Hierarchical increment).** For tumbler `t ∈ T` and level `k ≥ 0`, there exists an operation `inc(t, k)` producing tumbler `t'` such that:

  (a) `t' > t` (strictly greater under T1),

  (b) `t'` agrees with `t` on all components before the increment point,

  (c) when `k = 0` (*sibling*): `#t' = #t`, and `t'` differs from `t` only at position `sig(t)`, where `t'_{sig(t)} = t_{sig(t)} + 1`,

  (d) when `k > 0` (*child*): `#t' = #t + k`, the `k - 1` intermediate positions `#t + 1, ..., #t + k - 1` are set to `0` (field separators), and the final position `#t + k` is set to `1` (the first child).

We verify `inc(t, k) > t` for both cases. For `k = 0`: `t'` agrees with `t` on positions `1, ..., sig(t) - 1` and exceeds `t` at position `sig(t)`, so `t' > t` by T1 case (i). For `k > 0`: `t'` agrees with `t` on positions `1, ..., #t`, and `#t' > #t`, so `t` is a proper prefix of `t'`, giving `t < t'` by T1 case (ii).

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

*Proof (from T1, T4).* **Conjunct 1** (invalidity): Let `t` be a zero tumbler. Then `t₁ = 0`. T4 requires that a valid address does not begin with zero — the first component must be a positive node-field component. Since `t₁ = 0`, `t` fails T4 and is not a valid address.

**Conjunct 2** (ordering): Let `s` be a zero tumbler of length `m` and `t` a positive tumbler of length `n`. Since `t` is positive, there exists a first nonzero component; let `k = min({i : 1 ≤ i ≤ n : tᵢ > 0})`. For all `i < k`, `tᵢ = 0` (by minimality of `k`).

*Case 1* (`m ≥ k`): At positions `1, ..., k − 1`, `sᵢ = 0 = tᵢ` — no disagreement. At position `k`, `sₖ = 0 < tₖ`. By T1 case (i), `s < t`.

*Case 2* (`m < k`): For all `i ≤ m`, `sᵢ = 0 = tᵢ` (since `i ≤ m < k` and `tᵢ = 0` for `i < k`). The tumblers agree on every position of `s`, and `#s = m < k ≤ n = #t`, so `s` is a proper prefix of `t`. By T1 case (ii), `s < t`. ∎

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

Both operations produce results in T, and the subspace identifier — held as context — is never modified. The core guarantee is subspace closure: arithmetic on ordinals cannot escape the subspace.

For `⊕`, a stronger result holds: components before the action point are preserved positive from `o ∈ S`, and `oₖ + wₖ > 0` since both are positive. When all components of `w` after `k` are also positive, the result is in S. For single-component ordinals (the common case), `[x] ⊕ [n] = [x + n] ∈ S` unconditionally.

The subspace identifier is context — it determines which positions are subject to the shift — not an operand to the arithmetic. Both operations produce genuine shifts in the ordinal-only view; the 2-component view gives a genuine shift for `⊕` but a vacuous closure for `⊖`. The ordinal-only formulation is adopted because applying `⊖` to full 2-component positions finds the divergence at the subspace identifier, producing a no-op rather than a genuine shift.

For single-component ordinals, `⊖` gives closure in S ∪ Z: `[x] ⊖ [n]` is `[x - n] ∈ S` when `x > n`, or `[0] ∈ Z` when `x = n` (a sentinel, TA6). When the element field has deeper structure (`δ > 1` in T4), the ordinal `o` has multiple components. A displacement with action point `k ≥ 2` preserves all ordinal components before position `k` — the constructive definition copies `o₁, ..., oₖ₋₁` from the start position unchanged. For example, spanning from ordinal `[1, 3, 2]` to `[1, 5, 7]` requires displacement `[0, 2, 7]` (action point `k = 2`); `[1, 3, 2] ⊕ [0, 2, 7] = [1, 5, 7]` — position 1 of the ordinal is copied, preserving the ordinal prefix. The subspace closure holds in all cases because the subspace identifier is never an operand.

**Verification of TA7a.** In the ordinal-only formulation, the shift operates on `o = [o₁, ..., oₘ]` with all `oᵢ > 0` (since `o ∈ S`), by displacement `w` with action point `k` satisfying `1 ≤ k ≤ m`.

*For `⊕`:* By the constructive definition, `(o ⊕ w)ᵢ = oᵢ` for `i < k` (positive, preserved from `o`), and `(o ⊕ w)ₖ = oₖ + wₖ > 0` (both positive). Components after `k` come from `w`. The result has length `#w` (by the result-length identity). The result is in T; it is in S when additionally all components of `w` after `k` are positive. The subspace identifier, held as context, is unchanged.

*For `⊖`:* We analyze by action point. When `#w > m`, TumblerSub produces a result of length `max(m, #w) = #w > m` with trailing zeros at positions `m + 1` through `#w` (from the zero-padded minuend); this result lies in T \ S. The S-membership claims below assume the typical case `#w ≤ m`.

*Case `k ≥ 2`:* The displacement has `wᵢ = 0` for `i < k`. Since `o ∈ S`, `o₁ > 0`. The divergence falls at position 1 (where `o₁ > 0 = w₁`). TumblerSub produces: `r₁ = o₁ - 0 = o₁`, and `rᵢ = oᵢ` for `1 < i ≤ m` (copied from the minuend since `i > d = 1`). When `#w ≤ m`, the result has length `m` and equals `o` itself — a no-op; the result is trivially in S. The subtraction finds the mismatch at the ordinal's first positive component rather than at the displacement's intended action point.

*Case `k = 1`:* The displacement has `w₁ > 0`. Let `d = divergence(o, w)`. If `d = 1` (i.e., `o₁ ≠ w₁`): since `o ≥ w`, `o₁ > w₁`. TumblerSub yields `r₁ = o₁ - w₁ > 0` and `rᵢ = oᵢ > 0` for `1 < i ≤ m`. When `#w ≤ m`, all components are positive and the result is in S. If `d > 1` (i.e., `o₁ = w₁`, divergence later): TumblerSub zeros positions before `d`, giving `r₁ = 0`. The result has a zero first component and is not in S. Counterexample: `o = [5, 3]`, `w = [5, 1]` (action point `k = 1`, divergence `d = 2`). Result: `[0, 2] ∈ T` but `[0, 2] ∉ S ∪ Z`. This sub-case arises when `o` and `w` share a leading prefix — the subtraction produces a displacement with leading zeros rather than a valid ordinal position.

In all cases the subspace identifier, held as context, is never modified. TA7a holds. ∎

The restriction to element-local displacements is necessary. An unrestricted displacement whose action point falls at the subspace-identifier position could produce an address in a different subspace — TA7a cannot hold for arbitrary `w`.


## What tumbler arithmetic is NOT

We must state explicitly what the tumbler algebra does not guarantee. These negative results constrain what an implementer may assume.

**The algebra is not a group.** There is no additive identity — the zero tumbler is a sentinel, not a neutral element for addition. There is no additive inverse for every element — subtraction is only defined when `a ≥ w`. The algebra is not closed under subtraction in general.

**TA-assoc (AdditionAssociative).** Addition is associative where both compositions are defined: `(a ⊕ b) ⊕ c = a ⊕ (b ⊕ c)` whenever both sides are well-defined. Three cases exhaust the possibilities. Let `k_b` and `k_c` be the action points of `b` and `c` respectively. When `k_b < k_c`: both sides produce `aᵢ` for `i < k_b`, `aₖ_b + bₖ_b` at `k_b`, `bᵢ` for `k_b < i < k_c`, `bₖ_c + cₖ_c` at `k_c`, and `cᵢ` beyond — identical. When `k_b = k_c = k`: both sides produce `aₖ + bₖ + cₖ` at `k` (natural-number addition is associative) and `cᵢ` beyond — identical. When `k_b > k_c`: both sides produce `aₖ_c + cₖ_c` at `k_c` and `cᵢ` beyond — identical (the deeper displacement `b` is overwritten by the shallower `c` in both cases). The domain conditions are asymmetric — the left side requires `k_b ≤ #a`, while the right requires only `min(k_b, k_c) ≤ #a` — but on the intersection, the values agree.

The design does not depend on associativity. Shifts are applied as single operations in practice, never composed from multiple smaller shifts. An implementation with finite representations may break associativity through overflow at the action-point component, but the abstract algebra carries no such limitation.

**Addition is not commutative.** We do NOT require `a ⊕ b = b ⊕ a`. The operands play asymmetric roles: the first is a *position*, the second is a *displacement*. Swapping them is semantically meaningless. Gregory's `absadd` confirms: the first argument supplies the prefix, the second the suffix — the reverse call gives a different (and typically wrong) result.

**There is no multiplication or division.** Gregory's analysis of the complete codebase confirms: no `tumblermult`, no `tumblerdiv`, no scaling operation of any kind. The arithmetic repertoire is: add, subtract, increment, compare. Tumblers are *addresses*, not quantities. You don't multiply two file paths or divide an address by three.

**Tumbler differences are not counts.** Nelson is emphatic: "A tumbler-span is not a conventional number, and it does not designate the number of bytes contained. It does not designate a number of anything." The difference between two addresses specifies *boundaries*, not *cardinality*. What lies between those boundaries depends on the actual population of the tree, which is dynamic and unpredictable. Between sibling addresses 3 and 7, document 5 might have arbitrarily many descendants — the span from 3 to 7 encompasses all of them, and their count is unknowable from the addresses alone. The arithmetic is an *addressing calculus*, not a *counting calculus*.

The absence of algebraic structure beyond a monotone shift is not a deficiency. It is the *minimum* that addressing requires. An ordered set with an order-preserving shift and an allocation increment is sufficient. Anything more would be unused machinery and unverified obligation.


## Spans

A span is a pair `(s, ℓ)` where `s ∈ T` is a start address and `ℓ ∈ T` is a length (a positive tumbler used as a displacement), denoting the contiguous range from `s` up to but not including `s ⊕ ℓ`. The form of `ℓ` depends on the hierarchical level at which the span operates, because the action point of `ℓ` must match the level of the start address `s`.

Nelson makes spans self-describing at every hierarchical level: "A digit of 'one' may be used to designate all of a given version, all versions of a given document, all works of a given author, all documents in a given project, all documents on a given server — or the entire docuverse." The "1-position convention" exploits T5: because subtrees are contiguous, a span whose start is a high-level prefix and whose length reaches to the next sibling captures exactly that subtree's content.

And a span may be empty — populated by nothing at present — yet valid: "A span that contains nothing today may at a later time contain a million documents." The range is determined by the endpoints; what is actually stored within that range is a question about the current state of the system, not about the tumbler algebra.

**T12 (Span well-definedness).** A span `(s, ℓ)` is well-formed when `ℓ > 0` and the action point `k` of `ℓ` satisfies `k ≤ #s` (the TA0 precondition for `s ⊕ ℓ`). Equivalently, the number of leading zeros in `ℓ` must be strictly less than `#s`. A well-formed span denotes the set `{t ∈ T : s ≤ t < s ⊕ ℓ}`. This set is contiguous under T1 — there is no tumbler between two members that is not itself a member.

Contiguity is definitional: the span is an interval `[s, s ⊕ ℓ)` in a totally ordered set, and intervals in total orders are contiguous. Non-emptiness follows from TA-strict: since `ℓ > 0` and `k ≤ #s`, TA0 gives `s ⊕ ℓ ∈ T`, and TA-strict gives `s ⊕ ℓ > s` directly. The interval `[s, s ⊕ ℓ)` is therefore non-empty — it contains at least `s` itself.

We reserve T5 for the distinct claim that *prefix-defined* sets are contiguous — a non-trivial property of the lexicographic order.


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
| T0(a) | Every component value of a tumbler is unbounded — no maximum value exists | introduced |
| T0(b) | Tumblers of arbitrary length exist in T — the hierarchy has unlimited nesting depth | introduced |
| T1 | Tumblers are totally ordered by lexicographic comparison, with the prefix-less-than convention | introduced |
| T2 | Tumbler comparison is computable from the two addresses alone, examining at most min(#a, #b) components | introduced |
| T3 | Each tumbler has exactly one canonical representation; component-wise identity is both necessary and sufficient for equality | introduced |
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
| TA-assoc | Addition is associative where both compositions are defined: (a ⊕ b) ⊕ c = a ⊕ (b ⊕ c) | introduced |
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

