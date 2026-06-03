# Review of ASN-0068

I checked the proofs of CV-MAX (existence + uniqueness), CV-PRED, CV-IN-N, CV-SPAN-VIEW, CV-FIN, and the five worked examples for rigor, and audited the prose against the anti-bloat / forward-reference patterns flagged for this note. The mathematics holds — CV-MAX's two-region run reconstruction, the lockstep-offset uniqueness argument, the depth-independent walk in Example 4, and the restriction-fragmentation in Example 5 are all sound, and the cross-ASN references stay inside the foundation set. The remaining issues are prose-redundancy items of the kind the anti-bloat classifier targets.

## REVISE

### Issue 1: Trivial exhaustiveness prose duplicated in CV-SELF claim and justification
**ASN-0068, CV-SELF**: claim box — "The two sets are disjoint (by the `v¹ = v²` discriminator) and exhaustive (every pair either has `v¹ = v²` or `v¹ ≠ v²`, by trichotomy of equality)"; justification — "The discriminator is trichotomous, so `corr_{a,a} = D ∪ X` is exhaustive."
**Problem**: "every pair either has `v¹ = v²` or `v¹ ≠ v²`" is a trivially-true filler (the law of the excluded middle on equality), and the disjointness/exhaustiveness statement is made once in the claim box and re-derived in the justification. This is exactly the exhaustiveness-claim + same-thing-twice pattern called out for this note.
**Required**: State the `D ∪ X` decomposition in the claim. Drop the parenthetical "by trichotomy of equality" triviality and the justification's closing re-statement; the justification only needs to establish that `D` and `X` are precisely the `v¹=v²` and `v¹≠v²` cases.

### Issue 2: CV-PRED's closing "convention" restates the left-maximality disjunct
**ASN-0068, CV-PRED (final sentence)**: "We adopt the convention that left-maximality of a run starting at `v_a` is automatic when `v_a − 1` does not exist (i.e., `(v_a)_m = 1`), and symmetrically on the b-side."
**Problem**: The *Left-maximal* definition already opens with "either `v_a − 1` does not exist as a V-position of depth `m_a` (CV-PRED), or …". The CV-PRED sentence says the same thing in different words, in a different slot, before the definition it duplicates is even stated. CV-PRED's existence clause already supplies the `(v_a)_m = 1 ⟹ no predecessor` fact, so left-maximality's first disjunct consumes it directly with no separate convention needed.
**Required**: Delete the closing convention sentence from CV-PRED; the existence clause plus the left-maximality disjunction already carry it.

### Issue 3: CV-PRED "Dual inverse" clause has no use site
**ASN-0068, CV-PRED (*Dual inverse*)**: "For every `j ≥ 0`: `(v + j) − j = v`."
**Problem**: The CV-MAX existence and uniqueness proofs invoke the *Inverse property* `(v − j) + j = v` (e.g. the right-region reduction `((v−j)+j)+c = v+c`) and the last-component reduction, but I find no proof, example, or maximality clause that invokes the *Dual inverse* `(v+j)−j = v`. An unused clause carried in a definition box is accretion.
**Required**: Either cite the use site that needs `(v + j) − j = v`, or remove the clause. (The *Convention*, *Existence*, *Uniqueness*, and *Inverse property* clauses are all load-bearing and should stay.)

## OUT_OF_SCOPE

None. The degenerate-case claims (CV-LINK-DEGEN, CV-LINK-SELF, CV-SELF) and the necessity claim CV-IN-N are in-scope characterizations of this operation's admissibility and boundary behavior, not new territory. The open questions about concurrent modification, replication, sub-allocator-boundary runs, and multi-document composition are correctly deferred as future ASNs.

VERDICT: REVISE
