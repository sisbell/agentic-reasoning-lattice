# Channel Assignment — ASN-0126 review-81

**Date:** 2026-06-10 02:07

## Issue 1: Tangential R0 aside misstates its own proof
Reason: The fix is a pure deletion derivable from the ASN itself — the actual use of R0 (value-shape consequence to discharge L3, a static fact in the P5 proof two paragraphs down) is already present in the text, and the required action is simply to remove the mismatched parenthetical. No design intent or implementation evidence bears on whether this digression should stay.

## Issue 2: Closing "safety/liveness" paragraph restates settled results
Reason: The fix is to cut a paragraph that merely restates P3 and P5, both proven earlier in the same note; nothing about design intent or the implementation is at stake, and the redundancy is fully visible within the ASN.
