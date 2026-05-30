# Review of ASN-0042

## REVISE

### Issue 1: O14 states its bootstrap-registry clause three times
**ASN-0042, State Axioms / O14 (BootstrapPrincipal)**: The opening prose says "the bootstrap registry `Σ₀.B` is itself an ASN-0040-reachable registry conforming to B₀ conf. (finite, contiguous-prefix in every B6-valid namespace, and T4-valid)"; the formula block then lists "`Σ₀.B is an ASN-0040-reachable registry conforming to B₀ conf.`"; and immediately after the formula block: "This last clause asserts that `Σ₀.B` is an ASN-0040-reachable registry conforming to B₀ conf."
**Problem**: The identical clause appears three times in the same axiom — prose, formula, and a sentence whose only content is restating the formula. This is the reviser-drift pattern of "two paragraphs in the same document say the same thing in different words," compounded to three.
**Required**: Keep the formula clause; delete the standalone restatement sentence and trim the parenthetical in the opening prose to a single mention.

### Issue 2: The `findpreviousisagr` / "single allocation point advancing past delegated slots" corroboration is repeated four times
**ASN-0042, O17b, O18, DelegatorAllocatesPrefix, O10**: O17b — "every registry write in udanax-green funnels through a single allocation point — `findisatoinsertgr` … and `findpreviousisagr` … advancing unilaterally past existing (and delegated) slots with no inter-session signaling, shared counter, or lock." O18 — "`findpreviousisagr` issues each new account slot as a fresh granfilade entry, never re-purposing a previously baptized tumbler." DelegatorAllocatesPrefix — "the new account slot is entered through `findpreviousisagr` under the session's own account-tumbler authority." O10 — "each new tumbler issues from the single granfilade allocation point, which advances unilaterally past delegated slots."
**Problem**: The same implementation fact (one allocation point, fresh entry, advances past delegated slots) is re-asserted in four sections. Each restatement makes the precise reader confirm it adds nothing new. This is the flagged "multiple paragraphs … defer to the same" / repeated-corroboration pattern.
**Required**: State the `findpreviousisagr` corroboration once (at O17b, where the coupling is introduced) and replace the later three with bare back-references or delete them.

### Issue 3: The `delegated` predicate references `pfx(π')` for a principal not yet in `Π_Σ` without naming the state
**ASN-0042, State Axioms / Definition (delegated) and O15**: "conditions (i)–(v) hold for `(π, π')` at `Σ`," where (i) is `pfx(π) ≺ pfx(π')` and (iv) is `¬(E π'' ∈ Π_Σ : pfx(π') ≺ pfx(π''))`.
**Problem**: `pfx` is `pfx_Σ : Π_Σ → T`, but `π' ∈ Π_{Σ'} ∖ Π_Σ`, so `pfx_Σ(π')` is undefined — the conditions are stated "at `Σ`" yet quantify over a prefix that exists only at `Σ'`. The O8 proof silently corrects this (writing `pfx_{Σ_d}(π)` vs `pfx_{Σ_d^{post}}(π')`), so the looseness is real, not cosmetic.
**Required**: State explicitly that `pfx(π')` in conditions (i)–(v) denotes `pfx_{Σ'}(π')` (well-defined by O15's membership clause, immutable thereafter by O13), so the mixed-state reading is licensed rather than assumed.

### Issue 4: The node-level fork branch (`zeros(pfx(π)) = 0 → zeros(a') = 1`) is never verified on a concrete address
**ASN-0042, O10 / Worked Example (Fork)**: "With `π_A`'s sibling-advance fork and `π_B`'s field-opening fork both exhibited on concrete addresses, the two branches of Unilateral O10★ are witnessed."
**Problem**: Both worked witnesses (`π_A`, `π_B`) are account-level (`zeros(pfx) = 1`), exercising the `hwm>0` vs `hwm=0` branches. The structurally distinct node-level case — `zeros(pfx(π)) = 0` producing a *user-level namespace* `a'` with `zeros(a') = 1`, where the Form-A non-coverage sub-analysis (node-field-extending sub-delegates) becomes live — is asserted in general but checked against no specific address. The two node operators `π_N`, `π_M` are available in the example but no fork is traced from either.
**Required**: Add a concrete node-level fork (e.g., `π_N` forking `a' = [1,0,k]`) and verify `zeros(a') = zeros(pfx(π_N)) + 1 = 1`, `ω(a') = π_N`, and the Form-A exclusion, so the claim that the witness covers "both branches" holds for both principal levels.

## OUT_OF_SCOPE

### Topic 1: Ownership transfer and divergence of provenance (O6) from effective owner (O2)
**Why out of scope**: The ASN correctly notes Nelson's "bought the document rights" implies transfer but that the codebase has none, and defers it to the first Open Question. Transfer invariants are new territory, not a defect here.

### Topic 2: Cross-node identity federation consistent with O9
**Why out of scope**: O9 establishes node-locality for the system as specified (a forest of independent roots); federation is explicitly listed as an Open Question and would be a separate ASN.

VERDICT: REVISE
