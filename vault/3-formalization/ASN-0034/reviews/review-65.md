# Cone Review — ASN-0034/D0 (cycle 4)

*2026-04-16 02:29*

I'll work through the ASN systematically, checking cross-property consistency, precondition chains, and formal contract completeness against the actual text.

### T1's formal contract uses unbound variables `m` and `n`
**Foundation**: T1 (LexicographicOrder), body text: "For tumblers `a = a₁. ... .aₘ` and `b = b₁. ... .bₙ`" — introduces `m = #a` and `n = #b`
**ASN**: T1 formal contract, Definition line: "`a < b` iff `∃ k ≥ 1` with `(A i : 1 ≤ i < k : aᵢ = bᵢ)` and either (i) `k ≤ min(m,n) ∧ aₖ < bₖ`, or (ii) `k = m+1 ≤ n`."
**Issue**: The formal contract's definition uses `m` and `n` without binding them. These variables are introduced only in the body narrative ("For tumblers `a = a₁. ... .aₘ` and `b = b₁. ... .bₙ`"), which is separate from the formal contract. A reader of the formal contract alone — or a TLA+ formalizer working from contracts — cannot determine that `m = #a` and `n = #b`. Compare with TumblerAdd's formal contract, which uses the self-contained notation `actionPoint(w) ≤ #a` rather than introducing a separate variable for the length. T1's contract should use `#a` and `#b` directly, as every other formal contract in this ASN does.
**What needs resolving**: T1's formal contract Definition line must either bind `m` and `n` explicitly (e.g., "where `m = #a` and `n = #b`") or replace them with `#a` and `#b` throughout, making the contract self-contained.

---

### ZPD's formal contract references Divergence in postconditions but declares no dependency
**Foundation**: Divergence (Divergence), formal contract: defines `divergence(a, b)` with two cases — (i) component divergence at `k ≤ min(#a, #b)`, (ii) prefix divergence at `min(#a, #b) + 1`
**ASN**: ZPD (ZeroPaddedDivergence), formal contract, Postconditions (Relationship to Divergence): "For `a ≠ w`: in Divergence case (i) — component divergence at `k ≤ min(#a, #w)` — … `zpd(a, w) = divergence(a, w)`; in Divergence case (ii) — one operand is a proper prefix of the other — …"
**Issue**: ZPD's postconditions are stated entirely in terms of Divergence's case structure — they reference "Divergence case (i)" and "Divergence case (ii)" by name, and the postcondition values (`zpd = divergence`, `zpd ≥ divergence`, zpd undefined) are defined relative to Divergence's output. Yet ZPD's formal contract has no Depends line at all. Every other property whose formal contract references another property by name declares it in Depends (T1 declares T3, Divergence declares T3, TumblerAdd declares ActionPoint, etc.). ZPD is the sole exception. A formalizer reading ZPD's contract cannot trace the Divergence references to a dependency, and the postconditions cannot be verified without Divergence's definition in scope.
**What needs resolving**: ZPD's formal contract must include a Depends line declaring Divergence, stating which aspects of Divergence's definition (the two-case structure, the domain restriction `a ≠ b`) the postconditions consume.

---

### TumblerSub narrative's round-trip analysis uses terminology and scope that do not match D0's formal contract
**Foundation**: D0 (DisplacementWellDefined), formal contract: "Preconditions: a ∈ T, b ∈ T, a < b, divergence(a, b) ≤ #a" — one constraint beyond `a < b`. Postconditions include `#a > #b → a ⊕ (b ⊖ a) ≠ b` — a negative boundary, not a positive round-trip.
**ASN**: TumblerSub body text: "The roundtrip `a ⊕ (b ⊖ a) = b` therefore requires two independently necessary constraints: `zpd(b, a) ≤ #a` (ensuring TumblerAdd's precondition) and `#a ≤ #b` (ensuring the result length equals `#b`) — the conjunction established by D0."
**Issue**: Two gaps between TumblerSub's narrative and D0's formal contract. (a) **Terminology mismatch.** The narrative states the first constraint as `zpd(b, a) ≤ #a`; D0's precondition states it as `divergence(a, b) ≤ #a`. These are provably equivalent under D0's hypotheses — D0's proof establishes Divergence case (i) where `zpd(b, a) = divergence(a, b)` — but the equivalence is internal to D0's proof, not exported in any formal contract. A reader matching TumblerSub's narrative against D0's contract finds mismatched terms with no traceable bridge. (b) **Scope misattribution.** The narrative says D0 "establishes" a two-constraint conjunction, but D0's preconditions include only one constraint (`divergence(a, b) ≤ #a`). The second constraint (`#a ≤ #b`) is not a D0 precondition — D0 handles it solely as a negative postcondition (`#a > #b → ≠`), and the positive round-trip identity `a ⊕ (b ⊖ a) = b` under the full conjunction is deferred to D1, which does not exist in this ASN.
**What needs resolving**: (a) TumblerSub's narrative must either use `divergence(a, b) ≤ #a` (matching D0's contract) or explicitly state that `zpd(b, a) = divergence(a, b)` holds under D0's hypotheses, citing the ZPD–Divergence relationship and Divergence symmetry. (b) The attribution must be corrected: D0 establishes one constraint as a precondition and proves the necessity of the other via its negative postcondition, but does not establish the conjunction as a sufficient condition for the round-trip — that is D1's role.
