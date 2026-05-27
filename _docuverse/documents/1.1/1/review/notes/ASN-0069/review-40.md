# Review of ASN-0069

The ASN derives the fork operation with admirable rigor. Inductions are explicit (V1's IsDocument induction on emission count, V2's prefix induction with nested length sub-induction, V11's chain induction with two-stage premise discharge). Boundary cases are handled (V7 empty source, V7+V5 link-only source, V10 sibling forks, V11 fork chains). The ValidComposite★ verification walks through K.δ + K.μ⁺ + K.ρ × n sequentially, with sub-cases A/B of K.δ separately discharged. Design commitments (V4, V4b, V7) are explicitly flagged as not derivable from J4 alone.

I have found only minor wording issues; the mathematical content holds.

## REVISE

### Issue 1: V4's introduction wording conflates design commitment with derivation

**ASN-0069, §"The Arrangement Layer"**: "The fork installs the source's content-subspace V-positions and their I-addresses into `M'(d_new)`. We name what is established and then derive what follows."

**Problem**: V4 is later acknowledged as a design commitment of this ASN, "not derivable from J4 alone." The introductory wording "what is established" suggests V4 is a derived fact and obscures its design-commitment status from a reader encountering V4 for the first time.

**Required**: Either revise the introduction to make V4's design-commitment status explicit upfront (e.g., "We commit to a discipline and then derive what follows"), or move the design-commitment acknowledgment forward to immediately follow V4's statement rather than waiting until after the discussion of literal-inheritance justifications.

### Issue 2: V11 does not explicitly state that k ≥ 1

**ASN-0069, V11**: "For every chain of forks `d_src → d¹_new → d²_new → ... → d^k_new` starting from `Σ` (with `d⁰_new := d_src`), where each step `dⁱ⁻¹_new → dⁱ_new` is a fork composite..."

**Problem**: The chain syntactically requires at least one fork step (the induction base case handles k = 1). The k = 0 case (no forks, chain consists only of d_src) is not addressed; the conclusion at k = 0 would be vacuously true but the premise structure (premise at i = 1 with the "step 0's post-state denotes Σ" convention) only applies for k ≥ 1. The reader must infer this from the proof structure.

**Required**: Add an explicit "k ≥ 1" to V11's quantifier range, or note in the lemma statement that the chain length is at least 1.

### Issue 3: V11a's "sibling-stream index" phrasing is ambiguous

**ASN-0069, V11a**: "value `m ≥ 2` (the sibling-stream index of `dⁱ_new` within `A_v(dⁱ⁻¹_new)`'s enumeration) when step i is a subsequent fork"

**Problem**: Under T10a's enumeration convention (`tₙ₊₁ = inc(tₙ, 0)`, with `t₀` the base address), the 0th emission `inc(dⁱ⁻¹_new, 1)` has value 1 at position `#dⁱ⁻¹_new + 1`; the 1st emission has value 2; the nth has value n+1. So under 0-based indexing the *index* and the *value at position* differ by 1; under 1-based indexing they coincide. The phrasing identifies them without specifying which convention applies. The math is correct (m ≥ 2 in either interpretation), but the identification of "sibling-stream index" with "value m" is loose.

**Required**: Either fix the indexing convention explicitly (e.g., "the 1-based sibling-stream index" or "one greater than the 0-based index"), or rephrase to characterize m by its construction (e.g., "value `m` is the result of applying the inc(·, 0) operation `m − 1` times to the value 1 placed at position `#dⁱ⁻¹_new + 1` by `inc(dⁱ⁻¹_new, 1)`").

## OUT_OF_SCOPE

The Open Questions section correctly identifies several topics as future ASN work: concurrent fork handling, fork discoverability from the source, snapshot vs. living fork distinction, fork of a transcludent source, fork size bounds, version-space presentation, and referential validity through deletion. These are properly excluded from this ASN's scope.

VERDICT: REVISE
