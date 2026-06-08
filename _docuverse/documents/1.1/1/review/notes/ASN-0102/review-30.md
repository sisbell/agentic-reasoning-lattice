# Review of ASN-0102

## REVISE

### Issue 1: S8-fin discharge rests on an incorrect justification

**ASN-0102, X14 (invariant-discharge paragraph)**: "...S7a–S7d/S8-fin/S8-depth/C-fin (content store and depths unchanged by X1)."

**Problem**: S8-fin (ASN-0036) is the finiteness of the *per-document arrangement* `dom(Σ.M(d))`, and COPY *grows* that set by `W` positions. The stated justification — "content store and depths unchanged by X1" — establishes nothing about the arrangement domain's cardinality; X1 freezes `Σ.C`, not `Σ.M(d)`. The conjunct happens to hold (pre-state `dom(Σ.M(d))` is finite by S8-fin at Σ, and COPY adds finitely many positions since `W = (+ j : 1 ≤ j ≤ k : n_j)` is a finite sum), but the proof never says so. Lumping S8-fin with the content-store-frozen invariants is a category error.

**Required**: Give S8-fin its own one-line discharge: post-state `dom(Σ'.M(d)) = dom(Σ.M(d)) ∪ {copied positions}` adds exactly `W < ∞` positions to a finite pre-state domain, hence finite.

### Issue 2: S8-depth discharge mis-stated for the empty-subspace first insertion

**ASN-0102, X14**: "...S8-depth... (content store and depths unchanged by X1)."

**Problem**: In the `n_S = 0` case (P4, ValidFirstInsertionPosition), there is no pre-state content-subspace depth — COPY *chooses and pins* `m`. The depth is newly established, not "unchanged." The blanket justification fails to cover precisely the case where S8-depth is first instantiated for subspace `s_C` of `d`. (X16 handles the depth correctly in its parenthetical empty-subspace remark, so the fix is to route the X14 discharge through X16 rather than through "depths unchanged.")

**Required**: Discharge S8-depth via X16 for both cases — inherited `m` when `n_S ≥ 1`, chosen-and-pinned `m` when `n_S = 0` — rather than asserting depths are unchanged.

### Issue 3: Scope-rationale and identity-justification prose (anti-bloat)

**ASN-0102, "Amendment to ValidComposite★"**: "A COPY whose source or target is mutated earlier in the same composite is outside this note's scope; in the integrated model such an edit must be expressed as a separate standalone COPY against the already-committed boundary state."

**ASN-0102, P2**: "These name the same set: in the integrated model K.δ's IsDocument case (ASN-0047) registers a new document into Σ.E and dom(Σ.M) in one indivisible step, so dom(Σ.M) = E_doc is a standing identity at every reachable state."

**Problem**: Both are explanatory accretion around forward/foundation references. The first sentence justifies a scope boundary already fixed by the standalone-composite restriction stated immediately above it; it advances no claim. The second justifies *why* two notations coincide with a mechanism recap, where a bare citation (`dom(Σ.M) = E_doc`, ASN-0047) suffices for the reasoning that follows. Under the active `review-mode.anti-bloat` classifier these are the scope-rationale and definition-justification patterns to remove at source.

**Required**: Drop the scope-rationale sentence (the standalone restriction already excludes the case); compress P2's identity to the citation it rests on.

## OUT_OF_SCOPE

### Topic 1: Re-displacement of copied content, re-transclusion containment, and unreachable-allocator identity
**Why out of scope**: These are the note's own Open Questions and concern operations/states beyond a single COPY (subsequent edits, chained references, allocator reachability) — genuinely future territory, not defects here.

VERDICT: REVISE
