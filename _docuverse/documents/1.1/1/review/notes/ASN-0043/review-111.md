# Review of ASN-0043

## REVISE

### Issue 1: Worked-example invariant boilerplate contradicts its own preamble and repeats verbatim across six steps
**ASN-0043, "Worked Example" (Extension, Steps 1–6)**: The extension preamble states "*Each added link is a fresh sibling.* … FSP applies, so only the new check per step is shown below." Yet each of Steps 1, 2, 3, 4, 5, 6 still closes with a near-verbatim sentence of the form: "The remaining state-local invariants at Σ_i (L0, L1, L1a–c, …, L-fin) hold for the new entry by the fresh-sibling argument above, and for the pre-existing entries by L12."

**Problem**: This is the "two paragraphs say the same thing in different words" pattern, ×6, and it directly contradicts the preamble's promise that *only the new check per step is shown*. Once FSP is established and the preamble declares each added link a fresh sibling, restating "all the other invariants hold by FSP + L12" at every step adds nothing — it is exactly the meta-prose a reader skips to reach the step's actual new content (L11b, L13, arity-4, discrimination, multi-span, coverage-vs-decomposition).

**Required**: Delete the repeated closing sentence from Steps 1–6; the preamble already discharges it once. Keep only the per-step *new* checks the example exists to exercise.

### Issue 2: Forward-reference scaffolding clause that does not advance the argument
**ASN-0043, paragraph preceding "Definition — Endset"**: "We now define the components, admitting arity beyond three; the StandardTriple convention and L3 below fix the standard form and its formal invariant."

**Problem**: The clause after the semicolon is pure forward-reference scaffolding — it announces that two downstream items "fix the standard form and its formal invariant" without stating any content. The Convention and L3 that follow speak for themselves; this is the meta-prose-around-forward-references pattern the anti-bloat classifier targets.

**Required**: Cut the clause to "We now define the components, admitting arity beyond three." Let StandardTriple and L3 stand on their own.

### Issue 3: L11a is a cross-event lemma, not a state-local invariant, yet FSP "preserves" it with a redundant freshness argument
**ASN-0043, "A Shared Conformance Lemma" (state-local invariant list) and FSP proof, L11a bullet**: The list includes "L11a" among "the state-local L- and S-invariants," and the FSP bullet reads "*L11a.* `a ∉ dom(Σ.L)` (h1), so the new allocation event produces an address distinct from every previously-allocated link address."

**Problem**: L11a (LinkUniqueness) is a derived lemma about *distinct allocation events* producing distinct addresses, proved globally from L1c + S7d + GlobalUniqueness. Its per-state form is just set-distinctness of `dom(Σ.L)`, which is trivial. Listing it as a preserved state-local invariant and giving a separate freshness-based justification is redundant twice over: (i) the real content of L11a holds in `Σ'` automatically because FSP already preserves L1c and S7d, from which GlobalUniqueness re-derives it; and (ii) the freshness argument given is a *weaker, different* mechanism than L11a's actual basis. This conflates a global theorem with a state invariant.

**Required**: Remove L11a from the state-local invariant list and drop its FSP bullet, noting once (if needed) that L11a holds in `Σ'` because it follows from the preserved L1c + S7d via GlobalUniqueness.

## OUT_OF_SCOPE

### Topic 1: Global content-subspace invariant extending disjointness beyond the s_C slice
**Why out of scope**: L14/L14a are honestly scoped to `s_C`-resident content, and the first Open Question already flags whether a content-side invariant should fix a global content-subspace constant. This is new territory for a future ASN, not an error here.

### Topic 2: Equivalence of distinct span decompositions with identical coverage for query purposes
**Why out of scope**: The Coverage definition flags the lossy projection and the Open Questions list it explicitly; resolving when such endsets are query-equivalent is future work, not a gap in this ASN's stated claims.

VERDICT: REVISE
