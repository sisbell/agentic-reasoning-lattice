# Review of ASN-0118

I checked the substrate citations, the resolution bridge (CP0), the composite decomposition in both the append/empty and displacing cases, the J0/J1★/J1'★ provenance discharge, the tiling argument for prior-arrangement preservation, the link-discoverability wp, and the two-source worked example. The logic is sound: the operation is well-defined across the boundary cases (empty destination, append, `j = 0` full contraction, self-transclusion), the displacing-case K.μ⁻+K.μ⁺ composite faithfully realizes CP2/CP3a/CP3b/CP3c, and CP8's three-branch provenance argument correctly distinguishes range-new-unrecorded (K.ρ), range-new-recorded (P2), and not-range-new (P4★+P2). I found no correctness defect.

What I did find — and the `review-mode.anti-bloat` classifier flags this note for exactly this — is accreted meta-prose: two rationales stated twice, and two claim-justifications written by imagining the case the claim excludes.

## REVISE

### Issue 1: P4★-scoping rationale stated twice
**ASN-0118, "Standing precondition (composite boundary)" and the CP8 discussion**:
- Standing precondition: "P4★ (`Contains_C(Σ) ⊆ R`), which holds at composite boundaries but may fail at an intermediate atomic state."
- CP8: "The appeal to P4★ here is licensed precisely because COPY's pre-state `Σ` is a composite boundary (standing precondition): P4★ is one of ASN-0047's composite-boundary properties, not a per-state invariant, and would not be available at a state reached mid-composite."

**Problem**: Both sentences make the identical point — P4★ is a composite-boundary property, not a per-state invariant, hence unavailable mid-composite. The standing precondition already establishes it; the CP8 paragraph re-explains it at the point of use. This is the "multiple paragraphs defer to / re-state the same scoping fact" pattern.
**Required**: Keep one. Either state the scoping once in the standing precondition and let CP8 cite it bare ("by P4★, available since `Σ` is a composite boundary"), or drop the standing-precondition gloss and explain it only where used.

### Issue 2: I3-borrowing rationale stated twice
**ASN-0118, "The COPY operation" (CP3a) and "The destination's prior arrangement is preserved"**:
- CP3a: "from it we borrow, *for the shifted positions*, that they remain well-formed (I3-VP), preserve depth (I3-VD), and stay finite (I3-fin). The function-ness, no-holes, contiguity, and sequentiality of COPY's actual `Σ'.M(d)` rest instead on CP3c's domain closure and K.μ⁺'s strict-extension contract."
- Prior-arrangement section: "ASN-0082's I3 lemmas supply the per-position facts *about the shifted trailing content* … but they describe only the *shift*, leaving the gap `[p, p+W)` empty in I3's `M'(d)`. COPY fills that gap with the placement positions (CP2), so the function-ness and no-holes of COPY's actual `Σ'.M(d)` are *not* established by the I3 lemmas: they rest on the tiling argument below…"

**Problem**: The same caveat — "I3 gives the shifted-position facts (VP/VD/fin), but function-ness/no-holes come from CP3c/tiling, not I3" — is delivered in full twice, in two sections.
**Required**: Consolidate into one statement at the point where the displacement is established; have the other site reference it.

### Issue 3: content-residence precondition justified by imagining the case it excludes
**ASN-0118, "The COPY operation" (Precondition — content residence)**: "it is load-bearing in two places. Without it a resolved `vⱼ` could be a link V-position (`subspace(vⱼ) = s_L`), and S3★ would place `Σ.M(d_s)(vⱼ)` in `dom(Σ.L)` rather than `dom(Σ.C)` — falsifying CP0(a). And CP2 would then bind that link address to a content-subspace destination position `p + i`… The precondition discharges both obligations at once…"

**Problem**: Two anti-bloat patterns at once — the paragraph (a) imagines a link-V-position case that the precondition itself excludes, and (b) inventories its two use-sites ("load-bearing in two places," "discharges both obligations at once"). The reader must work through a counterfactual to reach a fact a positive statement gives directly.
**Required**: State it positively and once: "By content-residence every active position is in `s_C`, so S3★ gives `cᵢ ∈ dom(Σ.C)` (CP0(a)), and the destination bindings of CP2 land content addresses in content-subspace positions (S3★)." Drop the imagined violation and the "two places" inventory.

### Issue 4: CP3c justified by imagining the post-state it excludes
**ASN-0118, "The COPY operation" (CP3c discussion)**: "The gap it closes is concrete. In the displacing case CP3a asserts a *new* binding at `v + W` but does not by itself remove the pre-state binding at `v`; CP3b frames only `v < p` and CP6 only `subspace(v) ≠ s_C`. So nothing among CP2/CP3a/CP3b/CP6 vacates the pre-state binding at `p`, and a reader could admit a post-state in which `p` is bound both to `c₀` (CP2) and to the un-vacated `Σ.M(d)(p)` — a double binding that falsifies S2…"

**Problem**: This justifies CP3c by constructing a post-state CP3c rules out and attributing it to a hypothetical reader. The substantive point — CP3c vacates the pre-shift positions so each text V-position carries exactly one binding (S2) — is buried under the imagined double-binding. This is the "imagines a case the claim excludes" / defensive-justification pattern.
**Required**: Replace with the positive statement: "CP3c closes `d`'s text-subspace domain to the three disjoint abutting ranges (left, placement, shifted), so each text V-position carries exactly one binding and S2 is dischargeable from the postconditions alone." Keep the one-line note that CP3c is the COPY analogue of I3-V/D-DOM.

### Issue 5: the CP0 bridge over-derives an ascending coincidence CP0(a) does not consume
**ASN-0118, "What a spec-set names, and what resolution recovers"**: after grounding the interiors by lockstep ("the address `aⱼ + k` … is *exactly* the image `Σ.M(d_s)(vⱼ + k)` … run interiors included"), the bridge continues: "The runs being a disjoint maximal partition of the totally-ordered `act(ρ, Σ)`, each run's positions ascend with `k` and lie wholly below the next run's … the runs therefore occupy non-interleaving T1-intervals on which V-start order is interval order. C1b … reproduces the ascending enumeration of `act(ρ, Σ)` address-for-address…"

**Problem**: CP0(a) is a membership claim (`cᵢ ∈ dom(Σ.C)`); the lockstep step above already discharges it for run-leading and interior addresses alike. The non-interleaving / "V-start order = ascending position order" sub-argument establishes a stronger *sequence-level* coincidence. The flat order of `resolve(R, Σ)` is already fixed by ASN-0058 C1b (runs in V-start order) plus spec-set order, so the operation's determinism and CP2's placement order do not need it, and CP0(a)/(c), CP4, and CP11 are order-independent or multiset-level. If no downstream claim consumes the ascending-position coincidence, this sub-argument is excess derivation.
**Required**: Either trim the non-interleaving paragraph and let CP0(a) rest on lockstep + C1b, or name the claim that requires the ascending characterization so the derivation is visibly load-bearing.

## OUT_OF_SCOPE

The four Open Questions (partial-binding width shortfall vs. nominal extent, cross-depth source assembly, link undiscoverability after later contraction, the correspondence relation, link-subspace transclusion) are correctly framed as future territory rather than gaps in this ASN. COPY is well-defined for whatever `W` partial binding yields, and none of these is needed for the operation's stated guarantees. No additional out-of-scope topics to raise.

VERDICT: REVISE
