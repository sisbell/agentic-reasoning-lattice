# Review of ASN-0043

This is a rev-44 ASN and it is, on the technical merits, in very good shape: the FSP/FSE factoring is clean, the L1c chain derivations are explicit, and the worked example's six-step extension genuinely exercises the cases a singleton state cannot (L5 order-irrelevance, L8 discrimination, L8 coverage-vs-decomposition). I checked the producer chains (L9 Case A sweep, the worked-example L1c chain, TA5a side-conditions at the `k'=2`/`k'=1` boundaries) and found them sound. The findings below are notation and scope-of-rationale items the anti-bloat pass should catch at source.

## REVISE

### Issue 1: The allocator tree symbol 𝒯 is used without introduction
**ASN-0043, DocVal and L11a**: DocVal — "such a `d` is the terminus of a T10a-conforming allocator chain from the system tree 𝒯's root"; L11a — "each home `home(a) ∈ dom(Σ.M)` is a node of the system's single allocator tree 𝒯".
**Problem**: 𝒯 first appears in DocVal as though already defined, then is leaned on in L11a as "the single T10a system 𝒯" that supplies GlobalUniqueness's "distinct events within a single system" precondition. The symbol is never introduced. T10a (foundation) speaks of an allocator tree and a root allocator, but this ASN names a specific object 𝒯 and makes the L11a precondition discharge turn on its singleness — a load-bearing use that should not rest on an unintroduced symbol.
**Required**: Introduce 𝒯 once (e.g., "let 𝒯 be the system's single T10a allocator tree, rooted at the T4-valid root of T10a") before first use, or replace the symbol with T10a's own terminology and cite it.

### Issue 2: L8's definitional rationale reasons in out-of-scope search/matching territory
**ASN-0043, L8 — TypeByAddress**: "The design choice — coverage rather than span-set identity — falls out of Nelson's search semantics... since type-equivalence is what makes two links indistinguishable to any search request, two type endsets with the same coverage are interchangeable under search and therefore the same type." Also the earlier consequence: "under search semantics, every member of a class is indistinguishable from every other by type matching."
**Problem**: Search, matching, and sieving of discovery results are explicitly OUT OF SCOPE for this ASN. L8's *formal* content (the coverage-equality biconditional) is in scope and self-contained, but the justifying prose derives the choice *from* search interchangeability ("satisfies a search request," "interchangeable under search") — the precise machinery the ASN does not model. This is rationale built on territory the ASN cannot reference. A Nelson quotation grounding the choice is fine; reconstructing a search-indistinguishability argument to *derive* the definition is scope leakage the reader must work past.
**Required**: Reduce the rationale to the Nelson grounding plus the in-scope observation that coverage is the address-set projection (per the Coverage definition), and drop the "interchangeable under search / satisfies a search request" derivation. State the coverage criterion as a modeling commitment, not a consequence of unmodeled search.

### Issue 3: L11a closes with a restatement-as-contribution aside
**ASN-0043, L11a**: "Within-state single-valuedness (an address names at most one link) is immediate from the partial-function typing `Σ.L : T ⇀ Link`; L11a is the cross-event strengthening."
**Problem**: The first clause restates the defining property of a partial function (each argument has at most one image) as though it were a derived guarantee, then re-characterizes L11a relative to it. This adds no reasoning the `T ⇀ Link` typing does not already make trivially true; it is the kind of clarifying aside that accretes around a claim without advancing it.
**Required**: Delete the sentence, or compress to a half-line parenthetical if the within-state/cross-event distinction must be signposted.

## OUT_OF_SCOPE

### Topic 1: Query-time equivalence of equal-coverage, different-decomposition endsets
**Why out of scope**: The Open Question "Under what conditions should two endsets with different span decompositions but identical coverage be treated as equivalent for query purposes?" concerns query/search semantics, which this ASN does not model. It is correctly left open and should not be resolved here. (Note: this is the finer, search-level question; L8's type-equivalence is the in-scope commitment — keeping them distinct is the right call, see Issue 2 for the rationale-prose fix.)

VERDICT: REVISE
