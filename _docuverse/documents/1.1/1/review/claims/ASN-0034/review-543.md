# Cone Review — ASN-0034/T4 (cycle 2)

*2026-04-25 16:55*

### T4a sentinels invoke NAT-sub solely for cosmetic reduction
**Class**: OBSERVE
**Foundation**: NAT-sub right-telescoping
**ASN**: T4a setup paragraph: "Set `s₀ = 0` and `s_{k+1} = #t + 1` as sentinels.… NAT-sub's right-telescoping clause `(m + n) − n = m`, instantiated at `m = #t, n = 1`, reduces `s_{k+1} − 1 = (#t + 1) − 1` to `#t`".
**Issue**: The sentinel `s_{k+1} = #t + 1` is introduced only to compute `s_{k+1} − 1 = #t` for the last segment's upper bound, and the proof body itself works directly with `[s_k + 1, #t]` and the native `+1` inequality. The sentinel formalism adds a NAT-sub right-telescoping dependency that the actual proof does not exercise — a reviser-drift pattern where machinery is set up but not load-bearing. The proof would go through identically by describing the last segment as `[s_k + 1, #t]` from the outset, with NAT-sub's conditional-closure used only at `s_i − 1` (as in T4b).

---

### Use-site-inventory meta-prose in T4a's NAT-sub Depends
**Class**: OBSERVE
**Foundation**: n/a (structural slot prose)
**ASN**: T4a Depends, NAT-sub entry: "…the form NAT-discrete outputs directly in the Reverse Last-segment derivation."
**Issue**: The Depends entry's closing dash-clause is editorial commentary justifying *why* NAT-sub is invoked in this form rather than another, with cross-reference to NAT-discrete's output shape. This is structural-slot prose that explains the dependency's framing rather than what NAT-sub supplies. A consumer needs the use-site, not the comparative justification.

---

### Use-site-inventory meta-prose in T4b's NAT-sub Depends
**Class**: OBSERVE
**Foundation**: n/a (structural slot prose)
**ASN**: T4b Depends, NAT-sub entry: "…so no subtractive rewriting to `s_k ≤ #t − 1` is performed, and no further NAT-sub clause (strict-monotonicity Consequence at `p = 1`, right-telescoping) is invoked beyond conditional closure at `s_i − 1`."
**Issue**: Same pattern as T4a — the entry enumerates which NAT-sub clauses are *not* invoked and what subtractive rewrites are *not* performed, rather than stating what the cited clause supplies. This is the "use-site inventory" pattern: scope-of-dependency commentary belongs in review notes, not the formal contract.

---

### Parenthetical reduction commentary in T4's NAT-closure Depends
**Class**: OBSERVE
**Foundation**: n/a (structural slot prose)
**ASN**: T4 Depends, NAT-closure entry: "(the `m = 1` and `m = 2` steps need no such reduction, as `1 + 1 ≤ zeros(t)` and `2 + 1 ≤ zeros(t)` are already the numerals `2 ≤ zeros(t)` and `3 ≤ zeros(t)` by the definitions `2 := 1 + 1` and `3 := 2 + 1`)."
**Issue**: The parenthetical explains *why* certain steps in the Exhaustion derivation don't need NAT-closure's left-identity reduction — meta-prose about the structure of the derivation, embedded in the Depends slot. The entry would be cleaner stating what NAT-closure supplies (left-identity at the m=0 step) without the comparative aside about steps where it isn't needed.

---

### T4 body contains pure forward-reference paragraph for T4a/T4b/T4c
**Class**: OBSERVE
**Foundation**: n/a (internal structure)
**ASN**: T4 body: "Three downstream claims — **T4a (SyntacticEquivalence)**, **T4b (UniqueParse)**, and **T4c (LevelDetermination)** — build on T4 with additional foundations.… the present paragraph is a forward reference, not a restatement."
**Issue**: This paragraph advances no part of T4's reasoning and explicitly disclaims itself as "a forward reference, not a restatement." Forward-reference paragraphs that disclaim their own role are editorial scaffolding that a precise reader has to skip past.

---

### T4c re-derives `0 < 1` via NAT-addcompat instantiation when NAT-closure posits it directly
**Class**: OBSERVE
**Foundation**: NAT-closure (NatArithmeticClosureAndIdentity) — Axiom clause `0 < 1`
**ASN**: T4c Injectivity: "NAT-addcompat's strict successor inequality `n < n + 1`, instantiated at `n ∈ {0, 1, 2}` — the `n = 0` instantiation licensed by `0 ∈ ℕ` from NAT-zero…"
**Issue**: NAT-closure's Axiom slot already includes `0 < 1` directly, so the base link of the chain `0 < 1 < 2 < 3` could be cited from NAT-closure without instantiating NAT-addcompat at `n = 0`. The current path routes through NAT-addcompat at `n = 0`, which is what pulls NAT-zero into Depends (to license `0 ∈ ℕ` for the instantiation). Citing NAT-closure's `0 < 1` directly would shorten the chain and reduce NAT-zero's role to grounding the literal `0` in the label-defining biconditional alone — clearer attribution, fewer indirect citations.

---

### Hierarchical-structure prose carries forward-reference disclaimer
**Class**: OBSERVE
**Foundation**: n/a (presentation)
**ASN**: Hierarchical structure section: "The count of zero-valued components determines the specificity level — for each `k ∈ {0, 1, 2, 3}` … T4c is the single definitional site… The names appear here only as a forward reference to that definition; they are not defined by the present paragraph."
**Issue**: The closing sentence explicitly disclaims that the paragraph is a forward reference rather than a definition — meta-commentary about the paragraph's role rather than content advancing the reasoning. The paragraph could either say "T4c assigns these labels by zero count" without the disclaimer, or be deferred entirely until after T4c is presented.

---

VERDICT: OBSERVE

## Result

Cone review converged.

*Elapsed: 1656s*
