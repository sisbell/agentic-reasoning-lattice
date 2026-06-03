# Review of ASN-0075

## REVISE

### Issue 1: Directional mismatch in "Distinguishing Deletions from Additions"
**ASN-0075, "Distinguishing Deletions from Additions"**: "A naive set-difference of current ranges — `ran(M(d_A)) \ ran(M(d_B))` — would conflate two distinct phenomena... Our definition forces the disambiguation by requiring `(a, d_A) ∈ R` for content reported as deleted-from-A."

**Problem**: The set-difference example and the disambiguation paragraph discuss opposite halves of the operation. The example `ran(M(d_A)) \ ran(M(d_B))` selects addresses `a ∈ ran(M(d_A)) ∧ a ∉ ran(M(d_B))` — content **current in d_A, absent from d_B**. The two conflated phenomena ("content d_A had that d_B deleted" and "content d_A acquired that d_B never received") are both about this set, and the disambiguator that separates them is membership in `R` with respect to **d_B** (`(a, d_B) ∈ R`), i.e. this is the `DeletedFromBWithA` half. But the following paragraph switches to "deleted-from-A" and cites `(a, d_A) ∈ R` — which disambiguates `DeletedFromAWithB`, the half whose naive analogue would be `ran(M(d_B)) \ ran(M(d_A))`. As written, the stated disambiguator does not apply to the stated example. A reader following the argument cannot connect the requirement to the motivating diff.
**Required**: Make the two paragraphs refer to the same half — either change the example to `ran(M(d_B)) \ ran(M(d_A))` to match "deleted-from-A" and `(a, d_A) ∈ R`, or keep the example and rewrite the disambiguation in terms of `(a, d_B) ∈ R` for "deleted-from-B."

### Issue 2: Mislabeled cross-reference to D-IDENT
**ASN-0075, wp non-emptiness derivation (Q1)**: "The last conjunct (presence in `d_B`) is what makes the report *recoverable* in the sense of D-IDENT — every reported deletion has a concrete witness in the partner document."
**Problem**: D-IDENT establishes that output references are the I-addresses themselves rather than copies — identity preservation. It says nothing about witnesses, recoverability, or partner-document presence. "Recoverable in the sense of D-IDENT" attributes a claim to D-IDENT that D-IDENT does not make; the recoverability here comes from the witness/`CURRENT(a, d_B)` condition, not from identity preservation.
**Required**: Drop the "in the sense of D-IDENT" attribution, or restate it accurately (the witness condition is what supplies recoverability; D-IDENT separately guarantees the returned witness is the actual address).

### Issue 3: D-ACT justification restates itself
**ASN-0075, D-ACT**: "Any operation whose input type accepts I-addresses (or spans thereof) can consume the output directly. The abstract specification fixes only the set of I-addresses; because each address retains its identity (D-IDENT), the output is directly consumable by any I-address-based operation."
**Problem**: The claim sentence ("usable as input to any operation that consumes I-addresses"), the second sentence ("can consume the output directly"), and the third ("directly consumable by any I-address-based operation") all assert the same proposition. Two of the three add no reasoning. This is the same-thing-twice accretion the anti-bloat pass targets.
**Required**: Collapse to a single statement: output elements are I-addresses in `dom(C)` retaining their identity (D-IDENT), hence directly consumable by any I-address-based operation.

### Issue 4: Protocol-rationale accretion in the D-DISCR notational convention
**ASN-0075, D-DISCR "Notational convention"**: "K.α must be bundled with a K.μ⁺/K.ρ pair in the same composite: K.α's frame leaves `M` unchanged, so a standalone-K.α composite would produce `a ∈ dom(C') \ dom(C)` without placing `a` in any arrangement, violating J0... The bundling pattern is exhibited in Histories 1 and 2 below."
**Problem**: This is protocol rationale explaining *why* the bundling is necessary plus a forward pointer to where it is "exhibited," rather than reasoning that advances the lemma. The histories themselves carry inline justifications ("discharging J0", "discharging J1★") at each composite, so the upfront essay duplicates that work. The "exhibited in Histories 1 and 2 below" pointer is a use-site inventory that does not advance the argument.
**Required**: Remove the standalone rationale paragraph(s); the per-composite annotations already establish validity at point of use. Retain only the K.δ shorthand definition needed to read the histories.

## OUT_OF_SCOPE

### Topic 1: Third-document witness and multi-document generalization
**Why out of scope**: Open questions 3 and 5 (witness in a document outside the pair; families of more than two documents) are genuinely new territory — they require a witness structure this binary operation does not define. Correctly deferred, not an error here.

### Topic 2: Restoration / consuming SHOWDELETIONS output to re-insert content
**Why out of scope**: The final open question about a restoration operation reintroducing deleted content is arrangement-mutation mechanics, which belong to a future operation ASN.

VERDICT: REVISE
