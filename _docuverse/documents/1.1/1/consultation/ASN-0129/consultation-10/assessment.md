# Channel Assignment — ASN-0129 review-10

**Date:** 2026-06-11 16:18

## Issue 1: The conservativity accounting omits the store-domain enumeration bases, and `C_dom` is admitted without a ground
Reason: The audit restructure and the PC4 mechanism-sentence fix are internal (all three read routes are already named in PC6/FP), but the ground-vs-drop decision for `C_dom` needs evidence: `M_dom`'s ground is "what the emit surface checks," so the parallel question is whether any real surface operation checks or reads bare content existence.
Gregory question: Does any read or link-creation operation in udanax-green test or enumerate bare content existence — e.g., validating that an endset's I-addresses hold stored content before depositing the link — or is content only ever reached through document arrangement (V→I) reads, with no content-store existence check anywhere on the query or gating path?

## Issue 2: COD omits bare `T` while the note types terms at `T`
Reason: Internal — this is a coherence fix in the note's own type system; either resolution (add `T` to Codom with the evident coercion, or declare `T`-typed forms the defined fragment of `T ∪ {⊥}`) is executable from V-TUP, PC2, and V-PRIM as written.

## Issue 3: UV — the note's settlement of ASN-0128 Open Question 1 — is never exercised against a concrete state
Reason: Internal — the required trace extension is a mechanical evaluation of UV's already-committed rewrite/preservation rules at a constructible state, using gates and landing facts (Unary gate, C3, R0a, frontier-landing) the note already cites from its dependency cone; the review even supplies the construction.

## Issue 4: Duplicated fences and deferrals across sections (anti-bloat)
Reason: Internal — purely editorial consolidation of repeated scope statements to their canonical sites; no semantic content changes and no design-intent or implementation facts are involved.
