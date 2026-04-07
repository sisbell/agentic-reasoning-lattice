# Review of ASN-0036

## REVISE

### Issue 1: S8 cross-subspace disjointness cites T7 (identity) instead of T5/T1 (ordering)

**ASN-0036, S8 (Span decomposition)**: "Different subspaces: by T7 (ASN-0034), the first component of the element field permanently separates subspaces, so no position in subspace s₁ falls in any interval of subspace s₂ ≠ s₁."

**Problem**: T7 (SubspaceDisjoint) establishes `a.E₁ ≠ b.E₁ ⟹ a ≠ b` — identity separation. The partition proof requires *interval* disjointness: that no tumbler from subspace s₂ falls inside the half-open interval `[s₁.x, s₁.(x+1))`. Identity separation does not establish interval separation. Two tumblers being unequal (`s₁.x ≠ s₂.y`) says nothing about whether `s₂.y` lies between `s₁.x` and `s₁.(x+1)` in the ordering. The "so" in the quoted passage bridges a gap that T7 cannot cross.

The conclusion is correct — all tumblers in `[s₁.x, s₁.(x+1))` have first component `s₁` (by T1 case (i) at position 1: any tumbler with first component `> s₁` exceeds `s₁.(x+1)`, any with first component `< s₁` is below `s₁.x`). But this is a property of the lexicographic order, not of identity separation.

**Required**: Replace the T7 citation with T5 (ContiguousSubtrees): for prefix `[s₁]`, the set `{t : t₁ = s₁}` is a contiguous interval under T1. By PrefixOrderingExtension, if `s₁ < s₂` and neither `[s₁]` nor `[s₂]` is a prefix of the other (both length 1, differing at position 1), all extensions of `[s₁]` precede all extensions of `[s₂]`. Therefore contiguous blocks for distinct subspace identifiers are entirely disjoint, and no singleton interval in one subspace can contain any tumbler from another.

### Issue 2: V-position well-formedness is undefined

**ASN-0036, Two components of state**: "Σ.M(d) : T ⇀ T — the arrangement of document d. A partial function mapping V-space positions to I-space addresses."

**Problem**: I-addresses have a formal well-formedness constraint: S7b requires `zeros(a) = 3` for every `a ∈ dom(Σ.C)`, anchoring I-addresses in T4's field structure. V-positions have no analogous constraint. The worked example uses element-local tumblers (`1.1`, `1.2`, ..., `1.5`) and S8-depth constrains their depth within a subspace, but nothing formally states that V-positions are element-field tumblers or that their first component is the subspace identifier.

This matters in two places:

1. The S8 uniqueness proof applies T7 to V-positions by referencing "the first component of the element field." But T7 and T4's element-field definition apply to full tumblers with `zeros ≥ 3`. V-positions as shown in the worked example (`1.1`, `1.2`) have `zeros = 0` — they have no element field in the T4 sense. The proof implicitly assumes V-positions *are* element fields (of some full tumbler), but this identification is never stated.

2. S8-depth says "within a given subspace s" — presupposing that V-positions have a subspace component. The structural basis for this (first component = subspace identifier) is described informally ("V-addresses in the text subspace consistently use the form `s.x`") but not elevated to a formal property.

**Required**: Add a V-position well-formedness property parallel to S7b. Formally state that V-positions within `dom(M(d))` are element-field tumblers — that is, they correspond to the fourth field of a full tumbler address, with the first component serving as the subspace identifier. This grounds S8-depth's "within a subspace," justifies the application of T5/T7 to V-positions, and makes explicit the structural difference between the domain (`T_V ⊆ T`, element-field tumblers) and range (`T_I ⊆ T`, element-level addresses with `zeros = 3`) of the arrangement function.

## OUT_OF_SCOPE

### Topic 1: Unique maximal decomposition
**Why out of scope**: S8 proves existence of a finite decomposition via singletons. Whether a unique maximal (fewest-run) decomposition exists — and whether greedily merging adjacent compatible singletons yields it — requires defining "maximal," proving a merge lemma, and showing confluence. This is new territory, correctly identified as an open question.

### Topic 2: Operation preservation of S0–S3
**Why out of scope**: The ASN establishes invariants; showing INSERT, DELETE, COPY, etc. preserve them is explicitly scoped out. The wp analyses for S0 and S3 provide necessary conditions that any valid operation must satisfy but do not instantiate them.

VERDICT: REVISE
