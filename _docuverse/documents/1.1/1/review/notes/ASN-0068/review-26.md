# Review of ASN-0068

## REVISE

### Issue 1: CV-SPAN-VIEW re-narrates "presentational, not semantic" two to three times
**ASN-0068, CV-SPAN-VIEW**: Postcondition (c) already states "*input-dependent* presentational equivalence: the same triple `(v_a, v_b, n)` projects to different span-pairs at different depth pairs." The post-verification paragraph then repeats it ("both express the same ordinal count `n`... what CV-MAX coordinates is the *shared ordinal index* `k`"), and the closing paragraph repeats it a third time: "The triple form and the span-pair form carry the same information for fixed depths; the choice of representation is presentational, not semantic."
**Problem**: The injectivity/bijection (postcondition (b)) and input-parameterization (postcondition (c)) are the load-bearing content; the "presentational, not semantic" observation is then restated in two trailing prose paragraphs that add no new claim. This is the meta-prose accretion the anti-bloat classifier targets.
**Required**: Keep the formal postconditions (a)–(c); delete the closing "equivalently presents as a set of span-pairs... presentational, not semantic" paragraph and fold any surviving content (the differing-depth tumbler observation) into the Example 4 walkthrough where it is demonstrated concretely.

### Issue 2: CV-IN restates an admissibility consequence the per-side clauses already entail
**ASN-0068, CV-IN**: "If a single span literal lies in `R_a ∩ R_b` and both depths are defined with `m_a ≠ m_b`, both clauses constrain the same `σ` at incompatible depths and admissibility fails."
**Problem**: A span `σ = (start, width)` has one length `#width`. The per-side clauses already require `σ` to be level-uniform at depth `m_a` (so `#width = m_a`) and, if also in `R_b`, level-uniform at depth `m_b` (so `#width = m_b`). `m_a ≠ m_b` is therefore already unsatisfiable from the per-side clauses alone. The sentence is an exhaustiveness restatement imposing no new constraint.
**Required**: Delete the sentence, or if the corner is worth surfacing, reduce it to a one-clause parenthetical on the per-side level-uniformity clause rather than a standalone admissibility statement.

### Issue 3: Justification paragraphs carry forward-pointers to the Worked Examples
**ASN-0068, CV-SELF justification**: "Example 3 illustrates both components concretely." **CV-SPAN-VIEW prose**: "(Example 4 below illustrates this concretely)."
**Problem**: The examples in the Worked Examples section stand on their own and are already cross-referenced from that section's preamble ("a self-comparison case... (Example 3)... a differing-depths case (Example 4...)"). The inline forward-pointers embedded in the proof/justification slots are redundant deferrals — the accretion pattern where multiple sections point downstream.
**Required**: Drop the inline "Example N illustrates this" pointers from the justification and claim prose; the Worked Examples preamble already maps each example to the claim it exercises.

### Issue 4: Lemma justification closes with a historical/essay aside
**ASN-0068, CV-LINK-DEGEN justification**: "Nelson's 'word for word' intercomparison (LM 2/20) was conceived as a content-subspace operation; structurally, the operation specializes to `s_C` in practice."
**Problem**: This sentence sits inside a structural proof slot (the justification establishing emptiness via CL-OWN + S7) and asserts a generalization ("specializes to `s_C` in practice") that the lemma does not prove — the lemma proves emptiness for `s_L, d_a ≠ d_b`, not that the operation specializes. Essay content in a structural slot. The same Nelson framing recurs in the introduction and in the CV-ATOM closing paragraph.
**Required**: End the justification at the proven conclusion (`corr` restricted to `s_L` is empty, result `∅`). If the Nelson attribution is wanted, place it once in the introductory subspace discussion rather than appended to a degeneracy proof.

## OUT_OF_SCOPE

### Topic 1: Concurrent-modification and replication invariants
**Why out of scope**: The Open Questions on concurrent arrangement modification mid-comparison and on replicated-copy result agreement are correctly deferred — they require a concurrency/replication model this operation note does not establish, and replication touches BEBE territory excluded by Scope.

### Topic 2: Multi-document and version-history composition
**Why out of scope**: Composing multiple `compareversions` results into a multi-document correspondence, and walking a version history pairwise, are flagged as Open Questions and belong to a future composition ASN, not this pairwise-operation definition.

VERDICT: REVISE
