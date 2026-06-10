# Channel Assignment — ASN-0116 review-53

**Date:** 2026-06-09 18:49

## Issue 1: IP1 is discussed — with its maximality caveat — several paragraphs before it is stated
Reason: Pure reordering: the IP1 statement and its non-maximality caveat both already exist in the ASN; the fix moves the claim above its discussion and deletes the forward reference. The backward-I-merge caveat rests on the K.α allocation mechanism (`a = inc(a_prev, 0)`) already derived earlier in the note, so no design intent or implementation evidence is needed.

## Issue 2: The post-state dense-run domain is stated a third time, under the banner "worth stating once"
Reason: The fix is deletion of a re-derivation, collapsing it to a pointer that ties I-DOM (restricted to the whole text subspace) to the Q10 reading-order guarantee. Both I-DOM and the Q10 connection are already stated verbatim in the ASN, so the consolidation is internal.

## Issue 3: Restatement accretion — "Two finer points" and the per-clause gapped/filled bridge
Reason: Both parts are editorial: dropping the span-vs-byte restatement (already covered by every general-`n` claim in the note) and hoisting the `M'(d) = M'₀(d) ∪ {block}` bridge into the Effect preamble so the four clauses cite it once. All the affected text is present in the ASN; consolidating and deleting it requires no external input.
