# Review of ASN-0069

## REVISE

### Issue 1: V11's premise is insufficient for its IH and conclusion when d_src is edited between fork steps

**ASN-0069, V11** (statement and induction): V11's premise constrains "each step's source" — `d^{i-1}_new` for step `i` — between step `(i-1)`'s post-state and step `i`'s pre-state. For `i = 1` (where the source is `d_src`), the premise is vacuous (step 0's post-state ≡ step 1's pre-state by convention). For `i ≥ 2`, the source is `d^{i-1}_new`, not `d_src`. So `d_src` is unconstrained by V11's premise across any gap after step 1.

**Problem**: V11's IH at step `k − 1` states "`M^{k-1}(d^{k-1}_new)(v) = M(d_src)(v)`, both evaluated at the post-state of step `k − 1`." Read literally, `M(d_src)(v)` is at step `(k-1)`'s post-state. But the LHS `M^{k-1}(d^{k-1}_new)(v)` was set at step 1's V4 application to `M(d_src)(v)` at step 1's pre-state and preserved through the chain by V5a (since no step is M-targeted at `d^{k-1}_new` per the premise). For the IH equation to hold at step `(k-1)`'s post-state, `M(d_src)(v)` at step `(k-1)`'s post-state must equal `M(d_src)(v)` at step 1's pre-state — i.e., `d_src` must be unedited across the chain. V11's premise does not ensure this.

Concrete counterexample under the literal reading: with `M(d_src)(v) = a₁` pre-chain, run step 1, then apply K.μ~ on `d_src` so `M(d_src)(v) = a₂`, then run step 2. The premise at `i = 2` is satisfied (`d¹_new`'s content subspace untouched). But `M²(d²_new)(v) = a₁` (inherited via the chain) while `M(d_src)(v) = a₂` at step 2's post-state — the IH's equation fails.

The worked example's wording ("The I-addresses inherited by `d²_new` are still `a₁, a₂, a₃` — the same I-addresses originally allocated by `d_src`") suggests the intent is the *frozen* reading (the value at the chain's initial pre-state). The IH's "both evaluated at the post-state of step `k − 1`" suggests the *current-state* reading. These are inconsistent when `d_src` is edited between fork steps.

**Required**: Either (a) strengthen V11's premise so the per-step source preservation discipline extends to `d_src` across the entire chain (not just at step 1), making "unedited fork chains" in the title match the explicit premise; or (b) reformulate the IH and conclusion so `M(d_src)(v)` explicitly refers to a fixed past state — e.g., "`M^k(d^k_new)(v)` equals the value `M(d_src)(v)` held at the chain's initial pre-state `Σ`" — rather than the current state. The current statement is internally inconsistent in the edited-`d_src` case.

## OUT_OF_SCOPE

(none)

VERDICT: REVISE
