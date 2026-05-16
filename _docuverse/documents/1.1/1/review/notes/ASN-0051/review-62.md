# Review of ASN-0051

## REVISE

### Issue 1: SV11 attainment witness gap for (m ≥ 3, p = 2)

**ASN-0051, SV11 attainment scope summary**: "The witnessed attainment scope spans four configurations: ... (iii) `(m ≥ 2, p = 2)` with the two blocks having overlapping I-extents and `min_k n_k ≥ 2m − 1` via the multi-block overlap witness above"

**Problem**: The concrete multi-block overlap witness exhibited covers m = 2 only (10 sibling addresses, 15 V-positions, two-span endset). The prose that follows says "For m ≥ 3, the same nesting pattern is structurally admissible..." but does not exhibit a concrete (B, e). The "structurally admissible but not witnessed in this ASN" disclaimer is explicitly applied to "(m ≥ 3, p ≥ 3)" only — not (m ≥ 3, p = 2). The summary claim "witnessed attainment scope spans four configurations" therefore overstates what is concretely witnessed: it nominally includes (m ≥ 3, p = 2) but no witness is exhibited.

**Required**: Either (a) restrict (iii) to "(m = 2, p = 2)" and explicitly extend the structurally-admissible-but-unwitnessed marker to "(m ≥ 3, p = 2)", or (b) exhibit a concrete (m = 3, p = 2) witness. A natural witness extends the (m = 2, p = 2) construction: with the same arrangement (10 siblings, 15 V-positions, blocks β₁ at size 10 and β₂ at size 5), three single-element spans `(a₆, a₇ ⊖ a₆)`, `(a₈, a₉ ⊖ a₈)`, `(a₁₀, a₁₁ ⊖ a₁₀)` give β₁-offsets {5, 7, 9} (non-adjacent in β₁'s 10-offset extent) and β₂-offsets {0, 2, 4} (non-adjacent in β₂'s 5-offset extent), realizing m·p = 6 fragments. This needs verification of `min_k n_k = 5 ≥ 2m − 1 = 5` (tight at β₂), discharging the structural-attainability condition.

### Issue 2: Ambiguity in "intermediate state" terminology in Worked Example

**ASN-0051, Worked Example, Step 1**: "The intermediate state is: `M_int(d) = {v₁ ↦ a₁, v₂ ↦ a₂, v₃ ↦ a₄, v₄ ↦ a₅, v₅ ↦ a₃}`"

