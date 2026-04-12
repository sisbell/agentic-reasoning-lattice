# Formalize — ASN-0036 / S8

*2026-04-12 16:22*

**S8 (Finite span decomposition).** For each document `d`, the arrangement `{(v, Σ.M(d)(v)) : v ∈ dom(Σ.M(d))}` can be decomposed into a finite set of correspondence runs `{(vⱼ, aⱼ, nⱼ)}` such that:

(a) The runs partition the V-positions: every V-position in `dom(Σ.M(d))` falls in exactly one run — `(A v ∈ dom(Σ.M(d)) :: (E! j :: vⱼ ≤ v < vⱼ + nⱼ))`

(b) Within each run: `Σ.M(d)(vⱼ + k) = aⱼ + k` for all `k` with `0 ≤ k < nⱼ`

Each run represents a contiguous block of content that entered the arrangement as a unit — characters typed sequentially, or a span transcluded whole.

*Proof.* We construct a finite decomposition satisfying both conjuncts and prove it partitions `dom(M(d))`.

**Existence.** By S8-fin, `dom(M(d))` is finite. By S2 (ArrangementFunctionality), `M(d)` is a function, so each `v ∈ dom(M(d))` has a uniquely determined image `a = M(d)(v)`. For each such `v`, form the singleton run `(v, a, 1)`. Conjunct (b) requires `M(d)(v + k) = a + k` for all `k` with `0 ≤ k < 1` — the only such `k` is `0`, giving `M(d)(v) = a`, which holds by construction. Since `dom(M(d))` is finite, the collection of singletons is finite.

**Coverage.** Each `v ∈ dom(M(d))` lies in its own singleton's interval: `v ≤ v < v + 1`, where the right inequality holds because `v + 1 = inc(v, 0) > v` by TA5(a). So every V-position falls in at least one run.

**Uniqueness within a subspace.** Let `v, w ∈ dom(M(d))` be distinct V-positions with `v₁ = w₁ = S`. By S8-depth, `#v = #w = m` for some common depth `m`. We show `w ∉ [v, v + 1)`.

By S8a, `zeros(v) = 0`, so every component of `v` is nonzero and `sig(v) = max({i : 1 ≤ i ≤ m ∧ vᵢ ≠ 0}) = m`. By TA5(c), `v + 1 = inc(v, 0)` satisfies `#(v + 1) = m` and differs from `v` only at position `m`, with `(v + 1)_m = v_m + 1`. In particular, `(v + 1)ᵢ = vᵢ` for all `i < m`.

Suppose for contradiction that `t ≠ v` satisfies `#t = m` and `v ≤ t < v + 1`. Since `#t = #v = m`, the sequences diverge at some first position `j ≤ m`.

*Case j < m.* Then `tᵢ = vᵢ` for `i < j` and `tⱼ > vⱼ` (from `v ≤ t` by T1(i), since `j ≤ m = min(m, m)`). Since `(v + 1)ⱼ = vⱼ` (as `j < m`), and `tᵢ = vᵢ = (v + 1)ᵢ` for `i < j`, the first divergence between `t` and `v + 1` is at position `j` with `tⱼ > (v + 1)ⱼ`, giving `t > v + 1` by T1(i) — contradicting `t < v + 1`.

*Case j = m.* Then `tᵢ = vᵢ` for `i < m`, so `tᵢ = (v + 1)ᵢ` for `i < m` as well. The first divergence between `t` and `v + 1` is at position `m`. From `v ≤ t` with first divergence at `m`: `t_m ≥ v_m` by T1(i). From `t < v + 1` with first divergence at `m`: `t_m < (v + 1)_m = v_m + 1` by T1(i). Since components are natural numbers, `v_m ≤ t_m < v_m + 1` forces `t_m = v_m`. But then `t` agrees with `v` at all `m` components with `#t = #v = m`, so `t = v` by T3 (CanonicalRepresentation, ASN-0034) — contradicting `t ≠ v`.

Both cases yield contradictions. Since all V-positions in subspace `S` have depth `m` (S8-depth), no distinct V-position in the same subspace falls in `v`'s singleton interval.

*Remark.* S8-depth is essential. Without it, `dom(M(d))` could contain `s.3` (depth 2) and `s.3.1` (depth 3). By T1(ii), `s.3 < s.3.1` (prefix extension), and by T1(i) at position 2, `s.3.1 < s.4`. The position `s.3.1` would fall in the singleton interval of both `s.3` and `s.3.1` — violating unique partition.

**Uniqueness across subspaces.** Let `v ∈ dom(M(d))` with `v₁ = S₁` and `w ∈ dom(M(d))` with `w₁ = S₂`, where `S₁ ≠ S₂`. By S8a, `v` extends the single-component prefix `[S₁]` and `w` extends `[S₂]`. These prefixes are non-nesting: `[S₁] ≼ [S₂]` would require `S₁ = S₂` (both length-1 tumblers, so equality requires componentwise agreement by T3), contradicting `S₁ ≠ S₂`; symmetrically `[S₂] ⋠ [S₁]`.

