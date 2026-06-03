# Channel Assignment — ASN-0101 review-35

**Date:** 2026-06-03 16:55

## Issue 1: LP-family extension catalogue claims exhaustiveness but omits LP-Sub, LP-Fin, and LP-Fin Corollary
Reason: Internal fix. The required dispatch follows the same pattern the ASN already uses for state-relative, tumbler-structural lemmas: LP-Sub reads off `dom(C') = dom(C)` and `dom(L') = dom(L)` via D2/D3, while LP-Fin and its Corollary depend only on canonical-span structure over F with no transition-vocabulary dependence. No design intent or implementation evidence is needed — the fix is adding a catalogue row (or scoping the exhaustiveness sentence) entirely from D2, D3, and the existing dispatch logic.
