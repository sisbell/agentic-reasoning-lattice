# Review of ASN-0075

## REVISE

### Issue 1: "Coincides" claim in D-ACT is biconditionally too strong

**ASN-0075, §Actionability (D-ACT proof of witness-run decomposition uniqueness)**: "no element of `dom(C)` lies between consecutive emissions of one allocator under T1, and shift-adjacency within `dom(C)` therefore coincides with T1-consecutiveness within `dom(C)`."

**Problem**: The biconditional "coincides" is false. The forward direction — shift-adjacency in `dom(C)` implies T1-consecutiveness in `dom(C)` — holds (and is exactly what the preceding clause establishes). The reverse direction fails when crossing allocator boundaries: if `a = [d.0.s_C.k]` is the last emission of `A_C(d)` in `dom(C)` and `b = [d'.0.s_C.1]` is the first emission of `A_C(d')` with `d < d'` and no other allocator's content lies between them in `dom(C)`, then `a` and `b` are T1-consecutive in `dom(C)` but not shift-adjacent — `shift(a, 1) = [d.0.s_C.k+1] ≠ b`. The run decomposition existence and uniqueness argument actually requires only that shift-adjacency be a functional relation and `origin` be a function on `dom(C)`; it does not require biconditional correspondence with T1-consecutiveness. The "coincides" statement is therefore wrong as written and not load-bearing.

**Required**: Replace "shift-adjacency within `dom(C)` therefore coincides with T1-consecutiveness within `dom(C)`" with the one-directional statement actually needed: "shift-adjacency within one allocator's stream therefore implies T1-consecutiveness in `dom(C)`, making each I-adjacency equivalence class T1-contiguous within `dom(C)`." This preserves the "T1-contiguous run" characterisation without asserting the false reverse direction.

## OUT_OF_SCOPE

No out-of-scope flags. The Open Questions section properly defers extensions (multi-document witnesses, concurrent coherence, restoration semantics, link-subspace deletion analysis, cross-version comparison patterns) to future ASNs.

VERDICT: REVISE
