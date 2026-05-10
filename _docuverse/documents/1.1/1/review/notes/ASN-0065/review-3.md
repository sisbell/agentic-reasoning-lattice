# Review of ASN-0065

## REVISE

### Issue 1: 3-cut worked example claims three canonical blocks; there are four
**ASN-0065, Worked Example: 3-Cut Pivot**: "The new canonical decomposition has three blocks: ([1,1], A, 1), ([1,2], D, 1), ([1,3], B, 2)."
**Problem**: These three blocks cover positions [1,1]–[1,4] (total width 4), but V_S(d) has 5 positions. Position [1,5] → E (exterior, unchanged by R-EXT) is missing. C + 1 = 3.0.1.0.1.4 ≠ E = 5.0.2.0.1.2, so ([1,3], B, 2) does not extend to [1,5]. The block ([1,5], E, 1) is a fourth maximal run.
**Required**: State the canonical decomposition as four blocks: {([1,1], A, 1), ([1,2], D, 1), ([1,3], B, 2), ([1,5], E, 1)}.

### Issue 2: Misidentified cut position in 3-cut block narrative
**ASN-0065, Worked Example: 3-Cut Pivot**: "The cut at [1,4] split the original block β₁ into ([1,1], A, 1) and ([1,2], B, 2)"
**Problem**: β₁ = ([1,1], A, 3) has V-extent {[1,1], [1,2], [1,3]}. The position [1,4] is not in this block — it is the V-start of β₂ = ([1,4], D, 2). The split is caused by c₀ = [1,2], which is interior to β₁ at offset 1.
**Required**: Replace "The cut at [1,4]" with "The cut at [1,2]".

### Issue 3: Cross-ASN reference to non-foundation ASN-0061
**ASN-0065, Content Preservation**: "Unlike DELETE, which can remove all V-references to an I-address (causing orphaning per ASN-0061 D-ORPH)"
**Problem**: ASN-0061 is not a foundation ASN. Per self-containment rules, cross-ASN references to non-foundation ASNs are not permitted.
**Required**: Either remove the reference or restate the relevant property self-containedly (e.g., "DELETE can remove all V-references to an I-address, leaving content unreachable through any arrangement").

### Issue 4: Incomplete coupling constraint verification
**ASN-0065, R-CF(c)**: "J1 (ExtensionRecordsProvenance) is vacuously satisfied... J2 (ContractionIsolation) is vacuously satisfied... J3 (ReorderingIsolation) mandates exactly this: R' = R."
**Problem**: ValidComposite (ASN-0047) requires J0, J1, and J1' for the composite. The ASN verifies J1 and invokes J3, but omits J0 (AllocationRequiresPlacement: vacuous since dom(C') = dom(C)) and J1' (ProvenanceRequiresExtension: vacuous since R' = R). J2 is about elementary K.μ⁻ isolation and does not directly apply to the composite.
**Required**: Add one-line verifications: J0 is vacuous (no new content allocated, dom(C') \ dom(C) = ∅ by R-CF(a)), J1' is vacuous (no new provenance, R' \ R = ∅ by J3). Replace the J2 citation with a note that J2 does not apply (REARRANGE is K.μ~, not K.μ⁻).

### Issue 5: Open question about depth-2 generalization is already resolved
**ASN-0065, Open Questions**: "Can the depth-2 restriction (R-PRE clause iv, #v = 2) be relaxed to arbitrary V-position depths while preserving the commutativity of ordinal increment with the rearrangement permutation?"
**Problem**: D-CTG-depth (ASN-0036) proves that for depth m ≥ 3, all positions in a non-empty V_S(d) share components 2 through m − 1, reducing contiguity to contiguity of the last component alone — structurally identical to depth 2. D-SEQ then gives V_S(d) = {[S, 1, ..., 1, k] : 1 ≤ k ≤ n} at any depth. The displacement arithmetic is unchanged: only the last component varies. The generalization is immediate, not open.
**Required**: Either remove this open question or replace it with a note that the generalization follows from D-CTG-depth and D-SEQ, with the depth-2 restriction being a presentational simplification rather than a technical limitation.

### Issue 6: Vacuously true 3-cut/4-cut equivalence claim
**ASN-0065, after the Swap Postcondition**: "We observe the relationship between the two forms: when a 3-cut sequence (c₀, c₁, c₂) and a 4-cut sequence (c₀, c₁, c₁', c₂) with w_μ = c₁' − c₁ produce the same overall partition — two non-adjacent regions with no middle content — their postconditions coincide."
**Problem**: CS2 requires strict ordering of cut points, so w_μ ≥ 1 — the 4-cut form always has a non-empty middle region. The condition "produce the same overall partition" is unsatisfiable. The claim is vacuously true but reads as a substantive observation. The paragraph itself then notes the impossibility ("it cannot vanish entirely"), creating a structure of "if X then Y, but not X" that is confusing in a formal specification.
**Required**: Rephrase to state the structural observation directly: the 4-cut postcondition formulas (R-S1, R-S2, R-S3) reduce to the 3-cut formulas (R-P1, R-P2) when w_μ is set to zero in the expressions, but the preconditions prevent this case from arising. Or remove the paragraph, since the two forms are already clearly defined as distinct primitives.

## OUT_OF_SCOPE

### Topic 1: k-cut generalization for k > 4
**Why out of scope**: The natural class of permutations expressible by k cut points is a combinatorial question extending beyond this ASN's two-region transposition definition.

### Topic 2: Composability of rearrangements
**Why out of scope**: Whether the composition of two rearrangements is expressible as a single rearrangement, or whether sequences can produce arrangements unreachable by any single operation, is a question about the algebraic closure of the operation class — new territory.

### Topic 3: Front-end rendering of split link endsets
**Why out of scope**: How a rendering layer should present a link endset split across non-contiguous V-regions is a presentation concern, not a state-transition property.

VERDICT: REVISE
