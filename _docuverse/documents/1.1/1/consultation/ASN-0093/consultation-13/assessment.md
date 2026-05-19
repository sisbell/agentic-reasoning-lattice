# Channel Assignment — ASN-0093 review-13

**Date:** 2026-05-18 20:39

## Issue 1: Chain length not committed in substrate context
Reason: The fix is internal — the substrate can simply commit chains to be infinite (matching the existing conceptual-chain quantifier note in ChainPrefixExtension) or rephrase the (possibly infinite) qualifier. Either choice is a presentational decision derivable from the ASN's own structural commitments without external input.

## Issue 2: "T10a-discipline-satisfying chain" terminology overstates the discipline
Reason: Pure terminology rename; the substrate already disclaims tree embedding and the Definition's content is explicitly structural-only. The fix is internal nomenclature cleanup with no design or implementation question at stake.

## Issue 3: K.λ subsequent-emit E₁-preservation underwriting is implicit
Reason: DisjointSubAllocatorChains is already proved in the ASN as a derived lemma; the fix is adding explicit cross-references in the discharge matrix and precondition derivations. Purely internal cross-referencing work.

## Issue 4: ChainUniformZeroCount proof's TA5(b) citation is at k=0, not k>0
Reason: The fix is a wording correction citing the correct TA5(b) clause from ASN-0034, which is a foundation ASN already referenced. Derivable from the foundation claim's stated form without external channels.

## Issue 5: SubAllocatorAxiom.Exists "remain active" claim relies on M1, which is the inductive invariant
Reason: This is a layering/presentation issue about axiom vs. inductive invariant; the substrate's own simultaneous-induction framing already handles the dependency. The fix is restructuring the axiom statement — purely internal.

## Issue 6: The Open Questions item on link withdrawal contradicts L12's stated permanence
Reason: The fix requires understanding Nelson's design intent for tombstoning (LM 4/9) — whether tombstones preserve dom(L) entries with marker values or remove them — and how the implementation realizes withdrawal if at all. Both channels are needed.
Nelson question: In LM 4/9's tombstone-style withdrawal, is the withdrawn link's entry preserved in the address space with a tombstone-marked value, or is it removed entirely from the link store?
Gregory question: Does udanax-green implement any form of link withdrawal or retraction, and if so does it remove entries from the link store or mark them in place?

## Issue 7: Cross-document disjointness Case A "d₂[#d₁+1] ≠ 0" argument needs more care for d₁'s zero positions
Reason: The fix is adding a one-sentence precondition check citing Prefix's derived postcondition `#d₁ < #d₂`, which the proof already establishes implicitly. Purely internal proof-cleanup.

## Issue 8: "T10a-conforming step sequence" vs "structural inc-chain" relationship not explicit
Reason: Terminology clarification between this ASN and ASN-0043, both project documents. The fix is adding a sentence noting the rename is purely terminological — derivable from comparing the two ASNs' own content.

## Issue 9: Discharge matrix doesn't explicitly check C1b under K.σ at prior keys
Reason: The fix is strengthening matrix entries to note that `E(·)` is T4b's structural projection (defined in ASN-0034) and depends on no state component. Derivable from the foundation definition already referenced.

## Issue 10: Worked example Step 9 misclassifies sub-case at #d = #d_alt
Reason: Sub-case naming convention cleanup at the equality boundary; the proof's exhaustive coverage already handles `#d₁ = #d₂` (B.i with `≤`). The fix is renaming sub-cases or adding a clarifying note — purely internal presentation.
