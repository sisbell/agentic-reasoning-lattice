# Review of ASN-0086

## REVISE

### Issue 1: wp Case 2 restates the "K is not a wp conjunct" argument twice in full

**ASN-0086, Weakest-Precondition Analysis, Case 2 ("Result" and "Derivation (both directions)")**:

- Result: "The index membership K ∈ T_admissible is not a wp conjunct: by the Definition of Emit_K, K is a type-index that selects which operation is named — there is no operation Emit_∅ — so K ∈ T_admissible is presupposed in naming Emit_K, before any pre-state Σ is examined."
- Derivation: "The index membership K ∈ T_admissible is not a wp conjunct but a standing condition on which operation is named — there is no Emit_∅ (a K = ∅ would not be an admissible type...), so it is presupposed before any pre-state is examined rather than a predicate the wp ranges over."

**Problem**: These two paragraphs make the identical claim with identical reasoning ("no Emit_∅", "presupposed before the pre-state is examined"). This is the anti-bloat "two paragraphs in the same document say the same thing in different words" pattern. The active `review-mode.anti-bloat` classifier flags this at source. Compounding it, the defensive parenthetical "(with the index K ∈ T_admissible presupposed)" is then repeated a third, fourth, and fifth time across the load-bearingness paragraph, the "Substrate-conformance alone is insufficient" paragraph, and the "discipline alone is insufficient" paragraph.

**Required**: State the K-as-index point once (it belongs with the Result statement of the formula), and drop the recurring parenthetical from the three counterexample paragraphs — the standing condition does not need re-asserting at every witness.

## OUT_OF_SCOPE

### Topic 1: wp Case 1 supplies a sufficient, not weakest, precondition

Case 1 explicitly delivers `P0 ∧ P1 ∧ PC` as a *sufficient* precondition and openly notes PC (global conformance) is stronger than the local postcondition requires, without computing the genuine weakest (the local antichair condition around `a`). The mandatory bar — at least one non-trivial genuine wp — is met by Case 2, and Case 1's status is transparently labeled, so this is a deliberate scope choice rather than an error. Computing the true weakest precondition for single-tuple scope is a refinement for a later pass, not a defect in this note.

### Topic 2: cardinality/atomicity guarantees raised in Open Questions

The bounds on `|nullified(Σ)|`, Observe ordering, and Emit/Observe atomicity under concurrency are correctly deferred — they are new substrate guarantees, not gaps in the present relational-vocabulary layer.

Notes on what was checked and found sound: R0's two-branch freshness and the per-address L1c chain reconstruction (correctly using only `a` and `d`, never store-wide contiguity); R0a's split into a zero-counting cross-home case and a uniform-length same-home case; L-ContiguousPrefix's inductive extension via clauses (b)/(c) with the EmptyInitialLinkStore base; R7a's interleaved K.σ/K.λ replay (no K.α introduced, frontier-landing pins each `a_k`); and the worked sketch's concrete tumblers (`a₁=1.0.1.0.1.0.2.1` through `b₂=...0.2.4`) verify against (UL)/(UZ), R6a/R6b/R6c, and the audit-vs-active distinction. The `state-local-conforming` vs `substrate-conforming` separation is load-bearing and the `#E ≥ 2` (state-local) vs `#E = 2` (substrate, Cor1) distinction is handled correctly. No correctness flaw found; the ASN defines state (typed relations, active subset), operations, and invariants abstractly — no META.

VERDICT: REVISE
