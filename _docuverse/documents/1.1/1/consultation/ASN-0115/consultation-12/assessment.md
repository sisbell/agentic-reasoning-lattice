# Channel Assignment — ASN-0115 review-12

**Date:** 2026-06-05 06:58

## Issue 1: V-spec start depth is not constrained to the subspace's common depth, but R6's sharpening presupposes it
Reason: Internal. The substrate facts the fix turns on (common depth `m_S`, D-SEQ★ frontier) are already cited in the ASN, and the reviewer offers two self-contained resolutions (add the `#s = m_S(d)` conjunct or scope R6 to matched-depth and dispatch the mismatch as `act = ∅`); both are derivable from definitions and claims already present.

## Issue 2: R6 worked instance states the span denotation incorrectly
Reason: Internal. The error is a pure consequence of the half-open interval definition (ASN-0053) and T1 ordering (ASN-0034) already in the ASN — `[1,2,1] ∈ ⟦σ⟧` follows directly, so restricting the displayed set to its depth-2 slice needs no external input.

## Issue 3: R8's "store membership fixes subspace" step omits S3★-aux
Reason: Internal. The missing conjunct (S3★-aux, SubspaceExhaustiveness) is already cited earlier in the same ASN for `item` totality; this is a completeness fix re-citing existing machinery, requiring no design intent or implementation evidence.
