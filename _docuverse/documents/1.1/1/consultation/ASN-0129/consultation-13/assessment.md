# Channel Assignment — ASN-0129 review-13

**Date:** 2026-06-11 19:24

## Issue 1: V's inheritance claim for default-view semantics contradicts UV
Reason: Internal — the contradiction is between two passages of this note (V's inheritance sentence vs. UV's own premise), and the fix is the same on either horn of the dilemma: scope V's sentence to active-view inheritance plus the core family's default reading, and point the behavior atoms' default readings at UV. No design-intent or implementation evidence changes that rewording.

## Issue 2: `targets_keyed` mistyped as a class-indexed template atom
Reason: Internal — the correct characterization (single global atom, cross-type by construction, well-formed iff some registered class attaches BH3) is already stated in the note's own FP and V-IDX sections; the fix is moving or annotating that characterization at the definition site in V. The hoist-vs-annotate choice is editorial structuring, not a question either channel can settle.

## Issue 3: `is_doc`'s upstream grounding misstates the foundation contracts it cites
Reason: The reviewer's quoted ASN-0128 clauses (I1's branch-local hit behavior, S3's P-tgt) supply most of the corrected wording, but the rewrite re-grounds a claim about what the emit surface actually checks, and Gregory should confirm the branch structure against the code so the new parenthetical doesn't repeat the precision failure in a new form.
Gregory question: In udanax-green's emit path, is document-residence validation performed before or after the idempotency/dedup check — specifically, does a dedup hit return the existing address without ever consulting the document store, and does the nullify path check document residence on every call?

## Issue 4: Forward-reference accretion — duplicated interpretive prose and repeated deferrals
Reason: Internal — purely editorial deduplication. The review identifies exactly which sentences duplicate UV's own clauses and the intro's repeated PC6 deferral; trimming them changes no commitment and needs no external input.
