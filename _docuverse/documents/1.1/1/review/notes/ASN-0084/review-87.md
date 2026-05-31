# Review of ASN-0084

## REVISE

### Issue 1: Worked Example 1 merge check misstates the disqualifying condition

**ASN-0084, "Worked Example: 3-Cut Pivot on a 5-Position Document," Merge check**: "([1,3], B, 2) and ([1,5], E, 1) are not V-adjacent (3 + 2 = 5 ✓ for V-adjacency, but check I-adjacency: B + 2 = 3.0.1.0.1.0.1.4 ≠ E = 5.0.2.0.1.0.1.2, different origins)."

**Problem**: The pair *is* V-adjacent — the run ([1,3], B, 2) has V-extent {[1,3],[1,4]}, and v₂ = [1,5] = [1,3] + 2 = v₁ + n₁, exactly the Merge definition's V-adjacency condition (and the parenthetical itself marks "5 ✓ for V-adjacency"). The lead clause "are not V-adjacent" directly contradicts its own parenthetical. The runs fail to merge because they are **not I-adjacent** (B + 2 ≠ E), not because of V-adjacency. The conclusion (no merge) is correct; the stated reason is wrong.

**Required**: Replace "are not V-adjacent" with "are V-adjacent (3 + 2 = 5) but not I-adjacent," matching the phrasing used correctly in every other worked example's merge check.

### Issue 2: EXT-VAC asserts `c₀ ≤ [S, N+1]` without justification

**ASN-0084, "Consequences of R-PRE," Empty-exterior boundary cases**: "were ord(c_{n−1}) > N + 1, the position v = [S, N + 1] would satisfy subspace(v) = S ∧ #v = 2 ∧ c₀ ≤ v < c_{n−1} (since N + 1 < ord(c_{n−1}))..."

**Problem**: The parenthetical discharges only the upper conjunct `v < c_{n−1}`. The lower conjunct `c₀ ≤ v`, i.e. `ord(c₀) ≤ N + 1`, is asserted without proof, yet it is load-bearing for the contradiction with R-PRE(iv). The fact is true but requires a step: Width positivity (just above) gives w_α ≥ 1, so α ⊆ [c₀, c₁) ∩ V_S(d) is non-empty, forcing ord(c₀) ≤ N < N + 1.

**Required**: Add the one-line justification of `ord(c₀) ≤ N` (via Width positivity) so the `c₀ ≤ v` conjunct is discharged rather than assumed.

### Issue 3: R-BLK Phase 3 restates the R-COMM→contiguity argument in three overlapping passages

**ASN-0084, R-BLK, Phase 3 (Reassemble)**: paragraph B — "The I-start and width of each run are preserved because... by R-COMM, π commutes with ordinal shift within each region — so the consecutive V-positions vₖ, vₖ + 1, ..., map to consecutive V-positions π(vₖ), π(vₖ) + 1, ..., keeping the width intact." — and paragraph C ("Contiguity of reassembled runs") — "By R-COMM applied with the same-region precondition discharged (π(vⱼ + k) = π(vⱼ) + k), consecutive V-positions in the original run map to consecutive V-positions, so each reassembled run... occupies a contiguous V-position range."

**Problem**: Paragraphs B and C derive the identical claim — R-COMM yields π(vⱼ+k)=π(vⱼ)+k, hence consecutive V-positions map to consecutive V-positions and width is preserved — in different words, with the preceding paragraph already establishing the per-region commutation identity. This is the "two paragraphs say the same thing" pattern flagged for this note; the reader must reconcile three restatements of one inference.

**Required**: Collapse the width-preservation/contiguity derivation into a single passage citing R-COMM once. (A secondary instance of the same accretion: "extends OrdinalShift's domain from ℕ⁺ to ℕ" is restated in the Identification paragraph and again under Notation — keep one.)

## OUT_OF_SCOPE

### Topic 1: Composition of multiple rearrangements
**Why out of scope**: Whether two REARRANGE_K operations compose into a single rearrangement is correctly deferred to the Open Questions; it is new territory, not a defect in the single-operation semantics established here.

### Topic 2: Recovery of the canonical (maximal) partition from B'
**Why out of scope**: R-BLK explicitly proves only that B' is *a* valid partition (not necessarily maximal), and the merge-to-canonical process is posed as an Open Question. The ASN's claim is correctly scoped; the iterated-merge confluence question belongs to a future ASN.

VERDICT: REVISE
