# Review of ASN-0099

## REVISE

### Issue 1: F4 (MatchFormulaMinimality) framing
**ASN-0099, F4**: "F1's slot-existential / singleton-overlap form is the unique match predicate that, when wired into F2 ∧ F3, produces conformance with the reader's promise."
**Problem**: The label "Minimality" and the "unique" claim suggest mathematical uniqueness, but the proof establishes only (a) operational distinguishability (any P ≠ F1 yields a different operation — trivially true once F2 ∧ F3 are wired with F1) and (b) design rationale via three illustrative refutations (containment, reverse containment, threshold). The proof does not systematically enumerate the predicate design space. The substantive content is design-anchored against Nelson LM 2/46, not derivable from foundation invariants. Without enumeration, "unique" rests on rhetorical force from three examples rather than systematic exclusion. Universal quantifications over "weakening alternatives" are gestured at but not concretely instantiated as the strengthenings were.
**Required**: Either (a) downgrade the label ("OperationalDistinguishability" or "DesignJustification") with explicit framing that uniqueness is design-anchored, or (b) strengthen the proof by enumerating the strengthen/weaken lattice and discharging each branch with concrete witnesses (the proof currently gives three strengthenings; symmetric weakening witnesses are needed).

### Issue 2: F11 (PersistentDiscoverability) terminology overlap with ASN-0098
**ASN-0099, F11**: Named "PersistentDiscoverability"; the narrative paragraph uses "permanently discoverable."
**Problem**: ASN-0098 defines `discoverable_from(a, d, Σ)` as the V-side notion depending on `ran(M(d))`. F11's "discoverability" is the I-side `matches(a, I, ·)` against a *fixed* I-set — a distinct concept. The V-side `discoverable_from(a, d, ·)` is explicitly *not* persistent (K.μ⁻ contraction can drop V-positions, shrinking `ran(M(d))`). The worked example Query 5 actually demonstrates this non-persistence implicitly (`findlinks_V({v_a^2}, d_a, Σ_5) = ∅`) but the ASN doesn't surface the distinction. A reader fluent in ASN-0098 will read "persistent discoverability" and expect the V-side version to be claimed permanent.
**Required**: Add an explicit note distinguishing F11's I-side persistence (fixed I, preserved by L12+LP13+PerLinkInvariance) from ASN-0098's V-side `discoverable_from(a, d, ·)` (mutable through `ran(M(d))`). Spell out that the I-side persistence is exactly what permits F19's monotonicity while V-side answers can shrink across edits.

### Issue 3: F10a Case (ii) proof terseness
**ASN-0099, F10a, Case (ii)**: "d₁ ≺ d₂ with #d₁ < #d₂ forces d₂_{#d₁+1} ≥ 1 (M0's zeros(·) = 2 excludes a zero at the extension)..."
**Problem**: The parenthetical compresses a four-step argument the reader must reconstruct: (1) M0 gives `zeros(d₁) = zeros(d₂) = 2`; (2) T4's `d[#d] ≠ 0` places d₁'s 2 zeros at positions strictly less than `#d₁`; (3) prefix preservation under `d₁ ≺ d₂` carries those zeros to the same positions in d₂; (4) `zeros(d₂) = 2` total forces no additional zeros in extension positions `#d₁+1, ..., #d₂`, hence `d₂_{#d₁+1} ≠ 0`, and by T0's ℕ-discreteness `d₂_{#d₁+1} ≥ 1`. The conclusion is correct, but the chain is implicit. By the per-step citation convention applied elsewhere in the ASN (and in cited foundations like T10a-N), this should be spelled out.
**Required**: Expand the parenthetical to name the four foundation steps: M0 (zero count), T4 (no trailing zero), prefix preservation (d₁ ≺ d₂), and T0 (ℕ-discreteness for the `≥ 1` step).

## OUT_OF_SCOPE

### Topic 1: V-side analog of F9 (survivability under edits)
**Why out of scope**: V-side queries are inherently arrangement-dependent; K.μ⁻ contraction can shrink `dom(M(d))` and the V-image. The non-monotonicity is intentional. A restricted V-side persistence under non-contracting operations would be a specialized variant, not a general theorem of FINDLINKS.

### Topic 2: Query I containing addresses outside `dom(C) ∪ dom(L)`
**Why out of scope**: The spec handles arbitrary I ⊆ T; matches against "ghost" addresses compute normally. The author flags this in open questions for future design.

### Topic 3: Inverse direction (FOLLOWLINK, RETRIEVEENDSETS)
**Why out of scope**: Explicitly named as a separate operation by the author.

### Topic 4: Distributed/partitioned link store consistency
**Why out of scope**: Beyond the single-state Σ setting; flagged in open questions as architectural.

### Topic 5: Implementation indexing requirements
**Why out of scope**: The spec demands `result = findlinks` regardless of computation mechanism. Index design is implementation-side.

### Topic 6: Access control beyond the scope filter
**Why out of scope**: Access control composes via the abstract scope parameter S; richer authorization is orthogonal.

### Topic 7: Concurrent K.λ semantics
**Why out of scope**: SequentialTransitionAxiom forecloses concurrency at the substrate level; higher-layer concurrent protocols are out of scope.

### Topic 8: Combined filtered-and-scoped operation
**Why out of scope**: The author notes naive composition `findlinks_filtered(C, Σ) ∩ S` suffices and properties propagate; formal treatment is deferred.

VERDICT: REVISE
