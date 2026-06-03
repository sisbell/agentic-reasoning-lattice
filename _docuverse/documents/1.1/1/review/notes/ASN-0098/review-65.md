# Review of ASN-0098

## REVISE

### Issue 1: Thesis sentence duplicated verbatim across two sections
**ASN-0098, LP16 trailing prose and Nelson correspondence**: After LP16 — "Link discovery is a function of I-address intersection alone, and transclusion shares I-addresses by definition." And in the Nelson correspondence — "...the transclusion-discoverability mechanism of LP16 — discovery turns on I-address intersection alone, and transclusion shares I-addresses by definition."
**Problem**: The same claim is asserted twice in near-identical words. This is the "two paragraphs say the same thing in different words" pattern the anti-bloat classifier flags. The reader who follows LP16 already holds this conclusion; the Nelson recap re-delivers it.
**Required**: Keep the statement once (at LP16, where it is earned) and have the Nelson correspondence point to LP16 without re-paraphrasing its content.

### Issue 2: Coverage definition restates itself
**ASN-0098, "The Coverage of an Endset"**: "Crucially, coverage is a *purely combinatorial* property of the endset's span representation — it does not consult any state component. Coverage depends on the spans; nothing else."
**Problem**: "Coverage depends on the spans; nothing else" is a second phrasing of "purely combinatorial property... does not consult any state component." The trailing sentence adds no information.
**Required**: Drop the trailing restatement.

### Issue 3: Editorializing/recap sentences that re-deliver results just proved
**ASN-0098, "Frame Conditions" and "Discovery Independence of Origin"**: "Hence none of content allocation, link allocation, provenance recording, or node/account creation can displace any projection." and "The transclusion mechanism is the architectural lever that activates this provenance-indifference."
**Problem**: The first sentence restates the arrangement-fixing template result enumerated in the same paragraph (LP6/LP7/LP14 + K.δ node/account) — a use-site inventory recap. The second is essay editorializing in a structural slot; it advances no reasoning toward LP16, which states the mechanism precisely.
**Required**: Remove the recap enumeration (the template paragraph already carries the conclusion) and the "architectural lever" sentence; let LP16 stand on its own.

### Issue 4: Nelson correspondence section is a use-site recap of LP12a/LP16/LP18
**ASN-0098, "Nelson correspondence" paragraph in Ghost Projection section**: "Two of Nelson's informal survivability claims are now formal results..." mapping three informal claims to LP16, LP18, LP12a.
**Problem**: Beyond the verbatim duplication in Issue 1, the paragraph re-narrates the import of three claims already established and labeled. This is essay content recapping structural results rather than advancing them.
**Required**: Compress to bare pointers (claim ↔ LP-label) or fold the correspondence notes into the respective claims' prose, removing the standalone recap.

## OUT_OF_SCOPE

### Topic 1: Reverse-discovery primitive, V-order guarantees, link-to-link induced discovery, cross-document operation-equivalence, fork without link-subspace transclusion, link-canonical contraction
**Why out of scope**: These are correctly parked in the Open Questions section as future ASN territory, not gaps in the present note. The link-canonical contraction question (LP-Fin Corollary inverts at the link subspace) is honestly flagged as the dual of LP12b that this ASN does not close — appropriate to defer.

Note on correctness: the operation coverage is complete (K.α/K.λ/K.δ/K.ρ/K.μ⁺/K.μ⁺_L/K.μ⁻/K.μ~ all treated), boundary cases (empty arrangement, R=∅, empty endset, boundary insertion under tightness) are addressed, and the LP-Fin/LP12b/worked-trace derivations check out. The remaining items are prose-density, not proof gaps — but they are genuine anti-bloat findings under this note's classifier.

VERDICT: REVISE
