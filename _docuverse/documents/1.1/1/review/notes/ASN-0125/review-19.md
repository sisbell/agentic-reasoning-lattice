# Review of ASN-0125

The note is, with the exceptions below, soundly proved. I checked EL0–EL16 against their cited foundations and traced the worked example address-by-address (ℓ₀=H.0.s_L.1, ℓ₁=H.0.s_L.2, c₁=H.0.s_L.3, the P-chain, the standoff current(ℓ₀)=∅, the repair) — it holds. Boundary cases are covered: the empty store Σ₀ (EL-DM base), first/middle/last de-listing positions (EL9(2)), the fork (EL12), and the mutual-supersession standoff (EL14c). EL5's monotonicity correctly rests on old/new being stable across →* via R0a, and the "K.λ-only composites are valid" and "Layer transfer" lemmas correctly license the ASN-0086 machinery at full ASN-0047 vocabulary. The findings concern the recently-added [R]-route, one terminological ambiguity, and accreted prose.

## REVISE

### Issue 1: editlink's retraction-valued branch is under-specified, and its R6a interaction is unstated

**ASN-0125, EDITop / EL7(iv)**: "(When ℓ' is itself a disciplined retraction, step 1 additionally performs exactly that retraction's declared single-target effect — its purpose, not a side effect — and a stays active unless ℓ' was written against a.)"

**Problem**: This is the only postcondition the note gives for the case where `ℓ'` carries the retraction class — the route the most recent revision added ("add editlink as disciplined [R]-emission route"). Two gaps:

1. **The full `nullified(Σ₂)` is never stated.** For the standard edit the note gives the clean equation `nullified(Σ₂) = nullified(Σ)`. For the retraction branch it gives only `a`'s activity and an indirect "single-target effect." By R-Scope (ASN-0086) the actual postcondition is `nullified(Σ₂) = nullified(Σ) ∪ {target of ℓ'}` — write it.

2. **The R6a interaction is unstated and the operation invites a false reading.** "Editing a retraction" naturally suggests *retargeting* it. But when `a` is itself a retraction `r` targeting `t_old` and `ℓ'` targets `t_new`, `r` persists (L12) and continues to nullify `t_old` (R6a, RetractionStability, ASN-0086). So the edit does **not** move the nullification from `t_old` to `t_new`; it *adds* `t_new` while `t_old` remains nullified — `nullified(Σ₂) ⊇ {t_old, t_new}`. A reader cannot infer this from "step 1 performs that retraction's single-target effect"; EL7(iv) speaks only of `a`'s activity, never of `a`'s *prior* target. The DC retraction clause also imposes no constraint that `a` even be a retraction, so editlink admits "edit a content link into a retraction," whose result (`a` superseded *by a retraction tuple*) the note never addresses.

**Required**: State `nullified(Σ₂) = nullified(Σ) ∪ {ℓ'.e₂ target}` for the retraction branch, and state explicitly that the original retraction's effect persists (so the route does not retarget). If the intended use is attribution-only edits of an existing retraction, restrict DC's retraction clause to the same target (`ℓ'.e₂` covering `a`'s prior target). Otherwise, given the narrowness of the use case and the R6a subtlety, consider whether the [R]-route belongs in *this* note at all rather than a claim/retraction-lifecycle ASN — the DC two-clause predicate and the EL7(vi) three-way case split exist solely to support it.

### Issue 2: Df-LAY's "bare K.λ" is overloaded and the editlink-internal-emission reconciliation is left to the reader

**ASN-0125, Df-LAY**: "...the bare K.λ confined to original-link creation — emission whose slot-3 coverage is neither coverage(K_sup) nor coverage(R)... A bare Emit_{K_sup}, a bare Emit_R, or a bare K.λ carrying either class is not an editing-layer operation; the layer does not issue them."

**Problem**: editlink's step 1 *is* a `K.λ` that, under DC, carries `[K_sup]` or `[R]`. Read against the prohibition on "a bare K.λ carrying either class," this appears to contradict the discipline commitment's "every [R] emission through Nullify or editlink." The note relies (correctly) on the distinction between a *standalone* bare-K.λ-for-originals operation and editlink's *internal* K.λ steps, and on discipline being a protocol property over invoked operations rather than a transition predicate (EL1 establishes that "this step is part of an editlink" is not a state fact). But that reconciliation is never made; the term "bare K.λ" silently shifts between "the original-creation layer operation" and "any standalone substrate step."

**Required**: One sentence distinguishing editlink's internal `K.λ` steps (which may carry disciplined classes under DC) from the standalone bare-`K.λ` operation (which may not), and noting the commitment is read at the level of invoked layer operations.

### Issue 3: accreted prose flagged under the anti-bloat pass

**ASN-0125, EL3 remark 1 (second half)**: "The address-space candidate, closed in EL2(c), still earns a deeper point: the structural reading is refused even where nesting is available. Nelson refuses it for documents... Where not even nesting exists — and for links, by EL2(c), it does not — the refusal is not a choice but a fact."

**Problem**: EL2(c) already closes the address-space carrier formally (`#E = 2`, antichain R0a, version-of-link nesting unreachable). This passage re-opens the closed case to add a document-versioning analogy that does not advance the formal derivation — essay content re-treading a settled point. (The *first* half of the remark — that "separate supersession link" and "typed relation" are one architecture — is substantive and responsive to the problem's menu; keep it.)

A second, milder instance: "Remark (no enforceable coupling)" largely re-derives EL1's conclusion (intent absent from state, resemblance-trigger unsound and evadable); its one new point is that a J-clause coupling constraint cannot mention intent. Tighten to that point.

**Required**: Cut the EL3 remark 1 Nelson elaboration (or compress to a one-clause pointer to EL2(c)); reduce the coupling remark to its J-clause observation.

## OUT_OF_SCOPE

### The deep semantics of claims-targeting-claims and retraction-of-retraction
The note correctly admits meta-claims structurally (assert_sup with a claim endpoint; the [K_sup] editlink route) while deferring their currency well-foundedness to Open Question 3, and `current` remains well-defined (finite `reach_o`) even over them. This deferral is appropriate — flag nothing here. (It does not excuse Issue 1: a route the note *defines* must be fully specified even when its broader semantics are deferred.)

VERDICT: REVISE
