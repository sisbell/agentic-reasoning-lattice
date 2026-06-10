# Channel Assignment — ASN-0126 review-94

**Date:** 2026-06-10 06:09

## Issue 1: Op-set carry-over paragraph re-derives results already on the page
Reason: Purely editorial — compressing redundant re-derivations into pointers and fixing the "two vs three operations" ambiguity. All referenced content (the gated `Emit_K`, the `Nullify_Binary` wrapper, `Observe_K`'s pass-through, the final set `{Emit_K, Observe_K, Nullify_Binary}`) is already present in this note, so the fix is internal to the ASN with no design-intent or implementation-evidence question at stake.
