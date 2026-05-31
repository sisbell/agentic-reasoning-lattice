# Review of ASN-0043

I checked the central lemmas (CPP, PrefixSpanCoverage, FSP, FSE), the L1c chain derivation, and verified every conjunct of the state-local invariant set against the FSP discharge and the worked example.

## REVISE

(none)

The proofs I stress-tested all hold:

- **CPP / L1c.** The two-invocation structure correctly pins the third zero at position `#s+1`: first CPP (`p = #s`) gives agreement on `1..#s`; the second on the sub-chain `t₁..tₙ` (`p = #s+1`, valid since `#s+1 ≤ #t₁ = #s+2`) forces `a_{#s+1} = 0`. T4-validity of `s` then identifies the length-`#s` prefix as `home(a)`. The sibling-advance length precondition is genuinely met at each invocation because the opening `k₁=2` lifts length to `#s+2` and lengths never decrease.

- **PrefixSpanCoverage.** Both inclusions are complete, including the `k=m` sub-case of (⊆) where `t_m = shift(x,1)_m` is correctly split into the equal-length and proper-prefix branches, each contradicting `t < shift(x,1)`.

- **FSP completeness.** Every member of the state-local set (L0, L1, L1a, L1b, L1c, L3, L5, L6, L14, L14a, L-fin; S0–S3, S7a, S7b, S7d, S8-fin, S8a, S8-depth, D-CTG, D-MIN, D-SEQ) is discharged by an explicit bullet — none by "similarly." The derived invariants (L0b, L1d, L2, L8/L10/L13 consequences, L11a/b, L12/12a/12b) all reduce to the atomic set, so the list is the correct closure.

- **FSE.** The non-terminal positions argument is sound: `#E(a) ≥ 2` (L1b) places both the separator (`#home(a)+1`) and subspace identifier (`#home(a)+2`) strictly before the terminal `sig` position that `inc(·,0)` advances, so `home`, subspace, and `#E` are all preserved.

- **Worked example.** The 6-step extension exercises the non-singleton content of L5 (order-irrelevance, idempotent membership, extensional inequality), L8 discrimination (`coverage(Θ) ∩ coverage(Θ₄) = ∅` via the position-8 contradiction), and L8 coverage-vs-decomposition (`[g,g') ∪ [g',h) = [g,h)`). The TA5a side conditions (`k'=2 ⟹ zeros ≤ 2`, `k'=1 ⟹ zeros ≤ 3`) check out at every chain step.

The structure is also clean on forward references: L1c's proof, FSP, FSE, L9, and L11b all cite backward to lemmas already defined, so the anti-bloat patterns the classifier warns about (deferral chains, use-site inventories, why-the-axiom prose) are not present in this revision. The three pre-declined findings remain correctly addressed (L1b is grounded three ways; FSP's L1c bullet derives both strong conjuncts from the seed-equals-home constraint; PrefixSpanCoverage is retained as locally-applied span algebra).

## OUT_OF_SCOPE

The Open Questions section already enumerates the genuine future territory (global content-subspace constant, transclusion/link-store consistency, compound-link well-formedness, coverage-equivalence for queries). These are correctly deferred, not gaps in this ASN.

VERDICT: CONVERGED
