# Review of ASN-0091

## REVISE

### Issue 1: ActivatedEmission omitted from the RA-adm per-invariant discharge

**ASN-0091, "REARRANGE_K Realises the Abstract Class" → "State-Component-Only Invariants"**: "In particular, P0, P1, P2, P3, P6, P7, P7a, P8, NodeLineage, L0, L1, L1a, L1b, L1c, L3, L12, L14, L-fin, C0, C1, C1b, C1c, C2, and C-fin all hold at Σ' iff they hold at Σ."

**Problem**: ASN-0047's ExtendedReachableStateInvariants theorem lists the per-state invariant set as "...P8 ∧ NodeLineage ∧ **ActivatedEmission** ∧ L0 ∧ L1...". RA-adm requires *every* foundation invariant to be re-established at Σ', and the ASN discharges them by exhaustive per-invariant enumeration across three subsections (ASN-0036 foundation, ASN-0047 extended, state-component-only) plus P4a. ActivatedEmission appears in none of these lists — it is skipped exactly between NodeLineage and L0, mirroring the gap in the theorem's own ordering. The same omission recurs in all five worked-example admissibility paragraphs ("All other state-component-only foundation invariants — ... NodeLineage, L0–L14 ..."). Because the ASN's admissibility argument is by exhaustive enumeration rather than by a whole-package lemma, a missing conjunct is a genuine hole in the RA-adm discharge for REARRANGE_K.

**Required**: Add ActivatedEmission to the state-component-only group. It quantifies over Σ.E (and the allocator tree determined by E), both fixed by RA-frame's `E' = E`, so the discharge is one line — but it must appear. Update the worked-example admissibility paragraphs correspondingly.

### Issue 2: Incorrect ASN-0098 citations (LP-Comp, LP11 name)

**ASN-0091, "Composition Across Multi-Step REARRANGE Sequences"** (mixed-sequence paragraph): "The REARRANGE steps in such a mixed sequence are themselves governed by ASN-0098's LP11 (the K.μ~ case in **LP-Comp's** case-analysis) at the projection layer — LP-Comp is a documentation note ... while LP11 (**ReorderingRebinding**) is the substantive lemma..."

**Problem**: Two foundation citations cannot be verified against ASN-0098's claim set. (a) ASN-0098 defines LP11 as **ReorderingBijection**, not "ReorderingRebinding" — the ASN names it wrong. (b) "LP-Comp" does not appear anywhere in ASN-0098's claim statements; it is cited as a load-bearing case-analysis structure for the mixed-sequence argument but has no referent. A foundation reference that names a non-existent claim, or mis-names an existing one, is a citation error that must be corrected before downstream work relies on the mixed-sequence reasoning.

**Required**: Correct "ReorderingRebinding" to "ReorderingBijection". Either replace the LP-Comp reference with the actual ASN-0098 lemma that catalogs per-transition projection coverage (LP6/LP7/LP9/LP10/LP11/LP14 individually), or remove the LP-Comp scaffolding if it is not a real foundation claim.

## OUT_OF_SCOPE

### Topic 1: Link-subspace rearrangement semantics
**Why out of scope**: The ASN fixes the cut subspace at S = s_C (via CS3) and treats the link subspace only as a preserved frame (RE-sub). A REARRANGE operation acting *on* the link subspace, and its invariants, is genuinely new territory — correctly deferred to an Open Question rather than forced into this ASN.

### Topic 2: Upper bound on run-decomposition cardinality growth
**Why out of scope**: RE-frag establishes only that fragmentation is possible; the quantitative bound per invocation is a separate analysis, appropriately listed as an Open Question.

VERDICT: REVISE
