# Review of ASN-0075

## REVISE

### Issue 1: wp(SHOWDELETIONS, q) is not the weakest precondition
**ASN-0075, "The SHOWDELETIONS Operation"**: "wp(SHOWDELETIONS(d_A, d_B), q) = (d_A ∈ E_doc ∧ d_B ∈ E_doc ∧ Σ is a composite-boundary state)", where q abbreviates "Result = (DeletedFromAWithB(d_A, d_B), DeletedFromBWithA(d_A, d_B))".

**Problem**: q is pure set equality — the operation returns those two comprehensions by definition. Establishing q requires only that the comprehensions are computable: d_A, d_B ∈ E_doc and finiteness of dom(C) / the arrangements. Finiteness (C-fin, S8-fin) holds at *every* reachable state, not only at composite boundaries. So the composite-boundary conjunct is strictly stronger than what q needs; it is not the *weakest* precondition for q. The boundary requirement is genuinely load-bearing for D-EXH's exhaustiveness and for the semantic meaning of the report (via P4★/D-WIT, which only hold at boundaries) — but not for q. The text equates `wp(op, q)` with the operation's *stated precondition*, conflating the two.

**Required**: Either drop the boundary conjunct from `wp(op, q)` (the genuine weakest precondition for the bare set-equality q), or strengthen q to the classification-level postcondition (exactly-one-of CURRENT/DELETED/NEVER_INCLUDED per pair) for which composite-boundary *is* weakest. State which guarantee the boundary conjunct buys, rather than attaching it to a postcondition that does not require it.

### Issue 2: Section thesis duplicates the D-NEED corollary verbatim
**ASN-0075, "Why the Provenance Relation Is Load-Bearing" (opening) vs. Corollary D-NEED**: opening — "any conforming implementation must maintain auxiliary state components beyond (C, L, E, M) that suffice to disambiguate the predicates DELETED(a, d) and NEVER_INCLUDED(a, d) at every reachable state"; D-NEED — "Any system supporting SHOWDELETIONS must maintain at least one state component beyond (C, L, E, M) whose value disambiguates DELETED(a, d) from NEVER_INCLUDED(a, d) at every reachable state."

**Problem**: The section's opening sentence states the corollary's conclusion essentially word-for-word, before the lemma that earns it. This is the anti-bloat "two paragraphs say the same thing in different words" pattern flagged for this note's classifier.

**Required**: Reduce the opening to a one-line statement of what the section will prove and let D-NEED carry the conclusion, or vice versa — do not state the result twice in identical terms.

### Issue 3: Internal redundancy in the granularity paragraph
**ASN-0075, "The Three States of Content"**: "A per-occurrence removal … is therefore *invisible* to this classification while any occurrence of `a` survives in `d` (`a` becomes DELETED against `d` only when the *last* V-occurrence is removed)".

**Problem**: The parenthetical restates the preceding clause — "invisible while any occurrence survives" and "DELETED only when the last occurrence is removed" are the same fact. One clause suffices.

**Required**: Delete the parenthetical (or the preceding clause); keep a single statement of the set-granularity consequence.

## OUT_OF_SCOPE

### Topic 1: Per-occurrence (V-position) deletion detection
The ASN correctly scopes out distinguishing which of several V-positions holding the same I-address was removed. This is a Vstream concern; the I-address-set predicates are the right granularity here. No action needed — noted only to confirm the scoping is appropriate, not an error.

META: not applicable — the ASN defines an observational operation, the state it consults, and abstract invariants over its output; it specifies a system guarantee, not implementation mechanics, and has not drifted.

VERDICT: REVISE
