# Regional Review — ASN-0034/Span (cycle 2)

*2026-04-23 02:58*

### Defensive type-checking prose at end of T0
**Class**: OBSERVE
**Foundation**: (none)
**ASN**: T0: "The inequality `1 ≤ #a` is thus well-typed within ℕ, and with it the index domain `{1, …, #a}` is never empty, so bounded quantifiers of the form `(Q i : 1 ≤ i ≤ #a : …)` range over a nonempty set rather than collapsing to vacuity."
**Issue**: This closing sentence is meta-prose that justifies why the axiom is well-formed — explaining why `≤` is typed and why the quantifier range is nonempty — rather than stating content. Readers must parse it and then discard it; nothing downstream cites it. Matches the "new prose around an axiom explains why the axiom is needed rather than what it says" drift pattern.

### Meta-prose about quantifier typing in TA-Pos
**Class**: OBSERVE
**Foundation**: (none)
**ASN**: TA-Pos: "The bound variable `i` is typed to ℕ because the projection `tᵢ` is defined by T0 only on the index domain `{1, …, #t} ⊆ ℕ` and the bounding relation `≤` is ℕ-typed; the explicit `i ∈ ℕ` keeps parity with the `(A n ∈ ℕ :: …)` form used by the sibling NAT axioms."
**Issue**: Justifies a stylistic choice (why `i` is annotated `∈ ℕ`) rather than advancing the definition. The full sentence that follows ("`tᵢ` itself is a natural number by T0's carrier, the literal `0` against which it is compared is the `0 ∈ ℕ` posited by NAT-zero…") continues the same typing-audit mode: each symbol is accounted for in turn. These annotations belong in a dependency table, not in the claim body, and they make the reader work to reach the actual content (complementarity, partition).

### Defensive closing in TA-Pos notation note
**Class**: OBSERVE
**Foundation**: (none)
**ASN**: TA-Pos note on notation: "The lexicographic ordering and its prefix rule alluded to here are supplied by claims outside this region and enter no obligation of TA-Pos."
**Issue**: Pre-empts an objection that was not raised — a defensive disclaimer about obligations. The preceding example (`0 < 0.0` even though `Zero(0.0)`) is useful orientation; the obligation-disclaimer is not. If the lexicographic ordering is forward-referenced, a brief pointer suffices.

### Case-analysis closing in ActionPoint uniqueness
**Class**: OBSERVE
**Foundation**: (none)
**ASN**: ActionPoint derivation: "The case `m₁ = m₂` with `m₂ < m₁` is handled analogously: substituting `m₁` for `m₂` in `m₂ < m₁` gives `m₁ < m₁`, contradicting irreflexivity. The remaining pairing `m₁ = m₂` with `m₂ = m₁` asserts the equality directly."
**Issue**: The pairing `m₁ = m₂` ∧ `m₂ = m₁` is not a distinct case — it is the same equality stated twice. Listing it as the "remaining pairing" is an artifact of mechanically enumerating the four disjunct pairings of `(m₁<m₂ ∨ m₁=m₂) ∧ (m₂<m₁ ∨ m₂=m₁)` rather than reducing the argument. The uniqueness proof would be cleaner as: from `m₁ ≤ m₂` and `m₂ ≤ m₁`, expand both; if either strict inequality holds, transitivity with the other (non-strict) bound yields `m₁ < m₁`; otherwise both are equalities and `m₁ = m₂`.

### Elaborate derivation of `1 ≤ w_{actionPoint(w)}` from membership
**Class**: OBSERVE
**Foundation**: (none)
**ASN**: ActionPoint derivation: "For 1 ≤ w_{actionPoint(w)}: membership of actionPoint(w) in S gives w_{actionPoint(w)} ≠ 0. Instantiating NAT-zero's disjunction axiom … yields 0 < w_{actionPoint(w)} ∨ 0 = w_{actionPoint(w)}, and w_{actionPoint(w)} ≠ 0 excludes the equality, leaving 0 < w_{actionPoint(w)}. NAT-discrete's forward direction … yields 0 + 1 ≤ w_{actionPoint(w)}. NAT-closure posits 1 ∈ ℕ directly, licensing its additive identity … this gives the equality 0 + 1 = 1, and rewriting 0 + 1 ≤ w_{actionPoint(w)} by it yields 1 ≤ w_{actionPoint(w)}."
**Issue**: A chain of four axioms (NAT-zero, NAT-discrete, NAT-closure's additive identity, plus rewriting) to derive "positive nat ≥ 1" from `w_{actionPoint(w)} ≠ 0`. The derivation is correct but its density obscures what ActionPoint is actually establishing. This is the kind of audit-trail prose that accumulates across revise cycles — each axiom named to satisfy a per-step dependency check — and it leaves the reader tracking symbol bookkeeping instead of the claim. A shorter route: `0 < w_{actionPoint(w)}` from NAT-zero, plus a NAT-discrete step, suffices.

VERDICT: REVISE

(Rationale: new findings are OBSERVE-only, but the prior-findings REVISE — T3 cited without definition — remains unresolved in the ASN content.)

## Result

Regional review not converged after 2 cycles.

*Elapsed: 1401s*
