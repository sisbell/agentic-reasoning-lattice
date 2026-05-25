# Review of ASN-0069

## REVISE

### Issue 1: V10 framing restricts to consecutive sibling forks
**ASN-0069, V10**: "Let `Σ →* Σ¹` be a fork of `d_src` producing `d_new¹`, and let `Σ¹ →* Σ²` be a later fork of the same `d_src` (read at the post-state of the first fork) producing `d_new²`."

**Problem**: The parenthetical pins Σ¹ as the post-state of the first fork, restricting V10 to the case where the second fork *immediately* follows the first with no intervening transitions. The substance of V10 (distinct identities, independent arrangements, independent provenance) holds far more generally — any two forks of the same `d_src`, regardless of intervening transitions on unrelated documents. V1's subsequent-fork sub-case dispatches correctly at any later state, and T10a.7 gives distinctness across all sibling emissions.

**Required**: Restate V10 so the second fork starts from any state `Σ_g` reachable from `Σ¹` (not specifically `Σ¹`). The derivation already supports this — only the framing needs to admit it.

### Issue 2: K.μ⁺ precondition verification cites V5 at intermediate state
**ASN-0069, "The Fork Composite" verification**: "for every `v ∈ V_{s_C}(d_src)`, the target `M(d_src)(v) ∈ dom(C¹) = dom(C)` (S3★ at d_src restricted to subspace(v) = s_C, ASN-0047, with M¹(d_src) = M(d_src) by V5 carrying the source arrangement unchanged from Σ to Σ¹)"

**Problem**: V5 is stated as `(Σ →* Σ' :: M'(d_src) = M(d_src))` — a property of the *full composite*, not of the intermediate state Σ¹. The fact needed here — `M¹(d_src) = M(d_src)` at the K.μ⁺ pre-state — is supplied directly by K.δ's frame condition (`M¹(d') = M(d')` for `d' ≠ d_new`), which is what V5 itself depends on. Citing the derived composite property where the elementary frame suffices is circular in the verification.

**Required**: Replace the V5 citation with K.δ's frame condition at this step. The substance is unchanged.

### Issue 3: V11's premise wording understates what is actually required
**ASN-0069, V11**: "*no transition between consecutive fork composites modifies any source's arrangement* — that is, the pre-state of each step's fork composite agrees with the post-state of the prior step on all arrangements in the chain"

**Problem**: V11's substance requires only that `V_{s_C}(dⁱ_new)` and the values `M(dⁱ_new)|_{V_{s_C}(dⁱ_new)}` are preserved between steps. A K.μ⁺_L transition (link-subspace extension) on some `dⁱ_new` *does* modify its arrangement but cannot disturb V11's inheritance chain (V4's content-subspace selectivity makes link-subspace untouched). The current premise excludes operations that the conclusion does not actually require to be excluded.

**Required**: Either (a) tighten the premise to exclude only content-subspace modifications (K.μ⁺/K.μ⁻/K.μ~ targeting content positions on a chain source), or (b) keep the conservative premise but note in a remark that it is stronger than necessary.

## OUT_OF_SCOPE

### Topic 1: Concurrency semantics beyond SequentialTransitionAxiom
**Why out of scope**: The ASN correctly defers to ASN-0047's SequentialTransitionAxiom. Open question about concurrent fork-during-edit is a future ASN.

### Topic 2: Fork discoverability from the source's vantage
**Why out of scope**: Whether and how a source owner can enumerate descendants is a separate operation (likely an ENUMERATEVERSIONS-class ASN), not a property of the fork transition itself.

### Topic 3: Snapshot vs. living fork distinction
**Why out of scope**: This ASN commits to snapshot semantics (V4: literal V-position inheritance, V5a: bidirectional independence). Whether an alternative *living* fork operation should exist is a different ASN.

### Topic 4: Fork of a transcludent source
**Why out of scope**: The interaction of fork with `origin(a) ≠ d_src` content already in `M(d_src)` is a property of *transclusion preservation under fork*, distinct from the fork operation itself. Properly handled by the transclusion ASN.

### Topic 5: Bounded-size fork without exhaustive V-position enumeration
**Why out of scope**: Implementation-cost concern, not a property of the abstract transition.

VERDICT: REVISE
