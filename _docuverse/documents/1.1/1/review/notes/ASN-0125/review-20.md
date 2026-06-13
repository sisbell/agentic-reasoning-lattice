# Review of ASN-0125

I checked the load-bearing proofs against the substrate they cite. The hard ones hold up: EL0's `wp = false` is L12/LP13 read as a weakest precondition (correct); EL11(a)'s "no content address extends `old(e)`" step is sound (a `t ≽ y` inherits `y`'s three zeros within `1..#y`, exhausting `zeros(t) = 3`, forcing `E(t)₁ = s_L ≠ s_C`); the EL9(2) de-list construction's position-slide, the EL10 re-bind, the EL13 cross-home commutation, and the EL14(c) standoff all compute out correctly against the worked example. The EL-DM induction is not circular (EL6(v)/EL7(vi) are per-operation, discipline-independent for the schema half). I found no correctness errors.

The findings below are prose accretion, which this note's `review-mode.anti-bloat` classifier directs me to surface, plus one clarity defect inside an operation definition.

## REVISE

### Issue 1: A motivational sentence in `editlink`'s definition reasons about a case `DC` excludes
**ASN-0125, EDITop (the paragraph after the `DC` statement)**: "Superseding a retraction is a separate matter, and crucially *not* a retargeting: by R6a (RetractionStability, ASN-0086) a retraction's nullifying effect is permanent, so a successor retraction would *add* a nullified target rather than move one — a retraction-lifecycle question this note leaves to a dedicated treatment (Open Questions)."

**Problem**: This sentence conflates two distinct cases and reasons about the wrong one. "Superseding a retraction" reads as *the original* `a ∈ L_R` — a case editlink **admits**, since `DC` constrains only `ℓ'`, not `a`. But "a successor retraction" is `ℓ'` of retraction class — the case **excluded** by `DC`'s leading conjunct. The "so" glues them: the permanence of `a`'s nullifying effect (R6a, about `a` being a retraction) does not entail anything about `ℓ'` being a retraction. The R6a invocation does no work in the contract — it is motivational prose about a *deferred* topic, occupying a slot that should state what the precondition does and stop. This is exactly the flagged pattern (meta-prose one must untangle to follow the claim; a paragraph reasoning about a case the precondition already excludes). The preceding sentence already discharges the conjunct cleanly ("retraction is Nullify's office, and editlink is supersession").

**Required**: Keep the clean statement and drop the R6a speculation, or — if the "editing a retraction-class original" case is genuinely worth raising — state it precisely (`a ∈ L_R` is admitted; the original retraction persists by L12 and keeps nullifying by R6a; the successor is barred from `[R]` by `DC`) and route it to Open Questions without the `successor → R6a` slippage.

### Issue 2: The "home ≠ named principal" scope caveat is restated three to four times
**ASN-0125, EL8(b)**: "resolving a home further to a named owner is the office of an ownership layer (ASN-0042) overlaid on the substrate, not a function of Σ — an overlay the attribution guarantee neither needs nor invokes"
**ASN-0125, EL3 derivation**: "(resolving that home further to a named principal is an optional ASN-0042 overlay, not a function of the substrate state)"

**Problem**: The same caveat recurs in EL3, EL8(b), and the Claims-table EL8 row, with a fourth variant in EL13. EL8(b) is its natural home (the attribution claim). The EL3 and table instances say the same thing in different words. (The EL13 instance does different work — per-asserter "latest" needs single-home — and can stay.) This is the "two paragraphs say the same thing in different words" pattern, multiplied.

**Required**: State the caveat once at EL8(b) and let the other sites cite EL8 rather than re-deriving the same scope boundary.

### Issue 3: Df-LAY's disambiguation paragraph defends the definition against itself
**ASN-0125, Df-LAY**: "The 'bare K.λ' named here is the *standalone* original-creation operation, distinct from the K.λ step *internal* to editlink — which may carry [K_sup] under DC: the discipline commitment is read at the level of invoked layer operations (editlink is one operation, whose internal emissions DC governs), not as a predicate on individual transitions, which by EL1 cannot record whether a given K.λ 'is part of an editlink.'"

**Problem**: This is defensive prose resolving a tension the definition's own prior sentence creates ("a bare K.λ carrying either class is *not* an editing-layer operation" would otherwise forbid editlink's internal `[K_sup]`-carrying `K.λ`). It does carry some weight — without *something* the definition looks self-contradictory — but the EL1 hedge ("which by EL1 cannot record whether a given K.λ 'is part of an editlink'") is the disposable accretion: it justifies *why* the operation-level reading is chosen rather than stating the rule. The cleaner form is to define "bare K.λ" as standalone original-creation up front, so no after-the-fact reconciliation is needed.

**Required**: Fold the standalone/internal distinction into the operation-set definition where "bare K.λ" first appears, and drop the EL1-anchored justification for the reading.

## OUT_OF_SCOPE

(none — the note stays within EDITLINK: it defines `assert_sup`/`editlink`, the supersession relation, and the currency query; EL11/EL14's discovery of *claims* is the problem statement's explicit "reader's ability to identify the current successor," not general link discovery. The Open Questions are genuinely open and do not double-answer body results.)

VERDICT: REVISE
