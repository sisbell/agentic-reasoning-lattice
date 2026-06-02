# Review of ASN-0069

## REVISE

### Issue 1: V4 inherits content from `d_src` in the subsequent-fork case, contradicting J4's `d_op`

**ASN-0069, V4 (*arrangement inheritance*)**: "`(A v ∈ V_{s_C}(d_src) :: v ∈ dom(M'(d_new)) ∧ M'(d_new)(v) = M(d_src)(v))` … V4 holds unconditionally."

**Problem**: V4 is asserted for *every* fork, including subsequent (sibling) forks, and pins the inherited content to `M(d_src)`. But the foundation J4 (ASN-0047), as currently written, ties the subsequent-fork content to a *different* operand:

> "k = 0 sub-case fires when `A_v(d_src)` already has a frontier: `d_new = inc(prev_version, 0)` and `d_op = prev_version = max(dom(A_v(d_src)))`" … "(ii) K.μ⁺ populating M'(d_new) via … `(A v ∈ V_{s_C}(d_op) :: M'(d_new)(φ(v)) = M(d_op)(v))`. Derived consequence: `ran(M'(d_new)) = ran(M(d_op)|_{V_{s_C}(d_op)})`."

In the subsequent-fork case J4 fixes the content source as `d_op = prev_version`, **not** `d_src`. These coincide only when `prev_version` has not been edited since its own creation. If `prev_version` was edited after being forked, `M(d_op) ≠ M(d_src)` and V4's claim is false against the foundation. The ASN never mentions `d_op` or J4's operand-tracking rule anywhere — it is written against an earlier J4 that lacked the `k = 0` branch.

**Required**: Reconcile V4 with J4. Either (a) restate V4's subsequent-fork case to inherit from `M(d_op)` (the prior version), matching J4's clause (ii), and propagate the change through V8, V10(b), V11, and V12(d); or (b) if this ASN deliberately overrides J4's content source for subsequent forks, that override cannot stand against a foundation ASN — J4 is authoritative, so V4 must conform.

### Issue 2: §"Identity by Sub-Allocation" mischaracterizes J4

**ASN-0069, §"Identity by Sub-Allocation"**: "The subsequent-fork sub-case … is an *extension* of J4: J4's clause (i) names only the first-fork shape and does not contemplate sibling-stream advancement on `A_v(d_src)`'s frontier."

**Problem**: This is factually wrong against the given J4, which explicitly contemplates both sub-cases ("k = 1 sub-case … k = 0 sub-case … in both sub-cases `d_src ≼ d_new`"). The subsequent-fork shape is *in* J4, not an extension of it. Framing it as a deviation misstates what the foundation provides and obscures the real discrepancy (Issue 1: the content operand `d_op`).

**Required**: Remove the "extension of J4" framing for the subsequent-fork *identity* shape (it is J4 clause (i)+allocation-rule as written). Retain explicit-deviation framing only where the ASN genuinely strengthens J4 (literal V-position inheritance over J4's order-preserving bijection `φ`), and add the missing engagement with `d_op`.

### Issue 3: Downstream claims inherit the same `d_src`/`d_op` error

**ASN-0069, V10(b)**: "`d_new²` reads `M(d_src)` at `Σ_g`."
**ASN-0069, V12(d) derivation**: "`ran(M'(d_new)) = ran(M(d_src)|_{V_{s_C}(d_src)})` … every inherited I-address is content-subspace-referenced in `d_src`'s arrangement at the pre-fork state."
**ASN-0069, Worked Example, "Subsequent fork of d_src"**: "`M²(d_new²)` is again populated with `{[s_C,1]↦a₁,…}` (assuming `M(d_src)` has not been edited between the two forks)."

**Problem**: All three assume subsequent-fork content flows from `d_src`. Per J4 it flows from `d_op = prev_version`. V12(d)'s use of P4★ to land `(a, d_src) ∈ R` breaks: if `a ∈ ran(M(d_op))` but `a ∉ ran(M(d_src))`, then `(a, d_src)` need not be in `Contains_C(Σ)` and the P4★ step fails. The worked-example caveat is also mis-scoped — the relevant condition is "`prev_version` (= `d_new¹`) unedited since its creation," not "`M(d_src)` unedited."

**Required**: After fixing V4, restate V10(b) and the V12(d) derivation in terms of `d_op`, and correct the worked-example caveat to name the prior version as the content source.

## OUT_OF_SCOPE

### Topic 1: Concurrent fork vs. source modification, descendant enumeration, snapshot vs. living forks
**Why out of scope**: These are correctly parked in §"Open Questions" — they concern future operations and presentation guarantees, not the abstract effect of a single fork transition.

VERDICT: REVISE
