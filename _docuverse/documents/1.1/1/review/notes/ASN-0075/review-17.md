# Review of ASN-0075

## REVISE

### Issue 1: wp(SHOWDELETIONS, Q0) is not the weakest precondition

**ASN-0075, "Distinguishing... Vacuity of both report halves"**: The formula

```
wp(SHOWDELETIONS(d_A, d_B), Q0)
   =  Σ reachable
    ∧  d_A ∈ E_doc  ∧  d_B ∈ E_doc
    ∧  (A a ∈ dom(C) :  subspace_I(a) = s_C : ...)
```

includes "Σ reachable" as a literal conjunct.

**Problem**: This makes the formula stronger than necessary, so it is *not* the weakest precondition. For an observational operation, wp(op, Q) = (precondition) ∧ Q(Σ) — and Q0(Σ) is a state-level predicate well-defined at any Σ (the predicates CURRENT, DELETED, NEVER_INCLUDED depend on M, R, dom(C), subspace_I, none of which require reachability to evaluate). Consider an unreachable Σ' with dom(C') = ∅: Q0 holds trivially, so wp should be TRUE, but the ASN's formula evaluates to FALSE because "Σ reachable" fails. P4★ is invoked only in the *supplementary* argument that "R-disjointness implies Q0" — that argument requires reachability, but the universal-quantifier wp formula itself does not.

**Required**: Remove "Σ reachable" from the wp formula proper. Either present it as a separate meta-annotation ("for reachable Σ, this formula characterizes wp"), or restructure to distinguish (a) the wp formula (no reachability needed) from (b) the supplementary "R-disjoint ⟹ Q0" lemma (reachability needed). The asymmetry with Q1's wp — which correctly omits "Σ reachable" — exposes the inconsistency.

### Issue 2: Bijection in D-ACT — verify class-as-shift-chain explicitly

**ASN-0075, D-ACT**: "Each equivalence class C corresponds to a unique witness run... This assignment is a bijection between equivalence classes and witness runs: distinct classes have distinct minima... and the inverse — given a witness run (i_start, ℓ, origin), recover the class {i_start, shift(i_start, 1), …, shift(i_start, ℓ − 1)} — is determinate by the same shift function."

**Problem**: The argument establishes injectivity of the forward map (distinct minima) but leaves the load-bearing inverse-then-forward direction implicit. Specifically, for `Inverse ∘ Forward = identity`, one must show that starting from a class C, the reconstructed set `{min(C), shift(min(C), 1), ..., shift(min(C), |C|-1)}` equals C. This requires combining three pieces the ASN provides separately: (i) classes are T1-contiguous within dom(C), (ii) the no-intermediate-content argument shows consecutive same-origin dom(C) elements are shift-adjacent, (iii) min(C) is the lower endpoint. The assembly is left to the reader. The bijection sentence itself only addresses *injectivity*, not the surjectivity-onto-the-canonical-set claim.

**Required**: One explicit sentence chaining the pieces — e.g., "By T1-contiguity within dom(C) and the no-intermediate-content lemma, any T1-consecutive pair in C is shift-adjacent; induction from min(C) upward shows C = {min(C), shift(min(C), 1), ..., shift(min(C), |C|-1)}, completing the inverse direction of the bijection."

### Issue 3: D-ORD presentation order claim is weakly verified

**ASN-0075, D-ORD**: "the order is consistent with the witness document's V-position ordering of the referenced addresses... vpos_B(a) = min{v ∈ dom(M(d_B)) : M(d_B)(v) = a} under T1."

**Problem**: The ASN acknowledges that S5 permits multiple V-positions mapping to the same I-address and selects the minimum as a canonical representative, but does not verify that the resulting order on `DeletedFromAWithB` is well-defined as a total order. If two addresses a, a' in `DeletedFromAWithB` could share `vpos_B(a) = vpos_B(a')`, the ordering would be incomplete. Distinct I-addresses cannot occupy the same V-position by S2 (functionality of M(d_B)), so the minima must differ — but this one-line consequence is not stated.

**Required**: Add a sentence noting that S2 (M(d_B) is a function) forces distinct minima for distinct I-addresses, so `vpos_B` induces a strict total order on `DeletedFromAWithB`.

## OUT_OF_SCOPE

### Topic 1: Generalization to families of 3+ documents
**Why out of scope**: The ASN's open question explicitly identifies this as future work. Binary SHOWDELETIONS is the foundational case; multi-document extensions require new witness-structure analysis.

### Topic 2: Concurrency consistency model
**Why out of scope**: Concurrent state transitions are not yet specified in the foundation ASNs. SequentialTransitionAxiom (ASN-0047) makes transitions totally ordered.

### Topic 3: "Show additions" or "show changes" operation
**Why out of scope**: The ASN is specifically about deletions. A symmetric or unified operation would be a separate ASN.

### Topic 4: Restoration operation specifics
**Why out of scope**: The ASN's "Composability with Restoration" section notes that restoration is *enabled* but explicitly not specified here.

VERDICT: REVISE
