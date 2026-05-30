# Review of ASN-0082

## REVISE

### Issue 1: Interpretive restatement prose duplicates the lemmas it follows
**ASN-0082, The Ordinal Shift**: After citing TS1 — "shift is order-preserving: ... (TS1, ASN-0034)" — a separate paragraph restates it: *"The relative ordering of content is preserved through the shift. What was before other content remains before it after insertion ..."* The same happens after TS2: *"Injectivity ensures the shift creates no collisions: distinct V-positions remain distinct after shifting."*
**Problem**: Each cited foundation lemma is immediately followed by a paragraph that says the same thing in English without advancing the argument — exactly the "two paragraphs say the same thing in different words" / essay-in-structural-slot pattern the anti-bloat classifier targets. The reasoning is carried entirely by the TS1/TS2 citations; the prose is noise the precise reader must skip.
**Required**: Delete the interpretive paragraphs; the TS1/TS2 citations stand on their own. If a motivational line is wanted, keep one short clause, not a standalone paragraph per lemma.

### Issue 2: Dangling Q-references break self-containment
**ASN-0082, I3 grounding and elsewhere**: "I3 grounds Nelson's central guarantee (Q1, Q5) ...", "Nelson's guarantee that content appears 'in its original relative order on either side' (Q2)", "D-SHIFT grounds Nelson's two-space separation ... [LM 4/11]".
**Problem**: The labels Q1, Q2, Q5 are never defined in this ASN and refer to material in the source note. A reader cannot resolve them. These motivational groundings sit inside the formal-contract regions (between postcondition statement and consistency proof) as essay content. Per the self-containment standard, unexplained external labels are a defect.
**Required**: Either drop the Q-labels and inline-essay groundings, or replace each with a self-contained one-line statement that needs no external index. Move motivation out of the formal-contract slot.

### Issue 3: Near-duplicate boilerplate in the two cross-subspace worked examples
**ASN-0082, "Cross-subspace preservation" (insertion) and "Cross-subspace preservation" (contraction)**: Both open with the identical framing — *"Consider document d with both text and link subspaces populated. The text subspace S = 1 has ... contiguous positions; the link subspace S = 2 has two sparse positions (allowed by the foundation's frame note on D-CTG for V_2 ...)"* — and then walk the same table structure.
**Problem**: The verification content differs (I3-X vs D-CS), but the setup prose and the "tombstone gap at [2,...] remains" commentary are repeated verbatim across sections. This is accreted redundancy.
**Required**: Keep both examples (they exercise different operations) but factor the shared setup into a single statement, or trim the second example's narration to the lines that differ from the first.

## OUT_OF_SCOPE

### Topic 1: Contraction at ordinal depth greater than one (#p > 2)
**Why out of scope**: The contraction's `#p = 2` depth scoping axiom is a deliberate restriction, and the generalization (with the TA4 zero-prefix collision against S8a positivity at intermediate components) is already recorded in the Open Questions. This is a future ASN, not a defect here. The insertion half (I3) correctly handles general `m ≥ 2`; the asymmetry is acknowledged.

The mathematical core is sound: the round-trip identity `(ord(p) ⊕ w_ord) ⊖ w_ord = ord(p)` is discharged through TA4 with preconditions checked at depth 1, the D-S(a) ℕ-subtraction identity is carefully routed through ReverseInverse/TA-assoc/NAT-comm/TA4 rather than assuming an unaxiomatized ℕ-subtraction law, and the boundary cases (L=∅, R=∅, full deletion, cross-subspace) are each traced concretely. The findings are accreted prose, not correctness gaps.

VERDICT: REVISE
