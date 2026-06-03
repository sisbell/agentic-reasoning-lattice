# Review of ASN-0068

## REVISE

### Issue 1: CV-ATOM(b) derives aggregation from the wrong premise

**ASN-0068, Atomicity and Granularity (CV-ATOM derivation part (b))**: "Were they witnessed by `n` separate width-1 runs, each pair would be witnessed twice (once by the corresponding width-1 run, once at the corresponding offset of the width-`n` run that also satisfies the run conditions) — contradicting uniqueness."

**Problem**: CV-MAX's uniqueness is stated *over the maximal runs in `MaxRuns`*, not over all correspondence runs that a pair satisfies. A pair satisfies many non-maximal correspondence runs; that is not double-witnessing. For the argued "witnessed twice" contradiction to bite, both the `n` width-1 runs *and* the width-`n` run must lie in `MaxRuns`. But an interior width-1 run is right-extendable (the next consecutive pair corresponds), hence not right-maximal, hence not in `MaxRuns`. So the supposition "width-1 runs in `MaxRuns`" is false because of non-maximality — the very fact part (a) correctly invokes ("both endpoints already at maximality") — not because of a uniqueness contradiction. The derivation inverts cause and effect: it presupposes a configuration that maximality already forbids and then derives a contradiction from uniqueness.

**Required**: Ground (b) in maximality: consecutive correspondent pairs cannot lie in distinct maximal runs because an interior width-1 run fails right-maximality; the unique maximal run witnessing each such pair is therefore the full extension. Uniqueness then merely pins the representation; it is not what forces aggregation.

### Issue 2: CV-IN carries an unlabeled necessity argument whose derived bound is never consumed

**ASN-0068, The Input (paragraph beginning "Level-uniformity (S6) alone requires only...")**: "...The exact constraint `actionPoint(width(σ)) = m_σ` rules out this unbounded capture... The intersection with the arrangement, `⟦σ⟧ ∩ V_S(d)`, contains exactly `min(n_σ, n_S(d) − s_m + 1)` consecutive depth-`m_σ` V-positions..."

**Problem**: This is a multi-step necessity argument (why `= m_σ` rather than `< m_σ`) embedded as precondition prose. Two accretion patterns apply: (a) it explains *why the constraint is needed* rather than stating *what it constrains* — the actual precondition is one line; (b) its derived conclusion (the `min(n_σ, n_S(d) − s_m + 1)` extent bound, plus the "unbounded uniformly across the full range `1 ≤ k < m_σ`" exhaustiveness flourish) is not consumed by any later proof — CV-MAX's termination uses S8-fin and D-SEQ★ directly, and CV-FIN uses the product bound, neither invoking this result. A derivation whose output no downstream claim reads is accreted prose around the precondition.

**Required**: Either promote the necessity result to a labeled lemma (parallel to how foundations state necessity as T10a-N) and cite it where used, or trim it to the one-sentence statement of the precondition. If retained, identify the use site; if there is none, remove it.

## OUT_OF_SCOPE

### Topic 1: Concurrent-modification, replication, and multi-document composition invariants

The Open Questions enumerate concurrency-during-comparison, replicated-state determinism, sub-allocator-boundary runs, and multi-document correspondence composition. These are correctly deferred — they belong to future ASNs, not this one. No action needed; flagged only to confirm they are not gaps in CV-0068's stated scope.

VERDICT: REVISE
