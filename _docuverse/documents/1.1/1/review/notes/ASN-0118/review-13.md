# Review of ASN-0118

I checked the resolution bridge (CP0), the composite decomposition in both the append and displacing branches, the tiling that discharges D-CTG/S2, the provenance branch analysis, the non-trivial weakest precondition, and the worked example arithmetic. The proofs are explicit and the hard cases are covered.

## REVISE

(none)

Notes from the scrutiny, for the record:

- **CP0(a) interior addresses.** The bridge correctly grounds run-*interior* addresses `aⱼ+k` in S8 lockstep (`Σ.M(d_s)(vⱼ+k)=aⱼ+k`) over bound positions, not as bare arithmetic on run leaders, and routes integrity through S3★ + C1a (single-subspace, from content-residence) rather than C1 (full binding). The discard of the full-binding hypothesis is sound — C1a's precondition is met by content-residence, C2's loss is the only casualty and COPY never uses it.
- **CP3c.** The domain-closure clause makes S2 dischargeable from the postconditions alone. The three text ranges (left `[min,p)`, placement `[p,p+W)`, shifted `[p+W,max+W]`) are verifiably disjoint and abutting via TS1/TS4, with `min{v≥p}=p` (since `p∈V_{s_C}(d)` in the displacing case) fixing the placement/shifted seam at `p+W`. No residual double-binding.
- **Displacing decomposition.** K.μ⁻ retention `n'_{s_C}=j<N` (strict) with `n'_{s_L}=n_{s_L}` (non-strict, link untouched) correctly discharges K.μ⁻'s "some subspace strictly contracts" requirement and carries `d`'s link subspace through both steps to satisfy CP6's `subspace≠s_C` conjunct. The `j=0` boundary (text cleared, D-MIN★ vacuous at Σ₁) and the empty/append cases are each handled.
- **CP8 provenance.** The three-way split (range-new/unrecorded → fresh K.ρ via J1'★; range-new/recorded → P2; not-range-new → P4★+P2) is correct, and the P4★ appeal is properly licensed by the composite-boundary standing precondition.
- **CP7b wp.** `wp(COPY, "a discoverable from d") = (E j : coverage(Σ.L(a).eⱼ) ∩ {c₀,…,c_{W−1}} ≠ ∅)` for a link not already discoverable is correctly derived from `ran(Σ'.M(d)) = ran(Σ.M(d)) ∪ {placed}` (shift preserves prior images) and CP7a coverage-invariance — a genuine non-trivial wp.

## OUT_OF_SCOPE

### The five open questions are correctly deferred
**Why out of scope**: C2 width-preservation under partial binding (OQ1), placement ordering for repeated spans (OQ2), level-uniformity across mixed-depth assembly (OQ3), link undiscoverability after destination DELETE (OQ4 — ASN-0117 territory), correspondence-relation semantics (OQ5), and link-subspace transclusion (OQ6) are all genuine future territory, not gaps in this ASN's claims. OQ2's mechanical order is in fact already fixed by CP0's ordered concatenation; the open question reads as the *semantic* adequacy of syntactic order, which is fair to defer.

VERDICT: CONVERGED
