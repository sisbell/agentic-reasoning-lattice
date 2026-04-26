# Cone Review — ASN-0034/T6 (cycle 1)

*2026-04-25 22:27*

Reviewing the ASN as a system for cross-claim consistency, precondition chains, and reviser drift.

### T3 alias mismatch in T6 Depends
**Class**: REVISE
**ASN**: T6's Depends slot cites `T3 (SequenceEqualityIsComponentwise)` and the proof similarly refers to T3 by its componentwise content; but T3's actual section header is `**T3 (CanonicalRepresentation).**`, and T1's Depends slot consistently uses `T3 (CanonicalRepresentation, this ASN)`.
**Issue**: A single claim is being cited under two different canonical names within the same ASN. Downstream consumers building dependency graphs on PascalCase labels will see either a missing `SequenceEqualityIsComponentwise` claim or an unreferenced `CanonicalRepresentation` claim, depending on which way they index.
**What needs resolving**: Reconcile the citation in T6 with T3's declared header, or change T3's header — one canonical PascalCase label per claim, used everywhere.

### Spurious NAT-discrete citation in T6 Ingredient 3
**Class**: REVISE
**ASN**: T6 Ingredient 3: "Decidability of equality on ℕ follows from NAT-order's trichotomy together with NAT-discrete." Depends slot: "NAT-discrete — promotes 'non-zero' to 'strictly positive' at Ingredient 1; forecloses density for Ingredient 3."
**Issue**: NAT-discrete (`m < n ⟹ m + 1 ≤ n`) plays no role in deciding ℕ-equality. Trichotomy alone supplies the three-way disjunction `m < n ∨ m = n ∨ n < m`; deciding `=` reduces to deciding `<`. Discreteness of ℕ is orthogonal — equality is equally decidable on dense orderings (e.g. ℚ). The "forecloses density" framing in the Depends entry is meta-justification that does not match a step in Ingredient 3's argument. Reviser drift adding a citation that no inference consumes.
**What needs resolving**: Either drop the NAT-discrete citation from Ingredient 3 and from the Depends entry's "Ingredient 3" gloss, or exhibit the specific inference step in Ingredient 3 that consumes `m < n ⟹ m + 1 ≤ n`.

### Unused ℕ⁺-promotion machinery in T6 Ingredient 1
**Class**: REVISE
**ASN**: T6 Ingredient 1: "by T0 every component lies in ℕ, and NAT-zero with NAT-discrete (at `m = 0`) promotes non-zero components to ℕ⁺." The corresponding Depends entries: "NAT-zero — lower-bound premise `0 ≤ tᵢ` for Ingredient 1." and "NAT-discrete — promotes 'non-zero' to 'strictly positive' at Ingredient 1".
**Issue**: T6's decision procedures (a)–(d) compare components via equality and compare cardinalities/lengths against fixed numerals. None of them consults whether a component is `≥ 1` versus merely `≠ 0`; the strict positivity of field components is a property already established and exported by T4b's Postconditions, not something T6 must re-establish. Reviser drift: the prose explains a fact about T0/T4b's state of affairs rather than a step the decision procedure performs, and pulls NAT-zero + NAT-discrete into T6's Depends without a use-site.
**What needs resolving**: Either remove the ℕ⁺-promotion sentence and the NAT-zero/NAT-discrete dependencies from Ingredient 1, or identify the decision-procedure step that requires `0 < tᵢ` (as opposed to just `tᵢ ∈ ℕ`).

### T4b-style threshold check ordered after extraction in T6
**Class**: OBSERVE
**ASN**: T6 cases (b)–(d) are written as "Extract `N(a), U(a), N(b), U(b)`. Require `zeros(a) ≥ 1 ∧ zeros(b) ≥ 1`; asymmetric absence returns *no*…"
**Issue**: T4b's `U` is undefined when `zeros(t) = 0`; the procedure as written extracts `U(a)` before checking the precondition that makes `U(a)` denote anything. The intended reading (check thresholds first, then extract on the present branch) is recoverable, but the surface order inverts it. Sound as written under a charitable reading; flagging the presentation, not the logic.

VERDICT: REVISE
