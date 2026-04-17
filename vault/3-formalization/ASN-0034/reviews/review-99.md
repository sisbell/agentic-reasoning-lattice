# Cone Review — ASN-0034/T10a-N (cycle 4)

*2026-04-16 20:40*

### T10a-N Depends omits T0 despite using ℕ-successor strictness and ℕ-ordering
**Foundation**: N/A (internal)
**ASN**: T10a-N (AllocatorDisciplineNecessity), *Formal Contract* — `Depends` lists T10a, T10a.6, TA5, Prefix, T10. No T0.
**Issue**: The argument's load-bearing step converts TA5(d)'s equation `#t' = #t + k` (plus `k = 1`) into the strict length excess `#t₁ < #t₂`, and the Depends paragraph for TA5 paraphrases this outcome as "TA5(d) gives `#t₂ = #t₁ + 1 > #t₁`". The strict inequality `n + 1 > n` is a T0-level ℕ fact (successor strictness), not a clause of TA5. Likewise, the subsequent step "agreement on all `#t₁` positions and `#t₁ < #t₂` are precisely the conditions of the Prefix definition" silently weakens `#t₁ < #t₂` to `#t₁ ≤ #t₂` via T0's `≤`-definition (`m < n ⟹ m ≤ n`), matching exactly the kind of `≤`-unfolding that Prefix's Depends attributes to T0. Under the per-step citation convention the document establishes — T1, TA5, Prefix, and T10 each enumerate T0 for analogous uses of length comparison, successor, and `≤`-unfolding — T10a-N should cite T0 for these same steps but does not.
**What needs resolving**: Add T0 (CarrierSetDefinition) to T10a-N's Depends and tie it to the specific steps (successor strictness `#t₁ + 1 > #t₁`, the `<`-to-`≤` weakening feeding the Prefix precondition `#t₁ ≤ #t₂`), or justify a uniform exception that applies to T10a-N while T1/TA5/Prefix/T10 cite T0 explicitly for comparable steps.
