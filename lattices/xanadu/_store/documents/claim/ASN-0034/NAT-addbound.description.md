For every `m, n ∈ ℕ`, the sum `m + n` is bounded below by each of its
operands: `m + n ≥ n` (right dominance) and `m + n ≥ m` (left dominance).
Both sides are stated independently because commutativity of addition
is not enumerated — without `m + n = n + m`, neither form is derivable
from the other. Right dominance follows from NAT-zero (which gives
`0 ≤ m`), NAT-addcompat's right order compatibility (which lifts
`0 ≤ m` to `0 + n ≤ m + n`), and NAT-closure's left additive identity
(which rewrites `0 + n` to `n`). Left dominance follows by the parallel
route through NAT-zero's `0 ≤ n`, NAT-addcompat's left order
compatibility, and NAT-closure's right additive identity.
