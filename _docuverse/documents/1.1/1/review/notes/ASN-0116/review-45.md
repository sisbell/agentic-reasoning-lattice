# Review of ASN-0116

This is a dense, carefully constructed note. The composite decomposition (K.α × n → K.μ⁻ → K.μ⁺ → K.ρ × n) is sound, the gapped-vs-filled arrangement bookkeeping (`M'(d) = M'₀(d) ∪ block`) is handled honestly, the I-NEW block-exclusion attribution is genuinely rigorous, the range-based provenance discharge of J0/J1★/J1'★ is correct, and IP6's containment-not-emptiness wp is a real, non-trivial result. Boundaries — append, empty-subspace (both content-region sub-cases), front-insertion at `n'_{s_C}=0` — are all walked through. Two issues remain.

## REVISE

### Issue 1: The `k = 0` boundary of the shift indexing is unaccounted for

**ASN-0116, "The problem" + I-NEW + IP1 + worked example**: The setup defines the shift as "the ordinal shift `shift(v, n) = v ⊕ δ(n, #v)`" citing OrdinalShift, and I-NEW then asserts `(A k : 0 ≤ k < n : ... M'(d)(shift(p, k)) = shift(a, k))`. The worked example computes `A_new = {shift(a, 0), shift(a, 1)} = {[d.0.s_C.7], [d.0.s_C.8]}`, i.e. `shift(a, 0) = a`.

**Problem**: At `k = 0` the operation depends on `shift(p, 0) = p` (the block starts at the insertion point) and `shift(a, 0) = a` (the run starts at the allocated address). But OrdinalShift (foundation) carries the precondition `n ≥ 1`, and the stated formula does **not** extend to `n = 0`: `δ(0, #v)` is the zero tumbler — OrdinalDisplacement itself requires `n ≥ 1` — and `v ⊕ (zero tumbler)` is undefined because TumblerAdd requires `Pos(w)`. So `shift(·, 0)` cannot be computed from the formula the note states; it is the separate convention `shift(t, 0) := t`. The note relies on that convention in load-bearing positions (I-NEW, IP1, IP3, the worked example) without stating or citing it — even though the foundations it builds on (ASN-0036 S8, ASN-0058 OrdinalShiftBase, ASN-0084 ExtendedAssociativity) all state it explicitly.

**Required**: State or cite the convention `shift(t, 0) := t` where the `0 ≤ k < n` shift-indexing is introduced (a single clause referencing ASN-0036 S8 / ASN-0058 OrdinalShiftBase suffices). Without it, the first block slot and first allocated address are notationally undefined.

### Issue 2: The "position-based reader" J1'★ aside describes an impossible violation

**ASN-0116, worked example (J1'★ trace)**: "The subtle case is the shifted suffix: `a_3, a_4, a_5` now occupy the *new* slots `q_5, q_6, q_7`, yet they are range-old … and so receive **no** new record. A position-based reader who recorded them (because their V-positions changed) would manufacture entries with no range-new witness, violating J1'★".

**Problem**: At the pre-state `Σ` (a composite boundary, by precondition), P4★ gives `Contains_C(Σ) ⊆ R`; since `q_3, q_4, q_5 ∈ V_{s_C}(d)` map to `a_3, a_4, a_5`, the pairs `(a_3, d), (a_4, d), (a_5, d)` are already in `R`. Provenance records are `(I-address, document)` pairs — they carry no V-position — so a "position-based reader" re-recording the shifted suffix would write entries already present in `R`; the result is a no-op on `R`, never an element of `R' \ R`. J1'★ constrains only `R' \ R`, so the described violation cannot occur. The justification "violating J1'★" is unsound, and the hypothetical reader is an implementation the range-based architecture already excludes. The genuine point — provenance keys on I-address, so a position change induces no record — is correct; only the cited mechanism is wrong.

**Required**: Restate the aside without the impossible violation: because provenance keys on `(I-address, document)` and the shifted suffix retains its I-addresses (already in `R`), it induces no new entry — there is no J1'★ violation to avert. Or drop the hypothetical.

## OUT_OF_SCOPE

The note's Open Questions correctly defer shared-position transclusion, concurrent-insertion freshness, transclusion provenance, and post-edit fragmentation — all genuinely future territory, none a defect here. Nothing to add.

VERDICT: REVISE
