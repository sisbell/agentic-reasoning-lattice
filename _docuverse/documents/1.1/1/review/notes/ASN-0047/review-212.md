# Review of ASN-0047

## REVISE

### Issue 1: C-fin load-bearing rationale duplicated near-verbatim across three slots

**ASN-0047, Class (a) verification matrix / "C-fin — load-bearing note" / "Inherited from foundation" table**: The same load-bearing justification appears three times. The matrix cell states "extends dom(C) by one (finite + 1 = finite)." The standalone note then states: "C-fin is load-bearing for K.α's subsequent-emission case formula `a = inc(max{a' ∈ dom(C) : origin(a') = d}, 0)` — the indexed set ... is a subset of the finite `dom(C)`, so `max` is well-defined whenever the set is non-empty." The inherited-foundation table entry then restates this *verbatim*: "Load-bearing for K.α's subsequent-emission case formula `a = inc(max{a' ∈ dom(C) : origin(a') = d}, 0)` — the indexed set is a subset of the finite `dom(C)`, so `max` is well-defined whenever non-empty."

**Problem**: This is the anti-bloat note's "two paragraphs in the same document say the same thing in different words" pattern — here, in the same words. The standalone note and the inherited-table entry are duplicates; a reader who reads both gains nothing from the second.

**Required**: State the `max`-well-definedness rationale once (the inherited-table entry, since C-fin is foundation-inherited, is the natural home) and remove the standalone "load-bearing note" paragraph, or reduce it to a pointer.

### Issue 2: K.δ k=0 precondition names a "maximality clause" that is not distinctly present

**ASN-0047, FrontierEquivalence box and K.δ Case (ii) k=0**: The K.δ k=0 precondition is stated as exactly `t ∈ E ∧ ¬IsNode(t) ∧ inc(t, 0) ∉ E`, with the third conjunct annotated "(the operational frontier check)." Yet FrontierEquivalence's box refers to "the frontier conjunct on `t` (the maximality clause in K.δ k = 0's precondition)," and the k=0 discharge prose speaks of "the frontier conjunct on `t` (the maximality clause in K.δ k = 0's precondition)" as though a maximality clause sits in the precondition alongside the guard.

**Problem**: No separately-written maximality clause exists in the precondition — there is only the guard `inc(t, 0) ∉ E`. A precise reader looking for the named "maximality clause" / "frontier conjunct" finds only the guard, and must reconstruct that "maximality clause" *is* the guard read through FrontierEquivalence. The interchangeability is genuinely proved, but the prose names a precondition element that is not literally there.

**Required**: Either (a) make explicit that the guard `inc(t, 0) ∉ E` *is* the frontier/maximality conjunct (one phrase: "the guard `inc(t,0) ∉ E`, equivalently the frontier-maximality condition on `t` by FrontierEquivalence"), or (b) drop the "(the maximality clause in K.δ k = 0's precondition)" parenthetical and refer only to the guard. Apply consistently at every cite (J4, S7d, worked-example Step 4).

## OUT_OF_SCOPE

None.

VERDICT: REVISE
