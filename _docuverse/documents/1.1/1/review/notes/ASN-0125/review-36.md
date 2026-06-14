# Review of ASN-0125

This is a careful, largely sound note. I checked EL0's wp argument, the EL-DM induction over the editing-layer operations, the EL6/EL7 operation contracts (including the wp Case 2 active-at-birth derivation, which correctly uses R0a *at Σ′* to place the fresh emitter outside every pre-existing unit-depth retraction coverage), the EL9–EL16 consequence chain, and the worked example (the five-entry H/P trajectory is internally consistent down to the chain addresses). The proofs hold and the boundary cases the rubric demands — empty store (Σ₀ base), first emission, j=1/j=n de-listing, the `current(y)=∅` standoff, self-emit retraction targets — are all addressed. One defect remains.

## REVISE

### Issue 1: "bare K.λ" is a defined term used to mean its explicit opposite

**ASN-0125, Df-LAY**: "the *bare* K.λ — a standalone link allocation the layer issues directly, **as distinct from the K.λ step internal to editlink (which may itself carry [K_sup] under DC)** — *confined to original-link creation*: emission whose slot-3 coverage is neither coverage(K_sup) nor coverage(R)."

**ASN-0125, EL7(vi)**: "Step 1, **the bare K.λ(d_s, a', ℓ')**, preserves Df-DISC: ... The successor a' is a claim at Σ₁ ... iff |ℓ'| = 3 ∧ coverage(ℓ'.e₃) = coverage(K_sup)".

**Problem**: Df-LAY reserves "bare K.λ" for the *standalone* original-creation transition, **explicitly distinguished from editlink's internal K.λ** and **confined to slot-3 coverage ≠ K_sup and ≠ R**. EL7(vi) then applies the term "bare K.λ" to exactly editlink's internal step 1 — the thing Df-LAY said the bare K.λ is *not* — and analyzes the case where that step carries `coverage(K_sup)`, a value Df-LAY's bare K.λ cannot have. The defined term, in EL7(vi), denotes its own complement.

This is not only cosmetic: it muddies the EL-DM induction. EL-DM's step enumerates "L-framing transitions and original-creating bare K.λ" as one editing-layer operation and "editlink" (via EL7vi) as a separate one. The induction is only non-double-counting if EL-DM's "bare K.λ" excludes editlink's internal emission — which is precisely what Df-LAY asserts and EL7(vi)'s naming denies. A reader checking that the operation enumeration partitions cleanly is left unable to decide what "bare K.λ" covers.

**Anti-bloat angle**: Df-LAY introduces the distinction through a forward-referencing parenthetical (editlink is defined two sections later), and the clarification is then duplicated verbatim in the Claims-Introduced table ("the bare (standalone) K.λ — distinct from editlink's internal K.λ step, which may carry [K_sup] under DC"). A clarifying parenthetical stated twice and contradicted by the body is accreted prose that has stopped doing its job.

**Required**: Make the term consistent. The smaller edit is (a): in EL7(vi), rename step 1 from "the bare K.λ" to "step 1's internal K.λ" (or "editlink's raw K.λ step"), honoring Df-LAY's distinction and keeping EL-DM's operation enumeration unambiguous. Alternatively (b): drop the "bare/standalone" reservation and the duplicated table clarification entirely, and name the layer's two K.λ uses precisely wherever each appears. Either way the parenthetical-plus-table duplication should collapse to a single, respected term.

## OUT_OF_SCOPE

None. The note stays within supersession: it *uses* foundation operations (K.μ⁻/K.μ⁺_L in the EL9(2) de-listing construction, Nullify, Emit_K/Observe_K) rather than redefining them, and the nine Open Questions correctly defer authority (ASN-0042 overlay), meta-claim well-foundedness, and span-level endset correspondence to future work. The reliance of EL6(iv)'s E/R frame on ASN-0047's K.λ (rather than ASN-0086's three-component Emit_K) is adequately covered by the Layer-transfer paragraph and is not a finding.

VERDICT: REVISE
