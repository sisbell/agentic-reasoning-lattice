# Review of ASN-0131

The logic checks out. I verified RE-NCD (the separator-zero/field-agreement argument is correct), RE-ADDR (the unit-depth + antichain reduction to "retracts its own emitter address" is sound and the standing assumption is genuinely load-bearing), the union- and one-sided-intersection laws (both constructions in RE-UDIST-∩ are correct, and the injective counterexample really does isolate the split-witness obstruction from the image obstruction), the RE-CWP weakest precondition (the `Δ`/`I_R` reduction is equivalent to the full condition, and the `R = ∅` boundary collapses correctly), RE-SEL, and the retraction stability case (forward half under the flagged `coverage(Θ) ∩ dom(Σ.C) = ∅` hypothesis; backward half via R-Scope). The worked instance correctly exercises RE-OVL/RE-CLIP/RE-WHOLE/RE-UNIT. No correctness or missing-case defect found.

The findings below are all the residue this note's `review-mode.anti-bloat` classifier is meant to catch: forward-reference re-derivation and defensive citation that survived prior cycles.

## REVISE

### Issue 1: Retraction-permanence re-derives ASN-0086's R6a instead of citing it
**ASN-0131, §Stability "Under retraction"**: "the marking then persists across the *entire* ASN-0047 vocabulary, because `nullified` is a function of `Σ.L` alone (above) and `Σ.L` evolves only through `K.λ`. Every non-`K.λ` transition frames the link store ... leaving `nullified` fixed; each further `K.λ` only grows `Σ.L`, and a larger store never un-nullifies an address (R6a one step at a time...). Induction over any transition sequence from the retraction's post-state thus keeps `ℓ ∈ nullified`..."

**Problem**: R6a (RetractionStability, ASN-0086) already states one-step permanence for *every* transition: `a ∈ nullified(Σ) ⟹ a ∈ nullified(Σ')`. The frame-by-frame argument (non-`K.λ` frames `Σ.L`; `K.λ` only grows `Σ.L`; growth never un-nullifies) reconstructs exactly R6a's monotonicity content — and then cites R6a *inside* that reconstruction. The multi-step result is one-line induction over R6a; the whole vocabulary walk-through is redundant.

**Required**: Replace with "by R6a (ASN-0086) and induction, `ℓ ∈ nullified` at every state reachable from the retraction's post-state." Drop the `Σ.L`-evolution recital.

### Issue 2: Redundant per-transition expansion in the "three further kinds" stability paragraph
**ASN-0131, §Stability**: "Three further transition kinds leave the answer fixed for the same root reason — each leaves the queried fiber `Σ.M(d)` and the link store `Σ.L` fixed (LP8 supplying the K.δ document-registration case). Content allocation `K.α` touches neither `Σ.M` nor `Σ.L` ... and so changes no projection (LP6, ASN-0098); a freshly allocated I-address enters no region image without a separate arrangement edit. ... Provenance recording `K.ρ` writes only `Σ.R` ... (LP14, ASN-0098)."

**Problem**: The opening sentence already states the complete argument — the three transitions fix `Σ.M(d)` and `Σ.L`, which by RE-LOC are *all* `RE` reads — and flags the one genuine sub-case (K.δ needs LP8 because document registration grows `dom(Σ.M)`). The subsequent re-dispatch of K.α and K.ρ with their own external LP-citations (LP6, LP14) and the K.α aside ("a freshly allocated I-address enters no region image without a separate arrangement edit") restate that root reason via a heavier hammer (`project`-invariance from ASN-0098) when RE-LOC + the frame settles them directly.

**Required**: Keep the root-reason sentence and the K.δ/LP8 sub-case; drop the per-transition K.α and K.ρ expansion and the K.α aside.

### Issue 3: Belt-and-suspenders citation of the link prefix-antichain
**ASN-0131, §"Fresh emissions and the addressable population"**: "`dom(Σ.L)` is a tumbler-prefix antichain — distinct stored links never nest (R0a/FlatLinkDomain, ASN-0086; equivalently, the link sub-allocator discipline ASN-0093 imposes on *every* `K.λ` output, ASN-0047's included)." Recurs in the RE-ADDR table row: "the prefix-antichain of `dom(Σ.L)` (ASN-0093's link sub-allocator discipline; = ASN-0086's R0a)".

**Problem**: Two (three, with "ASN-0047's included") independent groundings for a single fact, in two places. Defensive citation; one suffices.

**Required**: Cite R0a (ASN-0086) once. Drop the "equivalently ... ASN-0047's included" alternative and the table row's second grounding.

### Issue 4: Unneeded exhaustiveness claim in the link-subspace-confined paragraph
**ASN-0131, §Stability**: "(Arrangement reordering `K.μ~` is *not* link-confined: it is link-subspace-fixing by admissibility and requires a non-trivial content effect by its precondition, so it always touches content — the two link-subspace-confined edits are exactly `K.μ⁺_L` and link-only `K.μ⁻`.)"

**Problem**: The section establishes two positive facts — `K.μ⁺_L` and link-only `K.μ⁻` leave a content-region answer fixed. It does not need to claim these are *exactly* the link-confined edits; the parenthetical exists solely to defend that surplus exhaustiveness claim against an imagined "what about `K.μ~`?" objection.

**Required**: Delete the parenthetical (or at least the "are exactly" clause). The two positive results stand on their own.

## OUT_OF_SCOPE

### RE-DEF's provisional return-value clause (RE-WHOLE) and the type-slot-match question
The whole-endset-vs-touching-spans return value is deferred to Open Question 1 with a stated trade-off (RE-UDIST distributes for the adopted value but not the alternative), and the type-slot-against-content meaning to Open Question 6. These are correctly deferred, not defects — I flag them here only so they are not mistaken for REVISE items. The selection (which `(i, e)` pairs) is fully settled; only the return value at a selected slot is open, which is a legitimate scoping of a design choice rather than an incompleteness in the operation's guarantees.

VERDICT: REVISE
