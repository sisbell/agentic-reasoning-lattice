# Channel Assignment — ASN-0116 review-48

**Date:** 2026-06-09 17:15

## Issue 1: Precondition-discharge prose is duplicated between the Effect/allocation sections and the valid-composite section
Reason: The fix is purely structural deduplication internal to the ASN — relocating each precondition discharge to a single authoritative site (the valid-composite section) and replacing the inline copies with pointers. Both the postconditions and the full discharge arguments (including the `findpreviousisagr` grounding) are already present in the ASN; nothing about design intent or implementation evidence is in question, only where each obligation is discharged.
