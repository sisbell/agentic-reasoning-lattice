# Cone Review — ASN-0034/TA5a (cycle 2)

*2026-04-17 18:43*

### T4c cited to interpret a T4-invalid witness in TA5a's `k ≥ 3` case
**Foundation**: T4c (LevelDetermination) — Postconditions explicitly restrict: "On tumblers `t ∈ T` that are not T4-valid — those with `zeros(t) ≥ 4` ... or with `zeros(t) ≤ 3` but violating the field-segment constraint (e.g., `[1, 0, 0, 2]` with adjacent zeros ...) — this corollary assigns no hierarchical level". T4c covers level *labels* by zero count, not field decomposition.
**ASN**: TA5a proof, Case `k ≥ 3`:
> "As a concrete witness: `inc([1], 3)` produces `[1, 0, 0, 1]`, where positions 2 and 3 are adjacent zeros, bounding an empty interior field segment (which parses — under T4c — as node `[1]`, separator, *empty user field*, separator, document `[1]`)."

And the Depends entry:
> "T4c (LevelDetermination) — invoked in the case `k ≥ 3` witness to interpret the resulting tumbler under the parsing rule ('which parses — under T4c — as node `[1]`, separator, *empty user field*, separator, document `[1]`'); T4c supplies the non-null-field rule whose violation is exhibited."

**Issue**: Two cross-cutting inconsistencies in a single citation.
(1) The witness `[1, 0, 0, 1]` has adjacent zeros and is therefore T4-invalid — exactly the boundary T4c's own Postcondition uses as its illustrative exclusion (`[1, 0, 0, 2]`). By T4c's contract, no level and no labels ("node", "user", "document") are assigned to T4-invalid tumblers, so appealing to T4c to read field names off `[1, 0, 0, 1]` contradicts T4c's own scope.
(2) The authority invoked is "the parsing rule" / "non-null-field rule", neither of which is T4c's content. T4c assigns a whole-tumbler *level label* by zero count; it does not decompose a tumbler into named field segments. Field decomposition (`fields(t) = (N(t), U(t), D(t), E(t))`) is T4b's content, and the segment non-emptiness reading is T4a's content — and both are likewise restricted to the T4-valid subdomain.

The effect is that TA5a's Depends list routes a load-bearing illustrative step (the "empty field" reading that makes the T4-violation visible) through a property that neither covers this kind of statement nor applies to this witness.

**What needs resolving**: TA5a must either (a) reformulate the `k ≥ 3` witness argument so that the T4 violation is exhibited purely via T4's positional clause "no two zeros adjacent" — without appealing to parsed field names, which would remove T4c from the citation — or (b) restructure the witness so that the "empty field" reading is sourced from properties whose scope actually includes this interpretation (T4a for segment non-emptiness, T4b for named field projections), while simultaneously reckoning with the fact that those properties too are restricted to T4-valid tumblers and therefore cannot be cited at `[1, 0, 0, 1]` directly.
