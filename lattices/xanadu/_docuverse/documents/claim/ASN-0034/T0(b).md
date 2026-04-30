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
