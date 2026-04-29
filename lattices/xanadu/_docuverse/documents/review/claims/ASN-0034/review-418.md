# Regional Review — ASN-0034/TA6 (cycle 4)

*2026-04-23 02:28*

### T1 Case k₁ < k₂ elides the k₁ ≤ p chain
**Class**: OBSERVE
**Foundation**: T1 (LexicographicOrder)
**ASN**: T1 transitivity, Case `k₁ < k₂`: "If `a < b` via T1(i): `aₖ₁ < bₖ₁ = cₖ₁` with `k₁ ≤ m`, and the existence of `cₖ₁` gives `k₁ ≤ p`" and similarly "cₖ₁ exists, so `m + 1 ≤ p`" in the T1(ii) sub-case.
**Issue**: The phrase "existence of cₖ₁ gives k₁ ≤ p" is elliptical for the chain (b<c's witness k₂ establishes k₂ ≤ p in both its T1(i) and T1(ii) sub-cases; k₁ < k₂ ≤ p then gives k₁ ≤ p). The adjacent `k₂ < k₁` case performs this kind of splitting explicitly; here the bound is asserted rather than derived. The argument is correct but the phrasing hides the split on how b<c is witnessed.

### TA-PosDom Case #z < k silently converts quantifier ranges
**Class**: OBSERVE
**Foundation**: TA-PosDom (PositiveDominatesZero)
**ASN**: TA-PosDom Case `#z < k`: agreement established as "For `1 ≤ i ≤ #z`, `i < k`, so `tᵢ = 0` … and `zᵢ = 0` …, giving `tᵢ = zᵢ`", then "By T1 case (ii) with witness `#z + 1`, `z < t`."
**Issue**: T1(ii)'s agreement clause at witness `k' = #z + 1` ranges over `1 ≤ i < #z + 1`. The proof establishes the equality on `1 ≤ i ≤ #z`. The equivalence `i ≤ #z ⟺ i < #z + 1` is NAT-discrete, used silently at the witness-substitution step. NAT-discrete is already in Depends for the separate `#z + 1 ≤ #t` step, so this is a phrasing gap, not a missing dependency.

### T4 Axiom slot mixes constraint, stipulation, and derived schema
**Class**: OBSERVE
**Foundation**: T4 (HierarchicalParsing)
**ASN**: T4 Axiom: "Valid address tumblers satisfy: `zeros(t) ≤ 3`; …; `t_{#t} ≠ 0`. T4 stipulates that a position `i` of `t` is a *field separator* iff `tᵢ = 0`. The canonical written form of a T4-valid address tumbler is given by the following schema…".
**Issue**: Three distinct content types sit in the Axiom slot: (a) the four structural constraints (genuine axiom clauses), (b) the stipulative definition of "field separator" (a notational naming, not a constraint), and (c) the per-`k` canonical-form schema, which is a consequence of (a) plus the no-adjacent-zeros and boundary constraints rather than an independent axiom. The mixture reads smoothly but blurs which parts commit new content and which merely name or rearrange.

### T1 trichotomy Case 2 reverse-witness shorthand
**Class**: OBSERVE
**Foundation**: T1 (LexicographicOrder)
**ASN**: T1 trichotomy, Case 2: "If `k' = k`, case (i) requires the opposite inequality at `k`, excluded by NAT-order's trichotomy, and case (ii) requires `k = n + 1` (resp. `m + 1`), contradicting `k ≤ n` (resp. `k ≤ m`). If `k' < k`, … case (ii) requires `k' = n + 1` (or `m + 1`) …".
**Issue**: The "(resp. m+1)" / "(or m+1)" shorthand collapses the two symmetric branches of the sub-split (aₖ < bₖ vs bₖ < aₖ) into one sentence without naming which reverse witness is under analysis in which branch. The pattern is inherited from the prior sub-split and correct under careful reading, but the dual-symmetric notation forces the reader to expand both directions mentally. Also, the ensuing step "contradicting k ≤ n" leaves implicit the NAT-addcompat + irreflexivity move that turns `n + 1 ≤ n` into a contradiction — NAT-addcompat is in Depends and used at the analogous step in sub-case (ii,ii), so the dependency is fine, but the contradiction step at this site is not cited.

VERDICT: OBSERVE

## Result

Regional review converged after 4 cycles.

*Elapsed: 1910s*
