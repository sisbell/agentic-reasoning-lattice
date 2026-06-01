# Review of ASN-0086

## REVISE

### Issue 1: CoverageEqualityDecidable claims a toolset its proof exceeds
**ASN-0086, Lemma — CoverageEqualityDecidable**: "the predicate `coverage(e) = coverage(e')` is decidable, using only T2 comparisons and TumblerAdd."

**Problem**: The proof's empty-gap handling constructs the zero-extension `c_k.0` and decides emptiness "by a single T2 comparison against the computable witness `c_k.0`." Zero-extension (appending a single `0` component) is neither a T2 comparison nor TumblerAdd — and it is not even producible by the tumbler algebra's primitive repertoire (`inc(c_k, 1) = c_k.1`, `inc(c_k, 2) = c_k.0.1`; neither yields `c_k.0`). It is a raw sequence operation on T0's carrier. The decidability argument is sound, but the stated toolset is false as written.

**Required**: Correct the toolset claim to include the sequence-construction step (e.g., "T2 comparisons, TumblerAdd, and zero-extension on T0's carrier"), or recast the empty-gap test so it genuinely uses only the named operations.

### Issue 2: Anti-bloat — definitional hedging buries the Unit-depth retraction discipline
**ASN-0086, Definition — Unit-depth retraction discipline**: The substantive definition is one sentence ("every `(b, F', G') ∈ L_R^Σ` has to-endset `G' = {(t, δ(1, #t))}` for some `t ∈ A_rel^Σ`"). It is then surrounded by multi-paragraph hedging: "sufficient for this per-state predicate but not equivalent to it … the converse fails … yet once `t` enters `A_rel` at the post-state … Membership … is therefore evaluated at the state Σ in question, not at the producing call's pre-state. A layer satisfies … A layer can guarantee … this is one sufficient strategy, not the only configuration the per-state predicate admits."

**Problem**: This is exactly the flagged pattern — prose around a definition that re-explains why/how it relates to Nullify rather than advancing the definition's meaning, with the "sufficient-not-equivalent / where-membership-is-evaluated" point restated several times. The reader must skip past it to recover the one-line predicate. The same redundancy recurs in the wp Case 2 domain-restriction block ("Substrate-conformance alone is insufficient" / "The discipline alone is insufficient"), where the two parallel necessity witnesses are genuine but framed with duplicative connective prose.

**Required**: Reduce the discipline definition to its predicate plus at most one clarifying line (per-state membership evaluated at Σ); fold the sufficiency-vs-equivalence remark into the Nullify discussion that consumes it rather than restating it at the definition site.

## OUT_OF_SCOPE

### Topic 1: Retraction asymmetry for higher-arity links
`nullified(Σ)` ranges over all of `A_rel^Σ = dom(Σ.L)` (any arity), but the witnessing existential consults `L_R^Σ`, which by the `L_K` definition admits only `|Σ.L(a)| = 3`. A higher-arity link with type-coverage `R` therefore cannot nullify, while a higher-arity link *can be* nullified. This produces no inconsistency for `A_K` (which is standard-triple only), so it is harmless here, but the higher-arity retraction semantics are a future-ASN concern, consistent with the stated standard-triple restriction.

VERDICT: REVISE
