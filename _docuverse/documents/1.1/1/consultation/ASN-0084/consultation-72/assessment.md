# Channel Assignment — ASN-0084 review-72

**Date:** 2026-05-30 15:25

## Issue 1: Multiset-of-I-addresses preservation is a dead derivation
Reason: Purely internal editorial deletion — the fix removes a derivation whose only consumer (S5) is shown by the ASN's own text to be a non-obligation, and retains the set-equality that R-RI already uses. No design intent or implementation evidence bears on whether to keep a non-advancing proof.

## Issue 2: R-NS proof re-derives what the frame condition already supplies
Reason: Internal proof-hygiene fix — the redundant substitution recovers an equation the ASN itself concedes the frame condition already supplies. Derivable from the ASN's own logical structure alone.

## Issue 3: R-PPERM "Remark (uniqueness scope)" is a non-advancing aside
Reason: Internal scope decision — the ASN's own definitions and consumers (R-RI, R-BLK) require only existence of a bijection, not uniqueness, so the remark is provably unused by the specification's own claims. No external channel needed.
