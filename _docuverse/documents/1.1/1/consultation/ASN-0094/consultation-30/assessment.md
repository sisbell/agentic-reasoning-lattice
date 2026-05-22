# Channel Assignment — ASN-0094 review-30

**Date:** 2026-05-21 22:51

## Issue 1: Direct ASN-0093 citations
Reason: The framework already names the relevant scaffolding clauses in *Scope and Substrate Scaffolding*; reframing ASN-0093 citations as consumption through ASN-0086's SubstrateConformingLayer Definition is a structural rewrite derivable from the ASN's existing interface.

## Issue 2: Sh2/Sh3 stratification implicit on Sh0/Sh1
Reason: The dependence of `slot_addrs(·)` well-formedness on Sh0/Sh1 is internal proof-bookkeeping. Either making the citation explicit or merging the inductions is a self-contained editorial fix.

## Issue 3: AllocatedAddressAntichain Step 3.1 — proof structure
Reason: Replacing the case-split with a forward derivation from `{n_1, n_2, n_3} ⊆ Z_a` plus `|Z_a| = 3` is a proof simplification using machinery already present (finite-set cardinality, NAT-card). Internal.

## Issue 4: Lemma RetractionTargetNotOnChain — `home(a_emit(Σ, d))` evaluated outside `dom(Σ.L)`
Reason: The distinction between L1a as an invariant over `dom(Σ.L)` versus `home(·)` as a T4b-driven projection on T4-valid addresses with `zeros = 3` is derivable from ASN-0043's existing definitions. Either adding a Definition or shifting the citation to T4b is internal.

## Issue 5: ASN-0086 Nullify backwards-compatibility — audit-slice multiplicity loss is buried
Reason: The required fix is presentational — surface an already-made design commitment to a top-level position in the *Interaction with Nullify* section. The semantic decision (set-semantics for R) is settled; only its visibility is at stake.

## Issue 6: Length and density
Reason: Splitting into multiple ASNs is a structural reorganization decision derivable from the ASN's own component boundaries (framework + contracts + catalog). No external channels needed.

## Issue 7: No concrete worked example for AllocatedAddressAntichain Step II's full NAT-card additivity
Reason: Constructing a worked example with `#w ≥ 2` exercising the NAT-card additivity path uses only machinery already present in the proof. Pedagogical addition, internal.

## Issue 8: Sh5 catalog audit table — rejected row sits inside the catalog table
Reason: Pure presentation fix — separate the rejected row into a callout outside the accepted-rows table. Derivable from the ASN alone.
