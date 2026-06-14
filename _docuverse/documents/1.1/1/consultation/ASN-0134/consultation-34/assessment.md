# Channel Assignment — ASN-0134 review-34

**Date:** 2026-06-14 09:06

## Issue 1: The K.σ-scoping exposition is restated in full at five sites
Reason: Purely editorial deduplication. The three facts being consolidated (caller-supplied `d`, same-`d` collision resolved by rejecting the loser, freshness as an assumed precondition supplied by the excluded entity layer) are all already established in the ASN; the fix is to designate §4 as the canonical site and replace the other four with pointers. No new design intent or implementation evidence is involved.

## Issue 2: §4's closing paragraph recapitulates its own per-instance analysis
Reason: Purely editorial. The synthesizing claim to retain (two-level step-vs-operation framing, "two families part company under discipline") and the per-instance derivations to drop are both already present in the section; the fix removes redundancy without altering any claim.

## Issue 3: Numbering/ordering justifications and a use-site inventory (minor)
Reason: Purely editorial. Removing document-ordering asides (V1's placement, W4's deferral) and the SAFE(b)/W5/OQ9 use-site inventory is a presentation change over content already in the ASN; no design intent or implementation fact is needed to decide where claims sit or which downstream sites cite them.
