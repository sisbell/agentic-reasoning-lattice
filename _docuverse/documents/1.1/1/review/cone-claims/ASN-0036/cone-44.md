Reading the five claims as a system before looking for gaps between them.

**AX-1, AX-2, S0** are axioms; no proof obligations. Their statements are clean and their Formal Contracts correctly self-describe as posits. S0's contract references S5 grounding — the previously declined finding establishes S5 exists elsewhere in the ASN; no issue.

**S1 proof.** Single step: S0 gives `a ∈ dom(Σ'.C)` as first conjunct of its consequent; universalise over `a`. Sound. Formal Contract accurately limits Depends to S0; GlobalUniqueness correctly annotated as a non-proof Forward Reference.

**S3 proof.** Base case: AX-1 empties the quantifier range at Σ₀; vacuously true. Inductive step: case split on Inherited vs. New-or-redirected is exhaustive (the two cases are logical complements, given the outer guard `v ∈ dom(Σ'.M(d))`; partial-function applications in the second disjunct are guarded by `v ∈ dom(Σ.M(d))` in both AX-2 and the proof). Inherited case: IH range met → J0 gives `a ∈ dom(Σ.C)` → S1 lifts to Σ'. New-or-redirected case: range exactly matches AX-2's quantifier → conclusion is immediate. Both cases covered; both subclaim applications are valid. Formal Contract's Preconditions and Depends correctly name AX-1, AX-2, S1 (all used; nothing unused cited; S0 is a transitive precondition through S1, not direct, and the direct-dependency convention is applied consistently).

Cross-claim consistency: the range AX-2 constrains maps precisely onto Case 2 of S3's inductive step; nothing in S1 is asked to do what AX-2 must supply. The three-axiom join structure (AX-1 for base, S1 for inherited case, AX-2 for new/redirected case) is clean and non-redundant.

One prose issue:

### Reviser-drift phrase in S3's proof body
**Class**: OBSERVE
**Foundation**: N/A
**ASN**: S3 (ReferentialIntegrity), proof body — "The earlier reading, that S1 alone forces `a ∈ dom(Σ'.C)` for any mapping established by a transition, conflated these: it assumed precisely the new-reference half that AX-2, not S1, supplies."
**Issue**: "The earlier reading" references a prior misunderstanding that is invisible to a reader without review history. The surrounding paragraph — explaining why AX-2 is needed, not what it says — is the reviser-drift pattern the guidelines name explicitly. The logical content (why S1 can't cover the new-mapping case) is sound and worth keeping; the historical reference to a superseded reading is not specification content.
**What needs resolving**: Remove or rephrase "The earlier reading, that S1 alone forces…conflated these" — the logical point it makes (S1 covers inherited references; AX-2 covers new ones; neither substitutes for the other) can be stated directly without invoking a prior incorrect view.

VERDICT: OBSERVE