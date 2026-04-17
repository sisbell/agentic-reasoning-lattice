# Cross-cutting Review — ASN-0034 (cycle 8)

*2026-04-17 04:16*

Scanning the ASN for cross-cutting issues not captured in Previous Findings.

### Divergence's Depends omits T0 despite the definition relying on T0-supplied operators

**Foundation**: (foundation ASN — internal consistency; per-step citation convention)
**ASN**: Divergence's Formal Contract reads: *"Depends: T1 (LexicographicOrder) — Divergence formalizes the 'first divergence position'... T3 (CanonicalRepresentation) — exhaustiveness... NAT-wellorder (NatWellOrdering) — case (i) selects `k` as the least index..."* The definition itself uses `#a`, `#b`, `aₖ`, `bₖ`, `min(#a, #b)` — every one a T0 operator — and the case predicates `aₖ ≠ bₖ` and `aᵢ = bᵢ` are ℕ-valued comparisons on T0-supplied components.
**Issue**: Sister definitional properties in this ASN cite T0 for exactly these operators — ActionPoint's Depends lists T0 explicitly for "the length `#w`, and the component projection `wᵢ` used in the definition"; Prefix's Depends cites T0 for "length `#p`, `#q` and component projection `pᵢ`, `qᵢ`"; TA-Pos's Depends cites T0 for "the length `#t`, and the component projection `tᵢ` used in the Definition". Divergence omits the citation despite consuming the same T0 operators.
**What needs resolving**: Divergence's Depends must cite T0 for the carrier-set, length, and component-projection operators that its definition and its case predicates reference, matching the per-step convention established across ActionPoint, Prefix, TA-Pos, TA5-SIG, and other definitional properties.

### T0(a) and T0(b) have no Depends clauses

