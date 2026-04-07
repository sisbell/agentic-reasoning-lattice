# Review of ASN-0051

## REVISE

### Issue 1: SV6 proof omits T5 (ContiguousSubtrees)

**ASN-0051, SV6 (CrossOriginExclusion)**: "By TumblerAdd, components before the action point are copied from s. When the action point is within the element field, the full document prefix (node, user, document fields and their separators) is copied, so every tumbler in ⟦(s, ℓ)⟧ shares origin(s)."

**Problem**: TumblerAdd establishes that the *reach* `s ⊕ ℓ` shares origin with `s` — it says nothing about arbitrary tumblers in the interval `[s, s ⊕ ℓ)`. The denotation `⟦(s, ℓ)⟧ = {t ∈ T : s ≤ t < s ⊕ ℓ}` contains every tumbler between `s` and the reach, not just TumblerAdd outputs. The step from "the endpoints share the document prefix" to "everything in between shares the document prefix" requires T5 (ContiguousSubtrees), which guarantees that `{t : p ≼ t}` is a contiguous interval under T1.

**Required**: Insert: "Since `origin(s) ≼ s` and `origin(s) ≼ s ⊕ ℓ` (as just shown), by T5 (ContiguousSubtrees), every `t` with `s ≤ t ≤ s ⊕ ℓ` satisfies `origin(s) ≼ t`, hence `origin(t) = origin(s)`."

---

### Issue 2: SV10 prose contradicts its own formal statement

**ASN-0051, SV10 (DiscoveryResolutionIndependence)**: "A link may be discoverable through a set of I-addresses A yet have empty resolution in a particular document:"

Followed by: `(E Σ, a, d, s :: a ∈ discover_s({M(d)(v) : v ∈ V}) ∧ resolve(Σ.L(a).s, d) ≠ ∅ ∧ π(Σ.L(a).s, d) ⊊ coverage(Σ.L(a).s))`

**Problem**: The prose says "empty resolution" but the formula requires `resolve ≠ ∅`. The formula demonstrates partial resolution (non-empty but proper subset), not empty resolution. The concrete example that follows also shows non-empty resolution ("resolution returns only the V-positions corresponding to i₂"). The independence claim has two faces — discovery without resolution, and discovery with only partial resolution — but the formal statement demonstrates neither the case the prose introduces.

**Required**: Either (a) change the prose to "yet have only partial resolution" to match the formula and example, or (b) provide two formal statements — one for empty resolution (different document for discovery vs. resolution) and one for partial resolution (the current formula).

---

### Issue 3: SV11 proof — false convexity claim and unverified normalization precondition

**ASN-0051, SV11 (PartialSurvivalDecomposition)**: "I(β_k) = {a_k + j : 0 ≤ j < n_k} is convex because ordinal increment (TA5(c)) is strictly monotonic (TA-strict). The intersection of two convex sets under a total order is convex, so each non-empty term is a contiguous subsequence of I(β_k)."

**Problem (3a — convexity)**: `I(β_k)` is NOT convex under T1. Strict monotonicity establishes a total order on elements of `I(β_k)`, not gap-freeness. Child-depth tumblers create gaps: for any `a_k + j ∈ I(β_k)`, the tumbler `c = inc(a_k + j, 1)` satisfies `a_k + j < c < a_k + (j+1)` (by T1 case (ii) and TA5), but `c ∉ I(β_k)` (different length). So `I(β_k)` is not convex in T.

The conclusion is correct but requires a different argument: the span `⟦(sⱼ, ℓⱼ)⟧` is convex (S0). For ordinal indices `j₁ < j₂ < j₃` with `a_k + j₁, a_k + j₃ ∈ ⟦(sⱼ, ℓⱼ)⟧`, we have `a_k + j₁ < a_k + j₂ < a_k + j₃` (TA-strict), so by convexity of the span, `a_k + j₂ ∈ ⟦(sⱼ, ℓⱼ)⟧`. Hence the intersection is contiguous within the ordinal sequence of `I(β_k)` — no convexity of `I(β_k)` needed.

**Problem (3b — normalization)**: "By S8 (NormalizationExistence), this span-set can be normalized." S8's precondition requires mutual level-compatibility: all component spans must have starts of the same tumbler length. Each covering span has start length `#a_k` (the I-start length of its mapping block). When a document transcludes content from sources at different allocation depths, mapping blocks may have I-starts of different lengths. In that case the covering spans are not level-compatible and S8 does not apply.

**Required**: (3a) Replace the convexity argument with the span-convexity-plus-ordinal-monotonicity argument. (3b) Either add a level-compatibility precondition, or weaken to "each covering span is individually level-uniform; normalization applies within each tumbler-depth group."

---

### Issue 4: Endset Fragment definition is unsatisfiable

**ASN-0051, Definition — Endset Fragment**: "a maximal set F ⊆ π(e, d) such that F = ⟦σ⟧ for some span σ"

**Problem**: `F ⊆ π(e, d) ⊆ dom(Σ.C)` (allocated I-addresses only). But `⟦σ⟧ = {t ∈ T : s ≤ t < s ⊕ ℓ}` contains ALL tumblers in the interval — including unallocated child-depth tumblers between consecutive ordinal increments. The condition `F = ⟦σ⟧` requires every tumbler in the span interval to be an allocated content address. This essentially never holds: for any span of width ≥ 1, the interval contains child-depth tumblers `inc(s, 1)` etc. that are in T but not in `dom(Σ.C)`.

The informal gloss ("maximal contiguous subsequence of I-addresses in π(e, d)") captures the right idea — consecutive ordinal increments within a mapping block. The formal restatement with `F = ⟦σ⟧` does not.

**Required**: Define fragments as maximal subsets of `π(e, d)` that are contiguous within some mapping block's ordinal sequence: `F = {a_k + j : j₁ ≤ j ≤ j₂} ⊆ π(e, d)`, maximal with respect to extending `j₁` downward or `j₂` upward within `π(e, d) ∩ I(β_k)`.

---

## OUT_OF_SCOPE

### Topic 1: Non-text subspace projection
SV11's decomposition formula uses ASN-0058's block decomposition, which covers only text-subspace V-positions (`v₁ ≥ 1`). If `M(d)` contains non-text V-positions (`v₁ = 0`, i.e., link-subspace entries), their I-addresses are not captured by the decomposition. A future link-subspace arrangement ASN would need to extend SV11 to cover the full arrangement.

**Why out of scope**: No ASN currently defines the link-subspace arrangement structure. SV11 is correct within its text-subspace scope; the extension requires new foundation work.

VERDICT: REVISE
