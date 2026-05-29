# Channel Assignment — ASN-0040 review-76

**Date:** 2026-05-29 00:54

## Issue 1: The "necessity" proof for B6 condition (i) conflates two distinct properties and forward-references results that depend on it
Reason: The fix is internal restructuring — separating the genuine T4-preservation theorem (already proved in the ASN) from the S2-aliasing design rationale (also already present, via S2, B7, B8). No design intent or implementation evidence is needed; the circularity and the split are both resolvable from the ASN's own content.

## Issue 2: B6 necessity carries defensive meta-prose and a redundant closing restatement (reviser drift)
Reason: Pure deletion/consolidation of redundant prose and forward pointers already in the text. Nothing external is required to identify and remove duplicated restatements.

## Issue 3: B0★ multi-step proof is asserted, not shown
Reason: The fix is to write the explicit induction (reflexive base + transitive step), a mechanical expansion derivable directly from B0 and the definition of reflexive-transitive closure already in the ASN. No channel needed.
