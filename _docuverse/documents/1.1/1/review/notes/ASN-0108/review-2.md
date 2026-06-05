# Review of ASN-0108

## REVISE

### Issue 1: W9a's termination condition uses "below the cursor" with two contradictory meanings
**ASN-0108, W9a (TerminationGuaranteed)**: "Over a *mutating* matching set the loop still terminates whenever the set does not grow without bound below the cursor — but W7 and W6 show that under a non-allocation-monotone key, growth below the cursor is invisible to the loop, so termination reflects exhaustion *of the reachable tail*, not of the matching set as a whole."

**Problem**: The same phrase "below the cursor" is required to mean opposite things in adjacent clauses, and at least one clause is wrong under any fixed reading.
- The loop advances the cursor toward larger keys; `After(c, Σ)` consists of keys *greater* than `κ(c)`. Termination is impeded only by unbounded growth in the tail *ahead* of the cursor (keys `> κ(c)`). Growth at keys `< κ(c)` is behind the cursor and never consumed.
- Clause 1 ("terminates whenever the set does not grow without bound below the cursor") is correct only if "below" means *ahead* (larger key).
- Clause 2 ("growth below the cursor is invisible to the loop") is correct only if "below" means *behind* (smaller key) — that is exactly the W6 silent-skip region.

These cannot both be true. As written, the stated termination condition (clause 1) names the wrong region: growth behind the cursor is invisible and cannot prevent termination, so it cannot be the thing whose boundedness termination "depends on."

**Required**: Fix the directional language. Termination over a mutating set holds when the *reachable tail ahead of the cursor* (keys `> κ(c)`) does not grow without bound; growth *behind* the cursor (keys `< κ(c)`) is invisible (the W6 blind spot) and is precisely why termination reflects exhaustion of the reachable tail rather than of `Match` as a whole. Use one consistent spatial convention throughout.

### Issue 2: W6 reconciliation overstates that an address-based key is allocation-monotone
**ASN-0108, W6 (reconciliation paragraph)**: "An alternative implementation seeking Nelson's guarantee must adopt an allocation-monotone key, which the address-based key supplies directly."

**Problem**: The body of W6 correctly scopes the append-at-tail guarantee to a *single* home document ("the forward hypothesis holds within a single home document's link allocator"; "the hazard vanishes for links homed where the reader is paging"). But `Match(q, Σ)` in general spans multiple home documents whose link allocators advance independently. T9 gives forward ordering only for `same_allocator`; across documents a freshly created link in an earlier-addressed document can receive an address `< κ(c)` for a cursor currently sitting in a later document — the identical silent-skip blind spot W6 attributes only to content-position keys. So the address-based key is *not* globally allocation-monotone, and the unqualified "supplies directly" contradicts the ASN's own first Open Question.

**Required**: Scope the reconciliation sentence: the address-based key supplies allocation-monotonicity (hence append-at-tail) *within a single home document*. For a multi-document matching set, even the address-based key admits the blind spot — and that is exactly the deferred multi-document question. Without this qualification the claim reads as unconditional.

### Issue 3: Mandatory boundary cases are not exercised in the concrete walks
**ASN-0108, W9a (worked examples)**: the two traces are `m = 4, N = 2` and `m = 5, N = 2`.

**Problem**: These cover `N | m` (trailing empty call) and `N ∤ m` (short non-empty terminal window), but omit two boundary regimes the protocol's correctness hinges on:
- *Empty matching set* (`m = 0`): the canonical zero case. The reader calls once at `c = ⊥`, `After(⊥, Σ) = ∅`, `Window = ∅`, next cursor `= ⊥` (unchanged), terminates in 1 call (formula: `⌈0/N⌉ + [N divides 0] = 1`). This is never stated, and the "next cursor = c unchanged if window empty" branch is only exercised here.
- *First window already short* (`N > m`): W4's proof relies on this branch ("when `N` does *not* divide `m`, the final non-empty window is already short") and its induction terminates at the base when `iN > m`, but no concrete trace confirms the single-short-window-from-the-start path or that the rank-block induction degenerates correctly.

**Required**: Add traces (or explicit statements) for `m = 0` and `N > m`, verifying W4's partition/termination and W9's short-window terminator in each.

## OUT_OF_SCOPE

### Topic 1: A global ordering key across independently-advancing multi-document allocators
**Why out of scope**: The ASN already names this as its first Open Question. The body's single-document scoping is the correct boundary for this note; what must be fixed (Issue 2) is only the unqualified reconciliation sentence, not the deferral itself.

### Topic 2: The satisfaction predicate determining `Match(q, Σ)` membership
**Why out of scope**: The ASN explicitly imports `Match` as given and defers which links match to the full-set/count operations. Taking `Match` as a primitive with only (M-fin) and (M-mut) is a sound scoping decision for a windowing note.

VERDICT: REVISE
