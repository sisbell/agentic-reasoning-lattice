# Cone Review — ASN-0034/T9 (cycle 7)

*2026-04-16 06:54*

I've read the entire ASN as an integrated system, cross-checking definitions, dependency chains, quantifier scopes, and case exhaustiveness across all properties. The proofs are logically sound — T1's transitivity handles all sub-cases correctly, T10a Consequence 5's inductive propagation is watertight, and T9's induction on the gap closes cleanly.

Previous findings #2–#7 and #9–#12 have all been resolved in the current text. Findings #1 and #8 remain but are not re-reported here.

After exhaustive analysis, one new finding:

### T4 is load-bearing throughout T10a but absent from its entire formal dependency structure

**Foundation**: (internal — foundation ASN)
**ASN**: T10a (AllocatorDiscipline), axiom: "The root allocator's base address satisfies T4"; postcondition T10a.4: "every output of a conforming allocator satisfies T4 by induction on the allocator tree"; postcondition T10a.5 (via TA5-SigValid): "For every valid address satisfying T4, sig(t) = #t"
**Issue**: T4 (HierarchicalParsing) is the central invariant of the entire allocator discipline — the axiom requires the root to satisfy it, T10a.4 proves the discipline preserves it, and T10a.5's divergence-propagation argument requires it (through TA5-SigValid, to establish `sig(b_A) = #b_A` so that `inc(·, 0)` modifies only the last position). Yet T4 appears in no formal Depends clause of T10a or any of its six postconditions. T10a's axiom has no Depends clause at all (unlike every other property in the document — T1, T8, TA5, and T9 each declare Depends covering the symbols in their primary statements). The postconditions reach T4 only through prose descriptions embedded in other dependencies: T10a.4 depends on "TA5a" with a parenthetical mentioning T4, and T10a.5 depends on "TA5-SigValid (sig = length)" without noting that TA5-SigValid's precondition is T4 satisfaction. A formal dependency analysis following only Depends links would never encounter T4 as a dependency of T10a — yet a change to T4's definition would change the meaning of the axiom, invalidate T10a.4's induction base, and potentially break TA5-SigValid's applicability in T10a.5. Compare with TA5, which both cites `sig(t) (TA5-SIG)` inline in its definition AND lists `TA5-SIG` in its formal Depends; T10a uses `T4` in its axiom but follows neither convention.
**What needs resolving**: Either a top-level Depends clause for T10a's axiom (covering at minimum T4, TA5, and TA5a — the three external properties the axiom directly references), or T4 added as an explicit dependency in the postconditions that use it (T10a.4 and T10a.5, at minimum). The dependency exists semantically throughout the property; it needs to exist formally in the contract.
