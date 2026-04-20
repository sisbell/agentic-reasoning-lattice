# Cone Review — ASN-0036/S8-depth (cycle 1)

*2026-04-15 09:35*

Now I have all the file contents I need. Let me trace through the critical cross-cutting chains.

From D-CTG.md, the formal invariant is:

`(A d ∈ D, S, u, w, v : u ∈ V_S(d) ∧ w ∈ V_S(d) ∧ v ∈ T ∧ v₁ = S ∧ u ≤_T v ∧ v ≤_T w : v ∈ dom(Σ.M(d)))`

The quantifier on `v` requires only `v ∈ T ∧ v₁ = S` — no depth restriction. And the body text confirms: "the invariant quantifies over all `v ∈ T`."

From T1.md, the order extends across depths via case (ii): `a` is a proper prefix of `b` implies `a <_T b`. This is also confirmed by the T10a-N foundation statement, which invokes "T1 case (ii)" for prefix comparisons between tumblers of different lengths.

From D-MIN.md, postcondition 1 argues: "Since `V_S(d)` is a non-empty contiguous interval in this space, and `[S, 1, …, 1]` is the absolute minimum of the space, `[S, 1, …, 1]` must be the lower endpoint of the interval — hence `min_S(d) ∈ V_S(d)`."

---

# Cone Review — ASN-0036/D-MIN — cycle 3

*2026-04-15*

### D-CTG's unrestricted quantifier over T jointly contradicts S8-depth and S8-fin via T1's cross-depth ordering

**Foundation**: T1 (LexicographicOrder, ASN-0034) — case (ii): if `a` is a proper prefix of `b` then `a <_T b`. S8-depth — invariant: all V-positions in a subspace share the same tumbler depth. S8-fin — invariant: `V_S(d)` is finite for every document and subspace.
**ASN**: D-CTG (VContiguity) — formal invariant: `(A d ∈ D, S, u, w, v : u ∈ V_S(d) ∧ w ∈ V_S(d) ∧ v ∈ T ∧ v₁ = S ∧ u ≤_T v ∧ v ≤_T w : v ∈ dom(Σ.M(d)))`. Body text: "the invariant quantifies over all `v ∈ T`."
**Issue**: The quantifier on `v` imposes `v ∈ T ∧ v₁ = S` but no depth constraint (`#v = #u` or equivalent). T1 case (ii) orders across depths: any tumbler is less than any extension of itself. Take `u = [S, 1]` and `w = [S, 3]` in `V_S(d)` at depth 2. The tumbler `v = [S, 1, k]` for any `k ∈ ℕ` satisfies `v ∈ T`, `v₁ = S`, and `u <_T v <_T w` — because `[S, 1]` is a proper prefix of `[S, 1, k]` (T1 case ii), and at position 2, `1 < 3` gives `[S, 1, k] <_T [S, 3]` (T1 case i). D-CTG therefore requires every `[S, 1, k]` for `k ∈ ℕ` to be in `dom(Σ.M(d))`. Since `subspace([S, 1, k]) = S`, all such tumblers land in `V_S(d)`. But `V_S(d)` is finite (S8-fin) and uniform-depth (S8-depth), and there are infinitely many `[S, 1, k]` at depth 3. The three invariants — D-CTG, S8-depth, S8-fin — are jointly unsatisfiable for any state where a subspace has two or more V-positions. This is not a gap in a single proof but an inconsistency across the invariant system: no reachable state with a non-trivial subspace can satisfy all three. Downstream properties — D-MIN, S8-crun, D-SEQ, ValidInsertionPosition — all cite D-CTG and therefore build on an inconsistent foundation.
**What needs resolving**: D-CTG's formal invariant must restrict `v` to same-depth intermediates — e.g., `#v = #u` — so that the contiguity claim ranges only over tumblers that could actually be V-positions of the same subspace without violating S8-depth and S8-fin. D-CTG-depth may already provide the correct depth-restricted formulation; if so, the formal invariant in D-CTG must be reconciled with it, and downstream dependents should cite whichever property carries the correct scope.

---

### D-MIN's postcondition 1 conflates convexity with initial-segment, leaving membership of `[S, 1, …, 1]` in `V_S(d)` unproved

**Foundation**: D-CTG (VContiguity) — establishes that `V_S(d)` is convex (no gaps between any two members under T1). S8a — all V-position components are ≥ 1.
**ASN**: D-MIN (VMinimumPosition) — postcondition 1: "`min_S(d) ∈ V_S(d)`." Argument: "Since `V_S(d)` is a non-empty contiguous interval in this space, and `[S, 1, …, 1]` is the absolute minimum of the space, `[S, 1, …, 1]` must be the lower endpoint of the interval — hence `min_S(d) ∈ V_S(d)`."
**Issue**: D-CTG provides convexity: for any `u, w ∈ V_S(d)`, every intermediate `v` (same subspace) between them is also in `dom(Σ.M(d))`. This is the no-gaps property. The argument infers that a non-empty convex subset of an ordered space must start at the space's absolute minimum. This is false: `{[S, 3], [S, 4], [S, 5]}` is convex in the T1 order among depth-2, subspace-S tumblers, but does not contain `[S, 1]`. The step from "contiguous interval" to "lower endpoint is the absolute minimum" requires a stronger property — that `V_S(d)` is an initial segment (downward-closed), not merely convex. No cited property provides downward closure. The claim that `[S, 1, …, 1] ∈ V_S(d)` whenever `V_S(d) ≠ ∅` is architecturally plausible (initial allocation starts at ordinal 1), but proving it requires an inductive argument about how each operation in Op maintains the minimum: INSERT must place the first position at `[S, 1, …, 1]`, and DELETE must not remove `[S, 1, …, 1]` while other positions remain. Neither AX-5's case split nor D-CTG's convexity establishes this. The gap propagates to S8-crun and D-SEQ, which depend on `min_S(d)` being a member of `V_S(d)` to characterize the run structure.
**What needs resolving**: D-MIN's postcondition 1 requires either (a) a separate invariant establishing that `V_S(d)` is downward-closed (or specifically that the absolute minimum is always present when `V_S(d) ≠ ∅`), proved by induction over the operation history, or (b) a re-definition of `min_S(d)` as the T1-minimum of the finite non-empty set `V_S(d)` (which exists and is a member trivially), with a separate theorem characterizing its value as `[S, 1, …, 1]` when the initial-segment property holds.
