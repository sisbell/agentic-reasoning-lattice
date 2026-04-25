# Regional Review — ASN-0034/NAT-addbound (cycle 2)

*2026-04-23 23:42*

### NAT-addbound uses a "Postconditions" slot inconsistent with the rest of the ASN
**Class**: REVISE
**Foundation**: n/a (foundation ASN)
**ASN**: NAT-addbound Formal Contract — `*Postconditions:* (A m, n ∈ ℕ :: m + n ≥ n)`. Every other claim in this ASN uses `*Axiom:*` and (where applicable) `*Consequence:*` / `*Definition:*` — NAT-zero, NAT-closure, NAT-addcompat, NAT-order, NAT-sub, NAT-discrete all follow that pattern. NAT-addbound is the only one that opens its structural slot as `*Postconditions:*`.
**Issue**: The prose explicitly describes NAT-addbound as "derivable from three NAT foundations and recorded as a named theorem" and walks a proof. That is a `Consequence:` in the vocabulary the rest of the document establishes. "Postconditions" is operation-contract terminology that imports an operation-contract reading — a postcondition is asserted by some operation — but NAT-addbound is not an operation, it is a universal fact about `+`. The slot choice is also disjoint from the slot vocabulary every other claim in this foundation uses, so a downstream consumer walking the document cannot tell whether `*Postconditions:*` is a new slot category with different semantics or just a one-off synonym.
**What needs resolving**: Either relabel NAT-addbound's slot to match the scheme the other claims use (likely `*Consequence:*`, since the statement is derived from declared foundations with a proof), or justify "Postconditions" by stating how it differs from `*Axiom:*` / `*Consequence:*` / `*Definition:*` and apply that slot scheme consistently across the ASN.

### NAT-discrete forward proof does not walk the `m = n` branch of its case split
**Class**: REVISE
**Foundation**: n/a
**ASN**: NAT-discrete Consequence proof, forward direction: "unfolding `m ≤ n` by the NAT-order definition `m ≤ n ⟺ m < n ∨ m = n` splits into two cases. In the case `m < n`, the axiom gives `m + 1 ≤ n`, which unfolds to `m + 1 < n ∨ m + 1 = n`; paired with the hypothesis `n < m + 1`, either disjunct is contradictory … The case `m < n` is therefore impossible, leaving `n = m`."
**Issue**: The proof explicitly announces two cases from unfolding `m ≤ n` — `m < n` and `m = n` — then walks only the first. It concludes "leaving `n = m`" as if the `m = n` case were a residue of eliminating `m < n`, but `m = n` is a separate branch of the split, not a residue. In that branch the conclusion `n = m` is immediate by symmetry of `=`, but the proof must say so: the discipline is that every branch of a case split is walked, even when the conclusion is one step. The present wording is exactly the "by similar reasoning" pattern — one case walked, the other case's obligation waved into the conclusion.
**What needs resolving**: State the `m = n` branch explicitly (e.g., "In the case `m = n`, symmetry of `=` gives `n = m` directly.") so both branches of the announced split terminate in `n = m` with explicit justification, and the forward direction reads as a closed case analysis rather than one walked case plus an inferred remainder.

### NAT foundation does not declare commutativity of `+`
**Class**: REVISE
**Foundation**: n/a
**ASN**: No claim in the ASN states `(A m, n ∈ ℕ :: m + n = n + m)` or exports it as Consequence. Evidence of the gap is visible in two places: NAT-sub's axiom slot lists **both** `(m − n) + n = m` and `n + (m − n) = m` — right- and left-inverse — because, per the accompanying prose, "citing either one without commutativity of addition would otherwise be tacit"; and NAT-addcompat lists **both** left compatibility `p ≤ n ⟹ m + p ≤ m + n` and right compatibility `p ≤ n ⟹ p + m ≤ n + m` for the same reason.
**Issue**: The foundation is paying the cost of undeclared commutativity (duplicated inverse clauses, duplicated compatibility clauses) without getting the fact itself. A downstream consumer that needs `a + b = b + a` outside the NAT-sub / NAT-addcompat contexts — to re-associate a sum, to argue symmetry of a predicate over `+`, to align operand order between cites — has no claim to cite. The current state is neither "commutativity is declared and both-sided clauses are redundant" nor "commutativity is deliberately withheld and its absence is documented"; it is a silent gap, recoverable only by noticing that both-sided clauses appear where a commutativity citation would halve them.
**What needs resolving**: Either add commutativity of `+` as a Consequence (or axiom, if the NAT foundations cannot derive it) and eliminate the duplicated both-sided clauses that exist to avoid citing it, or state in the ASN prose that NAT deliberately does not declare commutativity and that both-sided clauses are the foundation's substitute. Either choice closes the gap; leaving it tacit across two claims does not.

VERDICT: REVISE
