# Review of ASN-0113

The formal content is sound. I checked W3 (T12 well-formedness of `ext(d,S)`), W4 (the T5-based exact-coverage argument, including the non-vacuous depth-3 instance), W10/W11 (subspace confinement and disjointness), W16 (partition), and W19 (the three weakest-preconditions) — each derivation holds, boundary cases (empty/allocated-empty/unallocated, single-occupied-subspace, `m_S = 2` collapse, `m_S = 3` interior divergence) are covered, and foundation usage (D-SEQ★, T5, OrdinalDisplacement/Shift, S3★-aux, CL-OWN/CL-UNIQ) is correct and confined to foundation ASNs. The issues below are prose accretion flagged by the `review-mode.anti-bloat` classifier, not correctness gaps.

## REVISE

### Issue 1: Duplicated sibling-comparison meta-prose
**ASN-0113, "The substrate we measure"**: "Unlike the whole-document query, which bounds `O(d)` as one undifferentiated set, this query must partition `O(d)` by *kind*."
**Problem**: This restates, in a structural definitions section, the same contrast the introduction already makes ("Where the whole-document query answers 'from here, this far' with one span, this query must answer with *several* spans, one per kind"). The whole-document query (RETRIEVEDOCVSPAN / ASN-0112) is out of scope, and the recurring positioning against it does not advance the definition of `O(d)` or `V_S(d)` that the sentence interrupts. This is the "two paragraphs say the same thing in different words" pattern, the duplicate sitting in a structural slot.
**Required**: Drop the comparative clause from the substrate section; let the definition of `O(d)`/`V_S(d)` stand on its own. The introduction may keep one framing instance.

### Issue 2: W14 contains consumer-procedure essay around a two-line claim
**ASN-0113, "Comparing reports across documents" (W14)**: "a consumer iterates the fixed kind-list `(s_C, s_L)` … checks whether a member with `start₁ = S` is *present* … a one-member report could be either a text-only or a link-only document, both 'at position 1.'"
**Problem**: The load-bearing content of W14 is short — *an absent member signifies `V_S(d) = ∅` (W6/W7), hence `n_S = 0` (W1), so per-kind comparison is well-defined over the fixed kind-list*. The surrounding material is a procedural narrative of how a hypothetical consumer reconstructs the count vector. One must skip past the consumer walkthrough to reach the actual guarantee. The single genuine subtlety — kind is read from `start₁`, not list position, because the result is a subsequence — deserves one sentence, not a paragraph with a worked "position 1" illustration.
**Required**: Reduce W14's prose to the substantive chain (absent ⟺ `V_S = ∅` ⟹ `n_S = 0`, kind recovered from `start₁`); remove the consumer-iteration walkthrough.

## OUT_OF_SCOPE

### Topic 1: Consistency between per-subspace extents and a single overall document extent
**Why out of scope**: Open Question 4 correctly defers coordination with the single overall extent (RETRIEVEDOCVSPAN / ASN-0112) to future work; it is posed as an open question, not specified here, which is the right disposition.

### Topic 2: Permanence of reported extents across version fork and transclusion
**Why out of scope**: Open Questions 2 and 3 raise version-fork and transclusion behavior. These are new territory (version/transclusion machinery), appropriately left as forward-looking questions rather than claims.

VERDICT: REVISE
