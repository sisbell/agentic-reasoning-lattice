# Proof Review — ASN-0034 (cycle 3)

*2026-04-08 18:11*

19 properties (GlobalUniqueness, OrdinalShift, PartitionMonotonicity, T10a, T10a.1, T10a.2, T10a.3, T8, T9, TA-LC, TA3, TA3-strict, TA6, TA7a, TS1, TS2, TS3, TS4, TS5)

### T10a

## Verification of T10a (AllocatorDiscipline)

**Consequences T10a.1–T10a.3** are logically sound, assuming the cited properties at face value:

- **T10a.1**: Follows directly — repeated `inc(·, 0)` preserves length by TA5(c), so all siblings share the base length. ✓
- **T10a.2**: Follows from T10a.1 + Prefix — equal-length distinct tumblers are prefix-incomparable. ✓
- **T10a.3**: Follows by induction — each `inc(·, k')` with `k' > 0` adds `k'` to length by TA5(d); sibling production preserves length by T10a.1. ✓

**T10a-N (Necessity)** has a gap:

The proof argues: relaxing the `k = 0` restriction allows siblings of different lengths (via TA5(d)), therefore prefix nesting is "permitted." But different lengths are *necessary* for prefix nesting, not *sufficient*. Tumblers of different lengths can still be prefix-incomparable — e.g., `(1, 2, 3)` and `(1, 2, 4, 5)` differ in length yet neither prefixes the other.

To close the existential claim ("admits a pair of siblings where one is a prefix of the other"), the proof needs either:

1. A structural property of `inc` establishing that the input is a prefix of `inc(input, k)` when `k > 0` (i.e., `t ≺ inc(t, k)` for `k > 0`), which would make any equal-length sibling a prefix of the deeper sibling, **or**
2. A concrete counterexample with specific tumbler values showing prefix nesting under the relaxed rule.

The proof cites only the length postconditions TA5(c) and TA5(d). The jump from "the uniform-length defense is removed" to "prefix nesting is admitted" relies on an unstated structural guarantee about how `inc(·, k)` for `k > 0` relates to its input.

```
RESULT: FOUND

**Problem**: T10a-N (Necessity) asserts that relaxing the k = 0 restriction
"admits a pair of siblings where one is a prefix of the other," but the argument
only establishes that siblings would have non-uniform lengths. Different lengths
are necessary but not sufficient for prefix nesting. The proof cites only TA5(c)
and TA5(d) (length postconditions) and never establishes that inc(t, k) for k > 0
produces an output of which t is a prefix — the structural property needed to
construct the claimed prefix-nested pair.

**Required**: Either (a) cite or establish a property that t ≺ inc(t, k) for k > 0
(input is a prefix of output when depth is added), which immediately yields the
counterexample: s₁ = inc(b, 0) and s₂ = inc(s₁, k) give s₁ ≺ s₂; or
(b) construct an explicit counterexample with concrete tumbler values
demonstrating that the relaxed discipline produces prefix-nested siblings.
```

18 verified, 1 found.
