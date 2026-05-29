# Review of ASN-0042

## REVISE

### Issue 1: `delegated_Σ` has no fixed signature
**ASN-0042, State Axioms — Definition (delegated_Σ)**: "delegated_Σ(π, π') holds iff π ∈ Π_Σ, the successor state Σ' satisfies Σ → Σ', and the six conditions are met... The notation does double duty... context disambiguates."
**Problem**: The predicate is written as binary `delegated_Σ(π, π')`, but its body references "*the* successor state Σ'" and condition (iii) `π' ∈ Π_{Σ'} ∖ Π_Σ` depends on which Σ'. In a branching transition system a state has multiple successors, so the definite article presupposes a uniqueness that the model does not supply. Whether Σ' is existentially bound, a free parameter, or fixed "by context" changes the predicate's meaning — and O8's "historical reading" leans on a *specific* Σ' while NestingByDelegation's `R_Σ` is defined purely on Σ. A predicate's arity cannot be left to context.
**Required**: Pin the signature. Either make it 4-place `delegated(Σ, Σ', π, π')`, or adopt the structural `R_Σ` definition (most-specific covering parent on Σ alone) as primary and prove the six conditions hold at the introducing transition as a consequence. Drop the "context disambiguates" device.

### Issue 2: O7(a) re-proves the named covering-chain lemma
**ASN-0042, O7(a)**: "*Covering-chain lemma (cited).* O2 (OwnershipExclusivity)'s proof... establishes that any two tumbler prefixes of the same address are linearly ordered... (Both p and q agree with a on their leading components; whichever is shorter is a prefix of the other.)"
**Problem**: The lemma was extracted in *Ownership Domains* as a named result (PrefixesOfCommonAddressAreComparable) precisely so call sites cite rather than reprove. O7(a) instead attributes it to "O2's proof" and restates the argument inline. This is the duplication the extraction was meant to remove.
**Required**: Cite the named lemma by name; delete the inline re-derivation.

### Issue 3: "Why the axiom is needed" prose attached to axioms
**ASN-0042, pfx(π) and allocated_by_Σ**: e.g. "The mapping pfx is a primitive of the ownership model — it is posited, not derived. We justify its well-formedness..." and "This relation is primitive — it admits no derivation within the ownership model, and we justify its status as such."
**Problem**: These paragraphs explain *why* the axiom is posited and what would go wrong without it, rather than stating *what* it says. Per the anti-bloat classifier this is meta-prose in a structural slot; the formal contracts already carry the content.
**Required**: Reduce each axiom to its statement, signature, and the constraints that bind it (O5/O16 for `allocated_by`). Remove the well-formedness apologetics.

### Issue 4: Use-site inventories on derived properties
**ASN-0042, multiple**: PrefixBaptismCoupling ("so subsequent properties may cite the single load-bearing fact rather than reassemble..."); DelegatorAllocatesPrefix ("makes explicit a coupling that the subsequent proofs of O7 and OwnershipDomainPermanence already rely on tacitly"); MostSpecificCoveringUnique ("O7(a)'s case analysis, DelegatorAllocatesPrefix's identification π_a = π_d, and OwnershipDomainPermanence (Step 3) all rely on this"); O18 ("The O10 fork analysis cites the named derived property..."); the delegated_Σ definition ("makes delegated_Σ available to the proofs of O3, NestingByDelegation, and OwnershipDomainPermanence... without forward-reference").
**Problem**: Enumerating downstream consumers does not advance the property's meaning; it is bookkeeping that rots as the document changes.
**Required**: State each derived property and its proof; delete the consumer inventories.

### Issue 5: SelfOwnershipAtPrefix deferral stated twice in one paragraph
**ASN-0042, Worked Example — "Concrete witness for SelfOwnershipAtPrefix"**: opens "it does not re-derive the general fact" and closes "the present paragraph exhibits the concrete witness rather than re-derive the general fact... is established as the derived property SelfOwnershipAtPrefix in the Exclusivity Invariant section above."
**Problem**: The same disclaimer ("this is a witness, not the proof") appears at both ends of one paragraph. Two sentences saying the same thing.
**Required**: Keep one.

### Issue 6: Worked-example trajectory re-derived after claiming to summarize
**ASN-0042, O10 Fork — *Trajectory***: "we summarize the resulting baptismal registry rather than re-derive it" — followed by a full re-listing of each `Bop` call with its B6/B1 checks, duplicating the *Delegation* and *Sub-account namespaces* segments earlier in the Worked Example.
**Problem**: The B6/B1 obligations for `[1,0,2,0,4]`, `[1,0,2,0,5]`, the namespace baptisms, etc. are checked in both places. The text announces a summary and then performs the re-derivation it disclaims.
**Required**: Pick one site for the trajectory's B6/B1 discharge and cite the cumulative `Σ.B` at the other.

### Issue 7: O8 re-explains the delegated_Σ duality
**ASN-0042, O8 — "*Historical reading of `delegated_{Σ_d}(π, π')`*"**: a full paragraph re-deriving the historical-vs-structural reading already given at the delegated_Σ definition.
**Problem**: Two paragraphs in different sections say the same thing (the duality, the coincidence on actual transitions). Compounds the Issue-1 ambiguity rather than resolving it.
**Required**: With the signature fixed (Issue 1), this paragraph collapses to one sentence or disappears.

## OUT_OF_SCOPE

### Topic 1: Multi-step monotonicity of O3
O3 proves per-transition refinement (`#pfx(ω)` non-decreasing); a transitive-closure monotonicity statement is not given. This is an incompleteness, naturally paired with OwnershipDomainPermanence★, and can be added later — not an error in the present claims.

### Topic 2: Ownership transfer mechanics
The transfer/provenance tension is correctly recorded as an Open Question; concrete transfer machinery belongs to a future ASN. (Note the "birth certificate / deed" framing recurs in both the O3 and O6 sections — consolidate the prose, but the deferral itself is appropriate.)

VERDICT: REVISE
