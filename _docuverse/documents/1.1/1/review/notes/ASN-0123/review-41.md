# Review of ASN-0123

I checked the load-bearing proofs and worked them by hand: VN-B1's case analysis (the k=2/k=1/k=0 routing into a version namespace), the SA antichain argument, the severance theorem V9(a) and its structural O5(ii) maximality, V8's coverer-set equality, the G2 necessity argument (range-preservation forced via SA), V-WF's discharge of both ValidComposite★ clauses in both branches, and the three worked instances (addressing, owned carry-through, cross-owner carry-through). They hold. I found no correctness defect, no missing boundary case (empty source n=0, shared-content repeats |A|<n, iterated fork, links-only source are all covered), and no off-scope drift. The note is technically converged.

The findings below are the ones the `review-mode.anti-bloat` pass is for: accreted meta-prose around the precondition and the boundary dependency.

## REVISE

### Issue 1: P-tier carries a design-rationale walkthrough of a case the precondition excludes
**ASN-0123, The Operation (P-tier comment)**: "That restriction is what holds the fork to a single mint: a node-tier non-owner (zeros(pfx(π)) = 0, which O1a admits into Π) holds no document namespace, so reaching a document from a bare node prefix would first baptize an intermediate account — a second permanent entity (P1), breaking the single mint — and must instead establish an account first, an out-of-scope prior act; the account-tier restriction thus places the node-tier non-owner outside the domain."
**Problem**: P-tier's second disjunct (`zeros(pfx(π)) = 1`) already excludes the node-tier non-owner. This block then imagines that excluded case at length and supplies single-mint motivation inside a precondition slot. Single-mint is V0's claim, not the precondition's, and a precondition does not need a motivating essay to stand. This is reviser-drift (a paragraph reasoning about a case the carrier excludes) plus design-rationale prose the reader must read through to confirm no further condition is being imposed.
**Required**: Cut the node-tier walkthrough. If any justification is retained, compress to one clause — e.g. "the cross-owner branch is account-tier so the fork mints exactly one identity (reaching a document from a node prefix is an out-of-scope prior act)" — and let V0 carry the single-mint property.

### Issue 2: V9w re-litigates the boundary/interior subtlety already carried by the atomicity remark
**ASN-0123, V9w**: "The boundary hypothesis is load-bearing: P4★ is a composite-boundary property, not a per-state invariant — ASN-0047 classes it so precisely because it may fail at interior states — and P-bdy is what supplies the boundary that licenses its use for the source-side row here."
**Problem**: The two sentences preceding this already discharge `(a, d_src) ∈ R` by invoking P4★ at the P-bdy boundary — that citation is complete. The added gloss asserts the dependency is "load-bearing" and explains *why ASN-0047 classifies P4★ as a boundary property* ("because it may fail at interior states"). That is foundation-classification rationale layered on a finished step, and it restates the interior-vs-boundary theme the Remark (atomicity) already develops. It does not advance the proof.
**Required**: Drop the gloss; the P4★-at-boundary citation stands on its own. The interior-state caveat, if wanted, belongs once — in the atomicity remark.

## OUT_OF_SCOPE

None. The ASN respects the declared scope: it defines no INSERT/DELETE/COPY/REARRANGE, no link-creation or comparison operation, and touches windowing (V11) and J4 only as frame/foundation clarifications. The eight Open Questions correctly defer future territory (concurrent-fork serialization, derivation-direction recovery, link-subspace carry, supersession) rather than smuggling it into this note.

VERDICT: REVISE
