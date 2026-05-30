# Review of ASN-0082

This ASN is mathematically thorough — I checked the displacement arithmetic (OrdAddHom, OrdinalExceedsDisplacement, D-SEP, D-S), the wp derivations, the foundation citations, and the boundary cases (L=∅, R=∅, full deletion, cross-subspace), and the technical core holds up. The cited lemmas (TA4, TA2, TA3-strict, ReverseInverse, TS1–TS4, OrdShiftHom) are applied with their preconditions discharged, and the X-reappears-in-Q₃ correction (D-DOM replacing the old D-X) is handled correctly. The ASN carries the `review-mode.anti-bloat` classifier, and the surviving issues are accretion, not correctness.

## REVISE

### Issue 1: Forward-reference essay in the insertion Scope paragraph
**ASN-0082, Post-Insertion Shift / Scope**: "A composing INSERT operation will weaken I3-C to S0 (`dom(C) ⊆ dom(C') ∧ ...`) to permit n new I-addresses, and the composition's combined postcondition will be S0-compatible."
**Problem**: This describes the internal mechanics of a future, unwritten INSERT ASN — how it will rewrite I3-C — rather than advancing any claim in *this* ASN. It is forward-reference accretion: the reader must process speculation about downstream composition that has no bearing on the shift sub-operation being specified.
**Required**: Cut to a single scope sentence — this note characterizes the arrangement-only shift sub-operation; content placement and the dom(C) extension are future work. Drop the prediction about how I3-C will be weakened.

### Issue 2: I3-C rationale restated three times
**ASN-0082, Post-Insertion Shift**: the "shift stores no new content, so dom(C') = dom(C)" rationale appears in (a) the I3-C frame clause itself ("the shift stores no new content, so the reverse inclusion holds"), (b) the prose paragraph after the postconditions ("The content-store frame (I3-C) makes explicit that the shift is arrangement-only: S0... since the shift stores no new content — it is purely an arrangement operation — the reverse inclusion holds and dom(C') = dom(C)"), and (c) the Consistency paragraph ("I3-C constrains C' independently of M'(d) — the content store is unchanged regardless of arrangement modifications").
**Problem**: Two paragraphs (plus the clause) say the same thing in different words. Flagged pattern: "two paragraphs in the same document say the same thing."
**Required**: State the rationale once (in the I3-C clause). The follow-on prose and the Consistency restatement should reference it, not re-derive it.

### Issue 3: "Avoid ℕ-level reasoning" methodology aside restated across proofs
**ASN-0082, OrdinalExceedsDisplacement / D-SEP / wp analyses**: "We prove the dominance of an ordinal over the displacement entirely from tumbler arithmetic... rather than from any natural-number left-summand dominance, which the foundation's NAT-* axioms do not supply." Echoed at D-SEP(a) ("TA4 fires, giving ord(r) ⊖ w_ord = ord(p) directly, with no ℕ-level subtraction"), and at the S8a-post wp ("discharges this without any natural-number left-summand dominance"), and again in D-S(a).
**Problem**: This is methodology meta-prose — explaining *why* the proof routes through TA4/TA2 instead of ℕ subtraction — repeated at each use site. The first statement carries information (the foundation lacks the ℕ axiom); the repetitions are noise the reader steps around. Flagged pattern: "explains why a technique is used rather than advancing the argument."
**Required**: Keep one statement of the constraint (e.g., where NAT-CA is introduced, noting NAT-* omits left-summand dominance). The individual derivations stand on their cited lemmas without the recurring aside.

### Issue 4: Cross-subspace / cross-document frame boilerplate hoisted per lemma
**ASN-0082, post-state preservation lemmas**: nearly every post-lemma (S8-depth-post, S8a-post, D-CTG-post, D-MIN-post, D-SEQ-post, S8-fin-post, S2-post, S3-post) closes with a near-verbatim "By D-CS, other subspaces are unchanged. By D-CD, other documents are unchanged," and the contiguity triple additionally repeats "non-text subspaces: D-CS preserves V_S(d) (S ≠ 1) verbatim; the foundation imposes no D-X obligation there."
**Problem**: The off-subspace/off-document obligation is real, but its discharge is identical in every lemma; repeating it ~8 times is mechanical. Flagged pattern: "multiple paragraphs in different sections defer to the same downstream location."
**Required**: Hoist a single section-level statement — all post-lemmas below dispatch off-subspace obligations to D-CS and off-document obligations to D-CD — and let each lemma carry only its subspace-S argument. (Weakest of the four; if per-lemma self-containment is a deliberate convention, state that convention once instead.)

## OUT_OF_SCOPE

The two Open Questions (depth > 1 generalization of D-SEP/D-DP, and external-state reference updates after a shift) are correctly placed as future territory, not defects in this ASN. No additional out-of-scope items.

VERDICT: REVISE
