# Review of ASN-0094

## REVISE

### Issue 1: BundledDirectedPair walkthrough — BDP0/BDP1 chaining inconsistency
**ASN-0094, BundledDirectedPair walkthrough**: After BDP0 admits γ_0 with `slot_addrs(F_{γ_0}) = {d_cite}, slot_addrs(G_{γ_0}) = ∅`, the prose says "treat Σ_0a as the continuation state into Emission BDP1; alternatively, ignore BDP0 entirely and start from Σ_0 (the BDP1/BDP2 analysis below is independent of whether γ_0 was pre-emitted)." BDP1 then writes `Emit_K(Σ_0, home_cite, F_BDP1, G_BDP1)` and the table at Σ_2 records `from_K(d_cite) = {γ_1, γ_2}`.
**Problem**: The independence claim is false. If γ_0 is in `A_K^{Σ_2}`, then `from_K(d_cite)` is `{γ_0, γ_1, γ_2}` (since `from₁(γ_0) = d_cite`), and `pair_K(d_cite, ∅)` should evaluate to `true`. The table reflects γ_0-free state but the continuation prose says γ_0 is present.
**Required**: Pick one path explicitly — either (a) BDP1/BDP2 start from `Σ_0a` and the table is updated to include γ_0, or (b) BDP0 is a sealed-off aside (state explicitly "BDP1 starts fresh from Σ_0; BDP0 is exhibited only for the empty-G admissibility + Sh4 suppression test, and γ_0 does not participate in the rest of the walkthrough"). The current "independence" wording is incorrect.

### Issue 2: AllocatedAddressAntichain Sub-case 3b discharged "by symmetry" without explicit steps
**ASN-0094, *The Address-Set Projection***: Sub-case 3b's Step 3.3b reads "The argument is the side-label swap of Sub-case 3a's Step 3.3a: each of the three substantive moves... carries through under the swap with the identifier names exchanged, as the Case-symmetry preamble above licenses."
**Problem**: The Case-symmetry preamble argues that Steps 3.1 and 3.2 transfer because they don't reference domain membership, but Step 3.3 *does* reference domain membership (it consults `s_L ≠ s_C` with one side assigned to each domain). The framework writes out 3.3a explicitly but leaves 3.3b as "the swap." The worked example walks 3a concretely and gestures at 3b as a mirror image, but the formal proof omits 3b's three substantive moves. A strict reading rejects this as proof by "similarly."
**Required**: Either write 3.3b out as three lines parallel to 3.3a (this is cheap — six lines total), or strengthen the Case-symmetry preamble to explicitly enumerate that Step 3.3's *only* dependence on domain membership is via the disjointness predicate `s_L ≠ s_C`, which is symmetric in its two arguments, so the swap reduces to a single identity move.

### Issue 3: Coverage-equality decidability asserted but not shown
**ASN-0094, TypedRelationCatalog Definition**: "The test is decidable on arbitrary `K ∈ T_admissible` by checking `coverage(K) = coverage(K_rep)` against each of the finitely many registered representatives `K_rep`: coverage is a pure function of the endset value... and coverage-equality of two finite span sets is decidable."
**Problem**: `coverage(·)` is a union of "extension cones" `{t : s ≼ t}` over the finite span set. For canonical-slot endsets, this is `⋃ {{t : x ≼ t} : x ∈ slot_addrs}` and equality reduces to minimal-element-set equality modulo prefix relations — decidable but requires argument. For arbitrary (non-canonical) `K ∈ T_admissible`, displacements can be wide, spans can overlap, and two endsets with distinct span sets can have identical coverage (L5 in ASN-0043 already records that endset-equality and coverage-equality diverge). The framework's `T_cat` membership check sits *upstream* of Sh-conf clauses (a)/(b), so it must operate on arbitrary `K ∈ T_admissible`, not just canonical-slot.
**Required**: Either supply a one-paragraph derivation showing how coverage-equality reduces to a decidable comparison on finite span sets (likely via canonicalization to a minimal antichain of span starts), or restrict `T_cat`'s representative-list to canonical-slot endsets and explicitly note the restriction.

### Issue 4: Per-shape uniformity downgrade weakens the catalog without procedural compensation
**ASN-0094, Sh5(a)**: "*Status of per-shape uniformity (downgraded to aspiration in this draft).* The earlier draft phrased per-shape uniformity at the body-shape level... as a *commitment* enforced by hand-review. The present draft explicitly downgrades this from a commitment to an *aspiration*... no procedural recipe (documented difference table, body-shape derivation procedure from shape components, or auditor-side review checklist) is committed in the current draft."
**Problem**: The downgrade is acknowledged but the consequences for downstream consumers are not enumerated systematically. Sh5(b)'s catalog-row-structure paragraph still says "Every K registered at the shape generates the row's base templates mechanically" — this *requires* per-shape uniformity at the body-shape level to be more than aspiration, or the word "mechanically" is misleading. The framework cannot have it both ways: either two shape-mates share base templates by construction (commitment), or "mechanically" is a hand-curation hope (aspiration). The current text uses both phrasings.
**Required**: Reconcile the two readings. Options: (a) restore per-shape uniformity as a commitment with an explicit auditor checklist (a fourth-step procedure on top of the three-step extension checklist), or (b) replace "mechanically" with "by hand-curation" throughout the catalog row structure paragraph and the per-shape walkthroughs, and acknowledge that two layers registering at the same shape may diverge on base-template bodies.

