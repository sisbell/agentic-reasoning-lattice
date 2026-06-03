# Review of ASN-0070

This is a mature note. The inverse-image core (F0), the I/O subspace correspondence (F-subspace), the canonical existence/uniqueness theorem (F-canonical, including the recently tightened Step 0), and the six worked configurations are rigorous and complete. The case split in Step 1 is exhaustive, both inclusions of the `k = m` case are proved, the consecutivity characterisation in Step 2 is fully worked, and the postcondition's two halves (F-sound/F-complete) are honestly discharged. I found no correctness gaps. The findings below are the anti-bloat patterns the classifier asks for.

## REVISE

### Issue 1: F0 closing paragraph restates itself and foreshadows named claims
**ASN-0070, F0 (InverseImageRelation), paragraph after the well-definedness clause**: "Two endsets with the same coverage produce the same R(d, e). Resolution is a function of coverage and arrangement — nothing more."
**Problem**: These two sentences assert the same fact in different words (matching the "two paragraphs say the same thing" pattern). The surrounding commentary ("The definition is *abstract*. It does not depend on how M(d) is stored, decomposed, or accessed...") is not load-bearing — no downstream claim cites it — and the final clause ("The intersection ... may be any subset ... including ∅; R(d, e) is defined uniformly regardless") merely foreshadows F-empty, which establishes it formally. A reader following the definition skips past this to reach F-subspace.
**Required**: Collapse the duplicated pair into one sentence; drop the foreshadowing clause (F-empty owns it).

### Issue 2: F-multi carries subspace generality that CL-UNIQ already excludes, then explains the exclusion in a Remark
**ASN-0070, F-multi (MultiplicityPreservation), postcondition and Remark**: postcondition states "for `S = subspace_I(a)`" (admitting `S = s_L`); the Remark then writes: "unlike the link subspace, where CL-UNIQ (LinkSubspacePositionUniqueness, ASN-0047) forces the restriction of M(d) to dom_L to be injective."
**Problem**: The hypothesis (`v₁ ≠ v₂` with `M(d)(v₁) = M(d)(v₂) = a`) is unsatisfiable when `a` is a link address — CL-UNIQ excludes it. So the postcondition's `s_L` branch is vacuous, and the Remark spends prose explaining a case the claim's own precondition already rules out (the "imagines a case the precondition excludes" pattern). The generality is technically true-but-vacuous and forces the explanatory contrast.
**Required**: Scope the postcondition to the content subspace (`S = s_C`), where multiplicity is realisable, and drop the CL-UNIQ contrast from the Remark — keeping only the realisability witness (K.μ⁺ imposes no injectivity constraint).

## OUT_OF_SCOPE

### Topic 1: cross-home consistency and BEBE concurrency (Open Questions)
**Why out of scope**: Both open questions point at future models (multi-home resolution relationships, replication/multi-server traversal). They are correctly posed as forward questions, not as gaps in this ASN, and the second names BEBE, which the scope statement excludes. No flag.

VERDICT: REVISE
