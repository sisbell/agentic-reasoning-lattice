# Review of ASN-0030

## REVISE

(none)

## OUT_OF_SCOPE

### Topic 1: Per-endset resolvability
`resolvable(L, d) ≡ (E a ∈ endset(L) : reachable(a, d))` treats from, to, and type as a flat union. A link whose only reachable addresses are in the type endset is "resolvable" under this definition despite being unnavigable. A future link ASN should introduce per-endset resolvability (e.g., requiring at least one from-address and one to-address to be reachable).
**Why out of scope**: The definition is used here only to establish non-monotonicity (A7b), which holds under any reasonable strengthening.

### Topic 2: MAKELINK coverage
The operation analysis covers all foundation-defined state transitions. When a link ASN introduces MAKELINK, the identity/reachability analysis should be extended to cover it.
**Why out of scope**: MAKELINK is not specified in any foundation ASN.

### Topic 3: Mutual consistency of A4, A4a, A5
These introduce substantial V-space specifications for DELETE, REARRANGE, and COPY as requirements. Their mutual consistency (e.g., DELETE-then-INSERT roundtrip, REARRANGE composed with itself) and consistency with INSERT's P9 are not verified.
**Why out of scope**: This ASN introduces these as specification requirements. Verification belongs in the ASN that formalizes these operations.

### Topic 4: Concurrent operations and atomicity
The analysis examines single operations in isolation. Whether reachability loss is atomic with respect to concurrent readers, and whether concurrent operations on the same document can violate the accessibility partition, are unaddressed.
**Why out of scope**: Concurrency is orthogonal to the permanence guarantee itself.

VERDICT: CONVERGED
