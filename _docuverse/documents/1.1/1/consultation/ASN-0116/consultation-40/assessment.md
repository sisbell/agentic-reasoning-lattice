# Channel Assignment — ASN-0116 review-40

**Date:** 2026-06-09 11:18

## Issue 1: Valid-composite argument forward-references the lemmas it depends on
Reason: Pure reordering and citation fix — block well-formedness, I-DOM, and the coupling discharge are all already proved within the ASN; the fix is relocating them ahead of the validity claim and swapping the restated `ValidComposite★` definition for a citation. No design intent or implementation evidence is at stake.

## Issue 2: Post-state contiguity stated in unstarred (ASN-0036) form when the operative invariants are starred (ASN-0047)
Reason: Purely a label-consistency fix internal to the ASN — the note already declares it works inside ASN-0047's extended state and already cites D-CTG★/D-MIN★ a section earlier, so aligning the contiguity conclusion to the starred forms (or noting their reduction on `s_C`) needs nothing beyond the ASN's own content.
