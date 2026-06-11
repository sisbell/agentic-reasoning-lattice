# Review of ASN-0119

## REVISE

No REVISE items. The load-bearing claims were checked individually rather than taken on trust; the checks and their outcomes:

- **Arithmetic of the worked examples.** The pivot (`ABCDE`, cuts ord 2/3/6) was recomputed against R-P1/R-P2/R-EXT: destinations `{2,3,4}`, `{5}`, `{1}` tile `{1..5}` disjointly; the π table (1↦1, 2↦5, 3↦2, 4↦3, 5↦4) matches the R-PPERM branches; range and extent check out. The swap (`ABCDEF`, cuts ord 2/3/5/7) recomputes to `A E F C D B` with the middle's net displacement `+1 = w_β − w_α`, matching the displacement identity `(ord(c₀)+w_β) − ord(c₁) = w_β − w_α` derived in the intervening-content section. The composite realization (Move 1 cuts 2/3/5, Move 2 cuts 4/5/6) was verified step by step: `π₂∘π₁` composes to exactly the atomic π table, and `M_mid([s_C,4]) = a₂ ∉ {a₄, a₅}` exhibits RA8b under the stipulated address distinctness.
- **RA2a.** The injectivity contradiction is complete: a text position mapped outside `s_C` would collide with the non-S branch's fixed point; onto follows from injectivity plus S8-fin. No gap.
- **S3★.** The inversion `M'(d)(v) = M(d)(π⁻¹(v))` is licensed by RA2, `π⁻¹(v)` stays in the text subspace by RA2a, and the link case rides on R-NS pointwise fixity. Both subspace conjuncts are discharged, not just the content one.
- **Invariant coverage.** Every conjunct of ExtendedReachableStateInvariants is accounted for: the key-set-only invariants (S8a, S8-fin, S8-depth, D-CTG★, D-MIN★, D-SEQ★, S3★-aux) by the RA2 set-invariance argument; the value-dependent S8★ positively via R-BLK + R-CANON on the content subspace and the R-NS freeze on `s_L`; CL-OWN/CL-UNIQ via the same R-NS value freeze; the frame-keyed families (S4/S7a/S7b/C-family/E-family/L-family/P6/P7/P8) by RA0/RA4/RA6; cross-document closure at every `d' ≠ d` by RA9. P3 is discharged at equality per conjunct, and the vocabulary-quantified M1 and NoDeallocation obligations are addressed rather than skipped.
- **Couplings and boundary properties.** J0 and J1'★ are vacuous by genuinely empty antecedents (RA0, RA4). J1★ is correctly recognized as *not* settled by full-range invariance RA1 and is closed by the content-subspace value-set invariance through RA2a — the one place a careless proof would have hand-waved. P4a's trace-quantified induction is extended explicitly, with the new final-composite case checked (empty new-entry branch) rather than asserted "similarly."
- **K.μ~ coincidence.** All five admissibility clauses are discharged individually, and the value-degenerate identity-effect instance (legal under R-PRE, realized by no admissible K.μ~) correctly delimits the coincidence to the non-trivial case — including the observation that the bijection equation does not *define* π when `M(d)` is non-injective.
- **Boundaries.** Empty text subspace, too-short active runs, empty exteriors, and whole-document intervals are each classified (outside the domain vs. degenerate branch). The partiality of the operation is stated with R-PRE named clause by clause.
- **Contiguity.** RA7c is honestly labeled sufficient-not-necessary, and the four worked configurations exercise both sides of the boundary (within-region gap preserved; cross-cut healing; exterior/moved fragmentation; partial-block fragmentation), so the one property REARRANGE does not preserve in general is exhibited rather than asserted.
- **Anti-bloat scan.** The candidate patterns were checked: the K.μ~ deferral appears once and is resolved once; the value-degenerate paragraph and the offset-vs-net-translation paragraph carry real technical content (delimiting the coincidence claim; preventing a sign confusion against ASN-0034's forward-only `shift`); the repeated link-subspace-frozen statements each do distinct work (state framing, scope confinement, R-NS value freeze for the value-dependent invariants). None rises to a finding.

## OUT_OF_SCOPE

### Topic 1: Exact precondition for footprint run-structure preservation across regions
**Why out of scope**: RA7c is explicitly a sufficient condition; the general characterization (when relocated blocks re-tile a multi-region footprint's runs, as in the α∪β healing case) is staked as an open question and is new territory, not an error in this ASN.

### Topic 2: Concurrent rearrangements without a serializing authority
**Why out of scope**: Commutation conditions for two rearrangements on the same content scope are an open question the ASN itself poses; the atomicity section establishes only the single-operation guarantees, which is its proper scope.

### Topic 3: Cut semantics under transclusion and recoverability of prior arrangements
**Why out of scope**: Boundary-hood of a cut relative to another document's independent arrangement, and reconstruction of superseded orders from the Istream, belong to future version/transclusion ASNs; this ASN correctly confines itself to one document's arrangement and records both as open questions.

VERDICT: CONVERGED
