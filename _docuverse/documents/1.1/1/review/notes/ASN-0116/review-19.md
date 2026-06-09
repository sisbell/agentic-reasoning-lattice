# Review of ASN-0116

The operation is mathematically rigorous: the displacement arithmetic (`shift(q_k, n) = q_{k+n}`), the three-interval domain partition, the valid-composite decomposition over K.α/K.μ⁻/K.μ⁺/K.ρ, the coupling-constraint discharge (J0/J1★/J1'★/P7a at the boundary), the witness-set bijection of P4, the containment weakest-precondition of P6, and the worked example all check out. Boundary cases (append `J=N+1`, empty subspace, front-insert `J=1`) are handled. The K.μ⁻+K.μ⁺ split correctly evades K.μ⁺'s prior-domain-agreement constraint. I found no correctness gap.

The findings below are meta-prose accretion, surfaced under the note's `review-mode.anti-bloat` classifier.

## REVISE

### Issue 1: Use-site inventories appended to the new frame clauses
**ASN-0116, Effect / F-LINK**: "This is the stated premise on which the post-state inherits the per-state link invariants (L0, L1, L1a, L1c, L3, L14, L-fin, CL-OWN, CL-UNIQ) of ExtendedReachableStateInvariants (ASN-0047), and on which P5 and the P4 link-survival argument lean."
**ASN-0116, Effect / F-ENT**: "so the post-state inherits the entity invariants (S7d, NodeLineage, ActivatedEmission) by frame."
**Problem**: The frame claim (`Σ'.L = Σ.L`, `Σ'.E = Σ.E`) and its one-line justification ("none of INSERT's K-atomics touches `Σ.L`") are complete and advance the argument. The trailing enumeration of nine link invariants plus P5/P4, and of three entity invariants, is a use-site inventory — it lists downstream consumers rather than advancing the clause's meaning. The dependence belongs at (and is established at) the consuming sites, not catalogued in the frame clause. These clauses were just added (commit fa16cc572) and the inventory is exactly the accretion pattern the classifier flags.
**Required**: Drop the consumer inventories; keep the frame statement and its K-atomic justification.

### Issue 2: Placement-justifying forward pointers to the same downstream discharge
**ASN-0116, "The problem"**: "we discharge it below rather than defer it, so that the post-state satisfies the coupling invariants J0, J1★, J1'★ and the coverage property P7a that ExtendedReachableStateInvariants demands of every composite boundary."
**ASN-0116, Effect intro**: "The explicit step sequence and the discharge of each intermediate precondition are given in the next subsection."
**Problem**: Both passages justify *where* provenance/composite reasoning is placed ("rather than defer," "given in the next subsection") and point forward to the same downstream location (the valid-composite section and PROV). Justifying document ordering and stacking multiple forward deferrals to one location is flagged meta-prose; the reader meets the actual discharge regardless.
**Required**: State the provenance obligation once where it is discharged (PROV/I-PROV); remove the placement-rationale and the redundant forward pointer.

## OUT_OF_SCOPE

The four Open Questions (transclusion at a shared insertion point, concurrent fresh allocation without a serializer, provenance under transclusion, post-fragmentation contiguity) are correctly deferred — they fall under the retired/reframed COPY, REARRANGE, and concurrency work, not this ASN.

VERDICT: REVISE
