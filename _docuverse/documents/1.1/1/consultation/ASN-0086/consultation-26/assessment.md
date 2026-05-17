# Channel Assignment — ASN-0086 review-26

**Date:** 2026-05-17 03:34

## Issue 1: Subspace-distinctness axiom framing
Reason: The fix turns on whether the foundation ASNs (ASN-0034/0036/0043) entail `s_C ≠ s_L` as a derivable fact or whether it must be acknowledged as a primitive distinctness assumption. Nelson's design intent clarifies whether subspace identifiers are meant to be primitive distinct constants in the link model; Gregory's evidence on whether the udanax-green implementation treats `s_C` and `s_L` as concretely distinct values informs which framing matches the realized substrate.
Nelson question: In your design, are subspace identifiers (specifically the content subspace `s_C` and the link subspace `s_L`) intended as primitive distinct constants of the address-space partition, or is their distinctness an emergent property derivable from other design commitments?
Gregory question: In udanax-green, are `s_C` and `s_L` (or their concrete numeric equivalents in the granfilade/POOM code paths) assigned distinct constant values, and does any code path rely structurally on their inequality (e.g., subspace-dispatch in `findisatoinsertmolecule`)?
