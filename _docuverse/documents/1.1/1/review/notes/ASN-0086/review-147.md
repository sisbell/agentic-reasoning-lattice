# Review of ASN-0086

This note is mature and has clearly converged on its core proofs (R0, R0a, L-ContiguousPrefix, R7a, the Case 2 wp). The proofs I checked in detail are sound. The remaining issues are a framing contradiction, an uncited per-step fact, and some redundancy flagged by the anti-bloat mandate.

## REVISE

### Issue 1: R0a proof header contradicts Case 1's own statement of its dependencies
**ASN-0086, R0a (FlatLinkDomain), proof opening**: "The argument decomposes into two cases on `home(a)` vs. `home(a')`, both discharged by ASN-0093's chain machinery (or, equivalently, by T10a's allocator-disjointness lemmas)."

**Problem**: Case 1 (cross-home) then opens with "We show this case directly from L1's element-level constraint plus L1a's NUDE-prefix `home` projection — no chain machinery is required." The header asserts both cases ride on chain machinery / T10a disjointness; Case 1 explicitly disavows both. A precise reader is told the wrong premise set for half the proof. This is exactly the overclaim-in-a-structural-slot pattern the anti-bloat mandate asks to surface.

**Required**: Rewrite the header to state that Case 1 (cross-home) uses only L1 + L1a (zero-counting), and Case 2 (same-home) uses L-ContiguousPrefix + (UL) + T3 — i.e., the two cases have *different* premise sets.

### Issue 2: R0 first-branch L1c discharge asserts `zeros(d) = 2` without citation, and re-derives a chain ASN-0093 already supplies
**ASN-0086, R0 proof, first-emission branch, L1c discharge**: "...the `k = 2` step acts on `d` (`zeros(d) = 2 ≤ 2`, TA5a's tight bound for `k = 2`)..."

**Problem**: `zeros(d) = 2` is the load-bearing fact that makes the `k = 2` anchor step T4-preserving, but it is stated bare. It holds only because `d ∈ dom(Σ.M)` and M0 (ASN-0093, DocumentTumblerWellFormed) / S7d give `zeros(d) = 2`; the foundation ASNs' own per-step citation convention demands this be named. Separately, the entire first-branch chain `d → inc(d,2) → inc(·,0) → inc(·,1)` re-derives a result FirstEmission + ChainElementT4Validity (ASN-0093) already deliver — that `[d.0.s_L.1]` is the T4-valid first emission of `A_L(d)` — so the L1c discharge could cite ASN-0093 directly instead of reconstructing (and re-justifying T4-preservation at each `k>0` step).

**Required**: Cite M0/S7d for `zeros(d) = 2`. Either replace the re-derived anchor chain with a direct appeal to FirstEmission/ChainElementT4Validity (ASN-0093), or keep it but discharge each `k>0` step's zero-count against an explicitly cited source.

### Issue 3: Acknowledged-alias results padding the result inventory
**ASN-0086, R2 and R4**: "TupleAddressPermanence *(definitional alias of L12, not a result requiring verification)*"; "TupleAddressDisjointness *(definitional alias of SD ... not a result requiring verification)*".

**Problem**: R2 and R4 carry result numbers and full restatements while explicitly discharging "no separate obligation." Combined with R1/R3/R6a being one-line derivations, the numbered "R-series" overstates the note's proof content relative to its genuinely novel obligations (R0, R0a, L-ContiguousPrefix, R7a, wp). The anti-bloat classifier flags "essay content in structural slots."

**Required**: This is a judgment call — if the R-label↔foundation-lemma mapping table is the point, keep the aliases but compress R2/R4 to a single line in the Properties table rather than standalone titled paragraphs. If not, fold the aliases into the prose where they are first consumed.

## OUT_OF_SCOPE

### Topic 1: Invariants between `L_K` and arrangements `Σ.M`
**Why out of scope**: The note correctly scopes itself to `Σ.L` (M2 keeps arrangements empty here). Relational predicates that depend on whether from/to content is *visible* in a document require arrangement-modifying operations this substrate does not yet expose — the note's own first Open Question. A future ASN, not a defect here.

### Topic 2: Elevating the unit-depth retraction discipline to a substrate guarantee
**Why out of scope**: Whether retraction should become a designated K-operation with a shape constraint (vs. remaining a layer convention) is a substrate-design decision the note flags in its Open Questions. Leaving it as a layer commitment is a defensible scoping choice, not an error.

Note on drift: a large fraction of this note re-describes ASN-0043/0093 results, and its one genuinely new construct (active/audit via retraction) is a *layer convention*, not a substrate invariant. I considered META but decline it: the note also proves real substrate-conforming invariants (R0a antichain, depth-2 link addresses) and is self-aware about the convention/substrate boundary. Incomplete framing, not off-track.

VERDICT: REVISE
