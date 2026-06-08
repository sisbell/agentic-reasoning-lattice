# Review of ASN-0102

The operation is specified in genuine depth — the tiling argument (X16), the wp-of-S3★ computation, the J1★/J1'★/P4★ discharge, and five worked examples that each exercise a distinct boundary configuration. The arithmetic checks out and the boundary cases (empty subspace, append, self-transclusion overlapping the displaced region, coalescing copy) are covered. My findings are confined to the forward-reference accretion the `anti-bloat` classifier targets, plus one scope-drift in the P4★ argument.

## REVISE

### Issue 1: X8 narrates what X12 will do, and the claims table repeats the deferral

**ASN-0102, X8 (RunFragmentation)**: "Where the copied region abuts the surrounding arrangement, the whole-arrangement maximal merge (M12 of `Σ'.M(d)`) may reduce the count further; that boundary behaviour is treated in X12." The claims-table row for X8 repeats it: "whole-arrangement merge absorbs a boundary block only where I-adjacent (X12)."

**Problem**: This is the "multiple paragraphs defer to the same downstream location" pattern. X8 establishes the within-region count (`≤ k`); the boundary-absorption behaviour is X12's content. X8 should not pre-narrate it, and the summary row should not re-defer. The reader must hold a promissory note open until X12 to finish following X8.

**Required**: End X8 at the within-region merge result. Drop the forward sentence and the parenthetical `(X12)` from the table row; let X12 own boundary absorption without X8 announcing it.

### Issue 2: PC3 forward-justifies which downstream invariant will consume it

**ASN-0102, Precondition PC3**: "This pins `subspace(v) = s_C` for the inserted positions and is the conjunct S3★ will require below."

**Problem**: A precondition clause should state the structural fact (`subspace(v) = s_C`). The trailing "is the conjunct S3★ will require below" is a forward pointer into the proof obligations — prose that justifies the precondition's existence by naming its downstream use rather than advancing the precondition. The wp-of-S3★ paragraph already establishes the dependency at its own site.

**Required**: Stop PC3 at the subspace fact. Remove the "S3★ will require below" clause; the wp computation cites PC3 where it is consumed.

### Issue 3: X14's P4★ argument re-derives the system base case

**ASN-0102, X14**: "*P4★ ... discharged at the composite boundary.* P4★ is a composite-boundary property (ASN-0047), so we establish it at every boundary by induction on boundaries. Base case `Σ₀`: `Contains_C(Σ₀) = ∅ ⊆ R₀`."

**Problem**: P4★ is a system-wide composite-boundary property already carried by `ExtendedReachableStateInvariants` (ASN-0047). COPY's obligation, as a newly-added transition kind, is the *preservation step* — that its transition does not break P4★. Running the full boundary induction, including the initialization base case `Σ₀ = ∅ ⊆ R₀`, imports the system theorem into the operation spec. The base case is a foundation fact about `Σ₀` (and COPY cannot even fire at `Σ₀`, which has no documents), so re-stating it here is foundation work relocated into this ASN.

**Required**: Keep only COPY's preservation contribution — from P4★ at the opening boundary `B` plus composite-wide J1★, conclude P4★ at the closing boundary. Drop the base-case clause and the framing of "establish it at every boundary by induction."

## OUT_OF_SCOPE

(none)

VERDICT: REVISE
