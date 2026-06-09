# Review of ASN-0121

I verified the load-bearing material in detail:

- **FL-DEF derivation** — the soundness/completeness "forcing" argument correctly identifies the addressability conjunct as the slack-remover (R_min vs R_max), so the answer set is genuinely forced rather than stipulated.
- **nullified monotonicity over the full ASN-0047 vocabulary** — the structural argument (nullified is a function of `Σ.L` alone; non-K.λ ops frame `Σ.L` fixed; K.λ covered by R6a) is correct and, importantly, does not over-extend R6a beyond its native ASN-0086 scope. This is handled exactly right.
- **FL-WP** — the three cases partition correctly on `L_R^{Σ'}` membership (arity-3 ∧ slot-3 coverage equality), not on coverage match alone; (a)/(c) are exhaustive over fresh links; (b) covers existing-link survival. The ghost-pre-coverage conjunct in (a) and the self-retraction conjunct in (c) are both non-vacuous and correctly carried (mirroring ASN-0086 wp Case 2). The case-(b) ⊆/⊇ split (singleton `L_R` extension for ⊆, R6b for ⊇) genuinely establishes the *weakest* precondition rather than only sufficiency.
- **Traces 1–7** — I recomputed the coverage intersections, the `home` field-projections (e.g. `home(a₅) = [1,0,1,0,2] = d'`), the wide-span `athome` example (`p ⊕ ℓ = [1,0,1,0,2,1,1,1]`, document tumbler `[1,0,1,0,2]` in coverage), and the prefix tests in the node/document residence cases. All check out, including the self-retraction `b ∈ coverage(G_self)` by reflexivity of `≼`.
- **Boundary cases** — empty store, all-wildcard (unit), empty-constraint (zero), link-side empty endset, ghost types, orphans/resurrection are all covered.
- **Citations** — every referenced ASN (0034, 0043, 0047, 0086, 0093, 0098) is in the foundation set; no improper cross-references; no reinvention of foundation notation (`coverage`, `home`, `nullified`, `L_R`, `discoverable_from`, span/order machinery all used as given).
- **FL-REACH(d)** — the careful restriction from "supersets the discoverable union" to "supersets the *satisfying* discoverable union" (with the `q = (∗, ∅, ∗, ∗)` counterexample to the naive claim) is correct, and strictness-via-orphans holds.

I found no hand-waves, no proof-by-"similarly," no uncovered conjuncts, no incorrect derivations, and no missing edge cases within the operation's scope. The open questions are genuinely separable future work, not gaps in this operation. The one notational overload I noted — `F, G, Θ` reused for link endsets inside FL-WP while also naming request components in `q = (H, F, G, Θ)` — is consistently disambiguated by the `q.` prefix and does not rise to a revision.

## REVISE

(none)

## OUT_OF_SCOPE

(none — the scoped-out topics are correctly absent; the open questions appropriately defer version-qualified inquiry, V-spec/I-address agreement, and federation reach to future ASNs.)

VERDICT: CONVERGED
