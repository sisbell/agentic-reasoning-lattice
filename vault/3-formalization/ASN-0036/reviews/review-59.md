# Cross-cutting Review — ASN-0036 (cycle 2)

*2026-04-12 22:11*

Looking at this carefully, reading every property and tracing every dependency chain across the ASN.

### S8-depth correspondence runs apply V-position shift lemmas to I-addresses without a formal bridge

**Foundation**: OrdAddHom (OrdinalAdditionHomomorphism), OrdShiftHom (OrdinalShiftHomomorphism), OrdAddS8a (AdditionPreservesS8a), TumblerAdd (PositionAdvance, ASN-0034)
**ASN**: S8-depth (Fixed-depth V-positions), correspondence run definition — "for I-addresses, S7c guarantees element-field depth δ ≥ 2, so the subspace identifier E₁ is structural context outside the ordinal, and the shift acts on [E₂, ..., E_δ] without altering E₁"
**Issue**: The ASN builds a careful lemma chain — OrdAddHom → OrdAddS8a → OrdShiftHom — that formally establishes how tumbler addition interacts with the `ord`/`subspace`/`vpos` decomposition, proving subspace preservation and S8a preservation under shifts. This chain operates on V-positions (element-field tumblers with `zeros(v) = 0`). The correspondence run definition then defines `a + k = a ⊕ δ(k, #a)` for full I-addresses (four-field tumblers with `zeros(a) = 3`, three zero separators, and multi-field prefix structure). S8-depth claims subspace preservation for I-address shifts by prose argument ("TumblerAdd copies all earlier components unchanged"), but the lemma chain cannot be applied — OrdAddHom's `ord(v)` strips the first component of a V-position to get the within-subspace ordinal, while for a full I-address, stripping the first component yields `[N₂, ..., Nₐ, 0, U₁, ...]`, which is not an ordinal in any meaningful sense. The parallel claims for I-addresses — that `shift(a, k)` preserves `zeros(a) = 3`, preserves the element-field subspace identifier `E₁`, preserves T4 compliance, and that all zero separators remain in positions before `#a` — are structurally correct but follow from a different argument (TumblerAdd applied to multi-field addresses where the action point falls at the final element-ordinal component) than the one the lemma chain provides (TumblerAdd applied to element-field tumblers decomposed via `ord`/`subspace`/`vpos`). A formalizer following the lemma chain would have formal tools for V-position shifts but would need to construct a separate argument for I-address shifts from TumblerAdd's definition directly.
**What needs resolving**: Either extend the lemma chain to cover full I-addresses (e.g., a lemma establishing that `shift(a, k)` for `a` with `zeros(a) = 3` and `#fields(a).element ≥ 2` preserves `zeros`, T4 structure, and the element-field subspace identifier), or explicitly note in S8-depth that I-address shift properties follow from TumblerAdd's component-wise definition and S7c's `δ ≥ 2` guarantee via a direct structural argument distinct from the OrdAddHom/OrdShiftHom chain.

## Result

Converged after 3 cycles.

*Elapsed: 4844s*