**Problem**: The label "M_int(d)" denotes the *post-K.μ~* state (intermediate between Σ and the final Σ' of the larger composite). But K.μ~ itself decomposes into K.μ⁻ + K.μ⁺ internally, with its own intermediate state (post-K.μ⁻, pre-K.μ⁺) where dom is contracted. SV5's "Composite-level scope of SV5" paragraph explicitly references a *different* intermediate state Σ_int where `ran(M_int(d)) ⊊ ran(M(d))`. The same name "intermediate" applied to two distinct states across a few paragraphs invites confusion, particularly when the SV14(d) witness — extending the Worked Example — uses Σ_int to refer to the post-K.μ~ state too. Both intermediate states are mathematically well-defined and the surrounding prose disambiguates in each location, but a reader carrying SV5's "intermediate" semantics into the Worked Example sees a contradiction (the worked example's M_int has full domain; SV5's Σ_int has contracted domain).

**Required**: Rename the Worked Example's post-K.μ~ state to make the composite-vs-elementary distinction explicit (e.g., M_after-step-1, or M_after-reorder), reserving "intermediate" for the SV5-style elementary-stage state inside K.μ~.

### Issue 3: SV11 attribution paragraph should acknowledge sharing's quantitative footprint more directly

**ASN-0051, SV11 worked example, "Attribution of the 4 → 2 gap" paragraph**: "The entire strictness gap is attributable to mechanism (b) (within-block adjacency coalescence) and to mechanism (b) only..."

**Problem**: The attribution is correct (each block's 2 → 1 coalescence is purely mechanism (b); cross-block I-address sharing affects only |π| via set-union idempotence, not within-block fragment counts). But the next sentence — "its only quantitative footprint is inflating the summed term width to 6 (vs |π_text(e, d)| = 4 distinct I-addresses)" — buries an important reader-checkable identity: in the non-injective case, the sum of decomposition-term cardinalities exceeds the cardinality of π_text by exactly the count of multiply-mapped I-addresses across blocks. Here, {a₂, a₃} each appear in two blocks, contributing 2 to the inflation (6 − 4 = 2). The text gives the numerical comparison but not the structural relation.

**Required**: Add a one-line identity stating that `Σ_k |term_{j,k}| − |π_text| = Σ_a (m_a − 1) ⋅ |spans covering a|` where m_a is the multiplicity of a across blocks, so that the relationship between sharing multiplicity and cardinality inflation is readable. Without this, the worked example exhibits a numerical fact without making its general form available.

### Issue 4: SV11 attribution to "mechanism (b) only" risks overgeneralization

**ASN-0051, SV11 worked example, attribution paragraph**: "*Attribution of the 4 → 2 gap.* The entire strictness gap is attributable to mechanism (b) (within-block adjacency coalescence) and to mechanism (b) only, applied independently in each block..."

**Problem**: The attribution holds for this specific two-span witness, but the prose phrasing suggests a general claim that non-injective sharing never participates in the fragment-count gap. This is correct in the precise sense that fragment counts are computed per-block, but the rendering implies a stronger separation than holds: a witness that exhibits cross-block sharing AND within-block adjacency could not separate the two as cleanly. The "applied independently in each block" framing further suggests that mechanism (b) operates without reference to the cross-block configuration, which is true here but not made independent of the witness.

**Required**: Tighten the attribution to "in this witness, the 4 → 2 gap arises entirely from mechanism (b) within each block; non-injective cross-block sharing affects |π| via union idempotence but contributes no within-block coalescence", to avoid the reader inferring a global separation theorem from a witness-specific observation.

### Issue 5: SV11 disjoint-pair T-interleaving sub-case verbosity has unaddressed clarity issues

**ASN-0051, SV11 disjoint-pair case, four-case structural lemma**: The lemma identifies T-interleaving as case (IIIb) with j* < n_{k₁}.

**Problem**: The "Uniformity of the bracket across β_{k₂}" paragraph establishes that the same j* serves every f ∈ β_{k₂}, but the argument leans on β_{k₂}'s elements sharing a common prefix q_{k₂} on positions 1..#f − 1 *and* on the first #e positions of each f equaling exactly e_{k₁,j*}. The implication "the first #e positions of every f ∈ β_{k₂} are themselves a prefix of q_{k₂} (positions 1..#e ⊆ 1..#f − 1 since #f > #e ≥ #e)" contains the typo "#f > #e ≥ #e" — the right inequality is vacuous (#e ≥ #e is reflexive). The intended argument is `1..#e ⊆ 1..#f − 1` requires `#e ≤ #f − 1`, equivalently `#f > #e`. The vacuous tail makes the chain hard to parse.

**Required**: Replace `#f > #e ≥ #e` with `#f > #e ⟹ #e ≤ #f − 1`, or simply `#f > #e`. The redundant chain serves no logical function.

### Issue 6: SV13 omits a corollary for bilateral vitality

**ASN-0051, SV13 (SurvivabilityTheorem)**: The theorem synthesises projection, location, discovery, content, and partial survival, but does not state how bilateral vitality (introduced earlier with explicit text "for downstream consumers") behaves under each transition.

**Problem**: The ASN introduces bilateral vitality with stated downstream consumers in mind ("link-semantics ASNs and link-discovery policy notes that require the literal-Nelson reading"). The "Consumer note" disclaims internal use, but SV13 is the canonical entry point for cross-ASN citation — the synthesis where a downstream consumer would expect to find the bilateral-vitality survival statement. The corollary itself is one-line (bilateral vitality is preserved by SV2/SV4/SV5/SV5b, and SV3 can falsify the predicate when either side's last contributing V-position is removed), but its absence from SV13 forces every downstream consumer to re-derive it.

**Required**: Add a sub-clause to SV13(e) — or a separate SV13(h) — stating that bilateral vitality survives extension/reordering and may be lost only when contraction removes the last V-position whose I-address is in coverage(F) or coverage(G). The wp form already developed for π extends directly to bilateral vitality by conjunction across slots.

### Issue 7: Worked Example's K.μ~ admissibility in Step 1 not fully discharged

**ASN-0051, Worked Example, Step 1**: "Apply the bijection ψ on dom(M(d)) = {v₁, v₂, v₃, v₄, v₅} given by ψ(v₃) = v₅, ψ(v₄) = v₃, ψ(v₅) = v₄, ψ(v_i) = v_i for i ∈ {1, 2}..."

**Problem**: K.μ~ in ASN-0047 is the distinguished composite K.μ⁻ + K.μ⁺. The K.μ⁻ stage of this particular ψ must remove the V-positions whose V→I assignment changes — namely v₃, v₄, v₅ — and K.μ⁻'s D-SEQ admissibility requires the removed set to be an upward tail per subspace. The set {v₃, v₄, v₅} *is* the upward tail of V_{s_C}(d) in this case (after v₁, v₂), so K.μ⁻ can fire. Then K.μ⁺ adds v₃ ↦ a₄, v₄ ↦ a₅, v₅ ↦ a₃ — this must satisfy D-CTG/D-MIN, which it does. The Worked Example does not exhibit this internal decomposition, treating K.μ~ as a single step with the resulting M_int(d) directly. This is fine if K.μ~ admissibility is being read at the composite level, but Section "Step 1" labels it "K.μ~ (the distinguished K.μ⁻ + K.μ⁺ composite, ASN-0047)" — invoking the composite structure without verifying its admissibility.

**Required**: Add a one-line verification that the K.μ⁻ stage of K.μ~ removes a D-SEQ-admissible upward tail in this case (the set {v₃, v₄, v₅}), so the composite is enabled. The text mentions "K.μ⁻ removes from the maximum end of V_S(d) only" elsewhere in the same Worked Example for Step 2 — apply the same check at Step 1.

## OUT_OF_SCOPE

No items. The ASN appropriately defers type semantics, link discovery policy, version derivation, and replication to future ASNs through its Open Questions section. Several Open Questions (resolution under within-document sharing, bilateral vitality across forks) are genuine extensions rather than gaps in the present ASN.

VERDICT: REVISE
