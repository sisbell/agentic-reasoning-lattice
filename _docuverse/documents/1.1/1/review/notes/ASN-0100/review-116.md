# Review of ASN-0100

This is a thorough, mostly rigorous specification. The forward verification (per-state invariants at each intermediate, S2/S3★/D-SEQ★/S8★ all discharged), the wp analysis (genuinely non-trivial cases), the concrete worked examples (including the m_C = 3 off-prefix case), and the uniqueness-of-Σ' argument all meet the depth bar. The cross-references are all to foundation ASNs, so Standard 7 is satisfied. My findings are anti-bloat (the note carries `review-mode.anti-bloat`) plus one clarity item.

## REVISE

### Issue 1: Self-admitted duplicate provenance discharge

**ASN-0100, §A Worked Example (empty-document case)**: "*Discharge of J0, J1★, J1'★ (empty case).* The coupling logic is exactly the interior case (*Provenance discharge* above); only the delta differs."

**Problem**: The J0/J1★/J1'★ discharge is argued three times — the interior worked example, the empty worked example, and the general §Provenance section. The empty example, by its own wording, restates mechanics it has just declared identical to the interior case. The only content that is not a restatement is the delta ("no K.μ⁻ fires, pre-state `ran(M(d)) = ∅`, so all three Insertion images are range-new"). The precise reader has to re-read identical coupling logic to extract one sentence of new information.

**Required**: Collapse the empty example's coupling paragraph to a one-line pointer plus the delta. The general proof lives in §Provenance; the worked examples should only state what is *case-specific*.

### Issue 2: Essay-form narration of the I3 relationship, deferred-to from multiple sections

**ASN-0100, §Discovering the Three Effects → "Identification with the foundation's post-insertion shift"**: "I3 *vacates* the gap `[p, shift(p, n))` (I3-V…) without filling it, whereas INSERT fills exactly that gap … Hence `M'(d)` decomposes as (I3's post-insertion shift arrangement on Left ∪ Shifted-right) together with (the Insertion placement filling I3's vacated gap), and on Left ∪ Shifted-right the post-state arrangement *coincides* with I3's."

**Problem**: The load-bearing fact — "on Left ∪ Shifted-right, INSERT's `M'(d)` agrees with the I3 arrangement" — is then deferred to as "(§Effect Three)" from three separate invariant sections (§Arrangement functionality, §Referential integrity, §Post-state V-position well-formedness), each re-asserting "these coincide with the post-insertion shift arrangement." This is the multiple-paragraphs-defer-to-the-same-location pattern. The narration also re-derives the vacated-interval last components, which the per-region effect clauses already fix. The identification is real and reusable, but it is being carried as prose rather than as a named handle.

**Required**: State the identification once as a named sub-lemma (or fold it into INS.M-shift's claim row: "INS.M-shift coincides with I3 restricted to Left ∪ Shifted-right"), and have the invariant sections cite the handle rather than re-narrate the coincidence. Drop the redundant last-component re-derivation in the narrative paragraph.

### Issue 3: "coincides with I3's arrangement" is informal where I3 is a relational postcondition, not an object

**ASN-0100, §Verifying the Invariants (functionality, refint, well-formedness)**: repeated phrasing "their internal functionality is I3-S2 … the post-insertion shift arrangement is a function."

**Problem**: I3 (ASN-0082) is a postcondition schema; "I3's arrangement" vacates the gap, so its domain is strictly *different* from INSERT's `M'(d)` (which fills the gap). The lemmas I3-S2/I3-S3/I3-VP/I3-fin are about an arrangement satisfying I3's postconditions; applying them to INSERT's `M'(d)` is sound only because INSERT's restriction to Left ∪ Shifted-right is *pointwise equal* to the I3-specified mappings, with the Insertion region handled by separate cross-region disjointness. The text gestures at this ("on Left ∪ Shifted-right … coincides") but never states the restriction-equality step explicitly, so the lemma transport reads as if I3-S2 directly governs INSERT's full arrangement.

**Required**: Make the transport explicit once: "INSERT's `M'(d) ↾ (Left ∪ Shifted-right)` is pointwise identical to the I3-specified mappings; therefore I3-S2/S3/VP/VD/fin apply to that restriction, and full-arrangement properties follow by combining with the Insertion region." One sentence discharges the gap that the current "coincides" language leaves implicit across three sections.

## OUT_OF_SCOPE

None. The ASN bounds its scope correctly (link-subspace insertion, COPY, DELETE, versioning, replication are all explicitly excluded and not improperly claimed).

VERDICT: REVISE
