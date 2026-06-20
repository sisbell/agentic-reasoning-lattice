## Review: M6 — Content Retrieval & Query

I focused skepticism on the load-bearing claims and verified each against the upstream interfaces and source notes. The ones most likely to hide a defect all hold up:

- **SHOWDELETIONS via `deletions(d_A).denotes(a)`** — exact, not a phantom. The deletion cover is a per-level-class set-difference, so it never coalesces across a non-deleted ordinal (the gap leaves the spans non-adjacent), and cross-document/cross-chain addresses sit outside any chain-pinned interval by prefix divergence. Inputs are always real content addresses from `arranged_content`. Sound, and the `ever_placed`-based fallback is a genuine safety net. No M5 amendment needed — `deletions`/`content_runs`/`denotes` are all as-given.
- **COMPARE co-chain totality + R1 soundness** — `lo < hi` provably implies one content chain (different-origin I-intervals are prefix-disjoint and never overlap in tumbler order), so every `ordinal_gap` subtraction is total. Computing `u2` against `qb.i_start` (not `pb.i_start`) is the correct fix for both feet resolving to `lo`. Full cross-product gives R2 completeness under fan-out. `fold_adjacent = identity` is conforming (R4 optional).
- **The `gate_vspec` depth split** — well-formedness gated (`#start ≥ 2`, ordinal-level, level-uniform, zero-free), depth-*compatibility* deliberately *not* gated, so `#start ≥ 3` passes and resolves to ⟨⟩ (R6 for RETRIEVEV; `RangeNotPresent` for SHOWORIGIN_V where WF_V(v) makes depth a precondition). This faithfully distinguishes 0115's consulting-state depth predicate from 0077's stricter WF_V.
- **SHOWORIGIN_I de-scope** — genuinely unbuildable from M4 (point-only, `Ord` deliberately unused, range scans forbidden) + M3 (point-only); recording it as a decomposition amendment rather than overreaching into M4 is the correct boundary call, and it's settled-by-construction (no I-arity method exists for M10 to reach).
- **R⁻¹ index in M5, not M6** — the decomposition nominally hands M6 "its reverse-index hint over R," but the *as-given* M5 interface owns `docs_containing`; interface fidelity requires M6 to consume it. Stated and resolved soundly (Conflicts 1).

All seven ops compile against M1–M5 as given; every upstream signature, ownership move, and `unwrap` safety condition checks out; no invented or contradicted upstream API; no owned capability dropped; the stateless/no-slice posture trivially satisfies the composition contract.

### Revision list (all non-load-bearing)

1. **[SHARPENING]** Consolidate and attribute the **dense-occupancy reliance** (content `[s_C,1..n_C]`, links `[s_L,1..n_L]`). It is load-bearing for `doc_vspan`/`doc_vspanset` (counts ⇒ extents) and COMPARE's V-reconstruction, but it is *not* a named invariant in M5's as-given interface. State it once with provenance — ASN-0113 W2/W4 (the `([S,1],[0,n_S])` extent formula `ext_span` literally implements), ASN-0112 V8 (origin permanence), M5's contiguity maintenance, and append-only link seating — so a builder sees why reading counts alone (and accumulating `v_start` by run width) is correct.

2. **[SHARPENING]** Note why `run_addr` (ElemPos round-trip → validated `Address`) and `reach_i` (raw `shift` → bare `Tumbler` for the I-interval compare) differ on the *same* element-level i_start, to forestall a builder "simplifying" `run_addr` to a raw shift (which yields a `Tumbler`, not the `Address` the delivery/dedup path needs).

3. **[SHARPENING]** COMPARE `canonicalize`: `corr_key` clones four `Tumbler`s per call and `sort_by` invokes it twice per comparison (O(n log n) clones). Use `sort_by_cached_key` to compute each key once.

4. **[SHARPENING]** `doc_vspan`: add a one-liner that `from_endpoints(min, reach).unwrap()` is infallible because `#min == #reach == 2` and `min < reach` always hold, and that the bounding-box width round-trips exactly (divergence = 1 ≤ `#min` discharges D1) even in the cross-subspace case — making the synthesis self-evidently faithful to ASN-0112 σ_d.

5. **[SHARPENING]** `s_c()`/`s_l()` allocate a fresh `BigUint` on every call inside per-position loops (`retrieve_v`, `arranged_content`); hoist out of the loop or memoize via `once_cell::Lazy<Nat>`.

VERDICT: CONVERGED
