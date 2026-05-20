# Channel Assignment — ASN-0094 review-6

**Date:** 2026-05-19 21:30

## Issue 1: Sh4 contract invokes Observe_K with infinite arguments
Reason: Fix is internal — replace `coverage(F)` with the finite `slot_addrs(F)` in the Observe_K invocation, then specify post-filtering to exact slot-pair equality. AllocatedAddressAntichain (already in the ASN) bridges the syntactic slot-address pattern to the semantic candidate set; the proof reverification uses only structures already present.

## Issue 2: No worked example for FunctionalDependencyDiscipline
Reason: Fix is internal — construct an example by instantiating the FDD contract (clauses i–iii) and the singleton-returning `K_target_of` template, both fully specified in the ASN. No external evidence is required to exhibit a contract-driven rejection.

## Issue 3: No worked example for Sh4 emission suppression
Reason: Fix is internal — construct an example with an idempotent K (Tuple-Classifier or DirectedPair without FDD) exercising the Sh4 contract's clauses (i)–(iii). All ingredients are defined in the ASN.

## Issue 4: No worked example for K ∉ T_cat rejection
Reason: Fix is internal — exhibit an emission with `K ∈ T_admissible \ T_cat` rejected at Sh-conf's first conjunct. The catalog `T_cat` and Sh-conf's gating are fully specified in the ASN.

## Issue 5: AllocatedAddressAntichain Case 3 — "swap" wording obscures the symmetry
Reason: Fix is internal — pure rephrasing of the existing argument to clarify that the subspace labels swap, not the prefix relation. No new content needed.

## Issue 6: Initial state Σ_0 not formally pinned for induction
Reason: Fix is internal — state the framework's scope condition: preservation theorems hold along `↦*`-chains starting from any Σ_init with `L_K^{Σ_init} = ∅` for every `K ∈ T_cat`. The conditional framing is a framework-level decision.

## Issue 7: Sh-conf failure semantics underspecified
Reason: Fix is internal — the framework's `Emit_K` is a layer-level operation (distinct from substrate primitive K.λ, per Scope and Substrate Scaffolding), and the framework owns its own failure interface. Specify the failure return as a sum type or `⊥` sentinel at the layer level.

## Issue 8: Sh5 "base template" criterion not formally defined
Reason: Fix is internal — specify the criterion using ingredients already named in the ASN (shape components, K's name, Sh0–Sh4 with layer commitments, per-K disciplines, parametric arguments), then verify each catalog row against it.

## Issue 9: Compatibility constraint between FDD and SHCD not stated
Reason: Fix is internal — the structural exclusivity follows directly from FDD requiring idem=⊤ (DirectedPair) and SHCD requiring idem=⊥ (NonIdempotentDirectedPair Coverage). Stating this is a one-line addition derivable from existing definitions.

## Issue 10: Sh1 inductive step omits Case D, but Sh0 omits Case C and D
Reason: Fix is internal — add a one-line citation to R3 (TupleAddressPermanence, ASN-0086) establishing `L_K` monotonicity, which restricts the case analysis to A and B. R3 is already referenced elsewhere in the ASN.

## Issue 11: Sh5 catalog's `(0|1, A)` shapes — Provenance well-formedness ambiguity
Reason: Fix is internal — the ASN must decide whether `c_X = 0|1, t_X ≠ -` is well-formed (which preserves Provenance as registered) or tighten the rule. Provenance's worked example treats this as well-formed; the formal rule needs to match the example. Framework-level design decision.

## Issue 12: Sh4 Case D's pairwise distinctness extension to A_R^Σ ∪ {τ_new}
Reason: Fix is internal — make Sh4's universal-quantifier scope explicit (over all `(τ, τ')` pairs including reflexive). The bookkeeping is straightforward from the existing statement.

## Issue 13: Sh5 META claim conflates discipline with theorem
Reason: Fix is internal — either upgrade the "framework guarantees" sentence to a typed claim (DEF or LEMMA) or downgrade it to a discipline statement. Pure metaphysical-status decision the framework can make for itself.
