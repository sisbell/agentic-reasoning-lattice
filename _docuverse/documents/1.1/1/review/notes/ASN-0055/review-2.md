# Review of ASN-0055

## REVISE

### Issue 1: Statement labels and registry lack type annotations
**ASN-0055, Statement registry and body labels**: Labels use the form `**TA-LC** (*LeftCancellation*)` without type classification.
**Problem**: ASN-0034 establishes the convention `Label — DisplayName (TYPE, dafny_type)` — e.g., `T5 — ContiguousSubtrees (LEMMA, lemma)`. ASN-0055 extends the foundation but drops the type annotations from both the in-body labels and the registry table. These annotations drive downstream Dafny modeling (lemma vs. predicate vs. function).
**Required**: Add type annotations to each label. All three are lemmas: `TA-LC — LeftCancellation (LEMMA, lemma)`, `TA-RC — RightCancellationFailure (LEMMA, lemma)`, `TA-MTO — ManyToOne (LEMMA, lemma)`. Add a Type column to the registry table matching ASN-0034's convention.

### Issue 2: TA-MTO label covers only the forward direction; registry states the biconditional
**ASN-0055, TA-MTO section**: "**TA-MTO** (*ManyToOne*). For any displacement w with action point k and any tumblers a, b with #a ≥ k, #b ≥ k, and a_i = b_i for all 1 ≤ i ≤ k: a ⊕ w = b ⊕ w."
**Problem**: The bold label marks only the forward direction. The converse is proved two paragraphs later under "The converse also holds," and the biconditional is assembled only in the closing prose. But the registry entry states `a agrees with b on components 1..k ⟺ a ⊕ w = b ⊕ w` — the full biconditional. A reader citing "TA-MTO" cannot tell from the label alone whether they get the forward implication or the equivalence.
**Required**: State TA-MTO as the biconditional at the label point, then prove both directions below it. This makes the labeled claim match the registry entry.

## OUT_OF_SCOPE

*None.*

VERDICT: REVISE
