# Review of ASN-0087

## REVISE

### Issue 1: Forward-reference accretion around the reflexive-authoring route (WP Case 2)

**ASN-0087, *Inputs* / *What Is Indexed?* / *A Worked Example***:
- *Inputs* ("Address predictability"): "This predictability is what makes reflexive authoring possible (see *Weakest Precondition for Discoverability*, Case 2)."
- *What Is Indexed?*: "(A second, reflexive route is available to the home document alone; it is derived in *Weakest Precondition for Discoverability*, Case 2.)"
- *A Worked Example* (reflexive variant): "the caller must *predict* `ℓ = [d, 0, 2, 1]` from `Σ` via `A_L(d)`'s deterministic first-emission rule — see *Address predictability* in *Inputs*".

**Problem**: Three separate sections orbit the single downstream derivation in WP Case 2. *Inputs* and *What Is Indexed?* both forward-point to Case 2; the worked example then back-points to *Inputs*. This is the "multiple paragraphs in different sections defer to the same downstream location" pattern, plus a bidirectional pointer (*Inputs* ↔ worked example). The "Address predictability" paragraph itself exists only to license the reflexive route — it reads as content accreted to support a forward reference rather than advancing the operation's definition at its own site.

**Required**: Consolidate the predictability/reflexive discussion at the one site where it is load-bearing (WP Case 2), and remove the anticipatory forward pointers in *Inputs* and *What Is Indexed?* and the back-pointer in the worked example. State `ℓ`'s determinacy once where it is used.

### Issue 2: Redundant paragraph in *What Does Not Change*

**ASN-0087, *What Does Not Change***: Paragraph 2 ("This is not a separate guarantee... Neither operation touches `C`... The bytes remain where they were.") and paragraph 3 ("That creating a link has zero effect on referenced content — Nelson's phenomenology — is structural, not behavioral...").

**Problem**: Paragraph 3 restates paragraph 2's conclusion in different words. "Zero effect on referenced content" repeats "the bytes remain where they were"; "structural, not behavioral" repeats "not a separate guarantee... a direct consequence of the composite's structure." Two paragraphs saying the same thing.

**Required**: Delete paragraph 3, folding the single substantive addition (Nelson attribution, if wanted) into paragraph 2.

### Issue 3: Non-sequitur justification in the Effect frame

**ASN-0087, *Effect***: "`Σ'.R = Σ.R` [no provenance — provenance applies to content subspace only]" (and the parallel bracketed gloss `[no entity allocation]`).

**Problem**: `Σ'.R = Σ.R` holds because neither K.λ nor K.μ⁺_L touches `R` (frame), not because "provenance applies to the content subspace only." The bracketed clause is a justification of a different claim (why a link earns no provenance record) attached to a frame fact that needs no such reason. It is meta-prose in a structural slot.

**Required**: State the frame fact from the component frames (K.λ, K.μ⁺_L hold `R` fixed). If the content-subspace-only observation is worth keeping, it belongs in the J1★ discharge in *Invariant Preservation*, where it already appears.

## OUT_OF_SCOPE

### Topic 1: Well-formedness of forward-reaching endsets

The first and fourth *Open Questions* (constraints on endsets whose spans reference not-yet-allocated addresses; discoverability once that content is created) are genuine but belong to a future ASN refining `StandardAuthoring` / L4 generality. Correctly posed as open, not asserted here.

### Topic 2: Protocol-layer atomicity for `Σ_mid`

The *Atomicity* section correctly defers composite-level atomicity to the protocol layer rather than inventing a substrate mechanism. This is appropriate scoping, not a gap.

The substantive proofs check out: the S2 freshness argument (within-subspace via D-SEQ★ strict inequality, cross-subspace via SC-NEQ) is thorough, the D-SEQ★/S8★ post-state cases are handled, the worked example concretely verifies discoverability with correct prefix tests, and the wp analysis treats a non-trivial postcondition with both Case-1/Case-2 branches and the standard-authoring reduction. The findings are confined to meta-prose accretion.

VERDICT: REVISE
