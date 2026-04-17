# Cone Review — ASN-0034/T10a-N (cycle 3)

*2026-04-16 20:38*

### T1 Case 2 uses T3's contrapositive without citing it
**Foundation**: N/A (internal)
**ASN**: T1 (LexicographicOrder), proof part (b) Trichotomy, Case 2 — "Since `aᵢ = bᵢ` for all `i < k` but `aₖ ≠ bₖ`, we have `a ≠ b`."
**Issue**: The step "differing components ⟹ tumblers unequal" is the *reverse direction* of T3 (component-level disagreement falsifies tumbler equality). T10's proof cites this same step explicitly ("by the reverse direction of T3 (tumblers that differ in any component are distinct), `a ≠ b`"), and T1's own Case 3 cites T3 for the analogous length-based inequality ("we have `a ≠ b` by T3 (distinct lengths)"). T1's Depends paragraph for T3 enumerates only Case 1 ("invokes T3 to conclude `a = b`") and Case 3 ("invokes its contrapositive to conclude `a ≠ b` from `m ≠ n`") — Case 2's invocation of the same contrapositive is omitted from both the prose and the per-step Depends list. The omission matters because `a ≠ b` is load-bearing in Case 2: without it, trichotomy's "exactly one" cannot rule out `a = b` as a third concurrent option alongside the produced witness for `a < b` (or `b < a`).
**What needs resolving**: Either cite T3 (its reverse / contrapositive) at the Case 2 step where component-level disagreement is converted to tumbler inequality, and extend the T3 entry in T1's Depends to enumerate Case 2 alongside Cases 1 and 3, or justify why this step may remain implicit in Case 2 while being explicit in Case 3 and in T10.
