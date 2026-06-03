# Review of ASN-0069

## REVISE

### Issue 1: V8a introduces a third notation for the sibling/version stream that is never reconciled with V10's sibling notation
**ASN-0069, §"Structural Correspondence" (V8a setup)**: "Write the version stream of `d_src` as `w⁰ := d_src`, `w¹ = inc(d_src, 1)` ... and `wⁱ = inc(wⁱ⁻¹, 0)` for `i ≥ 2`"

**Problem**: These `wⁱ` are exactly the emissions of `A_v(d_src)` — i.e., the *sibling forks* of `d_src` that the "Notation for multiple forks" block names `d_new¹, d_new², …`. The worked example confirms the identity: "the new fork is `d_new² = inc(d_new, 0)`", which is precisely `w²`. So `w²` and `d_new²` denote the *same tumbler*, yet V8a invents a third notation (`wⁱ`) that the notation block does not cover and never connects to `d_new^i`. A precise reader cannot tell that V8a (version stream) and V10 (sibling forks) range over identical objects, nor that V8a and V11 are genuinely distinct (siblings, length `#d_src+1`, vs chain, length `#d_src+k`) rather than the same theorem twice.

**Required**: Either restate V8a using the established sibling notation `d_new^i`, or extend the "Notation for multiple forks" block to introduce the `w`-stream and assert `wⁱ = d_new^i` explicitly. State once that V8a's stream is the sibling configuration and V11's chain is the distinct nesting configuration, so the parallel inductions are not mistaken for duplication.

### Issue 2: The V8 paragraph previews a weaker second-version result that it then abandons
**ASN-0069, §"Structural Correspondence"**: "the transitive `d_src ↔ d_new` correspondence follows by composing two V8 instances ..." then "The two-step composition just sketched does not generalise by itself ... We supply that induction directly."

**Problem**: The second-version two-step sketch is the `k = 2` instance of V8a, which immediately follows and subsumes it. The text states a special case, declares it non-general, and discards it before proving the general claim. The discarded sketch advances no reasoning that V8a does not — the reader works through a composition that is announced as inadequate. This is preview-then-abandon meta-prose of the kind that accretes around inductive lemmas.

**Required**: Delete the second-version sketch and the "does not generalise by itself" disclaimer. Lead directly into V8a (the general induction), keeping only the one-sentence pointer that V8a gives the transitive correspondence across the stream.

### Issue 3: V7's property inventory is a defensive use-site enumeration redundant with the worked example
**ASN-0069, §"The Empty-Source Case"**: "This vacuity governs V4, V4b, V8, V8a, V9, V9a, V9b, V11, and the content clauses of V10 alike — including V11 and V8a, whose quantifiers range over `V_{s_C}(d_src)` and so are vacuous on the empty first fork, not substantive."

**Problem**: The paragraph opens by saying the empty case "is discharged concretely on `d_src°` in the worked example ... we do not restate that case-by-case here," then supplies a full property-by-property inventory with a defensive aside ("including V11 and V8a ... not substantive"). The organizing principle (vacuity by quantifier domain) is useful in one sentence; the exhaustive list of governed properties plus the defensive clarification is the use-site-inventory pattern, and it duplicates the concrete discharge the worked example already provides.

**Required**: Keep the single organizing sentence (structural properties hold substantively; properties quantified over `V_{s_C}(d_op)` hold vacuously). Drop the enumerated property list and the "including V11 and V8a … not substantive" defensive clause, letting the worked example carry the concrete discharge.

## OUT_OF_SCOPE

### Topic 1: Concurrent fork-during-modification, snapshot-vs-living forks, descendant enumeration
**Why out of scope**: These are correctly confined to the "Open Questions" section as future inquiries; they concern guarantees beyond the sequential-atomic transition model this ASN builds on, not gaps in the present derivation.

VERDICT: REVISE
