# Review of ASN-0115

I worked through the substrate dependencies, the Confinement lemma, the `act`/`deliver` definitions, and each of R1–R11 including the worked instances. The mathematics is sound: the Confinement proof (T5 + TumblerAdd) is correct, the `act` override is genuinely exercised by reachable states and correctly motivated, R6's no-interior-hole argument on the bindable slice holds (monotone `k ≤ n_S` ⇒ contiguous tail), R7's active-set agreement survives the override sub-case, and R8's link-vacuity (CL-OWN + CL-UNIQ) and content/link subspace dispatch (S3★ + SD + S3★-aux) are valid. The wp analyses (R7, R11) and the five worked instances all check out against the cited foundations. No correctness or missing-case findings.

The note carries the `review-mode.anti-bloat` and forward-reference classifiers, and there is one clean match to a named accretion pattern.

## REVISE

### Issue 1: R2's proof appends a downstream use-site inventory of S0
**ASN-0115, "Faithfulness, and where the invariant stops"**: After the R2 proof closes cleanly — "the delivered value simply *is* the store's value at the resolved address — that is the whole of R2" — the next sentence is: "Permanence *across* states … is a distinct guarantee that R2 does not invoke; it is carried by content immutability (S0) and made load-bearing in R7 (Repeatability) and R11 (PermanentSourcing)."

**Problem**: The phrase "made load-bearing in R7 (Repeatability) and R11 (PermanentSourcing)" is a forward enumeration of downstream consumers of S0 — exactly the "definition's introduction enumerates downstream consumers / use-site inventory" pattern the anti-bloat classifier names. The R2 proof is complete without it; the enumeration is scope-disclaimer prose pointing at claims not yet stated. The same deferral is duplicated in the Claims Introduced table, R2 row: "permanence-across-time belongs to R7/R11, via S0." A reader following R2 stops at "that is the whole of R2"; the forward inventory is prose to skip past.

**Required**: Keep the genuine scope delimitation (R2 is a single-state denotational equality; cross-state permanence is a separate guarantee carried by S0). Drop the enumeration of *which* downstream claims invoke it — the reader reaches R7/R11 on their own. Collapse to a single pointer and remove the duplicated claims-table annotation.

A smaller companion instance of the same shape: the R8 claim box carries a forward parenthetical "(cf. R9)" to a not-yet-stated claim. Unlike the box's other citations (R1, R2, S4 — established or foundation), this one points forward; fold it into R8's prose rather than the structural claim slot.

## OUT_OF_SCOPE

None to add. The note correctly stays clear of READLINK/FOLLOWLINK territory (R10 delivers a link as a `⟨ref, a⟩`, explicitly *not* its endset structure), and the five Open Questions (inline provenance, fail-vs-partial, relaxed S3★, channel faithfulness, straddling spans) are all genuine future work appropriately deferred, not gaps in this ASN.

VERDICT: REVISE
