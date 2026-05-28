# Review of ASN-0102

## REVISE

### Issue 1: Target subspace never constrained to s_C; wp computed against S3, not S3★
**ASN-0102, "The source designation and its resolution" / "What is preserved: content immutability forces shared reference"**: "a V-position `v` with `subspace(v) = S` that is a valid insertion position of `d`'s subspace `S`" and "`wp(COPY, S3) ⊇ (A j, i : 0 ≤ i < n_j : a_j + i ∈ dom(Σ'.C))`".
**Problem**: The operation copies *content* references, which resolve to addresses in `dom(C)` (C1). But the target subspace `S` is left generic. Under the extended state, the governing invariant is S3★ (ASN-0047): `subspace(v) = s_C ⟹ M(d)(v) ∈ dom(C)` **and** `subspace(v) = s_L ⟹ M(d)(v) ∈ dom(L)`. If `S = s_L`, COPY would bind link-subspace positions to content addresses in `dom(C)`, directly violating S3★. The wp here is computed against the weaker S3 and only checks `dom(Σ'.C)` membership — it never establishes the subspace-routing obligation that S3★ imposes.
**Required**: Add `S = s_C` (content subspace) to the precondition, or otherwise prove the resolved targets land in the subspace S3★ demands. Recompute the wp against S3★, showing the routing conjunct is discharged.

### Issue 2: Post-state density (D-SEQ / no V-gap) is asserted, never derived
**ASN-0102, X15**: "establishing X1, X3, X7, S2, S3, and the subspace's density discipline D-SEQ together" and X7's derivation: "its image lies at or above `v + W`, while the copied region occupies `[v, v+W)`; the two ranges are disjoint."
**Problem**: X7 establishes only *disjointness* (no overwrite), which is the easy half. The hard invariant — that post-state `V_S(d)` is *contiguous* with no gap, i.e. `{[S,1,…,1,c] : 1 ≤ c ≤ n_S + W}` — is never shown. This is exactly the tiling-without-gaps property the review standard flags as most-often hand-waved. X15 asserts D-SEQ "holds together" without derivation.
**Required**: Derive D-SEQ explicitly: unmoved positions occupy `c ∈ [1, p)`, copied occupy `c ∈ [p, p+W)`, displaced occupy `c ∈ [p+W, n_S+W]`, jointly covering `[1, n_S+W]` with no gap. One paragraph, but it must appear.

### Issue 3: Only the leading boundary absorption is considered; X12's "and only then" is unjustified
**ASN-0102, X12**: "The first copied block may absorb into the block immediately preceding `v`, and only then, exactly when they are both V-adjacent and I-adjacent."
**Problem**: The phrase "and only then" claims the leading boundary is the *sole* absorption site. But the trailing boundary — between the last copied block `(…, a_k, n_k)` and the first displaced block at V-start `v+W` with I-start `Σ.M(d)(v)` — is equally a merge candidate (V-adjacent by construction; I-adjacent iff `Σ.M(d)(v) = a_k + n_k`). X12 never addresses it, so "and only then" is false as stated.
**Required**: Treat both boundaries symmetrically, or prove the trailing boundary can never satisfy I-adjacency, justifying the exclusion.

### Issue 4: No concrete worked example
**ASN-0102, throughout**: no specific scenario is verified.
**Problem**: Per the review standard, the ASN must verify its key postconditions against at least one concrete scenario (e.g., COPY a 2-run, cross-origin source of width 4 into a 5-position content subspace at `p = 3`; check X1, X3, X7, X9, X11, and D-SEQ on the result). None is given. Every claim is stated abstractly with no instantiation.
**Required**: Add one worked example exercising the fragmentation (X8), contiguous target (X9), cross-origin separation (X11), and density.

### Issue 5: Precondition is scattered and incomplete
**ASN-0102, "The source designation and its resolution" / Definition of COPY**: the operation gives no consolidated precondition block.
**Problem**: An operation's precondition must be complete. Missing/implicit: (a) `R` is resolvable at the pre-state (each `r_i` well-formed, `V_{S_i}(d_i) ≠ ∅`); (b) the empty-subspace case (`n_S = 0`) — here there is no pre-existing common depth `m`, yet the definition invokes "the common depth `m` (S8-depth)"; the operation must instead invoke `ValidFirstInsertionPosition` and *choose* `m`, and prove D-MIN (`min = [S,1,…,1]`) results; (c) `W ≥ 1` (the empty-copy boundary — vacuously excluded by `p ≥ 1` and C2, but unstated).
**Required**: State a single precondition block covering source resolvability, the empty-subspace/first-insertion case with depth selection, and the width lower bound.

### Issue 6: `resolve(R)` evaluation state not pinned (self-transclusion snapshot)
**ASN-0102, Definition / X10**: "`resolve(R) = ⟨(a₁, n₁), …⟩`" (no state subscript) and X10: "resolution snapshots the source before any displacement, so even self-transclusion with `d_s = d` reads a frozen image."
**Problem**: When `d_s = d`, correctness of the snapshot depends on `resolve(R)` being evaluated against the *pre-state* `Σ`, not the partially-displaced `Σ'.M(d)`. The definition leaves the evaluation point implicit and X10 discharges it by citing Gregory rather than the formal transition semantics.
**Required**: Pin the definition to `resolve_Σ(R)` (pre-state evaluation), and derive the snapshot property from SequentialTransitionAxiom (precondition read against `Σ`) rather than from implementation evidence.

### Issue 7: `wp(COPY, S3) ⊇ …` notation imprecise and partial
**ASN-0102, "What is preserved..."**: "`wp(COPY, S3) ⊇ (A j, i : 0 ≤ i < n_j : a_j + i ∈ dom(Σ'.C))`".
**Problem**: The weakest precondition is a predicate, not a set; `⊇` is the wrong relation and obscures whether this is necessary, sufficient, or both. The quantification also covers only the copied region, omitting displaced bindings (which S3/S3★ must also satisfy in `Σ'`).
**Required**: State wp as an equality/biconditional over *all* post-state mappings of `d`, separating copied (must pre-exist) from displaced (preserved by X1).

### Issue 8: X8 "exactly k blocks" ignores cross-reference coalescence
**ASN-0102, X8**: "The copied region admits a block decomposition with exactly `k` blocks … `k` independent of `W`."
**Problem**: `B_copy` as defined has `k` blocks, but it need not be *maximally merged*. Within one reference, consecutive runs are non-I-adjacent (maximal, M12). Across references, the last block of `r_i` and the first of `r_{i+1}` are V-adjacent and may be I-adjacent (same origin, contiguous), satisfying the merge condition (M7). So the canonical block count can be `< k`. X8 conflates the constructed count with the fragmentation-determined canonical count.
**Required**: Distinguish the constructed `k`-block lay-down from the maximally-merged count; state that cross-reference I-adjacency may coalesce, with equality holding when no inter-reference boundary is I-adjacent.

## OUT_OF_SCOPE

### Topic 1: Self-transclusion with target strictly inside the source span
**Why out of scope**: Correctly deferred to the Open Questions. The basic disjoint self-transclusion snapshot, however, still needs the pre-state evaluation fix in Issue 6 — that is in scope.

### Topic 2: Permanence of containment records across later arrangement contraction
**Why out of scope**: X14's claim that the `Contains_C` record "persists across subsequent states (… even if `d` later drops it)" relies on provenance permanence (P2/P4★, ASN-0047). That permanence is a property of subsequent operations, not of COPY itself; deriving it here is future territory. COPY need only establish the record at completion (the `a_j + i ∈ ran(Σ'.M(d))` half), which it does.

VERDICT: REVISE
