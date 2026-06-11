# Review of ASN-0115

This revision is in strong shape. The Confinement lemma now carries a complete T5-based proof; the deep-case override argument is closed in both sub-cases (`m_S(d) < m−1` via the length bound, `m_S(d) = m−1` via the equal-length prefix collapse and T1 case (ii)); R7's case analysis covers the non-empty-restriction/override-fails-identically corner explicitly; R8's link-vacuity is properly discharged through CL-OWN + CL-UNIQ; and the four worked instances verify the claims they cite, with arithmetic that checks out (I verified the R6 instance — `reach = [1,7]`, slice `{[1,2]…[1,6]}`, `act = {[1,2],[1,3],[1,4]}` — and the R11 fork/contract instance against the K.μ⁻ frame). I found one remaining defect, in a claim statement rather than a proof.

## REVISE

### Issue 1: R6's claim statement uses `m_S` on a domain where it is undefined

**ASN-0115, R6 (SilentGapFiltering)**: "Moreover, for a depth-compatible `ρⱼ`, restricted to the depth-`m_S`, subspace-`S` slice of `⟦σⱼ⟧` — the only named positions the arrangement can bind — the unbound portion never falls as an interior hole within the subspace's contiguous active range…" (likewise the claims-table row: "for a depth-compatible spec the gap is a terminal overrun past the bound frontier, never an interior hole in the bindable slice").

**Problem**: Depth-compatibility is the disjunction `V_S(d) = ∅ ∨ #s = m_S(d)`, and `m_S(d)` is well-defined only while `V_S(d) ≠ ∅` (ASN-0047). So the moreover-clause's hypothesis ("for a depth-compatible `ρⱼ`") includes the `V_S(d) = ∅` branch, on which "the depth-`m_S` slice" and "the subspace's contiguous active range" reference an undefined symbol. The ASN holds itself to exactly this standard one section earlier — the `depthcompat` definition is annotated "well-formed because the disjunction guards `m_S(d)`" — and the body's case analysis is careful (it disposes of `V_S(d) = ∅` *before* introducing the slice machinery). Only the boxed statement and the table row fail to carry the guard.

**Required**: Either (a) guard the moreover-clause with `V_S(d) ≠ ∅` and note that the `V_S(d) = ∅` case is already covered by the empty-active-range half of the claim, or (b) state the slice at depth `#s` — which equals `m_S(d)` in the only depth-compatible branch where bound positions exist — making the statement well-formed on its whole domain with no case split. Apply the same fix to the claims-table R6 row.

## OUT_OF_SCOPE

### Topic 1: Gap localization and per-spec delimiting of the delivered stream
R6 establishes that gaps are signalled structurally, by absence. But the delivery is a flat concatenation whose items carry neither their V-positions nor per-spec boundaries, so a caller can detect an aggregate shortfall yet cannot, from the output alone, attribute a gap to a particular spec or position. Whether the protocol must provide delimiters or position annotations is wire-format/result-structure territory.
**Why out of scope**: This is a protocol-encoding question adjacent to the ASN's own first open question (inline provenance); the abstract delivery semantics defined here is complete without it.

### Topic 2: Error semantics for ill-formed requests
The operation is partial: a spec naming an unallocated document (`d ∉ dom(Σ.M)`) or carrying a non-ordinal span falls outside the V-spec preconditions, and the ASN deliberately does not say what the operation does there (R6 marks the allocation boundary explicitly).
**Why out of scope**: The ASN's second open question already names this; failure-vs-partial-delivery policy is a distinct future obligation, not an error in the defined domain.

The anti-bloat patterns flagged for this note were checked specifically: I found no axiom-rationale sub-paragraphs, no downstream-consumer inventories, no repeated deferrals to a common downstream location, and no paragraph analyzing a case its carrier excludes (the off-`{s_C, s_L}` subspace paragraph analyzes a case the preconditions deliberately admit, which is legitimate). The force-empty rationale paragraph states the "vacuum" point with mild redundancy but each sentence carries distinct content (discontinuity example, design verdict, deep-case proof); it does not rise to a finding.

VERDICT: REVISE
