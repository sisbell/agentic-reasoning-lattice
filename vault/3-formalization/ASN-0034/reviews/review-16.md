# Proof Review — ASN-0034 (cycle 2)

*2026-04-08 23:14*

22 properties (D0, D1, D2, OrdinalShift, PartitionMonotonicity, PositiveTumbler, ReverseInverse, T0(b), T8, TA-LC, TA-MTO, TA-RC, TA-assoc, TA-strict, TA0, TA1, TA1-strict, TA4, TA7a, TS3, TS5, TumblerAdd)

### TumblerAdd

RESULT: FOUND

**Problem**: The proof claims "Since `w > 0`, at least one component is nonzero, so `k` exists and is well-defined," but no dependency establishes what `> 0` means on `T` or that it implies a nonzero component exists. The only dependency is T0 (carrier set), which defines `T` as finite sequences over `ℕ` but says nothing about ordering.

Under the standard tumbler ordering (lexicographic with shorter-is-less for prefixes), the claim is **false**: `w = [0, 0]` satisfies `w > [0] = 0` because `[0]` is a proper prefix of `[0, 0]`, yet every component of `w` is zero, so `k = min{i : wᵢ ≠ 0}` does not exist and the definition is ill-defined for this input.

**Required**: Add the tumbler ordering definition as a dependency, and either (a) show that under that ordering `w > 0` implies `∃i: wᵢ ≠ 0`, or (b) strengthen the precondition to explicitly require at least one nonzero component (e.g., `∃i: wᵢ ≠ 0`) rather than relying on `w > 0` alone.

21 verified, 1 found.
