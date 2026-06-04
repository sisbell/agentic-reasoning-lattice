# Review of ASN-0087

This ASN is technically rigorous: the L1c chain construction is verified step-by-step with correct zero-count bounds, the invariant-preservation pass covers every conjunct of ASN-0047's ExtendedReachableStateInvariants, boundary cases (first vs. subsequent link, empty endset slots, reflexive endsets, `d_target ∉ dom(M)`) are handled, and it carries a concrete worked example plus non-trivial wp analysis. The prefix computations in the example check out. No correctness defects found.

The note carries the `review-mode.anti-bloat` classifier, and the findings below are accreted meta-prose, forward-reference clustering, and re-derivation of foundation guarantees.

## REVISE

### Issue 1: StandardAuthoring definition enumerates its downstream consumers
**ASN-0087, Inputs / "Standard authoring"**: "...and is the strongest hypothesis used in the wp reductions, the exclusion of reflexive endsets, and the vacuity of side effects on prior links' discoverability. Where this ASN cites 'under standard authoring'... we mean exactly this predicate."
**Problem**: A definition's introduction should advance its meaning, not inventory the sites that consume it. The use-site list and the closing "where this ASN cites..." pointer are the flagged "definition enumerates downstream consumers" pattern.
**Required**: Keep the predicate and the structural-vs-epistemic clarification; delete the consumer inventory and the citation-convention sentence.

### Issue 2: Multiple sections defer to the same downstream location (Reflexive Endsets / M-Reflexive)
**ASN-0087, wp section / Worked Example / Atomicity / M-DiscSymmetry**: "this structural exclusion is derived in *Reflexive Endsets* (M-Reflexive)"; "This is the M-Reflexive case; its derivation is in *Reflexive Endsets*"; "The reflexive case is treated in the 'Reflexive Endsets' section."
**Problem**: Four paragraphs in four sections forward-point to the same downstream derivation — the flagged "multiple paragraphs defer to the same downstream location" pattern. The deferrals compound; the reader bounces.
**Required**: State the reflexive result once (in Reflexive Endsets) and let the claim labels carry it; drop the repeated "derived below in X" prose.

### Issue 3: Σ_mid invariant re-verification re-derives K.λ's foundation guarantee
**ASN-0087, Atomicity, classes (α)/(β)/(γ)**: "The full per-state invariant set partitions into three classes by what they quantify over... inherited verbatim from Σ..."
**Problem**: `Σ_mid` is the post-state of the atomic substrate operation K.λ. ASN-0093/ASN-0047 already establish that K.λ preserves the per-state invariants on reachable states. Re-verifying L0, L1, L1c, L14, S3★, etc. at `Σ_mid` by hand re-proves a foundation guarantee. The load-bearing content here is only that `Σ_mid` is a complete reachable state where the link exists but is unplaced — that is one sentence.
**Required**: Replace the α/β/γ pass with a citation that `Σ_mid` is reachable and inherits ASN-0047's invariants from K.λ; retain only the discoverability-difference comparison between `Σ_mid` and `Σ'`, which is the genuinely new content.

### Issue 4: Duplicated composition sentence
**ASN-0087, Side Effects section** ("Composition of MAKELINK invocations preserves every per-state invariant: since `discoverable_from` is derived from `(L, M)`, preservation reduces to the per-step guarantees LP9, LP13, and L12.") **and M-PriorLinkDisc claim row** ("Composition across MAKELINK sequences preserves all per-state invariants (LP9, LP13, L12).")
**Problem**: The same statement appears twice in different words — the flagged "two paragraphs say the same thing" pattern.
**Required**: Keep it in one place (the claim row), remove the prose duplicate.

### Issue 5: wp enabledness/membership discussion carries procedural forward-pointers
**ASN-0087, Weakest Precondition section**: "Every wp expression below conjoins this predicate explicitly"; "Every wp expression below carries both explicitly"; "This membership clause keeps `discoverable_from` *defined*... it is distinct from `enabled(MAKELINK)`, which keeps the post-state from existing at all."
**Problem**: The enabled-vs-membership distinction is stated, then restated, then re-applied per case, plus two "every expression below..." forward inventories. The distinction is real but is delivered three times.
**Required**: State the enabledness convention and the membership/enabledness distinction once; let the two wp expressions stand without the "every expression below conjoins this" scaffolding.

### Issue 6: Claims-table rows have grown into paragraph-length derivation summaries
**ASN-0087, Claims Introduced (M-Inv-State, M-PriorLinkDisc, M-WP, M-Reflexive)**: e.g. M-Inv-State runs a full multi-clause classification ("...grouped by which frame supplies preservation: (i) *content-frame*... (ii) *entity-frame*... (iii) *document-set frame*...").
**Problem**: A claims table's Statement column is a structural slot for terse statements; these rows reproduce the body's derivation. Essay content in a structural slot.
**Required**: Reduce each to the claim itself (what holds), with the grouping/derivation living only in the body section it summarizes.

### Issue 7: Notation-reconciliation paragraph is procedural meta-prose
**ASN-0087, Inputs / "Notation convention — dom(M) and E_doc"**: "We use `dom(M)` throughout, and discharge ASN-0047 preconditions stated against `E_doc`... from membership in `dom(M)` by this M1 equality."
**Problem**: A paragraph justifying a notation choice and describing the discharge procedure. The substantive fact (M1 identifies the two) is one clause; the rest is housekeeping.
**Required**: Compress to a single parenthetical noting `dom(M) = E_doc` by M1; drop the procedural framing.

## OUT_OF_SCOPE

### Topic 1: Composite-level atomicity enforcement mechanism
**Why out of scope**: The ASN correctly identifies that substrate-level atomicity is absent and locates the guarantee at the protocol layer (Open Questions). The protocol layer is a future ASN, not a defect here.

### Topic 2: Well-formedness of forward-reaching endsets (addresses not yet in dom(C)/dom(L))
**Why out of scope**: L4 (EndsetGenerality) permits these; the precise constraints are correctly deferred to a future ASN via the Open Questions, not an error in MAKELINK's specification.

VERDICT: REVISE
