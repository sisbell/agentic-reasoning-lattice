# Regional Review — ASN-0034/OrdinalShift (cycle 1)

*2026-04-23 02:35*

### Meta-prose in NAT-closure and NAT-order axiom slots
**Class**: OBSERVE
**Foundation**: (internal)
**ASN**: NAT-closure: "The axiom slot introduces `+` before constraining it: its first clause `+ : ℕ × ℕ → ℕ` posits the signature — fixing arity (binary) and codomain (ℕ). The operation is posited directly on ℕ rather than derived from an earlier axiom — the same register NAT-order uses to posit `<`". NAT-order: "The axiom slot introduces `<` before constraining it… NAT-closure follows the same register for the arithmetic primitive, opening its axiom slot with the signature `+ : ℕ × ℕ → ℕ` before the unit-membership and left-identity clauses."
**Issue**: Both axioms carry cross-referencing prose explaining *why* the axiom is structured the way it is (same register, signature-before-constraint). This is reviser drift of the "explains why the axiom is needed rather than what it says" kind — it reasons about the shape of the axiom slot rather than advancing the mathematical content. The useful content (signature on first line, then clauses) already communicates itself to the precise reader.

### NAT-closure's "mirrored clause not axiomatized" note
**Class**: OBSERVE
**Foundation**: (internal)
**ASN**: NAT-closure: "The mirrored clause `n + 0 = n` is not axiomatized here; commutativity of `+` is not enumerated, so the right-identity form is not derivable from this axiom alone."
**Issue**: Defensive prose stating what the axiom does *not* contain. A downstream consumer who needs `n + 0 = n` will discover the absence from the axiom text itself; flagging non-coverage inside the axiom's own narrative is noise. If this is a guardrail against a past mistake, a why-line would make that explicit rather than framing it as absence-for-absence's-sake.

### OrdinalDisplacement promotion routes through NAT-addcompat unnecessarily
**Class**: OBSERVE
**Foundation**: (internal)
**ASN**: OrdinalDisplacement derivation: "Promote `n ≥ 1` to `n ≠ 0`: NAT-addcompat's `(A n ∈ ℕ :: n < n + 1)` at n = 0 gives `0 < 0 + 1`. NAT-closure posits `1 ∈ ℕ` directly, licensing its additive identity … this gives the equality `0 + 1 = 1`, and rewriting `0 < 0 + 1` by it yields `0 < 1`. NAT-order's `m ≤ n ⟺ m < n ∨ m = n` unfolds `n ≥ 1`…"
**Issue**: The same rewrite `0 + 1 = 1` and anchor `0 < 1` is then replayed *verbatim* inside ActionPoint's derivation for `1 ≤ w_{actionPoint(w)}`. Two foundation claims duplicate a five-step promotion chain instead of exporting it once. Also: NAT-order's disjointness axiom `m < n ⟹ m ≠ n` would collapse the final three steps (from `0 < n` to `n ≠ 0`) into one citation, eliminating the appeal to irreflexivity-by-substitution that the current proof uses but does not walk. Not a correctness error — just duplicated scaffolding that both claims carry.

### TA0's gloss on TA-Pos blurs the predicate/existence distinction
**Class**: OBSERVE
**Foundation**: (internal)
**ASN**: TA0 Depends: "TA-Pos (PositiveTumbler, this ASN) — precondition `Pos(w)` ensures the action point exists."
**Issue**: TA-Pos *defines* the predicate `Pos(·)`; it is ActionPoint's derivation (using NAT-wellorder on the nonempty set S) that yields existence of the action point. The gloss attributes existence to TA-Pos. The depends list already cites ActionPoint separately for exactly that role, so the overlap is harmless — but a reader tracing "who supplies what" sees two claims both credited with existence.

VERDICT: OBSERVE

## Result

Regional review converged after 1 cycles.

*Elapsed: 234s*
