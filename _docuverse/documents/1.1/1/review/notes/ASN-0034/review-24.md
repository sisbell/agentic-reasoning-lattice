# Review of ASN-0034

## REVISE

### Issue 1: TA3 proof — missing case for zero-padded-equal operands

**ASN-0034, Verification of TA3, "For the remaining cases..."**: "Let dₐ = divergence(a, w) and d_b = divergence(b, w) (under zero-padding)."

**Problem**: Cases 1–3 assume `dₐ = divergence(a, w)` is well-defined, but Divergence is only defined for unequal tumblers (`a ≠ b`). When `a` and `w` are zero-padded-equal — no divergence exists — and `a < b` by component divergence (T1 case (i)), the proof breaks: `dₐ` is undefined, and none of Cases 1–3 apply. Case 0 handles only prefix-related `(a, b)` pairs, so this configuration falls through. Concrete example: `a = [1, 3]`, `w = [1, 3]`, `b = [1, 5]`. Here `a < b` by component divergence at position 2, `a = w` (zero-padded-equal), and `a ≥ w`. The result holds (`a ⊖ w = [0, 0]`, `b ⊖ w = [0, 2]`, and `[0, 0] < [0, 2]`), but the proof text never shows it.

**Required**: Add a case between Case 0 and Cases 1–3 for when `a < b` by component divergence and `a` is zero-padded-equal to `w`: "`a ⊖ w` is the zero tumbler. Since `aⱼ = wⱼ` at the divergence `j` of `a` and `b`, and `bⱼ > aⱼ = wⱼ`, the pair `(b, w)` diverges at or before `j`, making `b ⊖ w` positive. By TA6, `a ⊖ w < b ⊖ w`."

### Issue 2: Circular dependency — TumblerAdd ⟷ TA4

**ASN-0034, dependency graph**: TumblerAdd `follows_from: [TA4]`

**Problem**: TumblerAdd is a constructive definition introduced before TA4. TA4 is a property verified using TumblerAdd. The dependency is reversed. Cycle: TumblerAdd → TA4 → TumblerAdd.

**Required**: Remove TA4 from TumblerAdd's `follows_from`. TumblerAdd is `introduced` with no dependencies.

### Issue 3: Circular dependency — Divergence ⟷ TA1-strict

**ASN-0034, dependency graph**: Divergence `follows_from: [T1, TA0, TA1, TA1-strict]`

**Problem**: Divergence is a pure definition ("the first position where two tumblers differ"). It depends only on T1 (which ensures exactly one case applies). TA0, TA1, and TA1-strict are properties of arithmetic that appear later and *use* Divergence — they are downstream, not upstream. Cycle: Divergence → TA1-strict → Divergence.

**Required**: Replace Divergence's `follows_from` with `[T1]`.

### Issue 4: Circular dependency — TA-strict ⟷ T12

**ASN-0034, dependency graph**: TA-strict `follows_from: [T1, T12, TA0, TA1, TA4, TumblerAdd]`

**Problem**: TA-strict's derivation uses only TumblerAdd and T1: "By the constructive definition, `(a ⊕ w)ₖ = aₖ + wₖ`. Since `wₖ > 0`, `aₖ + wₖ > aₖ`. By T1 case (i), `a ⊕ w > a`." T12 depends on TA-strict for non-emptiness, creating cycle TA-strict → T12 → TA-strict. TA0, TA1, TA4 are also unused. The property table correctly states "from TumblerAdd, T1."

**Required**: Replace TA-strict's `follows_from` with `[T1, TumblerAdd]`.

### Issue 5: Circular dependency — D0 ⟷ D1

**ASN-0034, dependency graph**: D0 `follows_from: [D1, T3, TA0, TumblerAdd, TumblerSub]`

**Problem**: D0 is stated before D1. D1's proof begins "By hypothesis `k ≤ #a ≤ #b` (D0)..." — D1 depends on D0, not vice versa.

**Required**: Remove D1 from D0's `follows_from`.

### Issue 6: Spurious dependencies — TumblerSub

**ASN-0034, dependency graph**: TumblerSub `follows_from: [Divergence, T1, TA1, TA1-strict, TA3]`

**Problem**: TumblerSub is a constructive definition using the Divergence concept and T1. TA1, TA1-strict, and TA3 are properties *verified using* TumblerSub — downstream consumers, not upstream dependencies. The property table correctly states "from Divergence, T1."

**Required**: Replace TumblerSub's `follows_from` with `[Divergence, T1]`.

### Issue 7: Spurious dependencies — TS5

**ASN-0034, dependency graph**: TS5 `follows_from: [T4, TA0, TS1, TS3, TS4, TumblerAdd]`

**Problem**: TS5's two-line derivation uses only TS3 and TS4: "By TS3: `shift(v, n₂) = shift(shift(v, n₁), n₂ − n₁)`. By TS4: `shift(shift(v, n₁), n₂ − n₁) > shift(v, n₁)`." T4, TA0, TS1, and TumblerAdd are not referenced. The property table correctly states "corollary of TS3, TS4."

**Required**: Replace TS5's `follows_from` with `[TS3, TS4]`.

### Issue 8: Spurious dependency — T12 on T5

**ASN-0034, dependency graph**: T12 `follows_from: [T1, T5, TA-strict, TA0]`

**Problem**: The ASN explicitly distinguishes T12 from T5: "Contiguity is definitional: the span is an interval `[s, s ⊕ ℓ)` in a totally ordered set... We reserve T5 for the distinct claim that *prefix-defined* sets are contiguous." T5 is not used in T12's derivation. The property table correctly states "from T1, TA0, TA-strict."

**Required**: Remove T5 from T12's `follows_from`.

### Issue 9: Spurious dependencies — additional corrections

**ASN-0034, dependency graph**: Multiple entries list labels not used in their derivations.

**Problem**:
- **T0(b)**: Spurious dependency on T0(a). The ASN says "T0(b) follows from T's definition as the set of all finite sequences over ℕ" — T0(a) is not used.
- **T7**: Spurious dependency on T1. T7 is "a corollary of T3 (canonical representation) and T4 (hierarchical parsing)." T1 is mentioned only as a downstream consequence ("The ordering T1 places all text addresses before all link addresses").
- **T9**: Spurious dependency on T10. T9 concerns a single allocator's sequential stream, derived from T10a and TA5. T10 (partition independence) is about cross-allocator behavior, unused in T9.
- **PositiveTumbler**: Spurious dependencies on T1, TA0, TA4. PositiveTumbler is a pure definition ("at least one nonzero component") with no dependencies.

**Required**: Remove the listed spurious labels from each entry's `follows_from`.

### Issue 10: TA1-strict name mismatch

**ASN-0034, dependency graph**: TA1-strict `name: strict (Strict order preservation)`

**Problem**: The property table names this "Addition preserves the total order (strict) when `k ≤ min(#a, #b) ∧ k ≥ divergence(a, b)`." The dep graph name "strict (Strict order preservation)" is a scanning artifact.

**Required**: Update to `name: Addition preserves the total order (strict)`.

## OUT_OF_SCOPE

### Topic 1: Span operations (containment, intersection, splitting)

**Why out of scope**: T12 establishes well-formedness and non-emptiness. Operations on spans — containment testing, intersection, splitting at a position — require their own ASN with preconditions, postconditions, and invariant-preservation arguments.

### Topic 2: Finite-model equivalence for bounded implementations

**Why out of scope**: The open question about whether a bounded implementation's representable range can be characterized as a finite-model property of the abstract algebra is metatheoretic — it concerns the relationship between the specification and implementations, not a property of the algebra itself.

VERDICT: REVISE
