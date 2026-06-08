# Review of ASN-0110

## REVISE

### Issue 1: RE-anon overclaims that the result yields no lower bound on the total contributing-link count

**ASN-0110, RE-anon (prose) and Claims table**: "Nor does the result yield a lower bound on the total contributing-link count … so the count of distinct endset values present has no general ordering against the link count. The only sound lower bound is stated *per role*: `|Eᵢ(I, Σ)|` lower-bounds the number of distinct links that touch `I` through slot `i`." The table restates: "no lower bound on total link count."

**Problem**: This is false. The per-role bound `|Eᵢ|` is itself a lower bound on the *total* contributing-link count, hence so is `max_i |Eᵢ(I, Σ)|`. Argument: each link has exactly one slot-`i` endset, so two distinct members of `Eᵢ` must come from two distinct links; thus `|Eᵢ| ≤ |{a : (a,i) ∈ W(I,Σ)}| ≤ |{a : (∃i)(a,i) ∈ W(I,Σ)}|` = total contributing links. Therefore `max_i |Eᵢ|` is a sound (computable-from-result) lower bound on the total. The supporting reasoning is only valid for the *combined* distinct-value count across roles (where a single link can inflate the count via multiple roles and shared values can deflate it); it does not license the broader claim about the total link count.

**Required**: Replace "the result does not yield a lower bound on the total contributing-link count" with the correct statement: `max_i |Eᵢ(I, Σ)|` is a sound lower bound on the number of distinct contributing links, while the *exact* count remains undetermined (which is what RE-anon's construction actually shows). Correct the Claims-table row accordingly.

### Issue 2: RE-reveal's single-link example overclaims result-level attribution

**ASN-0110, RE-reveal**: "if exactly one link touches `I` (e.g. the worked instance restricted to `a₂ = (F₂, F₁, Θ)` alone …), each role-family `Eᵢ` holds at most one endset, and the touching endsets returned across roles are trivially attributed to the one link."

**Problem**: RE-reveal is framed as result-level recovery ("From `retrieveendsets(I, Σ)` one recovers…"), but the attribution claimed in the degenerate example requires external knowledge that exactly one link touches — knowledge the result does not carry. The result `⟨{F₂}, {F₁}, ∅⟩` is indistinguishable from a two-link state (one link with `F₂` in slot 1, another with `F₁` in slot 2). So the pairing is *not* recoverable from the result even in this "degenerate" case; recovery holds only under the side condition that the contributing-link count is known to be 1, which (by Issue 1) the result does not determine. The example therefore demonstrates state-level structure, not result-level recoverability.

**Required**: Either qualify the example explicitly as recovery *conditioned on knowing the contributing-link count is 1* (an out-of-band fact, not derivable from the result), or remove the "trivially attributed" claim and rely solely on the hedge + deferral to OQ3.

## OUT_OF_SCOPE

### Topic 1: Precise boundary for per-link pairing reconstructibility
**Why out of scope**: The ASN already defers this to Open Question 3; characterizing exactly when from/to/type pairing is reconstructible is genuinely new territory, not a defect of this operation's specification.

### Topic 2: V-space presentation contract for partially-arranged endsets
**Why out of scope**: The lossy I→V projection of a returned endset is explicitly deferred (Open Question 1); the retrieval operation itself returns whole I-coverage endsets (RE-full), which is fully specified here.

VERDICT: REVISE
