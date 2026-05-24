# Channel Assignment — ASN-0051 review-81

**Date:** 2026-05-23 16:56

```
## Issue 1: SV11 attainment witness (m ≥ 1, p = 1) — worked example doesn't match the parametric form it claims to extend
Reason: This is an internal consistency issue between two parts of the same ASN. Both constructions (5-sibling gap-2 and 2m-1-sibling gap-1) are self-consistent witnesses already verified in the ASN; the fix is purely editorial wording — either rewrite the worked example to instantiate the parametric form, or reword the generalisation as an alternative witness.
```

```
## Issue 2: CrossDocumentDecoupling K.δ case terminology imprecise
Reason: This is a citation correction against the foundation ASN-0047's K.δ case structure (case (ii) k=0 with IsDocument effect path), which the reviewer has already characterised. The fix is derivable by reading ASN-0047 directly; no Nelson design-intent or Gregory implementation evidence is needed beyond aligning terminology with the cited foundation.
```

```
## Issue 3: SV5 cites "K.μ~'s ran-preservation corollary (ASN-0047)" but ASN-0047 has no such labelled corollary
Reason: This is a citation precision issue. The reviewer has already identified that ran-preservation follows directly from K.μ~'s bijection equation in ASN-0047 (which is labelled), and the fix is either to reword the derivation in-line or to add the labelled corollary to ASN-0047 first. Both options are internal authorial decisions about citation style.
```
