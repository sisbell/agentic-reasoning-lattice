# Review of ASN-0075

## REVISE

### Issue 1: Different-origin case in D-ACT conflates two distinct sub-cases

**ASN-0075, D-ACT (Actionability), Case 3 "Different origin"**: "T1 lexicographic comparison applied to `d` and `d'` (with the prefix branch handling the nested case `d ≺ d'` or `d' ≺ d`: at position `min(L_d, L_{d'}) + 1` the shorter prefix's extension carries a zero separator while the longer prefix carries a non-zero component) fixes some position `p` with `d_p ≠ d'_p`..."

**Problem**: The conclusion "fixes some position `p` with `d_p ≠ d'_p`" does not apply to the prefix case. If `d ≺ d'` (which occurs when `d' = inc(d, 1)` — a forked version of `d`, both with `zeros = 2`), then `d` and `d'` agree on all positions where both have values; there is no `p` with `d_p ≠ d'_p`. The parenthetical hints that the witness lies at `min(L_d, L_{d'}) + 1`, but this is a position in the *emissions* (where `A_C(d)`'s emission carries 0 as a separator and `A_C(d')`'s emission carries the inc'd component), not in `d` and `d'` themselves.

**Required**: Either explicitly split into two sub-cases (prefix vs. non-prefix divergence) with separate witness arguments, or introduce a zero-extension convention `d_p = 0 for p > L_d` and state it. Cleanest path: appeal to `b_C(d) < b_C(d')` plus non-nesting and apply PrefixOrderingExtension from the foundation, since `b_C(d) = [d.0.s_C]` carries 0 at position `L_d + 1` while `b_C(d') = [d.1.0.s_C]` (when `d ≺ d'` via fork) carries 1 there.

### Issue 2: wp(SHOWDELETIONS, Q0) derivation elides the subspace step

**ASN-0075, §SHOWDELETIONS Operation, wp(SHOWDELETIONS, Q0) derivation**: "for the conjunct `DELETED(a, d_A) ∧ CURRENT(a, d_B)` to hold, `CURRENT(a, d_B)` requires `a ∈ ran(M(d_B))`, which by `P4★` forces `(a, d_B) ∈ R` — contradiction."

**Problem**: P4★ requires `(a, d_B) ∈ Contains_C(Σ)`, not just `a ∈ ran(M(d_B))`. Contains_C requires a witness `v` with `subspace(v) = s_C`. Reaching that from `a ∈ ran(M(d_B))` requires: `a ∈ dom(C)` (from the `subspace_I(a) = s_C` quantifier) ⟹ `a ∉ dom(L)` (L14) ⟹ the witnessing `v` cannot be in `s_L` (S3★ contrapositive) ⟹ `subspace(v) = s_C` (S3★-aux). D-EXH unpacks exactly this chain four pages earlier; this derivation compresses it to a single inference step.

**Required**: Match D-EXH's level of detail and cite the L14 + S3★-aux + S3★ contrapositive chain that licenses the P4★ application, or cite D-EXH's earlier unpacking by name.

### Issue 3: D-ACT's "consumed without information loss" claim is unsupported

**ASN-0075, D-ACT**: "The witness-run collection can be enumerated, transmitted, and consumed without information loss."

**Problem**: "Consumed" is undefined, and "without information loss" is asserted without proof. The deletion set is recoverable from `{(i_start, ℓ, origin)}` triples via `{shift(i_start, k) : 0 ≤ k < ℓ}`, but this reconstruction isn't shown. Also, "no contiguous extension to the left or right" in the witness-run definition uses "left" informally — OrdinalShift requires `n ≥ 1` (no negative shift), so "left extension of `i_start`" needs predecessor-in-`dom(A_C(origin))` framing.

**Required**: Either remove the "without information loss" claim or sketch the reconstruction: deletion set = ⋃ over runs of `{shift(i_start, k) : 0 ≤ k < ℓ}`, with uniqueness following from the partition uniqueness already established. Formalize the maximality clause by referring to predecessor/successor within `A_C(origin)`'s enumeration.

## OUT_OF_SCOPE

### Topic 1: Link-subspace deletion semantics

**Why out of scope**: D-SUBSP correctly restricts SHOWDELETIONS to `s_C` and explains the structural reason (CL-OWN makes cross-document link comparison ill-formed). A per-document link-deletion operation would be a separate ASN with its own state requirements (e.g., link-provenance, which J1★/J1'★ explicitly do not maintain).

### Topic 2: Restoration operation consuming SHOWDELETIONS output

**Why out of scope**: The §Composability with Restoration section appropriately notes the output's form makes restoration *possible* without specifying it.

VERDICT: REVISE
