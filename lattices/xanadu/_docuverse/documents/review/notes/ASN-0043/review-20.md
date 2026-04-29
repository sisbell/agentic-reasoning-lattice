# Rebase Review of ASN-0043

## REVISE

### Issue 1: GlobalUniqueness cited for document-prefix uniqueness
**ASN-0043, Home and Ownership**: "home(a) uniquely identifies the creating document across the system (by GlobalUniqueness)"
**Problem**: GlobalUniqueness as introduced in this ASN applies to element-level tumblers — "any element-level tumbler produced by the allocation discipline" — i.e., addresses with `zeros(a) = 3`. The claim that `home(a)` *uniquely identifies the creating document* requires document-prefix uniqueness: distinct documents produce distinct prefixes. Document prefixes are document-level tumblers (`zeros = 2`), outside GlobalUniqueness's stated scope. S7 (StructuralAttribution, ASN-0036) establishes this for content via T9, T10, T10a+TA5(d)+T3 applied at the document level — the same three cases, but at a different level of the hierarchy than GlobalUniqueness covers.
**Required**: Either (a) cite the three cases directly at the document level (paralleling S7's derivation with L1a replacing S7a and L1 replacing S7b), or (b) widen GlobalUniqueness's stated scope to cover all allocator outputs (not only element-level tumblers), or (c) note that the claim is simply that `home` is a well-defined function of the address (which follows from L1 + T4 alone, with no uniqueness argument needed).

VERDICT: REVISE
