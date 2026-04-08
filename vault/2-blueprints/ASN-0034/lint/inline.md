# Inline Lint — ASN-0034

*Last scanned: 2026-04-07 19:53*

## D0

- **definition** | DEF-DISPLACEMENT | DisplacementFromAToB | names w = b ⊖ a as the displacement from a to b
- **commentary** | — | — | derivation of the displacement formula from TumblerAdd and TumblerSub, motivating D0

## GlobalUniqueness

- **definition** | ZEROS-COUNT | ZeroCount | zeros(t) function — count of zero-valued field-separator components determining hierarchical level
- **commentary** | — | — | closing paragraph on GlobalUniqueness as foundation for link stability, transclusion identity, and royalty tracing

## OrdinalDisplacement

- **definition** | OrdinalDisplacementNotation | OrdinalDisplacementShorthand | Shorthand δₙ for ordinal displacement when depth is determined by context

## OrdinalShift

- **derived** | OrdShiftDepth | OrdinalShiftDepthPreservation | shift preserves tumbler depth: #shift(v, n) = #v
- **derived** | OrdShiftStability | OrdinalShiftFirstComponent | when m ≥ 2, shift leaves the first component unchanged: shift(v, n)₁ = v₁
- **derived** | OrdShiftPositivity | OrdinalShiftPositivity | shift preserves component positivity: shift(v, n)ₘ ≥ 1 for all vₘ ≥ 0, n ≥ 1
- **derived** | SHIFT-DEPTH | OrdinalShiftDepth | shift preserves tumbler depth: #shift(v, n) = #v
- **derived** | OrdinalShiftHeadInvariance | OrdinalShiftHeadInvariance | when m ≥ 2, shift leaves the first component unchanged: shift(v, n)₁ = v₁
- **derived** | OrdinalShiftDepth | ShiftDepthPreservation | shift preserves tumbler depth: #shift(v, n) = #v
- **derived** | OrdinalShiftHead | ShiftHeadPreservation | when m ≥ 2, shift leaves the first component unchanged: shift(v, n)₁ = v₁
- **derived** | OrdinalShiftPositivity | ShiftComponentPositivity | shift preserves component positivity: shift(v, n)ₘ = vₘ + n ≥ 1 for all vₘ ≥ 0

## PartitionMonotonicity

- **derived** | SIBLING-PREFIX-NON-NESTING | SiblingPrefixNonNesting | sibling sub-partition prefixes produced by inc(·,0) are equal-length, distinct, and mutually non-nesting
- **derived** | SiblingPrefixesNonNesting | SiblingPrefixesNonNesting | Proves that sibling sub-partition prefixes produced by inc(·,0) are pairwise non-nesting (uniform length, distinct, and neither extends the other)
- **derived** | PREFIX-ORDERING-EXTENSION | PrefixOrderingExtension | For non-nesting prefixes p₁ < p₂, every address extending p₁ precedes every address extending p₂ under T1

## PositiveTumbler

- **commentary** | — | — | zero tumblers form an infinite chain under T1; no single zero tumbler exists
- **definition** | ZERO-TUMBLER | ZeroTumbler | tumbler whose every component is zero
- **derived** | POSITIVE-ABOVE-ZERO | PositiveAboveZero | every positive tumbler is greater than every zero tumbler under T1
- **derived** | — | PositiveDominatesZero | every positive tumbler exceeds every zero tumbler under T1
- **derived** | POS-GT-ZERO | PositiveDominatesZero | every positive tumbler is greater than every zero tumbler under T1

## T0b

- **derived** | T0a | UnboundedComponentValues | For every tumbler and position, a tumbler exceeding any given bound at that position exists
- **commentary** | — | — | Design rationale linking T0(a) and T0(b) to Nelson's "continually" and the two-dimensional unboundedness claim

## T10a

- **derived** | T10b | UniformSiblingLength | Siblings from the same allocator all have the same length as their base address
- **derived** | T10c | NonNestingSiblingPrefixes | Distinct siblings from the same allocator are prefix-incomparable
- **derived** | T10d | LengthSeparation | Child allocator outputs have strictly greater length than any parent sibling output
- **commentary** | — | — | Necessity argument showing that relaxing k=0 for siblings permits nesting, collapsing T10 partition guarantees
- **derived** | T10a-N | AllocatorDisciplineNecessity | relaxing the k=0 restriction for siblings permits prefix nesting, violating the T10 precondition
- **derived** | T10a-C3 | ParentChildLengthSeparation | child outputs have strictly greater length than parent sibling outputs, additively across nesting levels
- **derived** | T10a.1 | UniformSiblingLength | All siblings produced by a single allocator have the same length as its base address
- **derived** | T10a.2 | NonNestingSiblingPrefixes | Distinct siblings from the same allocator are prefix-incomparable
- **derived** | T10a.3 | LengthSeparation | Child allocator outputs are strictly longer than all parent sibling outputs, with additive separation across nesting levels

