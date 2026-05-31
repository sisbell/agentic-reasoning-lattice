# Channel Assignment — ASN-0043 review-163

**Date:** 2026-05-31 01:40

## Issue 1: The "Postcondition: T4-validity of a" paragraph is filed under CPP but does not use CPP
Reason: This is a structural/exposition fix entirely internal to the ASN — separating CPP's own positions-`1..p` conclusion from L1c's discharged postconditions, where the derivations (T10a.4 induction, two CPP invocations) are already present in the text. No design intent or implementation evidence bears on how the proof slots are organized.

## Issue 2: L0b's body re-derives well-definedness already established twice upstream
Reason: This is an internal redundancy fix — trimming L0b's justification to the lifting step it uniquely contributes, since the well-definedness it restates is already established in the CPP postcondition and the Notational convention. Derivable from the ASN's own content alone.
