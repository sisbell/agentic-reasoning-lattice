# Review of ASN-0093

I checked the three primitives, the sub-allocator chain machinery, the simultaneous-induction discharge, and the nine-step worked example. The correctness skeleton holds up: anchor construction (`b_C(d)=inc(d,2)`, `b_L(d)=inc(b_C(d),0)`), the C1c/L1c chain exhibitions (first-emit and subsequent-emit), the contiguity argument in ChainMembershipForOrigin, and the freshness closures (within-doc via ChainEnumerationInjectivity, cross-doc via T10, cross-subspace via T7) all close. The TA5a boundary at `zeros(b_C(d))=3` (k=1 admissible at exactly 3) and the prefix-document case `d ≺ d'` (separator divergence at `#d+1`) are both handled correctly. I found no missing edge case or proof gap.

The findings below are all the forward-reference/accretion patterns the `review-mode.anti-bloat` classifier directs me to surface, plus one dangling symbol.

## REVISE

### Issue 1: Definition enumerates downstream consumers
**ASN-0093, State model**: "the frame rows below cite this without re-deriving it."
**Problem**: The object-level fact (projections are state-independent) is legitimate and useful. The trailing clause is a use-site inventory pointing at the discharge matrix — it advances no reasoning, it only announces how a later table will reference the fact. This is precisely the "definition's introduction enumerates downstream consumers" pattern.
**Required**: Drop the clause; keep only the state-independence statement and its consequence.

### Issue 2: C-fin restates a downstream use-site already established at K.α
**ASN-0093, C-fin**: "C-fin is what makes the set `{a' ∈ dom(C) : origin(a') = d}` finite at every reachable state, in turn making the `max` invoked in `K.α`'s subsequent-emission precondition well-defined."
**Problem**: Use-site inventory. The well-definedness of `max` is already established at K.α's binding precondition ("The `max` is well-defined because the set is finite (C-fin restricted by `origin(·) = d`)"). Stating it again at C-fin's definition is the same fact in two places. L-fin's parallel definition carries no such sentence, confirming it is removable accretion.
**Required**: Delete the sentence; the K.α precondition is the correct site for the well-definedness claim.

### Issue 3: Forward reference to the discharge matrix inside an invariant statement
**ASN-0093, L14**: "(The discharge matrix records the StoreT4Validity dependency that supplies T7's T4-validity precondition.)"
**Problem**: A parenthetical pointer to a downstream section that records the dependency. It does not advance L14; it tells the reader where to look later. Combined with Issue 4 below, the L14 derivation is now stated three times (the invariant body, this pointer, the properties table, and again in the Cross-document section).
**Required**: Remove the parenthetical.

### Issue 4: L14 derivation restated a third time in the Cross-document section
**ASN-0093, Cross-document disjointness chain (final sentence)**: "Cross-subspace collisions between `dom(C)` and `dom(L)` are prevented by L14 (StoreDisjointness, above), itself derived from L0 + SC-NEQ + T7."
**Problem**: Duplication — "two paragraphs in the same document say the same thing." L14's derivation (`L0 + SC-NEQ + T7`) is already stated in the L14 invariant body and again in the Properties table. The substantive cross-subspace claim is covered by L14 itself; the appended re-derivation is noise the reader must skip.
**Required**: Either drop the sentence entirely (L14 already covers cross-subspace), or reduce it to a bare cross-reference without re-listing the derivation premises.

### Issue 5: ChainMembershipForOrigin enumerates which form downstream consumers will cite
**ASN-0093, ChainMembershipForOrigin (after the two bullet clauses)**: "The weaker subset inclusion ... is the immediate corollary of the contiguous-prefix form; downstream consumers cite either form as needed."
**Problem**: "downstream consumers cite either form as needed" is a use-site inventory appended to a lemma statement. Stating the corollary is fine; advertising that consumers will pick one form or the other is meta-prose.
**Required**: Keep the corollary; drop the "downstream consumers cite either form as needed" clause.

### Issue 6: Unexplained symbol in the Properties Introduced table
**ASN-0093, Properties Introduced**: "L1a | LinkScopedAllocation | INV | ASN-0043 (refactored: `E_doc` → `dom(M)`)"
**Problem**: `E_doc` is never defined in this note, and ASN-0043's L1a (per the foundation statements) is `home(a) ∈ dom(Σ.M)` — it already uses `dom(M)`, with no `E_doc`. The reader cannot resolve `E_doc`; it appears to be a stale artifact from a prior draft.
**Required**: Either define what `E_doc` refers to or remove the parenthetical refactoring note.

## OUT_OF_SCOPE

### Topic 1: Generalization of the anchor construction beyond two subspaces
The `inc`-based anchor construction relies on `s_C = 1` (so `b_C(d) = inc(d, 2)` directly yields `[d.0.s_C]`) and `s_L = s_C + 1` (so a single `inc(·, 0)` advances `b_C(d)` to `b_L(d)`). A third subspace `s ≥ 3` would not be reachable by one sibling advance.
**Why out of scope**: The substrate explicitly axiomatizes exactly two subspaces (SubspaceConventionAxiom) and lists the third-subspace coordination question under Open Questions. Generalizing the construction is a higher-layer concern, not an error in this note.

META: not applicable — the note specifies state (`Σ = (C, L, M)`), three operations, and the invariants they preserve at an abstraction an alternative implementation would also have to satisfy; the code citations in SubspaceConventionAxiom are sourcing for a design commitment, not implementation mechanics in the invariants themselves.

VERDICT: REVISE
