# Channel Assignment — ASN-0117 review-4

**Date:** 2026-06-08 22:22

## Issue 1: wp derivation's intermediate range identity drops the link-subspace images
Reason: Internal fix — the ASN already contains every fact needed (DEL-FSUB preserves `s_L` images verbatim, `A_del` lives in `s_C`, LP12 evaluates against full `ran(M(d))`). Correcting the intermediate identity is a matter of carrying the unchanged link-subspace images through the derivation, no design intent or implementation evidence required.

## Issue 2: P2's gap-closure clause is stated unconditionally but is undefined on the suffix-delete boundary
Reason: Internal fix — ASN-0082's D-SEP already splits into the unguarded arithmetic identity D-SEP(a) and the `R ≠ ∅`-guarded positional reading D-SEP(b), and the worked example already notes the suffix case is vacuous. Conditioning P2's clause is derivable from cited content alone.
