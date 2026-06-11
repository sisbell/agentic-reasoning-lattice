# Channel Assignment — ASN-0121 review-37

**Date:** 2026-06-11 16:51

## Issue 1: `findlinks` shadows a foundation symbol with different semantics
Reason: The fix is internal — the collision is between two symbols in our own formalization (this ASN's FL-DEF vs. ASN-0127's F-FIND), and the review already fully characterizes their semantic differences (positional vs. slot-agnostic, filtered vs. unfiltered, opposite monotonicity). Renaming/disambiguating and correcting the ASN-0086 attribution requires no design-intent or implementation evidence.

## Issue 2: Trace 6 does not fix its starting store, and its results are correct only on the base store
Reason: Purely internal bookkeeping in the worked example — Trace 6 needs the same explicit reset clause Trace 7 already uses, and the correct answer sets on the base store are already computed in the ASN. No external evidence bears on which store a trace starts from.

## Issue 3: FL-JUNK's formal hypothesis mismatches its own gloss and is stronger than the proof uses
Reason: The fix is derivable from the ASN's own proof, which uses nullified-equality only on existing links; the weakened hypothesis `nullified(Σ') ∩ dom(Σ.L) = nullified(Σ)` is verifiable against the proof text as it stands, and the born-nullified-junk regime is already established internally by FL-WP(a)/Trace 7(a). Nelson's 4/60 claim is already quoted and the weakening widens coverage toward it, raising no new intent question.
