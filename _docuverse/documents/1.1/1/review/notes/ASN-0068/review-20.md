# Review of ASN-0068

I checked the core proofs (CV-MAX existence/uniqueness, CV-PRED inverse properties, the V-position-capture argument in CV-IN, CV-SPAN-VIEW, and all four worked examples). The mathematics is sound: the walk-termination bounds (D-SEQ★/S8a on the left, S8-fin on the right), the lockstep-offset reduction via OrdinalShift's last-component formula and T3, the differing-depth handling, and the example computations all check out. My findings are confined to the forward-reference/accretion patterns the classifier flags.

## REVISE

### Issue 1: CV-FIN appends a bound-tightness essay with forward references to unintroduced examples
**ASN-0068, CV-FIN justification (final paragraph)**: "The interior bound `min(|dom(M(d_a))|, |dom(M(d_b))|)` is not in general an upper bound on `|MaxRuns|`: a self-comparison configuration ... (Example 3 below) achieves `|MaxRuns| = 3 > 2` ... The product bound is itself not always tight — Example 1 below achieves `|MaxRuns| = 1` against a product bound of `3 · 4 = 12` — but it is the smallest bound expressible from cardinalities of `dom(M)` alone."
**Problem**: CV-FIN's claim is finiteness; the first paragraph proves it. This appended paragraph defends *why this bound and not a tighter one*, forward-referencing Examples 1 and 3 that are introduced only in the later "Worked Examples" section. This is exactly the forward-reference-accretion pattern (claim prose deferring to a downstream location, plus defensive justification of a representational choice beyond what the claim asserts).
**Required**: Drop the tightness/forward-reference paragraph from CV-FIN. If the tightness observations are worth keeping, state them once in the Worked Examples section where Examples 1 and 3 actually live, not in the finiteness claim.

### Issue 2: CV-EMPTY's second paragraph inventories causes already covered by its proof
**ASN-0068, CV-EMPTY justification (second paragraph)**: "The empty input arises either by an explicit `R_a = ⟨⟩` from the caller or by CV-IN's empty-subspace clause forcing `R_a = ⟨⟩` when `V_S(d_a) = ∅` ... in both cases `⟦R_a⟧ = ∅` and the first paragraph applies directly."
**Problem**: The first paragraph already discharges the general case `⟦R_a⟧ ∩ dom(M(d_a)) = ∅`, which subsumes `⟦R_a⟧ = ∅`. The second paragraph is a cause inventory deferring to CV-IN; it adds no proof obligation and restates a special case of what is already proven.
**Required**: Remove the second paragraph. The first paragraph is the complete proof.

### Issue 3: Conclusion restates the introduction's grounding thesis verbatim
**ASN-0068, "What the Result Cannot Express" (closing)**: "The same grounding is what makes attribution, royalty flow, and link survival work uniformly across the docuverse."
**Problem**: This duplicates the introduction's "it inherits from the addressing scheme the same atomic, identity-grounded discipline that underwrites attribution, royalty flow, and link survival." Two paragraphs state the same thing in different words.
**Required**: Cut the restatement; the omission consequences (i)–(iii) already carry the section.

## OUT_OF_SCOPE

None. The Open Questions (concurrent modification, replication, version-history walks, cross-origin runs) correctly defer their topics to future ASNs rather than asserting claims about them.

VERDICT: REVISE
