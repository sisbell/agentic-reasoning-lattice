# Regional Review — ASN-0034/T2 (cycle 1)

*2026-04-24 12:29*

### Gregory's `tumblercmp` reference imports undefined terminology into T2's proof
**Class**: OBSERVE
**Foundation**: (internal, T0 CarrierSetDefinition)
**ASN**: T2 (IntrinsicComparison), post-proof paragraph — "Gregory's `tumblercmp` delegates to `abscmp`, which performs a purely positional comparison: exponent first, then lexicographic mantissa slot-by-slot. No external state is consulted."
**Issue**: T0 fixes the carrier as nonempty finite sequences over ℕ — there is no "exponent" or "mantissa" in that carrier, and the ASN does not establish a correspondence between Gregory's `abscmp` representation and `(d₁, …, dₙ)`. Used as post-hoc corroboration inside a formal proof slot, this informal implementation reference dangles without the structural mapping that would make it meaningful. It does not affect the soundness of the preceding proof, but a precise reader reaches for definitions that are not in scope.

### Motivational prose in T2's proof region
**Class**: OBSERVE
**Foundation**: (internal)
**ASN**: T2, paragraph beginning "Span containment tests, link search, and index traversal all reduce to tumbler comparison…"
**Issue**: The paragraph motivates *why* intrinsic comparison matters (downstream consequences for decentralization) rather than advancing or closing the proof. It sits between the proof's ∎ and the formal contract, blurring the boundary between proof content and commentary. The content itself is a legitimate statement of consequence, so the observation is purely about placement.

### "(or m + 1)" / "(respectively k ≤ m)" parentheticals in T1 trichotomy Case 2
**Class**: OBSERVE
**Foundation**: (internal)
**ASN**: T1 proof, Case 2, reverse-witness exclusion — "case (ii) requires k = n + 1 (resp. m + 1), contradicting k ≤ n (resp. k ≤ m). … case (ii) requires k' = n + 1 (or m + 1), contradicting k' < k ≤ n (respectively k ≤ m)."
**Issue**: The "(resp. …)" / "(or …)" parenthetical tracks the `aₖ < bₖ` vs `bₖ < aₖ` sub-split, but mixes two parallelism markers ("resp." and "or") and in the second sentence abbreviates the right-hand contradiction to "k ≤ m" instead of the parallel "k' < k ≤ m". The intended branches can be reconstructed, but the reader must do the reconstruction — a consistent "(resp.)" usage with matched parentheticals would carry the parallelism without work.

VERDICT: OBSERVE

## Result

Regional review converged after 1 cycles.

*Elapsed: 535s*
