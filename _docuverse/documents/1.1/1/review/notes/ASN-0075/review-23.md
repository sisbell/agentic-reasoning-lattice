# Review of ASN-0075

## REVISE

### Issue 1: D-EXH's composite-boundary hypothesis isn't reflected in SHOWDELETIONS's precondition

**ASN-0075, Lemma D-EXH and SHOWDELETIONS definition**: D-EXH's hypothesis is "Let Σ be a state reachable from Σ_0 by a finite sequence of valid composite transitions (equivalently, Σ is a composite boundary)." SHOWDELETIONS's precondition is "d_A ∈ E_doc ∧ d_B ∈ E_doc".

**Problem**: D-EXH's mutual-exclusion guarantee depends on P4★, which ASN-0047 establishes only as a composite-boundary property (Class (b) in ExtendedReachableStateInvariants), not as a per-state invariant. SHOWDELETIONS's stated precondition admits any state where d_A and d_B are documents — including intermediate states within a composite. At such an intermediate state (e.g., between an elementary K.α/K.μ⁺ pair and a not-yet-executed K.ρ in the same composite), a content address `a` can have `a ∈ ran(M(d))` while `(a, d) ∉ R` — the very row that D-EXH excludes by appeal to P4★. At that state both CURRENT(a, d) and NEVER_INCLUDED(a, d) are simultaneously true, falsifying D-EXH's "exactly one" claim. The author's defense — "SHOWDELETIONS is only meaningful at reachable states, so the restriction does not narrow its operational scope" — conflates two distinct notions of reachability (by elementary transitions vs. by valid composites) without grounding the narrower one in an explicit axiom. "Operational scope" is not formally pinned down by the spec, so a reader cannot tell whether intermediate-state invocation is forbidden by hypothesis or merely by intention.

**Required**: Either (a) tighten SHOWDELETIONS's precondition to require explicitly that the pre-state is a composite boundary (and propagate this through the wp formula), or (b) make explicit the system-level discipline that observational operations are invoked only at composite boundaries — and cite it as an axiom of the operation's contract — so D-EXH's hypothesis is discharged by construction rather than by appeal to informal "operational scope."

### Issue 2: D-ACT's structural observation about T1-consecutiveness in dom(C) is labeled "not needed for the bijection" yet spans a major case analysis

**ASN-0075, D-ACT**: "A separate structural observation, useful for situating each I-adjacency class within the larger dom(C) ordering (and not needed for the bijection argument above), is that no `t ∈ dom(C)` lies strictly between consecutive emissions ..." followed by ~600 words of four-case analysis (same-origin three cases plus different-origin with three nested sub-cases on prefix relations between d and d').

**Problem**: The author explicitly disclaims that this observation is load-bearing for any subsequent claim — the bijection between I-adjacency classes and witness runs is already established by the index-contiguity argument that precedes it. None of D-ACT's later claims, nor any other claim in the ASN (D-OBS, D-RECONS, D-SUBSP, etc.), cites this T1-consecutiveness result. The observation does not appear in the Claims Introduced table. Including a long case analysis whose result is unused weakens the ASN by inviting the reader to look for downstream consequences that aren't there, and risks the case analysis silently becoming load-bearing in a future revision without any audit trail of what depends on it.

**Required**: Either (a) cite an explicit consequence of T1-consecutiveness that some other claim in the ASN actually uses (e.g., promote it to a named lemma and reference it from where the consequence is consumed), or (b) remove the case analysis and replace it with a one-line forward reference: "T1-consecutiveness in dom(C) follows from T10a/T10 properties; we omit it here as no claim in this ASN depends on it."

## OUT_OF_SCOPE

(The author's Open Questions section appropriately catalogues future-work topics: shared-content-history characterisations, multi-document generalisations, concurrency models, version-chain interactions, the "deleted from all, witness in a third document" case, and granularity of presentation. No additional out-of-scope items needed.)

VERDICT: REVISE
