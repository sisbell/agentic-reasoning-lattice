## Properties Introduced

| Label | Name | Statement | Status |
|-------|------|-----------|--------|
| T0(a) | UnboundedComponentValues | Every component value of a tumbler is unbounded — no maximum value exists | introduced |
| T0(b) | UnboundedLength | Tumblers of arbitrary length exist in T — the hierarchy has unlimited nesting depth | introduced |
| T1 | LexicographicOrder | Tumblers are totally ordered by lexicographic comparison, with the prefix-less-than convention | introduced |
| T2 | IntrinsicComparison | Tumbler comparison is computable from the two addresses alone, examining at most min(#a, #b) components | introduced |
| T3 | CanonicalRepresentation | Each tumbler has exactly one canonical representation; component-wise identity is both necessary and sufficient for equality | introduced |
| T4 | HierarchicalParsing | An address tumbler has at most three zero-valued components as field separators, every field component is strictly positive, and every present field has at least one component (no adjacent zeros, no leading/trailing zero) | introduced |
| T5 | ContiguousSubtrees | The set of tumblers sharing a prefix forms a contiguous interval under T1 | introduced |
| T6 | DecidableContainment | Containment (same node, same account, same document family, structural subordination) is decidable from addresses alone | corollary of T4 |
| T7 | SubspaceDisjointness | Subspaces (text, links) within a document's element field are permanently disjoint | corollary of T3, T4 |
| T8 | AllocationPermanence | Once allocated, an address is never removed from the address space; the set of allocated addresses is monotonically non-decreasing | introduced |
| T9 | ForwardAllocation | Within a single allocator's sequential stream, new addresses are strictly monotonically increasing; gaps are permanent | lemma (from T10a, TA5) |
| T10 | PartitionIndependence | Allocators with non-nesting prefixes produce distinct addresses without coordination | introduced |
| T10a | AllocatorDiscipline | Each allocator uses inc(·, 0) for siblings and inc(·, k>0) only for child-spawning; this constrains sibling outputs to uniform length | introduced |
| PrefixOrderingExtension | PrefixOrderingExtension | p₁ < p₂ with neither a prefix of the other implies a < b for every a with p₁ ≼ a and every b with p₂ ≼ b | lemma (from T1) |
| PartitionMonotonicity | PartitionMonotonicity | Per-allocator ordering extends cross-allocator; for non-nesting sibling prefixes p₁ < p₂, every address extending p₁ precedes every address extending p₂ | theorem from PrefixOrderingExtension, T1, T3, T5, T9, T10a, TA5 |
| GlobalUniqueness | GlobalUniqueness | No two distinct allocation events anywhere in the system at any time produce the same address | theorem from T3, T4, T9, T10, T10a, TA5 |
| T12 | SpanWellDefinedness | A span (s, ℓ) is well-formed when ℓ > 0 and action point k of ℓ satisfies k ≤ #s; it denotes the contiguous interval {t : s ≤ t < s ⊕ ℓ}, non-empty by TA-strict | from T1, TA0, TA-strict |
| TA0 | WellDefinedAddition | Tumbler addition a ⊕ w is well-defined when w > 0 and the action point k satisfies k ≤ #a | introduced |
| TA1 | OrderPreservationUnderAddition | Addition preserves the total order (weak): a < b ⟹ a ⊕ w ≤ b ⊕ w | introduced |
| Divergence | Divergence | Divergence point of two unequal tumblers: first position k where aₖ ≠ bₖ (component), or min(#a, #b) + 1 (prefix) | from T1 |
| TA1-strict | StrictOrderPreservation | Addition preserves the total order (strict) when k ≤ min(#a, #b) ∧ k ≥ divergence(a, b) | from Divergence, TumblerAdd |
| TA-strict | StrictIncrease | Adding a positive displacement strictly advances: a ⊕ w > a | from TumblerAdd, T1 |
| TA2 | WellDefinedSubtraction | Tumbler subtraction a ⊖ w is well-defined when a ≥ w | from TumblerSub, T1 |
| TA3 | OrderPreservationUnderSubtractionWeak | Subtraction preserves the total order (weak): a < b ⟹ a ⊖ w ≤ b ⊖ w when both are defined | from TA2, T1, TA6, TumblerSub |
| TA3-strict | OrderPreservationUnderSubtractionStrict | Subtraction preserves the total order (strict) when additionally #a = #b | introduced |
| TA4 | PartialInverse | Addition and subtraction are partial inverses: (a ⊕ w) ⊖ w = a when k = #a, #w = k, and all components of a before k are zero | from TumblerAdd, TumblerSub |
| ReverseInverse | ReverseInverse | (a ⊖ w) ⊕ w = a when k = #a, #w = k, a ≥ w > 0, and all components of a before k are zero | corollary of TA3-strict, TA4, TumblerAdd, TumblerSub |
| TumblerAdd | TumblerAdd | a ⊕ w: copy aᵢ for i < k, advance aₖ by wₖ at action point k, replace tail with wᵢ for i > k; result length = #w | introduced |
| TumblerSub | TumblerSub | a ⊖ w: zero positions before divergence k, compute aₖ − wₖ at divergence point, copy aᵢ for i > k; result length = max(#a, #w) | from Divergence, T1 |
| TA5 | HierarchicalIncrement | Hierarchical increment inc(t, k) produces t' > t: k=0 advances at sig(t), k>0 extends by k positions with separators and first child | introduced |
| TA6 | ZeroTumblers | Every all-zero tumbler (any length) is less than every positive tumbler and is not a valid address | from T1, T4 |
| PositiveTumbler | PositiveTumbler | t > 0 iff at least one component is nonzero; zero tumbler iff all components are zero | introduced |
| TA7a | SubspaceClosure | Ordinal-only shift arithmetic: both ⊕ and ⊖ on ordinals produce results in T with the subspace identifier (held as context) unchanged | introduced |
| TA-assoc | AdditionAssociative | Addition is associative where both compositions are defined: (a ⊕ b) ⊕ c = a ⊕ (b ⊕ c) | theorem from TumblerAdd, T3 |
| TA-LC | LeftCancellation | a ⊕ x = a ⊕ y ⟹ x = y (left cancellation) | lemma (from TumblerAdd, T3) |
| TA-RC | RightCancellationFailure | Right cancellation fails: ∃ a ≠ b with a ⊕ w = b ⊕ w | lemma (from TumblerAdd, T3) |
| TA-MTO | ManyToOne | a agrees with b on components 1..k ⟺ a ⊕ w = b ⊕ w for displacement w with action point k | lemma (from TumblerAdd, T3) |
| D0 | DisplacementWellDefined | Displacement well-definedness: a < b and divergence(a, b) ≤ #a ensures positive displacement with TA0 satisfied | from T3, TA0, TumblerAdd, TumblerSub |
| D1 | DisplacementRoundTrip | Displacement round-trip: for a < b with divergence(a, b) ≤ #a and #a ≤ #b, a ⊕ (b ⊖ a) = b | lemma (from TumblerAdd, TumblerSub, T3, Divergence) |
| D2 | DisplacementUnique | Displacement uniqueness: under D1's preconditions, if a ⊕ w = b then w = b ⊖ a | corollary of D1, TA-LC |
| OrdinalDisplacement | OrdinalDisplacement | δ(n, m) = [0, ..., 0, n] of length m, action point m | introduced |
| OrdinalShift | OrdinalShift | shift(v, n) = v ⊕ δ(n, #v) | introduced |
| TS1 | ShiftOrderPreservation | shift preserves strict order: v₁ < v₂ ⟹ shift(v₁, n) < shift(v₂, n) | lemma (from TA1-strict) |
| TS2 | ShiftInjectivity | shift is injective: shift(v₁, n) = shift(v₂, n) ⟹ v₁ = v₂ | lemma (from TA-MTO, T3) |
| TS3 | ShiftComposition | shift composes additively: shift(shift(v, n₁), n₂) = shift(v, n₁ + n₂) | lemma (from TumblerAdd, T3) |
| TS4 | ShiftStrictIncrease | shift strictly increases: shift(v, n) > v | corollary of TA-strict |
| TS5 | ShiftAmountMonotonicity | shift is monotone in amount: n₁ < n₂ ⟹ shift(v, n₁) < shift(v, n₂) | corollary of TS3, TS4 |
