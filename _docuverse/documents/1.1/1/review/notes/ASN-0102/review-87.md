# Review of ASN-0102

I checked the five worked examples, the wp(COPY, S3★) reduction, the X8 merge analysis, the X16 tiling, and the X14 invariant-discharge. The technical content is sound: the tiling partition is correct, the within-reference no-coalesce argument (gap-free source ⟹ source-V-adjacent maximal runs ⟹ not I-adjacent) holds, the cross-subspace disjointness via component-1 distinctness is right, and the boundary-absorption conditions in X12 are correctly stated and demonstrated in the coalescing example. The findings below are the accretion patterns the `review-mode.anti-bloat` classifier asks for.

## REVISE

### Issue 1: Pre-state-pinning rationale stated redundantly across sections
**ASN-0102, "The source designation and its resolution" and X10(b)**: The resolution section editorializes — "This single pre-state pinning is what makes self-transclusion (d_s = d) well-defined: the copied span is read from the frozen pre-state image even as d is simultaneously displaced." — and X10(b) then restates the same content: "the target-as-source is read at the pre-state Σ and is itself displaced by · + W." The self-transclusion example demonstrates it a third time.
**Problem**: The resolution section's job is to *state the convention* (resolution pinned to Σ); the "what makes self-transclusion well-defined" gloss duplicates X10(b)'s guarantee, which the example then concretely establishes. Two prose paragraphs in different sections carry the same justification.
**Required**: State the convention plainly in the resolution section; let X10(b) carry the guarantee and the example carry the demonstration. Remove the duplicated rationale from one of the two prose sites.

### Issue 2: X14 elaborates composite-boundary obligations it disclaims as not the step's
**ASN-0102, X14**: "The composite-level couplings (J0, J1★, J1'★) and the composite-boundary properties (P4★, P4a, P7a) are ValidComposite★'s obligation, evaluated only between an embedding composite's initial and final states, not the elementary step's" — followed by ~5 sentences walking through J0-vacuity and J1★/J1'★-via-(SL).
**Problem**: Having declared these are not the elementary step's obligation, the prose then discusses them at length. A reader checking COPY's actual per-step obligations must work past obligations the text itself scopes out. The load-bearing fact is just "(SL) together with X1"; the J0/J1★ walk-through is the expansion.
**Required**: Condense to the one sentence that matters — COPY's contribution to any embedding composite's couplings is (SL) + X1 (no allocation, so J0 vacuous; every range-new address is recorded-with-residency). Drop the per-coupling re-derivation.

## OUT_OF_SCOPE

### Topic 1: Link discoverability under COPY's displacement
**Why out of scope**: COPY changes `ran(Σ.M(d))` (adds copied addresses) and, unlike pure K.μ⁺ extension, *relabels* existing content-subspace V-positions (the displaced/copied positions violate LP9's prior-domain-agreement clause E2). The effect on which links become discoverable from `d` is genuinely new territory — it is "link semantics," explicitly out of scope here, and belongs in a future ASN that treats discoverability under non-pure-extension arrangement changes. The note correctly makes no claim about it (its L-invariant discharges concern only link-subspace *positions*, which COPY does not touch).

VERDICT: REVISE
