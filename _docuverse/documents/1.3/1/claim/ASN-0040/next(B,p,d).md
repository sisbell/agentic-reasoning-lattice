**next(B,p,d) (NextAddress).**

  next(B, p, d) = if children(B, p, d) = ∅ then inc(p, d) else inc(max(children(B, p, d)), 0)

— find the greatest baptized sibling and produce its immediate successor; if none exists, produce the first child.

*Justification of well-definedness.* We must show that next(B, p, d) is well-defined for any registry B ⊆ T, parent p ∈ T, and depth d ≥ 1 — that is, each branch of the conditional produces an element of T, and the case split is exhaustive.

The case split is exhaustive: children(B, p, d) = B ∩ S(p, d) is a set, so it is either empty or non-empty. No third possibility exists.

*Case 1: children(B, p, d) = ∅.* The definition yields next(B, p, d) = inc(p, d). By TA5(d) (ASN-0034), inc(p, d) is well-defined for any p ∈ T and d ≥ 1, producing a tumbler of length #p + d whose first #p components are preserved from p, whose next d − 1 positions are zero-valued field separators, and whose final position has value 1. The result is an element of T — specifically, c₁ of the sibling stream S(p, d).

*Case 2: children(B, p, d) ≠ ∅.* The definition yields next(B, p, d) = inc(max(children(B, p, d)), 0). We must show that max(children(B, p, d)) exists and that the subsequent increment is well-defined. The set children(B, p, d) is a non-empty finite subset of T (finite because B is finite, non-empty by hypothesis). The lexicographic order T1 is a strict total order on T, so every non-empty finite subset has a unique maximum. Let t = max(children(B, p, d)). TA5's first (unlabeled) postcondition (ASN-0034) gives `inc(t, 0) ∈ T` for any t ∈ T; TA5(c) further specifies the form — length preserved, value at position sig(t) advanced by 1.

In both cases, next(B, p, d) produces an element of T. The definition is total on its domain {(B, p, d) : B ⊆ T finite, p ∈ T, d ≥ 1}. ∎

*Formal Contract:*
- *Definition:* next(B, p, d) = if children(B, p, d) = ∅ then inc(p, d) else inc(max(children(B, p, d)), 0), where children(B, p, d) = B ∩ S(p, d).
- *Preconditions:* B ⊆ T finite (discharged by B_fin when B = Σ.B for a reachable Σ); p ∈ T; d ≥ 1; S(p, d) defined.
- *Postconditions:* next(B, p, d) ∈ T — the result is a valid tumbler.
- *Axiom:* TA5(c) (sibling increment well-definedness), TA5(d) (child increment well-definedness), T1 (total order guarantees max exists).
