# Review of ASN-0091

## REVISE

### Issue 1: Foundation invariant discharge is incomplete in the abstract narrative
**ASN-0091, "REARRANGE as Vstream-Only Operation"**: "R-SP (RearrangeSufficientPrecondition) discharges RA-adm with respect to the ASN-0036 foundation invariants at the cut-sequence level... The ASN-0047 extended invariants — S3★ (generalised referential integrity), S3★-aux (subspace exhaustiveness), CL-OWN (link-subspace ownership), CL-UNIQ (link-subspace position uniqueness), and P4★ (content-subspace provenance bound) — lie outside R-SP's named scope and are discharged separately by REARRANGE_K's structural properties."

**Problem**: The narrative discharges ASN-0036 invariants via R-SP and five named ASN-0047 extended invariants explicitly. But several foundation invariants from the ExtendedReachableStateInvariants list lie outside both categories: P6 (ExistentialCoherence), P7 (ProvenanceGrounding), P7a (ProvenanceCoverage), P8 (EntityHierarchy), P4a (HistoricalFidelity), NodeLineage from ASN-0047; L0, L1, L1a, L1b, L1c, L3, L14, L-fin, L12 from ASN-0093/ASN-0047; C0, C1, C1b, C1c, C2, C-fin from ASN-0093; P0, P1, P2, P3 from ASN-0047. RA-adm requires each to be preserved at Σ', so each needs discharge. Most are trivially preserved by RA-frame (which fixes C, L, E, R, and dom(M) verbatim), but the ASN's narrative doesn't explicitly state this, leaving the reader to infer it.

**Required**: After the explicit discharge of S3★, S3★-aux, CL-OWN, CL-UNIQ, P4★, add: "All remaining foundation invariants — those depending only on Σ.C, Σ.L, Σ.E, Σ.R, or dom(Σ.M) — are trivially preserved across REARRANGE, since RA-frame fixes each of these components verbatim. In particular, P0, P1, P2, P3, P6, P7, P7a, P8, P4a, NodeLineage, L0–L14, L12, L-fin, C0–C2, and C-fin hold at Σ' iff they hold at Σ."

### Issue 2: Worked-example admissibility paragraphs do not enumerate all foundation invariants
**ASN-0091, "Worked Example" and "Worked Example — 4-cut Swap"**: Both admissibility paragraphs enumerate S2, S8a, S8-depth, S3★, D-CTG★, D-MIN★, D-SEQ★, S3★-aux, CL-OWN, CL-UNIQ, P4★.

**Problem**: The enumeration parallels the gap in Issue 1 at the worked-example level. Foundation invariants P0–P3, P6, P7, P7a, P8, P4a, NodeLineage, the link-store invariants (L0–L14, L12, L-fin), and content-store invariants (C0–C2, C-fin) are not addressed in the worked example's concrete admissibility verification. A claim of "every foundation invariant holds at Σ'" requires either explicit enumeration or an explicit closure statement.

**Required**: Add to each worked example's admissibility paragraph a closing sentence: "All other foundation invariants — P0, P1, P2, P3, P6, P7, P7a, P8, P4a, NodeLineage, L0–L14, L12, L-fin, C0–C2, C-fin — depend only on state components (Σ.C, Σ.L, Σ.E, Σ.R, dom(Σ.M)) preserved verbatim by RA-frame and so hold at Σ' by direct frame inheritance."

### Issue 3: S2 (functionality) of Σ'.M(d) is verified by concrete inspection but not derived at the abstract level
**ASN-0091, "REARRANGE as Vstream-Only Operation"** and **"Worked Example" admissibility**: At the abstract level, the ASN doesn't explicitly establish that Σ'.M(d) is a partial function (S2). In the worked examples, S2 is checked by direct inspection of the displayed map.

**Problem**: S2 is a foundation invariant that REARRANGE must preserve. For the abstract class, the argument is direct — π is a bijection (RA-π), and Σ'.M(d)(π(v)) = Σ.M(d)(v) is determined by Σ.M(d) (a function) and the unique pre-image π⁻¹(v') (single-valued by injectivity). The ASN doesn't state this. Without an abstract derivation, the worked-example inspection is the only basis, which doesn't generalize.

**Required**: Add a brief paragraph at the abstract level: "S2 (functionality of M'(d)) holds at Σ': by π's injectivity, each v' ∈ dom(Σ'.M(d)) = dom(Σ.M(d)) is the image of a unique v = π⁻¹(v') ∈ dom(Σ.M(d)); RA-π then assigns Σ'.M(d)(v') = Σ.M(d)(v), a function value determined uniquely by v', so Σ'.M(d) is a partial function."

### Issue 4: RE-eq witness's "applies symmetrically" wording is misleading
**ASN-0091, "Run Decomposition Is Not Invariant", equality witness**: "The maximal runs are ([1, 1], c, 1) and ([1, 2], a, 1) — again two singletons, since c + 1 ≠ a (the chain-structural argument applies symmetrically)."

**Problem**: The condition `c + 1 ≠ a` was already established in the pre-state argument ("neither `a + 1 = c` nor `c + 1 = a` can hold"). The parenthetical "(the chain-structural argument applies symmetrically)" is misleading: the post-state check isn't symmetric to anything, and the relevant fact `c + 1 ≠ a` is a state-independent structural property of `c` and `a` (both being chain elements from distinct sub-allocator chains).

**Required**: Replace the parenthetical with: "(the structural fact `c + 1 ≠ a` established above is state-independent — a property of `c` and `a` as chain elements — and carries directly into the post-state context.)"

## OUT_OF_SCOPE

### Topic 1: Link-subspace rearrangement semantics
**Why out of scope**: The ASN explicitly defers this in its Open Questions: "What semantics, if any, should rearrangement carry on the link subspace, and what invariants would such an operation be required to preserve?"

### Topic 2: Upper bound on fragmentation cardinality increase
**Why out of scope**: The ASN's Open Questions defers this: "What upper bound, if any, can be placed on the increase in maximal-run-decomposition cardinality from a single rearrangement invocation?"

### Topic 3: Completeness of cut-sequence rearrangements
**Why out of scope**: The ASN's Open Questions defers: "Can every bijection of dom(M(d)) that preserves the arrangement well-formedness invariants be realized by a finite composition of cut-sequence rearrangements?"

### Topic 4: Observational equivalence at the link-discoverability level
**Why out of scope**: The ASN's Open Questions defers: "Under what conditions are two distinct rearrangement transitions observationally equivalent at the level of link discoverability rather than at the level of arrangement equality?"

### Topic 5: Cross-document transclusion with cut splits
**Why out of scope**: The ASN's Open Questions defers: "What guarantees must rearrangement preserve about cross-document transclusion when a cut splits a span transcluded from the same source document into two non-contiguous pieces?" The current RE-trans handles preservation across rearrangement; the cut-induced split semantics for transclusion is a future ASN.

VERDICT: REVISE
