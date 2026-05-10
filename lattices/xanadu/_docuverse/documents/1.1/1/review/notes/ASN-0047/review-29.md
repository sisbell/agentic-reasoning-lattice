# Review of ASN-0047

## REVISE

(none)

## OUT_OF_SCOPE

### Topic 1: Version lineage and arrangement transitions
**Why out of scope**: The ASN defines elementary transitions on arrangements but does not specify how the version DAG relates to the sequence of transitions. Versioning is a separate structural concern — this ASN establishes the transition primitives that versions will be built from.

### Topic 2: Subspace preservation under reordering
**Why out of scope**: K.μ~ permits the bijection π to move V-positions across subspace boundaries (changing the first component). Whether reordering must respect subspace membership is a semantic constraint belonging to the operation specifications, not to the elementary transition taxonomy. The ASN correctly identifies this in its open questions.

### Topic 3: Transitive provenance through transclusion chains
**Why out of scope**: J1 records provenance for the immediate document receiving content. When document d₃ transcludes from d₂, which transcluded from d₁, the provenance chain (a, d₁), (a, d₂), (a, d₃) arises from separate composites. The properties of such chains — discoverability, completeness — require analysis beyond the elementary transition model.

### Topic 4: Link endset interaction with arrangement contraction
**Why out of scope**: K.μ⁻ on one document can remove I-addresses that participate in link endsets discoverable from other documents. The interaction between contraction and link discoverability is a cross-document semantic concern that belongs in the link ontology ASN, not here.

VERDICT: CONVERGED
