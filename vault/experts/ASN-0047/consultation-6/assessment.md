# Revision Categorization — ASN-0047 review-6

**Date:** 2026-03-17 03:54

## Issue 1: K.α preconditions embedded in prose, not formalized
Category: INTERNAL
Reason: The preconditions (origin(a) ∈ E_doc, IsElement(a), a ∉ dom(C)) are already stated in the ASN's prose — the fix is reformatting them into explicit `*Precondition:*` blocks matching K.δ's structure.

## Issue 2: J1/J1' biconditional characterization overstated for re-addition
Category: INTERNAL
Reason: The formal J1 and J1' are correct as stated; the fix is confined to replacing an imprecise prose summary with a precise one, and splitting P4's K.μ⁺ case into two subcases (new vs. already-in-R). All reasoning is derivable from definitions already in the ASN.

## Issue 3: Historical fidelity of R claimed without derivation
Category: INTERNAL
Reason: The review itself identifies all the building blocks (J1', P2, P0) as present in the ASN — the fix is writing out the inductive chain connecting them, which requires no external evidence.