## T12

- **definition** | D-SPAN | SpanPair | A span is a pair (s, ℓ) with start address and length, denoting a contiguous range from s up to but not including s ⊕ ℓ
- **commentary** | — | — | Nelson 1-position convention and self-describing spans at every hierarchical level
- **definition** | D-Span | Span | a pair (s, ℓ) denoting the contiguous range from s up to but not including s ⊕ ℓ

## T4

- **derived** | T4a | SyntacticEquivalence | non-empty field constraint is equivalent to no adjacent zeros, t₁ ≠ 0, and t_{#t} ≠ 0
- **derived** | T4b | UniqueParse | fields(t) is well-defined and uniquely determined under T4 constraints
- **derived** | T4c | LevelDetermination | zeros(t) bijectively determines hierarchical level on {0,1,2,3}
- **definition** | — | FieldSeparator | zero-valued tumbler component used as structural delimiter between fields
- **definition** | — | ZerosCount | function zeros(t) = #{i : tᵢ = 0} counting zero-valued components in a tumbler
- **definition** | — | FieldsExtraction | function fields(t) decomposing a tumbler into node, user, document, and element fields
- **commentary** | — | — | hierarchy is convention layered over flat arithmetic; algebra has no isparent/isancestor primitives
- **definition** | D-FieldExtraction | FieldExtraction | function fields(t) decomposing a tumbler into node, user, document, and element sub-sequences
- **definition** | D-ZeroCount | ZeroCount | function zeros(t) counting zero-valued components in a tumbler
- **definition** | — | ZerosFunction | zeros(t) = count of zero-valued components in tumbler t
- **definition** | — | FieldsFunction | fields(t) = decomposition of t into node, user, document, element sub-sequences
- **definition** | D-FieldSeparator | FieldSeparator | A zero-valued tumbler component acting as a structural delimiter between fields

## T6

- **definition** | D-FieldExtraction | FieldExtraction | fields(t) decomposition and field accessor notation N(t), U(t), D(t), E(t)
- **definition** | D-ZeroCount | ZeroCount | zeros(t) field-separator count function determining hierarchical level
- **commentary** | — | — | componentwise comparison procedure for finite sequences of natural numbers
- **definition** | D-FieldDecomposition | FieldDecomposition | The fields(t) function decomposing a tumbler into named components N(t), U(t), D(t), E(t)

## T7

- **commentary** | — | — | rationale for stating T7 explicitly; subspace identifier is address, not metadata
- **derived** | T7a | TextPrecedesLinksInOrder | text addresses (subspace 1) precede link addresses (subspace 2) under T1 lexicographic ordering

## T8

- **definition** | D-GhostElement | GhostElement | A tumbler position that is permanently allocated but has no stored content
- **commentary** | — | — | Nelson quote affirming permanent address specification

## T9

- **derived** | T9c | GrowingAllocatedSet | Consequence of T8+T9: the allocated address set is lattice-theoretically monotone-growing, new elements always at each allocator's frontier
- **commentary** | — | — | Global non-monotonicity of the tumbler line due to depth-first child insertion (2.1.1 between 2.1 and 2.2)
- **derived** | T9a | GrowingAllocationSet | T8 + T9 together imply the allocated-address set is lattice-theoretically growing: it only increases, with new elements always at each allocator's frontier

## TA-LC

- **derived** | TA1 | AddWeakMonotonicity | Weak monotonicity of ⊕: if a < b then a ⊕ w ≤ b ⊕ w
- **derived** | TA1-strict | AddStrictMonotonicity | Strict monotonicity of ⊕ when k ≥ divergence(a, b)
- **derived** | TA3 | SubtractWeakMonotonicity | Weak monotonicity of ⊖: if a < b and both ≥ w then a ⊖ w ≤ b ⊖ w
- **derived** | TA3-strict | SubtractStrictMonotonicity | Strict monotonicity of ⊖ under equal-length precondition
- **derived** | TA4 | AddSubtractRoundTrip | Round-trip identity: (a ⊕ w) ⊖ w = a under zero-prefix precondition
- **commentary** | — | — | Worked example illustrating TA-LC with a = [2, 5]
- **derived** | TA1S | TumblerAddStrictMonotone | If additionally k ≥ divergence(a,b), then a ⊕ w < b ⊕ w
- **derived** | TA3S | TumblerSubStrictMonotone | If additionally #a = #b, then a ⊖ w < b ⊖ w

## TA-RC

- **derived** | TA-RC-GEN | TailErasureCorollary | any two starts agreeing on positions 1..k produce the same result under any displacement with action point k

## TA-assoc

- **commentary** | — | — | opening frame: what the tumbler algebra does not guarantee (no group, no identity, no general inverse)
- **derived** | TA-noncomm | AdditionNonCommutative | addition is not commutative; operands play asymmetric roles (position vs. displacement)
- **derived** | TA-apmin | ActionPointComposition | action point of b ⊕ c equals min(k_b, k_c), proved as internal lemma and surfaced in postconditions

## TA0

- **definition** | DA0 | ActionPoint | The first nonzero component index of a tumbler displacement, defined as k = min({i : wᵢ ≠ 0})
- **commentary** | — | — | Introductory motivation for tumbler addition and displacement semantics
- **definition** | DA-TumblerAdd | TumblerAdd | Constructive three-rule definition of a ⊕ w: prefix copy, action-point advance, tail copy
- **definition** | DEF-ActionPoint | ActionPoint | The action point of a displacement w is the index of its first nonzero component

## TA2

- **definition** | — | TumblerSubtraction | introduces ⊖ notation for tumbler subtraction (displacement between positions)
- **definition** | DEF-TA2-SUB | TumblerSubtraction | introduces ⊖ (tumbler subtraction) notation and its informal meaning

## TA3

- **definition** | TD-ZPE | ZeroPaddedEqual | Named relation "x is zero-padded-equal to w" introduced inline when zero-padded sequences agree at every position
- **commentary** | — | — | Self-contained recap of TumblerSub subtraction algorithm included for proof readability
- **definition** | DEF-ZeroPaddedEquality | ZeroPaddedEquality | two tumblers are zero-padded-equal if their zero-padded sequences agree at every position

## TA5

- **definition** | DA-SIG | LastSignificantPosition | defines sig(t) as the index of the last nonzero component of a tumbler
- **derived** | TA5a | IncrementPreservesT4 | inc(t,k) preserves T4 iff k=0, or k=1 with zeros(t)≤3, or k=2 with zeros(t)≤2; fails for k≥3
- **commentary** | — | — | explains that inc(t,0) produces the next peer, not the immediate successor, and why this is harmless for allocation
- **derived** | TA5-SigValid | SigOnValidAddresses | sig(t) = #t for all valid addresses, following from T4's positive-component constraint
- **definition** | D-SigPos | LastSignificantPosition | defines sig(t) as the index of the last nonzero component of a tumbler

## TA7a

- **definition** | TD-S | SubspaceOrdinals | Named set S of ordinals with all-positive components, used as the domain for TA7a's closure claims
- **commentary** | — | — | Design rationale for ordinal-only formulation vs. 2-component [N, x] formulation
- **definition** | TA7-S | SubspaceOrdinalSet | Named set S of ordinals with all-positive components, the domain for element-local shift arithmetic
- **derived** | TA7b | SubspaceClosureSMembership | Stronger result: conditions under which ⊕ and ⊖ results remain in S (not merely T), with full case analysis by action point and divergence

## TumblerAdd

- **commentary** | — | — | worked examples illustrating action-point mechanics at leaf and mid-level
- **derived** | TA-RESULT-LENGTH | ResultLengthIdentity | #(a ⊕ w) = #w — result length equals displacement length, proved from the definition
- **derived** | TUMBLER-ADD-LENGTH | TumblerAddLength | #(a ⊕ w) = #w — result length equals displacement length, with derivation from k ≥ 1
- **derived** | TUMBLER-ADD-MANY-TO-ONE | TumblerAddManyToOne | distinct start positions with the same displacement yield the same result

## _order-structure-adjacency-and-interpolation

- **derived** | _zero-extension-is-immediate-successor | ZeroExtensionIsImmediateSuccessor | every tumbler has an immediate successor, namely its zero-extension
- **commentary** | — | — | Nelson's "finite but unlimited" docuverse as design rationale for inexhaustibility


*51 files scanned. 24 with embedded results.*
