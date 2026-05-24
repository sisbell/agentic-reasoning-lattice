# Review of ASN-0094

## REVISE

### Issue 1: NAT-card additivity derivation fails on interleaved disjoint sets
**ASN-0094, Appendix: Local NAT Primitives**: "For disjoint finite `S₁, S₂ ⊆ ℕ`, NAT-order's trichotomy makes one of `max(S₁) < min(S₂)` or `max(S₂) < min(S₁)` hold (disjointness rules out equality); without loss of generality `max(S₁) < min(S₂)`"
**Problem**: Trichotomy on (max(S₁), min(S₂)) yields one of <, =, > (disjointness excludes =), giving either max(S₁) < min(S₂) or max(S₁) > min(S₂). The framework reframes the > case as "max(S₂) < min(S₁)", which is not equivalent. Counterexample: S₁ = {2, 7}, S₂ = {3, 5} are disjoint; max(S₁) = 7 > 3 = min(S₂) (the > case), but max(S₂) = 5 and min(S₁) = 2, so 5 < 2 is false — neither claimed inequality holds. The WLOG and concatenation argument therefore only covers the non-interleaved sub-case (one set entirely below the other), not general disjoint finite ℕ-subsets.
**Required**: Derive additivity for the general case (e.g., by induction on |S₁| + |S₂|, by bijection counting, or by recursive merge of two enumerations). Audit consuming sites: LinkAddressNotPrefixOfEmit Step II.1 partitions {1, ..., #a} into non-interleaved {1..#b} and {#b+1..#a}, so its application is sound under either derivation; AllocatedAddressAntichain Step 3.1 invokes the subset-identity corollary, whose derivation appeals to additivity at the potentially-interleaved partition S = T ⊔ (S \ T) — replace with a direct pigeonhole argument or fix the underlying additivity proof.

### Issue 2: EffectiveWpSimplification Corollary's framing ignores per-K contract gates
**ASN-0094, Corollary — EffectiveWpSimplification**: "at any call site for which the framework's Sh-conf gate would admit `Emit_K(Σ, d, F, G)` (i.e., the call reaches the substrate primitive K.λ rather than being short-circuited to `⊥` by Sh-conf)" ... "the *effective wp* of `Emit_K` under the framework simplifies to `wp_eff(Emit_K(Σ, d, F, G), (a, F, G) ∈ A_K^{Σ'}) = d ∈ dom(Σ.M) ∧ K ∈ T_cat ∧ conf_K^Σ(F, G)`"
**Problem**: Per the Gate Ordering (consolidated) clause in the Sh-conf section, per-K discipline contracts — Sh4 idempotency contract (gate 3), FDD functional-dependency contract (gate 3), single-home commitment (gate 1) — can intercept a call between Sh-conf's clauses (gates 2 and 4) and short-circuit it to `⊥` before K.λ fires. (a) The parenthetical "Sh-conf admit ⟺ reaches K.λ" is therefore wrong for contract-registered K. (b) The wp_eff formula, named with postcondition `(a, F, G) ∈ A_K^{Σ'}` (new tuple active in Σ'), is necessary but not sufficient under contract K — a contract-suppressed call satisfies wp_eff but no new tuple is deposited, so wp_eff overshoots the true wp for the stated postcondition.
**Required**: Either restrict the equivalence to "Sh-conf admit AND every applicable per-K discipline contract doesn't suppress" as the condition for reaching K.λ, or restate wp_eff with conditional contract conjuncts (`K-under-Sh4 ⟹ C(F, G, Σ) = ∅`, `K-under-FDD ⟹ C_fd(F, Σ) = ∅`, `K-under-SHCD ⟹ d = d_K`). The wp_086 simplification claim is unaffected, but the corollary's current framing conflates "Sh-conf admits" with "K.λ fires."

### Issue 3: Sh5(b) "implicit registration check" lacks a falsifiability mechanism
**ASN-0094, Corollary — EffectiveWpSimplification, *Coverage-class disjointness from R*** : "The framework therefore imposes the following implicit registration check on every new catalog row: a row with `shape ≠ shape(R)` is admissible as a non-R-equivalent shape; a row would be admissible at `shape = shape(R)` only via direct `~`-equivalence with R"
**Problem**: This "implicit registration check" is stated but never connected to an enforcement mechanism. Sh5(b)'s minimal review checklist (Symbol enumeration, Per-symbol classification, Accept/reject decision) checks template-body symbol categories — not catalog-row shape-tuple admissibility. A catalog author could register K at shape exactly equal to shape(R) without `K ~ R`, escape Sh5(b)'s symbol audit, and break Step 2 Case A's `K ≁ R` precondition for all non-R K's at that shape. The framework's text claims this is "automatic" but supplies no gate that enforces it.
**Required**: Either (a) extend Sh5(b)'s review checklist with a shape-tuple admissibility step that rejects K with `shape(K) = shape(R) ∧ K ≁ R`, or (b) explicitly weaken the corollary's `K ≁ R` conclusion at catalog rows beyond R from a derived fact to a hand-curation aspiration (matching the Sh5(a) downgrade pattern). Currently the claim sits between the two without procedural support.

## OUT_OF_SCOPE

### Topic 1: Multi-process substrate coordination
**Why out of scope**: The framework explicitly commits to single-process substrate scope (Sh4 contract's *Scope* clause). Multi-process Sh4 atomicity is properly listed under Open Questions as a scope boundary.

VERDICT: REVISE
