# Proof Verification: S7a

RESULT: FOUND

**Problem**: The property statement is truncated. The final paragraph introduces a further design requirement — "Since Istream addresses designate content elements within documents, we require:" — but never completes the sentence. The element-level constraint (presumably `zeros(a) = 3` for all `a ∈ dom(Σ.C)`) is motivated but never actually stated.

Additionally, no `*Formal Contract:*` section is present. S7a is explicitly described as "a design requirement, not a convention," which makes it an axiom. It should have a formal contract with an `*Axiom:*` field capturing both conjuncts:
1. Document-scoped allocation: the document-level prefix of every content address identifies its creating document.
2. The unstated element-level constraint on content addresses.

**Required**:
1. Complete the truncated sentence beginning "we require:" — state the element-level constraint explicitly (e.g., `zeros(a) = 3` for all `a ∈ dom(Σ.C)`).
2. Add a formal contract, e.g.:
   ```
   *Formal Contract:*
   - *Axiom:* (a) For every a ∈ dom(Σ.C), prefix(a, document) identifies the document
     whose owner allocated a. (b) For every a ∈ dom(Σ.C), zeros(a) = 3 (element-level).
   ```
3. Declare T1 as a dependency if the "Contiguous subtrees" remark (which references T1) is meant to support S7a, or remove that reference.
