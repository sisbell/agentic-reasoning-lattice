# Channel Assignment — ASN-0068 review-1

**Date:** 2026-05-24 23:16

## Issue 1: CV-MAX proof is a sketch, not a proof
Reason: The required proof structure is specified in the issue itself, citing TS2/TS4 (ASN-0034) and M12 (ASN-0058) which are already foundation references in the ASN. The lockstep-offset and contradiction argument is constructable from these existing citations alone.

## Issue 2: No concrete example
Reason: The example uses the operation's own definitions applied to a stipulated V-position layout. No external evidence or design intent is needed — the example verifies internal consistency.

## Issue 3: k = 0 case for "v + k" notation not handled
Reason: The fix is a single citation to OrdinalShiftBase (ASN-0058), which the issue identifies directly. Purely internal.

## Issue 4: Result type undefined
Reason: The type definition follows mechanically from the run/triple/span-pair descriptions already in the text. No external input needed.

## Issue 5: CV-ATOM is redundant with CV-MAX
Reason: The decision between deletion and restatement turns on whether byte-level granularity was a deliberate design contrast with threshold/block-aligned diff schemes, which is design intent. Nelson can confirm whether atomicity-without-threshold was a designed-in property of the comparison operation.
Nelson question: Was byte-granular correspondence (no minimum quotation length, no merge threshold) a deliberate design property of compareversions, intended to contrast with conventional block-aligned or threshold-based diff — or is it merely a consequence of the addressing scheme with no separate design status?

## Issue 6: Link-subspace case is essentially trivial
Reason: Resolving whether the s_L case is degenerate (per CL-OWN) or genuinely meaningful requires Nelson on design intent (was link-arrangement comparison meant to be substantive?) and Gregory on whether the implementation supports or restricts s_L comparison.
Nelson question: Did the design contemplate comparing the link arrangements of two documents as a meaningful operation, given that CL-OWN forces every link in d's arrangement to have origin = d — or was compareversions intended only for s_C in practice?
Gregory question: Does the udanax-green implementation of compareversions accept link-subspace restrictions, and if so does it produce non-empty results for distinct documents, or does it specialize to content?

## Issue 7: Empty-restriction case not addressed
Reason: The empty-restriction result (∅) follows directly from the definition of `corr_{a,b}` and `⟦⟨⟩⟧ = ∅`. Single-sentence addition derivable from text already present.

## Issue 8: Self-comparison (d_a = d_b) not addressed
Reason: The characterization (identity decomposition plus self-transclusion runs) is derivable, but the choice to admit or exclude is a design decision. Nelson can clarify whether self-comparison was contemplated as a valid invocation of compareversions.
Nelson question: Was compareversions intended to admit d_a = d_b as a valid input (yielding identity-plus-self-transclusion correspondence), or was the operation always conceived as comparing two distinct documents?

## Issue 9: CV-SYM proof not shown
Reason: The verification swaps operands in the maximality disjunctions — purely syntactic, internal to the definitions just given.

## Issue 10: Span-pair projection well-formedness not verified
Reason: The verification chains T12, OrdinalDisplacement (ASN-0034), and S8-depth (ASN-0036), all foundation references already cited in the ASN. Internal.

## Issue 11: "v − 1" predecessor notation insufficiently grounded
Reason: The fix is citations to TS2 (ASN-0034) and D-SEQ★ (ASN-0047), both foundations the ASN already builds on. The uniqueness argument is mechanical from shift injectivity.
