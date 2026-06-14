# Review of ASN-0131

I worked through every introduced claim. The mathematics is sound: I verified the `⊆` direction of RE-UDIST-∩, both intersection counterexamples (including that the *injective* one defeats `⊇`), the necessary-and-sufficient touch-implication, the RE-ADDR antichain argument, the RE-RET forward/backward bearer argument (via R-Scope), and the RE-CWP weakest precondition (`coverage(e) ∩ Δ ≠ ∅ ⟹ coverage(e) ∩ I_R ≠ ∅`, with the `R = ∅` collapse). The worked instance correctly exercises RE-OVL/RE-CLIP/RE-WHOLE/RE-UNIT and the `coverage(e₃) ∩ dom(Σ.C) = ∅` field-agreement argument checks out. The `Σ.L`-evolution bridge is a legitimate (if dense) justification for transferring ASN-0086's `∀`-lemmas, and only `K.λ` touches `Σ.L` across the ASN-0047 vocabulary, so the bridge's premise holds.

The findings are organizational — accreted meta-prose around the forward references, which is exactly what this note's `review-mode.anti-bloat` classifier targets.

## REVISE

### Issue 1: RE-UDIST-∩ settled-status and structural-form content is triplicated

**ASN-0131, "Composing regions: union-distributivity" + Claims table (RE-UDIST-∩) + Open Question 4**

The same three ideas — (a) the touch-implication is the settled N&S characterisation, (b) no arrangement restriction recovers `⊇` (injective counterexample), (c) the *structurally-restricted sufficient* form is what remains open — are stated in full at three sites.

Body: *"What one would prefer is a structural condition that discharges the touch-implication without the per-endset quantifier... a two-lever sufficient form... The weakest such structurally-restricted sufficient condition — phrased on coverage and image structure directly, with the per-endset `touch` quantifier eliminated — is what Open Question 4 asks for; the exact touch-implication itself is settled here and is not at issue there."*

OQ4: *"...what is the weakest structurally-restricted sufficient condition for it... (for instance, a single-meet cardinality bound on each coverage against the union image together with the image-distribution gap...), with the per-endset `touch` quantifier eliminated?"*

The claims-table row for RE-UDIST-∩ then restates the obstructions, the settled status, and the open structural form a third time — at paragraph length, where every other row is one line.

**Problem**: The "two-lever / single-meet cardinality bound + image-distribution gap" candidate form appears in both the body and OQ4; the "settled, not open" framing (*"nothing in it remains to be discovered. Its defect is not soundness but form..."*, *"is settled here and is not at issue there"*) reads as a defense against re-litigation of a recently-changed status, not as advancing the argument. This is meta-prose accreted around the OQ4 forward reference — a reader must skip past status-defense and a pre-loaded answer-sketch to reach the actual content.

**Required**: State the diagnosis once in the body (two obstructions → no arrangement restriction suffices → touch-implication is the N&S characterisation), drop the "settled, not open / not at issue there" defensive framing to a clause, and let OQ4 ask only its forward question (the weakest structural-sufficient form) without re-establishing what the body settled. Compress the claims-table row to a one-line summary matching the other rows.

### Issue 2: RE-ADDR — a reusable lemma — is established inside the intersection composition argument

**ASN-0131, "Composing regions: union-distributivity"**: *"The construction turns on one general fact about emission, which we establish here. Write `Θ` for ASN-0086's designated retraction type... Hence the reusable fact — fresh-output addressability (RE-ADDR)..."*

**Problem**: RE-ADDR is a general, reusable fact about `K.λ` emissions (also load-bearing for RE-RET's "the emitter `b` is addressable" step and for asserting the counterexample links are addressable). Establishing it mid-proof of intersection composition — between the `⊆` derivation and the counterexamples — buries a foundational lemma in a downstream argument and forces the intersection narrative to detour through a full antichain/unit-depth proof before resuming.

**Required**: Lift RE-ADDR to its own slot near the `addressable(Σ)` definition (where addressability is first introduced), and cite it from the intersection counterexamples and from RE-RET, rather than proving it inline at first use.

## OUT_OF_SCOPE

None to add. Open Questions 1–7 correctly fence future territory (whole-vs-touching-spans, multiplicity, rendered answers, the structural-sufficient intersection condition, cross-store completeness, type-slot/content matching, link-subspace regions), and RE-UNIT properly positions RE as distinct from the identity-enumeration siblings (FINDLINKSFROMTOTHREE, etc.) without claiming their territory.

VERDICT: REVISE
