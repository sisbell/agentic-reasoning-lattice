# Channel Assignment — ASN-0069 review-87

**Date:** 2026-06-03 01:26

## Issue 1: V8c states the correspondence set over (d_src, d_new), but V8 establishes it over (d_op, d_new)
Reason: The fix is fully internal — V8's own statement already quantifies over `d_op`, and the operand frame `M'(d_op) = M(d_op)` is already invoked in V8's derivation. Correcting V8c's set and V8's heading to track `d_op` is a mechanical alignment with content already present in the note; no design intent or implementation evidence is required.
