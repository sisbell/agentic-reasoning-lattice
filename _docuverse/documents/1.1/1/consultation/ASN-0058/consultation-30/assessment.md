# Channel Assignment — ASN-0058 review-30

**Date:** 2026-05-14 22:20

## Issue 1: M16a applies `origin` to addresses outside S7's stated domain
Reason: The fix is a formal cleanup — either rename to a structural extraction function defined on the T4-valid + zeros=3 subset, or add `a + k ∈ dom(C)` as a precondition and discharge at use sites. Both options are derivable from S7's existing definition in ASN-0036 and the proof's own structure.

## Issue 2: M12a's partition corollary is asserted in one parenthetical sentence
Reason: Spelling out the right- and left-extension procedures with explicit stopping conditions and a termination argument from `|dom(f)| < ∞` is pure proof elaboration. The construction is fully determined by the maximal-run definition already in the ASN.

## Issue 3: M2 omits T3 from its dependency list while invoking it indirectly via M-int
Reason: Bookkeeping fix — enumerate the foundation facts (TumblerAdd, T1, T3, S8a, S8-depth, OrdinalShiftBase) actually used inside M-int's component-`m` reduction. Derivable by reading the existing proof.
