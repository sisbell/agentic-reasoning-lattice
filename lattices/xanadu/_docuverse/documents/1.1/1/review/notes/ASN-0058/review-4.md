# Review of ASN-0058

## REVISE

### Issue 1: M12 uniqueness proof — rightward argument not shown

**ASN-0058, CanonicalUniqueness proof (⟹ direction)**: "Hence $v₁ = v₂$; by the symmetric rightward argument, $n₁ = n₂$."

**Problem**: The leftward argument uses condition 2 (left non-extensibility) and constructs an explicit witness $v' = v₁ + (k₂ - 1)$ to contradict $R_2$'s maximality. The rightward argument uses condition 3 (right non-extensibility) and has a different structure: it assumes WLOG $n_1 < n_2$, observes $v_1 + n_1 \in V(R_2)$ (since $v_1 = v_2$ and $n_1 < n_2$), notes $f(v_1 + n_1) = a_1 + n_1$ by condition 1 of $R_2$, and contradicts condition 3 of $R_1$. The two arguments use different maximality conditions on different runs — calling this "symmetric" elides a genuinely different case.

**Required**: Show the rightward argument explicitly. It is short (4–5 lines) and uses condition 3 rather than condition 2, so "symmetric" is misleading. The argument: assume WLOG $n_1 < n_2$; then $v_1 + n_1 \in dom(f)$ (it is in $V(R_2)$ at offset $n_1 < n_2$) and $f(v_1 + n_1) = a_2 + n_1 = a_1 + n_1$ (by condition 1 of $R_2$, since $a_2 = a_1$); this contradicts condition 3 of $R_1$, which requires $v_1 + n_1 \notin dom(f) \lor f(v_1 + n_1) \neq a_1 + n_1$.

## OUT_OF_SCOPE

### Topic 1: Lattice structure of the set of equivalent decompositions
**Why out of scope**: The ASN's open question Q2 identifies this as future algebraic territory. The current ASN establishes the canonical (coarsest) decomposition; the refinement structure among all decompositions is new work.

### Topic 2: Contiguity invariants of the V-domain
**Why out of scope**: The ASN decomposes whatever $dom(M(d))$ happens to be. Whether $dom(M(d))$ is a contiguous V-range (no gaps) is a property of the arrangement layer's invariants, not of the mapping block algebra itself.

VERDICT: REVISE
