# Channel Assignment — ASN-0047 review-116

**Date:** 2026-05-19 14:26

```
## Issue 1: C-fin missing from ExtendedReachableStateInvariants
Reason: Fix is internal — C-fin is already a foundation invariant of ASN-0093 (cited throughout this ASN); adding it to the conjunct list and matrix row (analogous to L-fin) is purely structural completion using material already in the ASN.
```

```
## Issue 2: L1c attribution misplaced
Reason: Fix is internal — correct attribution requires only consulting ASN-0093's L1c statement (already cited by this ASN); the question is which table the entry belongs in and how to phrase the foundation source, both derivable from the existing dependency chain.
```

```
## Issue 3: K.δ case (ii) k = 0 frontier discharge — dense argument needs lemma extraction
Reason: Fix is internal — the FrontierEquivalence argument (three premises: T10a per-`(t,0)` uniqueness, P1 monotonicity, T10a GlobalUniqueness) and the T4b-stratification counterexample are already in the ASN body; extraction as a named lemma is reorganization, no new derivation.
```

```
## Issue 4: K.δ case (ii) k = 2 sub-case A induction structure implicit
Reason: Fix is internal — the base case (sub-case B with NodeUniqueAllocation discharge; sub-case C with NodeRegistryBootstrap at Σ₀) is already specified in the ASN; making the well-founded recursion explicit just connects existing pieces.
```

```
## Issue 5: K.μ~ existence-condition narrative — mixed case (dom_C empty, dom_L non-empty)
Reason: Fix is internal — link-subspace fixity is already proved in the *Decomposition of K.μ~* section; the mixed-case derivation (`π|_{dom_L} = id` forces π = id when dom_C is empty) follows directly from material already in the ASN.
```

```
## Issue 6: Composite-boundary verification matrix lacks J0/J1★/J1'★ inputs
Reason: Fix is internal — the chained derivation through S3★ + L14 + S3★-aux is already present in the P7a proof body within Class (b); the matrix row just needs to be expanded to reflect what the proof actually does.
```
