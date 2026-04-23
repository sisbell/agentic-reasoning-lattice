# Regional Review — ASN-0034/TA-PosDom (cycle 1)

*2026-04-23 01:05*

### Substitution of equals under `<` — document-level inconsistency
**Class**: OBSERVE
**Foundation**: (internal) NAT-zero prose vs. NAT-order's stated properties
**ASN**: Several proofs rely on substituting equals under `<` as a silent inference step:
- ActionPoint uniqueness: *"substituting `m₁` for `m₂` in `m₁ < m₂` gives `m₁ < m₁`"* and *"substituting `m₁` for `m₂` in `m₂ < m₁`"*
- T1(c) case `k₂ < k₁`: *"the second substitutes `k₁` for `n` in `n < k₂` to yield `k₁ < k₂`"*
- T1(c) sub-case (ii, ii): *"we derive `m < n` (via NAT-order transitivity or substitution)"*
- TA-PosDom Case `#z ≥ k`: *"composing with `0 < 1` via NAT-order transitivity (strict disjunct) or substitution (equality disjunct) yields `0 < tₖ`"*

Yet NAT-zero's proof prose explicitly disclaims this step: *"this route avoids substituting equals under `<`, a step not among NAT-order's stated properties."*
**Issue**: The NAT-zero disclaimer tells the reader that substitution of equals under `<` is a step not provided by NAT-order; four other proofs then use exactly that step without citation. Either the disclaimer is overstated (substitution of equals is Leibniz-inherited from `=` in the ambient register and should be taken as available throughout) or the disclaimer is correct and those four proofs have an ungrounded step. The document should take one stance consistently.

### T1(b) Case 3 — redundant detour through `m ≠ n`
**Class**: OBSERVE
**Foundation**: n/a
**ASN**: T1(b) Case 3: *"Both clauses force `m ≠ n`: (β) gives `m + 1 ≤ n`, hence `m < n`…; (γ) gives `n < m` symmetrically. … NAT-order's trichotomy at `(m, n)` resolves `m ≠ n` into `m < n ∨ n < m`."*
**Issue**: The proof derives `m < n` (from β) or `n < m` (from γ) **directly**, then weakens that to `m ≠ n` and re-derives the disjunction via trichotomy. The trichotomy appeal is redundant — the branch that produced `m ≠ n` already carries the strict inequality needed for the next step. Not incorrect, just a reasoning detour.

### Pos-not-t>0 note contains a claim about an outside relation
**Class**: OBSERVE
**Foundation**: TA-Pos
**ASN**: *"Note on notation (outside the formal contract) … the length-1 tumbler `0` is a proper prefix of the length-2 tumbler `0.0`, and under the prefix rule of that ordering `0 < 0.0`, so `0.0 > 0` even though `Zero(0.0)` holds."*
**Issue**: The example `0 < 0.0` references T1's prefix rule and presupposes that both `0` and `0.0` are elements of `T`. This is fine as motivation, but the note is careful to say "outside this region" — worth noting that the exemplification does use T1 machinery defined in this very ASN, so the note is internally demonstrable rather than depending on claims elsewhere.

VERDICT: OBSERVE

## Result

Regional review converged after 1 cycles.

*Elapsed: 174s*
