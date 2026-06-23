I worked through the four claims as a connected system — tracing SC's exhaustiveness, S6's length chain, WF's endpoint construction, and S11c's two element-chases — and then walked every precondition chain that crosses a claim boundary.

The mathematics holds up. SC's five-case split is exhaustive and mutually exclusive under T1's trichotomy, and the half-open convention is applied consistently (adjacency case (ii) correctly places the shared boundary in β only). S6's chain `#reach(σ) = #(s⊕ℓ) = #ℓ = #s` is properly gated on TumblerAdd's preconditions. WF correctly eliminates T1 case (ii) from `#s = #r`, lands `(s,r)` in Divergence case (i), and discharges all five of D1's preconditions plus T12's well-formedness via TumblerSub. S11c's Case 1 (`start(α)` endpoints, level_compat direct) and Case 2 (`reach` endpoints, carrier via TumblerAdd, length via S6) both ground WF's preconditions, and the two cases exactly cover SC case (iii)'s two forms. The worked examples compute correctly. The `WLOG`/symmetry deferrals are explicitly justified (each case clause is symmetric or carries an "or symmetrically" rider), so they are not hand-waves.

What I did find is reviser drift — sound content sitting in the wrong slots, in some places triplicated.

### S11c Axiom slot holds precondition-discharge proof, not an axiom
**Class**: OBSERVE
**Foundation**: TumblerAdd, S6, WF (referenced)
**ASN**: S11c *Axiom* — "In Case 2, where the witness γ' = (reach(β), reach(α) ⊖ reach(β)) draws both endpoints from reaches, TumblerAdd's carrier postcondition a ⊕ w ∈ T ... places reach(β) ∈ T and reach(α) ∈ T, discharging WF's carrier preconditions ... WF's length precondition for that witness, #reach(β) = #reach(α), is discharged by S6: ..."
**Issue**: The Axiom slot should state the external fact the claim takes as given — the half-open denotation convention. Instead it re-runs the proof's discharge of WF's carrier and length preconditions. That reasoning already appears verbatim in the Case 2 proof body *and* again in the TumblerAdd and S6 *Depends* entries. It is the same paragraph in three structural slots; the precise reader must verify it is identical each time rather than reading one axiom.
**What needs resolving**: Reduce the Axiom slot to the denotation/half-open convention it actually fixes. The WF-precondition discharge is correctly stated in the proof body and need not be repeated in the Axiom or Depends slots.

### S6 Depends carries a use-site inventory of foundations that don't apply
**Class**: OBSERVE
**Foundation**: TumblerAdd
**ASN**: S6 *Depends* (TumblerAdd) — "This is the sole source of the addition result-length: the in-scope foundations supply only the subtraction length (TumblerSub: #(a ⊖ w) = L) and the round-trip identity (D1: a ⊕ (b ⊖ a) = b), neither of which yields #(s ⊕ ℓ) = #ℓ for a general width ℓ."
**Issue**: A Depends entry should state what TumblerAdd supplies and how it is instantiated. The trailing enumeration of what TumblerSub and D1 do *not* supply is a use-site inventory / defensive justification — content the reader skips past to reach the actual dependency. The "sole source" claim is true, but stating it requires surveying the rest of the cone, which is not this entry's job.
**What needs resolving**: Drop the "sole source / neither of which" enumeration; keep the statement that TumblerAdd supplies `#(a⊕w)=#w` and how S6 instantiates it at `(s, ℓ)`.

### S11c attributes a technique to "S11", which is absent from scope and Depends
**Class**: OBSERVE
**Foundation**: N/A (intra-ASN reference)
**ASN**: S11c Case 2 — "Unlike Case 1's γ ... WF's carrier preconditions reach(β) ∈ T and reach(α) ∈ T are not immediate and must be discharged first. We do so as S11 does: each span σ ∈ {α, β} is well-formed, so start(σ) ∈ T, width(σ) ∈ T, Pos(width(σ)), and actionPoint(width(σ)) ≤ #start(σ) hold ..."
**Issue**: "as S11 does" cites a claim S11 that is neither in the reviewed ASN content nor in S11c's *Depends* list. The carrier-discharge technique is then spelled out fully inline, so the reference carries no logical weight — but it is a dangling attribution. If S11 is the claim that actually establishes this discharge pattern, it belongs in Depends; if it is just decorative, it points the reader at something unreachable.
**What needs resolving**: Either confirm S11 exists as a sibling claim and add it to S11c's Depends (if the technique is genuinely inherited from it), or drop the "as S11 does" attribution since the reasoning is given in full inline. (Upgrade to REVISE if S11 does not exist anywhere — then it is an unresolved reference.)

A lighter note in the same vein: S11c's Case 2 inclusion proof narrates its own structure ("which is sound but discards information the converse must restore"; "we recover the discarded guard start(α) ≤ t that membership in ⟦α⟧ demands but the displayed range omits"). The underlying case-split on the `≤`-clause is necessary and correct — T1 exports only strict transitivity — so this is signposting, not a defect, but it is prose the reader steps around rather than reasoning that advances the claim. Folded here rather than raised separately.

VERDICT: OBSERVE