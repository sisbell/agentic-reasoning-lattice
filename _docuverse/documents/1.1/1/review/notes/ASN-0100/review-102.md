# Review of ASN-0100

This note is mature — I checked the invariant proofs against the full ExtendedReachableStateInvariants list (S0/P0, S2, S3★, S8-depth/a/fin/★, D-CTG★/MIN★/SEQ★, S4, S7a/b/d, C1b/c, P6/P7/P7a, P4★/P4a, L0/L1/L1a–c/L3/L12/L14/L-fin, CL-OWN/UNIQ, S3★-aux, M0/M1, P1/P2/P3, P8) and the boundary cases (j=0, j=N append, empty document, empty-after-clearance, n=1, full-shrinkage decomposition). The forward arguments, the per-step atomicity bookkeeping, the projection-shift derivation, the wp analyses, and the uniqueness/forced-ordering analysis all hold up. All inter-ASN references are to foundation ASNs, so no self-containment violation. I found no rigor gaps.

The note carries the anti-bloat classifier, and the remaining findings are accreted prose, not correctness.

## REVISE

### Issue 1: Fourth worked example is self-admittedly redundant
**ASN-0100, §A Worked Example ("Empty-document re-insertion after full clearance")**: "The composite, post-state, and V-side invariant discharge then match the first-insertion example position-for-position; the sole difference is the K.α branch, which we isolate here."
**Problem**: This is the "two paragraphs say the same thing in different words" pattern. The example reproduces the full machinery of the preceding empty-document first-insertion example (K.μ⁺ placement, K.ρ firings, depth re-pinning, invariant discharge) to convey a single distinction: that a cleared subspace can carry residual content, so K.α fires the *subsequent*-emission branch (`a_0 = inc(a_prev, 0)`) rather than first-emission. Four worked examples (interior, append, empty-first, empty-re-insertion) is one more than the structural cases warrant.
**Required**: Compress the re-insertion case to a short note appended to the empty-document first-insertion example, stating the cleared-but-residual subtlety and the subsequent-emission branch in one or two sentences, rather than restaging the whole composite.

### Issue 2: Frame-proof restatement after the proof is complete
**ASN-0100, §Frame Conditions**: "`E' = E`. The entity set is unchanged: no K.δ fires in the decomposition, hence `E'_doc = E_doc`; INSERT registers no new document and creates no new node, account, or non-document entity."
**Problem**: The proof concludes at "no K.δ fires in the decomposition, hence `E'_doc = E_doc`." The trailing clause enumerating entity strata (node/account/non-document) that `E' = E` already excludes is defensive elaboration restating the conclusion. This is the same K.δ-rationale residue that f889b12/34e613ac began trimming, left in the entity-frame slot.
**Required**: Delete the trailing enumeration; the "no K.δ fires" step is the proof.

## OUT_OF_SCOPE

(none)

VERDICT: REVISE
