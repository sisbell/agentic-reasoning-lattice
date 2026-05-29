# Channel Assignment — ASN-0036 review-165

**Date:** 2026-05-29 04:36

## Issue 1: S8a is an admitted alias retained "for downstream citation"
Reason: Pure structural dedup — fold the per-component form into the domain-restriction axiom or keep S8a as sole carrier, and drop the justification phrase. The decision rests entirely on the ASN's own property structure; no design intent or implementation evidence bears on it.

## Issue 2: The S8a ≡ `zeros(v)=0` equivalence is restated four times
Reason: Editorial deduplication — state the equivalence once at S8a's carrier and remove the restatements. Fully derivable from the ASN's existing text.

## Issue 3: "Strand" is never defined
Reason: The fix is to add a one-line definition tying "strand" to the two-component state `(Σ.C, Σ.M)` or rename to match the body's "two-stream" vocabulary; both options are internal to the ASN's already-stated model and need no external channel.

## Issue 4: "Why the axiom is needed" prose on the domain-restriction axiom
Reason: Drop or compress meta-justification already carried by the axiom label — purely editorial, derivable from the ASN alone.
