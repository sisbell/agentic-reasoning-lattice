# Review of ASN-0045

## REVISE

### Issue 1: at-least-one enumeration silently uses trichotomy (NAT-order) without citing it

**ASN-0045, Well-Definedness / at-least-one**: "Together `0 ≤ zeros(t) ≤ 3` confines zeros(t) to the bounded segment, but the step from this bound to the *disjunction* … requires discreteness: NAT-discrete (ASN-0034) … and so enumerates the segment as `0 ≤ n ≤ 3 ∧ n ∈ ℕ ⟹ n ∈ {0, 1, 2, 3}`."

**Problem**: NAT-discrete alone does not yield the enumeration. Discreteness only rules out a natural lying strictly *between* two consecutive values; to conclude that `n` actually *equals* one of `0,1,2,3` you must compare `n` against each boundary (is `n < 1` or `n ≥ 1`? `n < 2` or `n ≥ 2`? …). Each such case split is an appeal to trichotomy — NAT-order (ASN-0034) — which the ASN's own foundation states is *independent* of discreteness ("This discreteness axiom is independent of strict total order"). NAT-order appears nowhere in the at-least-one prose nor in Partition's Depends list (which names only T4, T0, NAT-discrete, NAT-closure, T4c). Relatedly, treating `0,1,2,3` as "consecutive enumerated values" leans on the strict successor inequalities `0<1<2<3`, i.e. NAT-addcompat's `n < n+1`, which is likewise uncited. The ASN otherwise commits to the strict per-step ℕ-citation convention (it carefully cites NAT-discrete and NAT-closure), so the omission is an inconsistency in its own stated standard, not a harmless shorthand.

**Required**: Add NAT-order (trichotomy) — and NAT-addcompat for the successor inequalities — to the at-least-one derivation and to Partition's Depends, and show (or state) the comparison/case-split chain by which bound + discreteness + trichotomy yields `n ∈ {0,1,2,3}`.

### Issue 2: Account lists T4c as a base-biconditional dependency, contradicting the treatment given to the other three predicates

**ASN-0045, Properties Introduced / Account, *Depends***: "T0, T4, T4c, NAT-closure (the constant 1). The rename-equivalence postcondition additionally depends on T4b (UniqueParse) and T3 (CanonicalRepresentation)…"

**Problem**: For Node, Document, and Element the ASN states explicitly that "T4c … does no work in this biconditional and is not a proof dependency." Account's *base* postcondition `Account(t) ⟺ T4-valid(t) ∧ zeros(t) = 1` is structurally identical and equally does not need T4c — T4c is required only for the separate *rename-equivalence* postcondition. Yet Account's Depends lists T4c in the unqualified base list without the caveat applied to the other three, leaving a reader to conclude T4c is load-bearing for the base biconditional. This is a clarity/consistency defect in a document whose entire purpose is precise dependency attribution.

**Required**: Scope T4c (and T4b, T3) to the rename-equivalence postcondition only, and state for Account — as for the other three — that T4c does no work in the base biconditional.

## OUT_OF_SCOPE

None.

VERDICT: REVISE
