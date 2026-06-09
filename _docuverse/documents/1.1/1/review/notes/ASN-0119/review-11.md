# Review of ASN-0119

I worked through the imported operation and every system-level claim erected on top of it, checking the proofs against the foundation contracts and verifying the worked arithmetic by hand.

## Summary of verification

**Permutation and domain (P2).** The pivot destination ordinals `{2,3,4}/{5}/{1}` and swap `{2,3}/{4,5}/{6}/{1}` were checked to be pairwise disjoint and to tile `{1..n}` — `π` is a bijection, `dom(M'(d)) = dom(M(d))`. Consistent with ASN-0084 R-PIV/R-SWP.

**Identity correspondence (P0, P1).** `Σ'.C = Σ.C` and `ran(M'(d)) = ran(M(d))` follow from the bijection and the verbatim content frame. Confirmed against the worked range `{a₃,a₄,a₅,a₂,a₁} = ran(M(d))`.

**S2 / S3★.** Functionality from disjoint tiling; the S3★ inheritance correctly routes through `π⁻¹` (`M'(d)(v) = M(d)(π⁻¹(v))`, `π⁻¹(v)` again a text position) — the issue from review-10 is resolved. Link positions are frame-fixed, so their images stay in `dom(L)`. `π` maps each subspace onto itself, which is what the argument needs.

**Text-subspace invariants.** The observation that `V_{s_C}(d)` is unchanged *as a set* correctly discharges D-CTG/D-SEQ/D-MIN/S8a/S8-depth/S8-fin by inheritance; S8 is a theorem of any valid arrangement, so the run-structure change is not an independent obligation.

**Middle region (swap).** Net displacement `ord(c₀)+w_β − ord(c₁) = w_β − w_α` verified; the `+1` in the worked swap (`a₃: ord3 → ord4`) matches. The uniqueness-as-gap-filler argument is sound.

**Link footprint (P7a/P7b/P7c).** All four behaviors are exhibited with correct arithmetic: straddle-preserved `{B,C,D,E}` (`{2,3,4,5}→{2,3,4,5}`), exterior-meets-region fragmentation `{A,B}` (`{1,2}→{1,5}`), partial-coverage fragmentation `{B,C}` (`{2,3}→{2,5}`), and discontiguous-gains-contiguity `{B,E}` (`{2,5}→{4,5}`). The necessity condition ("fragmentation ⟹ straddles a cut, with no partial-coverage qualifier") is correctly stated and demonstrated. P7c is properly framed as sufficient-not-necessary.

**Atomicity (P8a/P8b).** The two-move decomposition of the worked pivot was recomputed: Move 1 yields `A C D B E`, Move 2 yields `A C D E B`; the intermediate `M_mid([s_C,4]) = a₂ ∉ {M, M'}` is genuinely divergent. P8a holds because any composite realizing the same `π` yields the unique `M(d)∘π⁻¹`.

**Isolation (P9) and well-definedness.** Frame `(∀d'≠d :: M'(d')=M(d'))` plus P0/P6 gives transcluder invariance even under shared range. Partiality is correctly handled: empty subspace, single position, and sub-minimum runs admit no valid cut sequence and the operation names no post-state.

The note meets the depth bar: concrete worked examples (pivot and swap) checked against postconditions, a non-trivial wp analysis isolating footprint contiguity as the single conditional property, and derived consequences (discoverability, isolation under transclusion) made explicit.

## REVISE

(none)

## OUT_OF_SCOPE

### The five Open Questions
**Why out of scope**: Cut-on-shared-transcluded-position, lock-free concurrent rearrangement, discovery-index invariants under footprint fragmentation, prior-arrangement recoverability from the Istream, and the displacement/subspace-boundary relationship are all genuine future territory. They are correctly placed in the Open Questions section rather than left as gaps in this ASN, which specifies the single-document, single-operation guarantee completely.

VERDICT: CONVERGED
