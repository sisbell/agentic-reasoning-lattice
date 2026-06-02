# Review of ASN-0070

This is a carefully constructed ASN. The core inverse-image definition (F0), the V-restricted denotation, the canonical-form uniqueness derivation, the wp analysis, the worked example (with four configurations exercising soundness, multiplicity, no-reach, and state-dependence), and the F-* derived properties are all rigorous and complete. Edge cases — empty endsets, undefined subspace depth, partial reach, multiplicity, cross-subspace coverage — are handled explicitly. I verified Step 1's case analysis (`k < m` infinite, `k = m` finite with both inclusions), the consecutivity characterization's induction, and the left/right inter-component closure arguments; all hold. The two issues below are presentational/citation accuracy, not correctness.

## REVISE

### Issue 1: F-contig lacks a formal contract block

**ASN-0070, "Computation via Decomposition" and "Claims Introduced" table**: F-contig is listed in the final claims table as a LEMMA ("introduced") and is fully proved inline (ending in ∎), but unlike every other introduced lemma (F-det, F-sound, F-complete, F-empty, F-multi, F-slot, F-origin, F-persist, F-state, F-multidoc), it has no Preconditions/Postcondition/Depends/Frame contract block in the "Derived Properties" section.

**Problem**: Inconsistent presentation. A reader scanning the Derived Properties section for the catalogued lemmas will not find F-contig, yet it is cited in the table and relied on by the decomposition computation. Its dependencies (M1, T12 order-convexity) are stated in prose but not in the structured Depends form used everywhere else.

**Required**: Give F-contig a formal contract block matching the other F-* lemmas (Preconditions: mapping block `β = (v, a, n)`, endset I-span `σ`; Postcondition: `I(β) ∩ ⟦σ⟧` is empty or a contiguous sub-progression; Depends: M1 ASN-0058, T12 ASN-0034; Frame: state-pure), or place it within the Derived Properties section.

### Issue 2: Incorrect citation name for the home definition

**ASN-0070, F-origin and F-multidoc**: "`home(M(d)(v))` for link addresses (Definition LinkHome, ASN-0043)" and "the home document `home(ℓ)` ... (Definition LinkHome, ASN-0043)".

**Problem**: ASN-0043 defines this as "home(a) — Home (DEF, definition)". There is no definition named "LinkHome" in ASN-0043. The cite names a definition that does not exist under that label.

**Required**: Cite the foundation by its actual name — `home` / "Home" (Definition Home, ASN-0043) — for accuracy.

## OUT_OF_SCOPE

(none — the ASN correctly confines itself to the query operation and defers partial-reach reporting, transclusion-lineage relationships, and concurrency semantics to the Open Questions.)

VERDICT: REVISE
