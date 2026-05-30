# Review of ASN-0084

The operational core is sound: the pivot/swap postconditions, the bijection lemmas (R-PPERM, R-SPERM), the well-definedness lemmas (R-PIV, R-SWP), and R-BLK's split/classify/reassemble are proved case-by-case with no checkmark-substitution, and the five worked examples genuinely exercise the three μ-displacement sub-cases plus the empty-exterior boundary. My findings are confined to forward-reference accretion and one instance of reviser drift, per the `review-mode.anti-bloat` classifier.

## REVISE

### Issue 1: Foundation-S8 transport is asserted in four places with a use-site inventory
**ASN-0084, "Invariant preservation" (Foundation-S8 transport) / R-SP / R-BLK / Canonical decomposition**: "This is the canonical discharge of post-state S8; R-SP, R-BLK, and the canonical-decomposition argument below invoke it without restating it."
**Problem**: This closing sentence is a pure use-site inventory — it names three downstream consumers without advancing the transport argument. The pattern then compounds: each named site points back ("that transport is discharged once in the invariant audit above (Foundation-S8 transport)" in Canonical decomposition; "post-state S8 is discharged from foundation S8, whose preconditions never reference a pre-state partition" in R-SP; "discharges post-state S8 from foundation transport, not from B'" in R-BLK). The single fact "post-state S8 follows from foundation S8 because its preconditions are dom-preserved" is stated four times.
**Required**: State the transport once where it is established; delete the downstream consumer inventory and the three back-pointers. Each site can simply cite "foundation S8" inline.

### Issue 2: R-SP and R-BLK carry mutual scope/documentary disclaimers
**ASN-0084, R-SP opening and R-BLK opening**: R-SP — "This lemma establishes sufficiency only (the ⇐ direction)... is the separate concern of R-BLK (RunDecompositionTransformation) and is not relitigated here." R-BLK — "R-BLK is documentary — it characterizes how the rearrangement acts on a given pre-state decomposition, independently of the R-SP sufficiency argument (which discharges post-state S8 from foundation transport, not from B')."
**Problem**: Two paragraphs in different sections whose function is to negotiate the division of labor between the two lemmas and disclaim what each does *not* do. This is meta-prose about the argument's structure, not the argument. A reader following R-SP must absorb a forward disclaimer about R-BLK before reaching the proof; the same in reverse.
**Required**: Delete both cross-disclaimers. R-SP's postcondition (sufficiency for Q) and R-BLK's postcondition (B' construction) already fix their respective scopes without an essay about their relationship.

### Issue 3: R-CS3 rebuts a diagnosis the claim never raises, then double-justifies
**ASN-0084, R-CS3, "The failure is at 'the subspace S,' not at a region width"**: "We argue from the actual definitions, not from an ordinal-difference width. Under the stated (cardinality) definition of region width, β = {v ∈ V_S(d) : c₁ ≤ v < c₂} = ... = {[1, 5]} is a perfectly well-defined set with |β| = 1, so the region extent is *not* untyped. The genuine load-bearing role of CS3 is that..."
**Problem**: The lemma claims that dropping CS3 makes R-PRE(iv) unsatisfiable. That claim is fully established by the direct argument (reading S = 1 forces every [1,k] with k ≥ 2 into the quantified range, contradicting S8-fin). The "not a region width" paragraph instead rebuts a *rejected* diagnosis — reviser drift: relocated rebuttal of a prior finding rather than forward reasoning. The subsequent "*Frame interplay.*" subparagraph then adds a second, independent justification ("The incoherence also surfaces in the frame condition...") for a result the main argument has already closed.
**Required**: State only the unsatisfiability argument (S = 1 reading → infinitely many positions demanded of a finite V_S(d)). Drop the "not a region width" rebuttal and the redundant frame-interplay subparagraph.

### Issue 4: R-PPERM "Uniqueness scope" essay sits in the lemma statement
**ASN-0084, R-PPERM / R-SPERM**: the multi-sentence S5 fibre-permutation discussion ("When M(d) has repeated I-addresses... π is then unique only up to that equivalence class of fibre-permutations. The cut-point-induced choice singled out here is the canonical representative...") occupies the lemma *statement*, after which R-SPERM defers: "Its uniqueness scope is exactly that stated in R-PPERM."
**Problem**: This qualifies a real claim (uniqueness under sharing), so it is content, not noise — but it is essay content placed in a structural slot (the lemma statement) and the deferral creates a second cross-reference. Flag placement, not existence.
**Required**: Move the uniqueness-scope qualification to a remark following the proof, leaving the lemma statement as the bijection formula and its defining equation.

## OUT_OF_SCOPE

### Topic 1: k-cut generalization, composition of rearrangements, run-count growth bounds, confluence of merge recovery
These are correctly deferred — they already appear in Open Questions, are not obligations of the operation specified here, and depend on machinery (general k-cut permutation class, sequential composition semantics) this ASN does not introduce.

META: not applicable — the ASN defines abstract state (M(d) arrangement), an operation on it (REARRANGE_K), and the invariants it preserves; it has not drifted into implementation mechanics.

VERDICT: REVISE
