# Review of ASN-0068

## REVISE

### Issue 1: CV-ATOM derivation re-litigates "maximality, not uniqueness" three times
**ASN-0068, CV-ATOM derivation part (b)**: "The supposition that these consecutive pairs are witnessed by `n` separate width-1 runs is therefore already false by non-maximality, not by any uniqueness conflict: the disqualifying fact is the same maximality failure that part (a) invokes. ... CV-MAX's uniqueness then merely pins this extension as the *sole* representation in `MaxRuns`; it is maximality, not uniqueness, that forces the aggregation."
**Problem**: The same attribution point — that aggregation is forced by maximality rather than uniqueness — is asserted three times within part (b) and again in the closing "Both behaviors flow from a single source" paragraph. This is reviser drift: prose re-explaining which mechanism does the work rather than advancing the derivation. The first sentence ("a width-1 run at an interior pair ... fails right-maximality and is excluded") already discharges the claim; the rest re-states it.
**Required**: Collapse part (b) to the single load-bearing observation (interior width-1 runs are right-extendable, hence non-maximal, hence excluded). Delete the repeated maximality-vs-uniqueness attribution sentences.

### Issue 2: Example 2 carries a defensive notation-collision aside
**ASN-0068, Example 2**: "(This cross-side offset between sides of a single pair is a different quantity from the cross-run offset `δ = j²_a − j¹_a = j²_b − j¹_b` of the CV-MAX uniqueness proof, which constrains two runs that witness the *same* pair; here we have two runs witnessing two *different* pairs.)"
**Problem**: This parenthetical exists only to pre-empt confusion between two uses of the word "offset." It advances no reasoning about the example; it defends the prose against a misreading. This is meta-prose in a worked-example slot.
**Required**: Remove the aside. If the collision is real, rename one of the two quantities at its definition site so no disambiguating paragraph is needed.

### Issue 3: CV-IN-N introduction explains why the result is structured rather than stating it
**ASN-0068, after CV-IN**: "The precondition `actionPoint(width(σ)) = m_σ` is not an arbitrary strengthening — it is necessary, and we record the necessity as a labeled result parallel to the foundation's T10a-N."
**Problem**: "we record the necessity as a labeled result parallel to the foundation's T10a-N" is framing about document structure and an appeal to a foundation result's *shape*, not its content. It advances the argument no further than "CV-IN-N states the necessity," which the label already conveys.
**Required**: Reduce to a single clause motivating the constraint (level-uniformity does not bound the action point), then state CV-IN-N. Drop the "parallel to T10a-N" rhetorical framing.

### Issue 4: Closing flourish in "What the Result Cannot Express"
**ASN-0068, final paragraph**: "These omissions are not deficiencies of the operation; they are consequences of grounding correspondence in I-address identity. Every operation that consumes I-addresses inherits exactness from the addressing scheme. The comparison operation is no exception — and the things it cannot express are precisely the things that would require a different grounding."
**Problem**: The (i)–(iii) list above it already states what the operation cannot express (legitimate "does-not-do" content). This trailing paragraph is essay content restating that point in general terms without adding a claim or constraint.
**Required**: Delete the paragraph; the enumerated list is the substantive content.

## OUT_OF_SCOPE

### Topic 1: Concurrent-modification invariants
**Why out of scope**: The first Open Question (invariants under concurrent mid-comparison modification) is genuinely new territory — it requires a concurrency/transition-interleaving model this single-snapshot operation does not define. Correctly left as an open question, not an omission.

### Topic 2: Replication equivalence across docuverse copies
**Why out of scope**: Determinism across replicated copies (second Open Question) depends on the replication/BEBE protocol, explicitly excluded by scope.

META: not applicable — the ASN defines state-grounded operation semantics (a read-only observer over `M`) with abstract invariants, and remains within specification territory; the findings are localized prose accretion, not drift.

VERDICT: REVISE
