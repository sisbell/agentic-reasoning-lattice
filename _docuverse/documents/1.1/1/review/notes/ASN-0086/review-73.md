# Review of ASN-0086

## REVISE

### Issue 1: R7a discharge (4)(iii) implicitly assumes all `d_k` are fresh

**ASN-0086, R7a proof, discharge (4)(iii) "Iteration in chain-order at each home selects `a_k`"**: "at the first occurrence of `d_k` in the re-ordered enumeration, the homed-set is empty by Δ-membership and the first-emission branch deposits at `[d_k.0.s_L.1]`"

**Problem**: This claim only holds when `d_k` is *fresh* (i.e., added by a K.σ-prefix at this iteration). For an *existing* `d_k ∈ dom(Σ.M)` with pre-existing homed links `H_k ⊆ dom(Σ.L)`, the homed-set at `Σ_{prev}'.L` at the first K.λ iteration at `d_k` is non-empty — by R0a-Cor1 at Σ, `H_k = {inc^j(d_k.0.s_L.1, 0) : 0 ≤ j ≤ J_{d_k}^Σ}`. The first/subsequent predicate evaluates to *subsequent*, not first; K.λ deposits at `inc(ℓ_prev, 0) = inc^{J_{d_k}^Σ + 1}(...)`, which is the first Δ element at `d_k` in chain-order, *not* `[d_k.0.s_L.1]`. The iteration loop earlier in the proof explicitly distinguishes fresh from existing `d_k` (only fresh ones trigger K.σ-prefix), but the chain-order discharge in (4)(iii) collapses this distinction.

**Required**: Either restructure (4)(iii) to split the first-K.λ-iteration-at-`d_k` into two cases (fresh d_k → first-emission branch with `a_k = [d_k.0.s_L.1]`; existing d_k → subsequent-emission branch with `ℓ_prev = inc^{J_{d_k}^Σ}(...)`), or add a sentence acknowledging that the "first occurrence" branch needs `d_k` fresh and stating the parallel argument for existing-`d_k`. The conclusion is the same in either case, but the discharge must show its work.

### Issue 2: R6c-Corollary stated conclusion is strictly narrower than the proof's Step 1 establishes

**ASN-0086, R6c-Corollary**: stated conclusion is "R6c's conclusion extends from `⊑` to `⊑̂`", i.e., `(a, F, G) ∉ A_K^{Σ'}` for the originally retracted tuple.

**Problem**: Step 1 of the proof actually establishes a strictly stronger result: `Σ.L` is pointwise-constant across every arrangement-modifying step, hence `A_K^{Σ_{k+1}} = A_K^{Σ_k}` pointwise (and `L_K`, `L_R`, `nullified` likewise). The Worked Sketch consumes this broader fact when it claims "`A_K^{Σ_2} = {(a₂, F₁, G₁)}` persists across any subsequent arrangement-modifying step `Σ_2 ↦ Σ_arr`" — preservation of `(a₂, F₁, G₁) ∈ A_K`, not just non-membership of the retracted `(a₁, F₁, G₁)`. The Worked Sketch acknowledges the gap parenthetically ("the broader full-`A_K` preservation cited here uses the same L12 + L12a underpinning") but the cite has no named lemma to land on.

**Required**: Either state R6c-Corollary's conclusion as `A_K^{Σ'} = A_K^Σ` for `Σ' ∈ ⊑̂\ ⊑` (a Σ.L-pointwise-constancy lemma covering both directions), or introduce a separate `LinkStoreInvarianceUnderArrangement` lemma that the Worked Sketch can cite by name. The current arrangement — proving more than is stated and asking the reader to recover the broader fact from the proof — is fragile.

### Issue 3: R7a's chain-discipline lemmas discharged via "each transfer through the same construction"

**ASN-0086, R7a "Per-step substrate-invariant discharge" K.λ-step block, *Chain-discipline preservation at the new chain element*"**: "The supporting chain lemmas (ChainEnumerationInjectivity, ChainUniformLength, ChainUniformZeroCount, ChainPrefixExtension, ChainElementT4Validity, DisjointSubAllocatorChains, StoreT4Validity, FirstEmissionFreshness, CrossDocDisjointness) each transfer through the same chain-extension construction: K.λ's deterministic rule respects the chain-discipline structure axiomatized by SubAllocatorAxiom, so each chain-discipline property continues to hold at the extended homed-set."

