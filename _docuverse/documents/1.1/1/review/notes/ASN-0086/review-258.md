# Review of ASN-0086

## REVISE

### Issue 1: SliceUniqueness parenthetical duplicates the higher-arity remark and adds defensive justification

**ASN-0086, Lemma — SliceUniqueness**: "(At-most-one, not exactly-one: a higher-arity address with `|Σ.L(a)| ≠ 3` fails every slice's `|Σ.L(a)| = 3` conjunct and indexes *zero* slices, consistent with *Definition — TupleAddress* and the higher-arity remark above. At-most-one is exactly what the disjoint union requires.)"

**Problem**: This restates content already given verbatim-in-substance in *Definition — TypedRelation* ("the store may also hold higher-arity links (`|Σ.L(a)| > 3`), which then inhabit `A_rel^Σ = dom(Σ.L)` but index no tuple of any `L_K`"). The parenthetical adds nothing to the proof — `Σ.L` is a partial function, so each `a` indexes at most one slice; that single sentence is the lemma. The trailing material is meta-prose: a use-site back reference ("consistent with *Definition — TupleAddress* and the higher-arity remark above") plus a defensive justification of the lemma's own framing ("At-most-one is exactly what the disjoint union requires"). This is the flagged "two paragraphs say the same thing in different words" pattern, with a defensive coda.

**Required**: Delete the parenthetical. The one-line function-ness argument already establishes at-most-one; the higher-arity exclusion lives in *Definition — TypedRelation* and need not be re-stated here.

### Issue 2: WP Case 1 "slack" sentences explain rather than advance

**ASN-0086, Weakest-Precondition Analysis, Case 1**: "The disjunct `a = a_emit(Σ, d_retr)` is the *self-emit branch*: it is reached precisely when the caller asks to nullify the very address at which the internal `Emit_R` will deposit its retractor. It is the slack that separates the weakest precondition from the merely sufficient `P0 ∧ P1`, which excludes this branch."

**Problem**: The subsequent *Reduction* paragraph derives the same disjunct rigorously and concludes that the wp "coincides with the operation's own precondition `P0 ∧ P-tgt`." These two sentences pre-announce that conclusion in essayistic terms ("the slack that separates...") before the derivation that earns it. They sit in a structural (wp-derivation) slot and restate, informally, what the formal reduction then proves.

**Required**: Drop the editorializing sentences; let the *Reduction* paragraph carry the self-emit disjunct. If a one-clause gloss on the self-emit branch is wanted, fold it into the derivation rather than stating it twice.

## OUT_OF_SCOPE

### Topic 1: Cross-layer type-collision and arrangement-visibility invariants

The Open Questions correctly defer the interaction between `L_K` and `Σ.M` visibility, dynamic admissible-type introduction across uncoordinated layers, and higher-arity relational projections. These are new territory layered above the K.σ/K.α/K.λ substrate, not gaps in this note's claims.

VERDICT: REVISE
