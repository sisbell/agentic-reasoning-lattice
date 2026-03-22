# Review of ASN-0072

## REVISE

(none)

## OUT_OF_SCOPE

### Topic 1: Link-subspace mapping injectivity
K.μ⁺_L does not prevent the same link ℓ from being arranged at multiple V-positions within the same document. No invariant asserts or denies link-subspace injectivity. All stated invariants are preserved with duplicates (S2 allows non-injective arrangements, CL-OWN only checks origin), so no correctness issue exists in this ASN. But Nelson's "permanent order of arrival" semantics suggests each link occupies exactly one position — a uniqueness invariant, if desired, belongs in a future ASN on link-subspace semantics.
**Why out of scope**: This is a design constraint on link-subspace structure, not an error in the transition framework defined here.

### Topic 2: Endset referential integrity
K.λ creates a link with endsets (F, G, Θ) ∈ Endset = 𝒫_fin(Span). No precondition requires the spans within endsets to reference addresses in dom(C). Whether link endsets must reference existing content — or may reference content that does not yet exist or resides in another document — is a semantic question about link validity.
**Why out of scope**: Endset referential integrity is a link-semantic property, not a state-transition property. This ASN correctly defines the structural framework; constraints on endset targets belong in a future ASN on link semantics.

### Topic 3: Link withdrawal mechanism
The ASN correctly identifies that D-CTG and link-subspace fixity constrain link-subspace contractions to suffix truncations, and that Nelson's design suggests an inactive-status mechanism rather than arrangement removal. The precise withdrawal invariants are explicitly deferred as an open question.
**Why out of scope**: The ASN acknowledges this as future work. The transition framework is complete without it — K.μ⁻ applied to the link subspace is structurally valid under the stated constraints.

VERDICT: CONVERGED
