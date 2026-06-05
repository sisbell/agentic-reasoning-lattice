# Channel Assignment — ASN-0113 review-7

**Date:** 2026-06-05 00:43

## Issue 1: The non-trivial mechanism of W4/W10 is never exercised by a concrete instance
Reason: The fix is purely internal — it asks for an additional worked instance at `m_S ≥ 3` using machinery (T5, T1, VSlice, `ext`, `δ`, D-SEQ★) already fully defined in the ASN; the required tumblers and exclusion check are mechanically derivable from the note's own definitions, requiring neither design intent nor implementation evidence.
