# Channel Assignment — ASN-0047 review-279

**Date:** 2026-06-01 19:21

## Issue 1: "Links not rearrangeable" is asserted but not enforced by the invariants
Reason: The choice between weakening the narrative (option a) and adding a position-pinning invariant (option b) turns on whether the design truly mandates permanent link order-of-arrival and whether the implementation actually prevents re-seating; this requires both design intent and implementation evidence.
Nelson question: Does the design intend a link's order-of-arrival position in its home document to be a permanent, unrearrangeable guarantee — or merely that links are withdrawable with no positional-stability promise?
Gregory question: When a link is withdrawn from a document's arrangement and later re-arranged (or when links are removed and re-added), does the implementation preserve each link's original V-position/order-of-arrival, or can a link end up at a different position?

## Issue 2: J4 intro duplicates the fork/sibling discriminator that Definition (Fork) claims to state "once"
Reason: This is a purely editorial deduplication — the contradiction between the "sole statement" disclaimer and the duplicated discriminator prose is resolvable entirely within the ASN by relocating the content to one location.
