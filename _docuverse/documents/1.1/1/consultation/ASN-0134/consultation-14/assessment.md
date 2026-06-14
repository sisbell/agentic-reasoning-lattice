# Channel Assignment — ASN-0134 review-14

**Date:** 2026-06-13 23:53

## Issue 1: The "not K-surface-emitted" claim — on which clause 8's necessity rests — contradicts ASN-0128's literal definition and is left unreconciled
Reason: The fix is a formal reconciliation entirely internal to the corpus. The review already quotes both load-bearing pieces — ASN-0128's *definition* of K-surface-emitted ("every L_K-growing step … is the deposit branch of an Emit_K invocation") and its I1a *proof* text ("the deposit branch … fires only on a miss: at the pre-state its I0-class had no active member") — and ASN-0134 itself already supplies the missing premise (Y's deposit pre-state is Σ ∪ {T_X}, "where it would be a hit"). Drawing the literal-vs-operative distinction and showing Y's deposit fails the miss-at-own-pre-state condition is pure logical assembly from definitions and proofs already present; neither design intent nor implementation evidence bears on it.

## Issue 2: The batch taxonomy omits the empty (m=0) and singleton (m=1) boundaries, while asserting exhaustiveness and non-atomicity
Reason: The degenerate boundaries are direct consequences of ASN-0134's own definitions plus ASN-0128's BH4 ("one Nullify_Binary per stale event"): an empty stale set yields zero steps (vacuously atomic), a singleton yields one step (atomic, behaving as a single operation). Scoping A5's non-atomicity to m ≥ 2 and stating the two boundaries is mechanical from the cited definitions; no question of design intent or implementation behavior arises.
