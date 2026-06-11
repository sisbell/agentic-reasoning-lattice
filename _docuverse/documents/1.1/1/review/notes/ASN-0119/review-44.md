# Review of ASN-0119

The ASN is in good shape structurally: the import of REARRANGE_K from ASN-0084 is clean, the invariant discharge against ASN-0047's package is unusually thorough, and the worked pivot/swap examples check out numerically (I verified every destination equation, the π table, the middle-region displacement `w_β − w_α`, and all four contiguity configurations against R-P1/R-P2/R-S1–S3). The remaining problems are a boundary-case overstatement, two compressed load-bearing derivations, one undischarged vocabulary obligation, and accumulated meta-prose of the kind the anti-bloat classifier targets.

## REVISE

### Issue 1: K.μ~ equivalence claim fails at the value-degenerate boundary
**ASN-0119, "The two streams"**: "REARRANGE imported as an atomic arrangement-rearrangement primitive (ASN-0084) that realizes the same *net* arrangement change as ASN-0047's own non-atomic `K.μ~` composite without ever vacating content."
**Problem**: K.μ~'s admissibility clause (ii) requires a non-trivial net effect `M'(d) ≠ M(d)`, and its precondition requires `M(d)|_{dom_C}` to take at least two distinct values. REARRANGE_K's R-PRE imposes no value-based condition. Shared content is reachable (ASN-0036 S5, ASN-0058 M13), so an arrangement in which every position of the affected interval maps to the same I-address is legal, and a pivot on it is REARRANGE-legal with `π ≠ id` yet `M'(d) = M(d)` — a net change (the identity) that no admissible K.μ~ realizes. The universal "realizes the same net arrangement change as K.μ~" is therefore false at this boundary.
**Required**: Qualify the correspondence — e.g., "realizes the same form of arrangement change as K.μ~, coinciding with an admissible K.μ~ whenever the net effect is non-trivial" — or drop the equivalence framing. Note explicitly that REARRANGE's domain includes value-degenerate identity-effect instances that K.μ~ excludes.

### Issue 2: "π permutes the text subspace onto itself" is asserted, never derived
**ASN-0119, "What is preserved"**: "`π⁻¹(v)` is again a text position (`π` permutes the text subspace onto itself)"; and later, "because `π` permutes the text subspace onto itself, the content-subspace value set is invariant."
**Problem**: This fact gates the S3★ preservation argument, the content-subspace value-set invariance, and through it J1★ and P4★ — four load-bearing discharges — yet it is supported only by a parenthetical. It is not in the imported R-PPERM/R-SPERM statements as such; it requires a short argument the ASN never gives.
**Required**: State and prove it, in either of two available ways: (a) from RA2 plus the non-S branch — π fixes every non-`s_C` position pointwise, so if some `v ∈ V_{s_C}(d)` had `π(v) = w ∉ V_{s_C}(d)`, then `π(w) = w = π(v)` with `v ≠ w` contradicts injectivity; hence `π(V_{s_C}(d)) ⊆ V_{s_C}(d)`, and bijectivity on the finite domain closes onto-ness; or (b) by citing R-PIV/R-SWP's tiling, which places every region destination in `[c₀, c_{n−1}) ∩ V_S(d)`, with exterior and non-S branches pointwise fixed.

