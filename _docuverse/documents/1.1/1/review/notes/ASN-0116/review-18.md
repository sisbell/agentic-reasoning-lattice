# Review of ASN-0116

This is a mature, carefully argued note. The two-layer decomposition is sound, the I3-transfer arguments (gapped arrangement + block-disjointness) are rigorous, the composite-over-K-vocabulary construction discharges each intermediate precondition, and the worked example exercises P0/P1/P4/P5/P6 plus all three boundaries (append, empty, front). The remaining issues are a frame-completeness gap and anti-bloat patterns the `review-mode.anti-bloat` classifier directs me to surface.

## REVISE

### Issue 1: INSERT's Frame contract omits the link store and entity set
**ASN-0116, Operation Frame (F-SUB, F-DOC)**: the Frame section lists only `(F-SUB)` and `(F-DOC)` — both about `M`. Content frame lives in I-IMM/P2, provenance in I-PROV. But the operation works in the extended state `Σ = (C, L, E, M, R)`, and there is no frame clause asserting `Σ'.L = Σ.L` or `Σ'.E = Σ.E`.
**Problem**: The post-state's discharge of ExtendedReachableStateInvariants (ASN-0047) inherits the link per-state invariants (L0, L1, L1a, L1c, L3, L14, L-fin, CL-OWN, CL-UNIQ) and entity invariants (S7d, NodeLineage, ActivatedEmission) **only** by frame `L' = L`, `E' = E`. P5 (DocumentIsolation) and the P4 link-survival argument likewise lean on `Σ.L` being untouched. The fact is asserted only in narrative prose ("beyond C and M the one further component INSERT touches is the provenance relation Σ.R"), not in the operation's Frame contract.
**Required**: Promote `L' = L` and `E' = E` to explicit Frame clauses, so the operation contract is self-contained and the per-state link/entity invariants have a stated premise.

### Issue 2: Redundant meta-framing around P0
**ASN-0116, allocation section**: "We record the freshness-and-distinctness guarantee the K.α composition carries, **since it is the load-bearing fact the rest of the argument leans on**. **It is not new content**: its freshness half is K.α's FirstEmission/SubsequentEmissionFreshness, and its value-independence half is S4..."
**Problem**: The decomposition (K.α freshness + S4) is then restated verbatim in the claim itself: "**P0 (OriginIdentity) (restatement of K.α freshness + S4)**". The paragraph and the claim's parenthetical say the same thing twice. The clauses "since it is the load-bearing fact the rest of the argument leans on" and "It is not new content:" are provenance-of-claim chatter (classifying the claim's role/novelty) rather than advancing its content.
**Required**: Drop the meta-framing; let the P0 claim's parenthetical carry the decomposition once.

### Issue 3: Coupling-mandatoriness restated across sections
**ASN-0116, provenance discharge**: "**These are not optional**: ASN-0047's ValidComposite clause (2) declares a composite that meets every transition precondition but violates a coupling constraint to be not a valid composite."
**Problem**: The same consequence is already stated in the composite section: "A composite that satisfies clause (1) but violates clause (2) is not a valid composite." Two paragraphs in different sections assert the same fact; the "These are not optional:" prefix is defensive emphasis.
**Required**: State the clause-2 consequence once (in the composite section, where it is established) and cite it, rather than re-asserting it with emphasis at the use site.

## OUT_OF_SCOPE

### Topic 1: Insertion at a transcluded/shared position
The first Open Question (insertion point shared by transclusion with another document) is correctly deferred — transclusion (COPY / ASN-0118) is out of scope.

### Topic 2: Concurrent insertions and freshness without a serializing authority
The second Open Question is legitimately future territory (replication/BEBE), not an error here.

VERDICT: REVISE
