# Channel Assignment — ASN-0040 review-112

**Date:** 2026-05-29 05:18

## Issue 1: B8's headline guarantee is unconditional but only proved under single authority
Reason: Internal. The proof already establishes that Case 2 is authority-independent (via B7) while Case 1 relies on B-Seq's single-authority serialization, and the formal-contract precondition already carries the qualifier. Scoping the headline to match is a purely editorial alignment with content already present.

## Issue 2: B8 Case 1 relabeling asserts "WLOG" without discharging the obligation
Reason: Internal. The two facts needed to close the relabeling — B4 (atomicity excludes an intermediate read-state) and B-Seq's total-ordering/no-fork (excludes a shared read-state s₂ = s₁) — are both already axioms in this ASN. The argument can be completed from existing properties without external evidence.

## Issue 3: B8 closing paragraph is reviser drift around an excluded case
Reason: Internal. The required action is deletion of a speculative paragraph whose content is subsumed by the Issue-1 scoping; no design intent or implementation evidence is needed to remove it.

## Issue 4: B3's closing sentence reaches into out-of-scope content storage
Reason: Internal. The ASN already declares content storage out of scope (the B3 body and the opening "Authorization ... is out of scope" framing), so removing or relocating the forward content-storage constraint is determined by the ASN's own stated boundaries.
