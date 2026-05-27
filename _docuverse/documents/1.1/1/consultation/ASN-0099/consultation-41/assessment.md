# Channel Assignment — ASN-0099 review-41

**Date:** 2026-05-27 07:36

## Issue 1: Strengthening 1's witness is structurally incomplete
Reason: The fix is internal — the ASN already has all the machinery (L3's slot-population rules, K.λ's well-formedness preconditions, canonical-span coverage shapes, non-nesting siblings) needed to either construct a fully-populated witness or restate the strengthening predicate. The reviewer's two suggested remedies are entirely derivable from existing ASN content.

## Issue 2: F4 misframes F1's relationship to AND-of-ORs
Reason: The structural correction (distinguish per-span overlap from across-slots quantifier; mark `findlinks_filtered` as the direct AND-of-ORs realization and F1 as its OR-across-slots relaxation) is internal. But F4's design-justification anchoring to LM 4/58 turns on whether Nelson's "one span of each endset satisfies a corresponding part of the request" governs only per-endset/per-constraint decomposed requests or also extends to the unfiltered single-I-set surface — Nelson consultation will sharpen the reanchoring.
Nelson question: Does LM 4/58's "one span of each endset satisfies a corresponding part of the request" govern only requests that decompose into per-endset parts (the filtered surface), or does it also constrain the unfiltered query where a single I-set is matched against all endsets uniformly?
