# Review of ASN-0116

I read this as the INSERT operation reframed as a valid composite over the K-vocabulary, with content allocation (K.α), arrangement displacement (K.μ⁻ → K.μ⁺), and provenance (K.ρ). I checked the load-bearing proofs cold rather than trusting the polish.

## REVISE

None. The proofs that carry the weight all hold:

- **Density without gaps (the usual hand-wave site).** The block-disjointness fact — that the index intervals `{1,…,J-1}`, `{J,…,J+n-1}`, `{J+n,…,N+n}` are consecutive, gap-free, disjoint, and union to `{1,…,N+n}` — is verified for every `J ∈ {1,…,N+1}`, including `J=1` (empty left), `J=N+1` (empty shifted suffix). I-DOM is constructed from this (not assumed from D-SEQ★), so there is no circularity with the reachability theorem.

- **The K.μ⁻ → K.μ⁺ realization.** The vacate-then-reinstall ordering is genuinely necessary and correct: K.μ⁺'s prior-domain agreement forbids rewriting suffix slots, so the suffix must first be vacated by K.μ⁻ to make the shifted positions *new*. Each elementary precondition is discharged at the correct intermediate state — in particular, the allocations must precede K.μ⁺ so that both block targets (`A_new`) and shifted-suffix targets (old suffix addresses) lie in the current `dom(C)`. The strict-contraction requirement (`J-1 < N`) holds down to `J=1`.

- **Whole-run freshness.** `A_new ∩ dom(C) = ∅` follows step-by-step from FirstEmissionFreshness/SubsequentEmissionFreshness, with the empty-arrangement/non-empty-content-region distinction (sub-cases a/b) handled correctly — the K.α start is fixed by the content region, not the arrangement.

- **No forward I-merge, universally.** `M(d)(q_J) = shift(a,n)` is impossible because `shift(a,n) = t_{m+n+1}` lies beyond the allocated frontier on `A_C(d)` (ChainMembershipForOrigin: origin-`d` content is a contiguous chain prefix), so `shift(a,n) ∉ dom(C')`, while `M(d)(q_J) ∈ dom(C)` by S3★ — independent of the suffix content's origin, including the transcluded-suffix regime.

- **IP4/IP6 depth.** The witness-set analysis correctly distinguishes that V-position witness *sets* are incomparable in general while witness *count* and resolved *content* are monotone, and IP6's wp is a genuine containment (`Added ⊆ D(d,Σ)`), not emptiness — with the ghost-plus-live-span pre-state as the witness that the emptiness form over-rejects. This is exactly the non-trivial wp the depth standard demands, and it is tied back to the new-block-witness gap.

- **Couplings and provenance.** J0/J1★/J1'★ are all driven by the range identity RAN (content-range gains exactly `A_new`; shifted-suffix addresses are range-old), and the worked example traces the subtle case (suffix addresses re-slotted but inducing no new R entry because provenance keys on I-address).

Cross-references are all to foundation ASNs (0034, 0036, 0043, 0047, 0058, 0082, 0093, 0098); no non-foundation references, no notation reinvented for something a foundation defines (the I-/F-labels are INSERT-local clause names citing their foundation source).

**Anti-bloat pass.** I looked specifically for the named forward-reference-accretion patterns: no "deferred to X / see Y below" scaffolding, no document-ordering justifications, no use-site inventories on definitions, no axiom-rationale sub-paragraphs. The interpretive sentences that restate the two-layer/isolation conclusions ("the shift is a relabelling of slots, not a transport of bindings"; "an insertion into one sharer is invisible to the others") fall under the explicit carve-out for statements of what the operation does or does not do. The recent revision history (removal of a redundant reachability-bridge sentence) appears to have already cleared the residual meta-prose.

## OUT_OF_SCOPE

The Open Questions (transclusion at the insertion point, concurrent insertions, transcluded-content provenance, post-fragmentation contiguity) are correctly deferred to the reframed future ASNs; the body defines no claims trespassing into COPY/DELETE/REARRANGE/MAKELINK territory.

VERDICT: CONVERGED
