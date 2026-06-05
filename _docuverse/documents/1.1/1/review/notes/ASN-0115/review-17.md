# Review of ASN-0115

I checked each of R0–R11 against its proof, focused on the boundary conditions a content-delivery query must survive — empty request, empty arrangement, unbound positions, shared addresses, cross-subspace and cross-document assembly, and the deletion-as-contraction asymmetry — and traced every cited invariant back to a reachable-state guarantee.

## What I verified

- **Totality of `item`.** The two-case split is exhaustive on `act` via S3★-aux (case coverage) with per-case S3★ (store membership). Correctly discharged.
- **R6 (no interior hole).** The proof properly restricts to the depth-`m_S`, subspace-`S` bindable slice, uses `act ≠ ∅` to pin the canonical start `s = [S,1,…,1,s_{m_S}]` (so the slice is `{[S,1,…,1,k] : s_{m_S} ≤ k < s_{m_S}+n}`), and reads off that unbound = `k > n_S` is a terminal tail. The off-prefix and `V_S(d)=∅` branches fall under the `act = ∅` case and satisfy R6's own definition of terminal overrun ("named positions past the bound frontier") — every depth-`m_S` named position sits at or above `min(V_S)=[S,1,…,1]`, so the unbound portion is always a suffix past the frontier, never below it. Sound.
- **Subspace confinement.** The ContiguousSubtrees argument (prefix `[s₁]`, then the longer prefix in R6) correctly forces every `t ∈ ⟦σ⟧` to share the start's leading components, so no single ordinal-level span straddles subspaces and `act` of one spec is homogeneous in kind. R10's cross-spec heterogeneity is consistent with this.
- **R7 (Repeatability).** Comparability (`Σ →* Σ'`, not merely co-reachable from `Σ₀`) is correctly required and motivated; the equal-restriction hypothesis makes `act` and resolved addresses agree, and S0/L12 hold the stored entries fixed. The symmetry remark legitimately discharges the WLOG.
- **R8 (link sub-case vacuity).** CL-OWN forces `d=d'` and CL-UNIQ forces `v=v'`; the back-running of store membership to subspace via S3★ + SD is spelled out. Correct, and the confinement of genuine transclusion to content is properly derived.
- **R11 wp.** The single live condition (i) with `a ∈ dom(Σ.C)` as automatic consequence (S3★ membership + S0 immutability) is a genuine, non-trivial weakest-precondition, and the worked orphaning instance exercises it across a K.μ⁻ contraction with the frame clause cited.

Worked instances are present and load-bearing for R6, R8, R9, R10, R11; R1–R5 and R7 carry explicit proofs. All cross-ASN citations are to foundation ASNs; the standing reachability precondition correctly licenses every per-state invariant invoked. The empty-request and empty-arrangement boundaries are settled by the definitions.

## OUT_OF_SCOPE

The Open Questions (inline provenance, outright failure, dangling references, channel faithfulness, boundary-straddling spans) are correctly deferred — each is new territory, not a defect in R0–R11. R9 honestly scopes itself to resolution-level traceability rather than overclaiming inline provenance in the delivered stream, given R1 discards addresses for content items.

I found no hand-waved case, no unaddressed invariant conjunct, no missing boundary, and no claim left as assertion without derivation.

VERDICT: CONVERGED
