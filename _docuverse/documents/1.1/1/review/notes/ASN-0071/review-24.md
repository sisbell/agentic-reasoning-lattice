# Review of ASN-0071

I checked the operation definitions, the resolution and find semantics, the PC/subspace-confinement proofs, the codomain (content-only) argument, the finiteness induction, and recomputed every worked scenario (single-address `Q`, multi-block `Q_D`, cross-depth `Q_E`, interior-action-point rejection).

## REVISE

(none)

The proofs that are most often hand-waved are here done explicitly:

- **Prefix confinement (PC)** is proven from TumblerAdd prefix-copy + T1, including the easily-skipped *totality* sub-argument (`#t ≥ #u`, the T1 case-(ii) exclusion) before comparing components — and it correctly avoids borrowing ASN-0058's C0a, which the vspec relaxation discards.
- The `actionPoint(ℓ) = #u ∧ #ℓ = #u` preconditions correctly force `ℓ = δ(ℓₘ,#u)` (leftmost-nonzero = deepest), so "`actionPoint ≥ 2` equivalently `ℓ₁ = 0`" holds and the interior band `2 ≤ actionPoint < #u` is genuinely non-empty only at `#u ≥ 3` — which the depth-3 `d_E` extension then exercises against a live arrangement rather than leaving abstract.
- Boundary cases are covered: empty query (F-EMPTY), unresolvable positions (F-FILT, with the infinite-`⟦σ⟧` intersection made explicit), shared I-address across positions and documents (F-DIST, F-PART via the multi-block `Q_D`), source `d_s ∉ E_doc` (wp-defined), and the exclusion direction tested against a concrete non-containing `d_C` (F-SOUND).
- The codomain argument invokes S3★ **and** S3★-aux (foreclosing a third subspace) plus L14, rather than leaving "only content matches" as an assertion.
- Finiteness is a clean three-step induction over *elementary* (not composite) transitions, correctly noting one composite may fire several K.δ steps.

Recomputed results match: `find(Q)(Σ) = {d_A,d_B,d_D}`, `find(Q_D)(Σ) = {d_A,d_B,d_C,d_D}`, `find(Q_E)(Σ⁺) = {d_A,d_B,d_C,d_D,d_E}`. All reach/intersection computations check out.

## OUT_OF_SCOPE

### Topic 1: Historical containment via `R`, distributed completeness, visibility filtering
**Why out of scope**: These are future operations (an `R`-based "ever-contained" query, replication consistency, access-control post-filtering). The ASN already isolates them in its Open Questions and "What we do not specify," and commits `find` to current-state semantics. No claim overreaches.

Foundation usage (ASN-0047/0053/0058) is consistent; no non-foundation ASN is cited by number; no reinvented notation.

VERDICT: CONVERGED
