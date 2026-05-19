# Channel Assignment — ASN-0093 review-8

**Date:** 2026-05-18 18:41

```
## Issue 1: L1c restatement weakens ASN-0043's L1c without acknowledgment
Reason: The fix is derivable from the ASN alone. The L1c chain exhibition already structurally pins k₁=2 (via the anchor construction `b_C(d) = inc(d, 2)`) and the length-increasing clause follows from TA5(d) at k=2 and TA5(c) preserving length thereafter. Aligning the L1c statement with what the discharge proves, and reconciling the preamble's "inherited" framing with the table's "substrate commitment" framing, are editorial choices the author can make from the ASN's own content.

## Issue 2: ChainPrefixExtension's quantifier scope ambiguous; freshness derivations route through a redundant step-argument detour
Reason: The fix is derivable from the ASN alone. The lemma's induction is over chain indices and SubAllocatorAxiom.ChainDiscipline explicitly defines A_C(d) as the conceptual inc(·, 0)-extension chain rooted at the first emission. Both clarifications — making the quantifier scope explicit and simplifying the freshness derivations to cite ChainPrefixExtension directly at the freshly emitted address — follow from definitions already stated in the substrate.

## Issue 3: K.α and K.λ effect clauses do not state dom(M') = dom(M) explicitly
Reason: The fix is derivable from the ASN alone. Adding `dom(M') = dom(M)` to K.α's and K.λ's Frame clauses alongside the pointwise function equality is a notational precision change requiring no external evidence — the intended semantics is already clear from M1 and the downstream consumers' reliance on M being preserved across these transitions.
```
