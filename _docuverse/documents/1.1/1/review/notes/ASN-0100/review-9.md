# Review of ASN-0100

## REVISE

### Issue 1: "Shifting both V-start and width by n" misdescribes the Shifted-right blocks

**ASN-0100, §Per-subspace span decomposition (S8★)**: "the Shifted-right blocks (each obtained from a pre-state block by shifting both V-start and width by `n` — preserving I-starts, since shift acts only on V-positions, not I-addresses)"

**Problem**: A pre-state block `(v, a, m)` maps `m` positions starting at V-position `v` to I-addresses `a, a+1, …, a+m−1`. After INSERT, the corresponding Shifted-right block is `(shift(v, n), a, m)` — V-start shifted by `n`, I-start unchanged, **width unchanged at `m`**. The phrase "shifting both V-start and width by n" reads as the width becoming `m + n`, which is wrong: the Shifted-right region has exactly the same number of mapped positions as the pre-state Right region. Concretely: a pre-state block `([1, 5], a, 3)` (mapping [1,5], [1,6], [1,7] to a, a+1, a+2) shifts under `n = 2` to `([1, 7], a, 3)` (mapping [1,7], [1,8], [1,9] to a, a+1, a+2) — not to `([1, 7], a, 5)`.

**Required**: Restate as "shifting V-start by `n`, preserving width and I-start." The S8★ preservation conclusion via M2 is correct; only the constructive sketch is mis-worded.

### Issue 2: Pre-state decomposition need not transfer "unchanged" across the insertion boundary

**ASN-0100, §Per-subspace span decomposition (S8★)**: "the Left blocks (one or more, inherited from the pre-state decomposition unchanged) and the Shifted-right blocks (each obtained from a pre-state block by shifting…)"

**Problem**: The pre-state maximally merged decomposition may contain a block whose V-extent spans the insertion point `p` — for example a single block covering `[1, 1]` through `[1, M]` when `p = [1, p_m]` with `1 < p_m ≤ M`. Such a block cannot be "inherited unchanged" as a Left block; it must be split at `p` into a Left portion (width `p_m − 1`) and a Right portion (width `M − p_m + 1`) that becomes a Shifted-right block. The S8★ existence conclusion (by M2 on the post-state) is unaffected, but the constructive description as written suggests Left blocks transfer without splitting.

**Required**: Note that pre-state blocks crossing `p` are split at `p` before Left/Shifted-right classification, or drop the constructive sketch and rely entirely on M2's existence argument applied to the post-state.

## OUT_OF_SCOPE

### Topic 1: Link-subspace insertion operation
**Why out of scope**: The ASN explicitly limits itself to the content subspace and acknowledges (in §Bounding the Scope and via Open Question 2) that an analogous link-subspace operation belongs in a future ASN.

### Topic 2: Concurrent INSERTs and recovery from partial failure
**Why out of scope**: The composite-atomicity assumption is articulated as a precondition of INSERT (INS.pre); the substrate machinery that secures it and recovery semantics under partial failure are properly deferred to Open Question 1 and to substrate-level specification.

### Topic 3: Derived document-level state (size, last-modified)
**Why out of scope**: INSERT's effect on derived/cached state is correctly identified as out of scope (Open Question 5); the abstract spec governs primitive state components only.

VERDICT: REVISE
