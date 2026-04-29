# Review of ASN-0063

## REVISE

### Issue 1: P4★ preservation argument omits K.μ~ (reordering)

**ASN-0063, "Containment scoping"**: "Existing transitions preserve P4★: K.α, K.δ, K.ρ hold M in frame; K.μ⁺ extends only content-subspace positions (by its amended precondition) and is coupled with K.ρ by J1★; K.μ⁻ contracts dom(M(d)), which can only shrink Contains_C."

**Problem**: K.μ~ is an existing transition not listed. The claim "existing transitions preserve P4★" is not fully substantiated. The missing case is non-trivial: K.μ~ creates a bijection π : dom(M(d)) → dom(M'(d)), and one must show that π maps content-subspace positions to content-subspace positions (so the multiset of content-subspace I-addresses is preserved and Contains_C is unchanged). The argument *is* available — the S3★ section proves link-subspace fixity under K.μ~, from which content-subspace fixity of Contains_C follows — but the P4★ paragraph does not connect to that result.

**Required**: Add K.μ~ to the P4★ preservation list with a derivation: "K.μ~: by link-subspace fixity (established in the S3★ analysis above), π maps content-subspace positions to content-subspace positions with values preserved, so Contains_C(Σ') = Contains_C(Σ) ⊆ R = R'."

### Issue 2: K.μ⁺ amendment impact on J4 (ForkComposite) not acknowledged

**ASN-0063, "Extending the Transition Framework"**: "K.μ⁺ is amended with a content-subspace restriction: new V-positions must satisfy subspace(v) = s_C. This complements K.μ⁺_L (defined below), which handles link-subspace extensions exclusively."

**Problem**: J4 (Fork, ASN-0047) is a composite defined as K.δ + K.μ⁺ + K.ρ. The K.μ⁺ amendment restricts K.μ⁺ to content-subspace V-positions. Consequence: when forking a document that has link-subspace mappings, the fork's K.μ⁺ step cannot copy those mappings — it can only populate the new document's content subspace. The forked document receives no link-subspace mappings. The ASN does not acknowledge this behavioral change to an existing composite. Without a statement, the reader cannot determine whether this is by design (links are per-version, not inherited) or an unexamined side effect.

**Required**: State the consequence explicitly: "The amended K.μ⁺ means J4 (Fork) populates only the content subspace of the new document. Link-subspace mappings from the source document are not copied. A mechanism for link inheritance under forking — whether via K.μ⁺_L steps in the fork composite or by other means — is outside this ASN's scope." This closes the gap without requiring the full fork treatment.

## OUT_OF_SCOPE

### Topic 1: Fork and version operations with link-subspace mappings
**Why out of scope**: The ASN's scope section explicitly excludes version creation. The full treatment of how forking, versioning, and version comparison interact with link-subspace arrangements belongs in a version-operations ASN, not here. Issue 2 above asks only for acknowledgment of the impact, not the full design.

### Topic 2: Efficient implementation of the discovery function
**Why out of scope**: The ASN correctly identifies disc as a derived function on system state and leaves implementation (enfilades, index structures) to the implementation layer. Nelson's "inter-indexing mechanisms" (LM 4/41) and the two-dimensional enfilade are mentioned as implementation context, not specification requirements.

### Topic 3: Concurrency model for link allocation
**Why out of scope**: The transition framework (ASN-0047) defines sequential state transitions. Concurrent CREATELINK operations targeting the same home document raise serialization questions that belong in a concurrency/replication ASN, not in the operation definition.

VERDICT: REVISE
