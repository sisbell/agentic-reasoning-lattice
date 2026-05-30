# Review of ASN-0082

This ASN carries the `review-mode.anti-bloat` classifier. The core mathematics — the post-insertion shift (I3 family), the post-contraction shift (D-family), the ordinal-extraction homomorphisms (OrdAddHom, OrdinalExceedsDisplacement), and the two span-width corollaries (I3-S, D-S) — is sound. I checked the boundary cases (insert at start/end/empty; contraction with L=∅, R=∅, full deletion), the bijection/gap-closure arguments, and the depth-1 natural-number identity in D-S; all hold. My findings are accumulated meta-prose, which is what the classifier directs me to surface.

## REVISE

### Issue 1: Contraction wp analysis is largely redundant with the insertion wp, and its trivial conjuncts get expository padding
**ASN-0082, "Weakest-precondition analysis (S8a-post backwards through the shift)"**: "Applying the same wp method as the insertion half (I3-VP above), we analyze the contraction's analogue — S8a-post…"
**Problem**: The insertion section already states it "illustrate[s] the wp method." The contraction wp re-runs the identical method, and because the operation fixes depth and subspace to literals, two of its four conjuncts are tautologies that nonetheless receive sentences of justification:
- Conjunct 1 (`1 > 0`): "Trivially true. The wp confirms that vpos(1, …) cannot fail S8a's componentwise-positivity conjunct at position 1; this discharges against the subspace scoping axiom S = 1, with no further structural assumption needed."
- Conjunct 3 (`2 ≥ 2`): "Discharged by the depth scoping axiom #p = 2, which makes the result depth-2 and satisfies S8a's depth conjunct."

This is essay content around tautologies; the reader skips past it to reach the load-bearing conjuncts 2 and 4.
**Required**: Keep one wp analysis (the insertion illustration is enough to expose the method). For contraction, retain only the non-trivial obligations (`v₂ − c > 0` via R-membership + S8a on p, and the TA2 well-definedness obligation `ord(v) ≥ w_ord`); drop the prose on `1 > 0` and `2 ≥ 2`.

### Issue 2: Defensive parenthetical in D-MIN-post explains a non-issue
**ASN-0082, D-MIN-post proof (L ≠ ∅ case)**: "so min(V_1(d)) ≤ v < p by min's lower-bound property and T1's transitivity (the comparison is between tumblers, not natural numbers, so the transitive step is T1's, not NAT-order's)"
**Problem**: The parenthetical guards against a misreading the claim never invites — every comparison in the surrounding sentence is plainly between tumblers. This is reviser drift: prose defending which transitivity is in play, not advancing the argument.
**Required**: Delete the parenthetical.

### Issue 3: D-SEQ-post carries a dependency-ordering justification
**ASN-0082, D-SEQ-post proof (cardinality chain, final bullet)**: "…so X = {[1, k] : p₂ ≤ k < p₂ + c} has exactly c elements. Both premises hold regardless of whether R is empty, so this does not invoke D-SEP(b)'s R ≠ ∅ guard"
**Problem**: The closing clause justifies that the step does not depend on a downstream guard — a non-circularity/dependency note rather than a step in the count. The flagged pattern: prose explaining why a dependency is or isn't invoked. The `|X| = c` computation stands on its own from pre-state D-SEQ and containment; the guard caveat is noise.
**Required**: End the bullet at "has exactly c elements." Drop the guard-avoidance clause.

### Issue 4: OrdinalDisplacementProjection definition reaches forward to a downstream operation
**ASN-0082, OrdinalDisplacementProjection**: "At the restricted depth m = 2 of the contraction operation, w = [0, c] for positive integer c, and w_ord = [c] with Pos([c])."
**Problem**: A local definition's final sentence specializes itself to the parameters of a downstream consumer ("the contraction operation"). The definition's meaning is the general projection; the depth-2 specialization belongs at the contraction use-site (where `w = [0, c]` is already restated), not inside the definition.
**Required**: State the projection generally; move the depth-2 instance to the contraction section where it is used.

## OUT_OF_SCOPE

### Topic 1: Generalization to ordinal depth > 1
**Why out of scope**: The depth-2 (single-component ordinal) restriction and the TA4/S8a precondition collision at intermediate components are correctly confined and already recorded under Open Questions. This is future-ASN territory, not a defect here.

VERDICT: REVISE
