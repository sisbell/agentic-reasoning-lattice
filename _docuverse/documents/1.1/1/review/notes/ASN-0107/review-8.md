# Review of ASN-0107

## REVISE

### Issue 1: A2 invokes document "subspaces" that the model does not define
**ASN-0107, "How the Count Changes: Content Added" (A2)**: "take `W₂` and `W₃` to range over the *entire* to- and type-subspaces of `d_new`, so `Q₂(Σ)` and `Q₃(Σ)` resolve to the full sets of I-addresses `d_new` currently arranges in those slots."
**Problem**: There is no "to-subspace" or "type-subspace" of a document. By SubspaceConventionAxiom (ASN-0093/0047) a document's arrangement has exactly two V-subspaces — content (`s_C`) and link (`s_L`). The from/to/type distinction is a property of the *link's slots* (`e₁,e₂,e₃`), not of the querying document's V-position layout. A query region `Wᵢ` is just a set of V-positions whose image is `Qᵢ(Σ)`; nothing in the model partitions a document's positions into "to" and "type" regions. The phrase conflates link-slot index with document-subspace identifier and so describes an object that does not exist.
**Required**: Restate the widening in terms the model supplies: `W₂` and `W₃` are query V-regions (each drawn from `d_new`'s content- and/or link-subspace positions) whose resolved images `Q₂(Σ), Q₃(Σ)` are the I-addresses `d_new` currently arranges at those positions. Keep the slot/region distinction explicit and drop the "to-/type-subspace" vocabulary.

### Issue 2: The worked example's type position violates referential integrity
**ASN-0107, "A Worked Instance"**: "place the type position in the link subspace (`s_L = 2`), `v_τ = [2,1] ↦ τ`" with `τ` introduced as "a type address `τ` (any tumbler the type endsets name)."
**Problem**: With `v_τ` a link-subspace V-position, S3★ (GeneralizedReferentialIntegrity, ASN-0047) forces `Σ.M(d)(v_τ) = τ ∈ dom(Σ.L)`, and CL-OWN forces `origin(τ) = d` — i.e. `τ` must be one of `d`'s *own* links, not an arbitrary classifying address. The example never establishes `τ ∈ dom(Σ.L)` nor `origin(τ) = d`; it treats `τ` as a free type tumbler. The example is the ASN's only concrete witness for the discovery-count claims (D2 contraction/extension/reorder), and it relies on `v_τ` being a valid, untouched arrangement entry, so its incoherence with the foundation invariants it implicitly uses is load-bearing for the demonstration.
**Required**: Either declare `τ` as a link in `dom(Σ.L)` with `origin(τ) = d` (and note it is a link-to-link type reference, admissible by L4(c)), or place the type query position in the content subspace and adjust the K.μ⁻ retention so it survives — and discharge S3★/CL-OWN explicitly for whichever choice is made.

## OUT_OF_SCOPE

### Topic 1: Independently-anchored, separately-evolving query parts
**Why out of scope**: The first open question (three parts anchored to different documents' arrangements that evolve separately) is genuinely new territory — the present ASN fixes a single resolution anchoring per request. Correctly deferred.

### Topic 2: Count-versus-retrieval cardinality agreement
**Why out of scope**: Relating `num` to the cardinality returned by FINDLINKS/ASN-0099 depends on the retrieval operation, which the scope excludes. Appropriately left as an open question.

VERDICT: REVISE
