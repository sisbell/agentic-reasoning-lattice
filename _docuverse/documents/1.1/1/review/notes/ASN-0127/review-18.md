# Review of ASN-0127

I traced every derivation, checked the witness arithmetic in F-IMG-SWING and the worked illustration, verified each boundary case (empty region, empty arrangement, fresh document, R = ∅ full clearance), confirmed the two-phase factoring discipline is maintained (F-INERT is only ever applied with a *fixed* I-argument), and checked that all cross-ASN references target foundations only. The recently reworked D-NONMONO K.μ~ case split — reframed around image ⊆-comparability rather than arrangement injectivity — is sound.

## REVISE

No REVISE items. Detail on the load-bearing checks:

- **F-IMG-SWING witnesses.** Both the injective membership-swing (`{a} ↦ {b}`) and non-injective cardinality-gain (`{a} ↦ {a,b}`) reindex correctly under `image(W,d,Σ') = {Σ.M(d)(u) : u ∈ π⁻¹(W) ∩ dom(Σ.M(d))}`. The cardinality argument (`|π⁻¹(W) ∩ dom| = |W ∩ dom|` always; image-cardinality pinned only when `Σ.M(d)` injective) is correct, as is "distinct equal-size finite sets cannot nest" (sets are finite by S8-fin).
- **D-NONMONO K.μ~ clause.** The trichotomy no-move / containment-move / incomparable-move is exhaustive; "strict containment ⟹ cardinality change ⟹ non-injective" and "non-injective necessary but not sufficient for a containment move" are both right. I verified the shrink witness (`v₁↦a, v₂↦b, v₃↦b`, `π(v₁)=v₃, π(v₂)=v₁, π(v₃)=v₂` gives `image(W,Σ')={b}⊊{a,b}`) and the non-injective *incomparable* witness (`v₁↦a,v₂↦b,v₃↦c,v₄↦a`, `π=(v₂ v₃)` gives `{a,b} ↦ {a,c}`, incomparable). Image-motion being necessary-but-not-sufficient for discovery-set motion holds because `Σ.L` is fixed under K.μ~.
- **D-CWP.** The post→pre bridge (`image(W,d_q,Σ') = I_R` via `dom(Σ'.M(d_q)) = R`, D-SEQ★ giving `R ⊆ dom`), the `A = A∪B ⟺ B⊆A` reduction through F-UDIST, and the `R=∅` boundary collapse (`findlinks_disc(W,d_q,Σ)=∅`) are all correct. Both `I_R` and `Δ` are pre-state functions of `(Σ,R)`, so the biconditional is genuinely a precondition.
- **E-INV/E-MONO/E-CONS.** The two-keystone split is precise: F-CIL governs the store-fixed lane (`Σ.L = Σ'.L`), and because the existence path admits K.λ (`Σ.L` grows), that lane correctly rests on LP13 rather than F-CIL. The E-INV note that "LP3★ fixes per-slot coverage but not the arity bound `|Σ.L(a)|`; LP13 supplies both" is a real distinction, properly drawn. E-CONS's exclusion direction (the only nontrivial half) is fully argued via E-INV.
- **Worked illustration.** The coverage premise (pairwise prefix-incomparability of `a₁,a₂,a₃` via ChainMembershipForOrigin + T10a.2; `a_θ` in subspace `s_L` incomparable with content) is sound, so `coverage({a_i}) ∩ I = {a_i} ∩ I` and the type slot never fires. The K.μ⁺ "rise" (Σ₁ → Σ₂ re-adding `v₂↦a₂`, restoring `L_2` to the discovery set with no link created), and the cardinality-changing reorder variant (`L_2'=({a₂},∅,Θ)` conforming; swing `{L_1} ↦ {L_2,L_2'}` at fixed *image* cardinality but moving *discovery-set* cardinality) both check out and are genuinely illuminating.

## OUT_OF_SCOPE

### Topic 1: Content-keyed query through Σ.C, and composition with ASN-0098's projection
**Why out of scope**: Both are named in the ASN's own Open Questions (Q1, Q4). A query that names addresses through `Σ.C` rather than `Σ.M`, and the "project-a-link-then-meet-a-content-region" composition with LP**, are new combinators — not gaps in this note's arrangement-mediated foundation.

### Topic 2: Uniform weakest precondition across the whole K-vocabulary
**Why out of scope**: D-CWP correctly scopes itself to the K.μ⁻ contraction instance and explicitly defers the uniform characterization (extension/reorder/off-document) to Q3. The extension and reorder *behaviors* are already characterized in D-NONMONO; only the unified wp *formula* is deferred, which is a legitimate future-ASN boundary.

VERDICT: CONVERGED
