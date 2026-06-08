# Review of ASN-0100

I checked the substrate decomposition, the six worked examples, every invariant in ExtendedReachableStateInvariants / ExtendedTransitionInvariants, and the two wp computations. The technical content is sound: every conjunct of the per-state invariant package is discharged (including the easily-skipped ones — L14 via fresh-`a_k ∉ dom(L)`, P3 via the P0∧P1∧P2∧L12 synthesis, S8★ via INS.C1a-app), the disjointness/exhaustiveness argument for S2 is complete, the K.μ⁻-omission cases are handled, and the boundary cases (append, prepend forced full-shrinkage, empty document, re-insertion into a cleared subspace, deep `m_C=3` off-prefix exclusion) are each exercised by a distinct example. I found no missing case and no broken derivation.

The findings below are all anti-bloat (`review-mode.anti-bloat`): residual meta-prose that a precise reader must read past. They are minor, but per the mode they are flagged at source.

## REVISE

### Issue 1: Reusability inventory in INS.I3-coincide
**ASN-0100, Effect Three (INS.I3-coincide)**: "Because `M'(d) ↾ (Left ∪ Shifted-right)` *is* (pointwise) the I3-specified arrangement on that domain, every I3 lemma about `M_{I3}` transports verbatim to that restriction."
**Problem**: This is a blanket use-site inventory ("every I3 lemma transports"). Each downstream verification site already names the specific lemma it needs (I3-S2 in §S2, I3-S3 in §S3★, I3-VP/I3-VD in §S8a, I3-fin in §S8-fin). The blanket sentence asserts reusability that the per-site citations re-establish individually; it advances no reasoning on its own.
**Required**: Drop the trailing sentence; the pointwise-coincidence equality immediately preceding it is the load-bearing fact, and the per-site citations carry the rest.

### Issue 2: Defensive non-claim in S8★ verification
**ASN-0100, §Per-subspace span decomposition (S8★)**: "The single C1a object discharges all of S8★'s conditions on the content subspace; no separate run construction is needed."
**Problem**: "no separate run construction is needed" justifies the absence of a technique rather than advancing the discharge. The C1a invocation and the M12b/M12a citations that follow already establish the conditions; the disclaimer is residue.
**Required**: Delete the clause after the semicolon.

### Issue 3: Summary restatement closing the prepend example
**ASN-0100, §A Worked Example (prepend case)**: "This combination — forced full shrinkage (`n'_{s_C} = 0`) plus total shift plus re-pin of the minimum — is the `j = 0` instance of the general decomposition; the `n'_{s_C} = 0` retention is not an optional alternative here but the only admissible value."
**Problem**: The example body already exhibits `n'_{s_C} = 0` as forced (Left = ∅, and the uniqueness section pins the retention range to `{0,…,p_m−1}` = `{0}` at `p_m = 1`). This closing sentence restates that content as a labelled summary in the example slot.
**Required**: Remove the restatement; the worked steps and their invariant checks already make the point.

## OUT_OF_SCOPE

### Topic 1: Link-subspace insertion (`K.μ⁺_L` analogue)
**Why out of scope**: Explicitly bounded out by the ASN and by the scope directive; the open question about link-subspace insertion invariants is correctly deferred, not an error here.

### Topic 2: Concurrent/independent-agent INSERTs and crash recovery
**Why out of scope**: Listed as open questions; these are future-ASN territory (serialisation basis, partial-failure recovery), not gaps in the single-state per-operation semantics this ASN fixes.

VERDICT: REVISE
