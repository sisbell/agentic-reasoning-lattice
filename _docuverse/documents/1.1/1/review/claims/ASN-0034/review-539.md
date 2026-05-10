# Cone Review — ASN-0034/NAT-addbound (cycle 1)

*2026-04-25 15:49*

### NAT-closure body is meta-prose around axioms rather than reasoning
**Class**: OBSERVE
**Foundation**: N/A (internal — NAT-closure body)
**ASN**: NAT-closure body: "The signature `+ : ℕ × ℕ → ℕ` carries two load-bearing commitments... Totality rules out partial addition and closure rules out sums that escape ℕ. ... The pair `1 ∈ ℕ` and `0 < 1` names a second constant in ℕ and locates it in the strict order."
**Issue**: The Formal Contract for NAT-closure has only Axioms — no Consequences requiring derivation. The body therefore has nothing to prove, but instead describes *why the axioms matter* (defensive justification: "Totality rules out partial addition", "closure rules out sums that escape ℕ"). This is the "new prose around an axiom explains why the axiom is needed rather than what it says" pattern flagged in the review criteria.

### NAT-addcompat body redundantly restates the axioms it lists
**Class**: OBSERVE
**Foundation**: N/A (internal — NAT-addcompat body)
**ASN**: NAT-addcompat body: three bullets `Left order compatibility: ...`, `Right order compatibility: ...`, `Strict successor inequality: ...`, then the Formal Contract repeats the same three statements as Axioms.
**Issue**: NAT-addcompat is purely axiomatic (no Consequences). The body bullets are syntactically identical to the Axiom bullets in the Formal Contract. A precise reader scans the body looking for derivations and finds only restatement; the prose adds no information beyond the contract.

### "Distinctness" parenthetical understates `0 < 1`
**Class**: OBSERVE
**Foundation**: N/A (internal — NAT-closure axiom labeling)
**ASN**: NAT-closure Formal Contract: "`0 < 1` (distinctness of the two named constants)".
**Issue**: The parenthetical labels `0 < 1` as "distinctness", but `0 < 1` asserts a strict-order placement that is strictly stronger than `0 ≠ 1`. Distinctness follows from `0 < 1` (via NAT-order irreflexivity) but the axiom commits to more. The label is loose informal annotation; the formal statement is precise.

VERDICT: OBSERVE

## Result

Cone review converged.

*Elapsed: 156s*
