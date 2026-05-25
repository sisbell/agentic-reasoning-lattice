# Review of ASN-0075

## REVISE

### Issue 1: Introduction understates the negative result that D-DISCR establishes
**ASN-0075, third paragraph of the introduction**: "any conforming implementation must therefore maintain state components — beyond C and M alone — sufficient to disambiguate the two predicates DELETED(a, d) and NEVER_INCLUDED(a, d) at every reachable state."
**Problem**: The witnesses Σ_1 and Σ_2 in D-DISCR have `(C_1, L_1, E_1, M_1) = (C_2, L_2, E_2, M_2)` componentwise; only R differs. The proof therefore establishes that no function of `(C, L, E, M)` collectively can discriminate, not merely that `(C, M)` is insufficient. The post-proof prose correctly states the stronger result ("beyond the four foundation components (C, L, E, M) collectively"), but the introduction reads as if L or E might suffice. The reader of the introduction takes away a weaker claim than the proof actually delivers.
**Required**: Strengthen the introduction's phrasing to "beyond (C, L, E, M) collectively" so the framing matches the witnesses.

### Issue 2: T1-contiguity of witness runs is asserted but not derived
**ASN-0075, §D-ACT (deletion witness run construction)**: "Each class is a maximal T1-contiguous run of addresses sharing one origin — a witness run."
**Problem**: The partition is constructed by I-adjacency (`shift(·, 1)` plus shared origin). The further property that each equivalence class is T1-contiguous *within dom(C)* — that no element of dom(C) lies between two consecutive class members in T1 order — is not derived. The derivation requires the structural fact that every content address has element-field length exactly 2: A_C(d) starts at `[d.0.s_C.1]` (#E = 2) and emits via `inc(·, 0)`, which preserves length by TA5(c). Without #E = 2 across dom(C), nothing rules out an interleaving address like `[d.0.s_C.k.x]` lying T1-between `[d.0.s_C.k]` and `[d.0.s_C.k+1]`. The argument is short but absent.
**Required**: Add a sentence such as "Within dom(C), every content address has element-field length 2 (A_C(d) emits via `inc(·, 0)`, preserving length by TA5(c) from the length-2 first emission `[d.0.s_C.1]`), so no element of dom(C) lies between consecutive emissions of one allocator under T1, and shift-adjacency within dom(C) coincides with T1-consecutiveness."

## OUT_OF_SCOPE

No items. The Open Questions section correctly defers concurrent semantics, n-document generalisations, link-subspace analysis, and restoration mechanics to future ASNs.

VERDICT: REVISE