### Issue 5: Sh4 Case A's case-equation closure is sound, but the "principal-transitions enumeration is expository" framing obscures the actual closure step
**ASN-0094, Sh4 proof, Case A**: "The case is *defined* by the equation `A_K^{Σ'} = A_K^Σ`, which the IH discharges without enumerating which transition classes achieve it; Case A's preservation is closed at the case-equation."
**Problem**: This is technically correct — if `A_K^{Σ'} = A_K^Σ`, then the universal over `A_K^{Σ'}` is identical to the universal over `A_K^Σ`, and the IH discharges it. But the framework then says R2 (TupleAddressPermanence) is needed to preserve "existing tuples retain their values" — yet R2 is not cited in Case A. If `A_K^{Σ'} = A_K^Σ` as sets *of triples*, then the triple values are equal by definition (set equality is element-wise). R2 is only needed if `A_K^{Σ'}` is described by addresses and the triples might mutate — but here the universal is over triples directly. The expository enumeration's preservation appeals (R2 + LinkStoreInvariance) are not consumed by the case-equation closure.
**Required**: Either drop the R2/LinkStoreInvariance citations from Case A's expository paragraph (they don't license the closure — the case-equation does), or explicitly note that the citations license the *prior* step "every step in the enumerated transition class produces `A_K^{Σ'} = A_K^Σ`" rather than the case's closure step.

### Issue 6: NullifyActiveSubsetCompatibility Case B's witness extraction relies on candidate-set hypothesis without surfacing the existence step
**ASN-0094, NullifyActiveSubsetCompatibility Corollary, Case B**: "*(ii) nullification.* `τ_prior ∈ A_R^Σ ⊆ L_R^Σ` has `a ∈ coverage(G_{τ_prior})` by the construction of `C`'s witness (the candidate-set membership requires `slot_addrs(G_{τ_prior}) = slot_addrs(G_{Nullify-call}) = {a}`, hence `coverage(G_{τ_prior}) ⊇ {a}` by PrefixSpanCoverage)."
**Problem**: The Case B hypothesis is `C ≠ ∅`, so an existential ∃τ_prior ∈ C is available, but the proof skips the existential-elimination step and names `τ_prior` directly. The conclusion `a ∈ nullified(Σ)` requires *any* such τ_prior to witness the existential in Definition (nullified). One witness suffices, so the existential-elimination is fine, but the proof reads as if τ_prior were uniquely determined. A reader checking the inference needs to confirm that one suffices.
**Required**: Add a single line before "τ_prior ∈ A_R^Σ ⊆ L_R^Σ has...": "Let τ_prior be any element of `C` (non-empty by the case hypothesis)." This eliminates the implicit choice and makes the existential-elimination explicit.

### Issue 7: BundledDirectedPair admits `c_G = 0` but the consequence for `pair_K(a, ∅)` semantics is not exercised
**ASN-0094, BundledDirectedPair walkthrough**: BDP0 admits an emission with empty G. The shape's `pair_K(a, Ĝ)` template uses set-equality on G, so `pair_K(d_cite, ∅)` is a well-defined Boolean.
**Problem**: The walkthrough exhibits Sh4 suppression on duplicate empty-G calls but does not evaluate `pair_K(d_cite, ∅)` at the resulting state. The empty-G boundary deserves a row in the template-evaluation table: under "include BDP0" continuation, `pair_K(d_cite, ∅) = true` (witnessed by γ_0); under "exclude BDP0", `pair_K(d_cite, ∅) = false`. Either reading exhibits a real template behavior at the cardinality boundary, but neither is shown.
**Required**: Add `pair_K(d_cite, ∅)` to the template-evaluation table at the appropriate continuation state (whichever Issue 1 resolves to).

## OUT_OF_SCOPE

### Topic 1: (0, 0) shapes
**Why out of scope**: Flagged as a refinement candidate in Open Questions. The current catalog does not exhibit a `(0, 0)` shape and the framework's Sh0/Sh1 inductions cover it vacuously. New canonical shapes belong in a future catalog extension, not in revisions to this ASN.

### Topic 2: Ghost-targeting slot semantics
**Why out of scope**: Flagged as a design choice in Open Questions. The current Sh-conf rejects ghost-targeting slot emissions deliberately. Admitting ghosts would require a new state-dependent conformance rule and a new family of shapes.

### Topic 3: Multi-process consistency for the *Sh4 idempotency contract* and *FDD functional-dependency contract*
**Why out of scope**: Flagged as a scope boundary in Open Questions. The current framework's atomicity premise reduces to within-call sequentiality on a single-process substrate. Cross-process consistency requires a coordination protocol outside the framework's commitments.

### Topic 4: A procedural recipe for body-shape uniformity at shape-mate rows
**Why out of scope**: The framework records this as a design aspiration in Sh5(a). A procedural recipe (body-shape derivation from shape components) would *extend* Sh5's META status into a mechanical-derivation theorem, which is a scope expansion rather than a fix.

### Topic 5: A formal containment claim for the predicate language under composition primitives
**Why out of scope**: The Consequences section notes that "the framework does not establish a closure theorem about these primitives." Whether composition strictly extends the catalog's atomic vocabulary is a property of the composition language adopted, not of the shape registry itself.

VERDICT: REVISE
