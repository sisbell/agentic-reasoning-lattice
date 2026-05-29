# Review of ASN-0045

## REVISE

### Issue 1: "At-least-one" is grounded in the bijection's domain instead of the arithmetic bound — a circular/non-sequitur derivation

**ASN-0045, Well-Definedness (at-least-one)**: "T4c asserts that `zeros(t) → hierarchical level` is a bijection *on* `{0, 1, 2, 3}`, and a bijection whose domain is `{0, 1, 2, 3}` is precisely the assertion that every T4-valid t has its zero-count in that set. … We need not reconstruct the range from the arithmetic bound `zeros(t) ≤ 3` and a lower anchor: the foundation already delivers the range as the bijection's domain."

**Problem**: This conflates two distinct things: (a) the *domain* of the abstract level-labeling map `zeros-count → level`, and (b) the *range* of the function `zeros(·)` over the T4-valid subdomain. T4c stating its map is "a bijection on {0,1,2,3}" presupposes that the zero-count being labeled is already a member of {0,1,2,3}. To conclude that a *specific* T4-valid `t` has `zeros(t) ∈ {0,1,2,3}`, you must first know `zeros(t)` is a legal domain element — which is exactly what at-least-one needs to establish. Reading the conclusion off the bijection's domain therefore assumes what it sets out to prove.

The non-circular source is precisely the arithmetic route the ASN disclaims: T4's axiom `zeros(t) ≤ 3` together with `zeros(t) ∈ ℕ` (so `zeros(t) ≥ 0`) gives `zeros(t) ∈ {0,1,2,3}`. The ASN's own fourth counter-example `[1,0,1,0,1,0,1,0,1]` (zeros = 4) demonstrates this: it is the bound `zeros(t) ≤ 3`, not the bijection's domain, that excludes the count from the set.

The appeal to surjectivity ("Surjectivity of the bijection further guarantees each of the four values is realized") is also misplaced — surjectivity asserts each level has *some* witness tumbler, which is irrelevant to whether a *fixed* `t` lands in {0,1,2,3}.

**Required**: Ground at-least-one in T4's axiom `zeros(t) ≤ 3` plus `zeros(t) ∈ ℕ` (T0's carrier) to get `zeros(t) ∈ {0,1,2,3}`, then invoke T4c to attach level names. Remove the disclaimer of the arithmetic bound and the irrelevant surjectivity appeal.

### Issue 2: "At-most-one" and the Depends clauses over-attribute disjointness to T4c's injectivity

**ASN-0045, Well-Definedness (at-most-one)** and **Partition / Depends**: "The disjointness thus rests on the functionality of zeros(t) together with T4c's injectivity, which already certifies the four indexing values as pairwise distinct."

**Problem**: Disjointness of the four predicates follows from exactly two facts: (1) `zeros(·)` is single-valued (functionality), and (2) the indices 0,1,2,3 are pairwise distinct *as natural numbers* (trivial from ℕ). T4c's injectivity asserts that *distinct zero-counts map to distinct levels* — a statement about the level codomain. Since each predicate is defined directly as `zeros(t) = k`, never via the level labels, the comparison is between zero-counts, not levels; injectivity does no work. The pairwise distinctness of 0,1,2,3 is a fact about ℕ, not something T4c's injectivity "certifies." The stated dependence is spurious and propagates into the Depends declarations of Partition.

**Required**: State that at-most-one rests solely on functionality of `zeros(·)` (T4) and distinctness of 0,1,2,3 in ℕ (T0). Strike the dependence on T4c's injectivity from both the prose and the Partition Depends clause.

## OUT_OF_SCOPE

None.

VERDICT: REVISE
