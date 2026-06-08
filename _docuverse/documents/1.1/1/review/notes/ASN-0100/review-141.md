# Review of ASN-0100

I checked the substrate decomposition, every invariant in ASN-0047's `ExtendedReachableStateInvariants` (per-state, composite-boundary, and composite-transition classes), all six worked examples, the projection-shift derivation, the wp analysis, and the atomicity argument at each intermediate state. I also ran the anti-bloat checks for forward-reference accretion and reviser drift.

## Findings

The proof obligations are discharged completely. Specific things I verified that are commonly skipped:

- **K.μ⁻ firing dichotomy is exact.** `Right = ∅ ⟺ V_{s_C}(d) = ∅ ∨ p_m = N+1` is correctly proven (when `p_m ≤ N`, `p` itself is a pre-state position, so `p ∈ Right`). The strict-contraction precondition of K.μ⁻ (`n'_{s_C} = p_m − 1 < N`) is discharged precisely in the fired case, including the prepend `n'_{s_C} = 0` full-clearance.
- **S2 functionality** correctly relies on pairwise region disjointness *plus* exhaustiveness (INS.M-exhaustive) — the latter is genuinely load-bearing (it rules out a fourth-region domain position with undefined image), not decorative.
- **D-CTG★ at `m_C ≥ 3`** is the live case (off-prefix slice tuples like `[1,2,1]`), and the closed-interval reduction handles it explicitly via T1 case (i), both for the general claim and the deep-subspace worked example. The arbitrary-pair-vs-extremes gap in D-CTG★'s quantifier is closed by transitivity in one step.
- **The first-/subsequent-emission branch keys on `dom(C)`, not arrangement** — the re-insertion-into-cleared-subspace example correctly exposes the decoupling of V-position index from I-chain index, which is exactly the trap an implementer would fall into.
- **Boundary cases** (prepend with forced clearance, append with omitted K.μ⁻, empty document with first-emission, `n=1` single-element) are each worked concretely with postcondition checks.
- **wp analysis is non-trivial** (discoverability transparency for tight endsets; provenance membership reducing to a Boolean over `(a,d)∈R` and chain-membership).

Atomicity is argued at the post-K.μ⁻ intermediate (the one state with no I3 counterpart) independently rather than by appeal to I3, and the post-K.μ⁺ intermediate correctly defers to the Σ' verification instead of re-proving.

**Anti-bloat / drift checks:** I found no defensive justifications, use-site inventories, or duplicated paragraphs rising to a finding. The I3-coincidence apparatus and the repeated `inherited I3-*` deferrals are backward references to a single established lemma (§Effect Three), not the flagged downstream-deferral pattern. The six examples are each distinct in the case they stress. The substrate decomposition does not drift to implementation mechanics — the note explicitly separates the unique post-state contract from the non-unique realizing interleaving, which is the correct abstraction stance.

## OUT_OF_SCOPE

The Open Questions (partial-failure recovery, link-subspace insertion, self-composition closure, concurrent INSERT serialization, derived document properties) are correctly deferred and bounded in §Bounding the Scope; they are new territory, not gaps in this ASN.

VERDICT: CONVERGED
