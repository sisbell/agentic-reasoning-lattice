# Review of ASN-0134

This is a careful note — the proofs spell out cases (H1's two axes, H2's interior *and* first-emission boundary, H0's sub-cases), the boundary sizes are covered (`m=0`/`m=1`/`m≥2` batches, `N=0`/`N≥1` stale), the conditional claims are marked as conditional (the §4 shared-frontier family, H3, SAFE(c)), foundation use is clean (all five dependencies are foundations; no illicit cross-references), and there are no checkmark or "by similarly" hand-waves. The §7 tumbler arithmetic checks out, and the §8 V2 strictness witnesses are genuine. Two issues remain.

## REVISE

### Issue 1: "Linearizable but not sequentially consistent" rests on an unstated, non-standard linearizability

**ASN-0134, §3 / G0 (§3) / Claims table**: §3 defines linearizability as "*the order respecting real-time precedence between a response and a subsequent invocation*"; G0 asserts it coexists with non-SC because "*linearizability constrains only the non-overlapping (real-time-ordered) operations and is met, while SC demands the overlapping pair keep program order and is not*"; the Claims table records G0 as "*not sequentially consistent; linearizable under A7*."

**Problem**: Textbook linearizability *implies* sequential consistency — its equivalence condition (L1) requires the witnessing serial order to respect each process's program order, exactly what SC requires, so any linearizable history is SC. The note obtains the textbook-impossible combination "linearizable ∧ ¬SC" only by treating agent P's two pipelined emissions inconsistently across the two claims:

- the SC counterexample needs `A <_S B` (P emitted A *then* B in program order) to close its cycle `A <_S B <_S (read β) <_S (read α) <_S A`;
- the linearizability claim treats the very same pair as *unordered* ("overlap in real time," so "linearizability constrains only the non-overlapping operations").

Under a *single* consistent program-order treatment the combination collapses: if A,B are program-ordered, textbook linearizability's L1 also forces `A <_S B`, the substrate's B-before-A commit violates it, and the execution is *not* linearizable either; if A,B are unordered, SC imposes no `A<B` constraint, the cycle dissolves, and the execution *is* SC. The bald assertion "linearizability constrains only the non-overlapping operations" is false for textbook linearizability — it is true only for a real-time-precedence-only weakening that the note adopts without flagging it as weaker than standard. A reader applying the standard hierarchy will read "linearizable but not SC" as an error.

**Required**: State explicitly that the note's "linearizability" is real-time-precedence-only and omits the per-process program-order (equivalence) constraint of textbook linearizability; note that it is therefore strictly weaker than textbook linearizability and does *not* imply SC (so the coexistence with "not SC" is not a contradiction of the standard Lin⟹SC theorem, which assumes sequential-process clients); and reconcile that the SC witness treats P's A,B as program-ordered while the linearizability claim treats the same pair as unordered — the pipelining regime is precisely where these two orders diverge, and that divergence is what the claim leans on.

### Issue 2: Forward-reference accretion — §1 previews §6's contiguity-vs-atomicity point

**ASN-0134, §1 (post-A5) and §6 (W2 aftermath)**: §1 states "*That contiguity therefore does not construct atomicity — a writer-side section leaves the reader gap open — is W2's scoping, taken up in §6. The one batch the corpus demands be (locally) contiguous — the definition's content run — we return to in §6.*" §6 then delivers it: "*Contiguity is all W2 buys, and the distinction §1 flagged is W2's to carry… it does not construct atomicity.*"

**Problem**: The §1 sentences introduce a §6 construct (W2, run contiguity — not yet defined in §1) only to defer it back to §6, with the point then restated in §6 carrying a back-reference to §1. The §1 prose does not advance §1's local argument (whose job, A5, is the step/batch grain); it is a forward-pointer the precise reader must work around, and the substance lives entirely in §6. The pattern recurs across the note's forward-reference web on the same deferred topic: §2's A6-aftermath previews "*the seed of §8's V1*," and §6 in turn defers the reader-side half to Open Question 4 — three sections building toward one deferred gap (reader-side batch atomicity) through connective meta-prose rather than a single statement plus the open question.

**Required**: Drop the §1 preview sentences ("is W2's scoping, taken up in §6"; "we return to in §6") and let §6/W2 carry the contiguity-vs-atomicity distinction at its single home; trim the parallel forward-pointers ("seed of §8's V1") to whichever section actually establishes the point, with OQ4 the sole defer-target for the reader-side gap.

## OUT_OF_SCOPE

### Topic 1: Verdicts over content population (reads of `dom(C)`)
§8 fixes the read surface as link-store reads (active views, frontier descents); A5 correctly observes a content run's mid-batch prefix "is witnessed by no read the note models." A quiescence/completeness predicate over *content* population would need a content-read primitive absent from ASN-0128's typed-relation surface.

**Why out of scope**: This is a new read primitive on top of the foundation surface, not a defect in this note's contract; the note works correctly within the surface it inherits and flags the limitation.

### Topic 2: Reader-side batch atomicity (Open Question 4)
The gap A5 isolates — making a multi-step batch appear all-or-nothing to a reader — is correctly identified and deferred to OQ4 rather than asserted.

**Why out of scope**: A genuine future contract, already named as an open question; not a missing obligation in MIC.

VERDICT: REVISE
