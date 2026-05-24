# Channel Assignment — ASN-0094 review-34

**Date:** 2026-05-23 19:10

```
## Issue 1: BundledDirectedPair admits `c_G = 0` but the case is unaddressed
Reason: Fix is derivable from the ASN — choose between walking the `n = 0` case explicitly (parallels existing Retraction `c_F = 0` Nullify-alias handling at the symmetric shape) or tightening to `1..*` (requires a new cardinality token outside the existing `{0, 1, *, 0|1}` vocabulary; the simpler option (c) cross-reference is the consistent choice). The Retraction walkthrough's bare-form treatment already supplies the template the BundledDirectedPair walkthrough can mirror.
```

```
## Issue 2: AllocatedAddressAntichain Step 3.1 cites an uncited set-theoretic fact
Reason: Fix is internal — derive the subset-equality-by-cardinality principle from NAT-card's uniqueness clause, which the surrounding paragraph already cites. Apply NAT-card to both `Z_a` and `{n_1, n_2, n_3}` and conclude equality of the strictly-increasing enumerations.
```

```
## Issue 3: Tuple-Classifier walkthrough lacks a rejection case
Reason: Fix is internal — add a symmetric rejection case mirroring Classifier's Rejection case 1, with G targeting `d ∈ A_doc^Σ` against `t_G = A_rel`, citing R4 (ASN-0086) for the partition disjointness. The exposition pattern is already established at the Classifier walkthrough.
```

```
## Issue 4: Coverage walkthrough describes the empty-`S_d` path but doesn't exhibit it
Reason: Fix is internal — add a "Template evaluation at Σ_0" table parallel to the existing Σ_3 table, showing `latest_K_for_addr(d_subject) = ⊥` and the consumer's dispatch obligation. All required content (the `⊥` value, the partiality propagation rule) is already stated; the issue is exhibition, not derivation.
```

```
## Issue 5: Sh4 Case D's "by Case B's argument" obscures the chain
Reason: Fix is internal — replace the phrasing with explicit citation of the *Sh4 idempotency contract* clause (iii), noting the contract fires uniformly across both `K ≁ R` and `K ~ R` regimes. The contract is already defined and Case D's structure already presupposes it; only the citation wording needs adjustment.
```

```
## Issue 6: Opt-in registry well-formedness is informal
Reason: Fix is internal — state FDD's structural preconditions (`c_F = 1 ∧ t_F = A_doc`) explicitly in its Definition. The preconditions are already implicit in the preservation proof's use of `from₁(τ)` (requiring `c_F = 1` per SlotAccessorTotality) and in `K_target_of`'s codomain `A_doc^Σ ∪ {⊥}` (requiring `t_F = A_doc`); making them explicit is a documentation clarification, not a new commitment.
```
