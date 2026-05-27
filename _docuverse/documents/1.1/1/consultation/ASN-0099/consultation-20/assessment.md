# Channel Assignment — ASN-0099 review-20

**Date:** 2026-05-26 22:24

## Issue 1: 𝒮 terminology conflates allocator state with full system state
Reason: Fix is a local definition/citation correction. The ASN already references Σ with components (C, L, M, E, R) throughout; either define 𝒮 locally as the full system state space or write the signatures without the misleading ASN-0034 citation. No external evidence needed.

## Issue 2: "Verifying F17" attributes Σ.L preservation to wrong claim
Reason: Fix is a citation handle correction internal to the ASN. The reviewer identifies exactly where the citation should land — A1 supplies Σ'.L = Σ.L directly, and F17 then takes that equality as its premise. No expert input required.

## Issue 3: F4's "weakening" branch frames F1 simultaneously as definition and consequence
Reason: Fix is a one-sentence meta-framing clarification. The reader's promise is already articulated extensively in the ASN ("Why intersection rather than containment", "The reader's promise rests on this singleton-overlap reading"); the fix is to surface F1's role as the reference predicate for F3 in the F4 derivation. Derivable from the ASN's own content.

## Issue 4: F2-sco's "dom(Σ.L) ∩ S" implicitly extends matches predicate domain to S
Reason: Fix is a well-definedness note about the match predicate's own domain. F1 itself shows `matches` consults `|Σ.L(a)|`, so its undefinedness outside `dom(Σ.L)` is intrinsic to the existing definition. No external channel needed.
