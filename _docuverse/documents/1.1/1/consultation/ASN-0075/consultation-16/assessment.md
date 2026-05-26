# Channel Assignment — ASN-0075 review-16

**Date:** 2026-05-25 17:34

## Issue 1: Implicit content value assumption in D-DISCR construction
Reason: Internal fix — K.α's signature (v ∈ Val as caller-supplied parameter) is already established in the ASN's foundation. The required revision is to make the value-equality choice explicit in the construction's prose; no design intent or implementation evidence is needed.

## Issue 2: "Immediately following" overstates bundling requirement
Reason: Internal fix — J0's semantics as a composite-boundary coupling (not adjacency-requiring) is established in ASN-0047, which is already cited. The revision is a terminology correction consistent with the existing framework.

## Issue 3: Bijection between equivalence classes and witness runs left implicit
Reason: Internal fix — the bijection is constructible from definitions already present in the ASN (T1-minimum, cardinality, shared origin from the equivalence relation). The revision makes the implicit construction explicit; no external input needed.
