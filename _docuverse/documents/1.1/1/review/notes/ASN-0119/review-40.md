# Review of ASN-0119

I verified the operation's core machinery thoroughly: the import of REARRANGE_K (RA0–RA2 from ASN-0084's R-FRAME/R-PIV/R-SWP/R-RI), the S3★ derivation via π⁻¹, the key-set inheritance of D-CTG★/D-SEQ★/D-MIN★/S8a/S8-depth/S8-fin, the S8★ discharge via R-BLK + R-CANON, the J0/J1★/J1'★ vacuity arguments, the P4★/P7a frame discharges, the P4a induction, the P3 equality discharge, the footprint-transport biconditional (RA7a), and both worked transpositions (pivot `ABCDE↦ACDEB`, swap `ABCDEF↦AEFCDB`, and the two-move composite reaching `ACDB E` as intermediate). The arithmetic and the invariant-conjunct coverage check out — all 32 per-state conjuncts, the three composite-boundary properties, and P3 are accounted for. The ASN is on-track and correct; the findings below are at the margins.

## REVISE

### Issue 1: Unproven generalization of the contiguity outcome
**ASN-0119, "Links" (after RA7c)**: "The contiguity outcome is thus binary — preserved or broken. The configurations below are representative illustrations of these two outcomes, not a closed enumeration: a footprint spanning three or more regions falls under none of them, yet still resolves to one of the same two."

**Problem**: The only proven statement about footprint contiguity is RA7c — confinement to one region is *sufficient* for run-structure preservation. The four labeled configurations exhibit the one-region and two-block/exterior cases. The quoted sentence then asserts the behavior of a case it does not establish: a footprint spanning three or more regions "still resolves to one of the same two." Under the weak reading ("the same two" = {single run, more than one run}) the claim is vacuous — any run count is trivially 1 or >1, so the sentence states nothing. Under the strong reading (the multi-region outcome is governed by the *same two mechanisms* the examples illustrate) it is an unproven claim about uncovered cases, presented in the body as established. Either way this is meta-prose that does not advance the argument, and the "representative illustrations, not a closed enumeration" clause is a defensive exhaustiveness disclaimer of exactly the kind that accretes around examples. This is the reviser-drift pattern: imagining a case the proven claims (RA7c) do not reach and asserting its resolution.

**Required**: Remove the generalizing sentence and the "not a closed enumeration" disclaimer, letting RA7c (the proven sufficient condition) and the four labeled examples stand on their own; or state and prove a precise claim characterizing the contiguity outcome for general (multi-region) footprints. If the general characterization is future work, route it to the Open Questions rather than asserting it in the body.

### Issue 2: Partiality conclusion stated redundantly across the well-definedness section
**ASN-0119, "Well-definedness, and a caveat on the arithmetic"**: the conclusion "input outside the domain ⟹ no transition" is book-ended around the boundary-case enumeration — first "fall outside the domain of definition; on them there is no transition," then after the empty/single/short-run cases "there is no valid cut sequence: REARRANGE does not apply, and the operation is simply silent on inputs outside its domain — it names no post-state."

**Problem**: The same conclusion is restated before and after the case enumeration in different words. The enumeration (empty text subspace, single active position, run shorter than the minimum interval) is the substance; the surrounding twin statements of "no post-state outside the domain" are the redundant frame.

**Required**: State the partiality conclusion once (the operation names no post-state outside R-PRE's domain), then enumerate the degenerate cases as instances. Drop the second statement of the conclusion.

## OUT_OF_SCOPE

### Topic 1: Weakest precondition for footprint-contiguity preservation
**Why out of scope**: RA7c gives a sufficient condition and the second worked configuration (`α∪β` straddling cut `c₁`, contiguous before and after) shows it is not necessary, so the *weakest* precondition for contiguity-preservation is strictly weaker than confinement and depends on which cuts a footprint straddles and whether the relocated blocks re-abut at its boundaries. Characterizing this in general (the multi-region case Issue 1 oversteps) is a refinement that belongs in a future ASN — it is appropriately gestured at by the existing open question on content-based discovery indices and footprint fragmentation, not an error to fix here. (Stated only to clarify the boundary: the in-body overclaim is the REVISE; the missing general characterization is not.)

VERDICT: REVISE
