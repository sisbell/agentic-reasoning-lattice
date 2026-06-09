# Review of ASN-0116

## REVISE

### Issue 1: Post-state well-formedness is established twice — once as K.μ⁺ preconditions, once as a standalone walk-through — and several invariants delivered free by the cited theorem are re-derived anyway

**ASN-0116, "INSERT as a valid composite" vs. "The document remains one coherent sequence" / PROV**:

The valid-composite argument discharges, as K.μ⁺'s clause-1 precondition, exactly: new-position S8a (clause ii), S8-depth/D-CTG★/D-MIN★ of the result (clause iii), and new-mapping referential integrity (clause i). Because K.μ⁺ is the last arrangement-modifying step (K.ρ does not touch M), the "result" there *is* the final post-state. The subsequent "coherence" section then re-establishes the same facts for the same state:

- *Contiguity.* Clause (iii): "the resulting content subspace `{q_1, …, q_{N+n}}` is the dense run … so S8-depth, D-CTG★, D-MIN★ hold." Re-derived in "Contiguity of the filled post-state": "By the block-disjointness fact … `V_S(d') = {q_1, …, q_{N+n}}` … This *is* the per-subspace contiguity of the post-state — D-CTG★/D-MIN★/D-SEQ★."
- *Block S8a* (clause ii ↔ "S8a and depth uniformity") and *block/new-mapping referential integrity* (clause i ↔ "Referential integrity") are likewise each established twice.

**Problem**: This is the duplication the anti-bloat directive targets — two passages establishing the same post-state property in different words. Worse, the ASN's treatment is internally inconsistent: it correctly *cites* ExtendedReachableStateInvariants for S8★ ("holds at the filled post-state directly by ExtendedReachableStateInvariants"), yet directly re-derives **P7a** (PROV section: "the post-state is a composite boundary, so it must also satisfy P7a … [direct derivation]"), **P7**, **S3★** (left/shifted regions), and **S2** (single-valuedness) — all of which ExtendedReachableStateInvariants delivers *for free* at the composite boundary once validity is shown. Once INSERT is exhibited as a valid composite, those per-state and composite-boundary invariants follow from the theorem; re-deriving them adds prose the precise reader must recognize as already discharged.

**Required**: Discharge each invariant once. Establish in the valid-composite section only what K.μ⁺'s precondition genuinely requires as an *input* to validity (new-position S8a, S8-depth, D-CTG★/D-MIN★, finiteness, new-mapping referential integrity), then lean on ExtendedReachableStateInvariants for the full post-state set — exactly as the ASN already does for S8★ — and delete the standalone re-derivations of contiguity, block S8a, referential integrity, P7a, P7, and single-valuedness. Alternatively, keep the comprehensive walk-through but explicitly mark which clauses are precondition-discharge and which are theorem corollaries, so no fact is proved twice.

## OUT_OF_SCOPE

None. The Open Questions (shared-position insertion, concurrent freshness, transclusion provenance, post-edit fragmentation) are correctly framed as future territory rather than claimed here, and the body references only foundation ASNs (0034, 0036, 0043, 0047, 0082, 0093, 0098).

VERDICT: REVISE
