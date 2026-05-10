# Review of ASN-0047

## REVISE

### Issue 1: K.μ~ empty content subspace case — compressed multi-step argument

**ASN-0047, K.μ~ definition (Elementary transitions section)**: "link-subspace fixity forces π to fix every position: K.μ⁺ (amended) cannot create link-subspace V-positions, so π must map each link-subspace position to a link-subspace position, and since no content-subspace positions exist to redistribute, π is the identity."

**Problem**: This compresses a multi-step argument into one sentence, and the stated reasoning has a gap. The conclusion (M'(d) = M(d), zero elementary steps) is correct, but the intermediate step — "K.μ⁺ cannot create link-subspace V-positions, *so* π must map each link-subspace position to a link-subspace position" — does not follow from the K.μ⁺ amendment alone. It requires S3★ + L14 + SC-NEQ: if π mapped a link-subspace position v to a content-subspace position π(v), then M'(d)(π(v)) = M(d)(v) ∈ dom(L), but S3★ requires M'(d)(π(v)) ∈ dom(C) for content-subspace π(v), contradicting dom(C) ∩ dom(L) = ∅. This is the same argument used in the S3★ analysis for dom_C ≠ ∅, but it is never stated for the dom_C = ∅ case.

Furthermore, "no content-subspace positions exist to redistribute, π is the identity" skips the cardinality argument: π restricted to dom_L(M(d)) injects into dom_L(M'(d)); K.μ⁺ cannot create link-subspace positions, so |dom_L(M'(d))| ≤ |dom_L(M(d))| − r; the injection forces r = 0; since dom_C = ∅, K.μ⁻ has zero positions to remove; the strict-subset requirement is unsatisfiable; K.μ⁻ cannot fire; therefore zero elementary steps.

The formal proof in the S3★ analysis and ExtendedReachableStateInvariants theorem covers only the dom_C ≠ ∅ case. The dom_C = ∅ case is left to this compressed informal argument. Since these are structurally different situations (non-trivial decomposition vs zero-step decomposition), both need explicit treatment.

**Required**: Expand the dom_C = ∅ argument to explicitly invoke S3★ + L14 (to establish π maps link to link), state the cardinality consequence (r = 0), and derive the zero-step conclusion from the strict-subset unsatisfiability of K.μ⁻. Five sentences would suffice — the reasoning parallels the dom_C ≠ ∅ proof in simplified form.

## OUT_OF_SCOPE

### Topic 1: Endset referential integrity for link values
**Why out of scope**: K.λ's precondition requires `(F, G, Θ) ∈ Link` — syntactically well-formed endsets — but imposes no constraint on whether the spans in F, G, Θ reference existing content in dom(C). A link can be created whose endsets point to non-existent I-addresses. An endset referential integrity invariant (analogous to S3★ for arrangements) belongs in a future link semantics ASN. The ASN already defers "endset semantics" to a separate analysis and lists a related open question about permanence properties for content participating in link endsets.

VERDICT: REVISE
