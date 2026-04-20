# Proof Verification: ValidInsertionPosition

I need to verify the ValidInsertionPosition proof against its dependencies and the checklist.

**Working through the checklist:**

1. **Precondition completeness** — The formal contract states: `d satisfies D-CTG, D-MIN, S8-depth, S8a; S ≥ 1`. I'll flag an issue below.

2. **Case coverage** — Two cases (non-empty, empty) are handled. Boundary cases (N=1, depth choices) are addressed. The empty case explicitly argues why m ≥ 2 is necessary.

3. **Postcondition establishment** — Four postconditions are claimed: depth preservation, subspace identity, S8a consistency, distinctness. Each is argued. The subspace identity proof states: "Since δ(j, m) has action point m ≥ 2, TumblerAdd copies component 1 unchanged." This relies on m ≥ 2.

4. **All conjuncts addressed** — All four postconditions have explicit proof paragraphs.

5. **Dependency correctness** — D-MIN (min form), OrdinalShift (result-length identity), TumblerAdd (component behavior), T3 (distinctness), S8-depth (common depth), S8a (well-formedness) — all declared and used. D-CTG is in the preconditions and used indirectly through the D-MIN corollary.

6. **Formal contract** — Has Preconditions, Definition, Postconditions. Structure matches the property type.

7. **Missing guarantees** — Here is the gap:

The non-empty case claims "m ≥ 2, since the first position placed in any subspace is established by the empty case, which requires m ≥ 2, and S8-depth preserves depth thereafter." This is an operational argument — it assumes all positions were placed through ValidInsertionPosition. But the formal contract's preconditions only say `d satisfies D-CTG, D-MIN, S8-depth, S8a`, which do not imply m ≥ 2. A document with V_S(d) = {[S]} (depth m = 1) satisfies all four: D-CTG (trivially, single element), D-MIN (min = [S], vacuously all post-first components are 1), S8-depth (trivially, single element), S8a (zeros([S]) = 0, S ≥ 1, [S] > 0). At m = 1 with N = 1, the definition yields j = 1: shift([S], 1) = [S] ⊕ δ(1,1) = [S] ⊕ [1]; action point is 1, so TumblerAdd gives r₁ = S + 1, producing [S+1] — a position with v₁ = S+1 ≠ S, violating the subspace identity postcondition.

```
RESULT: FOUND

**Problem**: The subspace identity postcondition (v₁ = S) depends on m ≥ 2 so that
δ(j, m) has action point m > 1 and TumblerAdd copies component 1 unchanged. The
non-empty case asserts "m ≥ 2" via an operational argument (the empty case requires
m ≥ 2, S8-depth preserves it), but this argument assumes positions were placed
exclusively through ValidInsertionPosition — an assumption absent from the formal
contract's preconditions. Under the stated preconditions (D-CTG, D-MIN, S8-depth,
S8a), m = 1 is consistent: V_S(d) = {[S]} satisfies all four invariants. At m = 1,
shift([S], 1) = [S+1], which has v₁ = S+1 ≠ S, falsifying the subspace identity
postcondition.

**Required**: Add m ≥ 2 to the formal contract's preconditions for the non-empty
case (e.g., "S8-depth depth m ≥ 2"), or introduce a system-level invariant that
every occupied subspace has depth m ≥ 2 and list it as a dependency. The narrative's
operational justification is sound but needs to be reflected in the formal contract.
```
