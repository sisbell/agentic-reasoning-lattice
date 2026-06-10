# Channel Assignment — ASN-0126 review-86

**Date:** 2026-06-10 03:22

## Issue 1: Justificatory clause embedded in the well-formedness definition
Reason: Internal. The fix removes a forward-justification clause and states the two conditions plainly — both conditions ("shape values lie in `{Unary, Binary, Multi}`" and "coverage-class keys are unique") are already present verbatim in the sentence, and the well-definedness consequence is already carried by the next sentence. Pure prose restructuring, no design intent or implementation evidence required.

## Issue 2: Significance/dependency clauses that don't advance the local argument
Reason: Internal. The fix deletes two motivational/dependency asides ("— the guarantee a consuming app relies on" and "is what P3 rests on"), leaving complete sentences whose substantive content is already in the ASN. Pure deletion, no channel needed.
