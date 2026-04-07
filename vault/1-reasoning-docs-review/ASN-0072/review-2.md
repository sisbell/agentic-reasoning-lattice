# Review of ASN-0072

## REVISE

### Issue 1: s_C ≥ 1 derivation cites wrong source
**ASN-0072, Link Store: Restated Definitions (SC-NEQ)**: "We note that `s_C ≥ 1` follows from S8a (all V-position components strictly positive)"
**Problem**: S8a is a guarded quantifier `(A v ∈ dom(M(d)) : v₁ ≥ 1 : ...)` — it tells you properties of V-positions *when* v₁ ≥ 1, but does not establish that content-subspace V-positions have v₁ ≥ 1 in the first place. The implication direction is reversed: S8a's applicability to content V-positions *follows from* s_C ≥ 1, not the other way around. The correct derivation parallels the s_L ≥ 1 argument given in the same sentence: content I-addresses are element-level (S7b, zeros = 3), and T4 requires element-field components to be strictly positive, so fields(a).E₁ = s_C > 0.
**Required**: Replace "follows from S8a" with "follows from S7b + T4" (or spell out the derivation: content I-addresses are element-level by S7b; by T4, element-field components are strictly positive; therefore s_C ≥ 1). The same derivation pattern used for s_L ≥ 1 applies identically to s_C.

### Issue 2: ValidComposite not formally restated for the extended state
**ASN-0072, Scoped Coupling Constraints**: "The coupling constraints for valid composites in the extended state Σ = (C, L, E, M, R) are J0, J1★, J1'★."
**Problem**: ASN-0047 formally defines ValidComposite with coupling constraints J0, J1, J1'. This ASN replaces J1/J1' with J1★/J1'★ and adds K.λ and K.μ⁺_L to the elementary transition set, but does not provide a formal definition block for the extended ValidComposite. The prose is unambiguous, but the statement registry has no entry for the amended definition, creating a gap: a reader checking the registry for "what defines a valid composite in the extended state" finds J1★ and J1'★ individually but not the composite definition that binds them.
**Required**: Add a formal definition block (ValidComposite★ or "ValidComposite, amended") that explicitly states: a composite in the extended state is valid iff each elementary step satisfies its precondition at the intermediate state, and J0, J1★, J1'★ hold for the composite. Add corresponding entry to the statement registry.

## OUT_OF_SCOPE

### Topic 1: Endset referential integrity
K.λ requires (F, G, Θ) ∈ Link (well-formed endsets) but imposes no constraint on whether the spans within endsets reference addresses in dom(C). Combined with L12 (link immutability), a link created with endsets pointing to non-existent content is permanently unresolvable.
**Why out of scope**: Endset grounding is a semantic constraint on link usage, not a structural property of the transition framework. This ASN correctly defines the mechanics; a future ASN on link semantics would add referential constraints on endset targets.

### Topic 2: Link withdrawal mechanism
The ASN correctly identifies that link-subspace contractions via K.μ⁻ are limited to suffix truncations (D-CTG + link-subspace fixity) and that Nelson's design suggests an inactive-status mechanism rather than arrangement removal.
**Why out of scope**: Explicitly deferred as an open question in the ASN. The transition framework supports the structural constraints; the withdrawal semantics require separate specification.

VERDICT: REVISE
