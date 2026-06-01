# Channel Assignment — ASN-0086 review-104

**Date:** 2026-05-31 20:12

## Issue 1: Emit_K function-ness misattributes max-uniqueness to R0a-Cor1
Reason: Fully internal. The fix substitutes T1's strict total order plus L-fin finiteness for the R0a-Cor1 appeal — both already cited in the ASN — and the argument that any finite non-empty subset of a strict total order has a unique max is self-contained. No design intent or implementation evidence is at stake.

## Issue 2: "substrate-conforming state" and "substrate-conforming layer" definitions duplicate and then diverge
Reason: Internal. Whether L5/L6/L8 already belong to the "full L/S/M/C invariant catalog" is a fact about the referenced ASN-0043 invariant taxonomy within the same formal corpus, and the remedy (state the catalog once, or drop the "exactly the two conditions" claim and re-justify) is an editorial self-consistency choice derivable from the ASN's own framing — not Nelson's design intent or udanax-green behavior.
