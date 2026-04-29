# Review of ASN-0047

## REVISE

### Issue 1: Reachable-state invariants table entry omits P7a
**ASN-0047, Properties Introduced table**: "Reachable-state invariants | Every state reachable from Σ₀ satisfies P4, P6, P7, P8, S2–S8-fin"
**Problem**: The theorem body explicitly includes P7a: "satisfies P4 (Contains(Σ) ⊆ R), P6, P7, P7a, P8, S2, S3, S8a, S8-depth, and S8-fin." The table entry drops P7a from the list. P7a is a load-bearing invariant — it guarantees provenance coverage for every I-address — and its omission from the summary could lead a reader to miss it as a required reachable-state property.
**Required**: Add P7a to the table entry for the reachable-state invariants theorem.

### Issue 2: "M₀ is the empty function" contradicts established totality
**ASN-0047, Initial state definition**: "M₀ is the empty function — (E₀)\_doc = ∅, so no arrangements exist"
**Problem**: The state model section establishes "M is a total function with M(d) = ∅ (the empty partial function) when d ∉ E\_doc." A total function is not an empty function — in standard mathematical usage, the empty function is the unique function with empty domain. M₀ has domain T (all tumblers); it maps every argument to the empty partial function. The clarifying clause helps, but the initial phrasing directly contradicts the totality established three paragraphs earlier. The same imprecision appears in the properties table ("M₀ empty").
**Required**: Replace with phrasing consistent with totality, e.g., "M₀(d) = ∅ for all d — (E₀)\_doc = ∅, so every arrangement is the empty partial function."

### Issue 3: "Purely destructive" mischaracterizes K.μ~
**ASN-0047, Temporal decomposition**: "The purely destructive transitions — K.μ⁻ and K.μ~ — are confined to the presentational layer alone"
**Problem**: K.μ⁻ is purely destructive — it removes mappings and nothing else. K.μ~ is a reorganisation: it preserves the multiset of referenced I-addresses (ran(M'(d)) = ran(M(d))) and the domain cardinality (π is a bijection). Its decomposition into K.μ⁻ + K.μ⁺ shows it contains a constructive component. Grouping it with K.μ⁻ under "purely destructive" misrepresents the distinction the ASN itself draws between K.μ⁻ (removal) and K.μ~ (rearrangement). The sentence immediately following distinguishes "constructive" coupling (K.α → K.μ⁺ → K.ρ), making the contrast between constructive and destructive load-bearing.
**Required**: Rephrase to reflect that K.μ⁻ and K.μ~ are the transitions *admitting* destructive change (or confined to the presentational layer), without asserting both are "purely destructive."

## OUT_OF_SCOPE

### Topic 1: Origin-containment correspondence
J0 requires every freshly allocated I-address to appear in *some* arrangement but does not require it to appear in the origin document's arrangement. Content allocated under d₁'s prefix (origin(a) = d₁) could be placed exclusively in d₂'s arrangement, leaving d₁ with no mapping to its own content and no provenance entry (a, d₁) ∈ R. The informal justification ("content enters the docuverse by being placed in a document") suggests placement in the origin document, but the formal J0 is weaker. Whether J0 should be strengthened — or whether the divergence between structural attribution and initial containment is intentional — is a design question for a future ASN on allocation-placement correspondence.
**Why out of scope**: J0 as stated is internally consistent with all proved invariants (P4, P6, P7, P7a). The gap is between informal intent and formal strength, not a correctness error.

### Topic 2: Composite granularity and intermediate provenance
J1' prevents valid composites from recording provenance for content that is not present in the final-state arrangement. A composite that inserts content (K.μ⁺) and then removes it (K.μ⁻) cannot record provenance for the intermediate containment, because the final-state ran(M'(d)) \ ran(M(d)) would be empty for that address. The system requires two separate composites (insert, then delete) to capture the historical association. Whether finer-grained provenance tracking is needed — or whether the composite-level evaluation is the right abstraction — belongs in a future analysis of provenance semantics.
**Why out of scope**: The current model is consistent; composites that satisfy J0/J1/J1' produce correct reachable states. The question is about the granularity of the abstraction, not an error in it.

VERDICT: REVISE
