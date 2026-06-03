# Review of ASN-0070

This note carries the `review-mode.anti-bloat` classifier. The core argument (F0 inverse-image, F1 operation, F-canonical) is mathematically sound and the foundation citations are to permitted foundation ASNs. The findings below target accreted prose and example over-supply, plus the explicit self-deferrals the anti-bloat pass exists to catch.

## REVISE

### Issue 1: Derived Properties catalogue restates the prose sections nearly verbatim

**ASN-0070, "State-Dependence" / "Multi-Document Reach" / "Slot Uniformity" / "Origin Symmetry" / "Reachability" vs. "Derived Properties"**: e.g. F-state's body reads "The composition of L12 (link invariance) with the absence of any state component beyond `M(d)`... is developed in the State-Dependence section above."

**Problem**: Five narrative sections each get a second, formal restatement as a lemma (F-persist, F-state, F-multidoc, F-slot, F-origin). The two passes say the same thing in different words — the exact duplication the anti-bloat mandate flags. The lemmas then explicitly defer back to the prose ("developed in the State-Dependence section above"), confirming the redundancy rather than advancing it. The catalogue's own intro ("These properties are not independent axioms... They are readings of the same definition") concedes the point.

**Required**: Pick one home per property. Keep the formal lemma contract (preconditions/postcondition/depends/frame) and fold any load-bearing Nelson-grounding into a single sentence there; delete the standalone narrative sections, or demote them to one-line motivations. Remove the back-deferrals.

### Issue 2: Worked-example over-supply with overlapping coverage and defensive justification

**ASN-0070, "A Worked Example" (seven configurations)**: Config 7 closes with "...none of which the single-component configurations 1 and 5 establish jointly," and each configuration is prefaced "This configuration exercises...".

**Problem**: Seven configurations is over-supply. Config 2 and Config 7 both exercise F-multi; Config 5 and Config 7 both exercise the link-subspace branch. The closing justification of Config 7 (and the "exercises X end-to-end" tag on each) is meta-prose defending why the example is present rather than computing a result. One contiguous-coverage example, one multiplicity example, one no-reach, one cross-subspace straddle, and one state-dependence example would cover every derived property without repetition.

**Required**: Reduce to the minimal set that touches each F-property once. Drop the per-configuration "this exercises..." framing and the comparative justifications; let the computation and the ✓ checks stand.

### Issue 3: Forward-reference deferrals and downstream-consumer enumeration

**ASN-0070, claims table (F-canonical row)**: "Supplies the representational-existence-and-uniqueness result that F-det and F-empty depend on." Also the recurring "—see Canonical Form" / "see Canonical Form below" pointers in "Result Form and the Operation" and "Computation via Decomposition."

**Problem**: The F-canonical status note enumerates its downstream consumers instead of stating what the claim establishes — a flagged accretion pattern. Multiple sections defer to the same downstream "Canonical Form" location.

**Required**: State F-canonical's content in its own row without naming consumers. Collapse the repeated "see Canonical Form" pointers to a single forward reference at first use.

### Issue 4: Open Questions inflated into restated prose

**ASN-0070, "Open Questions"**: the canonicalisation question is a multi-clause paragraph ("must a downstream contract that consumes a `follow` result (a citation, a stable archival reference, or a compact representation of an unbounded-cardinality coverage) mandate canonical form and expose a canonicalisation procedure...").

**Problem**: Several of the six questions re-narrate material already settled in the body (canonical form, state-dependence, partial reach) as interrogatives rather than naming a genuinely open obligation. Essay content in a structural slot.

**Required**: Reduce each open question to a single sentence naming the unresolved guarantee. Drop questions whose answer the body already fixes.

## OUT_OF_SCOPE

### Topic 1: Concurrency semantics of `follow` under concurrent modification
**Why out of scope**: The third Open Question (concurrency guarantees when the queried document is being modified) is genuinely new territory — it concerns the transition system's atomicity contract, not this query's postcondition. Correctly deferred, not an error here.

VERDICT: REVISE
