# Review of ASN-0081

## REVISE

### Issue 1: Additive compatibility identity used without derivation in D-SHIFT

**ASN-0081, D-SHIFT (Right Shift)**: "For any v ∈ R, ord(v) ≥ ord(r) = ord(p) ⊕ w_ord (since v ≥ r)."

**Problem**: The equality `ord(r) = ord(p) ⊕ w_ord` is asserted inline without derivation. This is the key algebraic identity connecting whole-tumbler addition (`r = p ⊕ w`) to ordinal-level addition — the bridge that makes the ordinal projection approach work. The depth-2 verification requires three steps:

1. `r = p ⊕ w = [S, p₂] ⊕ [0, c] = [S, p₂ + c]` (TumblerAdd, action point k=2)
2. `ord(r) = [p₂ + c]` (definition of ord)
3. `ord(p) ⊕ w_ord = [p₂] ⊕ [c] = [p₂ + c]` (TumblerAdd, action point k=1)

The depth-2 computation of `ord(r)₁ = p_m + c` appears later in D-SHIFT's well-definedness paragraph, and D-SEP(a) shows the closely related computation `ord(p) ⊕ w_ord = [p₂ + c]`. But the identity itself is never stated or verified in one place. The pieces are scattered across two sections without being assembled.

This identity is also the natural starting point for the depth > 1 generalization noted in Open Questions — at general depth, it holds whenever `w₁ = 0` and `actionPoint(w) ≤ #p`, because TumblerAdd copies positions before the action point from the first operand, so stripping the shared first component commutes with the addition. Stating it as a named lemma now would give the generalization a clean foundation to build on.

**Required**: State the identity `ord(p ⊕ w) = ord(p) ⊕ w_ord` (when `w₁ = 0`, `actionPoint(w) ≤ #p`) as a named property with the depth-2 computation shown, either (a) as a postcondition of the ordinal extraction definitions or (b) as a separate lemma before D-SHIFT. Then cite it by name in D-SHIFT and D-SEP.

## OUT_OF_SCOPE

### Topic 1: Generalization to ordinal depth greater than 1
**Why out of scope**: Already identified as the ASN's open question. The depth-2 scoping axiom is a deliberate restriction that makes TA4's zero-prefix condition vacuous and TA3-strict's equal-length precondition trivial. Generalization is new work, not an error in this ASN.

### Topic 2: Composability of sequential contractions
**Why out of scope**: The post-state satisfies all system invariants (proved) and D-SEQ follows from D-CTG-post + D-MIN-post + S8-depth-post, so a second contraction's preconditions can be met. But proving composition properties (e.g., two contractions commute when their spans are disjoint, or compose associatively) is new territory that would belong in a future ASN.

VERDICT: REVISE
