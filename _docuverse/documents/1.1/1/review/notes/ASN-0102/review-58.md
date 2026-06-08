# Review of ASN-0102

## REVISE

### Issue 1: J1'★ discharge establishes the wrong conjunct and deflects the rest

**ASN-0102, X14 (J1'★ paragraph)**: "Every pair COPY adds is `(a, d)` with `a ∈ A`, and by the effect clause COPY maps each such `a` at a content-subspace position `v + c` (P3), so `a ∈ ran_{s_C}(Σ'.M(d))` … a composite that nonetheless leaves a COPY-recorded pair without a boundary-level range extension is *rejected* by `ValidComposite★` (clause-2), not admitted by it."

**Problem**: J1'★ (ASN-0047) requires, for each `(a,d) ∈ R' \ R`, **two** conjuncts: (i) `a` present in the post-state content-subspace range, **and** (ii) the range-*new* conjunct `¬(E v ∈ dom(Σ.M(d)) : subspace(v) = s_C ∧ Σ.M(d)(v) = a)`. The X14 paragraph establishes only conjunct (i) (range *membership*). For an `a ∈ Old = A ∩ ran(Σ.M(d))`, conjunct (ii) is *false* — `a` was already in the pre-state content range. The discharge is saved only because such `a` are not in `R' \ R` (already in `Σ.R` by the P4★ inductive hypothesis `Contains_C(Σ) ⊆ Σ.R`), but that reasoning appears in a *different* paragraph (P4★) and in the self-transclusion example, never connected to the J1'★ discharge itself. As written, the J1'★ argument proves the wrong thing and then deflects the residual obligation onto `ValidComposite★`'s rejection rule rather than discharging it.

**Required**: Discharge J1'★ in the main text with the explicit `New`/`Old` split: for `a ∈ New`, both conjuncts hold by definition of `New`; for `a ∈ Old`, show `(a,d) ∈ Σ.R` (via the entering inductive hypothesis `Contains_C(Σ) ⊆ Σ.R`) so `(a,d) ∉ R' \ R` and the antecedent is vacuous. Do not lean on the example to carry the general proof.

### Issue 2: X8 pre-states and duplicates X12's boundary-absorption content

**ASN-0102, X8 (RunFragmentation)**: "The whole-arrangement maximal merge (M12 of `Σ'.M(d)`) may reduce the count further at the two abutment boundaries where the copied region meets the surrounding arrangement (X12). Either, both, or neither may fire — generically neither does…"

**Problem**: This is forward-reference accretion. X8 narrates, parenthesizes `(X12)`, and pre-explains the two-boundary absorption mechanism that X12 then *owns* and fully derives ("The copied region meets the surrounding arrangement at *two* boundaries, each an independent merge candidate under M7…"). The within-region merge count is X8's proper subject; boundary absorption is X12's. The cross-claim deferral ("may reduce further … (X12)") forces the reader to hold an unproved claim across two claims.

**Required**: Confine X8 to within-region fragmentation (`≤ k`); state once that boundary behavior is treated in X12 without re-describing the firing conditions, or move the abutment sentence entirely into X12.

### Issue 3: PC1 mischaracterizes the per-reference run count

**ASN-0102, "The source designation and its resolution"**: "each `k_i` is the maximal-contiguous-I-run count of reference `r_i` taken in isolation (C1a, M12 applied per reference)."

**Problem**: The per-reference block count from `resolve(d_s, σ)` (ASN-0058, C1a/M12) is the count of *maximal runs* — blocks maximal under the merge condition, which requires *joint* V-adjacency and I-adjacency. "Maximal-contiguous-I-run count" names only the I-side and misdescribes the decomposition the citation actually supplies.

**Required**: Replace with "maximal-run count" (the C1a/M12 decomposition) or state both contiguity conditions.

### Issue 4: Procedural narration in X14

**ASN-0102, X14**: "We must show this post-state is well-formed against the coupling invariants…"; "Each clause below is discharged once against `B`."; "Setup — `New` vs. `Old`…".

**Problem**: These are meta-prose narrating the proof's organization rather than advancing it (review carries `review-mode.anti-bloat`). The reader must skip past the scaffolding to reach the discharges.

**Required**: Drop the procedural framing sentences; let the per-clause discharges stand on their own.

## OUT_OF_SCOPE

### Topic 1: Re-displacement of copied content by a later operation
The first Open Question (origin/discoverability tie under subsequent displacement) concerns INSERT/DELETE/REARRANGE acting on already-copied content — operation mechanics excluded from this ASN. Correctly deferred.

VERDICT: REVISE
