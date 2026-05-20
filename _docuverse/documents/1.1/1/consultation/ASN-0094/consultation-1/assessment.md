# Channel Assignment — ASN-0094 review-1

**Date:** 2026-05-19 19:17

## Issue 1: Coverage cardinality formulation is mathematically broken
Reason: The fix is a formal repair internal to the ASN — choosing between `cov_allocated` operator vs syntactic span-form check, both derivable from ASN-0043 (coverage, PrefixSpanCoverage) and ASN-0034 (T0a/T0b) definitions already in scope. No design intent or implementation evidence is needed.

## Issue 2: Nullify under Retraction shape fails Sh-conf
Reason: Same root cause as Issue 1 — once coverage interpretation is fixed, the Nullify check is a direct verification against ASN-0086's Nullify definition. Internal to the ASN.

## Issue 3: Sh0–Sh3 induction handles only `→`, not `↦`
Reason: The remedy is mechanical — add a case citing LinkStoreInvarianceUnderArrangement from ASN-0086, which the review itself identifies. Pure proof completion using lattice-internal facts.

## Issue 4: Coverage template's `emission_order` is not defined cross-allocator
Reason: This is a design choice within the new substrate framework (global counter vs single-home restriction vs layer-supplied). The substrate is a fresh design atop Xanadu primitives, so neither Nelson's design intent nor udanax-green's implementation speaks to it. Internal.

## Issue 5: Sh4 is policy but K_sidecar_of's totality depends on it
Reason: Whether to elevate Sh4 to axiom, weaken `K_sidecar_of`, or make templates conditional is a substrate design choice. ASN-0086's R0/R1 already establish that idempotency cannot be derived from the substrate axioms — the question is what restriction layer to impose, which the ASN decides itself.

## Issue 6: `T_cat` is referenced but never defined
Reason: Definitional cleanup using existing lattice vocabulary (T_admissible from ASN-0086). The four readings enumerated in the review can be disambiguated by the ASN's own usage pattern. Internal.

## Issue 7: Shape registry mutability is unspecified
Reason: Design decision for the new substrate framework. Constancy is the natural axiomatic choice for inductive preservation arguments; the ASN can state this directly. Internal.

## Issue 8: `K_is_fresh` violates Sh5's mechanical-derivability claim
Reason: Choice between removing `K_is_fresh` from the family or generalizing Sh5 to admit registered external accessors. Pure design choice in the new framework. Internal.

## Issue 9: `latest_K_for_addr(d)` is partial on empty `S_d`
Reason: Definitional fix — make optionality explicit using the `⊥` convention already established for `to₁⁻`. Internal.

## Issue 10: The "typical case" of no allocated descendants is a load-bearing theorem
Reason: The property follows from R0a (link antichain, ASN-0086) and the content-side antichain (ASN-0093/0034). All ingredients are lattice-internal; the task is to state and prove the lemma. Internal.

## Issue 11: Sh5 is a proof sketch with no derivation procedure
Reason: Design choice — exhibit an algorithm parameterized on shape components, or downgrade Sh5 to META. The framework's content alone determines which path is sustainable. Internal.

## Issue 12: No concrete worked example
Reason: The example must be constructed from the ASN's own catalog and ASN-0086's tuple emission semantics. All inputs are already present in the lattice. Internal.

## Issue 13: Open Questions include items that are this ASN's responsibility
Reason: Resolution of items 6 and 8 follows from fixing Issues 4 and 3 respectively. Once those are addressed, the Open Questions list trims itself. Internal.
