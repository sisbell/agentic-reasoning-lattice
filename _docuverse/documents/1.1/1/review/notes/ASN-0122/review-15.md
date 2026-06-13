# Review of ASN-0122

I checked each definition and claim against the foundations, traced the proofs of X0–X12 and X-T, and recomputed the worked example end to end. I report what I verified and the few places I pressed hardest.

## Verification notes (what survived scrutiny)

**The relation and its basis.** `corr` is the kernel of `res` intersected with `P × Q`. X1/X2 correctly establish address-equality (not value-equality) as the relation: X2's construction is a genuinely valid composite under ValidComposite★ (J0, J1★, J1'★ discharged at the composite endpoints; `a₁ ≠ a₂` by S4/GlobalUniqueness), and the predicate provably never consults `C`. X5's locality proof is complete — the membership test is shown to read only `res|P`, `res|Q` and nothing of `C, L, E, R, M` outside the regions — and its three consequences (determinism, indifference of K.α/K.λ/K.ρ/K.δ, memorylessness) are correctly derived from the frame clauses.

**X9 (subspace vacuity).** The three sub-arguments (CL-OWN for cross-document, SD/L14 for content↔link, CL-UNIQ for same-document) correctly reduce any link-footed pair to `p = q`, and the `⊔`-decomposition is both exhaustive and disjoint. The claim is framed explicitly over *unrestricted* instances and serves as the justification for the content-confinement design choice (and is the lever Deficiency 2 turns on) — it is not a case the carrier "already excludes" for no reason.

**X11 (canonical report).** I confirmed the diagonal `succ` is injective per coordinate via TS2 (equal-depth precondition from S8-depth), that fan-out lands distinct successors and hence distinct chains, that feet strictly increase (TS4/TS5) so no cycles, and that the `(first foot, second foot)` key is injective on maximal pairs — so the canonical order is strict and the report unique. The σ_full whole-document span (`reach = [1,…,1,1+n]`, clipping to exactly `V_{s_C}(d)`) checks out.

**X-T / X7 / X6.** The transport lemma is correct (set equality holds via the two preservation equations read both ways). The shifting-contraction instantiation (X7iii) is the one that earns its keep — injectivity of the piecewise `id`/`σ` is genuinely discharged in three steps, with `L ∩ Q₃ = ∅` (D-DP(a)) supplying the cross-piece non-collision that `id` and given-bijection cases get for free. The chain composition (X6b) correctly telescopes injective res-preserving factors under the stated endpoint-persistence and interleaved-edit premises. The wp forms for reordering and contraction are non-trivial (pullback through `π`; survival conjuncts, including the symmetric both-feet self-comparison case).

**X4c, X8, the worked example.** The integer-interval argument in X4c is sound (monotonicity + T12(c) convexity ⇒ `K_P`, `K_Q` intervals ⇒ intersection an interval). X8's diagonal-as-own-chain reasoning holds even under off-diagonal sharing. The six-state worked example reproduces exactly: `corr`, the fan-out, `γ₁`/`γ₂`, the swapped transpose with second-foot tie-break, the boundary-crossing clip, and the disjoint-window detector all recompute correctly.

**Other checks.** Empty/self/full-vs-partial/repeated/chain edge cases are handled uniformly (empty regions degenerate to `∅`/`⟨⟩`; contract-to-empty falls out of X7ii's `Surv = ∅`). All ASN references are to foundation ASNs only — no self-contained-spec violation. Implementation observations are properly segregated from the abstract claims, and the two deficiencies are adjudicated by R2 and X9/precondition rather than smuggled into the spec. The binding (R1–R3) vs. reference (R4) split is correctly stated, and CANON is shown to satisfy R1–R3.

On the anti-bloat classifier: the recent prose-tightening (remark-on-n, X-T(b)) appears to have done its work. The remaining connective prose either advances a claim, handles a case, or carries a concrete example/analogy — none of which is meta-prose. Forward references are isolated inline pointers (region→X9; X3→X3-continued), not accreted justification, and no axiom-rationale sub-paragraphs, document-ordering apologetics, or duplicated paragraphs are present.

## REVISE

(none)

## OUT_OF_SCOPE

### The six Open Questions
**Why out of scope**: n-way alignment from pairwise reports, derived/cached correspondence indices, interoperable report granularity, multiplicity-annotated report equivalence, the arrangement-presence basis for "part of a version," and growth of the subspace vocabulary are all genuinely new territory. The ASN frames them as such; none is a gap in the present claims.

### Scope-excluded operations
**Why out of scope**: Version creation, document discovery, origin reporting, deletion comparison, content delivery, link/content operations, and the inter-server protocol are correctly absent; the edit operations enter only through their foundation contracts in the stability theorems (X7), not as objects of this ASN.

VERDICT: CONVERGED