For `m = 1`, each subspace `S` contains at most one V-position: the only depth-1 tumbler with first component `S` is `[S]` itself (by T3, any other depth-1 tumbler `[k]` with `k = S` is the same tumbler). The singleton interval `[[S], [S] + 1) = [[S], [S + 1])` at depth 1 contains no other depth-1 tumbler: `S ≤ k < S + 1` with `k ∈ ℕ` forces `k = S`. Within-subspace uniqueness is immediate.

For cross-subspace uniqueness at `m = 1`, we must show that no V-position from subspace `S₂ ≠ S₁`, at any depth, falls in `[[S₁], [S₁ + 1])`. The interval contains every proper extension of `[S₁]` (by T1(ii), `[S₁] < [S₁, x, ...]`, and by T1(i), `[S₁, x, ...] < [S₁ + 1]` since the first component `S₁ < S₁ + 1`), so we cannot restrict attention to depth-1 tumblers. We show every tumbler `t` in the interval has `t₁ = S₁`. From `[S₁] ≤ t`: if `t₁ < S₁` then `t < [S₁]` by T1(i), contradicting the lower bound; so `t₁ ≥ S₁`. From `t < [S₁ + 1]`: if `t₁ > S₁` then `t₁ ≥ S₁ + 1`, and either (i) `t₁ > S₁ + 1`, giving `t > [S₁ + 1]` by T1(i), or (ii) `t₁ = S₁ + 1` with `#t = 1`, giving `t = [S₁ + 1]`, or (iii) `t₁ = S₁ + 1` with `#t > 1`, giving `t > [S₁ + 1]` by T1(ii) — all contradicting `t < [S₁ + 1]`; so `t₁ ≤ S₁`. Combined: `t₁ = S₁`. Since any V-position `w` in subspace `S₂ ≠ S₁` has `w₁ = S₂ ≠ S₁` (by S8a), `w` cannot belong to `[[S₁], [S₁ + 1])`. Cross-subspace uniqueness holds at `m = 1`.

For `m ≥ 2`, the successor `v + 1` also extends `[S₁]`: since `sig(v) = m ≥ 2`, TA5(b) gives `(v + 1)ᵢ = vᵢ` for all `i < sig(v)`, so in particular `(v + 1)₁ = v₁ = S₁`.

Since `[S₁] ≼ v` and `[S₁] ≼ (v + 1)` and `v ≤ v + 1` by TA5(a), T5 (ContiguousSubtrees, ASN-0034) gives: for any `t` with `v ≤ t ≤ v + 1`, `[S₁] ≼ t`. Every element of `[v, v + 1)` therefore extends `[S₁]`. By T10 (ASN-0034), since `[S₁]` and `[S₂]` are non-nesting prefixes, any tumbler extending `[S₁]` is distinct from any tumbler extending `[S₂]`. In particular, `w` (which extends `[S₂]`) cannot belong to `[v, v + 1)`.

**Conclusion.** The singleton runs cover every V-position in `dom(M(d))` (coverage) and no V-position falls in two distinct singleton intervals (uniqueness within and across subspaces). The singletons partition `dom(M(d))`. Since `dom(M(d))` is finite (S8-fin), the decomposition is finite, establishing both conjuncts (a) and (b). ∎

*Formal Contract:*
- *Preconditions:* `dom(M(d))` finite (S8-fin); `M(d)` a function (S2); `(A v ∈ dom(M(d)) :: zeros(v) = 0 ∧ v₁ ≥ 1)` (S8a); within each subspace, all V-positions share a common depth (S8-depth).
- *Postconditions:* There exists a finite set of correspondence runs `{(vⱼ, aⱼ, nⱼ)}` satisfying (a) `(A v ∈ dom(M(d)) :: (E! j :: vⱼ ≤ v < vⱼ + nⱼ))` and (b) `(A j, k : 0 ≤ k < nⱼ : M(d)(vⱼ + k) = aⱼ + k)`.

What matters architecturally is that the number of runs `#runs(d)` is typically far smaller than `|dom(M(d))|` — the representation cost is proportional to the number of editing events, not the document size. Non-trivial runs arise when consecutive allocations produce consecutive I-addresses (as T10a and TA5(c) ensure operationally). Editing can both split and remove runs — inserting content in the middle of a run splits it into two, while deleting an entire run's V-span removes it. The number of distinct Istream allocation events underlying a document's history is monotonically non-decreasing (by S1), but the current arrangement's run count fluctuates with editing.

Gregory's evidence shows that `#runs(d)` has consequences beyond representation cost. Each correspondence run requires an independent tree traversal during V↔I translation. Gregory identifies the inner loop of this traversal as the documented CPU hotspot, responsible for 40% of processing time. For a document with `N` runs, a full V→I conversion requires `N` independent traversals — the cost is multiplicative in the fragmentation level, not merely additive. A consolidation function to merge adjacent runs was started in the implementation and abandoned mid-expression — the function body stops with an incomplete conditional: `if(`. Any implementation of the two-stream architecture must either consolidate runs or accept performance proportional to fragmentation level.
