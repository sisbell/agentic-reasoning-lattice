# Cone Review — ASN-0034/T4b (cycle 2)

*2026-04-25 20:05*

### T4 Exhaustion Consequence quantifier mismatched against T4a use-site
**Class**: REVISE
**Foundation**: n/a (internal)
**ASN**: T4 (HierarchicalParsing). T4's *Consequence:* slot states "`zeros(t) ∈ {0, 1, 2, 3}` for every T4-valid tumbler `t`". T4a's *Preconditions:* slot states "`t ∈ T` with `zeros(t) ≤ 3`. The field-segment constraint of full T4-validity is *not* assumed". T4a's setup then writes: "T4's Exhaustion Consequence — whose derivation uses only the bound `zeros(t) ≤ 3` together with NAT-zero's `0 ≤ zeros(t)`, NAT-order's trichotomy, and NAT-discrete, and thus applies under T4a's precondition without invoking the field-segment constraint — pins `k ∈ {0, 1, 2, 3}`."
**Issue**: T4a is not citing T4's Consequence as stated; it is appealing to the derivation behind that Consequence under a strictly weaker hypothesis. As written, T4 Exhaustion is universally quantified over T4-valid tumblers, but T4a's `t` need not be T4-valid (only `zeros(t) ≤ 3`). The text papers over the gap by re-examining what the derivation uses. A precise reader should be able to instantiate a cited Consequence at the use-site hypothesis — not have to verify "the derivation would still go through under the weaker assumption." T4b inherits this concern when invoking the same Consequence transitively through T4 in its Depends.
**What needs resolving**: Either restate T4's Exhaustion Consequence with the weaker hypothesis it actually requires (e.g., `(A t ∈ T : zeros(t) ≤ 3 : zeros(t) ∈ {0, 1, 2, 3})`), so T4a and T4b can cite it directly at their use-sites; or factor Exhaustion into T4 with the strong quantifier and a separately exported "Exhaustion-under-bound" derivative whose quantifier matches the consumer use-site. The aim is a contract whose stated quantifier holds at the use-site without a meta-argument about which steps of the derivation are needed.

### T4a setup arithmetic groundings duplicated at consumer sites
**Class**: OBSERVE
**Foundation**: n/a (internal)
**ASN**: T4a setup paragraph: "The arithmetic in what follows — the numerals `2` and `3`, the sums `s_i + 1`, `s_i + 2`, and `#t + 1`, and the last-segment upper bound `s_{k+1} − 1` — is grounded thus: NAT-closure posits `1 ∈ ℕ`...". T4b's derivation paragraph repeats nearly verbatim: "The arithmetic in what follows — the numeral `2`, sums `s_i + 1` and `s_i + 2`, and the partial subtraction `s_i − 1` — is grounded thus: NAT-closure posits `1 ∈ ℕ`...".
**Issue**: Two adjacent claim sections each open with a sentence-long arithmetic-grounding inventory of which numeral comes from which NAT-* axiom. The information is identical between sites and already encoded in each claim's *Depends:* slot. A reader walking the proof has to absorb the same grounding twice. This is the kind of book-keeping prose that could be implicit (or at most stated once per ASN at the top) rather than recapitulated at each derivation.

### T4b body introduces N, U, D, E as both component letters (via T4) and projection functions
**Class**: OBSERVE
**Foundation**: n/a (internal)
**ASN**: T4 *Definition:* slot uses `N₁. ... .Nₐ . 0 . U₁. ... .Uᵦ . 0 . D₁. ... .Dᵧ . 0 . E₁. ... .Eδ` where `N₁, …, Nₐ` are positional component letters. T4b *Definition:* slot then introduces `N, U, D, E : T ⇀ T` as partial-function names.
**Issue**: The same letters carry two distinct typings across adjacent claims — bound subscripted constants `Nᵢ ∈ ℕ⁺` in T4's canonical-form schema, and projection-function names `N : T ⇀ T` in T4b. The connection (T4b's `N(t) = (t₁, ..., t_{s₁−1})` is the sub-sequence T4's prose calls `N₁. ... .Nₐ`) is left implicit. A precise reader reconciling T4 against T4b has to infer the bridge.

VERDICT: REVISE
