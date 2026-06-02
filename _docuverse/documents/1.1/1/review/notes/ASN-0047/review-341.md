# Review of ASN-0047

I checked the elementary-transition definitions, the K.μ⁻ equivalence proof, the K.μ~ decomposition (admissibility clauses i–v, K.μ~-FIX, necessity/sufficiency), the D-SEQ★ derivation (both m=2 and m≥3 cases), the J4 fork (k=0 and k=1, duplicate-source multiplicity), the Class (a)/(b) invariant matrices, and the cross-layer derivations (P6, P7, P7a, P4a). The proofs are sound — the case splits are exhaustive, the boundary cases (empty subspace, full clearance, first insertion, duplicate-I-address fork) are handled, and the worked examples exercise the load-bearing postconditions. I found no skipped case, no proof-by-"similarly," and no cross-ASN reference outside the foundation set.

The note carries the `review-mode.anti-bloat` classifier. The findings below are the meta-prose / accretion items it asks me to surface; none touch correctness.

## REVISE

### Issue 1: Non-guarantee deferral paragraph does not advance the argument
**ASN-0047, *Link-subspace ownership* (the "Link V-position permanence" paragraph)**: "K.μ~ clause (v)'s link-subspace fixity binds a single K.μ~ transition only and is not a lifetime guarantee; link *identity* permanence — the address and value of an existing link — is discharged independently of arrangement order on `dom(L)` by L12."

**Problem**: This is a standalone bolded paragraph that states what clause (v) does *not* guarantee and redirects to L12. It introduces no claim, precondition, or step — a reader following the K.μ~ argument skips past it. It is the "defensive justification / non-guarantee" pattern the anti-bloat note flags.

**Required**: Delete it. If the distinction between per-transition link fixity and link-identity permanence is genuinely needed, fold it into clause (v)'s statement as a one-clause parenthetical, not a separate paragraph.

### Issue 2: K.μ⁻ amendment box restates what the elementary K.μ⁻ definition already says
**ASN-0047, *Amendments to existing transitions*, "K.μ⁻ amendment (PerSubspaceScope)"**: "In the extended state, K.μ⁻'s D-CTG / D-MIN postconditions read as the per-subspace forms D-CTG★ / D-MIN★; the contraction shape and its per-subspace strict-contraction clause are as stated at K.μ⁻'s definition."

**Problem**: The elementary K.μ⁻ definition (in *Elementary transitions*) already states its preconditions and derived consequences entirely in star form (S3★, D-CTG★, D-MIN★, D-SEQ★) and already gives the per-subspace constructive contraction shape with the strict-contraction clause. The first sentence of the amendment therefore describes a "D-CTG → D-CTG★" transformation that never needed performing, and the second sentence is a pointer back to the definition it amends. The only non-redundant content is the extended-state frame line (`L' = L`).

**Required**: Reduce the box to the one fact that is actually new in the extended state — the `L' = L` frame clause — or drop it and add `L' = L` directly to K.μ⁻'s elementary frame.

## OUT_OF_SCOPE

None beyond the topics the ASN already routes to its Open Questions (transitive transclusion provenance, renumbering-aware interior link contraction, concurrency/serialization of allocation, node-baptism protocol mechanism). These are correctly deferred, not errors here.

VERDICT: REVISE
