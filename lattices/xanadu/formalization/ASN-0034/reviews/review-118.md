# Cross-cutting Review — ASN-0034 (cycle 5)

*2026-04-17 02:50*

Scanning the ASN for cross-cutting issues beyond what Previous Findings have already captured.

### Inconsistent property aliases across Depends clauses

**Foundation**: (foundation ASN — internal consistency)
**ASN**: Numerous properties are referenced by different parenthetical aliases across the ASN's Depends clauses, with no single canonical alias in use:
- **T4** (title name: HierarchicalParsing): cited as *"T4 (HierarchicalParsing)"* in TA5, T10a, TA6; as *"T4 (AddressFormat)"* in T4a, T4b, T4c, T6, T7; as *"T4 (AddressTumbler)"* in TA5-SigValid and TA5a.
- **T4a** (title name: SyntacticEquivalence): cited as *"T4a (SyntacticEquivalence)"* in T4b, T4c, T6, T7; as *"T4a (FieldSegmentEquivalence)"* in TA5a.
- **T4c** (title name: LevelDetermination): cited as *"T4c (LevelDetermination)"* in T4a, T4b, T6; as *"T4c (NonNullField)"* in TA5a.
- **T0** (title name: CarrierSetDefinition): cited as *"T0 (CarrierSetDefinition)"* throughout most properties; as *"T0 (CarrierType)"* in TA5-SigValid, TA5a, T6.
- **TA5** (title name: HierarchicalIncrement): cited as *"TA5 (HierarchicalIncrement)"* in many sites; as *"TA5 (IncrementPostconditions)"* in GlobalUniqueness, T10a.5, T10a's formal contract; as *"TA5 (IncrementSpecification)"* in TA5a.
- **TA5-SIG** (title name: LastSignificantPosition): cited as *"TA5-SIG (LastSignificantPosition)"* in TA5; as *"TA5-SIG (SignatureFunction)"* in TA5a.
- **TA6** (title name: ZeroTumblers): cited as *"TA6 (ZeroTumblers)"* in TA3; as *"TA6 (ZeroSentinel)"* in TA7a.

**Issue**: Depends aliases serve as an anchor between a citing property and the cited property; when three different aliases refer to the same property, a reviser who renames or re-scopes the cited property has no mechanical way to locate every downstream citation. Some aliases (e.g., "T4c (NonNullField)") don't even match the cited property's stated postconditions — T4c's actual claim is the bijection between `zeros(t)` and hierarchical level, not a "non-null field" rule. Readers verifying precondition chains by grep on the parenthetical name will miss variant-aliased citations.
**What needs resolving**: The ASN must pick one canonical alias per property (typically the title name in bold) and normalize every Depends citation to use it, or it must explicitly document a "multiple aliases permitted" convention with a lookup table. As written, several citations point at aliases their target properties do not advertise, which is a silent integrity hazard for the cross-property audit that Depends is meant to support.

### Vocabulary entry for `zeros(t)` conflates formula with role-assignment

**Foundation**: (internal consistency)
**ASN**: The Vocabulary entry reads: *"zeros(t) — number of zero-valued field-separator components in tumbler t: #{i : tᵢ = 0}"*. But T4's formal definition says *"Define `zeros(t) = #{i : 1 ≤ i ≤ #t ∧ tᵢ = 0}`, the count of zero-valued components in `t`"* — no field-separator gloss — and TA5a repeats *"Let `zeros(t) = #{i : 1 ≤ i ≤ #t ∧ tᵢ = 0}` denote the count of zero-valued components of `t` (defined in T4)"*. TA5a's case analysis applies `zeros(t)` to arbitrary tumblers, including those that violate T4 (e.g., *"inc(t, k)` produces `t' = ...` where ... positions `#t + 1` and `#t + 2` are both zero"*). T10a likewise applies `zeros(t)` as a runtime precondition value; the identification of zeros as separators is only licensed for T4-valid `t` (by T4's definitional role-assignment) and breaks for arbitrary tumblers where adjacent zeros exist.
**Issue**: The vocabulary description "zero-valued field-separator components" presupposes T4's role-assignment, but the formula counts every zero regardless of whether it plays a separator role. For a tumbler like `[1, 0, 0, 3]` (used as a concrete counterexample in T4c and TA5a), the formula counts two zeros but only one can be a separator under any admissible parse — they can't both be separators because no two zeros are adjacent in a T4-valid address. The vocabulary entry therefore misstates what `zeros(t)` computes for the non-T4-valid case, which is the case TA5a's preservation analysis most needs to reason about.
**What needs resolving**: The vocabulary entry must either drop the "field-separator" gloss (so the name refers purely to zero-valued components, matching T4's and TA5a's formal definition) or restrict its domain to T4-valid tumblers (and then acknowledge that TA5a's case analysis over arbitrary `t` uses `zeros(t)` outside this domain). As written, a reader who takes the vocabulary at face value will expect separator semantics at a symbol the formal properties use extensionally.
