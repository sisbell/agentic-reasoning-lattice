# Review of ASN-0036

## REVISE

*No items.*

## OUT_OF_SCOPE

### Topic 1: Contiguity of V-position domains
The ASN uses "virtual byte stream" and "readable sequence" language that implies contiguity of `dom(M(d))` within a subspace, but no formal property requires it. Whether DELETE creates gaps or re-indexes remaining positions depends on operation semantics, which are properly excluded from this ASN's scope.
**Why out of scope**: Operation-specific effects (INSERT, DELETE, REARRANGE postconditions) are declared out of scope.

### Topic 2: Multiple text subspaces
S8a allows `v₁ ≥ 1`, admitting subspace identifiers 2, 3, ... beyond the text subspace `v₁ = 1` mentioned in the shared vocabulary. The ontology of subspaces beyond text (1.x) and links (0.x) — media, annotations, etc. — is not addressed.
**Why out of scope**: This is new territory requiring its own definitions, not an error in the current model.

### Topic 3: Maximal run decomposition uniqueness
S8 proves existence of a finite decomposition (via singleton runs) but does not address whether a unique coarsest decomposition exists. Already noted in the ASN's own open questions.
**Why out of scope**: This is arrangement theory that builds on S8 rather than correcting it.

VERDICT: CONVERGED
