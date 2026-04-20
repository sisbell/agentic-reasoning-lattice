**T0(b) (UnboundedLength).** `(A n ∈ ℕ : n ≥ 1 : (E t ∈ T :: #t ≥ n))`.

In words: there is no maximum tumbler length — for every bound, a tumbler of at least that length exists in T. The hierarchy has unlimited nesting depth. T0(b) follows from T's definition as the set of all finite sequences over ℕ — for any `n`, the constant sequence `[1, 1, ..., 1]` of length `n` is a member. We state it explicitly because it carries independent architectural weight: T0(a) ensures siblings within a level are inexhaustible, while T0(b) ensures levels themselves are inexhaustible.

*Proof.* We establish the universal claim by exhibiting, for arbitrary `n ≥ 1`, a witness `t ∈ T` with `#t ≥ n`.

Let `n ∈ ℕ` with `n ≥ 1` be arbitrary. Define

> `t = 1.1. ... .1` (n components)

— the constant sequence of `n` ones, that is, `t = d₁.d₂. ... .dₙ` with `dᵢ = 1` for all `1 ≤ i ≤ n`. We must verify two things.

*(i)* `t ∈ T`. The sequence `t` has length `n ≥ 1`, and each of its components is a natural number: `dᵢ = 1 ∈ ℕ` for all `1 ≤ i ≤ n`. Since T is the set of all finite sequences over ℕ with length ≥ 1, we have `t ∈ T`.

*(ii)* `#t ≥ n`. By construction `t` has exactly `n` components, so `#t = n`, and `n ≥ n` holds.

Since `n` was arbitrary, the universal claim holds. ∎

*Formal Contract:*
- *Postcondition:* For every `n ∈ ℕ` with `n ≥ 1`, there exists `t ∈ T` with `#t ≥ n`.
- *Depends:* T0 (CarrierSetDefinition) — step (i) invokes T0's carrier characterisation — that T is the set of all finite sequences over ℕ with length ≥ 1 — to conclude `t ∈ T` from `t` being the length-`n` constant sequence of ones, with `n ≥ 1` satisfying the length constraint and each component `dᵢ = 1 ∈ ℕ` satisfying the component-type constraint; and the length operator `#·` used in step (ii) to state `#t = n` and in the postcondition's `#t ≥ n` is the primitive that T0 introduces.

T0 is what separates the tumbler design from fixed-width addressing. Nelson: "New items may be continually inserted in tumbler-space while the other addresses remain valid." The word "continually" carries the weight — it means the process of creating new addresses never terminates. Between any two sibling addresses, the forking mechanism can always create children: "One digit can become several by a forking or branching process. This consists of creating successive new digits to the right." Each daughter can have daughters without limit, and each digit is itself unbounded.

The address space is unbounded in two dimensions: T0(a) ensures each component is unbounded (unlimited siblings at any level) and T0(b) ensures the number of components is unbounded (unlimited nesting depth). Together they make the address space infinite in both dimensions, which Nelson calls "finite but unlimited" — at any moment finitely many addresses exist, but there is no bound on how many can be created: "A span that contains nothing today may at a later time contain a million documents."

We observe that Gregory's implementation uses a fixed 16-digit mantissa of 32-bit unsigned integers, giving a large but finite representable range. When the allocation primitive `tumblerincrement` would exceed this range structurally (requiring a 17th digit), it detects the overflow and terminates fatally. The general addition routine `tumbleradd` silently wraps on digit-value overflow. Both behaviors violate T0. The abstract specification demands unbounded components; a correct implementation must either provide them or demonstrate that the reachable state space never exercises the bound. The comment `NPLACES 16 /* increased from 11 to support deeper version chains */` records that the original bound of 11 was concretely hit in practice — version chains deeper than 3–4 levels caused fatal crashes.
