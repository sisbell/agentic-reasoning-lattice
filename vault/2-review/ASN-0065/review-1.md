# Review of ASN-0065

## REVISE

### Issue 1: Empty μ claim contradicts strict ordering requirement
**ASN-0065, The 4-Cut Swap (final paragraph)**: "When μ is empty (c₁ = c₂, so w_μ = 0), the swap reduces to: β moves to [c₀, c₀ + w_β), α moves to [c₀ + w_β, c₃)."
**Problem**: CS2 requires strictly ordered cut positions: c₀ < c₁ < ... < c_{n−1}. For n = 4 this demands c₁ < c₂, which gives w_μ ≥ 1. The condition c₁ = c₂ is unreachable under the stated precondition. The entire paragraph describes an impossible case.
**Required**: Delete the paragraph, or rephrase it as a remark about the relationship between the two forms — e.g., "When separate 3-cut and 4-cut sequences produce the same partition (two non-adjacent regions with no middle), the postconditions coincide." Do not assert that c₁ = c₂ is possible within a valid 4-cut sequence.

### Issue 2: Non-foundation cross-ASN reference
**ASN-0065, State and Vocabulary**: "We adopt the ordinal extraction machinery from ASN-0061." and "As in ASN-0061, we restrict to depth-2 V-positions."
**Problem**: ASN-0061 is not a foundation ASN. The review standard requires each ASN to be self-contained, with cross-references permitted only to verified foundation ASNs (0034, 0036, 0047, 0053, 0058). The definitions of ord(v) and vpos(S, o) are already provided inline, so no content is missing — only the attribution creates the dependency.
**Required**: Remove "from ASN-0061" and "As in ASN-0061." Let the inline definitions and the depth-2 restriction stand on their own.

### Issue 3: No concrete worked example
**ASN-0065, throughout**: The ASN defines postconditions abstractly and verifies them symbolically. No specific numerical scenario is computed.
**Problem**: The review standard requires at least one concrete example verifying the key postconditions. A natural candidate: a 3-cut pivot on a 5-position document showing the exact V-to-I mapping before and after, checking R-P1, R-P2, R-EXT, and R-CP against the result. A 4-cut example would additionally verify R-S1/R-S2/R-S3 and would make the 4-cut implementation discrepancy immediately visible (the correct displacement places α at a different position than the implementation's diff[1] would).
**Required**: Add at least one worked example with explicit tumbler values for V-positions and I-addresses, tracing each postcondition clause.

### Issue 4: R-SPERM proof omits case verification
**ASN-0065, R-SPERM — SwapPermutation**: "Proof. By case verification against R-S1, R-S2, R-S3, R-EXT — each case is a direct substitution. Injectivity and surjectivity follow from the range partition. ∎"
**Problem**: The proof asserts four cases without showing any of them. R-PPERM (the 3-cut analogue) demonstrates the technique by verifying all three cases explicitly. R-SPERM should do the same for its four cases — they involve different postcondition clauses (R-S1 vs R-S2 vs R-S3 vs R-EXT) and different permutation branches. The standard requires each case when cases differ.
**Required**: Show the four case verifications. Each is one line (substitute the permutation branch into the corresponding postcondition clause and observe equality), so this adds roughly four lines to the proof.

## OUT_OF_SCOPE

### Topic 1: Involution and composition properties
The 3-cut pivot is an involution (self-inverse) only when w_α = w_β. When w_α ≠ w_β, applying the same pivot twice does not restore the original arrangement. The composition algebra of rearrangements — when two rearrangements compose to a single rearrangement, when they don't, and when a rearrangement is self-inverse — is genuinely new territory. The ASN correctly identifies this as an open question.
**Why out of scope**: This is rearrangement algebra, not a gap in the single-operation specification.

### Topic 2: Depth generalization beyond depth-2
The ASN restricts to depth-2 V-positions throughout and lists depth generalization as an open question. The commutativity of ordinal increment with the rearrangement permutation (used in R-BLK) relies on depth-2 arithmetic where ordinals are single natural numbers.
**Why out of scope**: The depth-2 restriction is explicitly stated and the generalization requires new machinery (multi-component ordinal displacement), not a fix to the current ASN.

VERDICT: REVISE
