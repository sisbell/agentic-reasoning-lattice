# Regional Review — ASN-0034/NAT-card (cycle 3)

*2026-04-24 02:00*

### T0's derivation of `0 < #a` is an unnecessary detour
**Class**: REVISE
**Foundation**: —
**ASN**: T0 prose: "NAT-order's `≤`-unfolding sends `1 ≤ #a` to `1 < #a ∨ 1 = #a`, and composition with NAT-closure's `0 < 1` via transitivity (strict branch) or substitution of `=` (equality branch) lifts to `0 < #a`, excluding `#a = 0`. The inequality `1 ≤ #a` is thus well-typed within ℕ and informative, and the index domain `{1, …, #a}` is never empty, so bounded quantifiers of the form `(Q i : 1 ≤ i ≤ #a : …)` range over a nonempty set rather than collapsing to vacuity."
**Issue**: The stated purpose is to show the index domain `{1, …, #a}` is nonempty. `1 ≤ #a` alone delivers this directly: reflexivity of `≤` (via `m = m` and the `m = n` branch of the definition) gives `1 ≤ 1`, so `1 ∈ {j ∈ ℕ : 1 ≤ j ≤ #a}` immediately. The detour through `0 < #a` adds nothing that the axiom `1 ≤ #a` did not already carry. It also introduces the literal `0` (and hence an implicit appeal to NAT-zero's `0 ∈ ℕ`) into T0's reasoning, but T0's Depends declares only NAT-closure and NAT-order — compare NAT-closure's and NAT-card's Depends slots, which both declare NAT-zero explicitly when they use `0`. The paragraph is reviser-drift: prose computing around the axiom rather than reading it.
**What needs resolving**: Either drop the `0 < #a` derivation (and with it the implicit NAT-zero use in T0's prose), grounding "index domain is never empty" directly on `1 ≤ #a` via reflexivity of `≤`; or, if the derivation is retained, declare NAT-zero in T0's Depends so the symbol `0` is grounded. Dropping is preferred — the nonemptiness claim the prose is justifying is immediate from the axiom.

### NAT-card disambiguation phrasing overstates the operator's domain
**Class**: OBSERVE
**Foundation**: —
**ASN**: NAT-card Axiom (trailing sentence): "`|·|` acts on subsets of ℕ and is distinct from T0's tumbler-length `#·`, which acts on sequences."
**Issue**: The formal contract restricts `|·|` to `S ⊆ {1, …, n}` for some `n ∈ ℕ`, which excludes any subset containing `0` (e.g. `|{0}|` is not defined by the postulate, since `0 ∉ {1, …, n}` for any `n`). The prose's "subsets of ℕ" is not literally false (every such `S` is a subset of ℕ) but suggests arbitrary subsets. The sentence's job is set-vs-sequence disambiguation, which a colloquial "subsets of ℕ" accomplishes, so this is loose phrasing rather than a grounding gap.
**What needs resolving**: — (OBSERVE)

VERDICT: REVISE
