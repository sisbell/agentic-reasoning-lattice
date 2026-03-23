# Review of ASN-0043

## REVISE

(none)

## OUT_OF_SCOPE

### Topic 1: Link-arrangement integration (link V-positions under Σ.M)
**Why out of scope**: The ASN correctly derives that S3 + L0 entails no arrangement can map a V-position to a link address, and explicitly acknowledges that Gregory's implementation does maintain link V-positions in a dedicated subspace. Reconciling this — extending S3 to accommodate link-subspace mappings, formalizing link visibility and deletion through the arrangement layer — is new model extension, not an error here. The ASN's scope section properly excludes "V-space effects of editing" and "three-layer deletion model."

### Topic 2: Compound link well-formedness
**Why out of scope**: L13 establishes that link-to-link references are structurally valid, but imposes no constraints on the resulting graph (cycles, self-reference, depth bounds). Whether compound link structures need well-formedness invariants is a design question for a future ASN, not a gap in the ontology.

### Topic 3: Coverage-based endset equivalence
**Why out of scope**: L8 defines type matching by span-set equality, meaning two endsets with identical coverage but different span decompositions are distinct types. The ASN explicitly flags this as an open question. A future ASN on query semantics or span normalization would address when coverage equivalence should replace span-set equality.

VERDICT: CONVERGED
