# Regional Review — ASN-0034/TA-dom (cycle 1)

*2026-04-23 04:14*

### Defensive typing paragraph in TA-Pos

**Class**: OBSERVE
**ASN**: TA-Pos (PositiveTumbler), second sentence of its defining paragraph: "The bound variable `i` is typed to ℕ because... `tᵢ` itself is a natural number by T0's carrier, the literal `0` against which it is compared is the `0 ∈ ℕ` posited by NAT-zero, the numeral `1` bounding the quantifier range is the `1 ∈ ℕ` posited by NAT-closure, and the relation `≤` ... is the non-strict companion of `<` defined on ℕ by NAT-order; the equality `tᵢ = 0` and the bounding inequalities `1 ≤ i ≤ #t` in the two clauses are thus well-typed within ℕ, and the negation `¬` ... is classical propositional negation applied to that equality, requiring no additional symbol on ℕ."
**Issue**: The paragraph enumerates the type of every symbol (`i`, `tᵢ`, `0`, `1`, `≤`, `=`, `¬`) as a defensive justification rather than advancing the claim. This reads as reviser drift — prose added in response to prior typing concerns that explains why each axiom is needed rather than using it. The formal contract's `(A t ∈ T :: …)` header already establishes the typing discipline.

### Redundant trichotomy invocation in T1 Case 3

**Class**: OBSERVE
**ASN**: T1 (LexicographicOrder), proof part (b), Case 3: "Both clauses force `m ≠ n`: (β) gives `m + 1 ≤ n`, hence `m < n` ...; (γ) gives `n < m` symmetrically. So `a ≠ b` by T3. NAT-order's trichotomy at `(m, n)` resolves `m ≠ n` into `m < n ∨ n < m`."
**Issue**: The case split has already committed to (β) or (γ); each clause directly yields `m < n` or `n < m`. Invoking trichotomy to re-derive the split is circuitous — the proof could go directly from the (β) branch to `m < n` and from the (γ) branch to `n < m` without laundering through `m ≠ n`.

### "Outside this region" ambiguity in TA-Pos notation note

**Class**: OBSERVE
**ASN**: TA-Pos, closing note: "The lexicographic ordering and its prefix rule alluded to here are supplied by claims outside this region and enter no obligation of TA-Pos."
**Issue**: T1 (LexicographicOrder), which defines `<` and its prefix rule, is defined *within this ASN*. "Outside this region" presumably means "outside the 'Zero tumblers and positivity' subsection," but the phrasing invites the reader to look for an external dependency that doesn't exist. The note is correct in spirit (TA-Pos does not depend on T1), but the locator is misleading.

VERDICT: OBSERVE

## Result

Regional review converged after 1 cycles.

*Elapsed: 285s*
