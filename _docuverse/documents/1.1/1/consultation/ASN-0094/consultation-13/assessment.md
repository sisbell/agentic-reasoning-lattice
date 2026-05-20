# Channel Assignment — ASN-0094 review-13

**Date:** 2026-05-20 00:03

## Issue 1: Provenance template family asymmetric in the catalog table
Reason: This is a Sh5(b)-discipline question internal to the framework — the base template family is mechanically determined by the shape `(1, 0|1, A, A, ⊤)`, and the choice between listing the full family (with explicit `⊥` handling) or documenting why `c_G = 0|1` precludes the other templates is derivable from the ASN's own Sh5(b) criterion plus the partial-accessor definitions of `to₁⁻`.

## Issue 2: Catalog table column format is inconsistent
Reason: Pure formatting/uniformity fix — apply the existing base/opt-in/parametric tagging criterion (already defined in the framework) consistently across all rows. The classification of each row's templates is determined by the criterion already stated in "Catalog row structure: base, opt-in, parametric."

## Issue 3: Template codomains are implicit
Reason: Codomain declarations follow mechanically from the shape components and the Sh2/Sh3 target-domain restrictions; the framework already establishes the types involved (`A_doc^Σ`, `A_rel^Σ`, `A_K^Σ`, `t_G^Σ`), so adding explicit signatures is internal.

## Issue 4: AllocatedAddressAntichain Lemma's symmetric Case 3 sub-case is hand-waved
Reason: The symmetric sub-case is a mechanical swap of subspace identifiers already characterized in the proof; writing it out explicitly is internal proof-discipline work derivable from the existing Step 3.1–3.3 structure plus the symmetric scaffolding clauses.

## Issue 5: Sh4 Case D's atomicity scope is informally characterized
Reason: This is a framework-scope decision — restricting Sh4's contract to single-process substrates (where "concurrent" reduces to within-call sequentiality) is internally derivable, and the Open Questions already flags cross-process consistency as deferred. The framework can scope itself without external input.

## Issue 6: `K_target_of`'s singleton-returning behavior depends on FDD but the dependency is not stated in the template's location
Reason: Pure documentation/cross-referencing fix — FDD's preservation theorem is already proved in the same section, so adding a precondition clause at the template's definition site that cites the existing FDD lemma is internal.

## Issue 7: The catalog's NonIdempotentDirectedPair Coverage row depends on a derived `emission_order` not formally registered as a scaffolding clause
Reason: The chain-index function is already implicitly supplied by T10a.7 (EnumerationInjectivity, ASN-0034) plus the per-document link sub-allocator chain scaffolding; naming it as an additional scaffolding clause and deriving `emission_order` from it is internal restructuring of citations already present.

## Issue 8: The framework's effective-wp derivation forward-references Lemma RetractionTargetNotOnChain
Reason: Pure structural reorganization — move the lemma before the wp derivation or add a forward-reference marker. No new content required; the lemma's proof already exists in the ASN.
