# Channel Assignment — ASN-0099 review-17

**Date:** 2026-05-26 21:08

```
## Issue 1: F4 misattributes witness realizability to L9
Reason: Pure citation correction within the dependency chain — swap L9/L11b for K.λ (ASN-0093) + L4 (ASN-0043). Derivable from the substrate ASNs as already cited elsewhere in F4's text.
```

```
## Issue 2: F4 title and scope mismatch — addresses minimality, not full uniqueness
Reason: Expository decision (retitle to MatchFormulaMinimality and credit F3 for the weakening direction, or extend F4 symmetrically). Internal to ASN-0099's own structure.
```

```
## Issue 3: Edge case `J = ∅` in filtered queries not discussed
Reason: Mechanical boundary case derivable directly from the filtered-form definition — coverage(eᵢ) ∩ ∅ = ∅ trivially fails the universal. Add one sentence to the boundary discussion.
```

```
## Issue 4: F12 type signature ambiguity at the `findlinks_V` precondition
Reason: Definitional choice the ASN must make explicit; (a)/(b)/(c) are all spec-internal options. No design-intent question — the ASN can fix the precondition crisply without external input.
```

```
## Issue 5: Cross-document anchor ordering relies on CrossDocDisjointness for ancestor-descendant case
Reason: Internal authorial decision about whether to lean on foundation lemma or local re-derivation. ASN-0093's CrossDocDisjointness is already in hand; no new evidence needed.
```

```
## Issue 6: A1 introduces a load-bearing assumption about prose of another ASN
Reason: The cleaner path (b) — "K.λ is the unique L-modifying operation in V" — is derivable from ASN-0093's K.λ effect clause and the V-enumeration already established in F9-cor's derivation. Restructuring is internal.
```
