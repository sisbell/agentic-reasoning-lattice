# Review of ASN-0075

## REVISE

### Issue 1: D-ACT cross-product partitioning claim is overstated
**ASN-0075, D-ACT proof (cross-product split)**: "every `t ∈ dom(C)` falls into exactly one of the four cases enumerated below, and the cross-product is jointly exhaustive on these two axes."

**Problem**: The stated cross-product is `origin(t) ∈ {d, ≠ d} × #t against L_d + 3 (<, =, >)`, which has 2 × 3 = 6 cells, not 4. The enumeration as written:
- Case 1 "Same origin, same length" covers cell `(d, =)`
- Case 2 "Same origin, shorter length" covers cell `(d, <)`
- Case 3 "Longer length (`#t > L_d + 3`)" with no origin constraint stated — the ASN explicitly says "Longer length (#t > L_d + 3)" and the argument inside derives `origin(t) = d` rather than presupposing it
- Case 4 "Different origin" — the ASN explicitly says "The length axis collapses here — the argument below does not depend on `#t`, so this single case covers different-origin tumblers at any length"

Cases 3 and 4 therefore both cover the cell `(origin(t) ≠ d, #t > L_d + 3)`. "Exactly one" is false — overlap exists.

**Required**: Either (a) restrict case 3 to "Same origin, longer length (`origin(t) = d`, `#t > L_d + 3`)" so the four cases partition the cross-product cleanly into `(d, =)`, `(d, <)`, `(d, >)`, and `(≠d, any)`; or (b) reword to "at least one" and acknowledge the overlapping coverage at `(≠d, >)`. The conclusion (no `t` lies strictly between `a` and `a'`) is unaffected because both arguments derive contradiction at the overlapping cell, but the partitioning structure as cited is wrong.

VERDICT: REVISE
