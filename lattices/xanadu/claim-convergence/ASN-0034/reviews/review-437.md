# Regional Review — ASN-0034/TA1-strict (cycle 1)

*2026-04-23 04:37*

### Stale motivation in trailing paragraph
**Class**: OBSERVE
**Foundation**: n/a (internal to ASN-0034)
**ASN**: Trailing paragraph after TA1-strict: "But TA1 alone does not guarantee that addition *advances* a position. It preserves relative order between two positions but is silent about the relationship between `a` and `a ⊕ w`. We need:"
**Issue**: Two problems. (a) "TA1" is not a claim in the shown text — only TA1-strict is defined. (b) The stated gap (advancement, the relationship between `a` and `a ⊕ w`) is already discharged: TumblerAdd exports `a ⊕ w > a` as one of its postconditions, with a proof ("Strict advancement") given earlier in the ASN. The motivation therefore imagines a case the prior claim already excludes — the classic reviser-drift pattern where a lead-in survives past the content that made it true.

### Redundant "unique least" phrasing in Divergence postcondition
**Class**: OBSERVE
**Foundation**: n/a
**ASN**: Divergence formal contract, Postconditions: "in case (i), `divergence(a, b) = k` is the unique least index satisfying `1 ≤ k ∧ k ≤ #a ∧ k ≤ #b ∧ aₖ ≠ bₖ ∧ (A i : 1 ≤ i < k : aᵢ = bᵢ)`"
**Issue**: The conjunction already contains `(A i : 1 ≤ i < k : aᵢ = bᵢ)`, which is itself a minimality clause — any witness must be the least disagreement index. The uniqueness proof in the prose does not appeal to "leastness" as an additional requirement; it derives uniqueness from the universal-agreement conjunct alone. So "unique" is sufficient; "unique least" is tautological against the stated conjunction.

### TA0 re-export adds no content beyond TumblerAdd's postconditions
**Class**: OBSERVE
**Foundation**: n/a
**ASN**: TA0 (WellDefinedAddition): *"TA0 exports TumblerAdd's first two postconditions as a single labelled well-definedness fact. Proof. Immediate from TumblerAdd's first two postconditions..."*
**Issue**: TA0's entire content is a re-export of two items already in TumblerAdd's postcondition list with identical preconditions. If the downstream citation pattern prefers a single named fact over a pair of postcondition references, the redundancy is justified; otherwise it duplicates claim surface without strengthening anything.

VERDICT: OBSERVE

## Result

Regional review converged after 1 cycles.

*Elapsed: 281s*
