# Review of ASN-0042

## REVISE

### Issue 1: Multi-node bootstrap illustration duplicated between O14 commentary and the Worked Example
**ASN-0042, State Axioms (post-O14 paragraph) and Worked Example (opening O14 check)**: The post-O14 paragraph verifies the multi-node instance against each O14 clause — "principals at `[1]` and `[2]` ... satisfying O14.4 (AccountTier) ... O14.5 (Injective) by T3 ... O14.6 (Valid) ... O14.7 (NonNesting)." The Worked Example opens with the identical exercise: "we check that O14's bootstrap clauses are satisfied: Π₀ ≠ ∅; each pfx has zeros ≤ 1 ... pfx is injective on Π₀ (`[1] ≠ [2]`) ... the pair is non-nesting ... `|Π₀| = 2 < ∞`."
**Problem**: The same `{[1], [2]}` instance is checked clause-by-clause against the same O14 conjuncts in two places. The post-O14 paragraph's multi-node half adds nothing the Worked Example does not carry in full.
**Required**: Keep the single-node case in the post-O14 paragraph as the satisfiability witness (it is unique) and delete the multi-node sentences, or drop the redundant re-verification from the Worked Example. One site should own the multi-node O14 check.

### Issue 2: Redundant restatement of O6 wedged between its two corroborating citations
**ASN-0042, Structural Provenance (closing lines after O6)**: "By O6's biconditional, `ω` is a function of `acct(a)` alone — the account field of an address determines its effective owner, with no lookup beyond the address itself."
**Problem**: This restates O6's own claim ("effective owner determined entirely by account field"), already previewed in the section's opening sentence ("the longest-match computation depends only on the node and user fields"). The restatement sits between the Nelson quote and the Gregory confirmation, so the same point is asserted three times consecutively with no new content (unlike the genuinely new `pfx(ω(a)) ≼ acct(a)` corollary above it).
**Required**: Drop the restatement sentence; let the Nelson quote and Gregory confirmation flank O6 directly, or fold the "no lookup beyond the address itself" observation into the corollary rather than restating the theorem.

## OUT_OF_SCOPE

None. The ASN stays within ownership state, operations on it, and its invariants; out-of-scope topics (modification rights, baptism mechanism, content model) are correctly deferred or cited only as foundation.

VERDICT: REVISE
