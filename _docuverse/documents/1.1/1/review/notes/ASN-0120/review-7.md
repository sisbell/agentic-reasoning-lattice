# Review of ASN-0120

I checked the load-bearing proofs in detail: the V→I confinement step (ordinal-displacement + T5 → `t₁ = s_C`), the exact coverage equation `coverage(e_j) ∩ dom(Σ.C) = ρ(R_j,Σ)`, the `#E = 2` exactness argument and its two uses (creation-state equality and stability under later K.α), the link-half disjointness in ML9 Fact (a), and the wp derivation including the `d' = d` boundary. They hold.

## REVISE

(none)

The proofs survive scrutiny on the points where this kind of ASN usually fails:

- **Confinement is re-derived, not borrowed.** The ASN correctly refuses to lean on ASN-0058's C0/C0a (which presume a *well-formed* reference) and instead re-establishes `⟦σ_j⟧ ⊆ s_C` directly from the ordinal-displacement form via T5, so the partial-span generalization of `ρ` is sound.
- **The `#E = 2` exactness is genuinely load-bearing and proven**, not assumed from C1b's weaker `#E ≥ 2`. It is what makes both ML2's content-coverage equality and ML8's stability-under-K.α hold; both directions are derived.
- **Boundary `d' = d` is handled.** Fact (b) treats the home-document case explicitly, showing the single added range point `a` is inert (`E(a)₁ = s_L ≠ s_C`), and the worked example exhibits exactly this — a link not discoverable from its own home.
- **The wp is the weakest precondition and non-trivial.** Residence-independence is the substantive content; `enabled` correctly folds home-allocation and non-empty-type resolution, and the definedness conjuncts are necessary.
- **Operation boundaries covered.** Empty type → rejected (ML6); empty from/to → permitted by L3 and the `enabled` spec; partial spans via active-position filtering; frame (ML10) confines effects to `Σ.L` and the home arrangement.
- **Foundation usage only.** All cross-references (0034, 0036, 0043, 0047, 0053, 0058, 0086, 0093, 0098) are to verified foundations; no foundation notation is reinvented.

## OUT_OF_SCOPE

### Topic 1: Link-subspace endset arguments (a link pointing at another link)
The ASN restricts endset arguments to content-subspace specs and defers link-to-link references (Open Question 3). This is new territory, correctly excluded.

### Topic 2: Semantics of an empty (non-type) from/to endset
The operation is *defined* on this boundary (the `enabled` spec does not require `ρ(R₁,Σ)≠∅` or `ρ(R₂,Σ)≠∅`), and the *meaning* is deferred to Open Question 2. Appropriate deferral, not a gap in the operation spec.

VERDICT: CONVERGED
