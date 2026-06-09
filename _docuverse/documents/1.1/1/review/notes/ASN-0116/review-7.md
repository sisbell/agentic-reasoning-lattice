# Review of ASN-0116

I verified the load-bearing arguments and could not find a REVISE-level defect. Summary of what I checked:

**Core arithmetic.** `shift(q_k, n) = q_{k+n}` is correct (OrdinalShift at action point `m = #q_k`), and `inc(a,0) = shift(a,1)` for the T4-valid I-addresses of `A_C(d)` (TA5-SigValid) — so `A_new = {shift(a,k)}` is exactly the next `n` elements of the content sub-allocator chain.

**Composition discipline.** The ASN correctly distinguishes ASN-0082's *gapped* `M'(d)` from INSERT's *filled* `M'(d)`, and — crucially — notices that I3-S3 and I3-S7 are proved under the content frame I3-C (`dom(C')=dom(C)`) which INSERT deliberately breaks via I-ALLOC. It discharges referential integrity and the content-store invariants (S7a/S7b/C1b/C1c/C2) directly at the K.α source plus P2 monotonicity, rather than borrowing inapplicable lemmas. This is the single most likely place to hand-wave, and it does not.

**Per-block-position attribution.** The I-NEW absence argument splits by index (`≤ N` via I3-V, `> N` via I3-CS) rather than by a single case on `J`, and the mixed-split case (`n ≥ 2` seated in the last `n−1` slots) is handled. I confirmed `q_{J+k}` for index `> N` is neither `< p` nor a shifted image (`u = q_{J+k-n} < p`), so I3-CS legitimately discharges it.

**Contiguity.** The interval argument (`{1..J−1} ⊎ {J..J+n−1} ⊎ {J+n..N+n} = {1..N+n}`) is consecutive, disjoint, gap-free, establishing D-SEQ/D-MIN/D-CTG of the *filled* post-state — correctly noting the D-family post-lemmas are contraction results and inapplicable. Single-valuedness of the union follows from the same disjointness.

**Link survival (P4).** The "bijection-not-inclusion" form is correct: prior witnesses partition into left/suffix/cross-subspace, map injectively (suffix relabelled by `v↦shift(v,n)`, TS2), images disjoint, so count is non-decreasing. I verified coverage-invariance rests on L12+LP3 (endset immutability), *not* on `A_new` freshness — and the ASN explicitly flags the L4/L9 ghost-reference case that would break a freshness-based argument.

**wp (P6).** `ran(M'(d)) = ran(M(d)) ∪ A_new` checked; via LP12 the wp is a *containment* (`Added ⊆ D(d,Σ)`), not an emptiness, and I verified `D(d,Σ')=D(d,Σ) ⟺ Added ⊆ D(d,Σ)` with the emptiness form correctly identified as sufficient-but-strictly-stronger. The "resolved content equality iff `coverage(e)∩A_new = ∅`" reduction is exact (using `A_new ∩ ran(M(d)) = ∅`).

**Worked example.** Exercises shift+resurrect, the P6 trap (ghost-plus-live-span: `ℓ ∈ Added ∖` nothing, already discoverable), a genuine orphan resurrection (LP18), isolation, and the append/empty boundaries. Concrete and consistent.

**Foundation usage.** Uses ValidInsertionPosition/ValidFirstInsertionPosition, K.α, I3 family, L12/LP3/LP12/LP18/LP19a, S3★, S4 — all foundation, no reinvented notation, no improper cross-references. The `S = s_C` precondition is correctly load-bearing (K.α yields only `s_C` addresses; an `s_L` seat would violate S3★).

The deferred topics (transclusion sharing the insertion point, concurrent-insertion freshness, provenance atomicity, post-edit fragmentation) are appropriately posed as open questions, not claims, so there is nothing to flag as OUT_OF_SCOPE.

No META: the ASN specifies state, an operation, frame, and preserved invariants abstractly; Gregory's evidence motivates but does not constitute the spec.

VERDICT: CONVERGED
