# Review of ASN-0069

## REVISE

### Issue 1: V11's inductive step double-counts V5 invocations

**ASN-0069, "Composability: Fork of a Fork" / V11 proof**:

> "1. *Source-arrangement preservation.* V5 applied to the k-th fork composite with `d^{k-1}_new` as source gives `M^k(d^{k-1}_new) = M^{k-1}(d^{k-1}_new)` ..."
> "2. *Literal inheritance.* V4 applied to the k-th fork gives `M^k(d^k_new)(v) = M^k(d^{k-1}_new)(v)` ..."

**Problem**: V4's literal statement is `M'(d_new)(v) = M(d_src)(v)` — post-fork M' on LHS, **pre-fork** M on RHS. At step k, V4 gives `M^k(d^k_new)(v) = M^{k-1}(d^{k-1}_new)(v)`, NOT `M^k(d^k_new)(v) = M^k(d^{k-1}_new)(v)` as the proof asserts. The "post-fork = post-fork (source)" form requires V5 implicitly to convert V4's RHS. Step 1 then invokes V5 again explicitly. V5 is double-counted.

**Required**: Either (a) use V4 directly with two steps (`M^k(d^k_new)(v) =[V4] M^{k-1}(d^{k-1}_new)(v) =[IH] M(d_src)(v)`), or (b) cite V8 (which has the post-post form) at Step 2 instead of "V4" so V5's role is non-redundant.

### Issue 2: V10's notation conflates parallel and sequential forks

**ASN-0069, V10**: "Two forks of the same source, `Σ →* Σ¹` producing `d¹_new` and `Σ →* Σ²` producing `d²_new`, are independent in three senses..."

**Problem**: Both arrows start from the same `Σ`. If both forks fire from the same pre-state where `A_v(d_src)` has emitted nothing, both are first forks and both produce `inc(d_src, 1)` — contradicting V10(a). The proof's appeal to T10a.7 (EnumerationInjectivity) only distinguishes emissions at different enumeration indices, which presupposes sequential ordering, not parallel branches.

**Required**: Clarify that the two forks are *sequential* (the second fork happens after the first, with `d²_new = inc(d¹_new, 0)` per V1's subsequent-fork rule). Use distinct symbols, e.g., `Σ →* Σ¹` and `Σ¹ →* Σ²`.

### Issue 3: Undefined reference "P.2" in K.μ⁺ verification

**ASN-0069, "The Fork Composite" verification**: "Strict extension: `V_{s_C}(d_src) ≠ ∅` by P.2."

**Problem**: No P.1 or P.2 is defined in the ASN. Likely a leftover label from an earlier draft naming the preconditions.

**Required**: Replace with an explicit reference — e.g., "by the non-empty-source case hypothesis" or the actual V0 precondition citation.

### Issue 4: V6's subspace-identifier justification cites the wrong property

**ASN-0069, V6 derivation**: "K.μ⁺ in J4's clause (ii) extends `M'(d_new)` only with positions drawn from `V_{s_C}(d_src)`, all of which have `subspace(v) = s_C` (S8a's positive-component property applied at depth `m_{s_C}` with first component `s_C`)."

**Problem**: S8a establishes zero-count, depth bound, and componentwise positivity — it does *not* establish that the first component equals `s_C`. The reason positions in `V_{s_C}(d_src)` have `subspace(v) = s_C` is by definition of `V_{s_C}(d_src) := {v ∈ dom(M(d_src)) : subspace(v) = s_C}`, not from S8a.

**Required**: Cite the definition of `V_{s_C}(d_src)` (ASN-0047) as the source of subspace identity; S8a is relevant only for positivity and depth.

### Issue 5: V_{s_C}(d_new) = V_{s_C}(d_src) exact equality not stated

**ASN-0069, V4**: "`(A v ∈ V_{s_C}(d_src) :: v ∈ dom(M'(d_new)) ∧ M'(d_new)(v) = M(d_src)(v))`"

**Problem**: V4 establishes one-way containment `V_{s_C}(d_src) ⊆ dom(M'(d_new))`. The verification implicitly shows `dom(M'(d_new)) = V_{s_C}(d_src)` (K.δ initializes to ∅, K.μ⁺ adds exactly these positions, K.ρ doesn't touch arrangements). The exact equality `V_{s_C}(d_new) = V_{s_C}(d_src)` is load-bearing for V8 and V11 but not named.

**Required**: Add a property (or sub-clause of V4 or V6) stating `dom(M'(d_new)) = V_{s_C}(d_src)` exactly, and thereby `V_{s_C}(d_new) = V_{s_C}(d_src)`.

### Issue 6: V8b's "preserve or shrink this inclusion but never violate it" is unclear

**ASN-0069, V8b**: "V8 establishes `V_{s_C}(d_src)|_{Σ'} ⊆ Corr_{Σ'}` at the post-fork state; each subsequent transition can preserve or shrink this inclusion but never violate it."

**Problem**: The inclusion `V_{s_C}(d_src)|_{Σ'} ⊆ Corr_{Σ'}` is a fixed claim about state Σ'. It cannot "shrink" — what shrinks is the set `{v ∈ V_{s_C}(d_src)|_{Σ'} : v ∈ Corr_g}` as g advances. "Never violate it" is also unclear: presumably means "Corr_g restricted to fork-time positions is monotonically decreasing in g."

**Required**: Restate as a monotonicity claim about a clearly-named time-indexed set, e.g., "Let `Π_g := V_{s_C}(d_src)|_{Σ'} ∩ Corr_g`. Then for any subsequent state `Σ_h` (h after g), `Π_h ⊆ Π_g`."

### Issue 7: K.μ⁺ verification cites S3 instead of S3★

**ASN-0069, "The Fork Composite" verification**: "for every `v ∈ V_{s_C}(d_src)`, the target `M(d_src)(v) ∈ dom(C¹) = dom(C)` (S3 at `d_src`, ASN-0036)"

**Problem**: In the ASN-0047 extended state (the substrate ASN-0069 operates on), S3 is *superseded* by S3★ (GeneralizedReferentialIntegrity). The proof should cite S3★ for consistency with the extended-state vocabulary.

**Required**: Replace "S3 at d_src, ASN-0036" with "S3★ at d_src restricted to subspace = s_C, ASN-0047".

### Issue 8: Worked example covers only first-fork case

**ASN-0069, "Worked Example"**: "A fork of `d_src` produces `d_new = inc(d_src, 1)`."

**Problem**: The example illustrates V1's first-fork sub-case (K.δ at k=1) but not the subsequent-fork sub-case (K.δ at k=0 via `inc(d_prev, 0)`). The subsequent-fork sub-case is a deviation from J4 that the ASN explicitly admits as an extension and deserves a concrete illustration to verify V1, V2, V10, and V11 against a non-first-fork scenario.

**Required**: Extend the worked example with a second fork of the same source, showing `d²_new = inc(d¹_new, 0)`, verifying that V2's prefix-ancestry chain holds (`d_src ≼ d²_new`), and confirming V10(a) (`d¹_new ≠ d²_new`).

## OUT_OF_SCOPE

No items — the ASN's Open Questions section already enumerates the topics deferred to future ASNs (concurrency, version DAG structure, snapshot vs. living fork semantics, transcludent source forks).

VERDICT: REVISE
