# Review of ASN-0058

## REVISE

### Issue 1: Use-site inventory in the ContentReference definition
**ASN-0058, Definition (ContentReference)**: "The common depth satisfies `m ≥ 2`, a consequence of the preconditions rather than a separate assertion. ... Downstream claims (C0a, C1a) that hypothesize `m ≥ 2` draw it from here."
**Problem**: The closing sentence is a use-site inventory — it enumerates downstream consumers (C0a, C1a) of the `m ≥ 2` fact rather than advancing the definition. This is exactly the forward-reference accretion the note's classifier targets: the consumers cite this fact at their own sites already, so naming them here is redundant. The framing "a consequence of the preconditions rather than a separate assertion" is also defensive padding — the derivation that follows already shows it is a consequence.
**Required**: Keep the derivation (`#v ≥ 2` from S8a, `m = #v ≥ 2` from S8-depth). Delete the "Downstream claims (C0a, C1a) ... draw it from here" sentence and the "rather than a separate assertion" qualifier.

### Issue 2: M12 parenthetical explains a definitional choice and pre-states termination proved later
**ASN-0058, M12 (CanonicalUniqueness)**: "(Condition 2 uses only TumblerAdd, avoiding TumblerSub which is not well-defined for ordinal decrement at arbitrary tumbler depth. Leftward extension terminates because `dom(f)` is finite — the run cannot be extended beyond the leftmost position in `dom(f)`.)"
**Problem**: Two accretion patterns. First, "Condition 2 uses only TumblerAdd, avoiding TumblerSub..." explains *why* the condition is phrased as it is rather than stating what it says — rationale prose attached to a definition. Second, the termination claim duplicates the partition corollary's "Termination" paragraph ("By S8-fin ... `dom(f)` is finite ... each phase terminates after at most `|dom(f)|` steps"), where it is actually proved. The parenthetical pre-states the same fact in different words.
**Required**: Drop the parenthetical. Termination belongs solely in the partition corollary; the TumblerAdd phrasing is self-evident from condition 2 as written.

### Issue 3: Rhetorical essay sentence in the M2 proof slot
**ASN-0058, M2 (DecompositionExistence), end of proof**: "The question that S8 leaves open is: given that at least one decomposition exists, how many are there, and what relates them?"
**Problem**: This is narrative/essay content occupying a proof slot — it advances no step of the M2 argument and merely sets a rhetorical hook for the next definition. The "Problem" section already poses "How do they compose and decompose?"; this restates that motivation mid-proof.
**Required**: Remove the sentence. If a transition to Decomposition Equivalence is wanted, let the Nelson quote ("There may be many representations...") carry it without the rhetorical question.

### Issue 4: Defensive disclaimer in the Span Algebra Analogy remark
**ASN-0058, Remark (Span Algebra Analogy)**: "We treat the connection as an aid to intuition; the block algebra below is developed on its own primitives."
**Problem**: The remark body is a legitimate analogy (allowed), but this closing sentence is a defensive justification of the document's own method — it tells the reader what the authors chose to do rather than stating a fact about the objects. The remark's own content (the analogy is "not an identity") already conveys that the block algebra stands alone.
**Required**: Delete the closing sentence; the analogy is self-evidently intuition once it states where the correspondence is and is not exact.

## OUT_OF_SCOPE

None. The note stays within mapping-block algebra over arrangements; operation effects, link semantics, and version comparison are correctly absent.

Correctness note: I checked the load-bearing proofs — M-int (both bound derivations and the T3 closure), M2's V-extent translation, M7/M7-cov non-overlap, M12a/M12b and the M12 two-inclusion argument, C0's infinite-family contradiction, M16a's prefix-preservation, and C2's three-step cardinality chain. The arguments are case-complete and the boundary cases (`k = 0` via OrdinalShiftBase, `n = 1`, empty arrangement, `j = uₘ` in C2) are handled. No correctness gaps found; the findings are accreted prose only.

VERDICT: REVISE
