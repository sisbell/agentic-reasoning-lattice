# Review of ASN-0115

This is a careful, technically sound note. The resolution-then-dereference decomposition is right, the Confinement lemma is proved correctly (T5 applied with `p = [s₁,…,s_{m−1}]`, `a = s`, `c = reach(σ)`), the wp analysis in R11 is genuinely non-trivial (the two-conjunct precondition collapsing to one is a real insight), and the query-relevant boundaries — empty spec-set, empty document, terminal overrun, transclusion, cross-subspace, orphaned content — are each carried by a concrete worked instance. I checked the R6, R8, and R11 worked instances arithmetically and they hold.

The note carries `review-mode.anti-bloat`, and the findings below are the residue of the recent R8 flowing-prose restructure: the same proposition is now asserted in a claim box and then twice more in consecutive prose paragraphs.

## REVISE

### Issue 1: The "sharing is in resolution, not the output" proposition is stated three times
**ASN-0115, §"What co-delivery does with transclusion"**: the same claim appears in the R8 box —

> "The sharing is a fact of *resolution*, not of the delivered output"

— then again at the end of the first following paragraph —

> "That makes the shared identity a property of *how the delivery is computed*, not of the delivered bytes."

— then again as the opening of the very next paragraph —

> "Because the identity lives in the computation, the sharing is internal to resolution, not disclosed by the output."

**Problem**: This is the anti-bloat "two paragraphs say the same thing in different words" pattern, concentrated at the Para-1-end / Para-2-start seam and echoing the box. The two paragraphs do each carry one distinct payload — Para 1: content identity is by creation (S4), so co-resolution dereferences `a` twice rather than copying; Para 2: therefore co-delivery is informationally equivalent to two isolated requests (the Nelson 3/4 commonality point). But a precise reader must skip past the restated "resolution-not-output" proposition at three sites to reach those two distinct payloads.
**Required**: State the proposition once (the R8 box already does). Have Para 2 lead directly with its new content — that co-delivery "carries no information a pair of isolated requests lacks" — rather than re-opening with the box's claim. Para 1's closing sentence and Para 2's opening clause should not both restate the box.

### Issue 2: R9 exhibits the same box-restates-prose shape
**ASN-0115, §"What co-delivery reveals: coherent multi-origin assembly"**: the R9 box already fixes the kind-asymmetry —

> "a content item carries only the value `Σ.C(a)`, so its origin `origin(a)` is *not* recoverable from the output — it is determinate only through the resolution mapping"

— and the following "two obligations" paragraph re-derives the same split:

> "Output-recoverability — whether that home survives into the delivered output — is where the two item kinds genuinely part."

**Problem**: Milder than Issue 1 (the paragraph adds the coherent/determinate dichotomy and the "met automatically" reasoning, which are new), but the determinate-via-resolution-not-output point is stated in both box and prose.
**Required**: Consolidate so the box states the asymmetry and the prose advances to the obligation analysis without restating it. Addressing Issues 1 and 2 together removes the pattern at both sites.

## OUT_OF_SCOPE

None. The Open Questions correctly route inline provenance, hard-failure modes, unbound resolved references, channel faithfulness, and subspace-straddling spans to future work rather than asserting claims about them, and link-structure reading (READLINK/FOLLOWLINK) is properly deferred while only the link *reference* `⟨ref, a⟩` is delivered here.

VERDICT: REVISE
