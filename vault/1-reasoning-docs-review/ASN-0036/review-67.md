# Review of ASN-0036

## REVISE

(none)

## OUT_OF_SCOPE

### Topic 1: Correspondence runs and T12 spans
The decomposition uses correspondence runs `(v, a, n)` with `n ∈ ℕ`, while the foundation defines spans as `(s, ℓ)` with `ℓ ∈ T` (a tumbler displacement). The formal bridge — that a run of length `n` at depth `m` corresponds to a span with displacement `δ(n, m)` — is natural but unstated.
**Why out of scope**: This is a span-algebra concern, not an error in S8's self-contained proof.

### Topic 2: Reachability of unbounded sharing
S5 shows consistency (existence of states with arbitrary sharing multiplicity) but not reachability through actual operations. Whether operations can produce states with sharing multiplicity exceeding any bound is an operational question.
**Why out of scope**: Operation-specific effects are excluded from this ASN's scope.

VERDICT: CONVERGED
