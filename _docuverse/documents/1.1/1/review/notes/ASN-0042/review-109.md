# Review of ASN-0042

## REVISE

### Issue 1: `delegated` relation used with undefined two-place arity in O7
**ASN-0042, O7 (OwnershipDelegation)**: "`(A π, π' : delegated(π, π') :`"
**Problem**: The relation is defined as four-place `delegated(Σ, Σ', π, π')` with a *single* abbreviation `delegated_Σ(π, π')`. O8 correctly uses the four-place form. O7's quantifier introduces a bare `delegated(π, π')` that matches neither the definition nor the abbreviation — the binding states for `pfx(π)` and `pfx(π')` are left implicit at exactly the point where O7(a)'s proof depends on reading `pfx(π)` at `Σ` and `pfx(π')` at `Σ'`. A reader cannot tell which transition the quantifier ranges over.
**Required**: Restate O7's statement and Formal Contract using either `delegated_Σ(π, π')` or the full four-place form, consistently with O8.

### Issue 2: Prose around O17b explains downstream interaction rather than what the axiom says
**ASN-0042, O17b (BaptismalRegistryCoupling)**: "A delegation transition falls in the *baptism* branch, not the frame branch: O18 ... records `pfx(π') ∈ Σ'.B ∖ Σ.B` ... and condition (v) fixes that prefix as `next(Σ.B, p, d)`. The frame branch therefore covers only genuine no-op-on-`B` operations."
**Problem**: This is the flagged anti-bloat pattern — new prose around an axiom that argues how it interacts with O18/condition (v) downstream rather than advancing the axiom's own content. The axiom already states the two-branch disjunction; the delegation/branch reconciliation belongs in O18's or the delegation proof's reasoning, where it is in fact re-derived.
**Required**: Drop the trailing reconciliation paragraph; if the delegation-is-baptism fact is needed, cite it at the one site (DelegatorAllocatesPrefix / O18) that uses it.

### Issue 3: Defensive justification against a non-claim in the Exclusivity Invariant
**ASN-0042, The Exclusivity Invariant**: "The predicate enumerates no registry and computes no longest match; it answers a single two-tumbler containment question, so it cannot by itself single out one owner. Exactly-one-effective-owner is supplied instead by the longest-match selection rule that defines `ω` (O2 below), not by the boolean's arity."
**Problem**: The real content — exclusivity is a property of `ω`, not of `owns` — is established by O2. The "not by the boolean's arity" rebuttal defends against a misreading nobody is asserting, and carries a forward pointer "(O2 below)." This is defensive meta-prose the precise reader must skip to reach the actual lemma.
**Required**: Reduce to the load-bearing sentence (exclusivity is a property of `ω`, established at O2) and remove the arity rebuttal.

### Issue 4: Forward-reference accretion to the Worked Example and to "below"
**ASN-0042, O7(c) and Bootstrap seeds**: "(an explicit account-level delegation chain witnessing this is given in the Worked Example)"; "The delegated prefix `[1, 0, 2]` is deliberately *not* seeded — it is baptized at the delegation transition below, satisfying O18's freshness conjunct"; AccountField: "The construction is given once in the Formal Contract below."
**Problem**: Multiple sections defer to the same downstream location (Worked Example) or justify document ordering ("not seeded ... below," "given once ... below"). These are the flagged forward-reference / ordering-justification patterns. The recursion of O7(c) is either proved abstractly or it is not; an example is an illustration, not a discharge of the proof obligation.
**Required**: Either prove the unbounded-recursion claim where O7(c) is stated, or state it as illustrated-not-proved without the forward pointer. Remove the ordering-justification asides on seeding and on AccountField's construction placement.

### Issue 5: Derived result with no abstract consumer
**ASN-0042, DelegatorAllocatesPrefix**: full derived property + Formal Contract.
**Problem**: This derived property (delegator = allocator of the delegate's prefix) is not cited in the Depends/derivation of any abstract claim (O3, O7, O8, O10, O4 all list other premises). Its sole consumer is one line of the Worked Example. A derived theorem whose only use is decorating an example is accreted weight, not advancing the reasoning chain.
**Required**: Either show it is load-bearing for an abstract claim (and cite it there) or demote the fact to an inline remark in the Worked Example.

## OUT_OF_SCOPE

No material scope violations. O10's "the system does not grant modification" framing brushes access control (declared out of scope), but the discharged claim is purely ownership-model (fork existence with `ω(a') = π`), so it is correctly in scope. The ASN consumes ASN-0040's baptism machinery as a foundation rather than re-deriving baptism invariants, which is appropriate.

META: not triggered — the ASN defines ownership state, the delegation operation, and reachable-state invariants stated abstractly enough to bind any conforming implementation, so it has not drifted into implementation mechanics.

VERDICT: REVISE
