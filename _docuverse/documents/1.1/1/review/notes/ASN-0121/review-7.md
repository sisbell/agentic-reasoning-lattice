# Review of ASN-0121

## REVISE

### Issue 1: "span denotes a contiguous subtree (T5)" miscites the foundation

**ASN-0121, "Residence and endpoints are orthogonal axes" / "What is being matched"**: "Because a span in document-address space denotes a contiguous subtree (T5, ASN-0034), `H` may bound residence at the granularity of a node, an account, or a single document, and `athome` tests membership of `home(a)` against whatever that subtree is."

**Problem**: A span `(s, ℓ)` denotes the half-open interval `{t : s ≤ t < s ⊕ ℓ}` (σ.denotation, ASN-0034/0053), which is a *subtree* only for the canonical unit-depth prefix span — the result PrefixSpanCoverage (ASN-0043) establishes (`coverage({(x, δ(1,#x))}) = {t : x ≼ t}`). T5 (ContiguousSubtrees) gives the *converse-direction* fact — that prefix subtrees are order-convex intervals — not that an arbitrary span denotes a subtree. A general span starting and ending mid-subtree denotes an interval that is no subtree at all. So the cited support is the wrong lemma, and the universally-quantified claim ("a span … denotes a contiguous subtree") is false as written. The foundation's own per-step citation discipline (e.g., T10/T1 "discharged from T0 rather than left implicit") sets the bar this sentence falls below.

**Required**: Restrict the claim to prefix spans and cite PrefixSpanCoverage (ASN-0043) for "a prefix-rooted home span denotes the subtree `{t : p ≼ t}`"; T5 may be cited only for the convexity/contiguity of that subtree, not for the span-equals-subtree identity.

### Issue 2: FL-MON's value-preservation step needs the multi-step persistence lemma, not single-step L12

**ASN-0121, FL-MON proof**: "(By immutability `sat(a, q, Σ') = sat(a, q, Σ)`; and `a ∈ addressable(Σ')` because `a ∈ dom(Σ'.L)` by link-store monotonicity across `Σ →* Σ'` (ASN-0098 StoreMonotonicity★) …)"

**Problem**: The parenthetical is careful to cite the *multi-step* StoreMonotonicity★ for the domain fact, but justifies `sat(a, q, Σ') = sat(a, q, Σ)` by bare "immutability." `sat` constancy needs `Σ'.L(a) = Σ.L(a)` across the reachability closure `Σ →* Σ'`, which is L12 (a single-step invariant) lifted by induction — i.e., LP13 (UnconditionalLinkPersistence, ASN-0098), the very lemma the ASN relies on elsewhere. Naming "immutability" without distinguishing single-step L12 from its `→*` closure is the same kind of step-skip the domain half was careful to avoid.

**Required**: Cite LP13 (ASN-0098) for `Σ'.L(a) = Σ.L(a)` across `Σ →* Σ'`, matching the precision already applied to the domain conjunct.

## OUT_OF_SCOPE

### Topic 1: Version/time-qualified inquiry surfacing retracted links
Correctly deferred by the ASN's open questions and consistent with the retraction-scope guidance; no claim is asserted, so nothing to fix here.

VERDICT: REVISE
