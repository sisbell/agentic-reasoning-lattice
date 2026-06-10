# Review of ASN-0115

I checked the load-bearing proofs against the substrate: the Confinement lemma (T5 application is sound, `p ≼ t` correctly transferred), the override "bites only in the shallow case" argument (the deep case `#s > m_S(d)` genuinely forces an empty geometric intersection via the `#s = m_S(d)+1` reconciliation), R6's no-interior-hole / terminal-overrun argument (correctly scoped to the bindable slice, D-SEQ★ frontier respected), R7's repeatability proof (correctly handles that `act`'s depth branch reads the whole subspace, not just the `⟦σⱼ⟧` restriction), R8's subspace-sharing dispatch (S3★-aux + S3★ + SD) and link-vacuity (CL-OWN + CL-UNIQ), and all five worked instances (R6, R8, R9, R10, R11). The arithmetic in every worked instance checks. The wp analysis in R11 is genuine and non-trivial. No correctness gap, no missing edge case, no bad cross-reference (every citation is to a foundation ASN), scope respected.

The one finding is in the prose dimension the `review-mode.anti-bloat` classifier targets, and it sits in the area the most recent commit touched ("clarify arrangement mutability in act override and R4/R7").

## REVISE

### Issue 1: The cite-and-don't-edit discipline is fully developed in both R4 and R7
**ASN-0115, R4**: "…so 'as it stood' coincides with 'current' only for a version whose arrangement is not subsequently edited — *a discipline the caller keeps by citing-and-not-editing*, not an invariant the address enforces."

**ASN-0115, R7**: "…repeatability holds exactly when the consulted restriction is unchanged — R7's hypothesis — *which a caller secures by citing a version whose arrangement it does not subsequently edit.*"

**Problem**: These two clauses state the same caller discipline in different words — exactly the "two paragraphs in the same document say the same thing" pattern. The theme is reinforced a third time in the substrate recap ("the one component that may lose entries through editing … P3") and a fourth in the Synthesis ("the arrangement is the only mutable input"). R4 and R7 each have a *legitimate local hook* for mentioning mutability — R4 must rebut "naming a version freezes its arrangement," and R7 must interpret the unchanged-restriction hypothesis — but the *full caller-discipline restatement* belongs to one of them, not both. Spread across four sites, the point reads as accreted clarification rather than one statement.

**Required**: State the citing-and-not-editing discipline once, in R7 (where repeatability/stability is the subject and the S0-vs-arrangement-immutability framing already lives). In R4, keep only what version-relativity needs — "resolution is against the *current* `Σ.M(dⱼ)`; the arrangement is mutable (P3), so naming a version does not freeze it" — and drop the duplicate "a discipline the caller keeps by citing-and-not-editing" clause. Leave the substrate mention as bare foundation recap and let the Synthesis summarize without re-deriving the discipline.

## OUT_OF_SCOPE

(none — the genuinely out-of-scope topics, namely inline-provenance, outright failure, dangling references under relaxed S3★, channel faithfulness, and the boundary-straddling span, are correctly deferred to the Open Questions rather than given claims; the scope-excluded sibling operations are not defined here.)

VERDICT: REVISE
