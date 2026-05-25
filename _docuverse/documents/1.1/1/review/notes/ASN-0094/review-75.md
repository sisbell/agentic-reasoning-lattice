# Review of ASN-0094

## REVISE

### Issue 1: CoverageEqualityDecidability uniformity step underspecified
**ASN-0094, Lemma — CoverageEqualityDecidability, Step (3)**: "For each delimited interval `[e_k, e_{k+1})`, test membership in `coverage(E)` and in `coverage(E')` via the representative point `e_k`... Because each span is a T1-interval and the partition is finer than every span's boundary, membership is uniform on each delimited interval: `e_k ∈ coverage(E)` iff every point of `[e_k, e_{k+1})` is in `coverage(E)`."

**Problem**: The proof asserts uniformity within each delimited interval without deriving it. The decidability claim depends on this step: if `[e_k, e_{k+1})` could straddle a span boundary, the representative-point test would be unsound. The argument needs one explicit sentence linking "EP contains every span boundary" to "no span boundary falls strictly inside any `(e_k, e_{k+1})`".

**Required**: Add: "Since `EP` contains both `s_i` and `s_i ⊕ ℓ_i` for every span, no span boundary lies strictly inside any `(e_k, e_{k+1})`; hence `[e_k, e_{k+1})` is either entirely contained in `[s_i, s_i ⊕ ℓ_i)` or entirely disjoint from it, so the union over spans is uniform on `[e_k, e_{k+1})`."

### Issue 2: Lemma LinkAddressNotPrefixOfEmit Step II.2 citation chain hides the structural argument
**ASN-0094, Lemma — LinkAddressNotPrefixOfEmit, Case II.B Step II.2**: "All of `n_1, n_2, n_3` lie in `1..#b`, so T4b's field projections — `N(·)` at `1..n_1 − 1`, `U(·)` at `n_1 + 1..n_2 − 1`, `D(·)` at `n_2 + 1..n_3 − 1` — also lie within `1..n_3 − 1 ≤ #b`."

**Problem**: T4b alone does not fix the positional index ranges of N/U/D — it only asserts that `fields(t)` is well-defined. The actual ranges come from T4a (field segments as maximal non-zero contiguous sub-sequences delimited by zeros) combined with T4c (zero count = 3 → four hierarchical fields). The phrase "T4b's field projections" elides T4a's structural role.

**Required**: State the chain explicitly: "By T4a (field segments are maximal non-zero contiguous sub-sequences delimited by zeros) + T4c (`zeros = 3` → four fields N, U, D, E) + T4b (uniquely computable projection), at any T4-valid `zeros = 3` address with zero positions `n_1 < n_2 < n_3`, the field projections occupy positions `1..n_1 − 1`, `n_1 + 1..n_2 − 1`, `n_2 + 1..n_3 − 1`, `n_3 + 1..#·`."

### Issue 3: "FDD ⇒ Sh4" implication asserted, not derived
**ASN-0094, FunctionalDependencyDiscipline section**: "*FDD subsumes Sh4 at FDD-registered K.* At FDD-registered K the layer runs only the FDD clauses (i)–(iii), with Sh4's clauses dormant. The Sh4 conclusion still holds because `C ⊆ C_fd`: FDD's stricter from-slot-uniqueness entails Sh4's weaker slot-pair-distinctness."

