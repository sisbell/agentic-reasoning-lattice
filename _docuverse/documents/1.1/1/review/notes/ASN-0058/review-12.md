# Review of ASN-0058

## REVISE

### Issue 1: "Text-subspace" labeling inconsistent with `v₁ ≥ 1`
**ASN-0058, M2 and Definition (Block Decomposition)**: "every arrangement `M(d)` admits a block decomposition of its text subspace"; B1's quantifier `(A v ∈ dom(M(d)) : v₁ ≥ 1 : ...)`.
**Problem**: By S8a, every V-position in `dom(M(d))` satisfies `v₁ ≥ 1` — text (`v₁ = 1`) *and* link (`v₁ = 2`) and any other subspace. The formal range covers all subspaces while the prose claims text-only. M12's proof carries the same inconsistency: "all text-subspace V-positions in `dom(M(d))` share the same depth (S8-depth)" — S8-depth fixes one depth per subspace, not one across all.
**Required**: Choose one. If decomposition is text-only, change `v₁ ≥ 1` to `v₁ = 1` throughout B1 and adjust M12's S8-depth invocation. If decomposition covers every subspace, strike "text-subspace" from M2 and the Definition preamble.

### Issue 2: M0 proof cites TumblerAdd for `j = 0`, where it does not apply
**ASN-0058, M0 proof**: "By TumblerAdd (ASN-0034), `v + j = [v₁, ..., v_m + j]` and `v + k = [v₁, ..., v_m + k]`; when `j ≠ k`, these differ at component `m` ..."
**Problem**: For `j = 0`, `v + 0 = v` is by *convention* (the ASN's own extension), not TumblerAdd — TumblerAdd's precondition `Pos(w)` fails for `δ(0, m)`, which is the zero tumbler. The component formula happens to extend correctly, but citing TumblerAdd at `j = 0` is wrong.
**Required**: Either (i) split the proof into `j = 0` (use the convention plus TS4 for `v < v + k`) and `1 ≤ j < k` (TumblerAdd or TS5), or (ii) replace the TumblerAdd citation with a unified citation of TS5 + TS4 (which subsume both cases without invoking the zero-displacement special case).

### Issue 3: M1 has no derivation
**ASN-0058, M1**: "Within a mapping block `β`, the mapping preserves ordinal position. For all `j, k` with `0 ≤ j < k < n`: `v + j < v + k ∧ a + j < a + k`."
**Problem**: The "justification" is a Nelson quote about endpoints determining interiors. That is commentary on the design choice, not a proof. M1 is derivable — for `j = 0`, TS4 gives `v < shift(v, k)`; for `1 ≤ j < k`, TS5 gives `shift(v, j) < shift(v, k)` — but the ASN never derives it.
**Required**: A short proof citing TS4 (ShiftStrictIncrease) for the `j = 0` case and TS5 (ShiftAmountMonotonicity) for `1 ≤ j < k`. Keep the Nelson quote as motivation, but distinguish motivation from proof.

### Issue 4: M7 necessity for V-adjacency is gesture, not argument
**ASN-0058, M7**: "I-adjacency alone is insufficient: if the V-extents are not adjacent, there is no contiguous V-range for the merged block to cover."
**Problem**: The merged triple `(v₁, a₁, n₁ + n₂)` does have a definite V-extent `{v₁ + k : 0 ≤ k < n₁ + n₂}`. The actual obstruction is: if `v₂ > v₁ + n₁`, then `v₁ + n₁` is either (a) not in `dom(M(d))` — B3 fails for the merged block claiming `M(d)(v₁ + n₁) = a₁ + n₁`; or (b) covered by some other block `β''` — B2 fails between the merged block and `β''`. The I-adjacency-fails case in the same paragraph is argued with this level of specificity; V-adjacency is not.
**Required**: Make the B3/B2 case split explicit, matching the rigor of the I-adjacency necessity argument that immediately precedes it.

### Issue 5: C1a verification of "S8-depth for restrictions" is implicit
**ASN-0058, C1a verification**: "(iii) S8-depth (fixed depth): by C0a, every position in `dom(f)` has first component `u₁`, so `dom(f) ⊆ V_{u₁}(d_s)`; by S8-depth, all positions in `V_{u₁}(d_s)` share the common depth `m`."
**Problem**: S8-depth in ASN-0036 is stated for arrangements `M(d)`, not for arbitrary restrictions. What M11/M12 actually need is that `dom(f)` has a common depth; the proof should make explicit that this follows by inheriting from `V_{u₁}(d_s) ⊇ dom(f)`, not by claiming "S8-depth holds for `f`" as a stand-alone arrangement.
**Required**: Restate the condition M11/M12 require (common depth for the function's domain) and show that this follows from S8-depth on `d_s` plus the inclusion `dom(f) ⊆ V_{u₁}(d_s)`. Avoid the form "S8-depth for `f`," which suggests `f` is an arrangement in its own right.

## OUT_OF_SCOPE

None. The scope statement's "Arrangement canonical decomposition and contiguity invariants" most naturally reads as referring to operation-effects on decompositions and to D-CTG/D-MIN invariants under editing — not to the static algebra of decompositions that this ASN is centrally about. The Open Questions (lattice structure, V-extent vs block-count, cross-source resolution ordering) are correctly flagged as future work.

VERDICT: REVISE
