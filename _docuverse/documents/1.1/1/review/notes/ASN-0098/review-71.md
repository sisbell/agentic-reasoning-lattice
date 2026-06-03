# Review of ASN-0098

I checked the projection proofs, the K.μ-family displacement lemmas (LP9–LP11), the wp computation (LP12a/b), and the substrate-finitude machinery (LP-Sub, LP-Fin, LP-Fin Corollary), including boundary cases — empty arrangement (LP10), empty retention (LP12a), document registration (LP8), and tight-endset freshness (LP19a/LP19). The mathematical content is sound; the exact-difference formulas, the K.μ~ bijection-pullback, and the LP-Fin sub-case split (A contributes 0, B contributes exactly n) all hold up. Boundary coverage is complete. The remaining issues are residual meta-prose around forward references, consistent with this note's anti-bloat classifier.

## REVISE

### Issue 1: Restating aphorism closes the LP16 discussion
**ASN-0098, "Discovery Independence of Origin" (LP16)**: "No notification of the link is required; the link is *passively* discoverable from `d_new` simply because `d_new` arranges the I-address.\n\nLink discovery is a function of I-address intersection alone, and transclusion shares I-addresses by definition."
**Problem**: The standalone final sentence restates the immediately preceding two sentences ("Discoverability extends to every document that transcludes any I-address in coverage" + "passively discoverable... simply because `d_new` arranges the I-address"). Two statements saying the same thing in different words — the second is an essay flourish, not new reasoning.
**Required**: Delete the trailing sentence; the paragraph already carries it.

### Issue 2: Forward roadmap pointer inside the "anything is left" formalisation
**ASN-0098, after LP12a**: "For mere existence of the link, nothing is required at all — this is the substantive content of the next claim."
**Problem**: The clause "— this is the substantive content of the next claim" is a forward pointer to LP13 that the section ordering already supplies. It advances no reasoning about the formal restatement it is attached to.
**Required**: Drop the clause. If the contrast with LP13 is wanted, let LP13's own statement carry it.

### Issue 3: Roadmap tail on the LP12→LP12a transition
**ASN-0098, before LP12a**: "K.μ⁻ is the only K.μ family member that can *destroy* discoverability. We compute wp explicitly."
**Problem**: "We compute wp explicitly" is a roadmap sentence; the LP12a claim block that immediately follows announces the wp computation by its own statement. The substantive content (K.μ⁻ as the sole discoverability-destroying operation) is in the preceding sentence and can stand alone.
**Required**: Delete "We compute wp explicitly."

## OUT_OF_SCOPE

### Topic 1: Reverse-discovery, V-order preservation, link-canonical contraction
**Why out of scope**: These are correctly deferred to the Open Questions section as future ASN territory (reverse-discovery primitive invariants, V-order/I-order reflection under K.μ~, the link-subspace dual of LP12b). They are not gaps in this ASN's stated scope.

VERDICT: REVISE
