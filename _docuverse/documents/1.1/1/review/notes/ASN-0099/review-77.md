# Review of ASN-0099

This ASN is mathematically careful — the definitions are precise, the proof chains in F13, F20a, F9-λ, and the meta-lemmas are explicit rather than hand-waved, and the worked example (Queries 1–6) verifies the key postconditions against concrete scenarios as required. I found no rigor gaps in the proofs themselves. The findings below are the accumulated meta-prose and redundancy that the `review-mode.anti-bloat` classifier flags, plus one placement issue.

## REVISE

### Issue 1: Silent-projection fact stated twice in different words
**ASN-0099, "A Two-Phase Factoring"**: Phase 1 says "V-positions in `R` that are absent from the arrangement contribute nothing to the image — the comprehension restricts to `R ∩ dom(Σ.M(d))`, so it fabricates no I-address absent from the arrangement." The paragraph immediately after F12 repeats: "For V-positions in `R` outside `dom(Σ.M(d))`, the silent projection in `image` absorbs them."
**Problem**: Two paragraphs in the same section say the same thing. The post-F12 paragraph adds nothing the Phase 1 statement and the `image` definition's comprehension restriction do not already establish. The accompanying "no silent fallback" editorial is a defensive justification of a guard already pinned by F12's `defined when` clause.
**Required**: Drop the post-F12 restatement (and the "no silent fallback" gloss); the Phase 1 statement and F12's `defined when` already carry both facts.

### Issue 2: "coverage(∅)=∅ / empty slot is never a witness" repeated across four locations
**ASN-0099, bolded "Empty endsets at non-type slots" paragraph (after F4)**: "L3 requires only slot 3 to be non-empty; other slots may carry `∅`. Then `coverage(∅) = ∅` and the slot is never a witness — but other non-empty slots may witness the existential."
**Problem**: This is verbatim content from F4's own preamble ("non-type slots may be empty (`coverage(∅) = ∅`, so an empty slot is never a witness)"), and the same fact recurs in the Endset Filtering unsatisfiability clause ("`Σ.L(a).eᵢ = ∅` ... `coverage(∅) = ∅` meets no `J`") and in the Empty Query section. The standalone bolded paragraph is pure repetition of material the reader has just read three paragraphs up.
**Required**: Delete the standalone bolded paragraph; F4's preamble already states it at the point of use.

### Issue 3: Definition section enumerates its downstream consumers
**ASN-0099, "A Two-Phase Factoring"**: "The two phases consult components with different stability properties — the mutable `Σ.M` and the monotonic `Σ.L` — a distinction F9 and F11 turn on."
**Problem**: This is a use-site inventory in a definitional slot — it previews which downstream claims consume the stability distinction rather than advancing the factoring's meaning. F9 (Σ.L preserved across V∖{K.λ}) and F11 (persistence) re-establish the relevant facts at their own sites; the forward pointer is non-load-bearing.
**Required**: Remove the "a distinction F9 and F11 turn on" clause. If the mutability/monotonicity contrast is worth stating, state it where it does work (F9/F11), not as a preview here.

## OUT_OF_SCOPE

None. The "What We Have Not Specified" section correctly scopes out FOLLOWLINK/RETRIEVEENDSETS, replication, caching, and access control, consistent with the declared boundaries.

VERDICT: REVISE
