# Review of ASN-0114

This is a careful, well-constructed note. The mathematics holds: F1's witness argument is sound (the recorded endset is its own span-set), the two collapses are correctly derived from ASN-0053 S2, F2's convexity argument (via S0) is valid, the worked instance checks out arithmetically (δ(2,#a₃) shifts a₃→a₅, LP-Fin Corollary gives the F-restricted coverage {a₃,a₄,a₇,a₈}, and a₅ witnesses disconnectedness in T), and the wp analyses are non-trivial and correct. Depth is present: consequences are derived, a concrete example discharges F2 and F7, and the F7 wp for `R = ⟨⟩` is real analysis. All substrate citations are to foundation ASNs. The note does not drift — it specifies a query's precondition, postcondition, frame, and invariants abstractly at the coverage level.

The findings below are accretion issues, which is what the `review-mode.anti-bloat` classifier asks for.

## REVISE

### Issue 1: The L12↔LP13 composition is stated four times, and the intro's standalone attribution to L12 is imprecise
**ASN-0114, "Determinism over time" (F5)**: The intro says "From coverage exactness (F1) and link immutability (L12, composed along Σ →\* Σ' by LP13)... and, by L12, that value never changes once a ∈ dom(Σ.L)."
**Problem**: The relationship "L12 is single-step / LP13 composes it across Σ →\* Σ'" is restated in four places that say the same thing: (a) the intro's parenthetical "(L12, composed along Σ →\* Σ' by LP13)"; (b) the intro's next sentence "by L12, that value never changes once a ∈ dom(Σ.L)"; (c) the Derivation in full ("L12... fixes a link's value across a single transition... LP13... supplies that composition"); and (d) the Claims table Status, "from F1 and L12 immutability, the latter composed by LP13." Separately, (b) read on its own is imprecise: L12 is a single-transition invariant, so "never changes once a ∈ dom(Σ.L)" — a quantification over the reflexive-transitive closure — is LP13's guarantee, not L12's. The intro thus contradicts its own Derivation, which explicitly says the single-step fact "must be composed along the sequence" by LP13.
**Required**: State the composition once, in the Derivation where it belongs. Reduce the intro to the permanence consequence and its meaning (two requests separated by any operations denote the same positions), citing LP13 for the multi-step persistence rather than re-deriving the citation mechanics or attributing multi-step permanence to L12 alone.

### Issue 2: The synthesis re-derives the dependency structure already carried by the Claims table
**ASN-0114, "Synthesis"**: "...with F2, F3, F5, F6, and F8 following as corollaries (F2, F3, F6 from F1; F5 from F1 and link immutability; F8 from F0 and F1)."
**Problem**: The parenthetical restates the per-claim derivation annotations that the Claims Introduced table already records in its Status column ("corollary of F1," "from F1 and L12 immutability, the latter composed by LP13," "corollary of F0 and F1," etc.). It adds no reasoning the table does not already carry, and it states F5's dependency a *fifth* time (cf. Issue 1). This is the dependency structure repeated, not advanced.
**Required**: Drop the parenthetical dependency inventory. The synthesis can name F1, F4, F7 as the primary commitments and the rest as corollaries without re-listing each derivation chain; the table is the canonical place for that.

## OUT_OF_SCOPE

The note's scope boundaries are well-drawn. Resolution of an endset against a document's arrangement is correctly carved out (the "boundary we must respect" section and Open Question 2), and the Scope list and Open Questions already cover normal form, serialization-boundary signalling, higher-slot distinction, and multi-document coverage. No additional future-ASN topics surfaced.

VERDICT: REVISE
