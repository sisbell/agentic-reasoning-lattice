# Channel Assignment — ASN-0040 review-60

**Date:** 2026-05-28 22:47

## Issue 1: Stray/incorrect citation "(by B4)" in the B1 proof
Reason: Purely editorial — the contiguous-prefix form comes from the inductive hypothesis (B1 at state B), and B4's role (single-state read) is unrelated. Deleting the misattributed citation is derivable from the ASN's own proof structure.

## Issue 2: B6 necessity of condition (i) conflates T4-preservation with namespace disjointness, and the d=1 branch depends forward on B7
Reason: The fix is a structural choice between two internally-derivable options (drop the d=1 collapse argument, or relabel it as motivation) — both resolvable from the existing necessity sub-cases (a) and (b) d=2, which already establish (i) for T4. No design intent or implementation evidence needed.

## Issue 3: Triplicated induction scaffolding across B1, B_fin, B10 (anti-bloat)
Reason: Pure refactoring — factor the shared B0a frame/baptismal case-split into one cited lemma. The lemma content is already stated in B0a; nothing external is required.

## Issue 4: B9 trace re-argues the general unbounded claim instead of exhibiting the M=5 instance
Reason: Editorial trim — the trace should instantiate (M=5 in three baptisms) rather than re-prove the no-ceiling theorem already in B9's proof. Fully internal.
