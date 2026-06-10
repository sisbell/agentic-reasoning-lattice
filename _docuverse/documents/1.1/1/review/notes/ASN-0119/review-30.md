# Review of ASN-0119

This note imports REARRANGE_K from ASN-0084 (a foundation) and lifts it into ASN-0047's extended state `(C, L, E, M, R)`, discharging the system-level invariant package and the link-survival guarantees on top of ASN-0084's permutation results. I checked every proof, the invariant coverage against ASN-0047's two theorems, the worked examples arithmetically, the boundary cases, and — per the `review-mode.anti-bloat` classifier — scanned for forward-reference accretion.

## REVISE

No REVISE items. What I verified:

**Worked examples check out arithmetically.** The pivot (`A B C D E ↦ A C D E B`, cuts ord 2,3,6, `w_α=1, w_β=3`) satisfies R-P1/R-P2/R-EXT pointwise; destinations `{2,3,4}∪{5}∪{1}` tile `{1..5}` disjointly (RA2), range `{a₁..a₅}` invariant (RA1), `π` table consistent with `M'(π(v))=M(v)`, footprint of `a₃` transports `{[s_C,3]}↦{[s_C,2]}` (RA7a). The swap (`A B C D E F ↦ A E F C D B`, cuts 2,3,5,7) satisfies R-S1/R-S2/R-S3; middle displacement `+1 = w_β−w_α` matches `diff[2]`. The two-move composite (cuts 2,3,5 then 4,5,6) reaches the atomic result (RA8a) through observable intermediate `A C D B E` with `M_mid([s_C,4])=a₂ ≠ a₄, a₅` (RA8b). All correct.

**Invariant coverage is complete and the hard conjuncts get real arguments.** Every conjunct of ExtendedReachableStateInvariants plus P3 and the composite-boundary properties P4★/P4a/P7a is addressed. The frame-preserved families (C-, E-, L-store) are correctly lumped under the `C/E/R/L` frame; the genuinely value-dependent ones get derivations: S3★ via the *inverse* permutation (not by claiming a key keeps its image — the note explicitly notes `M'(d)(v) ≠ M(d)(v)` inside the interval); J1★ via content-subspace-range invariance, with the precise observation that full-range RA1 alone does not close it; S8★ via R-BLK + R-CANON (correctly, since REARRANGE *refragments* runs); CL-OWN/CL-UNIQ via the frozen `s_L` arrangement frame. P4a is discharged by trace-prefix persistence (the witness state `Σ_k` is untouched by the appended atomic step) rather than by `R'=R` alone — the one place a frame argument would have been insufficient, and the note does not take that shortcut.

**The vocabulary-extension move is justified.** Adding REARRANGE to ASN-0047's closed atomic vocabulary as a one-step valid composite is sound *because* the note proves REARRANGE preserves the entire invariant package; the distinction from K.μ~ (no content-removed intermediate) is argued, not asserted.

**Boundary cases are handled.** Partiality on degenerate inputs (empty `V_{s_C}(d)`, single position, run shorter than the minimum affected interval) is treated as out-of-domain silence; the empty-exterior case (`c₀ = min`) is correctly identified as a vacuous *branch* that stays *inside* the domain.

**wp analysis is non-trivial.** Footprint contiguity is correctly isolated as the single property not preserved in general (`wp` beyond R-PRE), with RA7c stated as *sufficient, not necessary* and the non-necessity proved by the across-blocks config that lands contiguous while straddling a cut. Discoverability (RA7b) is unconditional, reduced to `coverage ∩ ran ≠ ∅` (LP12) and invariant by RA1.

**No cross-ASN references outside the foundation set** (ASN-0034/0036/0043/0047/0058/0084/0098 are all foundations; "Question N" cites the consultation, not an ASN), and **no implementation drift** — the Gregory `diff[2]`/collision material is explicitly marked "an observation rather than a claim" and "defects relative to the abstract operation," keeping the note on the system-guarantee side.

**Anti-bloat scan.** I examined the candidates — the LP3/LP11 "re-prove rather than cite" parenthetical, the RA1 "hypothesis of R-RI, not a result of it" provenance note, the dense single-paragraph coupling discharge, and the layered restatement of link survival before RA7a formalizes it. Each is either a concise justification of a non-obvious choice (REARRANGE sits outside ASN-0047's vocabulary, so the foundation lemmas genuinely cannot be cited), a precision aid that prevents a misattribution, or discovery-voice motivation appropriate to a note. None requires the reader to skip meta-prose to follow a claim; I found no forward-reference accretion (only one forward pointer, to RA7a), no axiom-rationale sub-paragraphs (no new axioms), and no document-ordering justifications. The borderline within-paragraph restatement of "the link does nothing" in the Q4 paragraph is mild and does not rise to a finding.

## OUT_OF_SCOPE

### Topic 1: REARRANGE at depths greater than 2, and in subspaces other than `s_C`
The note explicitly confines itself to the text subspace at depth 2 — the exact scope at which ASN-0084's closed-form permutations are established — and disclaims any claim beyond it. Generalizing the transposition to deeper V-positions or to the link subspace is new territory for a future ASN, not a gap here.

### Topic 2: The five Open Questions
Cross-document boundary-hood under shared transclusion, unserialized concurrent rearrangement, the content-index/arrangement invariant under footprint fragmentation, recoverability of a prior arrangement, and the boundary-preservation guard for a formula-based displacement layer are all correctly deferred. They are stated as questions, not claims, and each names work that builds on this ASN rather than correcting it.

VERDICT: CONVERGED
