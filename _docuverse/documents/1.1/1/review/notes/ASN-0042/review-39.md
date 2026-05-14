# Review of ASN-0042

## REVISE

### Issue 1: NestingByDelegation derived in text but absent from Properties Introduced table
**ASN-0042, State Axioms section / Properties Introduced table**: The State Axioms section defines and proves NestingByDelegation as a derived property (`(A Σ : Σ reachable from Σ₀ : (A π₁, π₂ ∈ Π_Σ : π₁ ≠ π₂ ⟹ ...))`). The Properties Introduced table lists FiniteRegistry — also a derived property proved in that same section — but omits NestingByDelegation.
**Problem**: The table is the ASN's catalog of properties. The "first-delegator form" Remark in AccountLevelPermanence explicitly cites NestingByDelegation's forest geometry, and the inductive case structure of the sub-delegate analysis in O10 tacitly relies on it. A reader consulting the table for what the ASN delivers cannot locate it.
**Required**: Add a row to the Properties Introduced table for NestingByDelegation with provenance (e.g., "from O1b, O12, O13, O14(vi), delegation condition (vi), covering-chain lemma").

### Issue 2: The cumulative invariant "every principal's prefix is in Σ.B" is used but not formally derived as a named property
**ASN-0042, Worked Example self-ownership paragraph; O10 proof non-coverage analysis**: The Worked Example's "Self-ownership at the prefix" paragraph asserts the general theorem `(A Σ, π ∈ Π_Σ : ω_Σ(pfx(π)) = π)`, justified in prose by "Combining O18's inductive clause... with O14's seventh clause..., every principal's prefix is in `Σ.B`". O10's non-coverage analysis says "Now invoke O18 (DelegationBaptizes): every Form B sub-delegate's prefix `pfx(π_i) = pfx(π).0.U^{(i)}_1` lies in `Σ.B`".
**Problem**: O18 alone supplies the inductive step (each delegating transition baptizes the new delegate's prefix); O14(vii) supplies the base case (every bootstrap principal's prefix lies in `Σ₀.B`). Combining them yields the cumulative invariant by induction on transition path length, but the spec neither states this as a named property nor proves it. O10's bare citation "invoke O18" elides the bootstrap case for sub-delegates entirely, and the worked example's self-ownership claim depends on the same unstated invariant. Per the rigor standard, derived guarantees must be explicitly derived; this guarantee is asserted but not built.
**Required**: Add a named derived property (e.g., `PrefixBaptismCoupling: (A Σ reachable, π ∈ Π_Σ : pfx(π) ∈ Σ.B)`) to the Properties Introduced table with provenance from O14(vii), O15, O18, T8. Prove it inline (induction on transition path length: base case O14(vii); inductive step O15 cases on whether a new principal enters via O18 — using T8 to carry baptized prefixes forward). Replace the in-line citation "invoke O18" in O10's non-coverage analysis with a citation to this derived property; replace the prose-only justification in the worked example with a citation.

### Issue 3: Self-ownership at the prefix asserted as a general theorem but not catalogued
**ASN-0042, Worked Example self-ownership paragraph**: "the general fact holds unconditionally in every reachable state for every principal: `(A Σ, π ∈ Π_Σ : ω_Σ(pfx(π)) = π)`."
**Problem**: This is a clean, useful, general theorem proved in the worked example by a structural argument (reflexivity of `≼`, O1b for distinct prefixes, cumulative prefix-baptism invariant for `pfx(π) ∈ Σ.B`). It is invoked directly nowhere else in the proof body but reads like a load-bearing corollary of the ownership model. Stranding a general theorem inside a worked example obscures it from the catalog and means future ASNs cannot cite it by name.
**Required**: Promote the self-ownership theorem to the Properties Introduced table as a derived property (e.g., `SelfOwnershipAtPrefix`), with provenance from O1b, O2, and the prefix-baptism invariant (Issue 2). Retain the worked example as the verification scenario, not the proof site.

## OUT_OF_SCOPE

(None — the ASN remains squarely within the abstract specification of ownership.)

VERDICT: REVISE
