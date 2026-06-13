# Channel Assignment — ASN-0125 review-24

**Date:** 2026-06-13 16:32

## Issue 1: "No canonical selector exists" is undefined, overclaimed relative to its own argument, and in tension with EL13
Reason: The fix is internal — the conflict is between EL14(d) and EL13, both already in the note, and the material to resolve it is present: EL13 already supplies the distinction (T1-least tie-break is Σ-definable but "ranks namespaces, not times") and the cross-home commutation symmetry that any temporal selector must violate. Defining "canonical" as a Σ-definable single-valued selector respecting assertion/temporal order (equivalently, invariant under EL13's cross-home symmetry) and proving its non-existence — or weakening the headline to "no temporal/recency-respecting selector is state-definable" — is derivable from the ASN's own content. No design-intent or implementation fact is in question.

## Issue 2: Df-LAY restates its own operation-set definition (anti-bloat)
Reason: Pure editorial redundancy verifiable from the Df-LAY paragraph itself — the operation set, the confinement clause on bare `K.λ`, and the positive discipline commitment already exclude the named cases, so the sentence adds no constraint. Dropping it requires no design intent or implementation evidence.