### Issue 3: Completeness claim leaves M1 (and the closed-vocabulary obligation) undischarged
**ASN-0119, end of "What is preserved"**: "With both of ASN-0047's invariant theorems discharged, the invariant package REARRANGE joins is fully accounted for."
**Problem**: ASN-0047's M1 (ArrangementMonotonicity, `dom(M) ⊆ dom(M')`) is a standing transition invariant that belongs to neither ExtendedReachableStateInvariants nor ExtendedTransitionInvariants (whose sole conjunct is P3), so discharging the two theorems does not account for it. Since the ASN deliberately extends the closed atomic vocabulary, every vocabulary-quantified constraint now ranges over REARRANGE steps — M1 among them, and at the foundation layer the closed-Σ frame of NoDeallocation/T8 (no transition may shrink the allocated set). Both hold trivially for REARRANGE (`dom(M') = dom(M)` by RA9 plus `M'(d)` total on the same key set; no allocation event occurs, so the allocator-tree state is untouched), but neither is stated, and the "fully accounted for" sentence asserts a completeness the text does not deliver.
**Required**: Add the one-line discharges of M1 and the allocated-set monotonicity obligation, or weaken the completeness sentence to name what it covers.

### Issue 4: Duplicated meta-prose — frame-lifting rationale and the sufficiency caveat
**ASN-0119, "The two streams" vs. "Links"; "Links" (RA7c paragraphs)**:
(a) "The two streams": "ASN-0084's frame names only the content store and the arrangement; lifting the operation into the extended `(C, L, E, M, R)` state, we extend that frame with an explicit clause for each component it does not name — RA6 ... RA4 ... by the same discipline." Then "Links": "ASN-0084's REARRANGE_K frames only the content store and the arrangement; its frame R-FRAME-P/R-FRAME-S says nothing about the link store `L`. Lifting the operation into the `(C, M, L)` state, we extended that frame at the outset with an explicit clause — RA6 ... — because REARRANGE writes only `M(d)`."
(b) The RA7c caveat is stated, restated, and re-restated: "We record this as a *sufficient* condition ... not as a weakest precondition"; then "That precondition is *sufficient, not necessary*, and what it controls is *run structure*, not a single-span result: confinement neither heals existing gaps nor is required for a straddling footprint to land contiguous on its own"; then inside the examples, "it neither heals the gap nor manufactures a single span" and "confirming that confinement is *not necessary* for a contiguous result."
**Problem**: (a) is the same content twice, the second instance narrating the document's own history ("we extended that frame at the outset") — exactly the relocated-rationale pattern this note is flagged for. (b) states the sufficiency-not-necessity point in full twice before the examples confirm it; one statement plus the worked confirmations suffices.
**Required**: State the frame extension once, where RA4/RA6 are introduced; in "Links," simply invoke RA6. Collapse the RA7c caveat to a single statement; let the examples carry the confirmation without editorial restatement.

### Issue 5: `coverage(a, i)` is introduced while claimed not to be
**ASN-0119, "Links"**: "— both imported (ASN-0098, Definition — Coverage and Definition — Project), not introduced here."
**Problem**: ASN-0098 defines `coverage(e)` on endsets and writes `coverage(Σ.L(a).eᵢ)`; the two-argument, state-suppressed form `coverage(a, i)` is this ASN's own shorthand. The suppression is harmless across the transition only because RA6 freezes the link store — a fact the shorthand silently presupposes — and the "not introduced here" clause is both defensive meta-prose and literally inaccurate for this form.
**Required**: Either use ASN-0098's notation, or define the shorthand honestly: `coverage(a, i) := coverage(Σ.L(a).eᵢ)`, noting it is state-independent across the REARRANGE transition by RA6. Delete "not introduced here."

### Issue 6: RA8a — undefined notation and a compressed composition argument
**ASN-0119, "Atomicity: two cuts at once"**: "`M'(d) under T = M(d) under (T₁ ; T₂)` **(RA8a)** ... because both realize the same `π` and the arrangement is determined by `π` applied to the same content (RA1)."
**Problem**: The displayed equation uses `T`, `T₁ ; T₂`, and "under" without definition, and as written equates `M'(d)` with `M(d)` under different decorations. The general claim (table: "any two-move composite achieving the same net π") needs two steps the parenthetical skips: (1) the composite of two arrangement rearrangements is an arrangement rearrangement with bijection `π₂ ∘ π₁` (so `M_final(u) = M(d)((π₂ ∘ π₁)⁻¹(u))`), and (2) the post-arrangement is uniquely determined by the bijection and pre-state via `M'(d)(u) = M(d)(π⁻¹(u))`, which is the defining equation plus bijectivity. The worked example verifies one instance; the labeled claim is general.
**Required**: Replace the display with a stated equation (e.g., `M'_atomic(d) = M'_composite(d)` whenever `π₂ ∘ π₁ = π`) and give the two-line composition derivation.

## OUT_OF_SCOPE

### Topic 1: Weakest precondition for footprint run-structure preservation across regions
**Why out of scope**: RA7c is deliberately a sufficient condition; the exact characterization (including footprints spanning three or more regions and seam healing/breaking) is new territory the ASN correctly defers to its Open Questions rather than an error here.

### Topic 2: Commuting concurrent rearrangements
**Why out of scope**: Order-independence of two rearrangements on one document without a serializing authority is a new coordination result, properly listed as an Open Question, not a gap in this operation's specification.

### Topic 3: Recoverability of prior arrangements
**Why out of scope**: Whether and how a superseded V→I order is reconstructible from the permanent store is a versioning/history concern (CREATENEWVERSION territory), not an obligation of the rearrangement primitive.

VERDICT: REVISE
