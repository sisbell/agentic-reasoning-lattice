# Review of ASN-0131

I read this as a query operation (RETRIEVEENDSETS) over state: it defines the operation's denotation (RE-DEF), its soundness/completeness, decidability, union-composition, a non-trivial weakest precondition (RE-CWP), a complete transition-impact taxonomy (RE-EDIT), and retraction stability (RE-RET), grounded in a worked instance. It is squarely "operation on state with stability invariants," stated abstractly enough to bind an alternative implementation. I verified the major derivations and the worked example, and the work is unusually thorough — the finite-image-vs-infinite-coverage decidability point, the field-segment-agreement argument for `coverage(e₃) ∩ dom(Σ.C) = ∅`, the RE-CWP wp, and the honest "discipline, not derivation" framing of the retraction type are all correct and well-made. I found one gap in a flagship derived guarantee.

## REVISE

### Issue 1: RE-RET's "iff sole addressable bearer" omits the single-target-scope premise

**ASN-0131, "Under retraction" / RE-RET**: "A pair `(i,e)` that `ℓ` contributed therefore leaves the answer **iff `ℓ` was its sole addressable bearer in `Σ`**: the retraction's own emitter cannot keep it alive, and any other live Σ-bearer does." And in the worked instance: "retracting `ℓ₁` alone leaves `(1, e₁)` in the answer, because the live `ℓ₂` still bears it."

**Problem**: The backward direction (not-sole-bearer ⟹ pair survives) asserts that "any other live Σ-bearer" `ℓ'` still contributes the pair in the post-state — i.e., `ℓ'` remains addressable after `ℓ` is retracted. But "`ℓ'` addressable in `Σ`" does not by itself yield "`ℓ'` addressable in `Σ'`": one must know that retracting `ℓ` enlarges `nullified` by `ℓ` **and no other addressable link**. That is exactly R-Scope (SingleTupleScope, ASN-0086) — `{t : ℓ ≼ t} ∩ A_rel^{Σ'} = {ℓ}`, arity-independent — which itself rests on R0a (FlatLinkDomain: `dom(Σ.L)` is a prefix antichain, so no distinct link satisfies `ℓ ≼ ℓ'`). The derivation cites R6a (permanence of `ℓ`'s own nullification, the *forward* half) but never names the single-target-scope premise the *backward* half depends on. Against the ASN's otherwise meticulous per-step citation discipline (R6a, R6c, L12a, LP16, …), this is a real hole in the chain: absent R-Scope/R0a, the retraction of `ℓ` is not established to leave `ℓ'` addressable, and the "iff" is unproven in the surviving direction — including the concrete `ℓ₂`-survives claim in the worked instance.

**Required**: In RE-RET and the worked-instance retraction paragraph, name the premise and show the chain: for `ℓ'` ∈ addressable(Σ) with `ℓ' ≠ ℓ` — by R0a, `ℓ ⋠ ℓ'`; by R-Scope (ASN-0086), `ℓ' ∉ nullified(Σ')`, so `ℓ' ∈ addressable(Σ')`; by L12 the value is unchanged and the K.λ frame leaves the image fixed, so `ℓ'` still witnesses `(i, e)`. (The forward direction — sole bearer ⟹ drop — is already complete via R6a plus the established content-blindness of the emitter `b`.)

## OUT_OF_SCOPE

### Topic 1: The normative home of the retraction-type seating discipline
RE-RET correctly identifies that `coverage(R) ∩ dom(Σ.C) = ∅` for the designated retraction type is "an imposed layer convention, not a structural fact," and proposes seating `R` at a dedicated subspace `s_R ≠ s_C`. Stating this as the *condition* under which content-region retraction is removal-only is within this ASN's purview, and the conditional framing ("an undisciplined `R` ... would instead surface `b` as `(3, R)`") is exactly right to keep here. Establishing that seating as a *system-wide* allocation/typing invariant, however, belongs to the retraction/allocation layer (the ASN-0086 lineage), not to a query ASN — leave it where it is.

(The ASN's own Open Questions — entirety vs touching-spans, multiplicity collapse, rendered/V-order mode, intersection-distributivity, cross-store completeness, type-slot matching against content, and link-subspace regions — are each appropriately deferred with reasons, and need no further flagging.)

VERDICT: REVISE
