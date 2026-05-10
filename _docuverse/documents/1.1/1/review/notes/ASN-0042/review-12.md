# Review of ASN-0042

## REVISE

### Issue 1: Delegation relation omits T4 validity as an explicit condition
**ASN-0042, Definition (Delegation)**: "subject to four structural constraints: (i) … (ii) … (iii) … (iv) `zeros(pfx(π')) ≤ 1`"
**Problem**: The four conditions are locally incomplete. A prefix such as `[1, 2, 0]` satisfies all four — (i) it strictly extends `[1, 2]`; (iv) `zeros = 1 ≤ 1` — yet violates T4 (ends with zero; the user field after the separator is empty, breaking the non-empty field constraint). The blanket statement in "Ownership as a Structural Predicate" that `pfx(π)` is "a valid tumbler (satisfying T4)" covers this, but the delegation definition presents itself as self-contained ("subject to four structural constraints"), and the subsequent preservation paragraphs explicitly argue O1a and O1b without mentioning T4. A downstream author using conditions (i)–(iv) as the complete delegation specification could produce invalid prefixes, which would then break the AccountPrefix lemma and the O6 biconditional (both depend on T4 for well-defined field parsing).
**Required**: Either add condition (v) `T4(pfx(π'))` to the delegation relation, or add a "Delegation preserves T4" paragraph parallel to the O1a/O1b paragraphs. The argument is brief: `pfx(π)` satisfies T4 (induction hypothesis); condition (i) gives `pfx(π) ≺ pfx(π')`; the new prefix extends a T4-valid tumbler; T4 validity of the extension must be verified (no adjacent zeros, no trailing zero, every present field non-empty). The properties table entry for `pfx(π)` should also list T4 alongside injectivity and `zeros ≤ 1`.

## OUT_OF_SCOPE

### Topic 1: Ownership transfer mechanism
**Why out of scope**: The ASN correctly identifies the tension between Nelson's "someone who has bought the document rights" and the absence of any transfer machinery in either the design or the codebase. Transfer would require an external registry that decouples authority from provenance — new conceptual territory, not an error in this ASN.

### Topic 2: Delegation event recording
**Why out of scope**: Whether delegation events must be persistently recorded, or whether the address hierarchy itself constitutes sufficient structural evidence, is a separate design question. The ownership model as stated is silent on audit trails.

### Topic 3: Cross-node identity federation
**Why out of scope**: O9 establishes node-locality cleanly. How the same human holds independent principals on separate nodes, and what invariants a federation mechanism would need to satisfy, is future work that builds on O9 rather than correcting it.

VERDICT: REVISE
