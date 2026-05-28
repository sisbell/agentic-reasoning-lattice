# Review of ASN-0077

## REVISE

### Issue 1: Cross-ASN reference to ASN-0043 in O0 derivation
**ASN-0077, O0 (b) derivation, third bullet**: "...P3 (ArrangementMutabilityOnly, ASN-0047), whose `dom(L) ⊆ dom(L') ∧ (A ℓ ∈ dom(L) :: L'(ℓ) = L(ℓ))` conjuncts (extending L12 of ASN-0043) discharge link-store append-only behavior across the full transition vocabulary as a labeled foundation invariant" and later "with the L12/P3 invariant forcing those latter transitions to preserve L rather than silently rewrite it."
**Problem**: ASN-0043 is not in the foundation list (0034, 0036, 0040, 0047, 0053, 0058, 0098). Each ASN must be self-contained, citing only foundation ASNs. The substantive claim is already discharged by P3 from foundation ASN-0047; the parenthetical historical reference to L12 of ASN-0043 and the composite "L12/P3" usage violate the no-cross-references rule.
**Required**: Remove the parenthetical "(extending L12 of ASN-0043)" and change "L12/P3 invariant" to "P3 invariant" (citing only ASN-0047).

### Issue 2: Framing convention left implicit in O0 (b) closure step
**ASN-0077, O0 (b) derivation, third bullet**: "every other transition either declares an explicit L' = L frame clause (K.α, K.δ, K.μ~, K.μ⁺_L) or targets only other components (K.μ⁺ and K.μ⁻ on M(d), K.ρ on R), with the L12/P3 invariant forcing those latter transitions to preserve L rather than silently rewrite it."
**Problem**: P3 only guarantees `dom(L) ⊆ dom(L')` (monotonicity) and value preservation on `dom(L)`. It does not preclude K.μ⁺, K.μ⁻, or K.ρ from silently *adding* fresh entries to `dom(L)`. The argument's reliance on P3 to "force preservation" is insufficient for the no-growth conclusion — the actual load-bearing step is the framing convention "components not mentioned in the effect or frame are unchanged." K.μ⁺/K.μ⁻/K.ρ's frame clauses in ASN-0047 do not name L explicitly, so the no-L-growth conclusion rests on this convention, not on P3.
**Required**: Either (a) cite the framing convention explicitly as the basis for L-preservation under K.μ⁺/K.μ⁻/K.ρ and reduce P3's role to value-preservation on `dom(L)`, or (b) verify by inspection of each operation's effect clause that no L-modification is specified, rather than appealing to P3.

VERDICT: REVISE
