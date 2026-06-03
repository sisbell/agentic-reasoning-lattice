# Channel Assignment — ASN-0075 review-64

**Date:** 2026-06-03 10:37

## Issue 1: The "no-write" fact is stated three times, with a forward-pointer announcing the duplication
Reason: Pure editorial deduplication — the fix is to state the no-write fact once and invoke it by label. No design intent or implementation evidence is needed; the ASN's own structure determines the fix.

## Issue 2: D-OBS repeats verbatim prose from the operation-definition paragraph
Reason: Internal prose deduplication — keep the formulation in D-OBS and delete the duplicate. Derivable from the ASN alone; no channel needed.

## Issue 3: DELETED-vs-NEVER_INCLUDED distinction is re-explained across three sections
Reason: Structural consolidation of overlapping prose around the existing D-DISCR/D-NEED carriers. The set-difference-conflation point and its folding are internal editorial decisions requiring no external channel.

## Issue 4: D-ACT is a content-free restatement of D-IDENT
Reason: The review itself directs removal, and whether D-ACT adds content is judged against this ASN's own claims (no consuming operation is in scope here). Internal; no channel needed.
