# Review of ASN-0076

## REVISE

### Issue 1: Missing intermediate step in #E ≥ 2 induction
**ASN-0076, §E0 (successor step discharge of `#E(ℓ_new) ≥ 2`)**: "the step case — subsequent emission — preserves #E by TA5(c), since inc(·, 0) does not change tumbler length."
**Problem**: TA5(c) establishes only `#t' = #t` (total tumbler length preserved). The step from total-length preservation to element-field-length preservation requires an explicit intermediate step: since `inc(·, 0)` modifies only `sig(t)` (which is `#t` for T4-valid `t` by TA5-SigValid), and that position was non-zero before the increment and remains non-zero after, `zeros(t)` is unchanged. Only with `#t` and `zeros(t)` both preserved does the T4 field decomposition remain identical, yielding `#E(t') = #E(t)`. The conclusion is correct, but the chain "length preserved ⟹ #E preserved" is not immediate from TA5(c) alone.
**Required**: Add the explicit zeros-preservation observation in the step case, citing TA5-SigValid for `sig(t) = #t` on T4-valid outputs and arguing that incrementing a non-zero component leaves it non-zero (T0 closure under successor), so `zeros(t)` is preserved and the field decomposition — and hence `#E` — is preserved.

### Issue 2: Misleading L1c citation in E2 distinctness argument
**ASN-0076, §E2 second paragraph**: "More structurally: L11a (LinkUniqueness, ASN-0043) guarantees that distinct T10a-conforming allocation events produce distinct link addresses. The allocation events producing ℓ_old, ℓ_new, and ℓ_sup are pairwise distinct (they fire at distinct states, and L1c's chain-existential admits each independently), so their outputs are pairwise distinct addresses."
**Problem**: L1c (LinkAllocatorConformance) is a per-link existence-of-chain invariant; it does not establish that the three K.λ events are pairwise distinct. The correct citation for distinctness of the three events is SequentialTransitionAxiom (ASN-0047), which makes transitions atomic and totally ordered — so the three K.λ firings occur at three distinct time points. The "fire at distinct states" half of the parenthetical is right; the "L1c's chain-existential admits each independently" half mis-attributes the distinctness.
**Required**: Replace the L1c citation here with SequentialTransitionAxiom, or strike the parenthetical entirely (the "fire at distinct states" observation alone, combined with L11a, suffices).

### Issue 3: Maximality argument at Step 2 leaves prefix structure implicit
**ASN-0076, §E0 (supersession step, identification of `ℓ_sup`)**: "By T10a.7 (EnumerationInjectivity, ASN-0034) applied to A_L(d_new), the enumeration of dom(A_L(d_new)) is strictly increasing under T1, so ℓ_new — the most recently emitted output of A_L(d_new) in dom(Σ_1.L) — strictly exceeds every prior output and is therefore the maximum."
**Problem**: T10a.7 establishes strict monotonicity of the full allocator enumeration `t_0, t_1, t_2, …`, but the K.λ rule's `max` ranges over `{ℓ' ∈ dom(Σ_1.L) : origin(ℓ') = d_new}` — a subset whose maximum being `ℓ_new` requires that no later element of the enumeration (i.e., one that strictly exceeds `ℓ_new` under T1) sits in `dom(Σ_1.L)`. This holds because K.λ advances the prefix of `A_L(d_new)`'s enumeration by exactly one element per fire (so the set is always an initial segment of the enumeration), but the argument is left implicit.
**Required**: Add a one-line observation that the set is an initial segment of `A_L(d_new)`'s enumeration (by induction over K.λ fires on `d_new`), so its maximum is the most recently emitted element.

## OUT_OF_SCOPE

None — the ASN's Open Questions appropriately defer downstream concerns (supersession chains, multi-link supersession, type-endset convention for `τ_sup`, resolution policy, interaction with content edits). No additional deferrals are warranted.

VERDICT: REVISE
