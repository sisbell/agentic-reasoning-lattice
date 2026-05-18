# Channel Assignment — ASN-0047 review-99

**Date:** 2026-05-18 01:47

## Issue 1: Ghost-base versioning is admitted without design rationale
Reason: Both channels needed — Nelson to confirm whether the design intent admits versioning from a structurally valid but unallocated document address, and Gregory to confirm whether the implementation actually exercises this case or always requires the source to be live.
Nelson question: Does Literary Machines describe or sanction versioning from a document address that is structurally valid but has not been allocated as an entity, and if so what use case does it serve?
Gregory question: Does udanax-green's `docreatenewversion` (or equivalent) permit the source document operand to be uninstantiated in the registry, or does it always require the source to exist in allocated state?

## Issue 2: Foundation invariant S7d weakened to S7d★ without prominent flagging
Reason: Pure presentation/organization fix — relocate and re-emphasize the S7d→S7d★ relaxation near K.δ. Derivable from the ASN's own content.

## Issue 3: P5 introduced before P3, but P3 supersedes P5
Reason: Pure labeling/organization fix — merge or reorder P5 and P3. Derivable from the ASN's own structure.

## Issue 4: K.μ~ "zero elementary steps" expansion is semantically awkward
Reason: Internal definitional restructuring — either restrict K.μ~'s precondition to π ≠ id, or acknowledge the degenerate case as a distinct admissibility regime. Derivable from the ASN's own composite-transition machinery.

## Issue 5: D-SEQ★ derivation cites S8-depth for shared first component
Reason: Internal correction — replace the misattribution with the correct grounding (definition of V_S(d) + subspace projection). Derivable from the ASN's own notation block.

## Issue 6: K.α cross-document distinctness omitted from the freshness-discharge summary table
Reason: Internal completeness fix — add the missing row citing the Cross-document disjointness chain lemma at content-allocator anchors. Derivable from the ASN's existing lemma.

## Issue 7: Reviser drift in axiom prose — use-site enumeration
Reason: Internal stylistic trim — remove consumer-enumeration prose from axiom bodies. Derivable from the rubric and the ASN's own structure.
