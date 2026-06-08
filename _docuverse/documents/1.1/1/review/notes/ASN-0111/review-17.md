# Review of ASN-0111

## REVISE

### Issue 1: Ghost-type completeness stated twice, near-verbatim
**ASN-0111, "Type is interpreted by address" (RL5)**: Paragraph 1 ends "ghost types are permitted (L9, ASN-0043), and the read of a ghost-typed link is no less complete than any other." Paragraph 2 ("Two facts about the type slot bear directly...") ends "Together these make the read of a ghost-typed link no less complete than any other: the read delivers a fully interpretable type even when the type address holds nothing."
**Problem**: The two paragraphs assert the same conclusion in the same words, and paragraph 2's "First... Second..." inventory restates L3 (mandatory non-empty type) and L8 (coverage-identity without dereference) — both already invoked in paragraph 1 and again in RL-ARITY. This is the duplication / use-site-inventory pattern: two paragraphs in one section saying the same thing.
**Required**: Delete the "Two facts about the type slot..." paragraph; fold the one non-redundant fact (from/to may be empty while type must not) into RL-ARITY where it already lives.

### Issue 2: RL0 wp discussion is defensive meta-prose deferring to RL7
**ASN-0111, "Deriving the read" (RL0)**: "This wp is deliberately the same as the precondition, and we should say plainly why rather than present a tautology as analysis." ... "the single-state wp is trivial because the read is stateless... and that is a fact worth stating, not a gap. ... the composite wp is the substantive one, and it is RL7 read as a weakest precondition."
**Problem**: Past the claim itself (defined iff `a ∈ dom(Σ.L)`, `wp = a ∈ dom(Σ.L)`), the passage argues *against an anticipated reviewer objection* ("not a gap," "rather than present a tautology as analysis") and forward-defers the real wp content to RL7 twice. This is reviser drift — prior-finding rebuttal relocated into the prose — plus a forward-reference deferral. It does not advance the reasoning; a reader must skip it to reach RL1.
**Required**: Reduce RL0 to the claim and the single sentence that the link-shape of an address is necessary-but-not-sufficient. Let RL7 carry the composite-wp content without RL0 pre-announcing it.

### Issue 3: RL2 restates "slot is a primitive, not a reconstructed label" three times
**ASN-0111, "The structure the read must preserve" (RL2)**: "slot position is part of the value, not a label a reader reconstructs from an unordered pool"; then "that grouping is a primitive of the returned value, not a label a reader must reconstruct"; then "the positional accessor `eᵢ` is a model primitive."
**Problem**: One structural point (L6: slot index is a model primitive) is made three times in different words within a single claim's body. The intervening Nelson/udanax-green digression ("the type 'is symmetrical with the other endsets,' LM 4/44," "udanax-green caps every link at exactly three endsets") is historical justification padding the N≥3-vs-3 observation.
**Required**: State the slot-primitive point once, retain the single sentence distinguishing the dominant N=3 case from the admitted N>3 case, and drop the repeated restatements and the LM-citation aside.

### Issue 4: RL7 parenthetical re-explains a foundation lemma's internals
**ASN-0111, "Determinacy" (RL7)**: "(LP13 is itself the closure of L12 under the schema that lifts single-step persistence to →* by induction on the transition sequence; the same multi-step result RL8 invokes.)"
**Problem**: This explains *how LP13 is proved* (foundation territory, not this ASN's concern) and forward-defers to RL8. RL7 needs only to cite LP13 for definedness-and-value persistence across `→*`; the provenance of LP13 and the RL8 cross-reference are accretion.
**Required**: Cite LP13 for the two-part persistence and delete the parenthetical.

## OUT_OF_SCOPE

(none — the scope boundary against FOLLOWLINK/search/count/MAKELINK is correctly observed; the worked-example contrasts with "follow" and "search" are illustrative, not claims about those operations.)

VERDICT: REVISE
