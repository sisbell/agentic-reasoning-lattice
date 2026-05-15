# Channel Assignment — ASN-0058 review-27

**Date:** 2026-05-14 20:52

## Issue 1: M16a omits T4-validity verification for the shifted address
Reason: The fix is internal — verifying the four T4 conjuncts for `a + k` follows mechanically from TumblerAdd's behavior (only the last component changes, from `a_{#a} ≥ 1` to `a_{#a} + k ≥ 1`) and the ASN's already-established T4-validity of `a`. No design intent or implementation evidence is needed.

## Issue 2: Title and body use inconsistent terminology
Reason: The choice between renaming to "Mapping Block Algebra" versus formally introducing "bundle" depends on whether Nelson used "bundle" as a designed term with specific semantic content distinct from mapping block. Nelson can confirm whether "bundle" appears in Literary Machines as a load-bearing term or whether the title is stale drafting.
Nelson question: Does Nelson use "bundle" as a defined term in Literary Machines (or the concept notes) with a meaning distinct from an I-span / mapping block — and if so, what does it denote?
