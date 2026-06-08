# Review of ASN-0113

The span machinery is used correctly: W4's exact-coverage derivation via T5 (with the strict upper bound legitimately weakened to `≤ reach`) is sound, the prefix `[S,1,…,1]` of length `m_S−1` is genuinely common to `start_S` and `reach`, and the worked instances (incl. the depth-3 case that exercises the non-vacuous T5 prefix-confinement) check out. W10/W11/W16/W19/W20 derivations are correct. My findings are about the note's overstated dependency footprint, which the `anti-bloat` classifier asks me to surface.

## REVISE

### Issue 1: Unused permanence dependencies listed as relied-upon facts
**ASN-0113, "The substrate we measure"**: "We rely on these foundation facts about the shape of each `V_S(d)`: … **L12 / P0** (link and content permanence): allocated keys persist and their values never change."
**Problem**: This is a use-site inventory entry that no claim consumes. The operation is a pure query of the present state (W8); permanence is irrelevant to observing a single state, and L12/P0 are about *value stability across transitions*, not "the shape of `V_S(d)`" that the list purports to collect. No W-claim (W0–W20) invokes L12 or P0. This is exactly the accreted dependency-inventory noise the anti-bloat pass targets.
**Required**: Remove L12/P0 from the list, or relocate them to wherever (if anywhere) a claim actually uses them. If nothing uses them, delete.

### Issue 2: W8's read-set contradicts its own dependency claim
**ASN-0113, W8 (PureQuery)**: "The operation reads `C`, `L`, `M`, and the document identity, and writes nothing … It is a function of the present state alone — indeed of `M(d)` alone, since the members are computed from `V_{s_C}(d)` and `V_{s_L}(d)`."
**Problem**: The two halves disagree. The result is computed from `V_S(d) = {v ∈ dom(M(d)) : v₁ = S}` — that is, from `dom(M(d))` and the subspace projection alone. The I-address *values* `M(d)(v)` are not consulted, and neither `C` nor `L` is read to produce the span-set. So "reads `C`, `L`, `M`" overstates the footprint and contradicts "depends on `M(d)` alone." (This is the same overstatement that produced Issue 1 — the note treats `C`/`L` as inputs when they are not.)
**Required**: State the actual read-set: the result is a function of `dom(M(d))` (equivalently `M(d)`) alone; `C` and `L` are not read by this operation. Reconcile the sentence accordingly.

## OUT_OF_SCOPE

### Topic 1: Permanence/version/transclusion behavior of the report
**Why out of scope**: The open questions about version forks, transclusion, and consistency with a single overall extent (ASN-0112) are correctly posed as future work, not defined as claims here. No action needed.

VERDICT: REVISE
