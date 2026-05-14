# Channel Assignment — ASN-0042 review-62

**Date:** 2026-05-14 13:34

```
## Issue 1: Bootstrap seed wording conflates seeding with allocation
Reason: Pure terminology audit. The ASN's definition of `allocated_by_Σ` (transition-induced) and the bootstrap-seeds table already correctly distinguish seeding from allocation; the fix is to align the worked-example prose with these existing definitions.
```

```
## Issue 2: "Account-level family" misnomer in O7(c) chain construction
Reason: Internal labeling fix. The proof already separates the node→account boundary step from the within-account inductive extension; renaming follows directly from T4c (LevelDetermination) and condition (iv) as stated in the ASN.
```

```
## Issue 3: O3 worked-example verification omits the delegator witness
Reason: Missing citation of a fact already established earlier in the same worked example (`delegated_{Σ_0}(π_N, π_A)` was verified in the *Delegation* paragraph). Purely a cross-reference fix.
```

```
## Issue 4: Implicit uniqueness of the most-specific covering principal
Reason: The corollary follows from condition (ii), O1b, and the already-named covering-chain lemma — all internal to the ASN. The fix states it explicitly and cites it at O7(a) and DelegatorAllocatesPrefix.
```

```
## Issue 5: O10's namespace-vs-content gap is acknowledged but not in the postcondition
Reason: Editorial choice between two options the review already articulates. Both Nelson's confinement of the node operator to account allocation (LM 4/19) and Gregory's `docreatenewversion` evidence are already curated in the prose; the structural fact `zeros(a') = zeros(pfx(π)) + 1` is derivable from the existing proof construction.
```
