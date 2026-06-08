# Review of ASN-0102

I checked the core mechanics (effect clause, the three position classes, the tiling in X16), the `wp(COPY, S3★)` reduction, the run-fragmentation argument in X8, and the full invariant discharge in X14. The operational content is sound: the three V-classes tile `[1, n_S+W]` without gap or overlap, S2/S8a are correctly re-established, and the source-V-contiguity argument closing the within-reference no-merge claim is valid. There is a non-trivial wp and four worked examples, so the depth requirements (concrete examples, wp analysis) are met.

My findings are accretion, consistent with the `review-mode.anti-bloat` classifier.

## REVISE

### Issue 1: X2 recites K.α's allocation mechanism instead of advancing the corollary
**ASN-0102, X2 (NoFreshAllocation)**: "K.α selects between two cases on the per-document content set `D_d`... When `D_d = ∅` the next address is the *first emission* `[d.0.s_C.1]`, determinate and unchanged. When `D_d ≠ ∅` the next address is the *subsequent emission* `inc(a_prev, 0)` off the per-document frontier `a_prev = max D_d`..."
**Problem**: X2 is "a corollary of X1." The conclusion it needs is only: `D_d` is identical at `Σ` and `Σ'` (from X1 + X6), so the same K.α case fires with the same handle. Enumerating *what the handle is* in each case (`[d.0.s_C.1]` vs `inc(a_prev,0)`) recites K.α's internal mechanism and does not advance the "unchanged" claim — it is essay content reproducing ASN-0093.
**Required**: Reduce to the load-bearing step — `D_d` unchanged (X1, X6) ⟹ K.α's allocation handle unchanged — and drop the per-case emission recitation.

### Issue 2: X14's mid-composite coupling prose explains the composite framework rather than COPY's effect
**ASN-0102, X14**: "This is the *mid-composite* case: an earlier elementary step of the same composite (an earlier K.μ⁺ or COPY) may have made `a` resident after `Σ_0`, so `(a, d)` may be genuinely `R`-new at the composite level; J1'★ is nonetheless discharged because `a` is range-new relative to `Σ_0`."
**Problem**: COPY's coupling obligation is its step-local recording fact (SL); the composite-level J1★/J1'★ verification is a property of `ValidComposite★` (ASN-0047), evaluated between the composite's boundaries. This paragraph narrates composite-framework subtleties (what *other* steps of an enclosing composite might do) rather than what COPY contributes. It is rationale around the coupling clause, not a statement of COPY's effect.
**Required**: State only what COPY discharges — (SL) plus the `Σ_0`-residency split needed to show its *unconditional* write never violates J1'★ — and remove the imagined enclosing-composite narration.

### Issue 3: the `Σ_0`-residency / A-membership split is re-stated three times
**ASN-0102, X14**: the same case analysis ("`a ∉ ran_{s_C}(M_{Σ_0}(d))`" vs "`a ∈ ran_{s_C}(...)` ⟹ by P4★ at `Σ_0`, `(a,d) ∈ R_{Σ_0}`, persists by P2") recurs in the J1'★ discharge, then again in the P4★ discharge ("If `d' = d`... a pre-state-range member... a member of `A`..."), then again in the P4a discharge ("A pair already in `R_{Σ_0}`... A pair in `R' ∖ R`...").
**Problem**: Three paragraphs in the same section carry the same split (already-resident-at-`Σ_0` vs newly-recorded-from-`A`) in different words — the "two paragraphs saying the same thing" accretion pattern, compounded across the three boundary obligations.
**Required**: Factor the split once (e.g., as a single lemma: post-state `s_C`-range = pre-state `s_C`-range ∪ `A`, with `A`-members recorded by SL and pre-state-range members carried by P4★+P2), then cite it in each of P4★, P4a, J1'★ rather than re-deriving it.

## OUT_OF_SCOPE

(none — the ASN's Open Questions are appropriately forward-looking and no claim strays into INSERT/DELETE/REARRANGE/link/version/replication mechanics.)

VERDICT: REVISE
