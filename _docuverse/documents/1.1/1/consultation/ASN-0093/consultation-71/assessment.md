# Channel Assignment — ASN-0093 review-71

**Date:** 2026-05-31 12:44

## Issue 1: Duplicate statement about where the two derived inductions live
Reason: Pure editorial deduplication — strike the post-matrix sentence and trim the meta-clause from the framing paragraph. No design intent or implementation evidence is involved.

## Issue 2: StoreT4Validity asserts a T4-valid seed without deriving it
Reason: The seed's T4-validity is supplied internally by C2 (`origin(a) ∈ dom(M)`) and M0 (`dom(M)` is T4-valid with `zeros = 2`), both already proved in the ASN; the symmetric link case uses L1a + M0. Fully derivable from the note's own content.

## Issue 3: B5a cited without discharging its precondition
Reason: The precondition `a_prev_{sig} > 0` follows from `a_prev` being T4-valid (ChainElementT4Validity) plus TA5-SigValid placing `sig(a_prev) = #a_prev` at the nonzero terminal — all citations already present in the ASN, mirrored in the C1b cell. Internal.

## Issue 4: Worked-example closing line is an exhaustiveness/coverage claim
Reason: Straight deletion of a meta-summary sentence whose content is already visible in the worked steps. No external input needed.
