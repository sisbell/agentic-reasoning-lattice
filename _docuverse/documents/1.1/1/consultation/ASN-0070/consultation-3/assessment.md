# Channel Assignment — ASN-0070 review-3

**Date:** 2026-05-25 12:43

## Issue 1: F-subspace consequence derivation hand-waves the biconditional
Reason: The fix is internal — the needed foundations (S3★, S3★-aux, L0, L14) are all already cited in the ASN, and the reviewer's prescription supplies the exact case analysis structure required.

## Issue 2: V-restricted denotation undefined for empty content subspace
Reason: The fix is internal — the choice among the three resolution paths (convention, precondition refinement, or trivial-equation argument) is a definitional matter resolvable from ASN-0070's own machinery; ASN-0036's S8-depth and ASN-0047's LinkVPositionDepthAxiom already characterize when `m_S(d)` is well-defined, and an empty-subspace document trivially yields `R(d, e)|_S = ∅`.

## Issue 3: F-canonical Step 1 over-restricts canonical form widths
Reason: The fix is internal — the argument that finite V-restricted denotation in subspace `S` at depth `m_S(d)` forces ordinal-displacement-form widths is derivable from ASN-0053's span structure and ASN-0070's own V-restricted denotation definition combined with subspace partition.

## Issue 4: F-canonical Step 2 conflates `⟦·⟧` and `⟦·⟧_V`
Reason: The fix is internal — the bridge from V-restricted-denotation equality to full-denotation equality under level-uniformity follows from the span structure of ASN-0053 (start at depth `m_S(d)` in subspace `S` determines the V-tumbler boundary of the lexicographic interval), and S9 then applies as cited.

## Issue 5: F-empty's canonical form argument has the same `⟦·⟧` vs `⟦·⟧_V` gap
Reason: The fix is internal — TA-strict from ASN-0053 places the start `s` in `⟦σ⟧`, and the canonical-form construction guarantees `subspace(s) = S ∧ #s = m_S(d)`, so `s ∈ ⟦σ⟧_V`; the bridge is mechanical given the canonical-form construction.

## Issue 6: `m_S(d)` notation used without formal introduction
Reason: The fix is internal — purely a notation consolidation that unifies the already-cited S8-depth (ASN-0036) and LinkVPositionDepthAxiom (ASN-0047) under a common per-subspace symbol, with the empty-subspace acknowledgment cross-referenced to Issue 2's resolution.

## Issue 7: Worked example does not exercise F-state
Reason: The fix is internal — the state-changing transitions (K.μ⁻, K.μ⁺, K.μ~) are defined in ASN-0047 and can be applied to the existing example configuration to construct a fourth scenario; no implementation evidence or design-intent clarification is needed for an illustrative example.
