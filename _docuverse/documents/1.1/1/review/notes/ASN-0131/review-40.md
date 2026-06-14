# Review of ASN-0131

This note defines RETRIEVEENDSETS as a pure query surfacing role-tagged endsets over a content region without naming links. I checked the core definitions and every introduced claim. The mathematics is sound: the existential factoring underlying RE-DEF/RE-UDIST is correct (`touch_W` depends only on `e`, so it factors out of the link existential, giving `RE = {(i,e) ∈ Avail(Σ) : touch_W(e)}`); RE-SND/RE-CMP are genuine immediate reads of the biconditional; RE-CWP's weakest precondition is derived correctly (`image(Σ') = I_R ⊆ image(Σ)` via the D-CWP bridge, "no pair dropped" ⟺ the stated implication, with the `R = ∅` boundary collapsing to `RE(Σ) = ∅`); and the retraction iff (RE-RET) is correctly conditioned on the unit-depth discipline and the explicit `coverage(Θ) ∩ dom(Σ.C) = ∅` hypothesis, with the field-agreement argument (unit-depth ⟹ prefix-relation ⟹ subspace-identifier clash) sound for the from-/to-endsets and honestly flagged as a hypothesis for the type slot. The worked instance exercises RE-OVL, RE-CLIP, RE-WHOLE, per-endset surfacing, and RE-UNIT against a concrete state. Boundary cases (empty image, no addressable links, empty endset slot, `R = ∅`, sole-bearer retraction) are covered.

My findings are confined to the anti-bloat patterns the classifier directs me to surface: the M-only cross-model lift and its depth caveat are justified repeatedly across three locations.

## REVISE

### Issue 1: The depth-independence caveat of the M-only lift is stated twice in the Stability prose

**ASN-0131, "Stability: the answer as the document is edited"**: The lift paragraph states: "This lift is the load-bearing step, and it is depth-independent: it turns on the edit's write-set being Σ.M(d) alone, not on D-SHIFT's #p = 2, so it covers the delete at every content depth — even where the common content depth m_{s_C} ≥ 2 ... outruns D-SHIFT's depth-2 realisation." The gain/lose paragraph then restates it: "the membership-tracking conclusion resting on the M-only frame, hence holding at every content depth m_{s_C} ≥ 2, even as the concrete gain/lose picture just drawn for the delete instantiates only D-SHIFT's depth-2 displacement (the insert mechanics, I3, being general at every text depth)."

**Problem**: Both passages assert the same fact — the conclusion holds at every content depth `m_{s_C} ≥ 2` despite D-SHIFT being realised only at `#p = 2`, with I3 general. The depth caveat (`m_{s_C} ≥ 2` / D-SHIFT depth-2 / I3 general) is the same content in different words. A reader following the gain/lose discussion must re-process a caveat already established one paragraph earlier. This is the "two paragraphs say the same thing" pattern.

**Required**: Establish depth-independence once (the lift paragraph), and in the gain/lose paragraph reference it rather than re-stating the `m_{s_C} ≥ 2` / D-SHIFT-depth-2 / I3-general triple. The gain/lose paragraph's distinct content (the gain-and-lose picture is the through-region case) does not need the caveat re-argued.

### Issue 2: The RE-EDIT table entry re-derives the M-only lift instead of stating the claim

**ASN-0131, Claims Introduced table, RE-EDIT**: "Over the combined vocabulary of ASN-0047's atomic arrangement movers and ASN-0082's shift-based insert/delete — the latter, as M-only arrangement edits, frame Σ.L, Σ.E, Σ.R by the cross-model lift *M-only ⟹ frames `L`, `E`, `R`* (grounded on the edit's write-set being Σ.M(d) alone, hence depth-independent and covering the delete past D-SHIFT's depth-2 realisation; I3 is general), so addressable/Avail hold fixed and only the image swings..."

**Problem**: This is the third appearance of the M-only lift plus its depth caveat — the entry re-argues the cross-model lift and the D-SHIFT-depth-2 point that the prose has already carried (twice, per Issue 1). A claims-table entry is a structural slot meant to state the guarantee; here it carries the derivation. Measured against the note's own table convention (RE-DEF, RE-OVL, RE-SND, etc. are statement-length), RE-EDIT is an outlier overloaded with justificatory prose. This is essay content in a structural slot.

**Required**: Reduce RE-EDIT to its claim — which transition kinds can move the answer and which leave it fixed (content-subspace movers and shifts on `d`, plus `K.λ`; everything else fixed, including link-subspace-confined edits under `W ⊆ s_C`), with the lift and depth-independence cited to their prose derivation rather than restated.

## OUT_OF_SCOPE

None. The future territory — entirety-vs-touching-spans (OQ1), multiplicity/counting (OQ2), V-rendering (OQ3), intersection-distributivity (OQ4), cross-store completeness (OQ5), type-slot-against-content (OQ6), and link-subspace regions (OQ7) — is correctly left as open questions rather than claimed, and the contrastive mentions of FINDLINKSFROMTOTHREE etc. are not dependencies.

VERDICT: REVISE
