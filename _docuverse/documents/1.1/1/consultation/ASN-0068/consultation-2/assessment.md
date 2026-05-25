# Channel Assignment — ASN-0068 review-2

**Date:** 2026-05-24 23:43

## Issue 1: CV-IN's subspace constraint is informally claimed but not formally enforced
Reason: The fix is a self-contained consistency tightening — the choice between strengthening CV-IN's `actionPoint(width(σ)) ≥ 2` requirement or relaxing the prose draws on definitions already imported (ASN-0034 TumblerAdd, ASN-0047 L0/L14, ASN-0053 S6, ASN-0058 C0).

## Issue 2: Logical error in CV-MAX uniqueness proof's `δ − 1 ≥ 0` step
Reason: Pure logical-step correction, fully derivable from the proof's own variables and the case hypothesis `δ > 0`.

## Issue 3: "Valid V-predecessor" definition is dense and admits two readings
Reason: Definitional clarification using ASN-0047 D-SEQ★/D-MIN★ and ASN-0036 S8a, all already cited in the ASN.

## Issue 4: Existence proof's left walk at `i = 0` is vacuous and confusing
Reason: Pure proof-rewording fix relying only on the existence-proof variables already in scope.

## Issue 5: Right- and left-maximality of the constructed run not explicitly tied back to walk termination
Reason: Index-translation bookkeeping is mechanical from the proof's own definitions of `n_R` and `j`; no external evidence needed.

## Issue 6: CV-ATOM, CV-RO, CV-DETERM are stated as separate claims but derived only informally
Reason: All three derivations follow from the ASN's own definitions — the run condition admits `n ≥ 1`, the signature returns `Result` without side-effecting clauses, and CV-MAX already proves uniqueness — so the fix is internal reformulation.

## Issue 7: Empty input case is a footnote rather than a formal claim
Reason: Pure structural promotion of an existing remark to a labeled claim; the substance is already in the ASN.

## Issue 8: Equivalence `Result ≅ P(Span × Span)` claimed without specifying the dependency
Reason: Notational tightening — the parametric dependence on `m_a, m_b` is fixed by ASN-0036 S8-depth applied to the input, all internal.

## Issue 9: Self-comparison with differing restrictions not explicitly addressed
Reason: Additional case description follows mechanically from the existing `corr_{a,a}` formula and intersection semantics already introduced.

## Issue 10: Result type omits the shared I-address; design choice unstated
Reason: The justification — that `M(d_a)(v_a + k)` is state-derivable, so omitting the I-address avoids duplication — is internal to the operation's signature and the storage model already in the ASN.
