# Cone Review — ASN-0036/D-MIN (cycle 1)

*2026-04-15 08:25*

Now I have the full picture. Let me compile my review based on the provided ASN content and the files.

---

# Cone Review — ASN-0036/D-CTG (cycle 2)

*2026-04-15*

### V_S(d) preconditions attribute `v > 0` to S8a, but S8a's formal contract does not export it

**Foundation**: S8a (VPositionWellFormedness) — axiom: `(A d ∈ D, v : v ∈ dom(Σ.M(d)) : zeros(v) = 0 ∧ v₁ ≥ 1)`; postconditions: `zeros(v) = 0` (equivalently, every component strictly positive), `v₁ ≥ 1`
**ASN**: V_S(d) (SubspaceVPositionSet) — body text: "Every element of V_S(d) satisfies S8a (V-position well-formedness): zeros(v) = 0, v₁ ≥ 1, v > 0." Formal preconditions: "S8a — every v ∈ dom(Σ.M(d)) satisfies zeros(v) = 0 ∧ v₁ ≥ 1 ∧ v > 0"
**Issue**: S8a's formal contract exports two conjuncts: `zeros(v) = 0` and `v₁ ≥ 1`. V_S(d) attributes a third conjunct `v > 0` to S8a — in both body text and formal preconditions — that appears nowhere in S8a's axiom, postconditions, or body text. The notation `v > 0` is also ambiguous in this context: it could denote the lexicographic comparison `v > [0]` (under T1), which follows from `v₁ ≥ 1` since the first-component comparison resolves it; or it could denote componentwise positivity (every component exceeds zero), which restates `zeros(v) = 0` for natural-number components. Either reading is derivable from S8a's two stated conjuncts, but S8a exports neither — V_S(d) introduces a notation that its cited source does not use, then presents it as provided by that source. No downstream property currently consumes the `v > 0` conjunct (D-CTG cites V_S(d) for set inclusion only; D-MIN cites S8a directly for positivity), so the overclaim is not load-bearing at present. But the precondition chain from V_S(d) to S8a is formally broken for this conjunct: a reader or formalizer tracing `v > 0` back to S8a will not find it.
**What needs resolving**: Either remove `v > 0` from V_S(d)'s S8a attribution (it's redundant with `zeros(v) = 0` or `v₁ ≥ 1` under either interpretation), or — if the notation serves a downstream purpose not yet apparent — add it to S8a's postconditions with an explicit definition of what `> 0` means for tumblers. The choice of reading (lexicographic vs. componentwise) should be stated, not left to the reader.
