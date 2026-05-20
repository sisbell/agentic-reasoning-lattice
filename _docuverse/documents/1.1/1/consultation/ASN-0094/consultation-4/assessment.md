# Channel Assignment — ASN-0094 review-4

**Date:** 2026-05-19 20:31

## Issue 1: `K_sidecar_of` well-definedness incorrectly attributed to Sh4
Reason: The fix among options (a)/(b)/(c) hinges on whether single-sidecar-per-parent is part of Attribute's design intent (Nelson) and whether the implementation enforces such a constraint (Gregory).
Nelson question: Was Attribute (parent → sidecar) intended to carry at-most-one sidecar per parent document as part of its design semantics, distinct from the slot-pair distinctness Sh4 enforces?
Gregory question: Does udanax-green enforce an at-most-one-to-slot-per-from-slot constraint on attribute-like relations beyond simple slot-pair distinctness?

## Issue 2: Sh4 proof's case-split misses the mixed K = R scenario
Reason: The reviewer states the conclusion still holds; this is a proof-structuring gap. The missing Case D argument (pairwise distinctness on a subset inherits from pairwise distinctness on the superset) is derivable from the ASN's own content.

## Issue 3: References to non-foundation ASNs
Reason: The fix is mechanical citation cleanup — replace ASN-0036/ASN-0093 references with the scaffolding bullets already present, or with foundation citations the reviewer identifies. Internal restructuring.

## Issue 4: Sh4 contract atomicity scope is wrong-grained
Reason: The ASN already establishes that `L_K` is `~`-class indexed; replacing "same K" with "same `~`-equivalence class of K" is a one-word fix derivable from the ASN's own definitions.

## Issue 5: Shape syntactic well-formedness underspecified
Reason: The parenthetical in the Shape definition already states the intent; promoting it to an explicit biconditional `t_F = - ⟺ c_F = 0` is a definitional formalization derivable from the ASN.

## Issue 6: Attribute and Citation share structural shape but list disjoint templates
Reason: The choice between (a) merging into a single role-neutral entry and (b) introducing a distinguishing shape component depends on whether Nelson's design intent treats these as fundamentally different primitives or as one pattern under naming conventions.
Nelson question: Are Attribute (parent → sidecar) and Citation (citing → cited) conceived as distinct relational primitives in the design, or as the same `(1, 1, A_doc, A_doc, ⊤)` pattern under role-specific naming?

## Issue 7: Sh1 proof says "Symmetric to Sh0" with no exhibited substitution
Reason: The substitution is from F-clauses to G-clauses within Sh-conf; exhibiting clauses (b) and (c) in place of (a) and (c)'s F-side is derivable directly from the ASN's own definitions.
