# Review of ASN-0113

This is a rigorous, well-structured query specification. The proofs (W3, W4, W5, W10, W11) are complete, the worked instances exercise the genuine cases (including the non-vacuous depth-3 check of T5 prefix-confinement), and the boundary cases (empty/W0, one-member/d', two-member/d, unallocated/W-pre) are all covered. I found no correctness gaps. The findings below are the anti-bloat patterns this note's classifier asks for: meta-prose and forward-reference accretion the precise reader must skip past.

## REVISE

### Issue 1: Defensive trivial-vs-substantive framing in W9
**ASN-0113, "Only the two counted subspaces appear"**: "The substantive guarantee is not the definitional inclusion `occupied(d) ⊆ {s_C, s_L}` (which holds by construction of `W6`, since the candidate set is the literal `{s_C, s_L}`) but the fact that `O(d)` *exhausts* into exactly these two subspaces..."
**Problem**: This paragraph builds a trivial reading only to dismiss it. The W6 inclusion is true by construction and no reader would mistake it for the claim; setting it up to knock it down is meta-prose that obscures the actual derivation (W9 from S3★-aux + SC-NEQ).
**Required**: Delete the not-X-but-Y framing; state W9 and its derivation directly.

### Issue 2: Misreading-correction plus forward reference in W14
**ASN-0113, W14 (Comparability)**: "The reason is *not* that each report exposes both kinds — it does not: W7 emits exactly `|occupied(d)|` members, *omitting* any empty subspace... Rather, the comparison is total because `n_S(d) = |V_S(d)|` is a *total function*... (Open Question 2)."
**Problem**: Imagines a wrong rationale (comparability from "both kinds exposed") the claim never depended on, then corrects it — reviser-drift meta-prose. The trailing "(Open Question 2)" is a forward reference into an *unnumbered* Open Questions list, so the pointer is both deferral-prose and imprecise.
**Required**: State the positive fact (n_S is total because it counts V_S(d) directly) without the strawman; drop or inline the Open Question pointer rather than referencing a numbered item that does not exist.

### Issue 3: Proof-structure justification in W10
**ASN-0113, W10 (SubspaceConfinement)**: "Unlike W4, this quantifies over *every* `t` in the denotation — tumblers of arbitrary depth, including the whole subtree hanging below each V-position — so it needs its own argument, not W4's depth-`m_S`-restricted reasoning."
**Problem**: Meta-commentary explaining *why* W10 cannot reuse W4's proof, prefacing an argument that is then given anyway. The two-line first-component argument stands on its own and does not need the comparison to W4.
**Required**: Drop the "unlike W4 / needs its own argument" preamble; lead with the argument.

### Issue 4: Rationale-for-recording preface to W5
**ASN-0113, "Exactness is contingent on contiguity"**: "We pause to record what makes W4 hold, because an alternative implementation must not lose it."
**Problem**: Justifies the act of recording the claim rather than advancing it. The "alternative implementation must satisfy" motivation is already the standing premise of the whole specification.
**Required**: Remove the prefatory sentence; W5's biconditional and its two-direction proof carry the content.

### Issue 5: Redundant restatement of the symmetric witness in W12
**ASN-0113, W12 (ProfileIrreducibility)**: "The content and link mechanisms are not exchanged — text is added only by coupled content composites and links only by uncoupled link composites, exactly as in the surrounding paragraph; what changes between the two witnesses is solely which count is driven and which is held."
**Problem**: This sentence restates the mechanism just constructed in the preceding paragraph ("exactly as in the surrounding paragraph" admits the duplication). The symmetric witness needs only "vary the content axis, hold the link axis" — the re-explanation that the mechanisms are not swapped is defensive padding.
**Required**: Compress to a single clause naming the varying axis; delete the re-derivation of the mechanism.

### Issue 6: Implementation code-trace detail in W-pre
**ASN-0113, W-pre**: "...fails the open-document check (`findorgl` returns FALSE because `checkforopen` finds no registry entry) and the dispatcher emits the FEBE failure marker `?`... (consultation, code trace `fns.c:140`, `do1.c:327`, `granf1.c`)."
**Problem**: The empty-vs-unallocated distinction is a legitimate concrete example, but file:line dispatch internals are implementation mechanics that the abstract claim (unallocated `d` is outside the operation's domain) does not rest on.
**Required**: Keep the behavioral observation (empty returns the empty span-set with success; unallocated fails); drop the function-name/line-number trace.

VERDICT: REVISE
