# Cone Review — ASN-0034/TA7a (cycle 2)

*2026-04-26 09:29*

Reading the ASN as a system. Going to focus on findings not already captured in Previous Findings.

### Use-site inventory and defensive justification in T4's Exhaustion Consequence
**Class**: OBSERVE
**Foundation**: T4 (HierarchicalParsing)
**ASN**: T4 *Consequence* slot:
> "The hypothesis is the bound alone — the field-segment constraint of full T4-validity plays no role in the derivation and so does not appear in the quantifier — and the Consequence applies a fortiori at every T4-valid tumbler... Stated under the bound-alone hypothesis so that downstream consumers — T4a (precondition `t ∈ T ∧ zeros(t) ≤ 3` without the field-segment constraint) and T4b (transitively, via T4-validity) — instantiate the cited Consequence directly at their use-site, without a meta-argument about which derivation steps are needed."

**Issue**: The slot mixes the actual Consequence statement with an inventory of which downstream consumers will instantiate it (T4a, T4b) and a defensive justification of why the hypothesis is stated as it is. This is essay content in a structural slot — the kind of meta-prose the reviewer must skip past to find the load-bearing claim. Similar fragments appear in T4's body ("T4 is purely definitional...") and inside T4b's Definition and Postconditions slots, where the same exhaustion-applies-via-T4-validity sentence is restated.

---

### Tail-positivity precondition in TA7a Conjunct 1 spans an automatic position
**Class**: OBSERVE
**Foundation**: ActionPoint postcondition `1 ≤ w_{actionPoint(w)}`
**ASN**: TA7a Conjunct 1 precondition: `(A i : actionPoint(w) ≤ i ≤ #w : wᵢ > 0)`, with proof phrase "by the tail-positivity precondition restricted to its upper sub-range."

**Issue**: The precondition's range begins at `k = actionPoint(w)`, but ActionPoint already supplies `wₖ ≥ 1`, so the `i = k` instance is automatic. The proof itself only consumes the strict sub-range `k < i ≤ #w` (the action-point case is discharged separately via `wₖ ≥ 1` from ActionPoint). The tightest precondition is `(A i : actionPoint(w) < i ≤ #w : wᵢ > 0)`. The current form is sound but slightly looser than the proof requires.

---

VERDICT: OBSERVE

## Result

Cone review converged.

*Elapsed: 2685s*
