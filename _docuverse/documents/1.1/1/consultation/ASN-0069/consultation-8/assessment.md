# Channel Assignment — ASN-0069 review-8

**Date:** 2026-05-25 14:09

## Issue 1: `d²_new` symbol overloaded across V10, V11, and the worked example
Reason: Pure notation disambiguation. V10 (siblings of `d_src`) and V11 (chained fork of `d¹_new`) are both defined within this ASN; the fix is choosing distinct symbols for the two structurally distinct tumblers. No design intent or implementation evidence is needed.

## Issue 2: V7's empty-case composite lacks explicit ValidComposite★ verification
Reason: The coupling constraints J0, J1★, J1'★ are defined in ASN-0047 (already referenced throughout this ASN), and they hold vacuously for the K.δ-alone composite because `ran(M'(d_new)) = ∅`, `R' = R`, and `dom(C') = dom(C)`. The verification is mechanical from existing referenced material.

## Issue 3: V8b's re-installation example glosses over I-address choice for intermediate positions
Reason: K.μ⁺'s mechanics (S3★ requiring `M'(d)(v) ∈ dom(C)` for each new V-position, and the multi-position step framing) are defined in ASN-0047, already referenced in this ASN's verification section. The clarification is derivable from K.μ⁺'s definition alone.

## Issue 4: V11a transitivity argument is single-step, but conclusion is over a chain
Reason: Pure proof structure — converting "repeated application" into an explicit induction on chain length `k`, using V2 as base and the single-triple transitivity (already derived) as inductive step. No external channels needed.
