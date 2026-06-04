# Review of ASN-0087

The operation decomposition (`K.λ ; K.μ⁺_L`), the precondition reduction, the two-case wp analysis, the worked example arithmetic, and the three-class invariant audit are all sound and complete — I checked the per-state invariant list against ASN-0047's `ExtendedReachableStateInvariants` and every required conjunct is discharged, with boundary cases (empty endsets for `i ≠ 3`, first-link empty subspace, reflexive endsets) handled explicitly. The technical content has converged. The remaining findings are accretion, consistent with this note's `review-mode.anti-bloat` classifier.

## REVISE

### Issue 1: Navigation-only deferral sentence in *Freshness of the Allocation*
**ASN-0087, Freshness of the Allocation**: "The freshness of the V-position `v_ℓ` in `dom(M(d))` is established where it is consumed, in the S2 verification of the post-state invariants."
**Problem**: This sentence advances no reasoning — it is a pointer telling the reader where the work happens. The S2 verification in *Invariant Preservation* establishes `v_ℓ ∉ dom(Σ.M(d))` self-containedly via its two-part (within-subspace / cross-subspace) argument and does not depend on this announcement. A reader following the freshness argument must skip past it.
**Required**: Delete the sentence. The section's job is done once `ℓ`'s freshness is shown; the V-position freshness lives in S2 and needs no forward advertisement.

### Issue 2: Defensive meta-characterization trailing M-DepthConv
**ASN-0087, Inputs (M-DepthConv)**: "This is a scoped, normative commitment — for any document `d` whose every link V-position was placed by MAKELINK, `m_L(d) = 2` — not a system-wide invariant."
**Problem**: M-DepthConv's load-bearing content is the rule itself (commit first-link depth to `m = 2`, after which S8-depth pins it), which is what makes M-Pre's "caller does not supply `v_ℓ`" hold in the first-link case. The trailing clause classifies the *nature* of that rule ("normative commitment ... not a system-wide invariant") rather than stating what it does — the "not a system-wide invariant" is a defensive disclaimer against a misreading. This is the "prose explaining why/what-kind rather than what it says" pattern.
**Required**: State the rule and its scope ("for any `d` whose link V-positions were all placed by MAKELINK, `m_L(d) = 2`") and drop the "scoped, normative commitment ... not a system-wide invariant" gloss.

### Issue 3: Presentation-justification framing in *Side Effects on Prior Links' Discoverability*
**ASN-0087, Side Effects on Prior Links' Discoverability**: "The biconditional above is stated for `d` because, by M-PriorLinkDisc, `d` is the only document whose prior-link discoverability MAKELINK can change; for any `d_target ≠ d` the arrangement is frame-preserved and prior-link discoverability is unchanged, so the side-effect window is confined to the home document."
**Problem**: The opening clause justifies *why the section was written the way it was* ("is stated for `d` because...") and cites M-PriorLinkDisc — the very claim the section establishes inline — to defend its own scoping. The substantive content is only the confinement result (other documents' prior-link discoverability is unchanged). The justification wrapper is meta.
**Required**: State the confinement directly ("For `d_target ≠ d`, `Σ'.M(d_target) = Σ.M(d_target)`, so prior-link discoverability is unchanged; the side-effect window is the home document `d`.") without framing it as an explanation of the section's presentation choice.

## OUT_OF_SCOPE

### Topic 1: Forward-reaching endset well-formedness
The first Open Question (constraints on endsets whose spans reference not-yet-allocated I-addresses) is correctly deferred — L4 permits such endsets and their disciplined treatment is a future concern, not a gap here.

### Topic 2: Protocol-layer composite atomicity
The intermediate-state visibility question (Open Question 5) belongs to a protocol-layer ASN above the substrate, as the Atomicity section correctly identifies; not a revision to this note.

VERDICT: REVISE
