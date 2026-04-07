I'll read the ASN and foundation materials carefully.

# Integration Review of ASN-0047

## REVISE

### Issue 1: K.μ⁻ amendment missing from Properties Introduced table
**ASN-0047, Properties Introduced table**
**Problem**: The K.μ⁻ amendment (PerSubspaceContiguity) is listed in "Properties That Were Integrated" but has no entry in the Properties Introduced table. Both K.α amendment and K.μ⁺ amendment have entries; K.μ⁻ amendment does not.
**Required**: Add a registry entry for the K.μ⁻ amendment, parallel to the K.α and K.μ⁺ amendment entries.

### Issue 2: K.μ~ decomposition invalidated by K.μ⁺ amendment
**ASN-0047, Elementary transitions, K.μ~**: "When dom(M(d)) is non-empty, it decomposes into K.μ⁻ (removing all mappings) followed by K.μ⁺ (re-adding them at new positions)."
**Problem**: The K.μ⁺ amendment restricts K.μ⁺ to `subspace(v) = s_C`. When `dom(M(d))` contains link-subspace mappings, the amended K.μ⁺ cannot re-add them. The "remove all, re-add all" decomposition produces an `M'(d)` missing its link-subspace mappings, contradicting K.μ~'s definition (π bijects all of `dom(M(d))` onto `dom(M'(d))`). The intermediate-state verification also cites S3 (`ran(M(d)) ⊆ dom(C)`) rather than S3★ — incorrect in the extended state where `ran(M(d))` may include `dom(L)` addresses. The ExtendedReachableStateInvariants proof provides the correct analysis (link-subspace fixity forces K.μ⁻ to remove only content-subspace positions), but the original K.μ~ paragraph now states a decomposition that is invalid for any arrangement containing link-subspace mappings.
**Required**: Update the K.μ~ decomposition to: K.μ⁻ removes content-subspace mappings (link-subspace preserved by fixity), K.μ⁺ re-adds content-subspace mappings at new positions. Update the intermediate-state verification to use S3★. At minimum, add a forward reference noting that the extended analysis in ExtendedReachableStateInvariants refines this decomposition for arrangements with link-subspace mappings.

### Issue 3: Incorrect inclusion chain in Consequence for J4
**ASN-0047, Amendments to existing transitions, Consequence for J4**: "ran(M'(d_new)) ⊆ ran(M(d_src)) ⊆ dom(C) by J4's definition, so P7 compatibility is maintained."
**Problem**: The second inclusion `ran(M(d_src)) ⊆ dom(C)` is false in the extended state. When `d_src` has link-subspace mappings, `ran(M(d_src))` includes link addresses in `dom(L)`, and `dom(L) ∩ dom(C) = ∅` by L14. The conclusion (`ran(M'(d_new)) ⊆ dom(C)`) is correct but the intermediate step is not.
**Required**: Derive the conclusion directly: J4's K.μ⁺ step creates only content-subspace V-positions (by the K.μ⁺ amendment), and S3★'s content clause gives `M'(d_new)(v) ∈ dom(C)` for each such `v`. Therefore `ran(M'(d_new)) ⊆ dom(C)` without routing through `ran(M(d_src))`.

### Issue 4: First worked example violates K.μ⁻ amendment
**ASN-0047, Worked example: fork with subsequent insertion, K.μ⁻ step**: "Remove the mapping at V-position [1,1]... dom(M₄(d₂)) = {[1,2], [1,3]}"
**Problem**: The K.μ⁻ amendment adds a D-CTG/D-MIN postcondition, and ExtendedReachableStateInvariants includes both in the authoritative invariant set. The deletion removes V-position [1,1] from {[1,1], [1,2], [1,3]}, producing {[1,2], [1,3]} with minimum [1,2] — violating D-MIN (which requires minimum [s_C, 1] = [1,1]). The amendment explicitly states contraction is constrained to "removal from the maximum end of V_S(d) or removal of all positions." Removing [1,1] is neither. The subsequent reorder step operates on a state with D-MIN broken.
**Required**: Change the deletion to remove from the maximum end — e.g., remove V-position [1,3], yielding {[1,1], [1,2]} which satisfies D-MIN. Update the reorder step to swap [1,1] and [1,2] instead of [1,2] and [1,3]. The example still demonstrates provenance divergence (R retains the stale entry for the removed content) equally well with a suffix removal.

VERDICT: REVISE
