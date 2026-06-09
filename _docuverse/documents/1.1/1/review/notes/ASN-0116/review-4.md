# Review of ASN-0116

This is a carefully constructed ASN that correctly factors INSERT into the two foundation effects (content allocation K.α and the I3 arrangement shift) and keeps the content/arrangement layers cleanly separated. The proofs are mostly rigorous — the direct discharge of S3★ (rather than inheriting the content-frame-dependent I3-S3) is exactly the kind of care the operation demands, and the bijection-not-inclusion form of P4 and the containment wp of P6 are correct. Two completeness gaps remain, one of which is a parallel of an omission the ASN itself otherwise handles well.

## REVISE

### Issue 1: New content addresses' structural invariants never discharged (I3-S7 is non-inheritable, exactly like I3-S3)

**ASN-0116, "The document remains one coherent sequence"**: "We do not inherit referential integrity from ASN-0082's I3-S3: that lemma is proved under the content frame I3-C (`dom(C') = dom(C)`, content fixed), and INSERT deliberately breaks I3-C via I-ALLOC".

**Problem**: The ASN recognizes that I3-S3 cannot be inherited because INSERT breaks the content frame — but the identical reasoning applies to ASN-0082's **I3-S7** (AllocationInvariantsPreservation), which is likewise "preserved post-insertion ... trivially by I3-C (dom(C') = dom(C)) and I3-D." INSERT breaks I3-C, so I3-S7 is equally non-inheritable. Consequently the post-state's content-store structural invariants for the freshly allocated run `A_new` — S7b (`zeros(a) = 3`), C1b (`#E(a) ≥ 2`), C2/S7a (`origin(a) = d`), C1c (allocator conformance) — are never established. The well-formedness section proves V-position properties (S8a, S8-depth, S2, S3★, contiguity) thoroughly but says nothing about whether the new *content addresses* are structurally valid element-level content. The post-state must satisfy these to be a reachable/valid state (ExtendedReachableStateInvariants, ASN-0047).

**Required**: Add an explicit clause — symmetric to the I3-S3 treatment — stating that I3-S7 cannot be inherited under INSERT's broken content frame, and that S7a/S7b/C1b/C1c for `A_new` are instead discharged by K.α (ASN-0093: C1, C1b, C1c, C2), while the unchanged addresses retain them by P2 (append-only, values fixed).

### Issue 2: OrdShiftHom cited at the k = 0 boundary where its precondition is unmet

**ASN-0116, "The document remains one coherent sequence" (new-block well-formedness)**: "By **OrdShiftHom** (ASN-0036), each `shift(p, k)` is zero-free with all components positive, `subspace(shift(p, k)) = S`, and `#shift(p, k) = m` ... So every new-block position is S8a-well-formed".

**Problem**: The block index runs `0 ≤ k < n`, so it includes `k = 0`, i.e. `shift(p, 0) = p`. OrdShiftHom's precondition is `n ≥ 1` (shift amount), so it does not cover `k = 0`. The conclusion still holds — `shift(p, 0) = p` is S8a-well-formed by the operation's precondition — but the citation is incorrect at this boundary.

**Required**: Split the case: `shift(p, 0) = p` satisfies S8a by precondition; `shift(p, k)` for `1 ≤ k < n` satisfies S8a by OrdShiftHom.

### Issue 3: I3-V attribution is inaccurate in the append case

**ASN-0116, Effect (I-NEW)**: "the INSERT-specific fill of the block that I3 leaves vacated (the positions I3-V withholds from `dom(M'(d)`) until they are re-populated)".

**Problem**: I3-V (PostInsertionVacating, ASN-0082) quantifies only over `v ∈ dom(M(d))` — pre-existing positions `≥ p` not in the shifted image. In the occupied case (`J ≤ N`) this is exactly the block, and the attribution is correct. In the **append** case (`J = N+1`, `p ∉ dom(M(d))`), the block positions `q_{N+1}, …, q_{N+n}` were never in `dom(M(d)`, so I3-V is silent about them; their absence from the gapped arrangement comes from the domain-closure characterization I3-CS, not from I3-V.

**Required**: Attribute the vacated block to I3-V in the occupied case and to I3-CS (domain closure) in the append case, or cite both.

## OUT_OF_SCOPE

(none — the open questions on transclusion, concurrency, provenance, and post-insert fragmentation are correctly deferred rather than claimed.)

VERDICT: REVISE
