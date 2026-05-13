# Channel Assignment — ASN-0043 review-49

**Date:** 2026-05-13 09:51

## Issue 1: TA5a wording attributes a constraint where none exists
Reason: Pure citation fix against ASN-0034's TA5a guarantee, which is already part of the lattice. The reviser corrects wording at two sites to match TA5a's actual statement — no design intent or implementation evidence is needed.

## Issue 2: L1a's English claim is stronger than its formal statement (allows non-registered "documents")
Reason: Choosing between tightening the formal statement (requiring `d` to be S7d-allocated) versus weakening the English (structural document-level-ness only) hinges on design intent — was MAKELINK always meant to operate under an existing/registered document? — and on what `docreatelink` actually requires of its document parameter.
Nelson question: Does Xanadu's design require that a link's home document be an already-created document (with an owner), or is it permissible for a link to be created under a structurally well-formed document-level prefix that has not been allocated as a document in the system?
Gregory question: Does `docreatelink` (and the chain through `findisatoinsertmolecule`) require the document parameter to refer to a document that has been previously created in the granfilade, or will it allocate a link address under any structurally valid document-level tumbler prefix?

## Issue 3: GlobalUniqueness cited under an unrecognized name
Reason: Naming alignment with ASN-0034's canonical label `GlobalUniqueness`; the reviser drops the parenthetical "UniqueAddressAllocation" at all sites. Internal lattice fix, no external channel needed.
