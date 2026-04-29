# Cone Review — ASN-0034/T4c (cycle 1)

*2026-04-25 17:48*

I'll review this foundation ASN for internal consistency, focusing on definitional uniformity, precondition chains across the dependency lattice (NAT-* and T4 family), and proof completeness.

### Defensive justifications of slot choice (Consequence vs Axiom)
**Class**: OBSERVE
**Foundation**: NAT-sub, T4a
**ASN**: NAT-sub Formal Contract — "Strict monotonicity ... is exported as a *Consequence:* rather than an additional axiom clause, because its content derives from..." and "Strict positivity ... is exported as a *Consequence:* rather than an additional axiom clause, because..." Also NAT-sub body: "Retaining it as an axiom clause would launder that derivation through a non-minimal clause, the same concern that kept NAT-order's disjointness form..." T4a: "recorded as a Consequence rather than an Axiom because the biconditional is proved from T4's axioms and the foundation dependencies, not posited."
**Issue**: These passages explain *why* a fact is in the Consequence slot rather than what the fact says. The reader does not need to be told the editorial policy that consequences are derived rather than posited; the slot label already conveys this. The cross-reference to NAT-order's disjointness rationale extends the policy commentary further. This is meta-prose around the structural slots that the precise reader must skip past.

### Use-site inventory in NAT-sub axiom body
**Class**: OBSERVE
**Foundation**: NAT-sub
**ASN**: NAT-sub body — "The axiom body invokes symbols beyond ℕ's primitive membership. The strict order `<` together with its non-strict companion `≤` and reverse companions `≥`, `>` ... appear in the signature's domain condition `{(m, n) ∈ ℕ × ℕ : m ≥ n}` and in the antecedents `m ≥ n` of the conditional-closure and inverse-characterisation clauses. The binary addition `+` ... appears in the sums `(m − n) + n`, `n + (m − n)`, `m + n`, and `n + m`. NAT-addbound's right-dominance clause ... discharges the conditional-closure precondition implicit in the unguarded equation..."
**Issue**: This paragraph enumerates which dependency supplies which symbol at which use-site, duplicating information already present in the Depends slot. It is the use-site inventory the review guidance flags as noise. The conditional-closure preconditions for the unguarded telescoping clauses are a real concern, but they belong as one-line observations in the Depends entries (which they already are), not as an independent prose paragraph.

### Arithmetic-grounding preludes in T4a and T4b
**Class**: OBSERVE
**Foundation**: T4a, T4b
**ASN**: T4a — "The arithmetic in what follows — the numerals `2` and `3`, the sums `s_i + 1`, `s_i + 2`, and `#t + 1`, and the last-segment upper bound `s_{k+1} − 1` — is grounded thus: NAT-closure posits `1 ∈ ℕ` and closes ℕ under addition, so `2 := 1 + 1 ∈ ℕ`..." T4b — "The arithmetic in what follows — the numeral `2`, sums `s_i + 1` and `s_i + 2`, and the partial subtraction `s_i − 1` — is grounded thus..."
**Issue**: These paragraphs preview every numeral and sum that will appear, then justify each one's ℕ-membership in advance. Once the Depends slot lists NAT-closure and NAT-sub with their roles, the inline citations at use-site would suffice. The prelude form does not advance the proof; it inventories citations.

### Forward-reference paragraph in T4b for `t.X₁`
**Class**: OBSERVE
**Foundation**: T4b
**ASN**: T4b — "To access individual components of a field we introduce the notation `t.X₁`, grounded in T0's projection as follows. Whenever `X(t)` is defined, `X(t)` is a nonempty finite sequence over `ℕ⁺ ⊆ ℕ`, so `X(t) ∈ T` with `#(X(t)) ≥ 1` by T0, and T0's component projection `·ᵢ` is defined at every `i ∈ {1, …, #(X(t))}` — in particular at `i = 1`. We set `t.X₁ := (X(t))₁`..."
**Issue**: The notation `t.X₁ := (X(t))₁` is a one-line abbreviation of T0 subscript composed with `X`. The grounding paragraph re-establishes facts (X(t) ∈ T, T0 supplies subscript) that follow immediately from the projections having been declared as `T ⇀ T`. The same content recurs in the Postconditions slot. One occurrence — in Postconditions, where t.X₁'s domain pattern is recorded — is sufficient.

VERDICT: OBSERVE

## Result

Cone review converged.

*Elapsed: 898s*
