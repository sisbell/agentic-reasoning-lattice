# Review of ASN-0086

## REVISE

### Issue 1: `#E(a')` count in Appendix B is wrong

**ASN-0086, Appendix B, failure mode (a) concrete instantiation**: "`#E(a') = 4 ≥ 2` (element fields `1, 1, 1, 2.1.1`)"

**Problem**: For `a' = 1.0.1.0.1.0.2.1.1` (length 9) with zeros at positions 2, 4, 6, T4b's E-projection gives `E(a') = positions 7..9 = [2, 1, 1]`, so `#E(a') = 3`, not 4. L1b's threshold `#E ≥ 2` is satisfied either way, but the stated count is inconsistent with the `#E` notation used throughout (where `#E` denotes the length of the E field, per L1b and the worked sketch's earlier `#E(a₁) = #E(b₁) = #E(a₂) = #E(b₂) = 2`).

**Required**: Correct to `#E(a') = 3`, or clarify the notation if a different convention is intended (and update L1b's threshold accordingly).

### Issue 2: "Prefix ending at second zero" in Appendix B is wrong

**ASN-0086, Appendix B, failure mode (a) concrete instantiation**: "`home(a') = 1.0.1.0.1 = d ∈ dom(Σ.M)` (the prefix ending at `a'`'s second zero)"

**Problem**: `home(a') = 1.0.1.0.1` has length 5 and ends at position 5 (the D component, immediately before `a'`'s third zero at position 6). The second zero of `a'` is at position 4; a prefix ending there would have length 4. This contradicts R0a Stage 1's own correct formulation: "The `home` prefix has length `p₃ − 1` (the positions up to and including `D(·)`, which immediately precedes the third zero)."

**Required**: Correct to "the prefix ending just before `a'`'s third zero" (or "of length 5, ending at the D component").

### Issue 3: "Sibling siblings" typo in Worked Sketch Step 3

**ASN-0086, Worked Sketch, Step 3 (concrete), P3 discharge**: "`a₁ = 1.0.1.0.1.0.2.1` and `a₂ = 1.0.1.0.1.0.2.3` are sibling siblings in the depth-2 allocator `A_{a₁}`"

**Problem**: "sibling siblings" is a typo; the next sentence uses "siblings" correctly for `b₁` and `a₂`.

**Required**: Correct to "are siblings in the depth-2 allocator `A_{a₁}`".

## OUT_OF_SCOPE

### Topic 1: Concurrent semantics of Emit and Observe
**Why out of scope**: Explicitly listed in Open Questions; defining a concurrency model is a future ASN.

### Topic 2: Multi-arity active subsets `A_K^{(n)}`
**Why out of scope**: The note scopes `A_K` to standard-triple links and flags `A_K^{(n)}` as an open question.

### Topic 3: Substrate-level discharge of the Setup hypothesis and Subspace-distinctness axiom
**Why out of scope**: Both are flagged as "external constraints on emission policy" with explicit "future work" notes; tightening ASN-0036's class-(ii) emission primitive to require `subspace_I(c) = s_C` and elevating `s_C ≠ s_L` to a foundation axiom are future-ASN concerns.

### Topic 4: Substrate-level elevation of the sibling-frontier discipline
**Why out of scope**: Listed in Open Questions; tightening Emit_K's specification or the substrate emission primitive to enforce prefix-incomparability with `dom(Σ.L)` would discharge R0a's discipline-conditionality but is reserved for future work.

### Topic 5: Relaxing the discipline to admit deeper-sited link addresses
**Why out of scope**: Listed in Open Questions; relaxing R0a-Cor2's `#E = 2` narrowing to allow Nelson's design-intent `#E ≥ 3` requires reformulating R0a over a tree of allocators and is a separate future ASN.

VERDICT: REVISE
