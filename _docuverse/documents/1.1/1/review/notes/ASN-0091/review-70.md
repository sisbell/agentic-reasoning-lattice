# Review of ASN-0091

The mathematical core is sound. I checked the three run-cardinality witnesses (fragmentation, coalescence, equality), the four worked examples, the ChainDisjointAdjacency lemma, the RE-ran/RE-μ derivations, and the K.μ~ admissibility discharges (i)–(v) — all compute correctly and the case analyses are complete. Boundary cases (empty arrangement, identity, shared I-addresses, interior cuts, first/last position) are covered. No correctness gap found.

The issues below are anti-bloat and precision, consistent with this note's `review-mode.anti-bloat` classifier.

## REVISE

### Issue 1: RA-adm discharge restates the full foundation invariant list verbatim
**ASN-0091, "Clause Correspondences and Per-Invariant Discharges"**: "ASN-0047's ExtendedReachableStateInvariants is the explicit form of this implication, giving `reachable(Σ') ⟹ invariants(Σ')` for the enumerated per-state foundation list — S2, S3★, S3★-aux, S4, S7a, S7b, S7d, S8a, S8-fin, S8-depth, S8★, D-CTG★, D-MIN★, D-SEQ★, C1b, C1c, C-fin, P6, P7, P8, NodeLineage, ActivatedEmission, L0–L-fin, CL-OWN, CL-UNIQ — and, at composite boundaries, P4★, P4a, P7a."
**Problem**: The argument needs exactly three steps — ExtendedReachableStateInvariants gives all per-state invariants at any reachable state; Σ' is reachable; therefore RA-adm holds. Re-enumerating the entire invariant list (already fixed in ASN-0047's theorem) adds nothing to the reasoning; it is foundation content copied into a structural slot. The trailing sentence on S7 and the ASN-0093 substrate predicates (M0, C1, C2) compounds the restatement.
**Required**: Cite ExtendedReachableStateInvariants by name and conclude RA-adm from reachability of Σ'. Drop the verbatim list.

### Issue 2: RE-ran's two-case uniformity is re-derived at each downstream use site
**ASN-0091, "Discoverability Is Preserved"** and **"Cross-Document Transclusion Preserved"**: in the first — "RE-ran (in its generalised form derived above — target case by π-bijectivity, non-target cases by RA-frame's other-document clause) is uniform over all d ∈ dom(Σ.M)"; in the second — "By RE-ran applied at d (uniform over all d ∈ dom(Σ.M) per its generalised statement — for the target case d = d_tgt, by π-bijectivity; for any non-target document d ≠ d_tgt, by RA-frame's other-document clause, which fixes Σ'.M(d) = Σ.M(d) entirely and so preserves the range trivially)".
**Problem**: RE-ran is already stated and proved uniformly for every `d' ∈ dom(Σ.M)` in "Domain Stability and Range Invariance." These two parenthetical re-justifications say the same thing (the target/non-target provenance) in different words at the point of use. Once the uniform claim is established, downstream citations need only name RE-ran.
**Required**: Replace both parentheticals with a bare citation of RE-ran. The provenance lives at the claim's derivation, not at every consumer.

### Issue 3: Empty-case "every RE-* claim holds vacuously" over-generalises its own justification
**ASN-0091, "REARRANGE as Vstream-Only Operation"**: "every RE-* claim holds vacuously (ranges, projections, and multiplicities are all over the empty set)".
**Problem**: The parenthetical justification covers only the M(d)-indexed claims (RE-ran, RE-proj, RE-μ). The component-global claims — RE-C, RE-L, RE-R, RE-origin, RE-cov — do hold in the empty case, but by RA-frame, not vacuously over an empty set (`Σ.C` may be arbitrarily large). The blanket "every RE-* claim holds vacuously" attaches a justification to claims it does not cover.
**Required**: Scope the "vacuous" justification to the arrangement-indexed claims, and note the component-global claims hold by RA-frame.

### Issue 4: Defensive scope-justification inside ChainDisjointAdjacency
**ASN-0091, "Run Decomposition Is Not Invariant", ChainDisjointAdjacency**: "Domain disjointness is established without appeal to any prefix-positional disagreement, so the conclusion holds uniformly across all length cases."
**Problem**: The proof concludes `x+1 ≠ y` from domain disjointness; it is already complete at that point. This sentence pre-empts a length-case objection that the proof never raised — defensive meta-prose explaining why no case split is needed rather than advancing the lemma.
**Required**: Delete the sentence.

## OUT_OF_SCOPE

### Topic 1: Link-subspace rearrangement semantics
The Open Questions raise what invariants a link-subspace REARRANGE would preserve. REARRANGE_K acts only on `s_C` (CS3 forces `S = 1`), and clause (v) fixes the link subspace pointwise. A link-subspace reordering operation is new territory, correctly deferred.

### Topic 2: Source-span reconstitution after a split transclusion
RE-trans explicitly leaves open whether two fragments of a same-source transclusion jointly reconstitute the original span. This belongs to a future ASN on transclusion geometry, not a defect here.

VERDICT: REVISE
