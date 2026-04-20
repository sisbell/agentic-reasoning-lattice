# Revision Categorization — ASN-0002 review-3

**Date:** 2026-03-06 13:27

## Issue 1: CREATELINK's V-space effect is unspecified
Category: GREGORY
Reason: The ASN's state model defines V-space with a link subspace, but whether CREATELINK populates it is an implementation question — does the code insert an entry into the target document's link subspace mapping, or do links exist only in I-space?
Gregory question: When CREATELINK creates a link, does it insert a V-space entry in the target document's link subspace (analogous to how INSERT adds text V-positions), or does the link exist only as an I-space content entry with no V-space presence in any document?

## Issue 2: Endset reference domain contradicts ghost address linkability
Category: BOTH
Reason: Nelson's text says links can reference ghost elements, but the mechanism matters — whether endsets are stored as spans (start + length, naturally covering gaps and ghosts) or as sets of individual addresses determines how to resolve the contradiction. Nelson clarifies intent; Gregory clarifies storage representation.
Nelson question: When you say links may be made to ghost elements that "embrace all the contents below them," is the endset a span descriptor (a range that may cover addresses without stored content) rather than a set of individual content addresses?
Gregory question: How are link endsets stored in the implementation — as span descriptors (start address + width) that define a range, or as enumerated sets of individual I-addresses? Can a stored endset span cover addresses not in dom.ispace?

## Issue 3: AP4a is stated about structure not present in Σ
Category: INTERNAL
Reason: The fix is a modeling decision — either extend Σ to include the range-to-entity mapping or demote AP4a to an informal design requirement. Both options are derivable from the ASN's own discussion of the allocation tree and ghost addresses, requiring no external evidence.

## Issue 4: REARRANGE's precondition is absent
Category: GREGORY
Reason: The valid inputs for REARRANGE — what arguments it takes, whether regions must be disjoint/contiguous/non-empty, whether they must be within bounds — are implementation-level constraints that the code defines.
Gregory question: What arguments does the REARRANGE operation take (two disjoint spans? arbitrary regions?), and what constraints must those arguments satisfy for the operation to be well-defined — must regions be disjoint, contiguous, non-empty, and within the document's current V-space bounds?

## Issue 5: Five derived properties are labeled "introduced" in the properties table
Category: INTERNAL
Reason: The ASN's own text explicitly states the derivation chains (e.g., "follows from AP0 ∧ AP2," "This follows from AP14 ... and AP0"). Correcting the table labels requires only matching the text's own stated dependencies.
