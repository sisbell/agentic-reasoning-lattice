# Channel Assignment — ASN-0047 review-148

**Date:** 2026-05-31 15:29

## Issue 1: First content V-position depth is not pinned by K.μ⁺'s precondition
Reason: The fix is internal — `ValidFirstInsertionPosition(d, v, m)` is an existing ASN-0036 foundation predicate already cited in the ASN; the change merely wires it into K.μ⁺'s precondition for the `V_{s_C}(d) = ∅` case, mirroring how K.μ⁺_L cites LinkVPositionDepthAxiom. No design intent or implementation evidence is needed.

## Issue 2: Within-account entity-distinctness discharge is too narrow
Reason: The fix is internal — T10a.6 (DomainDisjointness) and T10a GlobalUniqueness are foundation properties already in use throughout the ASN; the same-parent-account cross-chain case is dischargeable directly by these existing lemmas without new evidence.

## Issue 3: Essay prose around LinkVPositionDepthAxiom explaining why no companion axiom exists
Reason: The fix is internal and editorial — deleting the companion-axiom justification paragraph and relocating the one load-bearing fact (content first-insertion depth from `ValidFirstInsertionPosition`) into K.μ⁺'s precondition, which is already resolved under Issue 1.

## Issue 4: Forward-reference accretion — repeated deferral and axiom-discharge meta-commentary
Reason: The fix is internal and editorial — removing redundant "Proved as part of … below" stubs (the invariant list in ExtendedReachableStateInvariants already enumerates them) and deleting the clause-(c) self-justification parenthetical, leaving the direct axiom citation.

## Issue 5: K.α "no local amendment" downstream use-site inventory
Reason: The fix is internal and editorial — stating that K.α's content-subspace precondition is inherited from ASN-0093 and removing the catalogue of downstream citation sites; the inheritance fact is already established in the ASN.
