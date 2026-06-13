# Channel Assignment — ASN-0133 review-4

**Date:** 2026-06-13 11:30

## Issue 1: Q5a omits the extinction-discipline hypothesis its proof requires
Reason: Internal — pure logical correction using definitions already present. Q-EXT's stated hypothesis (SF spelling *and* extinction discipline), X-DEF, Q3, and Q5's explicit disavowal of extinction are all in the note, and the note's own commit bullet already states the correct form ("an SF spelling **and whose fires falsify it**"). Restoring the dropped X-DEF conjunct to Q5a, the commit bullet, and the Q6 restatement is derivable from the ASN alone.

## Issue 2: the worked example's producer domain is never grounded in QD
Reason: Internal — the fix uses QD's own base catalog (M_K, A_K, L_K, L_dom, Reg) and the QD-audit rule, both already cited and exercised throughout the note. Grounding `targets` as `M_K` of a target-marking type (or a named `℘_fin(T)`-valued PL term) and confirming `needs_attention : T → Bool` is a self-contained modeling choice within the worked example's own latitude; neither Ted Nelson's design intent nor udanax-green evidence bears on a spec-level QD expressibility question.
