# Cone Review — ASN-0034/T10a.2 (cycle 2)

*2026-04-14 00:45*

I've read the full ASN carefully against the previous findings. One new cross-cutting issue.

### Prefix definition's proper-prefix entailment `#p < #q` depends on T3 but presents it as definitional

**Foundation**: Definition (Prefix), formal contract: "`p ≺ q` iff `p ≼ q ∧ p ≠ q`"
**ASN**: Prefix body text: "A proper prefix `p ≺ q` requires `p ≼ q` with `p ≠ q`, entailing `#p < #q`." T10a.2 proof: "suppose for contradiction that `tᵢ ≼ tⱼ`. Since `tᵢ ≠ tⱼ`, this is a proper prefix relationship, which requires `#tᵢ < #tⱼ` — contradicting `#tᵢ = #tⱼ`."
**Issue**: The Prefix definition presents `#p < #q` as an entailment of `p ≼ q ∧ p ≠ q`, as though it follows from the definition alone. It does not. The derivation requires T3 (CanonicalRepresentation): if `p ≼ q` and `#p = #q`, then the prefix condition `(∀i : 1 ≤ i ≤ #p : qᵢ = pᵢ)` covers all positions of both tumblers, and T3 gives `p = q`, contradicting `p ≠ q`. Without T3, you cannot rule out `#p = #q` — you have componentwise agreement at equal lengths but no axiom to conclude equality of tumblers from it. T10a.2's proof depends on this entailment to derive its contradiction: the entire argument that same-length siblings cannot be proper prefixes of each other routes through this claim. The entailment is also absent from the Prefix formal contract — the contract defines `p ≺ q` as `p ≼ q ∧ p ≠ q` but does not export `#p < #q` as a postcondition. Previous finding #4 identifies T1's dependency on T3; this is a separate consumption point with a different character — the Prefix definition packages a T3-dependent theorem as a definitional consequence, hiding the dependency from both the reader and the formal contract.
**What needs resolving**: Either cite T3 explicitly in the Prefix definition's entailment (making the dependency visible and adding `#p < #q` to the formal contract as a derived postcondition), or redefine proper prefix as `p ≼ q ∧ #p < #q` (which avoids the T3 dependency entirely but changes the definition). T10a.2's proof must then cite whichever resolution is chosen, rather than treating the strict-length inequality as self-evident from the prefix relation.
