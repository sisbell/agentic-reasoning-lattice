# Cone Review — ASN-0034/T4b (cycle 1)

*2026-04-17 12:14*

### T4's Axiom omits the separator role-assignment that T4b relies on
**Foundation**: T4 (HierarchicalParsing) — Formal Contract Axiom
**ASN**: T4b (UniqueParse) proof — "We claim that a position `i` satisfies `tᵢ = 0` if and only if `i` is a field separator. The forward direction holds by construction: every separator has value 0 in the T4 address format `N₁. ... .Nₐ . 0 . U₁. ... .Uᵦ . 0 . D₁. ... .Dᵧ . 0 . E₁. ... .Eδ`. ... T4 assigns zero-valued positions the role of separators, so if `tᵢ = 0` then `i` is a separator position".
**Issue**: T4b's uniqueness argument requires a biconditional identification of zero-valued positions with separator positions. This biconditional is only asserted in T4's body prose ("Define a *field separator* as a component with value zero"; "An address tumbler has the form `N₁. ... .Nₐ . 0 . U₁. ... .Uᵦ . 0 . D₁. ... .Dᵧ . 0 . E₁. ... .Eδ`"). T4's Formal Contract Axiom states only positional conditions on zero-valued indices (`zeros(t) ≤ 3`, the field-segment constraint); it does not assert that zeros play the separator role or that the field format has exactly this shape. Downstream properties citing T4 axiomatically therefore cannot license the role-assignment that T4b's separator-recovery step uses.
**What needs resolving**: Either promote the separator role-assignment and address-format skeleton from T4's body prose into T4's Formal Contract Axiom (so T4b's citation of T4 for "zero-valued positions are exactly separator positions" has a formal source), or derive the role-assignment from the existing positional axiom plus some explicit definitional clause that T4b can cite in place of the prose.

### Notation ℕ⁺ used in T4b's signature without definition
**Foundation**: T0 (CarrierSetDefinition) — defines components as `aᵢ ∈ ℕ` but never introduces ℕ⁺.
**ASN**: T4b (UniqueParse) — "`fields : T ⇀ Seq(ℕ⁺) × Seq(ℕ⁺) × Seq(ℕ⁺) × Seq(ℕ⁺)`"; and "Each projection returns a finite sequence of *strictly positive* natural numbers: T0's carrier ℕ makes every non-zero component positive".
**Issue**: ℕ⁺ appears in T4b's type signature (four times) as if it were a known object, but it is not defined in T0 or anywhere upstream. T4b's prose glosses it as "strictly positive natural numbers" and attributes the exclusion of zero to T0, but the symbol itself is introduced for the first time in a postcondition type signature. A reader cannot cite T4b's signature formally without an upstream definition of ℕ⁺.
**What needs resolving**: Either define ℕ⁺ (e.g., as `{n ∈ ℕ : n > 0}`) at the point where it is first used, or add it to T0's notation and make the carrier/subcarrier distinction explicit so T4b's signature is grounded.

## Result

Cone converged after 2 cycles.

*Elapsed: 739s*
