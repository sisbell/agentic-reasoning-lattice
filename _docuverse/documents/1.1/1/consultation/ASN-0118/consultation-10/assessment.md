# Channel Assignment — ASN-0118 review-10

**Date:** 2026-06-08 22:51

## Issue 1: S8-depth not discharged for the placement (gap-fill) positions
Reason: The fix is fully derivable from the ASN's own already-cited machinery — ValidInsertionPosition/ValidFirstInsertionPosition give `#p = m_{s_C}(d)`, and shift preserves tumbler length (`#shift(p,i) = #p`), exactly mirroring the S8a patch the ASN already performs via OrdShiftHom(b). No design intent or implementation evidence is required; this is a one-line invariant discharge using axioms the ASN already invokes.
