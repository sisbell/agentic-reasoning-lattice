# Cone Review — ASN-0034/TumblerSub (cycle 1)

*2026-04-25 21:42*

### Reviser drift in NAT-sub: meta-prose defending Consequence-vs-Axiom classification
**Class**: OBSERVE
**Foundation**: n/a (foundation ASN, internal consistency)
**ASN**: NAT-sub body, two paragraphs:

> "Strict monotonicity — `m ≥ p ∧ n ≥ p ∧ m < n ⟹ m − p < n − p` — is exported as a *Consequence:* rather than an additional axiom clause, because its content derives from the right-inverse together with NAT-addcompat's right order compatibility and NAT-order's at-least-one trichotomy with irreflexivity. Retaining it as an axiom clause would launder that derivation through a non-minimal clause, the same concern that kept NAT-order's disjointness form `m < n ⟹ m ≠ n` from being separately exported and left it as a derivable contrapositive..."

> "Strict positivity — `m > n ⟹ m − n ≥ 1` — is exported as a *Consequence:* rather than an additional axiom clause, because its content is not purely subtractive..."

The Formal Contract bullets repeat the defense ("recorded as a Consequence rather than an axiom clause so the derivation is not laundered through a non-minimal clause"; "recorded as a Consequence rather than an axiom clause because its content is not purely subtractive…").

**Issue**: The opening sentence of each consequence-paragraph defends the *spec-design choice* of categorizing strict monotonicity / strict positivity as a Consequence rather than an Axiom. It cross-references an unrelated structural decision in NAT-order ("the same concern that kept NAT-order's disjointness form... from being separately exported"). A reader trying to follow the derivation must skip past these meta-justifications to reach the proof. The pattern matches the named drift class: prose around an axiom slot explaining *why the spec is structured this way* rather than *what the axiom says or how the consequence follows*. The defense is also redundant with the Formal Contract bullets, which restate it.

### Section labeled "Precondition" in TumblerSub actually contains a derived lemma
**Class**: OBSERVE
**Foundation**: n/a
**ASN**: TumblerSub body:
> "**Precondition:** `a ≥ w` (T1). We prove that when `zpd(a, w)` is defined, this entails `aₖ > wₖ` at `k = zpd(a, w)`."

**Issue**: The bold label "Precondition:" announces the precondition `a ≥ w`, but the section's body is not a statement of the precondition — it is a multi-paragraph derivation of a *consequence* of the precondition (`aₖ > wₖ` at the divergence point) used to discharge NAT-sub's `aₖ ≥ wₖ` and to support the Pos derivation later. A reader scanning section labels for "what does this operation require" will read past this hoping for a separate "Lemma" or "Auxiliary" header. The Formal Contract's `Preconditions:` slot already states the precondition cleanly; the body section should be relabelled to reflect that it is a derived support lemma, not a precondition statement.

VERDICT: OBSERVE

## Result

Cone review converged.

*Elapsed: 284s*
