# Channel Assignment — ASN-0086 review-14

**Date:** 2026-05-16 20:56

## Issue 1: Worked Sketch's L1c verification misidentifies the allocator producing link addresses
Reason: The fix is derivable from the ASN's own R0 Step 2 chain construction — correctly identifying which allocator hosts each address is a matter of reading the chain steps (i)–(iii) already specified. The naming convention (e.g., A_{base}) is an internal exposition choice that doesn't require external evidence.

## Issue 2: Emit_K's signature is functional but its definition is non-deterministic in home-document choice
Reason: Resolving the signature requires both Nelson's design intent on whether link emission was conceived as document-scoped at the caller interface, and Gregory's evidence on how the concrete implementation parameterizes home-document selection — both inform whether (a), (b), or (c) is the right design.
Nelson question: In the original link model, was the home document of a new link intended to be a caller-supplied parameter of the emit operation, or determined implicitly by allocator policy or ambient context?
Gregory question: In udanax-green's link-emission path (`docreatelink`, `findisatoinsertmolecule`), how is the home document for a new link determined — explicit parameter, derived from current context, or allocator-chosen — and is this choice exposed at the operation's call interface?

## Issue 3: Nullify's single-tuple-scope is implicitly conditional on substrate-wide discipline adherence
Reason: The choice between making the dependency explicit, elevating the discipline, or adding defensive verification depends on whether Nelson designed sibling-frontier as a substrate invariant or an allocator convention, and on whether udanax-green's substrate enforces it uniformly or only at specific call sites.
Nelson question: Was sibling-frontier link emission (links sited only at sibling-frontier positions, never as descendants of existing links) intended as a substrate-level structural guarantee, or merely as the conventional behavior of one allocation routine?
Gregory question: Does udanax-green have any code path that can deposit a link address at a strict prefix-extension of an existing link address (i.e., as a descendant rather than a sibling), or does the implementation uniformly enforce the sibling-frontier discipline across all link-store-extending operations?
