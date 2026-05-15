# Review of ASN-0084

## REVISE

### Issue 1: Helper lemma proof uses right-cancellation on mismatched operands

**ASN-0084, canonical decomposition Step (a), "Existence of a maximum" helper lemma**: "Case A: m + s = B. Then m + s = B = (B − m) + m, and NAT-cancel's right-cancellation property (ASN-0034) yields s = B − m."

**Problem**: NAT-cancel right-cancellation has the form `n + m = p + m ⟹ n = p` — both sides must share the same right operand. In the chain `m + s = (B − m) + m`, the LHS has `s` on the right and the RHS has `m` on the right. These operands are distinct (assuming `s ≠ m` generically), so right-cancellation cannot fire on this equation. Commutativity of NAT addition would salvage the step, but NAT-addcomm is conspicuously absent from the foundation — NAT-addbound's prose ("Both directions are proved separately because addition's commutativity is not assumed") explicitly confirms this. The companion Case B step has the same flaw applied to the strict-inequality form.

**Required**: Use NAT-sub's left-inverse property `n + (m − n) = m` instead of the right-inverse property. Specifically, instantiate left-inverse at `(m, n) = (B, m)` to obtain `m + (B − m) = B`. Combined with the case hypothesis `m + s = B`, this gives `m + s = m + (B − m)`. Now NAT-cancel **left-cancellation** `m + n = m + p ⟹ n = p` matches the form (common left operand `m`) and yields `s = B − m`. Apply the symmetric fix to Case B using the strict version of left order-compatibility's contrapositive. The conclusion is unchanged; only the cited foundation properties need to be swapped.

Note: The involution proof earlier in the same lemma uses right-cancellation correctly — both `(B − (B − s)) + (B − s)` and `s + (B − s)` carry `(B − s)` on the right — so only the "Subtract m from both sides" sub-derivation needs the fix.

## OUT_OF_SCOPE

### Topic 1: Composition of multiple rearrangements
**Why out of scope**: The ASN's Open Questions section explicitly defers this. Whether successive REARRANGE operations factor through a single cut-point form is a separate ASN's territory.

### Topic 2: k-cut rearrangements for k > 4
**Why out of scope**: CS1 fixes n ∈ {3, 4} as a deliberate scope choice. Generalization to richer cut topologies is a future ASN.

### Topic 3: Operations on subspaces other than text at depth 2
**Why out of scope**: The ASN states this restriction openly in its scope paragraph. Link-subspace or deeper-text rearrangements would require their own contiguity and ordering analysis.

### Topic 4: Maximality of B' = R-BLK(B)
**Why out of scope**: R-BLK's closing remark identifies the gap — B' is a valid but possibly non-maximal partition, and the 4-cut worked example exhibits a B/H merge that R-BLK does not perform. Characterizing exactly which pre-state pairs produce post-state mergeability is left to subsequent work.

VERDICT: REVISE
