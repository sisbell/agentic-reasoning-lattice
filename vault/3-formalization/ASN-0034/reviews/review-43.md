# Cone Review — ASN-0034/GlobalUniqueness (cycle 8)

*2026-04-14 08:39*

Looking at this ASN as a complete system, checking every definition, precondition chain, and case analysis against the previous findings.

### T10a permits duplicate child-spawning from the same domain element, producing a counterexample to GlobalUniqueness that escapes all five cases

**Foundation**: (internal consistency — T10a axiom strength vs. GlobalUniqueness proof requirements)

**ASN**: T10a axiom: *"To spawn a child allocator, the parent performs one `inc(·, k')` with `k' ∈ {1, 2}`... to establish the child's prefix, then delegates further allocation to the child."* GlobalUniqueness Case 5: *"Let A₁ and A₂ be two non-root allocators with domain prefixes p₁ and p₂ where p₁ ≼ p₂ and p₁ ≠ p₂."* Exhaustiveness: *"if nesting, the addresses have different zero counts (Case 4) or the same zero count (Case 5)."*

**Issue**: T10a does not constrain a parent allocator from invoking `inc(t, k')` on the same domain element `t` with the same `k'` more than once. Since `inc` is deterministic, two such invocations produce the identical base address `inc(t, k')`, spawning two child allocators whose domains are identical sequences — same base, same `inc(·, 0)` chain, same address values at every index. These are distinct allocation events producing the same address values, a direct counterexample to GlobalUniqueness under T10a as stated.

The proof's five-case partition cannot route the resulting pairs. The two children have identical domain prefixes (`p₁ = p₂ = t`), identical spawning parameters (`k'₁ = k'₂`), and identical output zero counts. Case 1 requires same producing allocator — these are different allocators (created by different events). Case 3 requires non-nesting prefixes — identical prefixes satisfy both `p₁ ≼ p₂` and `p₂ ≼ p₁`, so the non-nesting condition `p₁ ⋠ p₂ ∧ p₂ ⋠ p₁` fails. Case 4 requires `zeros(a) ≠ zeros(b)` — same k' from same prefix gives same zero count. Case 5 explicitly assumes `p₁ ≠ p₂`. No case accepts the pair. The `p₁ = p₂` subcase with *different* k' values is handled correctly — `k'₁ ≠ k'₂` yields different output zero counts, routing to Case 4 — so only the same-element same-k' duplicate is unhandled.

**What needs resolving**: T10a must incorporate a uniqueness constraint ensuring each `(parent_domain_element, k')` pair produces at most one child-spawning event, so that the duplicate scenario is axiomatically excluded. Under this constraint, `p₁ = p₂` forces `k'₁ ≠ k'₂`, guaranteeing different output zero counts and routing to Case 4; the exhaustiveness paragraph should then explicitly address why identical-prefix same-k' pairs cannot arise.
