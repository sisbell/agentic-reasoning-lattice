# Channel Assignment — ASN-0100 review-77

**Date:** 2026-06-05 04:38

## Issue 1: INS.identity.version corollary adds nothing INSERT-specific and reaches into out-of-scope version machinery
Reason: Purely structural fix — the corollary is redundant with INS.alloc (`origin(a_k) = d` holds for any target document), and Scope already excludes version derivation. Removing or restating as an INS.alloc instance is derivable from the ASN's own claims.

## Issue 2: Verbatim repetition of the freshness-boundary parenthetical across sections
Reason: Editorial deduplication — state the freshness fact once at INS.alloc and cite it downstream. The lemma content is unchanged; no design intent or implementation evidence is in question.

## Issue 3: Reviser-drift sentence defends a case the frame trivially discharges
Reason: Internal — `E' = E` (INS.frame.E) already discharges ActivatedEmission by frame like P8/NodeLineage/M0. Dropping the circular witness sentence follows from the ASN's existing frame argument.

## Issue 4: The INSERT-vs-COPY section is essayistic and partly restates INS.identity
Reason: Editorial trimming — the load-bearing contrast (INSERT allocates fresh; COPY references without allocating) and the genuine corollaries are already established; removing the re-narration needs no external input.
