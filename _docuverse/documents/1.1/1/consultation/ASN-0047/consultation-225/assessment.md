# Channel Assignment — ASN-0047 review-225

**Date:** 2026-06-01 06:41

## Issue 1: Fork section explains the same excluded case twice
Reason: Pure editorial deduplication — both paragraphs re-derive the link-only-source exclusion already entailed by the `V_{s_C}(d_src) ≠ ∅` precondition (via S3★ content clause and L14, all present in the ASN). No design intent or implementation evidence is needed to consolidate the rationale into one clause.

## Issue 2: "K.μ~ is a named composite, not a primitive transition" restated across slots
Reason: Pure editorial deduplication — the compositional status is established at the definition site (*Decomposition of K.μ~*); removing the repeated disclaimers and referencing the named definition is internal to the ASN's own structure, requiring no external channel.
