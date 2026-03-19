# Review of ASN-0053

## REVISE

No issues.

## OUT_OF_SCOPE

### Topic 1: General span difference beyond containment
S11 proves the difference bound for the containment case (⟦β⟧ ⊆ ⟦α⟧ yields at most 2 spans). The general case — proper overlap yields 1 span, separated/adjacent yields 1 span (just α), and reverse containment yields 0 spans — is straightforward but unstated. A general S11 covering all SC cases would be a natural complement.
**Why out of scope**: S11 correctly scopes its claim to the interesting case (containment is the only configuration producing 2 spans). The other cases are simpler and could be stated as corollaries in a future ASN that builds on this algebra.

### Topic 2: Exact representability of finite position sets
S7 proves ⟦Σ⟧ ⊇ P (covering), not ⟦Σ⟧ = P (exact). For positions at a uniform level within a single subspace, exact representation is achievable (each unit span isolates exactly one position). For mixed-level positions, ⊇ is the best possible — a span at a coarser level necessarily includes all finer-level positions in its interval. The ASN's ⊇ is correct and conservative; tightening it for the level-uniform case would be a clean addition.
**Why out of scope**: S7 establishes a basic covering result. The exact-representation refinement requires formalizing "position isolation" at the finest level, which is new territory.

### Topic 3: LeftCancellation as a foundation property
The ASN transparently acknowledges that LeftCancellation "is properly a tumbler arithmetic fact, belonging with ASN-0034." The property is correctly proven and essential for S5. A future revision of ASN-0034 could adopt it as a foundation lemma, letting this ASN reference rather than re-derive it.
**Why out of scope**: The property is new (not defined in ASN-0034), correctly proven here, and needed for self-containment. Promoting it to the foundation is a packaging decision, not a correctness issue.

VERDICT: CONVERGED