**Problem**: Nine distinct lemmas are bundled into one sentence with "each transfer through the same construction". The transfer mechanisms genuinely differ — ChainUniformLength needs TA5(c); ChainUniformZeroCount needs T10a.8; ChainPrefixExtension needs TA5(b); FirstEmissionFreshness only fires at first-emission steps and not subsequent ones; CrossDocDisjointness is a structural property at anchors, not chain-extension. Lumping them under "K.λ respects chain-discipline" elides which TA5 / T10a clause discharges which lemma at each step type (K.σ-prefix vs. K.λ-emission, fresh-home vs. existing-home). For an R7a proof whose explicit aim is to demonstrate that no `Σ.L`-affecting transition escapes K.λ, the chain-discipline preservation block is the load-bearing site that distinguishes substrate-conforming from L-invariant-conforming-but-non-chain-emitting layers.

**Required**: Enumerate the chain-discipline lemmas per step type and per mechanism, parallel to the structure used in the four preceding mechanism groups of the same block. At minimum, separate (a) chain-extension lemmas preserved at the new chain element of `A_L(d_k)` (ChainEnumerationInjectivity, ChainUniformLength, ChainUniformZeroCount, ChainPrefixExtension, ChainElementT4Validity, StoreT4Validity), (b) anchor-structural lemmas preserved by frame (DisjointSubAllocatorChains, CrossDocDisjointness), and (c) site-specific lemmas (FirstEmissionFreshness — applicable only on first-emission branch).

### Issue 4: R0 proof, subsequent-emission case — "ℓ_prev is the maximum index"

**ASN-0086, R0 proof, subsequent-emission case**: "By ChainEnumerationInjectivity (ASN-0093) and ChainMembershipForOrigin (ASN-0093), `ℓ_prev` is the maximum index of the contiguous prefix of `A_L(d)`'s realized chain"

**Problem**: `ℓ_prev` is a *tumbler address* (the value at the maximum chain index), not a chain index itself. The K.λ contract defines `ℓ_prev := max{ℓ' ∈ dom(Σ.L) : origin(ℓ') = d}` — the max is taken under tumbler order T1 over a set of addresses. The wording conflates address and index. Minor but recurs in the proof's reading.

**Required**: Rewrite as "`ℓ_prev` is the chain element at the maximum realized index" or "`ℓ_prev` is the T1-max of the contiguous prefix of `A_L(d)`'s realized chain". The chain-extension argument (`inc(ℓ_prev, 0) = next chain element`) is correct either way.

### Issue 5: Definition of `nullified` scope rationale — overweight for its placement

**ASN-0086, Definition of `nullified`, "Scope rationale"**: the paragraph runs ~400 words inside a Definition slot, justifying the restriction `a ∈ A_rel^Σ` against Nelson's design intent and explaining the layer-convention recovery for non-tuple retraction via classifier tuples.

**Problem**: This is design-rationale prose, not mathematical content, embedded in a Definition. A Definition should fix `nullified(Σ)`'s extension and refer downstream consumers (R6a, R6b, Nullify, etc.) to a separate discussion. As written, every reader who reaches the Definition is paying full attention-cost on the rationale even when they want only the membership criterion. The rationale itself is fine — the placement is wrong.

**Required**: Move the design-rationale paragraph to a separate "Design Note" or "Implementation Note" section near the relational-layer discussion, and replace its current inline placement with a single-sentence pointer ("The restriction `a ∈ A_rel^Σ` is intentional; see Design Note: NonTupleRetractionViaClassifierTuples"). Definitions should be terse.

## OUT_OF_SCOPE

### Topic 1: Higher-arity link extension of `L_K^{(n)}` and `A_K^{(n)}`

The note explicitly restricts attention to standard-triple links (|Σ.L(a)| = 3) and notes higher-arity links "exist in dom(Σ.L) but are not members of any L_K". The Open Questions section names this. Extending the active/audit distinction to multi-arity typed relations and characterizing Nullify's effect on higher-arity addresses is genuinely new territory, not a revision of this ASN.

### Topic 2: Concurrent observation consistency model

The Open Questions list ordering guarantees on Observe results and atomicity of Emit relative to concurrent Observe. These are interesting future questions about the substrate's consistency model, not gaps in this ASN's specification.

### Topic 3: Cross-layer type collision

The final Open Question asks what happens when two layers independently choose colliding type addresses under L9 (TypeGhostPermission). This is a multi-layer governance question, properly belonging to a future ASN on layer composition.

VERDICT: REVISE
