# Cone Review — ASN-0034/T12 (cycle 2)

*2026-04-18 05:52*

### TA0 and TA-strict Depends omit T0 for `#` (and TA-strict omits T0 entirely)
**Foundation**: T0 (CarrierSetDefinition) — introduces the carrier `T` and the length operator `#`. T1's Depends entry makes the discipline explicit ("the definition uses length `#a` and component projection `aₖ` for `a ∈ T`, which T0 introduces"); the previous finding on Definition (Span) also asserts that "T1 and TA0 each cite T0 by name for exactly these usages."

**ASN**:
- **TA0 (WellDefinedAddition)**. Depends entry for T0 reads only: "T0 (CarrierSetDefinition, this ASN) — supplies the meaning of `∈ T` in the postcondition `a ⊕ w ∈ T`." But TA0 also writes `#` directly in its precondition `actionPoint(w) ≤ #a` and in its postcondition `#(a ⊕ w) = #w`; the `a, w ∈ T` precondition is a third T0 usage not covered by the "postcondition `a ⊕ w ∈ T`" scope the T0 entry cites.
- **TA-strict (StrictIncrease)**. Statement: `(A a, w ∈ T : Pos(w) ∧ actionPoint(w) ≤ #a : a ⊕ w > a)`. Depends list enumerates "TumblerAdd … TA-Pos … ActionPoint … TA0 … T1" — T0 is absent, despite `∈ T` (in the quantifier range) and `#a` (in the precondition) appearing directly in TA-strict's own body.

**Issue**: The ASN articulates a discipline under which an ASN that writes T0's vocabulary directly cites T0 directly (Definition (Span)'s revised Depends and T1's Depends both follow it). TA0 and TA-strict do not. TA0's T0 citation is scoped narrowly to "the postcondition `a ⊕ w ∈ T`," silently leaving the `#` usages in the precondition and second postcondition, and the `∈ T` in the precondition, unsourced. TA-strict cites TA0 only "to discharge the membership `a ⊕ w ∈ T`" on the inequality's left-hand side; this does not source the `∈ T` in the quantifier range `a, w ∈ T` or the `#a` in the precondition — neither of which passes through TA0's re-export handle. Under the ASN's own discipline, these usages need a direct T0 citation; under an alternative "inherit T0 transitively" convention, the direct T0 citations in T1, Definition (Span) (per previous finding), and TA0's postcondition become unmotivated.

**What needs resolving**: Either (a) extend TA0's T0 entry to enumerate the `#a` precondition usage and `#(a ⊕ w) = #w` postcondition usage (and the `∈ T` precondition usage), and add a T0 entry to TA-strict's Depends naming the `∈ T` quantifier-range and `#a` precondition usages; or (b) declare a uniform transitive-inheritance convention for T0 across all properties in the ASN and reconcile it with the direct T0 citations currently appearing in T1, Definition (Span), and TA0's postcondition.