**Foundation**: (foundation ASN — internal consistency)
**ASN**: T0(a)'s Formal Contract has only *"Postcondition: For every tumbler `t ∈ T`..."*; T0(b)'s has only *"Postcondition: For every `n ∈ ℕ` with `n ≥ 1`, there exists `t ∈ T` with `#t ≥ n`."* Neither carries a Depends clause. T0(a)'s proof explicitly invokes "ℕ is closed under successor" at step (i) — that's NAT-closure — and uses T0's carrier characterisation to conclude `t' ∈ T`. T0(b)'s proof invokes T0's carrier characterisation to conclude `t ∈ T`.
**Issue**: The ASN's convention that definitional and theorem-level properties carry Depends clauses enumerating every property consumed in the proof is applied to every other non-axiom formal contract in the ASN. T0(a) and T0(b) are theorem-level properties — each has a stated Postcondition supported by a proof — not axioms; their proofs invoke at minimum T0 (carrier characterisation) and, for T0(a), NAT-closure (successor closure). Without Depends, a reviser tightening NAT-closure or T0's extensional definition has no mechanical signal that T0(a) and T0(b) consume those facts.
**What needs resolving**: T0(a) and T0(b) need Depends clauses matching the granularity of other theorem-level properties — at minimum citing T0 for the carrier operators consumed in each proof, and NAT-closure for T0(a)'s successor step.

### T2's Depends omits T1 despite T2 being about T1's computability

**Foundation**: (foundation ASN — internal consistency)
**ASN**: T2 (IntrinsicComparison) opens *"The order relation T1 is computable from the two tumblers alone..."* and its proof unfolds T1's definition in detail: *"The definition of `<` in T1 asks for the existence of a witness position `k ≥ 1` satisfying two conditions..."* Case 1 and Case 2 of the proof both consult T1's case (i) and case (ii) structure. T2's Formal Contract, however, lists only *"Depends: T3 (CanonicalRepresentation) — postcondition (a) requires T3 for the equality case."*
**Issue**: T1 is the subject of T2's claim and the source of the case structure T2's proof unfolds; T2 cannot be reconstructed without T1, yet T1 is absent from the Depends. This is a structural gap of the same kind the ASN treats carefully elsewhere (e.g., T5 cites Prefix and T1 despite Prefix already indirectly tying back to T1). A reviser tightening T1's case structure — say, narrowing T1 case (ii)'s precondition or altering its agreement clause — has no Depends-backed visibility into T2's consumption of it.
**What needs resolving**: T2's Depends must cite T1 (and also T0 for the length and component-projection operators that the proof's at-most-`min(#a, #b)` bound and componentwise-comparison terminology reference), matching the per-step convention the ASN applies to every other property whose proof unfolds a cited property's structure.

### ZPD Definition's Depends omits T0

**Foundation**: (foundation ASN — internal consistency)
**ASN**: ZPD's Formal Contract lists *"Depends: Divergence (Divergence) — the Relationship to Divergence postconditions consume Divergence's two-case structure..."* — Divergence is the sole entry. The definition itself, however, writes *"pad to length `L = max(#a, #w)`: `aᵢ = 0` for `i > #a`, `wᵢ = 0` for `i > #w`. If `(A i : 1 ≤ i ≤ L : aᵢ = wᵢ)`, `zpd(a, w)` is undefined. Otherwise, `zpd(a, w) = min {k : 1 ≤ k ≤ L ∧ aₖ ≠ wₖ}`"* — consuming T0's length `#·`, component projection `·ᵢ`, and the ℕ-valued components that make `aₖ = 0` and `aₖ ≠ wₖ` well-formed predicates, plus NAT-wellorder for the `min(·)` construction (the standard per-step discharge ActionPoint, Divergence, and TA-Pos use for the same pattern).
**Issue**: The convention the ASN otherwise maintains — definitional properties cite T0 for the carrier operators they reference and NAT-wellorder for `min(·)` constructions over nonempty subsets of ℕ — is not applied to ZPD. A reader reconstructing ZPD's foundation cannot trace `max(#a, #w)`, the component predicate `aₖ ≠ wₖ`, or the `min{…}` step back to their axiomatic sources through Depends alone; each must be inferred from the narrative.
**What needs resolving**: ZPD's Depends must cite T0 for the length, padding-value, and component-projection operators that the definition consumes, and NAT-wellorder for the `min(·)` step, matching the per-step convention Divergence and ActionPoint apply to structurally identical definitions.

### Citation aliases for NoDeallocation and NAT-* axioms sometimes omit the standard parenthetical

**Foundation**: (foundation ASN — internal consistency; Previous Finding 14 on alias normalization)
**ASN**: T8's Depends reads *"AllocatedSet (AllocatedSet) — defines `allocated(s)`... NoDeallocation (the system defines no removal operation — the sole premise required for the monotonicity conclusion...)"* — the NoDeallocation citation replaces the standard `Property (Alias)` parenthetical with a narrative gloss. Elsewhere NoDeallocation is cited as *"NoDeallocation (NoDeallocation) [forward reference — NoDeallocation is stated after this section]"* (in AllocatedSet's Depends). Similarly, in several Depends clauses NAT-* axioms are cited as *"NAT-sub (NatPartialSubtraction)"*, *"NAT-order (NatStrictTotalOrder)"*, etc. — full alias; but in D1's Depends, NAT-cancel is never cited while conditional subtraction is used (the issue is separately captured), and in various places citations like *"NAT-addcompat's left order compatibility"* appear in prose without the `(NatAdditionOrderCompatibility)` parenthetical that opens the Depends entry.
**Issue**: Previous Finding 14 captured alias drift among T4/T4a/T4c/TA5/T0/TA6 variants. The NoDeallocation citation in T8 shows a related pattern: the standard `Property (Alias)` format is replaced by a parenthetical that describes the property's content. A reviser using grep on the alias name to locate consumers will miss the T8 citation. The convention appears to be `Property (AliasInTitle) — explanation`; T8's NoDeallocation citation omits the alias-in-title component.
**What needs resolving**: Normalize NoDeallocation's citation in T8 to match the `NoDeallocation (NoDeallocation)` form used in AllocatedSet's Depends, so every Depends entry is locatable by alias-text search. More generally, the ASN needs a single canonical citation format applied uniformly, so the Depends graph is mechanically traversable.
