# Review of ASN-0042

This ASN's reasoning is sound — I worked the O10 fork construction against the worked-example trajectories (including the node-level case where the d=2 stream `S([1],2)` coincides with the account stream, and `hwm` correctly counts delegated prefixes so `hwm_0+1` never collides with `pfx(π_A)`), checked O2's four-step well-definedness, and traced the NestingByDelegation induction. The math holds. The remaining findings are prose accretion, which the `review-mode.anti-bloat` classifier directs me to surface at source.

## REVISE

### Issue 1: `allocated_by_Σ` introduction duplicates its own axiom block
**ASN-0042, State Axioms (AllocatedBy)**: the prose paragraph "We take `allocated_by_Σ(π, a)` … as a primitive relation … The relation records that the baptism procedure, executing on behalf of `π`, produced `a`; the procedure itself is the mechanism placed out of scope. The signature: …" is immediately followed by the axiom block restating *Signature*, *Semantics* ("holds when the baptism procedure, executing on behalf of `π`, produced `a`"), and *Mechanism* ("Out of scope; belongs to the tumbler baptism specification").
**Problem**: Two adjacent passages say the same thing in different words — the flagged "two paragraphs in the same document say the same thing" pattern. The reader parses the introduction, then re-parses the identical content in structured form.
**Required**: Delete the prose paragraph; keep the structured axiom block (Signature/Semantics/Mechanism), which carries all the content.

### Issue 2: O18 prose explains why the axiom is structured rather than what it says
**ASN-0042, O18 (DelegationBaptizes)**: "O18 asserts only this per-transition fact: each transition introducing a new principal records that principal's prefix into the baptismal registry as a tumbler not present immediately prior. It carries no base case of its own; the bootstrap state's prefix membership is supplied separately by O14's seventh clause, and the two are combined by the induction in PrefixBaptismCoupling below."
**Problem**: Restates the axiom verbatim ("records that principal's prefix … not present immediately prior" = the formula), then adds meta-prose about base-case bookkeeping and forward-references PrefixBaptismCoupling. This is the flagged "new prose around an axiom explains why the axiom is needed rather than what it says" + downstream deferral pattern. The base-case/induction split is established at PrefixBaptismCoupling's own proof; stating it here too is redundant.
**Required**: Remove the paragraph. The axiom formula stands on its own; PrefixBaptismCoupling already names O14(vii) and O18 as its base/step inputs.

### Issue 3: NestingByDelegation path-independence paragraph + the `delegated_Σ*` deferral
**ASN-0042, Definition (delegated)** and **NestingByDelegation**: the definition note defers — "The reflexive-transitive closure `delegated_Σ*` is a separate relation, built from the structural parent relation `R_Σ` … defined alongside NestingByDelegation below." Then NestingByDelegation devotes a full paragraph ("This structural `R_Σ` coincides with the introducing-delegation relation, and the coincidence is path-independent. When O15 introduces `π'` … the most-specific covering principal of `pfx(π')` is identical in `Π_{Σ_k}` and in the larger `Π_Σ` …") to justifying that the definition is well-formed.
**Problem**: A definition deferred forward, then a justification paragraph defending the definitional choice — the flagged "prose justifies document ordering / non-circularity" and "multiple paragraphs defer to the same downstream location" patterns compounding. The path-independence fact is then re-used inside the inductive step's "Witness preservation" clause anyway, so it is argued twice.
**Required**: Define `R_Σ` and `delegated_Σ*` once at the point of first use (the Definition (delegated) block), stating only the construction. Fold the single load-bearing fact (most-specific covering principal is preserved as `Π` grows, by condition (vi)) into the inductive step where it is consumed; drop the standalone coincidence paragraph.

### Issue 4: O10's single-baptism construction is restated four times
**ASN-0042, O10 (DenialAsFork)**: the construction `a' = pfx(π).0.{hwm_0 + 1}` with `hwm_0 := hwm(Σ.B, pfx(π), 2)` and the unilateral single-baptism claim appear in (i) the *Construction* paragraph, (ii) the inline `Unilateral O10★` blockquote, (iii) the paragraph immediately after the blockquote ("The single-baptism witness is unconditional: PrefixBaptismCoupling ensures …"), (iv) the Formal Contract *Postconditions*, (v) the Formal Contract *Unilateral postcondition*, and (vi) the *Invariant*.
**Problem**: The same formula and the same unconditionality argument ("PrefixBaptismCoupling ensures every sub-delegate's prefix lies in `Σ.B`, so `hwm_0 + 1` is never claimed") are repeated five-plus times. A precise reader must confirm each restatement is identical rather than a subtle variant.
**Required**: State the construction and the unconditionality argument once (in the proof body). The blockquote and the post-blockquote paragraph are redundant with the Formal Contract's *Unilateral postcondition*; collapse to a single statement.

### Issue 5: `pfx(π)` axiom enumerates downstream consumers
**ASN-0042, pfx(π) (OwnershipPrefix)**: "*Related properties (derived invariants, stated separately):* injectivity is O1b; the account-level boundary (`zeros(pfx(π)) ≤ 1`) is O1a." This is repeated in the Properties Introduced table row for `pfx(π)`.
**Problem**: A definition's introduction enumerating its downstream consumers rather than advancing its own meaning — the flagged pattern. O1a and O1b carry their own statements and provenance; the pointer adds nothing the index doesn't already give.
**Required**: Drop the "Related properties" line from the axiom; the table cross-reference suffices.

### Issue 6: "Summary of the Model" duplicates the Properties Introduced table
**ASN-0042, Summary of the Model**: the numbered 10-point list ("1. *Structural* … (O1) … 10. *Fork-inducing at boundaries* … (O10)") restates the table that immediately follows.
**Problem**: Two summaries of the same properties back-to-back. The prose list adds adjectival gloss but no formal content beyond the table.
**Required**: Keep the table (formal) and reduce the summary to the one genuinely new sentence — that principal identity is exogenous to O1–O10 — or delete the list.

## OUT_OF_SCOPE

### Topic 1: Ownership transfer invariants
**Why out of scope**: The tension Nelson raises ("someone who has bought the document rights") and the divergence between provenance (O6) and authority (O2) under a transfer regime is correctly deferred to the Open Questions. Formalizing transfer belongs in a future ASN, not here.

VERDICT: REVISE
