# Review of ASN-0042

## REVISE

No issues found. Every claim is derived with explicit case analysis, every edge case is addressed, and the foundation (ASN-0034) is used correctly without reinvention.

**Verification summary of what was checked:**

**O2 well-definedness.** The three-part argument (coverage via O4, linear ordering of covering prefixes, uniqueness via O1b) is airtight. The key step — that any two prefixes of the same tumbler are linearly ordered by ≼ — is proved explicitly and correctly. The finiteness argument (at most `#a` possible covering prefix lengths, each uniquely determined) closes cleanly.

**O6 biconditional.** Both directions of `pfx(π) ≼ a ≡ pfx(π) ≼ acct(a)` were verified across all case combinations: `zeros(pfx(π)) ∈ {0, 1}` × `zeros(a) ∈ {0, ≥1}`. The critical step for `zeros(pfx(π)) = 1` — that the forced zero at position `α+1` must be `a`'s first field separator because all preceding components are positive — follows correctly from T4 applied to both the prefix and the address.

**Delegation preservation.** O1a (via condition iv), T4 (via condition v), and O1b (via the length contradiction `#pfx(π''') ≤ #pfx(π) < #pfx(π') = #pfx(π''')`) are all preserved. The O1b proof correctly uses the at-most-one-new-principal constraint (O15) to exhaust pairwise checks.

**O7(a) categoricality.** Verified that condition (vi) blocks all principals in Π_Σ that might have prefixes extending `pfx(π')`, and condition (ii) bounds all remaining covering principals to prefix lengths ≤ `#pfx(π)` < `#pfx(π')`. The argument that any covering prefix of `a ∈ dom(π')` must also cover `pfx(π')` (via linear ordering of covering prefixes) closes the gap between "most-specific for `pfx(π')`" and "most-specific for any `a` in `dom(π')`."

**Account-level permanence Corollary.** The induction on principal introduction order is valid. The key step: the delegator of any new `π'` with `pfx(π) ≺ pfx(π')` has a prefix either equal to `pfx(π)` (hence is `π` by O1b) or strictly extending `pfx(π)` (hence traceable to `π` by the inductive hypothesis). The converse case (`pfx(π') ≺ pfx(π)`) is correctly blocked by condition (vi).

**O10 existence.** Both cases verified. For `zeros = 1`: sub-delegates' prefixes (form `N.0.U.U'…`, all positive after the zero) cannot match the zero at the user-document boundary of any document-level address. For `zeros = 0`: choosing `u` exceeding all existing user-field components produces an address unreachable by any sub-delegate. Constructed addresses satisfy T4 (verified: 3 zeros, non-adjacent, no boundary violations, all fields non-empty).

**O14 base cases.** Single-node (`Π₀ = {π_N}` at `[1]`) and multi-node (distinct node-level principals) both satisfy all five clauses. Non-nesting holds vacuously for singletons and by T3 for distinct single-component positive tumblers.

**Worked example.** All delegation conditions verified for `π_N → π_A`. Sub-account namespace (`acct(a₄) = [1,0,2,3] ≠ pfx(π_A) = [1,0,2]`) demonstrates strict containment. Fork example correctly shows `pfx(π_A) ⋠ a₃` and ownership of the fork address. Cross-account isolation (`a₃` under `π_N`) confirms O9 consequences.

**Foundation usage.** T1, T3, T4, T5, T8, T10, T10a, T0(a), TA5, TA6, FieldParsing all referenced correctly. No notation reinvented.

## OUT_OF_SCOPE

### Topic 1: Ownership transfer mechanism
**Why out of scope**: Nelson mentions "someone who has bought the document rights" (LM 2/29), but the ASN correctly identifies that the system as specified contains no transfer machinery. O3's monotonic refinement and O6's inalienable provenance mean transfer would require a registry external to the address structure — new architectural territory, not an error in this ASN's model. The ASN records this as an open question.

### Topic 2: Cross-node identity federation
**Why out of scope**: O9 establishes that the same human would hold separate, independent principals on each node. Whether and how these independent roots might be federated is a protocol-level concern. The abstract ownership model is clean without it.

### Topic 3: Delegation enforcement at runtime
**Why out of scope**: The delegation conditions (i)–(vi) are structural constraints on valid state transitions. The question of how a running system prevents rogue prefix claims — the enforcement gap that Gregory's unconditional `validaccount` reveals — belongs to the authentication/authorization layer, which O11 explicitly defers.

VERDICT: CONVERGED
