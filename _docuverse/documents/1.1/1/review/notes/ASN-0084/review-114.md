# Review of ASN-0084

I checked each lemma proof (R-PIV, R-SWP, R-PPERM, R-SPERM, R-COMM, R-BLK, R-CANON, R-RI, R-NS), the bijection/finiteness arguments, the edge cases, and the anti-bloat patterns flagged for this note. The ASN is self-contained against the two foundations (ASN-0034, ASN-0036) and introduces no references to non-foundation ASNs.

## REVISE

None. Detailed verification notes:

- **Well-definedness (R-PIV/R-SWP).** Exhaustiveness and disjointness are shown by explicit half-open ordinal ranges `[p, p+w_β)`, `[p+w_β, p+w_β+w_α)`, etc., with `w_α, w_β, w_μ ≥ 1` discharged by Width-positivity. Union equals `[c₀, c_{n−1}) ∩ V_S(d)`; RHS references land in `dom(M(d))` via R-PRE(iv). Complete.
- **Bijectivity (R-PPERM/R-SPERM).** Image ⊆ `dom(M(d))`, per-case injectivity, cross-case image disjointness (subspace separation + R-PIV/R-SWP ranges), then finite self-injection ⇒ surjection via S8-fin. Sound.
- **R-CANON forward/backward extension.** The "same ordinal ⇒ same position" steps correctly rely on within-run prefix sharing (shift moves only the last component) plus T3, so they hold even for non-text subspaces at depth > 2 without needing D-CTG-depth (which is text-only). The merge-pair contradiction closes both directions; conclusion rests on S8 uniqueness of the maximal partition.
- **Cross-group disjointness (R-BLK).** `[1] ⋠ [2]`, `[2] ⋠ [1]` with `[1] ≼ [1,k]`, `[2] ≼ [2,k]` correctly invokes T10 (PartitionIndependence). Valid.
- **Edge cases all exercised:** empty `V_S(d)` excluded by R-PRE(ii); minimum `w_α=w_β=1` and empty exteriors (boundary example); equal/unequal/reversed widths (examples 2–4); fixed-μ and backward-μ sub-cases; non-S pass-through (link example). EXT-VAC's conclusion (`c_{n−1} ∉ dom(M(d))`, empty right exterior) holds under D-SEQ; R-PRE(iv) independently pins `c_{n−1}` to at most `[S, N+1]`, consistent with the trace.
- **Meta-prose check.** The worked-example wrap-up sentences (e.g., "exercises the non-S machinery …") are statements of what the example demonstrates, which the anti-bloat guidance explicitly excludes from meta-prose. The "Invariant preservation" enumeration is genuine audit work (each invariant discharged), not a use-site inventory. The Phase-1/Phase-3 non-S content is correctly partitioned (splitting fact in Phase 1, carry-through in Phase 3) — no cross-phase deferral remains.

## OUT_OF_SCOPE

### Topic 1: k-cut generalization (k > 4)
**Why out of scope**: The ASN deliberately fixes n ∈ {3,4} via CS1. Generalizing the permutation class is new territory, correctly listed in Open Questions.

### Topic 2: Composition of multiple rearrangements
**Why out of scope**: This ASN specifies a single REARRANGE_K operation. Closure of the operation class under composition is a separate result.

### Topic 3: Weakest precondition for the post-state invariant suite Q
**Why out of scope**: The ASN proves the full invariant suite is preserved (Invariant-preservation block + R-RI + post-state S8 discharge). A formal wp characterization for an abstract Q is a distinct analysis, appropriately deferred.

### Topic 4: Run-count growth bounds and cut-vs-run-boundary constraints
**Why out of scope**: R-BLK notes B′ may be non-maximal and R-CANON normalizes it; quantitative growth bounds are future work.

VERDICT: CONVERGED
