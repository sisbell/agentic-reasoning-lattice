# Channel Assignment — ASN-0107 review-20

**Date:** 2026-06-08 11:38

## Issue 1: P0a cites LP21 for a fact about raw request sets, where it does not apply
Reason: The fix is internal — the ASN already states the correct ground ("immediate from `sat`, which consults `Qᵢ` only set-wise"), and the definition of `Q` as raw address sets is given in the ASN itself. Dropping or replacing the LP21 parenthetical requires no external design intent or implementation evidence.

## Issue 2: Essay-content closers in structural slots (anti-bloat)
Reason: This is a pure editorial cut of rhetorical restatements; identifying and removing meta-commentary is derivable from the ASN's own text with no design-intent or implementation question at stake.
