# Review of ASN-0100

## REVISE

### Issue 1: Cross-document projection invariance applies single-step lemmas to a multi-step composite without lifting

**ASN-0100, §Verifying the Invariants → Cross-document independence, and §Coverage and link discoverability (INS.proj, d' ≠ d case)**: "project(ℓ, i, d', Σ') = project(ℓ, i, d', Σ) ... by frame M'(d') = M(d') together with LP4 (ArrangementSpecificity; ASN-0098) and LP5 (CrossDocumentIndependence; ASN-0098)."

**Problem**: LP4 and LP5 are stated in ASN-0098 strictly per single transition ("For every transition Σ → Σ'"). INSERT is a composite of `2n+1`/`2n+2` elementary steps. The ASN demonstrates elsewhere that it knows single-step lemmas must be lifted: it invokes LP3★ (MultiStepCoverageInvariance) for coverage, and it traces the `d = d` projection explicitly step-by-step (LP6, LP10, LP9, LP14). The cross-document case receives only a citation of the single-step LP4/LP5, with no chaining or multi-step justification — exactly the "X follows from Y + Z is a claim, not a proof" gap. No "LP4★/LP5★" exists in the foundation, and the Closure schema (★) lifts only membership/value clauses, not set-equality of projections, so the lift is not free.

**Required**: Either chain LP4 across each elementary step explicitly (M(d') is unchanged at every step by each step's cross-document frame, so the projection is invariant at each step and hence across the composite), or give the direct argument (project(ℓ,i,d',·) depends only on the composite-invariant M(d') and on coverage, which LP3★ already fixes). Match the rigor used for the `d = d` case.

### Issue 2: P4a discharge cites a non-boundary internal state as the witness, and misnames the property

**ASN-0100, §Verifying the Invariants → Provenance, and §Atomicity and Canonical Order**: "P4a (HistoricalFidelity; ASN-0047) ... For each new (a_k, d) added by step 4's K.ρ firings, the historical state is the substrate state at the end of step 3, in which a_k ∈ ran(M'(d))."

**Problem**: ASN-0047's P4a (named *TraceWitnessing*, not "HistoricalFidelity") quantifies the witness state over *composite boundaries* — the trace `Σ₀ →* Σ₁ →* … →* Σ_n = Σ`, with `M_k` the arrangement of a boundary state `Σ_k`. "The end of step 3" is an elementary intermediate *interior* to INSERT's final composite; it is not a member of `{Σ₀, …, Σ_n}`, so it is not an admissible P4a witness as defined. The conclusion is still true (the correct witness is `Σ' = Σ_n`, where `a_k` remains in `ran(M'(d))` because step 4's K.ρ frames M), but the cited witness is the wrong referent. The descriptive name "HistoricalFidelity" also diverges from the foundation's "TraceWitnessing" (standard 7).

**Required**: Cite `Σ'` (the composite boundary) as the P4a witness, noting that K.ρ's M-frame keeps `a_k ∈ ran(M'(d))` at `Σ'`. Use the foundation name TraceWitnessing.

## OUT_OF_SCOPE

(none — the COPY contrast, version-chain corollaries, and link-subspace remarks are all explicitly framed as out of scope and used only to fix INSERT's own identity character.)

VERDICT: REVISE
