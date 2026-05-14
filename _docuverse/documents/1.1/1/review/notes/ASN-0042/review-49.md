# Review of ASN-0042

## REVISE

### Issue 1: Worked example's sub-account namespace + subsequent delegation contradicts O18

**ASN-0042, Worked Example, "Sub-account namespace"**: "If `π_A` subsequently delegates `[1, 0, 2, 3]` to `π_B`, then `ω(a₄)` refines to `π_B` and `pfx(π_B) = acct(a₄) = [1, 0, 2, 3]` — provenance sharpens to equality."

**Problem**: The Sub-account namespace paragraph just established that `[1, 0, 2, 3]` was baptized as a namespace (i.e., `[1, 0, 2, 3] ∈ Σ.B`). O18 (DelegationBaptizes) requires delegated prefixes to be *fresh*: `pfx(π') ∈ Σ'.B ∖ Σ.B`. A subsequent delegation of an already-baptized prefix is therefore structurally impossible. The conditional is vacuously true, but its presentation as a continuation ("subsequently") is misleading — a reader following the timeline will assume this is a reachable scenario when it cannot occur in any model satisfying O18.

**Required**: Either (a) remove the conditional, (b) reframe it as an alternative timeline where the namespace baptism did *not* occur, or (c) explicitly acknowledge that O18 prohibits this transition and use the conditional to illustrate the structural commitment rather than a possible trajectory.

### Issue 2: O1's preconditions over-restrict the predicate's domain

**ASN-0042, O1 (PrefixDetermination), Formal Contract**: "Preconditions: π ∈ Π, a ∈ T, T4(pfx(π)), T4(a). Postconditions: owns(π, a) is a total, decidable predicate on Π × T."

**Problem**: The postcondition claims totality on `Π × T` (the unrestricted address carrier), but the preconditions require `T4(a)`. The well-formedness argument preceding the contract correctly identifies that only `T4(pfx(π))` and T3's component determinacy are needed — the Prefix relation `p ≼ a` reduces to one length comparison and at most `#p` component comparisons on naturals, both well-defined for any `a ∈ T` regardless of T4-validity. The `T4(a)` precondition is over-stated and inconsistent with the postcondition.

**Required**: Either drop `T4(a)` from preconditions (preferred — preserves the total-on-`Π × T` claim), or weaken the postcondition's domain to `Π × {a : T4(a)}` and explain the choice. The current contract is internally inconsistent.

## OUT_OF_SCOPE

None additional — the ASN's Open Questions section already captures the relevant deferrals (ownership transfer, overlap enforcement, content accessibility, domain density, cross-node federation, provenance/transfer divergence, delegation event records), and the identity scope note correctly excludes authentication mechanisms.

VERDICT: REVISE
