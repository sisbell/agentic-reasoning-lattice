# Review of ASN-0070

## REVISE

### Issue 1: Downstream-consumer inventory in the F-canon-form / F-canonical split
**ASN-0070, "Canonical Form" (paragraph after clauses (i)–(iii))**: "That a canonical form of this shape *exists and is unique* ... is a separate proof obligation, established next as a theorem (F-canonical, THM); **F-det and F-empty lean on this uniqueness result, not on the shape alone.**"
**Problem**: The clause naming F-det and F-empty as consumers is a use-site inventory attached to a definition — a forward-reference accretion pattern. It does not advance the DEF/THM distinction.
**Required**: State the DEF (shape) vs THM (existence+uniqueness) split; delete the "F-det and F-empty lean on this" inventory. The dependence is already recorded in each lemma's Depends line.

### Issue 2: "Does not appeal to" defensive prose in the joint V-restricted denotation
**ASN-0070, "V-Restricted Denotation"**: "This is a property of the filtered denotation sets alone — it does not appeal to S3★-aux's exhaustiveness, nor even to `dom(M(d))` membership ... Disjointness here matches F0's own partition, where the same single-valued first-component projection (not exhaustiveness) supplies disjointness."
**Problem**: The disjointness is already established in the preceding sentence (subspace clause + SC-NEQ). The two trailing sentences only narrate what the argument does *not* rely on and cross-match F0 — meta-prose that the reader must skip.
**Required**: Keep the substantive justification (every element of one set has first component s_C, the other s_L, and s_C ≠ s_L). Delete the "does not appeal to..." and "matches F0's own partition..." sentences.

### Issue 3: Cataloguing rationale for F-sound / F-complete
**ASN-0070, "Derived Properties" (intro)**: "They are not independent obligations but consequences of the postcondition by set-equality unpacking ... **We catalogue them separately because they correspond to the two distinct error modes an implementation might exhibit ... and because verifiers may find it convenient to check each direction separately.**"
**Problem**: Essay content justifying why two lemmas exist, in a structural slot. It adds no reasoning to either lemma.
**Required**: Reduce to the substantive fact (each lemma is one inclusion of the postcondition equality). Remove the "we catalogue them separately because" rationale.

### Issue 4: "Two arguments play different roles" paragraph in F-multi
**ASN-0070, F-multi (closing paragraph)**: "The two arguments play different roles. The implication is what the operation guarantees ... The admissibility result is what makes the hypothesis a non-trivial precondition ... F-multi names both together because operational interest in multiplicity preservation depends on both ..."
**Problem**: Pure meta-prose explaining why the lemma bundles an implication with an admissibility result. The two arguments are already labelled and proved above it.
**Required**: Delete the paragraph.

### Issue 5: Corollary-label justification in F-state (and duplication with the State-Dependence section)
**ASN-0070, F-state**: "This is not a property of `follow` per se; it is the composition of L12 ... **We catalogue it as a corollary because callers reasoning about resolution-stability across transitions must invoke it.**"
**Problem**: (a) The "we catalogue it as a corollary because..." clause justifies the label rather than the claim. (b) This restates, almost verbatim, the earlier "State-Dependence" section ("This is not a derived property of the operation but a structural consequence of two facts already established: (i)... (ii)..."). Two passages in different sections say the same thing.
**Required**: Drop the cataloguing-rationale clause. Collapse the duplicate composition argument into a single site (either the section or the corollary, not both).

### Issue 6: Worked-configuration preambles tally what prior configurations failed to exercise
**ASN-0070, "A Worked Example" (configs 5, 6, 7)**: e.g. "The four configurations above all yield `Σ_V^{s_L} = ⟨⟩`; none exercises the link-subspace branch ..."; "The five configurations above each yield a *single*-component result ..."; "The six configurations above never exercise fragmentation ..."
**Problem**: Each added configuration opens with a running inventory of the coverage gaps of every earlier configuration. This is exactly the use-site/exhaustiveness accretion the anti-bloat classifier targets — it compounds with every cycle that adds a configuration. The worked computations themselves are object-level and fine; the enumerating preambles are not.
**Required**: State each configuration's purpose in one clause (e.g., "Cross-subspace straddle: both result components non-empty."). Remove the cumulative tally of prior configurations' omissions. Reconsider whether all seven configurations earn their place — configs 1, 2, 3, 5, 7 already cover sound/complete/multi/empty/cross-subspace/both-populated.

### Issue 7: Positivity-convention rationale stated twice
**ASN-0070, "V-Restricted Denotation" definition** ("The positivity clause ... is what makes the filter an *admissible-V-position* filter rather than a bare depth-and-subspace filter ... these are not V-positions of `d` and the postcondition equality would force them to be excluded anyway. The positivity clause makes this exclusion explicit...") **and F-canon-form clause (i)** ("The start positivity is a *canonical-form convention*, not a consequence of the postcondition equality ... only the convention separates them.").
**Problem**: Two heavily defensive passages arguing the same underlying point ("the bare denotation admits extra tumblers; positivity/the convention excludes them"). The inline counterexample `([1,0], δ(3,2))` in clause (i) is object-level and worth keeping; the surrounding "not a consequence of...", "would be excluded anyway", "only the convention separates them" framing is redundant defense across two sites.
**Required**: Keep the filter definition's positivity clause and the one counterexample. Trim the duplicated "this is a convention, not a consequence / excluded anyway" justification to a single sentence at one site.

## OUT_OF_SCOPE

### Topic 1: Partial-reach reporting and content-retrieval coupling
The Open Questions on whether the result must preserve which I-addresses failed to resolve, and on the resolution↔content-lookup relationship, are genuine future-ASN territory (result-form contracts, retrieval operation), not defects here.
**Why out of scope**: These concern downstream system-level contracts and a retrieval operation this query note does not define.

### Topic 2: Concurrency semantics of `follow`
The concurrency Open Question is correctly deferred.
**Why out of scope**: Transaction/concurrency model is a separate concern from the pure-query denotation specified here.

META: not applicable — the note specifies state-relative query denotation, a per-subspace result invariant, and frame, which is in-scope abstract specification; its problems are accreted meta-prose, not drift.

VERDICT: REVISE
