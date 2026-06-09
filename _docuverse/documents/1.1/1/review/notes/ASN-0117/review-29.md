# Review of ASN-0117

I checked every claim against its cited foundation, verified the case split, recomputed the displacement arithmetic, and traced the invariant-preservation discharge for both realisations. The note is rigorous. Details below.

## Verification performed

**Realisation split (`R ≠ ∅` composite vs. `R = ∅` lone K.μ⁻).** The case boundary is correct. `R = ∅ ⟺ J + c = N + 1 ⟺ J − 1 = N − c`, so when no suffix survives the surviving prefix `{q_1,…,q_{J−1}}` already equals the closed-up run `{q_1,…,q_{N−c}}` and a K.μ⁺ step would have zero survivors to add — correctly excluded by K.μ⁺'s strict-extension precondition. The lone-K.μ⁻ route and J2 (ContractionIsolation) for the frames are correctly applied.

**Composite ≡ ASN-0082 displacement.** Step-2's stated mapping (`q_J ↦ M(d)(q_{J+c})`, …) reindexes exactly to ASN-0082 D-SHIFT (`M'(d)(q_{k−c}) = M(d)(q_k)`), so the net effect is genuinely the foundation contraction, not merely asserted to be.

**Coupling discharge (`R ≠ ∅`).** J0 (no fresh content), J1★ (no range-new I-address: each re-placed survivor was already in `ran(M(d)|_{s_C})` in the initial state, so the trigger conjunct is false), and J1'★ (no new provenance) are correctly evaluated *only at the composite boundary*, which is what defeats the apparent intermediate-state violation after step 1. P4★/P4a/P7a are correctly handled via `R' = R` and shrinking `Contains_C`.

**wp refinement.** `ran(M'(d)) = ran(M(d)) ∖ A_del^{excl}` checks out: the `s_L` term is correctly omitted from `A_del^{excl}` because `A_del` is text-subspace content (disjoint from link images by SD/L0), and the per-link existential (not per-slot universal) is correctly identified as the *weakest* condition given LP12's existential discoverability.

**Boundaries and examples.** Middle, multi-position suffix shift, leading-span (`J=1`, empties then re-pins depth), suffix-delete, delete-everything (`n'_{s_C}=0`), within-document sharing (`A_del^{excl}=∅`), and cross-document transclusion are all worked and each verified against the stated postconditions. Gap-closure non-collision (`q_{J−1} < q_J`, consecutive, no overlap) holds.

**Citations.** All references (ASN-0034, 0036, 0043, 0047, 0082, 0093, 0098) are to foundation ASNs and use foundation notation rather than reinventing it.

## REVISE

(none)

## OUT_OF_SCOPE

### The five Open Questions
**Why out of scope**: Deletion below the document origin (`J < 1`), concurrent-edit serialisation, content-index/arrangement invariants, backtrack reconstructibility, and cross-document orphan obligations are each new territory. The note correctly excludes them via precondition (`1 ≤ J`) or defers them explicitly; none is an error in this ASN.

### Link-arrangement contraction (`subspace(p) = s_L`)
**Why out of scope**: DELETE is restricted to `S = s_C`. Removing a link's arrangement entry (vs. the immutable link itself, L12) is a distinct operation not claimed here, so there is nothing to flag.

VERDICT: CONVERGED
