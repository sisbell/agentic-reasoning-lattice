# Review of ASN-0116

## REVISE

### Issue 1: P6 is cited but never introduced as a claim in the prose
**ASN-0116, "A weakest precondition" section / "Claims Introduced" table**: The wp section states `wp(INSERT, D(d, Σ') = D(d, Σ)) ≡ INSERT-pre ∧ {a : (∃i) coverage(Σ.L(a).eᵢ) ∩ A_new ≠ ∅} ⊆ D(d, Σ)` but never labels it. P0 through P5 are each introduced as boxed, named claims (**P0 (OriginIdentity)**, … **P5 (DocumentIsolation)**); the wp result is not. Yet the worked example cites it three times ("The P6 trap.", "✓ P6 (containment, not emptiness).", "P6 new-block") and the "Claims Introduced" table lists "P6 (DiscoverabilityWP)" as introduced.
**Problem**: A reader following the boxed P0–P5 sequence finds no P6; the label exists only in the table and the worked example, referring to a claim the prose never formally states. The claim is cited as established before it is named.
**Required**: Box and label the wp result as **P6 (DiscoverabilityWP)** in the wp section, parallel to P0–P5, so every reference resolves to a stated claim.

### Issue 2: "verbatim" overstates the I-SHIFT / I-LEFT citation
**ASN-0116, Effect (I-SHIFT, I-LEFT)**: "(I-SHIFT) … — verbatim ASN-0082 **I3 (PostInsertionShift)**." and "(I-LEFT) … — ASN-0082 **I3-L**."
**Problem**: ASN-0082's I3/I3-L characterize the *gapped* post-state `M'₀(d)` whose domain (by I3-V / I3-CS) deliberately excludes the inserted block. INSERT's post-state `M'(d) = M'₀(d) ∪ {block fill}` is a *different* arrangement. The statements `M'(d)(shift(v,n)) = M(d)(v)` and `M'(d)(v) = M(d)(v)` therefore do not hold "verbatim" for INSERT's `M'(d)`; they require the additional fact that the block `{shift(p,k)}` is disjoint from the shifted-suffix and left positions. The ASN does establish that disjointness — but only later, in the contiguity argument — so the citation depends on a downstream lemma the word "verbatim" hides.
**Required**: Either replace "verbatim" with "by I3 together with block-disjointness (established below)," or move the disjointness observation ahead of the Effect so the carry-over from `M'₀(d)` to INSERT's `M'(d)` is licensed at the point of citation.

## OUT_OF_SCOPE

### Topic 1: Provenance coupling (ASN-0047 J1★ / K.ρ)
**Why out of scope**: INSERT is specified in the two-layer substrate (Σ.C, Σ.M) rather than ASN-0047's extended state with the provenance relation R. The ASN does not claim to be an ASN-0047 valid composite, and it already poses the provenance/atomicity question in Open Questions. Establishing the J1★ coupling between freshly allocated I-addresses and recorded provenance is future territory, not a defect here.

### Topic 2: Concurrent insertions and serializing authority
**Why out of scope**: The freshness argument (P0) is single-authority; concurrent allocation without serialization is correctly deferred to Open Questions.

VERDICT: REVISE
