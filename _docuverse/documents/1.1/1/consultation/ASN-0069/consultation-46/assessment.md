# Channel Assignment — ASN-0069 review-46

**Date:** 2026-05-27 17:50

## Issue 1: T3 (CanonicalRepresentation) missing from Dependency Audit
Reason: Pure audit update — T3 is already invoked explicitly in V11a's recovery argument (and implicitly in V2's parallel argument); the fix is adding it to the Dependency Audit's ASN-0034 supply list. Derivable from the ASN's own content.

## Issue 2: V11 premise scope remark conflates two distinct discharge mechanisms
Reason: Restructuring uses mechanisms already present in the ASN — V5a Corollary 2 (operational discharge for non-immediate-source modifications) and V11's conclusion anchoring at Σ (historical fixing for d_src modifications after step 1). The fix is expository, splitting the remark into two paragraphs that separately cite the operative mechanism in each case.

## Issue 3: V9a's parenthetical justification is compressed and slightly wrong
Reason: The correct two-step argument uses V3 (inherited I-addresses come from pre-fork dom(C)) and ASN-0047's SubAllocatorAxiom (A_C(d_new) was inactive pre-fork because d_new ∉ E_doc pre-fork) — both already in this ASN's dependency set. The fix is rewriting the parenthetical to cite both steps explicitly.

## Issue 4: V8a's claim is narrower than its name suggests
Reason: This is a naming/scoping choice between matching name to body (rename to "K.α") or broadening body to match name (cover all M-preserving steps K.α, K.λ, K.ρ via their frame conditions in ASN-0047). Both options are internal restructuring; V8b already covers the general state-relativity case.

## Issue 5: V11a's value characterization claim is loose at the boundary
Reason: The mathematical content (TA5(d) at k=1 yielding value 1, TA5(c) at k=0 incrementing the trailing component on successive emissions) is already worked out in the ASN body. The fix is presentational — adopt the unified "1 + j" characterisation or explicitly enumerate the disjoint cases with exhaustiveness.

## Issue 6: Verification of K.δ sub-case A freshness leans on T10a's at-most-once clause without addressing alternate emission paths
Reason: The structural distinctness of TA5(d) outputs at different k' values is mechanical from TA5 in ASN-0034, already in the dependency set; T10a.7's enumeration injectivity over the parent allocator's joint spawning space is likewise already cited. The fix is selecting and inserting the appropriate citation chain into the freshness derivation.
