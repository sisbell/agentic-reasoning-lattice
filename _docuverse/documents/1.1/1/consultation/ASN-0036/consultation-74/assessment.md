# Channel Assignment — ASN-0036 review-74

**Date:** 2026-05-10 23:39

## Issue 1: S7c's load-bearing role is misattributed
Reason: Internal cross-reference correction — the ASN's own structure shows S7c is consumed by S8's I-address shift definition, not by S8-depth. Derivable from ASN content alone.

## Issue 2: S3's claimed dependency on NoDeallocation is unsubstantiated
Reason: Internal consistency between table and body — the body cites S1, so either align the table with what's used or invoke NoDeallocation in the body. Both options are derivable from ASN-0036 and ASN-0034 content.

## Issue 3: S7's cross-document uniqueness invokes GlobalUniqueness without an explicit allocation-event premise
Reason: Need Nelson to confirm whether documents are intended to be allocated under user prefixes via T10a's baptism discipline (the baptism principle is already cited but not formally tied to document-level allocation). Gregory not needed — this is about design commitment, not implementation evidence.
Nelson question: Does Nelson's baptism principle commit documents themselves to being allocated as document-level tumblers (zeros = 2) under their owning user's prefix via the same allocator discipline that produces I-addresses, so that distinct document creations are distinct allocation events under T10a?

## Issue 4: D-CTG's parametric statement and text-only restriction don't line up
Reason: Internal formalization fix — the ASN already establishes the text-only restriction in prose; the task is to bind it into the formal statements. Derivable from ASN content alone.

## Issue 5: Issue with j = m case argument in S8 uniqueness proof
Reason: Pure proof-gap fix — the review supplies the exact bridging sentence using TumblerAdd's prefix rule already cited elsewhere in the proof. Derivable from ASN content alone.
