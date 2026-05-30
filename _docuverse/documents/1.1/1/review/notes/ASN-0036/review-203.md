# Review of ASN-0036

I checked the major proofs (S1, S4, S5, S7, S8, OrdShiftHom, D-CTG-depth, D-SEQ) line by line, the boundary cases (empty arrangement, depth 2, depth ≥ 3, run boundaries), and the anti-bloat patterns flagged by the note's classifier.

## REVISE

None.

The mathematics is sound and the proofs are complete:

- **S8 (correspondence-run partition)** — the lockstep-successor `succ` is correctly shown to be a within-subspace partial function (OrdShiftHom + S8-depth), injective (TS2 at common depth, with `#u = #u'` derived from `#shift(u,1)=#w`), and acyclic (TS4 + T1 irreflexivity). The finite in/out-degree-≤1 acyclic-graph argument legitimately yields the disjoint-path decomposition, and the displacement-identity induction correctly isolates the `i=0` case (where TS3's `n₁≥1` precondition fails) from `i≥1`. Partition coverage, disjointness, and uniqueness are each discharged.
- **D-CTG-depth / D-SEQ** — the infinite-intermediate construction at a disagreement position `j ∈ [2, m−1]` correctly verifies `u < w < x`, S8a on `w`, and the T0(a)-driven infinite distinct-witness sequence contradicting S8-fin. The `j = m−1` empty-range subcase is handled.
- **S5** — the empty-transition-system device making S0/S1 vacuously true is load-bearing (the claim is about models of S0–S3, not the state-level fragment), and both cross-document and within-document constructions are exhibited.
- Boundary cases are present: vacuous empty state, depth-2 finite block, depth-≥3 reduction, and the run-boundary at the transclusion/append seam in the worked example (Σ₂ Run A forward-maximality where images jump `…1.5 → …2.1`).
- Concrete grounding is strong — the Σ₀–Σ₃ lifecycle exercises S0, S3, S5, S7, S8, and D-SEQ against specific tumblers, plus explicit contiguity-violation examples at depth 2 and ≥ 3.
- Cross-ASN references are all to ASN-0034 (foundation); no invented notation, no non-foundation references.

On anti-bloat: the residual restatements I scrutinized are load-bearing rather than noise. The per-component restatement of S8a establishes the `vᵢ ≥ 1` equivalence that OrdShiftHom, D-CTG-depth, and D-SEQ all cite; "any correct implementation must satisfy this constraint" (S8-depth) asserts the abstractness criterion the spec requires, not filler. Nothing forces a precise reader to skip past meta-prose to follow a claim.

## OUT_OF_SCOPE

### Topic 1: Contiguity in non-text subspaces
D-CTG, D-MIN, D-SEQ are stated only for the text subspace (S = 1). Link-subspace (S = 2) position conventions are correctly deferred — links are out of scope.

### Topic 2: Operation preservation of D-CTG/D-MIN/S2
Whether INSERT/DELETE/COPY/REARRANGE preserve the contiguity invariants (and the insertion-at-occupied-position case) is correctly an operations-layer obligation, flagged in Open Questions.

### Topic 3: Subspace alignment (v₁ vs the I-address's element-field subspace)
No state invariant ties `subspace(v)` to the first element-field component of `M(d)(v)`. The note correctly routes this to the operations layer as a preservation obligation.

### Topic 4: `Val` constraints and sharing-inverse computability
Heterogeneous content typing and the cost bound for the reverse `address → referencing-documents` query are genuinely future territory.

VERDICT: CONVERGED
