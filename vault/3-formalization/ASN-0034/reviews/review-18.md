# Cross-cutting Review — ASN-0034 (cycle 1)

*2026-04-08 23:53*

I've read the entire ASN-0034 as a single system, tracing precondition chains, definition usage, and case analysis exhaustiveness across all 60+ properties. Here are my findings.

### T8 proof characterizes allocation incompletely, contradicting GlobalUniqueness Case 4
**Foundation**: T8 (AllocationPermanence), GlobalUniqueness
**ASN**: T8 proof, Case 3: "T10a constrains allocation to a single mechanism: each allocator advances its frontier by repeated application of `inc(·, 0)` (TA5), producing an address strictly greater than the previous, and inserts it into the allocated set."
**Issue**: T8's exhaustive case analysis claims allocation is "a single mechanism" — sibling production via `inc(·, 0)`. But child-spawning via `inc(·, k')` with `k' > 0` also produces addresses that enter the allocated set. GlobalUniqueness Case 4 confirms this, treating `c₀ = inc(t, k')` as an allocated address: "every child output — including `c₀` itself — have uniform length `γ + k'`." The two properties disagree on whether child-spawning is an allocation event. If `c₀` is allocated (as GlobalUniqueness requires for its uniqueness argument), then T8's Case 3 is incomplete — it only describes one of two allocation mechanisms. Both are insert-only, so the monotonicity conclusion still holds, but the claimed exhaustiveness of the three-case partition is unsound as written: child-spawning allocation events are classified as "pure arithmetic" (Case 2) by T8 while simultaneously being treated as allocation events by GlobalUniqueness.
**What needs resolving**: T8's Case 3 must explicitly cover both sibling allocation (`inc(·, 0)`) and child-spawning allocation (`inc(·, k')` with `k' > 0`), or the ASN must clarify whether `c₀` enters the allocated set at the moment of the parent's `inc(·, k')` or at some later child-level operation — and then GlobalUniqueness Case 4 must be consistent with that choice.
