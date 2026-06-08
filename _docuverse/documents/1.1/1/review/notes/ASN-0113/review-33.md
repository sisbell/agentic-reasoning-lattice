# Review of ASN-0113

## REVISE

### Issue 1: W2–W4 omit the non-empty guard their own derivations require
**ASN-0113, Claims Introduced table**: W2 "`ext(d, S) = ([S,1,…,1], δ(n_S, m_S))`", W3 "`ext(d, S)` is a well-formed … T12 span", W4 "`⟦ext(d, S)⟧ ∩ VSlice(S, m_S) = V_S(d)`".
**Problem**: `ext(d, S)` is undefined when `V_S(d) = ∅`: then `n_S = 0`, so `δ(n_S, m_S) = δ(0, m_S)` violates OrdinalDisplacement's precondition `n ≥ 1` (it is not even positive), and `m_S` is undefined since S8-depth only fixes a common depth on a non-empty `V_S(d)`. W3's proof leans explicitly on "`n_S ≥ 1` (the run is non-empty)." Yet the table states W2–W4 unconditionally, while W5 alone carries the guard "*for `V_S(d) ≠ ∅`*." A reader treating the table as the contract sees three claims about a span that does not exist for empty subspaces.
**Required**: State the carrier domain `S ∈ occupied(d)` (equivalently `V_S(d) ≠ ∅`) on W2, W3, and W4, matching W5's presentation.

### Issue 2: W14's claims-table entry is essay content in a structural slot
**ASN-0113, Claims Introduced table, W14**: "Comparability — iterating the fixed kind-list `(s_C, s_L)`, a consumer recovers each `n_S(d)` *by subspace identifier* `start₁ = S` (not list position, since W7 makes the result a subsequence): member present ⇒ boundary-count; absent ⇒ `n_S = 0`, sound by W6/W7; so per-kind comparison …"
**Problem**: A table cell holds a multi-clause reconstruction procedure with embedded justifications and a parenthetical caveat — the statement of the claim is buried. The "iterate, check present/absent, read by identifier" recipe is prose; the table should carry the invariant.
**Required**: Reduce the W14 entry to its claim ("per-kind comparison `n_S(d₁)` vs `n_S(d₂)` is well-defined across documents sharing a kind-list; absent member ⇒ `n_S = 0`"); leave the reconstruction procedure to the body section, where it already appears.

### Issue 3: W5's converse and its design conclusion imagine a state D-CTG★ excludes
**ASN-0113, "The extent of a single subspace"**: "Suppose `V_S(d)` is *not* contiguous … (for instance `{[S,1], [S,3]}` with `[S,2]` inactive) … Faithful reporting then requires a *span-set* within the single subspace, one member per contiguous cluster."
**Problem**: D-CTG★/D-SEQ★ are standing foundation invariants holding at *every* reachable state, so `V_S(d)` is never non-contiguous; the constructed gap state is unreachable. The "one member per contiguous cluster" conclusion describes machinery the operation never produces (W7 emits one member per *subspace*, full stop). This is precisely the case the first Open Question already parks. The biconditional's forward direction (exactness rests on contiguity) is the load-bearing content; the counterfactual construction and the fragmented-span-set conclusion are the excluded-case prose the anti-bloat pass targets.
**Required**: Keep the dependency statement (exactness of `ext(d, S)` is contingent on the standing D-CTG★ run-shape); drop the unreachable-state construction and the "span-set within a single subspace" design conclusion, which duplicate Open Question 1.

## OUT_OF_SCOPE

None. The operation's body stays within per-subspace extent reporting; version-fork permanence, transclusion consistency, and reconciliation with a single overall extent are correctly confined to Open Questions, not claimed.

VERDICT: REVISE
