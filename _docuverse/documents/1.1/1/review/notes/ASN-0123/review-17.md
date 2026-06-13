# Review of ASN-0123

I reviewed this as an operation specification, concentrating on the places operations fail: precondition completeness, case exhaustiveness, the boundary cases (empty source, first/last position, cross-owner), frame conditions, and the load-bearing novel proofs. I traced the proofs rather than the summaries.

The genuinely new content — not foundation citation — is PS, VN-B1, the `nextv` frontier, SA, the severance theorem (V9a), and the G1/G2/G3 derivations. I checked each.

- **PS coverage induction** (`n₀ ≼ e` for every `e ∈ E`): the case split is complete (node via NodeBaptism(b); K.δ case (ii) for `k∈{0,1,2}` each preserving position 1, with the `k=0` operand forced non-node so `#t ≥ 3` and `sig(t)=#t` lands strictly past position 1). Holds. The `ω` totality then rests only on coverage, which is what O2 consumes. The hybrid is honestly flagged as a standing assumption.
- **VN-B1**: induction over atomic transitions, all four K.δ arrivals into `S(d,1)` analyzed — Node excluded by `zeros`, `k=2` by the penultimate-separator argument, `k=1` forcing exactly `c₁`, `k=0` forcing `c_{m+1}` via the operand `c_{j-1}∈E` plus freshness. Contiguity is preserved without invoking B2's global precondition. Correct, and the deliberate avoidance of B2 is well-justified.
- **`nextv` frontier**: `next(E,d,1)=c_{hwm+1}` derived from VN-B1 + S0 alone (both `m=0` and `m≥1` branches collapse correctly). Sound.
- **SA**: the antichain argument (a proper extension would seat a third zero inside the longer document prefix, contradicting `zeros=2`) is correct, and its use in G2/V10 to collapse subtree coverage to address identity is exactly right.
- **Severance (V9a)**: the eight-step proof closes both branches of the final comparability split (`d_src ≼ pfx(π)` ⊥ O1a via Z-mono; `pfx(π) ≼ d_src` ⊥ O2 maximality). O5(ii) is legitimately applied to `π_o ∈ Π_Σ` at the allocating K.δ. Airtight — severance is a theorem, not a stipulation.
- **G2 necessity**: range preservation `A ⊆ ran(M'(v))` is forced via LP12 + SA (the unit-depth-span construction over each carried `a`), and the copy-failure argument (addresses, not values, populate coverage) is correct. This is the operation's strongest derivation.
- **V-WF**: both ValidComposite★ clauses discharged; the `n=0`, owned, and cross-owner branches each yield a single identity K.δ (the account-tier restriction on cross-owner is *forced*, not stylistic, and correctly excludes the node-tier non-owner). J1★/J1'★ pinned by the `R'` clause.
- **V9w**: the dependence on P-bdy (P4★ is a composite-boundary property, fails at an interior start) is explicitly and correctly load-bearing; the failure scenario given is exactly the right one.
- **Both worked instances** (`d=1.1.0.1.0.1` fork chain; the three-position/two-address carry-through with `|A|=2<n=3`) check out arithmetically, including `a₁⋠a₂`, the `{[1,1],[1,3]}` projection, and `|R'∖R|=|A|`.

Boundary coverage is complete: empty source (`n=0`, vacuous couplings), links-only source (`n=0`, V2b excludes foreign-link transcription), shared intra-document content (M14 case, worked), iterated forks (V6 closure with `B6(wⱼ,1)` unconditional at every depth), and transcluded source content (origin traces to true authors, V9w). The VD biconditional is carefully restricted to the address-encoded fragment, with the unrestricted forward direction correctly shown to fail on cross-owner forks.

## REVISE

(none)

The load-bearing proofs hold, every invariant conjunct the composite touches is discharged (directly for step preconditions and couplings, via ExtendedReachableStateInvariants for the post-state), the boundary cases are present, two concrete worked instances verify the key postconditions, and the necessity derivations (G1/G2/G3) and the severance impossibility supply the non-trivial weakest-precondition-style content (V10 is an exact iff for link discoverability from `v`). No cross-references to non-foundation ASNs appear in the body. The ASN defines state-abstract guarantees, not implementation mechanics, and the udanax-green evidence with its four deviations is kept properly distinct from the contract.

## OUT_OF_SCOPE

Nothing in-scope is missing. The future territory — version-namespace discipline against non-VERSION allocators, recovering derivation direction for cross-owner forks, link-subspace re-creation, concurrent-fork serialization, location-fixed windowing, withdrawal/supersession, post-contraction provenance semantics, and shared-identity correspondence — is already enumerated in the Open Questions and correctly deferred. The ASN defines no claims for the harness-listed out-of-scope operations (creation-from-nothing, comparison, content/link ops, delivery, replication); it touches them only through frame conditions and enabling statements, which is appropriate.

VERDICT: CONVERGED
