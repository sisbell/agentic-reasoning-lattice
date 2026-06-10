# Review of ASN-0119

I checked the proofs against the imported ASN-0084 contracts and the ASN-0047 invariant package, verified the two worked examples numerically, and stress-tested the boundary cases and the vocabulary extension.

## Verification performed

**The worked examples check out arithmetically.** Pivot (`A B C D E ↦ A C D E B`, cuts ord 2,3,6): destination ordinals `{2,3,4}` (R-P1), `{5}` (R-P2), `{1}` (R-EXT) are disjoint and tile `{1..5}`, so RA2 holds; range `{a₁..a₅}` unchanged (RA1); the `π` table is internally consistent with every footprint example. Swap (`A B C D E F ↦ A E F C D B`, cuts ord 2,3,5,7): R-S1/S2/S3 produce `a₁ a₅ a₆ a₃ a₄ a₂`; middle displacement `+1 = w_β − w_α = 2 − 1` matches Gregory's `diff[2]`. The four contiguity examples (`{C,E}`, `α∪β`, `{A,B}`, `{B,C}`) all map through `π` exactly as claimed.

**The constant-displacement constants are correct.** Pivot: β by `−w_α`, α by `+w_β`. Swap: β by `−(w_α+w_μ)`, μ by `w_β−w_α`, α by `w_β+w_μ`. All verified against R-PPERM/R-SPERM.

**The hard derivations are sound.** S3★ via `M'(d)(v) = M(d)(π⁻¹(v))` and π-subspace-fixity is correct (verified the substitution `u = π⁻¹(v)`). J1★'s closure turns on the content-subspace value-set invariance `{M'(d)(v):s_C} = {M(d)(u):s_C}`, which is genuinely stronger than RA1's full-range invariance — the note correctly flags this. P4★, P7a, J0, J1'★ all reduce to the frame plus that invariance. RA7a's biconditional chain is rigorous in both directions (π surjective on `dom(M(d))` closes ⊆).

**Invariant coverage is complete.** Every ExtendedReachableStateInvariants conjunct is addressed: the M-dependent ones (S2, S3★, S3★-aux, S8★ via R-BLK+R-CANON, D-CTG★/D-MIN★/D-SEQ★/S8a/S8-depth/S8-fin via key-set invariance, CL-OWN/CL-UNIQ via frozen `s_L`) get explicit arguments; the frame-preserved ones (S4, S7-family, C-family, L-family, E-family, P6/P7/P8) get a uniform frozen-component argument. The catch-all is legitimate because those conjuncts genuinely depend only on `C/E/R/L`, all verbatim frames — this is one uniform argument, not "proof by similarly." P3, P4a all discharged.

**The P4a trace argument has no gap.** Both trace types to `Σ'` are handled (ending-in-REARRANGE via prefix-witness persistence; other-final-composite via ASN-0047's pre-state-local argument plus the combined induction). The "combined induction" caveat is load-bearing, not decoration — it closes the genuine concern that ASN-0047's induction did not range over REARRANGE-interleaved traces.

**Boundary cases handled.** Empty / singleton / sub-minimal documents fall outside R-PRE (no transition); first-position cut and whole-document rearrange stay inside the domain with vacuous exterior branches; the bijection and extent conservation survive both.

**Cross-references are all to foundation ASNs** (0034, 0036, 0043, 0047, 0058, 0084, 0098) whose claim statements are provided — permitted. The note reinvents no foundation notation; it imports REARRANGE_K rather than restating it, and its value-add (ASN-0047 integration, link survival via ASN-0098 projection, isolation, atomicity) is genuinely beyond ASN-0084's smaller state model.

The prose density in the ASN-0047 discharge paragraph is high, but every sentence does work — I did not have to skip meta-prose to follow a claim, and the forward-reference deferral patterns the anti-bloat pass targets are absent (consistent with the recent state-tuple/P4a/RA3 trim). The lone implementation discussion (green-implementation displacement defect) is correctly framed as motivating observation, not as a spec claim, so the ASN stays in state/operation/invariant territory.

## OUT_OF_SCOPE

### Topic 1: REARRANGE at V-position depth > 2, or in subspaces other than `s_C`
**Why out of scope**: The note confines itself to the text subspace at depth 2, matching the exact scope where ASN-0084's REARRANGE_K (CS3/CS4) is defined, and explicitly disclaims other depths/subspaces. General-depth transposition needs its own ASN-0084-level closed-form permutation before it can be lifted; it is new territory, not a defect here.

### Topic 2: The five Open Questions (cross-document boundary-hood, unserialized concurrent rearrangements, discovery-index invariant under fragmentation, prior-arrangement recoverability, boundary-preservation guard for formula-based displacement)
**Why out of scope**: These are correctly identified by the note as future work; each requires machinery (a shared-boundary discipline, a concurrency model, an index invariant) that this single-document atomic operation neither provides nor needs.

VERDICT: CONVERGED
