# Channel Assignment — ASN-0094 review-52

**Date:** 2026-05-24 01:38

## Issue 1: SHCD attachment wording is internally inconsistent
Reason: The third paragraph cites Nelson's design intent (link mechanism is universal, semantic interpretation lives at the front end) to back the structural-eligibility reading, while the first two paragraphs use "Coverage instantiation" language suggesting a semantic restriction. Settling which reading is binding requires confirming Nelson's intent regarding whether substrate-level mechanisms (like SHCD's emission-ordering) are meant to be available at any structurally-eligible K or reserved for a particular semantic link role.
Nelson question: Did Nelson's design intent treat substrate-level mechanisms like emission-order-aware coverage tracking as universally applicable to any link with the appropriate structural shape, or as semantically scoped to a particular link role such as supersession?

## Issue 2: "Instantiation" terminology obscures the catalog row structure
Reason: The fix is derivable from the catalog row's existing structure — the row already defines SHCD as a per-K opt-in extension and `_via` as a parametric consumption pattern, and the existing prose ("opt-in", "parametric") supplies the replacement vocabulary. No design-intent or implementation evidence is needed; this is internal terminology cleanup to bring walkthrough section headers into alignment with the catalog row's vocabulary.
