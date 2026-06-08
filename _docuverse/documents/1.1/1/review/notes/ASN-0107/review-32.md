# Review of ASN-0107

I checked the matching-set definition, both anchorings, the E/D/A/R laws, the R6 weakest-precondition derivation, and the worked instance (counts, reordering, contraction) against the foundation contracts. The technical core is sound — the D2 reordering formula now reads the single-inverse form `Σ.M(d_q)(u)` over `u ∈ π⁻¹(Wᵢ)` and agrees with the worked example. One construction is asserted without the derivation the rest of the note maintains.

## REVISE

### Issue 1: W2's k-for-k swap asserts a preserved count without deriving it
**ASN-0107, "What the Count Does Not Say" / W2 (NonReconstructibility)**: "with `k = |match|` currently-matching links, a `k`-for-`k` swap — withdraw all `k` from the discovery view (a `K.μ⁻` contraction severing every consulted endpoint that reaches them) and create `k` fresh matching links in the queried region — holds the discovery count fixed at `k` while every member of the matching set changes."

**Problem**: The two compressed steps do not compose into "count fixed at `k`" as written. The withdrawal is a `K.μ⁻` contraction that severs the consulted endpoints — by D2's own contraction clause this strictly shrinks the resolved request (`Qᵢ(Σ') ⊆ Qᵢ(Σ)`), removing exactly the addresses the `k` links reached. For `k` *fresh* links to then match, their coverage must meet the now-smaller resolved request `Qᵢ(final)`; a bare link-creation (`K.λ`) cannot make them discoverable, because their endpoints are not in the contracted region. Restoring `k` matches requires fresh content (`K.α`), arrangement extension into the queried region (`K.μ⁺`), and links pointing there (`K.λ`) — and the claim that the final count lands on *exactly* `k` (neither below, from over-contraction, nor above, from residual matches) is the non-trivial part, left unshown. The note's own parenthetical concedes the single-swap case is the clean one ("`A single withdrawal paired with a single creation … only when k=1`"), which is precisely the case that needs no balancing argument.

**Required**: Either derive the composite (name the `K.μ⁻` → `K.α`/`K.μ⁺`/`K.λ` sequence and show the final matching set has cardinality `k` and is disjoint from the initial one), or ground W2 on the `k = 1` single-swap alone — which already establishes "equal counts need not denote equal matching sets" — and drop the undischarged `k`-for-`k` elaboration.

### Issue 2: Trailing-suffix definition enumerates its downstream consumers
**ASN-0107, paragraph introducing the trailing-suffix property**: "We call this the *trailing-suffix property* of `K.μ⁻`, and the R-laws below invoke it without re-deriving it."

**Problem**: This is a use-site inventory — the definition's introduction names which later claims will consume it rather than advancing the property's content. Under the note's anti-bloat classifier this is the flagged "definition enumerates downstream consumers" pattern; the clause adds no reasoning a reader of R1/R2/R6 needs at the point those claims cite the property.

**Required**: End the sentence at the property's statement ("…We call this the *trailing-suffix property* of `K.μ⁻`."). The R-laws already cite it where they use it.

## OUT_OF_SCOPE

### Topic 1: n-set requests for arity N > 3
The note fixes `sat` to slots 1–3 and states the development "generalises slot-by-slot." Counting semantics for links with `N > 3` consulted slots is future territory, not an error here.

VERDICT: REVISE
