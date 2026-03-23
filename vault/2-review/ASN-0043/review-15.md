# Review of ASN-0043

## REVISE

### Issue 1: PrefixSpanCoverage exclusion proof — unspecified first divergence point

**ASN-0043, PrefixSpanCoverage, Exclusion direction**: "if `t` does not extend `x`, there exists some `j ≤ #x` with `t_j ≠ x_j`. As `t ≥ x`, we have `t_j > x_j`."

**Problem**: The claim `t_j > x_j` follows from `t > x` only when `j` is the *first* position at which `t` and `x` differ — i.e., `j = divergence(t, x)`. For an arbitrary later divergence point, the inequality can go either direction. Counterexample: `x = [1, 5]`, `t = [2, 3]`. Here `t > x` (diverge at position 1, `2 > 1`), but at `j = 2`, `t_2 = 3 < 5 = x_2`. The gap appears in both the same-depth case ("since `t ≠ x`, some `j ≤ #x` has `t_j ≠ x_j`. As `t > x`, we have `t_j > x_j`") and the greater-depth case (identical phrasing).

**Required**: Replace "there exists some `j ≤ #x` with `t_j ≠ x_j`" with "let `j` be the least position `≤ #x` with `t_j ≠ x_j`" (equivalently, `j = divergence(t, x)` when `divergence(t, x) ≤ #x`). Then `t > x` and T1(i) give `t_j > x_j`, and the rest of each case follows as written.

### Issue 2: GlobalUniqueness case (iii) — unjustified ancestor claim

**ASN-0043, GlobalUniqueness, case (iii)**: "Without loss of generality, suppose `p_a ≼ p_b` — the allocator at `p_a` is an ancestor of the allocator at `p_b`."

**Problem**: The step from "comparable prefixes (`p_a ≼ p_b`)" to "ancestor-descendant relationship" is stated as obvious but not justified. The claim is true under T10a's discipline — child spawning via `inc(·, k')` with `k' > 0` extends the parent's output by TA5(d), so the child allocator's prefix necessarily extends the parent's prefix, making prefix ordering isomorphic to the allocator ancestry tree. But the proof doesn't state this reasoning. It cites T10a only for the subsequent depth argument, not for the ancestor implication. A reader unfamiliar with the allocator tree structure would see an unjustified leap.

**Required**: Add one sentence connecting comparable prefixes to allocator ancestry, e.g.: "Under T10a, child spawning via `inc(·, k')` with `k' > 0` extends the spawning point (TA5(d)), so the child's prefix extends the parent's — comparable allocator prefixes therefore imply ancestor-descendant relationship in the allocator tree."

## OUT_OF_SCOPE

### Topic 1: PrefixSpanCoverage and GlobalUniqueness as foundation candidates

**Why out of scope**: Both results are general properties of the tumbler allocation system — PrefixSpanCoverage is about tumbler arithmetic and span coverage; GlobalUniqueness is about the three-case exhaustion of allocator prefix relationships. Neither is specific to links. Their placement in the link ontology ASN means future ASNs needing these results would either re-derive them or reference a non-foundation ASN. They are natural candidates for promotion to ASN-0034 (tumbler algebra) or ASN-0036 (streams). Note also that GlobalUniqueness strengthens ASN-0036's S4 (OriginBasedIdentity) by covering the comparable-prefix case (iii), which S4's cited derivation ("from T9, T10") does not address.

### Topic 2: Link arrangement model

**Why out of scope**: The ASN acknowledges that Gregory's implementation places links in V-positions within a document's permutation matrix, while S3 restricts `Σ.M(d)` to `dom(Σ.C)`. The ASN correctly derives non-transclusion from S3 + L0 under the current model. Extending S3 to accommodate link V-positions — and determining whether non-transclusion should be an independent invariant surviving that extension — belongs in a future ASN defining arrangement semantics for the link subspace.

VERDICT: REVISE
