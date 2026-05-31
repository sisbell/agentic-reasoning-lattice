# Review of ASN-0043

## REVISE

### Issue 1: Forward-pointer deferrals in "Why Connections Need Identity"
**ASN-0043, "Why Connections Need Identity"**: "(Nelson's formulation of this principle is quoted at L2.)" and "(Nelson's CONS-cell formulation is quoted at L13.)"
**Problem**: Both parentheticals are pure navigation prose — they announce that a quotation has been relocated downstream rather than advancing the argument at the point of use. The reader must hold a pointer and resolve it later. This is exactly the forward-reference accretion the note's classifier targets: prose whose only content is deferral to another location. The three requirements (distinguishable / owned / referenceable) stand on their own; the announcements that the supporting Nelson quotes live elsewhere carry no reasoning.
**Required**: Either fold the relevant Nelson sentence in at first mention or drop the parentheticals; do not leave bare "quoted at X" deferrals in the motivating prose.

### Issue 2: L8 design-choice paragraph restates the definition it follows
**ASN-0043, L8 (after the `same_type` biconditional and Consequences)**: "The design choice — coverage rather than span-set identity — is a modeling commitment grounded in Nelson's account above... We make `coverage` the criterion because coverage is exactly the address-set projection of an endset (per the Coverage definition above); two type endsets that reference the same address set are taken to be the same type regardless of how their spans are decomposed."
**Problem**: This paragraph says, in different words, what the L8 biconditional already states ("The relation is on coverage... not on span-set identity") and what the Coverage definition's own note already states ("coverage is a lossy projection: two endsets with different span decompositions may have identical coverage"). It is a third restatement of one fact — coverage-not-span-identity — sandwiched between the biconditional, the Consequences derivation, and the Nelson quote that grounds the same point. The substantive content (the equivalence-relation Consequences, the Nelson grounding) is elsewhere; this paragraph is connective essay that the precise reader skips.
**Required**: Remove the paragraph, or compress to the one clause that is not already stated (the appeal to Nelson), letting the L8 statement and the Coverage note carry the rest.

### Issue 3: Named-accessor well-definedness justification is meta-prose in a definitional slot
**ASN-0043, Convention — StandardTriple, "Named accessor"**: "We introduce the abbreviation `Σ.L(a).type ≡ Σ.L(a).e₃` ... ; its well-definedness follows from L3, which guarantees `|Σ.L(a)| ≥ 3` for every `a ∈ dom(Σ.L)` in a conforming store."
**Problem**: The abbreviation is the definitional content; the trailing clause is a defensive justification reaching forward to L3 to pre-empt the question "does `.e₃` always exist?". L3's `|Σ.L(a)| ≥ 3` is the carrier of that fact and is cited at every site that uses `.type`. Embedding the justification in the synonym's introduction adds a forward dependency that the definition does not need to advance its meaning.
**Required**: State the synonym `Σ.L(a).type ≡ Σ.L(a).e₃` without the well-definedness clause; the `≥ 3` guarantee is already L3's job at the use sites.

## OUT_OF_SCOPE

### Topic 1: Worked example omits explicit checks for D-MIN, S0–S2, S8-fin
**Why out of scope**: The worked example verifies L0–L14 and a representative subset of ASN-0036 invariants; the omitted S-invariants (D-MIN witness `[1,1]`, store-immutability, finiteness) are foundation guarantees holding trivially in a two-content/one-link state and need not be re-derived against a foundation already verified. Adding them would be completeness theater, not a correctness gap in this ASN.

VERDICT: REVISE
