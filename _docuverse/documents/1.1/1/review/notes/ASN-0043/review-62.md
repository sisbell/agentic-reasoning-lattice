# Review of ASN-0043

## REVISE

### Issue 1: L9 Case B's "frontier" assumes a single allocator

**ASN-0043, L9 proof — Allocation of `a` (Case B)**: "The element-level allocator for `d'`'s link subspace already exists, with a current frontier somewhere in `s_L` ... the allocator's state after those allocations is a frontier address in `d'`'s link subspace at element field depth ≥ 2). The next link address is `inc(·, 0)` from that frontier ... Continue sibling advances if necessary until the output is in the unoccupied complement of `dom(Σ.L)`."

**Problem**: The proof refers to "the element-level allocator" — singular — but T10a permits multiple allocators within `d'`'s link subspace once child-spawns occur (a link at element-field depth 3, allocated via `inc(d'.0.s_L.x, 1)`, spawns a new allocator). Case B's "the prior link allocations under `d'` were produced by a T10a-conforming allocator chain through steps (i)–(iii)" implicitly assumes every prior link traced steps (i)–(iii) and then advanced as siblings at depth 2 — but L1b only requires `#E ≥ 2`, not `= 2`, so prior links at deeper levels are admissible. The single-allocator framing obscures which allocator's frontier is meant. "Continue sibling advances if necessary" never says when it is necessary or how many steps suffice.

**Required**: Use an allocator-agnostic construction. For example: "Pick any existing link `b ∈ dom(Σ.L)` with `home(b) = d'`. By L-fin (`dom(Σ.L)` finite) and T10a.7 (the sibling chain `b, inc(b, 0), inc²(b, 0), …` is injective hence infinite), the least `i ≥ 1` with `incⁱ(b, 0) ∉ dom(Σ.L)` exists; set `a = incⁱ(b, 0)`. By T10a.8 `zeros(a) = zeros(b) = 3`; by chain-prefix-preservation `home(a) = home(b) = d'`; L1c follows by extending `b`'s L1c chain with `i` sibling advances."

### Issue 2: L11b's sibling-chain wording is opaque

**ASN-0043, L11b proof — Construction of fresh `a'`**: "The least-`i` choice ensures that the structural sibling chain `a⁽⁰⁾, a⁽¹⁾, …, a⁽ⁱ⁾` — every prefix of which lies in `dom(Σ.L)` except the last — extends `dom(Σ.L)` to `dom(Σ'.L)` by a single sibling step beyond the existing initial segment of occupied siblings."

**Problem**: "Every prefix of which lies in `dom(Σ.L)` except the last" requires the reader to parse "prefix" as "initial segment of the chain," "lies in" as "every element is a member of," and "except the last" as a quantifier exclusion. The intent — that `a⁽ʲ⁾ ∈ dom(Σ.L)` for `0 ≤ j < i` and `a⁽ⁱ⁾ ∉ dom(Σ.L)` — is obscured by the layered metalanguage.

**Required**: State the membership condition directly: "the least-`i` choice ensures `a⁽ʲ⁾ ∈ dom(Σ.L)` for `0 ≤ j < i` and `a⁽ⁱ⁾ ∉ dom(Σ.L)`."

### Issue 3: L1c's k₁ ∈ {1, 2} is loose given the chain-origin constraint

**ASN-0043, L1c**: "`k₁ ∈ {1, 2}` ∧ `(A i : 1 ≤ i ≤ n : #tᵢ > #h(a))`"

**Problem**: For a chain to end at a link address `a` with `zeros(a) = 3` (L1) while satisfying `t₀ = h(a)` (whose `zeros = 2` by S7d), at least one step must add a zero. By TA5(d), only `k = 2` adds a separator zero; `k = 1` extends without adding a zero. A chain starting with `k₁ = 1` from `t₀ = h(a)` produces `t₁ = h(a).1` with `zeros = 2`; reaching `a` requires a later `k_j = 2` step, which would shift T4b's parsing of the document field and force `h(a) ≠ t₀`, contradicting the chain-origin clause. So `k₁ = 2` is the only first step compatible with the chain-origin constraint. The text admits `k₁ ∈ {1, 2}` but the proof use-sites (Case A of L9, the worked example) both use `k₁ = 2`. The looser membership is harmless but obscures the actual structural constraint.

**Required**: Either tighten to `k₁ = 2` (with a brief proof that `k₁ = 1` violates `t₀ = h(a)` for any element-level destination), or add a remark explaining why `k₁ = 1` is admitted by L1c but unreachable in practice — so a reader is not confused when every concrete chain uses `k₁ = 2`.

### Issue 4: Worked example L8 verification leaves the coverage-vs-span-set distinction abstract

**ASN-0043, worked example — L8 verification**: "two distinct span decompositions of this same address set (for example, `{(g, δ(1, 8))}` versus a hypothetical multi-span decomposition with the same union coverage) would denote the same type by L8, illustrating the coverage-vs-span-set distinction"

**Problem**: The worked example flags the L8 design choice (coverage equality, not span-set equality) but exhibits no concrete second decomposition. The coverage `{t : g ≼ t}` of `(g, δ(1, 8))` is non-trivial to redecompose without invoking deeper spans — the reader cannot verify the claim against the rest of the worked example.

**Required**: Either exhibit a concrete second endset `E'` with `E' ≠ {(g, δ(1, 8))}` (as sets of spans) but `coverage(E') = {t : g ≼ t}`, or drop the parenthetical and let L8's prose carry the distinction. As written, the example asserts the property without illustrating it.

## OUT_OF_SCOPE

None — the ASN's scoping declaration covers operations, V-space effects, resolution, indexing, scale, access control, version-spanning behavior, and deletion semantics, and the ASN observes these boundaries.

VERDICT: REVISE
