# Review of ASN-0069

## REVISE

### Issue 1: V4a is a verbatim restatement of V4; V8 reframes the same equality
**ASN-0069, §"The Arrangement Layer" (V4a) and §"Structural Correspondence" (V8)**

V4 commits to `(A v ∈ V_{s_C}(d_op) :: v ∈ dom(M'(d_new)) ∧ M'(d_new)(v) = M(d_op)(v))`. V4a then states: "both `M(d_op)(v)` and `M'(d_new)(v)` are defined, and both equal the same I-address `a`. The V-position `v` is *the same tumbler* in both arrangements." V8 states `(A v ∈ V_{s_C}(d_op) :: M'(d_op)(v) = M'(d_new)(v))`, derived as `M'(d_op) = M(d_op)` (frame) composed with V4.

**Problem**: V4a adds nothing over V4 — definedness of `M(d_op)(v)` follows from `v ∈ V_{s_C}(d_op) ⊆ dom(M(d_op))`, and "same tumbler in both arrangements" is already the content of V4's shared bound variable. V8 is V4 re-expressed in post-state coordinates via the source frame. Three labeled properties assert the single fact "the inherited I-address at each content-subspace V-position is equal in source and fork." This is the "two paragraphs say the same thing in different words" pattern flagged by the anti-bloat classifier.

**Required**: Delete V4a (fold its one observation — definedness on both sides — into V4 if needed). Keep V8 only as the post-state correspondence framing that downstream lemmas (V8b, V8c, worked example) consume, and state it as a one-line corollary of V4 + the source frame rather than re-deriving the equality.

### Issue 2: V11a's length-identity step over-derives and contradicts V11's premise
**ASN-0069, §"Composability" (V11a)**: "the V2 derivation's nested-induction-on-emission-count argument, applied to `A_v(dⁱ_new)` ... — first emission via TA5(d) at `k = 1`, each subsequent emission via TA5(c) ... By V1, `dⁱ⁺¹_new` is an emission of `A_v(dⁱ_new)` in either sub-case"

**Problem**: V11 fixes every chain step as the *first* fork of its immediate source, so `dⁱ⁺¹_new = inc(dⁱ_new, 1)` always. The length increment `#dⁱ⁺¹_new = #dⁱ_new + 1` then follows directly from TA5(d) at `k = 1`. The imported nested induction over `inc(·, 0)` subsequent emissions and the "in either sub-case" hedge describe subsequent forks that V11's premise excludes from the chain — heavier machinery than the claim needs and inconsistent with the stated premise.

**Required**: Replace the nested-induction citation with a direct one-line appeal to TA5(d) at `k = 1`; drop "in either sub-case."

### Issue 3: Worked example invokes an undefined operation
**ASN-0069, §"Worked Example"**: "The CompareVersions operation on `(d_src, d_new)` over the full content subspace would return a single maximal run `([s_C, 1], [s_C, 1], 3)`"

**Problem**: `CompareVersions` is named as if established, but no such operation is defined in this ASN or in the cited foundations. The example leans on machinery it has not introduced.

**Required**: State the example's point in terms the ASN actually owns — I-address equality at each shared V-position (V8), yielding the correspondence triple — without invoking a named comparison operation.

## OUT_OF_SCOPE

### Topic 1: Version intercomparison operation
**Why out of scope**: A CompareVersions / intercomparison operation that surfaces maximal corresponding runs is a future operation ASN. This ASN correctly establishes the structural substrate (V8, V8b) it would rest on; it should not invoke the operation itself (see Issue 3).

VERDICT: REVISE
