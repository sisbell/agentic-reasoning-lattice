# Review of ASN-0082

The mathematical content is sound. I checked the load-bearing derivations — OrdinalExceedsDisplacement (TumblerAdd `a⊕w≥w` for the weak half, TA4 for strictness, TA3-strict + T1 for the right-region lift), D-SEP(a) (TA4 at depth 1, vacuous zero-prefix), D-SEP(b)'s D-CTG bracket argument, D-CTG-post's closed-form `{[1,k]:1≤k≤N−c}`, and the D-S(a) regrouping `(s₂+c′)−c=(s₂−c)+c′` discharged via ReverseInverse + NAT-CA + TA4 — and each holds. Boundary cases (L=∅, R=∅, full deletion, insert at start/end/empty) are exercised concretely. The depth-2 contraction restriction and its TA4/S8a collision rationale are honestly flagged. The findings below are anti-bloat, consistent with this note's `review-mode.anti-bloat` classifier.

## REVISE

### Issue 1: Pairwise disjointness enumerated three times
**ASN-0082, I3 "Consistency" paragraph and "Weakest-precondition analysis (I3-S2...)"**: the Consistency paragraph works *Shifted vs left / Shifted vs shifted / Shifted vs cross-subspace / ... / Vacated vs assignment regions*; the I3-S2 lemma then states "The consistency check above establishes pairwise disjointness of the three assignment regions"; then the I3-S2 wp analysis re-derives the identical seven cases (shift∩shift via TS2, shift∩left via TS4, shift∩cross via subspace preservation, ..., shift∩vacate via the exclusion clause).
**Problem**: The same seven-case disjointness argument is carried three times for one operation. The contraction half repeats the pattern: D-DP(a)+D-BJ already establish region disjointness, the S2-post lemma proves functionality from them, and the S2-post wp analysis then re-enumerates six cases. The reader must skip past two redundant passes to confirm nothing new is said.
**Required**: Keep one enumeration. Since the I3-S2 / S2-post lemmas already cite the consistency/D-DP results, either delete the wp re-enumeration or fold the Consistency paragraph's content into the wp pass — not both.

### Issue 2: "Without this clause … underdetermined" defensive justification, duplicated
**ASN-0082, I3 closure prose**: "Without these clauses, the assignment and vacating postconditions constrain only positions that were in dom(M(d)) … leaving dom(M'(d)) underdetermined." **D-DOM**: "Without D-DOM, D-L and D-SHIFT alone would constrain only the surviving L and R positions, leaving dom(M'(d)) ∩ subspace 1 underdetermined; D-DOM closes it from above."
**Problem**: Two instances of the same hypothetical-counterfactual justifying *why* a domain-closure clause exists rather than stating what it asserts. This is the "explains why the clause is needed" pattern.
**Required**: State each closure clause directly. One terse note ("the closure clause pins dom(M'(d)) from above") suffices; drop the parallel "without it, underdetermined" hypotheticals.

### Issue 3: NAT-CA justification carries set-theory gesture and use-site inventory
**ASN-0082, NAT-CA Justification**: "witnessed by the canonical bijections `A ⊎ B ≅ B ⊎ A` and `(A ⊎ B) ⊎ C ≅ A ⊎ (B ⊎ C)` of disjoint unions … so we supply these two carrier facts here, where the span-algebra corollaries I3-S(a) and D-S(a) require reordering scalar ℕ sums."
**Problem**: The bijection clause is an informal appeal that adds no rigor to a stated axiom, and the trailing "where I3-S(a) and D-S(a) require …" is a use-site inventory — both are prose about why/where rather than what the axiom states.
**Required**: State the two equations. Retain only the terse non-derivability note (the NAT-* extraction omits commutativity, which the order-monotone non-commutative model shows is independent); drop the disjoint-union witnesses and the consumer list.

## OUT_OF_SCOPE

### Topic 1: Depth > 1 generalization of contraction
**Why out of scope**: The Open Question already records this; the TA4/S8a collision argument correctly defers it to a future ASN rather than treating it as a gap here.

VERDICT: REVISE
