# Channel Assignment — ASN-0058 review-29

**Date:** 2026-05-14 21:49

## Issue 1: M16a's T4-validity derivation has an unjustified descendancy step
Reason: The fix is a proof restructuring that cites S7b's existing postcondition (ASN-0036) directly instead of routing through the T10a allocator-tree closure. The review specifies the simpler route, and both ASN-0058 and the cited foundation axioms contain everything needed.

## Issue 2: Four-step structural skeleton is duplicated across M2, M7-cov, M12a
Reason: This is a structural refactoring — extract a tumbler-interval-characterization lemma stated over foundation preconditions (S8a, S8-depth, TumblerAdd, T1). The skeleton already exists in three places; consolidating it requires no design intent or implementation evidence, only proof reorganization within the ASN.

## Issue 3: M12a's "Equal widths" sub-case relies on a hidden symmetry argument
Reason: The fix is a single explicit sentence invoking NAT-order trichotomy to close the residual `n_1 = n_2` case. Purely internal proof hygiene — derivable from the ASN's own structure.

## Issue 4: M16a's k=0 case in (b) of M-sub is asymmetric with k=0 case in (a)
Reason: The fix adds a one-line note citing S7b (`zeros(a) = 3`) and S7c (`#E(a) ≥ 2`) from ASN-0036 to explain why the I-side has no analogous sharpness case. M16a itself already derives `#a ≥ 8` from these axioms, so the fix is purely a cross-reference within the ASN.
