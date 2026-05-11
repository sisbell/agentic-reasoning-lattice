# Channel Assignment — ASN-0036 review-84

**Date:** 2026-05-11 02:29

## Issue 1: S7c postcondition (c) uses informal "ordinal-only formulation" terminology
Reason: Pure formal-reformulation task. The fix replaces an informal phrase with a direct reference to TA7a's operand precondition (o ∈ S) — both TA7a's contract and the structure of `E(a)` are already available in the ASN and ASN-0034. No design intent or implementation evidence is needed.

## Issue 2: D-CTG-depth proof omits explicit S8a verification for the constructed intermediate w
Reason: Internal proof gap. The verification follows mechanically from S8a's three conjuncts applied to the construction of w (components copied from v₁, plus n > 0 and tail 1s). All ingredients are present in the ASN; no external evidence required.

## Issue 3: S5 Depends entry conflates the two constructions' uses of T3
Reason: Documentation cleanup internal to the ASN — the two constructions and their distinct uses of T3 are already spelled out in the proof body. The fix is to split the Depends entry to match what the proof already does. No external input needed.

## Issue 4: S8's existence proof and the k ≥ 1 subspace-preservation derivation are loosely connected
Reason: Structural reorganization of an internal proof. The choice between (a) extracting subspace preservation as a corollary or (b) tagging the k ≥ 1 derivation as an auxiliary fact is a presentation decision derivable from the ASN's own definitions of correspondence runs and S7c. No external evidence needed.