**Problem**: `C ⊆ C_fd` is a set inclusion on the gate-check candidate sets, not on the relations themselves. The Sh4 conclusion is a property of `A_K^Σ`. The actual derivation: take distinct τ ≠ τ' in `A_K^Σ`; by FDD + R1, `from₁(τ) ≠ from₁(τ')`; hence `slot_addrs(F_τ) ≠ slot_addrs(F_{τ'})`; hence slot-pairs differ. This direct argument on the relation is the load-bearing step; the contract-side argument `C ⊆ C_fd` is auxiliary.

**Required**: Replace with: "Take any distinct τ ≠ τ' ∈ A_K^Σ. By FDD's contrapositive plus R1 (AddressInjectivity), `from₁(τ) ≠ from₁(τ')`. Hence `slot_addrs(F_τ) ≠ slot_addrs(F_{τ'})`, so their slot-pairs differ. Sh4's conclusion holds on A_K^Σ."

### Issue 4: BundledDirectedPair walkthrough's narrative-variant structure invites confusion
**ASN-0094, BundledDirectedPair walkthrough**: The main timeline runs `Σ_0 → Σ_1 → Σ_2`. The empty-G case (BDP0) is presented as a "narrative variant" branching to `Σ_1'`, with extensive disambiguation prose: "The 'parallel' terminology in subsequent prose refers to the walkthrough author's choice of two separate first-step explorations from the same `Σ_0`, *not* to parallel reachability in the state graph (which is sequential under `↦`)."

**Problem**: The variant structure forces multi-paragraph disambiguation because Σ_1' is symbolically tied to Σ_0 but never composes into the main timeline. The empty-G case is structurally just another emission; presenting it linearly avoids the variant scaffolding entirely.

**Required**: Restructure as `Σ_0 → Σ_1 (BDP0, empty-G) → Σ_2 (BDP1, multi-target) → Σ_3 (BDP2, single-target)`. All three cardinality regimes co-exist in `A_K^{Σ_3}` and template evaluation exhibits all three. Eliminate the variant scaffolding and the disambiguation paragraph.

### Issue 5: Bloat patterns — defensive justification and redundant forward references
**ASN-0094, multiple sections**: The note carries the `review-mode.anti-bloat` classifier; three patterns recur:

(a) **"Catalog Curation Discipline" defensive prose**: The "per-shape uniformity convention" paragraph spends most of its length explaining *why* hand-curation isn't framework-derivation, ending with "the framework supplies no mechanical gate that would enforce body-shape convergence... a future catalog extension at an existing shape may register divergent template bodies without violating any framework gate." This is the anti-bloat pattern "new prose around an axiom explains why the axiom is needed rather than what it says."

(b) **Sh-conf "Caller-side dispatch" paragraph**: Re-enumerates the gate sequence with caller-side framing, then forward-references the very next section ("The consolidated *Gate Ordering* below is the canonical statement..."). Adds no content beyond what Gate Ordering already covers.

(c) **"Common rejection patterns" enumeration**: Numbered 1–6 with notes like "pattern 5 is derived first at Classifier, and pattern 6 is derived first at BundledDirectedPair." Each downstream walkthrough back-references the pattern number, creating an extra indirection layer.

**Required**: (a) Compress Catalog Curation Discipline to three short rules without defensive framing. (b) Delete the Caller-side dispatch paragraph; add one line to the Gate Ordering section ("Callers may invoke any gate as a side-effect-free read to distinguish rejection causes before issuing Emit_K"). (c) Eliminate the forward-reference list; introduce each pattern inline at first use only.

### Issue 6: ASN size and split-pending decision
**ASN-0094, overall structure**: 43K words covering (a) Sh-conf axiom and Sh0–Sh4 preservation, (b) three per-K layer-discipline contracts with preservation arguments, (c) seven canonical shapes with template walkthroughs, (d) four bridge lemmas, (e) two corollaries. The Properties Introduced table has 17 load-bearing entries plus 14 supporting definitions.

**Problem**: The framework (Sh-conf + Sh0–Sh4), the disciplines (three layer contracts), and the catalog (seven shapes with templates) are distinct concerns. Their coupling in one ASN forces forward references between sections, inflates the conformance check surface, and makes the review boundary unclear. Per project memory, review-30 already recommended a 3-way split and the operator deferred; the pre-protocol-docs window is the deferred trigger.

**Required**: Split into (i) framework (shapes, Sh-conf, Sh0–Sh4, slot accessors, bridge lemmas), (ii) disciplines (Sh4/FDD/SHCD contracts with preservation arguments), (iii) catalog (seven shapes with template families and walkthroughs). The split lifts the per-component review burden and surfaces the dependency structure cleanly.

## OUT_OF_SCOPE

### Topic 1: Composite shapes
**Why out of scope**: Whether relations whose F or G is constrained by another relation's content require a new restriction axis is flagged in Open Questions. Future ASN, not a revision.

### Topic 2: Multi-process consistency
**Why out of scope**: The Sh4/FDD/SHCD contracts commit to single-process substrates by design. Characterizing the minimum coordination protocol for multi-process substrates extends scope, not patches the framework.

### Topic 3: Non-empty initial link store baselines
**Why out of scope**: Preservation theorems presuppose `L_K^{Σ_init} = ∅`. Retrofitting onto non-empty initial states is explicitly flagged as a scope boundary in Open Questions.

### Topic 4: Document-container target symbol (`A_M`)
**Why out of scope**: Whether target-domain vocabulary should admit `A_M` for `dom(Σ.M)` (Nelson metalink semantics) is flagged with explicit Nelson/udanax-green tradeoffs.

VERDICT: REVISE
