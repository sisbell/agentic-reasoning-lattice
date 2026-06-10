# Review of ASN-0115

I verified the formal content before turning to prose. The proofs hold up under scrutiny: the **Confinement lemma**'s T5 application is correct (`p = [s₁,…,s_{m-1}] ≼ s` and `≼ reach(σ)`, with `s ≤ t ≤ reach(σ)` yielding `p ≼ t`); the **R6** gap analysis is genuinely complete — it splits `V_S(d) = ∅` / `≠ ∅`, then `act = ∅` / `≠ ∅`, pins the canonical start `[S,1,…,1,s_m]` only when a witness `v ∈ act` exists, and correctly establishes that depth-`m_S` unbound positions form a terminal overrun `k > n_S` with no interior hole; **R7**'s comparability requirement (`Σ →* Σ'`, not common-ancestor reachability) is correctly motivated by divergent-branch re-allocation; **R8**'s link-vacuity via CL-OWN + CL-UNIQ is airtight; **R11**'s wp reduction to a single live condition (store-membership discharged by S3★, not a separate conjunct) is right. All five worked instances compute correctly (I re-derived `s ⊕ ℓ`, the depth-2 slices, and the `[2,3] ∈ ⟦σ⟧` straddle counterexample). No cross-ASN reference violations — every citation is to a foundation ASN. No drift (the operation is specified abstractly as a state-function with realization-independent invariants).

The one finding is residual meta-prose, which is squarely what this review mode exists to catch.

## REVISE

### Issue 1: Self-referential meta-prose in R9's explanatory paragraph
**ASN-0115, §"What co-delivery reveals: coherent multi-origin assembly" (prose after the R9 box)**: "Output-recoverability is where the two kinds genuinely part, and the box records that asymmetry as R9's substantive content."

**Problem**: The clause "and the box records that asymmetry as R9's substantive content" is self-referential commentary on the document's own structure; it does not advance the reasoning. The preceding clause already names output-recoverability as the distinguishing point, and the box was read moments earlier. The clause is cleanly removable — "...Output-recoverability is where the two kinds genuinely part. Because each spec is resolved against its own arrangement (R4)..." flows intact and loses nothing. This is exactly the connective tissue that accretes across revision cycles, and its location in the just-restructured R9 commentary (per the git log, "restructure R9 commentary to lead with output-recoverability") is precisely where such churn settles.

More broadly, the paragraph re-walks content the box already states in full: the box gives content→`origin(a)` not output-recoverable / determinate-via-resolution and link→`home(a)` recoverable; the paragraph re-derives the same per-position dispatch ("for a content position it is the document-level prefix `origin(a)`; for a link position it is the link's home `home(a)`"). The genuinely additive content is the single observation that determinacy is *automatic* (origin/home are functions of the resolved address), plus the Nelson 4/10–11 and Gregory `specset2ispanset` grounding.

**Required**: Delete the self-referential clause. Tighten the paragraph so it contributes only what the box does not already state — the determinacy-is-automatic justification and the supporting evidence — rather than re-deriving the box's kind-asymmetry.

## OUT_OF_SCOPE

The five Open Questions (inline content provenance, outright-failure semantics, dangling-reference resolution, channel faithfulness, subspace-straddling spans) are correctly deferred rather than claimed, each to a distinct location — no "multiple sections deferring to one downstream point" pattern. No additional future-ASN gaps to surface.

VERDICT: REVISE
