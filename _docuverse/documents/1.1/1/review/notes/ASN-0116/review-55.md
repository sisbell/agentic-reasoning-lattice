# Review of ASN-0116

I read the note as a specification of the INSERT operation: an allocation effect (fresh content identity) and an arrangement effect (uniform suffix shift), realized as a valid composite over the K-atomic vocabulary, with four named invariants discharged. I checked the proofs, the boundary cases, the composite-validity argument, the weakest-precondition analysis, the worked example, and scanned for forward-reference accretion.

## REVISE

(none)

I attempted to break the note on the points an operation specification most often fails. Each held:

- **The arrangement shift is not a single atomic, and the note does not pretend it is.** It rewrites the I-address at *existing* suffix positions (forbidden by K.μ⁺'s prior-domain agreement) while strictly growing the domain (forbidden by K.μ⁻ and K.μ~). The note confronts this directly, decomposing the shift into `K.μ⁻` (vacate) then `K.μ⁺` (re-install block + shifted suffix), and discharges each step's elementary precondition at the intermediate state — including the load-bearing ordering constraint that K.α must precede K.μ⁺ so the block targets are in `dom(C)` when installed. This is exactly the "who shifts them, atomic?" hazard, met head-on.
- **Boundary coverage is complete and the branches are genuinely distinct.** Interior (`1 ≤ J ≤ N`, K.μ⁻ present), front (`J = 1`, the only branch exercising `n'_{s_C} = 0` strict contraction), append (`J = N+1`, K.μ⁻ dropped as inapplicable *and* unnecessary), and empty subspace — the last correctly split into sub-case (a) fresh-document first-emission and sub-case (b) re-insertion after full contraction, where the content region is non-empty so even `k = 0` is a *subsequent* emission while the arrangement still re-pins depth and `min` from scratch. I verified the arithmetic `shift(q_k, n) = q_{k+n}`, the block-disjointness interval tiling `{1,…,J-1} ⊎ {J,…,J+n-1} ⊎ {J+n,…,N+n} = {1,…,N+n}`, and the gapped/filled bridge against ASN-0082's I3-CS (which genuinely excludes the block).
- **The wp (IP6) is non-trivial and correct.** Substituting RAN into LP12 gives `D(d,Σ') = D(d,Σ) ∪ Added`, so preservation requires `Added ⊆ D(d,Σ)` — a *containment*, not an emptiness. The note correctly identifies that the emptiness form (`coverage ∩ A_new = ∅`) is sufficient but strictly stronger, and that it over-rejects the ghost-plus-live-span pre-states L4/L9 permit. The IP6-trap and resurrection examples illustrate both branches.
- **IP4's witness analysis derives real consequences.** I checked the four-part decomposition (left/shifted-suffix/cross-subspace/new-block), the bijection onto the first three parts, the count formula, and the incomparability argument (the largest shifted witness `shift(v_max, n)` cannot have been a prior witness without contradicting `v_max` maximal). The inclusion of *cross-subspace* witnesses — link-subspace positions whose images lie in `coverage(e)` — is a subtle point the note gets right.
- **Provenance couplings trace cleanly at the boundary.** J0/J1★/J1'★ are all driven by RAN, with the shifted suffix correctly classified as range-*old* (no new record) and only `A_new` range-new. The worked example walks each constraint, and P7a is preserved via `R ⊆ R'` for prior addresses plus I-PROV for fresh ones.

Citations are all to provided foundations (ASN-0034/0036/0043/0047/0082/0093/0098); no cross-ASN reference to a non-foundation, and no notation reinvention (`shift`, `δ`, `project`, `coverage`, `K.α`/`K.μ`/`K.ρ` used as defined; `q_k`, `A_new`, `M'₀(d)` are local abbreviations, not re-definitions).

**Anti-bloat scan (per the `review-mode.anti-bloat` classifier):** I looked specifically for forward-reference meta-prose, axiom rationale, downstream-consumer inventories, document-ordering justifications, deferral chains, and duplicate paragraphs. The note introduces no axioms; its cross-references are backward (to verified foundations) or internal-backward (`(Effect)`, `(RAN)` pointing to where a fact was established, which is DRY, not bloat); it contains no "see below," "deferred to," or non-circularity/ordering justifications; and the step-ordering remark ("which is exactly why the allocations must precede this step") is a substantive precondition dependency, not a placement excuse. The link-survival prose bullets overlap IP4, but these are object-level *statements of what the operation does to links* — explicitly carved out by the guidance as not-meta-prose — and constitute the expected prose half of a note's prose+claim coupling. No accreted forward-reference meta-prose remains to flag.

## OUT_OF_SCOPE

The four Open Questions (transclusion at the insertion point, concurrent insertion freshness, provenance under transclusion, post-edit run fragmentation) are correctly posed as future work and define no claims, so there is nothing to flag. They align with the retired/reframed scope boundaries (COPY/ASN-0118, etc.).

VERDICT: CONVERGED
