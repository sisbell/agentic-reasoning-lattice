# Review of ASN-0069

## REVISE

### Issue 1: V9's consequence claims `{d_src, d_new}` but this is wrong for subsequent forks

**ASN-0069, §"Provenance Recording", discussion after V9**: "querying R for 'documents containing I-address `a`' returns at least `{d_src, d_new}` for every `a ∈ ran(M'(d_new))` (and possibly more, if `a` was also transcluded elsewhere)."

**Problem**: This is false for subsequent forks. On a subsequent fork the content source operand is `d_op = max(dom(A_v(d_src))) = d_prev`, not `d_src` (J4's operand rule, restated in this ASN's §"What Must Be Constructed"). Counterexample: fork `d_src` to `v1` (first fork, `d_op = d_src`); insert fresh content `b` into `v1` via K.α/K.μ⁺, so `origin(b) = v1` and `b` was *never* in `d_src`'s arrangement; now fork `d_src` again. The second fork has `d_op = v1`, inherits `b`, and records `(b, d_new²)`. Querying R for `b` returns `{v1, d_new²}` — `(b, d_src) ∉ R`, because `b` never appeared in `d_src`. The claimed `d_src` membership does not hold. Notably, V12(d) gets this right — it correctly writes `(a, d_op) ∈ R''`, deriving the source-side pair against the *operand* `d_op`, not `d_src`. V9's consequence slips back to `d_src` and contradicts V12(d).

**Required**: Restate the V9 consequence in terms of the content source operand: a fork records `(a, d_new)` and the operand-side record is `(a, d_op)` (V12(d)), so the query returns at least `{d_op, d_new}`. Membership of `d_src` holds only on a first fork (where `d_op = d_src`) or where `a` independently passed through `d_src`'s content subspace; do not assert it unconditionally.

## OUT_OF_SCOPE

### Topic 1: V6a link-projection semantics (coverage / project / discoverable_from)

**ASN-0069, §"Subspace Selectivity", V6a and its three preceding definitions**

**Why out of scope**: The Scope section lists "link semantics" as out of scope. V6a introduces a full link-resolution apparatus — `coverage(e)` (union of spans), `project(a, i, d, Σ)` (V-positions whose images fall in a slot's coverage), and `discoverable_from(a, d, Σ)` — none of which the foundations (ASN-0034/0036/0047) define. This is link-projection semantics: how a link's endsets resolve onto a document's arrangement. The fork's actual link guarantee that *is* in scope — that the link subspace is not inherited and the link store is unchanged — is already fully captured by V6 (`V_{s_L}(d_new) = ∅`) and the `L' = L` frame condition (a one-line consequence of V3/V5's frame). The discoverability-inheritance lemma and its machinery belong in a link-semantics ASN, where `project`/`coverage`/`discoverable_from` can be defined as first-class objects rather than inlined here. The worked example's "Link discoverability (V6a)" paragraph (which itself reasons "hypothetically" about whether `a₁ ∈ coverage(...)`) should be trimmed with it.

VERDICT: REVISE
