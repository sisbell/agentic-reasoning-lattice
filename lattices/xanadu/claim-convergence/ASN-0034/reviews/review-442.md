# Regional Review — ASN-0034/T12 (cycle 1)

*2026-04-23 05:13*

### Case 3 of T1 Trichotomy skips the mirror via "by similar reasoning"
**Class**: REVISE
**Foundation**: T1 (LexicographicOrder), part (b) Trichotomy, Case 3.
**ASN**: After establishing the `m < n` branch in detail (witness `k = m + 1` for `a < b`, explicit exclusion of reverse via both T1(i) and T1(ii) clauses), the proof closes with: "If `n < m`, the mirrored argument gives `b < a`."
**Issue**: The `n < m` branch is not walked. It must both (1) produce a witness for `b < a` and (2) exclude a reverse witness for `a < b`. The mirroring is symmetric but non-trivial — the reverse-witness exclusion in the explicit branch relied on "case (ii) would require `n + 1 ≤ m`", which mirrors to "case (ii) would require `m + 1 ≤ n`", not a mere relabelling. Review discipline here forbids "by similar reasoning".
**What needs resolving**: Spell out the `n < m` branch: exhibit the witness `k = n + 1` for `b < a` via T1(ii) and explicitly rule out both clauses for a reverse witness of `a < b`, or justify the symmetry by a substitution argument that makes the correspondence mechanical.

### Meta-prose in TA0 and TA-strict introductions
**Class**: OBSERVE
**Foundation**: TA0, TA-strict.
**ASN**: "TA0 exports TumblerAdd's first two postconditions as a single labelled well-definedness fact." and "TA-strict exports TumblerAdd's ordering postcondition as a single labelled fact so downstream users (chiefly T12 span well-definedness) can cite one corollary rather than TumblerAdd's full postcondition list."
**Issue**: Defensive justifications explaining *why* the labelled export exists and listing its use-site, rather than stating what the claim asserts. Reviser-drift pattern: prose explaining the axiom's motivation rather than its content.

### Architectural-load-bearing aside after T1
**Class**: OBSERVE
**Foundation**: T1 (LexicographicOrder), post-proof paragraph.
**ASN**: "Nelson's assertion that the tumbler line is total ... is architecturally load-bearing. ... If two addresses were incomparable, the interval between them would be undefined, and the entire machinery of span-sets, link endsets, and content reference would collapse."
**Issue**: Essay content explaining downstream consequences of T1, not advancing the proof or the claim. Belongs (if anywhere) in the ASN's motivation, not in a formal contract's neighborhood.

### T5-reservation aside inside T12
**Class**: OBSERVE
**Foundation**: T12 (SpanWellDefinedness), after the proof.
**ASN**: "We reserve T5 for the distinct claim that *prefix-defined* sets are contiguous — a non-trivial property of the lexicographic order."
**Issue**: A disambiguation note about a claim not made here. Adds no reasoning to T12's postconditions.

### TA-strict lists TA0 as a dependency redundantly
**Class**: OBSERVE
**Foundation**: TA-strict (StrictIncrease), Depends list.
**ASN**: "TA0 (WellDefinedAddition) — membership `a ⊕ w ∈ T` so T1's ordering applies to the left-hand side."
**Issue**: TA-strict's proof is "immediate from TumblerAdd's ordering-guarantee postcondition `a ⊕ w > a`". If TumblerAdd commits to that ordering postcondition, it already commits — on its own contract — to the well-typedness of its two sides; citing TA0 to re-establish membership is a double citation of the same source.

VERDICT: REVISE

## Result

Regional review converged after 2 cycles.

*Elapsed: 523s*
