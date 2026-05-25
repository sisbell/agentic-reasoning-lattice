# Channel Assignment — ASN-0069 review-6

**Date:** 2026-05-25 13:41

## Issue 1: V1's IsDocument argument for the subsequent-fork sub-case is implicit
Reason: The fix is internal — the required induction parallels V2's existing structural-ancestry induction and uses machinery (KDeltaZerosK01, P1) already cited in the ASN; the V0 verification section already spells out the inductive argument, so V1 just needs to inline it.

## Issue 2: V8b's membership criterion elides the domain conjunct
Reason: The fix is internal — V8b already supplies the precise definition `Π_g := F ∩ Corr_g` and Corr_g's domain conjunct; the text-level restatement just needs to align with the formal definition, which is a presentation fix using content already present in the ASN.
