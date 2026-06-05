# Review of ASN-0115

## REVISE

### Issue 1: Open Question 4 is already settled by R5

**ASN-0115, Open Questions**: "What must be guaranteed about the relative ordering of two items drawn from the same address via distinct positions when those positions fall in different specs?"

**Problem**: R5 (OrderFidelity) already fully determines this. R5 states: "the items of ρᵢ wholly precede the items of ρⱼ whenever i < j, irrespective of the relative V-magnitudes of the two specs." Two items in *different specs* are ordered by spec index regardless of V-magnitude — and a fortiori regardless of whether they resolve to a shared address (address-sharing does not change spec membership, and R0 concatenates by spec index `j`, not by address). The worked instance under R8 even exhibits exactly this: `R = ⟨(d, σ_w), (d, σ_u)⟩` with both positions resolving to `a` delivers them in spec order `w` before `u`. So the open question is closed by the ASN's own R5, making its appearance in Open Questions inconsistent.

**Required**: Either remove Open Question 4, or, if a genuine residual remains (e.g., a finer guarantee R5 does not cover), state precisely what R5 leaves open and why the spec-order rule does not settle it.

## OUT_OF_SCOPE

### Topic 1: Inline provenance, single-span subspace straddle, channel faithfulness, unbound-reference delivery

**Why out of scope**: Open Questions 1, 2, 3, 5, and 6 each name territory the ASN deliberately and correctly defers (R9's inline-vs-traceable distinction, R6's authorization/existence boundary, R2's frame limit, and the V-spec ordinal-level restriction excluding straddle spans). These are future ASNs, not errors here. Only Open Question 4 (above) is anomalous.

VERDICT: REVISE
