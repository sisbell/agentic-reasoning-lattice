# Review of ASN-0042

## REVISE

### Issue 1: O15 condition (viii) carries an axiom-justification essay, not the axiom
**ASN-0042, O15 (PrincipalClosure)**: "Without (viii), O15 would admit a strict extension whose intervening stream positions were never baptized — a prefix that O18's material baptism (which adds exactly `next(Σ.B, p, d)`, O17b) cannot realize in the single introducing transition. Gregory's allocation path confirms the restriction: `findpreviousisagr` followed by `tumblerincrement(…, 1)`... so (viii) records sequential next-reachability as the admissible discipline."
**Problem**: This paragraph explains *why the condition is needed* (counterfactual collapse, implementation corroboration, Nelson exegesis) rather than stating *what it says*. It is the "new prose around an axiom explains why the axiom is needed" anti-pattern, and it forward-references O18/O17b mid-definition. A precise reader must skip past it to reach the actual conjunct.
**Required**: Reduce to the formal clause `pfx(π') = next(Σ.B, p, d)` for some B6-valid `(p, d)`. Move the necessity argument, if kept at all, to a single dedicated remark — not embedded in the predicate's defining list.

### Issue 2: The `delegated` definition enumerates downstream consumers instead of advancing meaning
**ASN-0042, Definition (delegated)**: "Condition (vii) asserts the pre-state freshness `pfx(π') ∉ Σ.B`; its post-state counterpart `pfx(π') ∈ Σ'.B ∖ Σ.B` is O18. Condition (viii) asserts pre-state next-reachability...; it is what makes O18's material baptism realizable as a single `Bop(p, d)` step (O17b)."
**Problem**: A definition's body should fix the predicate, not catalogue which later results (O18, O17b, Bop) consume each conjunct. This is the "definition's introduction enumerates downstream consumers" pattern.
**Required**: State the four-place signature and the conjuncts; drop the O18/O17b consumer commentary.

### Issue 3: The next-reachability caveat is restated in five places in different words
**ASN-0042**, the clause "the right is to delegate single-step stream extensions of an already-baptized prefix, not an arbitrary strict descendant" (or paraphrase) appears in: the `delegated` definition, O15 prose, O7(c) prose, O7 Formal Contract postcondition (c), and O10 condition (c).
**Problem**: "Two paragraphs in the same document say the same thing in different words" — here five. The caveat compounds across the note. Each restatement must be kept in sync; they will drift.
**Required**: State the constraint once (in O7(c), where the recursive right is the object-level claim) and reference it elsewhere as `condition (viii)` without re-prose.

### Issue 4: O17b axiom buried under implementation-corroboration essay
**ASN-0042, O17b (BaptismalRegistryCoupling)**: "Gregory confirms the funnel: every granfilade write in udanax-green flows through the single ISA-allocation choke point `findisatoinsertgr` and the sole write primitive `insertseq`... The `Bop` of ASN-0040 is the abstract image of that funnel."
**Problem**: This is essay content in an axiom slot — it argues the axiom is faithful to the implementation rather than stating the coupling. The preceding "Consequently every registry reachable under → is reachable under ASN-0040's..." already does the load-bearing work.
**Required**: Keep the formal coupling and the transfer consequence; demote the funnel narrative to at most one corroborating sentence.

### Issue 5: Redundant precondition on O1
**ASN-0042, O1 Formal Contract**: "*Preconditions:* `π ∈ Π`, `a ∈ T`, `T4(pfx(π))`."
**Problem**: `T4(pfx(π))` is already guaranteed unconditionally by the `pfx` axiom's postcondition (b) (`T4(pfx(π))` for every `π ∈ Π`). Listing it as a precondition implies `owns` could be invoked on a non-T4 prefix, which the model excludes. The decidability postcondition likewise needs only prefix comparison, not field extraction, so the T4 hypothesis is doing nothing here.
**Required**: Drop `T4(pfx(π))` from O1's preconditions (or note it is inherited from the `pfx` axiom rather than assumed).

## OUT_OF_SCOPE

None. The note's claims (O1–O10, supporting lemmas) all concern ownership state, the delegation/fork operations on it, and their invariants, stated abstractly; the substantive proofs (O2 exclusivity, O3 refinement, O8 irrevocability, O10 unilateral fork, the non-coverage analysis) are case-complete and the worked example exercises every property against concrete addresses. The findings above are local accretion, not topic drift.

VERDICT: REVISE
