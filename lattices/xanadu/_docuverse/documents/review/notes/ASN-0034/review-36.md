# Proof Verification: Divergence

Looking at the Divergence definition section against the checklist:

**1. Precondition completeness** — `a, b ∈ T`, `a ≠ b` are stated. Complete.

**2. Case coverage** — The two cases are mutually exclusive (case (i) requires a disagreement within the shared range; case (ii) requires full agreement) and exhaustive for `a ≠ b` (if no shared-position disagreement exists, T3 forces `#a ≠ #b` to avoid `a = b`). The uniqueness of `k` in case (i) follows from the universal agreement prefix `(A i : 1 ≤ i < k : aᵢ = bᵢ)` combined with `aₖ ≠ bₖ`. Sound.

**3–4. Postcondition / conjuncts** — The "exactly one case applies" claim is asserted with adequate informal justification via T1's case structure. Acceptable for a definition.

**5. Dependency correctness** — T1 is used (the two divergence cases mirror T1's two ordering cases). TA0 and TA1-strict are referenced in the motivating paragraph about unsatisfiability. These are correctly listed. T3 is used implicitly for exhaustiveness (same-length + all-components-equal ⟹ equal) but is available transitively through T1's proof.

**6. Formal contract** — The Divergence section has no `*Formal Contract:*` block. Every other property in the dependencies (T1, TA0, TA1, TA1-strict) has one. A definition should have at minimum:

```
*Formal Contract:*
- *Preconditions:* a ∈ T, b ∈ T, a ≠ b
- *Definition:* divergence(a, b) = k where (i) k = min({i : 1 ≤ i ≤ min(#a, #b) ∧ aᵢ ≠ bᵢ}) if such i exists, or (ii) k = min(#a, #b) + 1 otherwise
```

**7. Missing guarantees** — No external guarantees assumed beyond what dependencies provide.

```
RESULT: FOUND

**Problem**: The Divergence definition section has no `*Formal Contract:*` block. All other properties in the ASN (T1, TA0, TA1, TA1-strict) include one. Per the specification's own convention, each property section must end with a formal contract summarizing its interface.

**Required**: Append a formal contract to the Divergence definition, e.g.:

*Formal Contract:*
- *Preconditions:* a ∈ T, b ∈ T, a ≠ b
- *Definition:* divergence(a, b) = k, where (i) if ∃ i with 1 ≤ i ≤ min(#a, #b) and aᵢ ≠ bᵢ, then k = min({i : 1 ≤ i ≤ min(#a, #b) ∧ aᵢ ≠ bᵢ}); (ii) otherwise k = min(#a, #b) + 1
```
