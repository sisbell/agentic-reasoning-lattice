# Review of ASN-0116

I worked this ASN against its own claims, the foundation contracts (ASN-0034/0036/0043/0047/0082/0093/0098), and the named boundary cases. The decomposition into a K-vocabulary composite is exhibited correctly and each step's precondition is discharged at the intermediate state it acts on. I traced the hard invariants — density without gaps, referential integrity, the provenance couplings, and link survival — and they hold.

What I checked and confirmed:

- **Composite validity (ValidComposite★ clause 1).** Each of `K.α(×n)`, `K.μ⁻`, `K.μ⁺`, `K.ρ(×n)` has its elementary precondition satisfied at its intermediate state. K.μ⁻'s reliance on D-SEQ★ at its input is sound because K.α frames `M`, so the arrangement at the post-K.α state is literally `Σ.M`, which satisfies D-SEQ★ at the composite boundary. K.μ⁺'s requirement that targets lie in `dom(C)` is exactly why allocation must precede it — correctly ordered. The strict-contraction condition `J−1 < N` holds across `1 ≤ J ≤ N`, and K.μ⁻ is correctly dropped (inapplicable, `J−1 = N`) in the append and empty cases.
- **Clause 2 couplings.** J0, J1★, J1'★ all reduce to the range identity RAN (`ran(M'(d)) = ran(M(d)) ∪ A_new`, content-subspace-new addresses exactly `A_new`). I verified RAN from I-LEFT/I-SHIFT/I-NEW/F-SUB and confirmed J1'★'s subtle "shifted suffix is range-old" reasoning: provenance keys on (I-address, document), and the suffix re-slots addresses already in `ran(M(d))`, so it manufactures no `R'∖R` entry.
- **Density (I-DOM).** The block-disjointness interval argument is correct in all cases including `J = N+1` (empty shifted-suffix interval) and the empty subspace (`N=0`, empty left and suffix). The gapped/filled bridge (`M'(d) = M'₀(d) ∪ {block}`) is justified by direct computation against the K.μ⁻/K.μ⁺ output; I instantiated J=3/n=2/N=5, J=1 front, J=N+1 append, and N=2/n=5 to confirm.
- **IP1 forward/backward merge.** The forward non-merge argument (`M(d)(q_J) ∈ dom(C)` by S3★ vs `shift(a,n) ∉ dom(C')` beyond the chain frontier) is correct and robust to the suffix content's origin. The backward-merge caveat (block I-merges into the left run when `q_{J-1}` holds `a_prev`) is accurate, so IP1's "run, not necessarily maximal" qualification is the right strength.
- **IP4.** The four-part witness decomposition (left/shifted-suffix/cross-subspace/new-block) is exhaustive and disjoint; the count formula and the resolved-content monotonicity (`coverage(e) ∩ ran(M(d)) ⊆ coverage(e) ∩ ran(M'(d))`, equality iff `coverage(e) ∩ A_new = ∅`) follow from RAN. The containment-direction analysis (incomparable vs `⊊`) is correct.
- **IP6.** The wp derivation via LP12 + LP3★ + RAN yielding `D(d,Σ') = D(d,Σ) ∪ Added` and hence the **containment** wp `Added ⊆ D(d,Σ)` (not emptiness) is a genuine non-trivial wp, and the worked example's `ℓ ∈ Added ∩ D(d,Σ)` (the member the emptiness form over-rejects) vs orphaned `ℓ' ∈ Added∖D(d,Σ)` separates the two forms correctly.
- **Frames.** F-LINK (`Σ'.L = Σ.L`) and F-ENT (`Σ'.E = Σ.E`) hold — every atomic in the sequence frames `L` and `E`. IP5 isolation is the conjunction of F-DOC and IP2/F-LINK.
- **Re-insertion after full contraction (empty-subspace sub-case b).** The distinction between the empty *arrangement* and the (non-empty) *content region* governing the K.α start address is handled correctly and is a genuinely subtle point.

Cross-reference discipline (standard #7): every citation in the body is to a foundation ASN (0034/0036/0043/0047/0082/0093/0098); the K.μ~ and LP18 mentions are foundation transitions/lemmas, not the retired operation ASNs. Depth (standard #6): postconditions carry derived consequences, the worked example exercises IP0–IP6 plus four boundaries, and IP6 supplies a real wp. No drift into implementation mechanics — implementation evidence is consistently used to ground abstract guarantees, not to specify them.

The anti-bloat pass found dense but substantive prose: the IP1 merge discussion, the IP4 containment analysis, and the composite-shape justification ("why K.μ⁻+K.μ⁺, not one atomic") all advance reasoning. The two-layer identity/arrangement theme recurs across the motivation and IP3, but at the boundary between motivational framing and formal claim, which is conventional. No labeled rationale sub-paragraphs, no downstream-consumer inventories, no document-ordering apologetics, no relocated-finding residue that I can point to defensibly.

## OUT_OF_SCOPE

The Open Questions correctly defer transclusion at a shared insertion point (ASN-0118), concurrent-insertion freshness without a serializing authority, transclusion provenance with a foreign origin, and post-edit fragmentation of the inserted run. These are future territory, not gaps in this ASN.

VERDICT: CONVERGED
