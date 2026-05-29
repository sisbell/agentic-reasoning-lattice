# Review of ASN-0040

The construction is unusually careful: every induction handles its frame case explicitly, S(p,d)/S0/S1 are proved rather than asserted, B7's case split is exhaustive and the unequal-length-parents subcase is genuinely closed (not hand-waved), and B8's same-namespace argument correctly drives `m₂ ≥ m₁+1` from B0★ + B1. I checked the freshness argument in Bop, the well-definedness of `next`, and the B7 disjointness cases against the canonical form, and found no errors. The remaining issues are a boundary-coverage gap and minor accretion.

## REVISE

### Issue 1: Concrete trace never reaches the element level — the binding boundary of B6/TA5a is unexercised

**ASN-0040, "A baptism traced"**: The trace runs B₀ → B₄, reaching at deepest `[1,0,1,0,1,1]` with `zeros = 2` (document / sub-document).

**Problem**: B6(iii) is only *binding* at two places, and the trace exercises neither:
- **d = 2 from a document** (`zeros(p) = 2`): produces an element (`zeros = 3`), hitting TA5a's `k = 2 ∧ zeros(t) ≤ 2` boundary exactly. The trace's deepest `d = 2` baptism is Step 3 (user → document, `zeros(p) = 1`, slack of one).
- **d = 1 from an element** (`zeros(p) = 3`): produces a sub-element at TA5a's `k = 1 ∧ zeros(t) ≤ 3` boundary. Step 4 exercises `d = 1` only at `zeros(p) = 2`.

The element level (`zeros = 3`) — the deepest level and the one where the four-level zero budget is saturated — is never concretely baptized. The review standard makes boundary cases mandatory (empty, zero, first, **last**); the *last* hierarchical level and the tightest sufficiency constraint are precisely what the trace skips. B6's sufficiency proof is correct, but its most error-prone case is the one not checked against a concrete address.

**Required**: Extend the trace with at least one element-level baptism — e.g. `next(B₄, [1,0,1,0,1], 2) = inc([1,0,1,0,1], 2) = [1,0,1,0,1,0,1]`, verifying `zeros = 3 = 2 + (2−1)` (B5), B6(iii) at the boundary `zeros(p) = 2 ≤ 2`, and T4-validity of the result (`zeros = 3` permitted, no adjacent zeros). Optionally add a sub-element step (`d = 1` from that element) to exercise the `zeros(p) = 3` boundary.

### Issue 2: B6 necessity re-derives a foundation result the sufficiency direction cites

**ASN-0040, B6 proof, "(⟹) Necessity", condition (ii)**: "Let d ≥ 3. By TA5(d), inc(p, d) appends d − 1 ≥ 2 zeros followed by 1. Positions #p + 1 and #p + 2 are both zero — adjacent zeros … violating T4's non-empty-field constraint."

**Problem**: The sufficiency direction routes the `d ≥ 3` exclusion through TA5a (which already states `inc(t, k)` violates T4 for `k ≥ 3`), but necessity re-proves the same adjacent-zero violation by hand. The two halves of one theorem treat the identical foundation fact inconsistently — one cites, one re-derives. The re-derivation duplicates TA5a's failure clause.

**Required**: Cite TA5a's `k ≥ 3` failure guarantee for the `d ≥ 3` case, matching the sufficiency direction, rather than reconstructing it.

## OUT_OF_SCOPE

### Topic 1: Cross-authority uniqueness in distinct namespaces

B8 Case 2 (different namespaces) relies only on B7 and holds regardless of commit authority, yet B8 is scoped to a single baptismal authority. The cross-replica / shared-namespace concern is correctly deferred in the Open Questions; no action needed here.

VERDICT: REVISE
