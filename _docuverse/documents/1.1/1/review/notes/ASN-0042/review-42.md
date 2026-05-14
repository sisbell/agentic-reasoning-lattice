# Review of ASN-0042

## REVISE

### Issue 1: O10's Form B analysis has imprecise quantifier scope
**ASN-0042, *The Fork as Ownership Boundary*, proof of O10**: "Now invoke PrefixBaptismCoupling: every Form B sub-delegate `π_i` ∈ Π_Σ has pfx(π_i) = pfx(π).0.U^(i)_1 ∈ Σ.B in the reachable state Σ, hence U^(i)_1 ∈ S(pfx(π), 2) ∩ Σ.B, hence U^(i)_1 ≤ hwm_0. The set S' := { U^(i)_1 : π_i is a Form B sub-delegate } satisfies S' ⊆ {1, …, hwm_0}..."
**Problem**: The claim "pfx(π_i) = pfx(π).0.U^(i)_1" is only valid for length-(#pfx(π)+2) Form B sub-delegates; Form B sub-delegates with prefix length > #pfx(π)+2 have form pfx(π).0.U^(i)_1.U_2.… and do not fit this equality. Consequently S' need not satisfy S' ⊆ {1, …, hwm_0} — a longer Form B sub-delegate could have U^(i)_1 = hwm_0+1. The proof's final conclusion ("no Form B sub-delegate covers a'") still holds because longer Form B sub-delegates are excluded by the length argument in the prior sentence, but the intermediate S' claim is overstated.
**Required**: Restrict the PrefixBaptismCoupling argument explicitly to length-(#pfx(π)+2) Form B sub-delegates: "Among length-#pfx(π)+2 Form B sub-delegates, every π_i has pfx(π_i) = pfx(π).0.U^(i)_1, and by PrefixBaptismCoupling + B1, U^(i)_1 ≤ hwm_0." Drop the unrestricted S' definition or scope it to the length-#pfx(π)+2 class.

### Issue 2: Worked example omits the field-opening boundary case of O10
**ASN-0042, *Worked Example*, "Fork (O10)" paragraph**: The fork scenario fixes `hwm_0 = 5` and exhibits only the sibling-advance branch `inc([1, 0, 2, 0, 5], 0) = [1, 0, 2, 0, 6]`.
**Problem**: The proof of O10 handles two structurally distinct branches of `next`: the field-opening branch when `hwm_0 = 0` (yielding `inc(pfx(π), 2)` of length `#pfx(π) + 2` via TA5(d)) and the sibling-advance branch when `hwm_0 ≥ 1` (yielding `inc(pfx(π).0.{hwm_0}, 0)` via TA5(c)). The boundary case `hwm_0 = 0` (where no Form B sub-delegate of length `#pfx(π) + 2` can exist at all because PrefixBaptismCoupling + B1 force `S(pfx(π), 2) ∩ Σ.B = ∅`) is the cleanest verification scenario and is not exhibited.
**Required**: Add a concrete scenario in the worked example for fork at `hwm_0 = 0` — e.g., a freshly-delegated principal with no prior children, exhibiting `a' = inc(pfx(π), 2)` and verifying O10(a), O10(b) against this case.

### Issue 3: O7(c)'s recursive-chain construction is informal
**ASN-0042, *Delegation*, proof of O7(c)**: "Inductively: at Σ_k (the state immediately after π_0, …, π_k have been introduced), the existing prefixes have lengths 1, 3, 4, …, k+2 respectively, and the covering principals of pfx(π_{k+1}) (length k+3) in Π_{Σ_k} are exactly π_0, …, π_k..."
**Problem**: The exhibition of an unbounded delegation family `pfx(π_k) = [1, 0, 1, 1, ..., 1]` is valid as a witness, but the inductive verification of conditions (ii) (most-specific covering) and (vi) (no existing strict extension) at each Σ_k is sketched in prose rather than discharged formally. Specifically, the assertion that "the covering principals of pfx(π_{k+1}) in Π_{Σ_k} are exactly π_0, …, π_k" relies on the chain construction without showing that no other principal in `Π_{Σ_k}` can cover `pfx(π_{k+1})` — a complete argument would invoke NestingByDelegation at Σ_k to constrain the non-chain principals to be non-nesting.
**Required**: Either strengthen the inductive step to discharge conditions (ii)/(vi) at each Σ_k by explicit citation (NestingByDelegation forcing non-chain principals into the non-nesting disjunct relative to `pfx(π_{k+1})`), or weaken the claim to "the family exhibits arbitrarily long chains, modulo a base state at which Π contains only the chain ancestors."

VERDICT: REVISE
