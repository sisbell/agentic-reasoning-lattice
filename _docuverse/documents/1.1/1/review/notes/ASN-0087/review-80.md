# Review of ASN-0087

I read the full note and checked the operation decomposition, preconditions, effect, the wp analysis, side-effect characterization, the worked example, and every invariant discharge against ASN-0047's `ExtendedReachableStateInvariants` / `ExtendedTransitionInvariants` theorems. The mathematical content is in good shape: edge cases (empty endset for `i ≠ 3`, empty vs. non-empty link subspace, first-vs-subsequent emission, cross-document discoverability) are all handled, the S2 discharge separates within-subspace and cross-subspace exclusion explicitly, and the D-CTG★ argument is proved at arbitrary depth `m ≥ 2` rather than assuming `m = 2`. The invariant checklist is complete against the foundation theorems, and the worked example verifies the novel property (discoverability) concretely.

The findings below are anti-bloat (the note's active classifier): genuine but localized prose redundancy.

## REVISE

### Issue 1: "Permanence of the Binding" restates the same conclusion redundantly
**ASN-0087, Permanence of the Binding**: "...the binding `v_ℓ ↦ ℓ` is therefore *invariant* under every K.μ~ transition. The link subspace is fixed pointwise by reordering."
**Problem**: The second sentence ("The link subspace is fixed pointwise by reordering") is a pure restatement of the first — the K.μ~ invariance of the binding was just derived from clause (v). With the later "Thus the binding is mutable only by removal, never by re-binding...", the section states "only K.μ⁻ can change it" three times.
**Required**: Drop the standalone restatement; keep the clause-(v) derivation (K.μ~ fixes `v_ℓ`) and the one-line synthesis that K.μ⁻ is the sole mutator.

### Issue 2: "discoverability is a derived property of (L, M)" duplicated across sections
**ASN-0087, What Is Indexed? / Side Effects on Prior Links' Discoverability**: "Discoverability is therefore a derived function of `L` and `M`..." (What Is Indexed?) versus "Discoverability is a derived property of `(L, M)`, not a state component the frame can directly assert about..." (Side Effects).
**Problem**: The same insight (discoverability is derived from `L` and `M`, not stored) is asserted in two sections and again in the M-NoIndexState row. The Side-Effects occurrence reads as motivating boilerplate before the actual LP12-at-`Σ`/`Σ'` characterization, which is the load-bearing part.
**Required**: State the "derived, not stored" fact once (it belongs in *What Is Indexed?* / M-NoIndexState) and have *Side Effects* open directly with the `ran(Σ'.M(d)) = ran(Σ.M(d)) ∪ {ℓ}` delta and its LP12 consequence.

## OUT_OF_SCOPE

### Topic 1: Well-formedness for forward-reaching / never-allocated endset spans
**Why out of scope**: Open Question 1 correctly defers the constraints on endsets covering not-yet-allocated or never-allocated addresses; `StandardAuthoring` is presented as a discipline this ASN uses, not a substrate-enforced invariant, and tightening it belongs to a future ASN.

VERDICT: REVISE
