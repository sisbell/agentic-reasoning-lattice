# Revision Categorization — ASN-0043 review-42

**Date:** 2026-04-09 15:56



## Issue 1: Non-transcludability of links is derived but claimed as deliberate
Category: INTERNAL
Reason: The fix is purely about formal presentation — either promote the derived property to an independent invariant or weaken the prose claim. All the definitions, evidence, and design reasoning are already present in the ASN; no external consultation is needed to decide how to restructure the formal dependency.

## Issue 2: L9 witness — L1c verification does not handle initial allocation
Category: INTERNAL
Reason: The fix requires adding the child-spawning sequence for the initial allocation case, which is fully derivable from T10a and TA5a already cited in the ASN. The allocation discipline mechanics are established in ASN-0034; no implementation evidence or design-intent clarification is needed.
