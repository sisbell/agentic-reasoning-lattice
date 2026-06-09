# Channel Assignment — ASN-0118 review-6

**Date:** 2026-06-08 22:04

## Issue 1: Resolution machinery reinvents ASN-0058's content-reference algebra
Reason: Internal — the fix is to cite ASN-0058's existing `ContentReference`/`ContentReferenceSequence`/`resolve` definitions and define the flat sequence as the expansion of its run-pair output. No design intent or implementation evidence is needed; both ASNs are already present.

## Issue 2: CP0(a) duplicates ASN-0058 C1 (ResolutionIntegrity)
Reason: Internal — once Issue 1 lands, CP0(a) simply cites ASN-0058 C1 (and C1b/C2) rather than re-deriving from S3★. The needed result lives in a foundation already in scope.

## Issue 3: Partial-binding behavior is silently decided by `act`, yet listed as an Open Question
Reason: The choice between adopting ASN-0058's full-binding precondition (partial binding deferred) versus declaring silent-skip-by-restriction the intended semantics turns on what a span-set is *meant* to designate (Nelson) and on what the implementation actually does with an unbound interior position (Gregory).
Nelson question: When a span designates content "exactly," does the design require every named position to be bound — i.e., is a partially-bound span ill-formed — or may COPY designate only the bound subset?
Gregory question: When a COPY/transclusion span covers V-positions that have no current binding in the source arrangement, does udanax-green reject the operation, skip the unbound positions, or something else?

## Issue 4: S8a of the *placement* positions is attributed to a shift lemma that covers only displaced content
Reason: Internal — S8a for `p + i` follows from `p` being a valid insertion position (S8a-valid) and `shift` preserving S8a via OrdShiftHom (ASN-0036), all already cited in the ASN. The fix is swapping the citation, not new evidence.
