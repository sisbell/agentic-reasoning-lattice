## Question 1 [theory]

> Does *Literary Machines* 2/46 (and Nelson's broader discoverability framing) prescribe the singleton-overlap match criterion specifically, or only constrain match predicates to a family from which F1 is one design-justified choice?

**LM 2/46 alone prescribes only the user-facing guarantee — not the match predicate.**

The 2/46 text concerns discoverability:

> "The reader should be able to ask, for a given document or place in the document, 'What connects here from other documents?'—and be shown all these outside connections without appreciable delay." [LM 2/46]

That's a *deliverable* (find the relevant in-links, fast), not a predicate spec.

**The predicate semantics live at LM 4/58, not 2/46:**

> "A link satisfies a search request if one span of each endset satisfies a corresponding part of the request." [LM 4/58]

This *is* the singleton-overlap shape: existential within each endset, conjoined across the three endsets — the "AND of the ORs." That structural shape is prescribed, not optional.

**But within that shape, F1 is one design-justified choice.**

Nelson's "one span...satisfies a corresponding part" is structurally definite (∃ per endset, ∧ across endsets) but leaves the *overlap predicate itself* underdetermined: any nonempty intersection? boundary-inclusive? proper containment? coverage threshold? Different disambiguations all sit inside the family 4/58 sanctions.

F1's singleton-overlap reading is design-justified by the robustness principle at 4/60:

> "THE QUANTITY OF LINKS NOT SATISFYING A REQUEST DOES NOT IN PRINCIPLE IMPEDE SEARCH ON OTHERS." [LM 4/60]

Singleton-overlap honors that — adding non-overlapping spans to other endsets cannot suppress a match.

**Summary:** 2/46 constrains only the user guarantee. 4/58 mandates the AND-of-ORs existential structure. Within that family, F1 is design-justified (by 4/60), not uniquely prescribed.
