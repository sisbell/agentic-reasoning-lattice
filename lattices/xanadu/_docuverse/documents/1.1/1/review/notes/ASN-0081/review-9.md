# Review of ASN-0081

## REVISE

### Issue 1: Missing order-equivalence postcondition for ord/vpos

**ASN-0081, D-BJ proof (a)**: "For any v₁ < v₂ in R, we have ord(v₁) < ord(v₂) (since they share the subspace identifier, the ordering depends only on the ordinal). [...] we conclude ord(v₁) ⊖ w_ord < ord(v₂) ⊖ w_ord, hence σ(v₁) < σ(v₂). ∎"

**Problem**: This proof uses an unstated property at two steps: (a) v₁ < v₂ ⟹ ord(v₁) < ord(v₂) when both share a subspace, and (b) ord(σ(v₁)) < ord(σ(v₂)) ⟹ σ(v₁) < σ(v₂) when both have the same subspace identifier. The same unstated property appears in D-DP's proof ("hence ord(v) < ord(p)"). The property follows from T1 (lexicographic comparison of [S, a] vs [S, b] reduces to comparing a vs b when first components equal), but it is nowhere stated as a postcondition of ord or vpos despite being load-bearing in two separate proofs.

**Required**: State the order-equivalence as a postcondition of ord (or as a joint property of ord/vpos):

```
For V-positions v₁, v₂ with subspace(v₁) = subspace(v₂) and #v₁ = #v₂:
  v₁ < v₂ ⟺ ord(v₁) < ord(v₂)
```

Derive from T1 (shared first component forces lexicographic comparison to the remaining components, which are exactly the ordinal components). Cite this property in D-BJ(a) and D-DP.

## OUT_OF_SCOPE

### Topic 1: Generalization beyond depth-2 V-positions
**Why out of scope**: The scoping axiom (#p = 2) is clearly stated. At depth > 1 ordinals, TA4's zero-prefix condition is no longer vacuous, TA3-strict's equal-length precondition needs justification across deeper ordinal structures, and D-CTG-depth would require non-vacuous proofs. This is acknowledged in the Open Questions section and belongs in a future ASN.

VERDICT: REVISE
