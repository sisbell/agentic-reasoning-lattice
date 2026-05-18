# Review of ASN-0086

## REVISE

### Issue 1: R7a's class-(i) replay frame is asserted, not derived

**ASN-0086, R7a proof, "Class-(i) replay frame" sub-paragraph**: "The replay's class-(i) step has frame conditions *freshness plus the structural properties (T4-valid(d_k) ∧ zeros(d_k) = 2) of a document address*. T10a-conformance of d_k — its full spawning chain through any account/node allocator ancestors — is an opaque substrate guarantee delegated to ASN-0036's S7d at Σ', not a precondition the replay step independently reconstructs."

**Problem**: T10a's transition admissibility (AllocatedSet's T2 in ASN-0034) requires that a child spawn is admissible "only when parent(A) ∈ Act(s) and spawnPt(A) ∈ domₛ(parent(A))" — an explicit runtime precondition on the spawn state, not a global structural property. If d_k's account-allocator isn't activated in Σ_{prev}, class-(i) cannot admit d_k's allocation from that state. The original ↝-trajectory may have activated d_k's ancestor allocators between Σ and Σ' (witnessing them at Σ' but not Σ). The replay vocabulary {(i), (iii)} excludes account/node allocation steps, so R7a's decomposition does not cover the case where d_k's account-allocator wasn't yet activated in Σ. The substrate primitive's actual preconditions for class-(i) (whether it checks ancestor activation or merely structural properties) are not committed in the Setup's Frame conditions.

**Required**: Either (a) extend the replay vocabulary to include account/node allocation steps when needed, accepting that R7a's reduction includes hierarchy-construction primitives, or (b) justify with explicit citation to ASN-0034/ASN-0036 that class-(i)'s precondition is structural-only, independent of ancestor activation state. The "deliberately does not include" assertion needs to become a proven property of the substrate primitive.

### Issue 2: Notation error in R7a statement

**ASN-0086, R7a statement**: "there exists a finite sequence `Σ = Σ_0 → Σ_1 → … → Σ_m = Σ_n'` (`m ≥ 1`)"

**Problem**: `Σ_n'` is undefined. The body of the statement and the proof treat the terminal state as `Σ_m` alone, with `Σ_m.L = Σ'.L` but `Σ_m ≠ Σ'` in general.

**Required**: Drop the `= Σ_n'` clause.

### Issue 3: ASN-0036 P3 mis-attribution

**ASN-0086, Definition — BroadExtension**: "By the arrangement-modification frame (above) — ASN-0036's P3 (ArrangementMutability) governs Σ.M-only mutability without affecting Σ.C or extending dom(Σ.M)..."

The same attribution recurs in R6c-Corollary: "arrangement-modifying transitions hold Σ.L identical by ASN-0036's P3 frame condition".

**Problem**: P3 (ArrangementMutability) is in ASN-0047, not ASN-0036. ASN-0086's Setup explicitly states "no dependence on ASN-0047". The arrangement-modification frame property used here is supplied by ASN-0036's S9 (TwoStreamSeparation) for content invariance + ASN-0043's L12 + L12a for link store invariance.

**Required**: Replace "ASN-0036's P3 (ArrangementMutability)" with the correct citations (S9 from ASN-0036 + L12 + L12a from ASN-0043), or acknowledge dependence on ASN-0047 in the Setup.

### Issue 4: "Substrate emission primitive" terminology is inconsistent

**ASN-0086, Setup ("State transition relation" paragraph)**: introduces class (iii) as "the substrate emission primitive for the link store" — i.e., the broader "emit-at-any-L1c-conforming-fresh-address" admission.

**ASN-0086, Properties Introduced table, `→` entry**: "Dom-extending state transition relation with frame conditions per class (i)/(ii)/(iii) and substrate emission primitive for `Emit_K`"

**Problem**: The phrase "substrate emission primitive" denotes the broad class (iii) in the Setup but the table phrasing "for Emit_K" suggests the disciplined subset. The asymmetry confuses what class (iii)'s admissibility actually is. Compounded by the prose elsewhere ("R0a is conditional on the sibling-frontier discipline", "Emit_K is the relational layer's sibling-frontier-disciplined subset of class (iii)") — the reader has to repeatedly track whether a given "substrate emission primitive" reference is the broad or narrow version.

**Required**: Fix consistent terminology. Use "substrate emission primitive" exclusively for the broad class-(iii) primitive, and use "Emit_K" or "disciplined emission" for the narrower disciplined subset. Correct the table entry.

### Issue 5: Forward-reference accretion patterns (anti-bloat classifier)

The note carries the `review-mode.anti-bloat` classifier. The following patterns appear:

**(a) Recipe paragraph after R5's proof**: "*Recipe — self-targeting emission.* The Consequences below and the Nullify operation (Three Operations) share a single dependency chain... Below we cite this recipe rather than reinstantiate it."

A definition's introduction enumerating downstream consumers, with explicit DRY-justification ("Below we cite this recipe rather than reinstantiate it") in a structural slot. Either inline the recipe at each use-site or remove the meta-prose; do not justify document organization in-band.

**(b) "Class-(i) replay frame" sub-paragraph in R7a's proof**: Defensive justification of the replay vocabulary's exclusion of account/node allocators ("The replay vocabulary {(i), (iii)} deliberately does not include account/node allocation steps: such ancestors are carried by Σ' itself... because the replay's purpose is to reconstruct..."). This is justifying ordering choices rather than discharging a proof obligation (Issue 1).

**(c) "Crafted-span retractions" paragraph in Nullify's definition**: "Nothing in Emit_R's definition prevents a caller from emitting a retraction with a broader-coverage to-span..." Imagines a case the Nullify operation's defined argument shape already excludes. Out-of-scope discussion in the operation's definition slot.

**(d) "Setup dependence" remark after R5's proof**: "The L14a-preservation step relies on the Setup hypothesis... R5 is therefore Setup-required even though the L14a check is on the fresh emitter address `a'`, not on the span targets." Meta-prose explaining hypothesis usage rather than proving R5.

**(e) Emit_K's "Note." paragraph**: "Whether the fresh emission (a, F, G) lands in the active subset A_K^{Σ'}... is the subject of WP Case 2 (Weakest-Precondition Analysis, below)." Forward-defers a question to a downstream section the reader will encounter naturally.

**(f) "Antichain discharges P3" sub-paragraph in Nullify's definition**: Justifies that the no-strict-prefix-extension condition is derived (not a per-call precondition). The Nullify definition could simply state P0, P1, P2 and observe single-tuple scope is substrate-derived — without the multi-paragraph "let me explain what isn't a precondition" detour.

**(g) Definition — Extension's final sentence**: "The phrase 'Σ' extending Σ' used throughout this note (and lifted from ASN-0043 invariant restatements such as L9, L11b) is this relation." Meta-prose about terminology source.

**(h) Note on the precondition after R0's proof**: "*Remark on the precondition.* The hypothesis dom(Σ.M) ≠ ∅ is necessary..." Defensive justification anticipating an objection; the necessity follows directly from L1a and needs no separate remark.

**(i) Properties Introduced table dependency strings**: Per-claim dependency inventories like "(= L0 + L1 + L1a + L1b + L1c + L3 + L11a + L12 + L12a + L14a + L-fin from ASN-0043; T0(a) + T0(b) + T10a axiom + T10a.2 + T10a.4 + T10a.6 + T10a.7 + T10a.8 + TA5 + TA5a from ASN-0034; S3 + S7d from ASN-0036; Setup hypothesis at the L14a-preservation step)" are exhaustive use-site catalogs. The summary nature of the table is undermined by paragraph-length dependency inventories.

**Required**: Remove or trim these patterns per the anti-bloat classifier. Each paragraph should advance reasoning, not justify document organization.

### Issue 6: R6b META framing

**ASN-0086, R6b**: "*[META: property of the Definition of nullified's quantifier range.]* ... Deciding `a ∈ nullified(Σ)` requires only one level of existential check, with no further evaluation of `nullified(·)` on the witness; changing the Definition's quantifier range to `A_R^Σ` would change R6b without any further proof obligation, which is what the META classification reflects."

**Problem**: The META framing is followed by a sentence justifying why the META framing applies. This is meta-meta-prose. R6b is simply a direct reading of the Definition's quantifier range — call it a LEMMA reading off the Definition, or fold it into the Definition entirely.

**Required**: Either state R6b as "By Definition of nullified, the existential ranges over `L_R^Σ` (audit slice), so single-depth checking is immediate" without the META label and self-justifying prose, or fold the property into the Definition of `nullified` and remove R6b as a separate claim.

### Issue 7: Concrete consequence for non-disciplined emissions missing

**ASN-0086, R0a-Cor2 (DepthTwoLinkAddresses)**: Establishes `#E(a) = 2` under the discipline, narrowing L1b's substrate admission `#E ≥ 2`.

**Problem**: No concrete example illustrates what a non-disciplined link emission with `#E > 2` would look like, so the practical content of "discipline narrows from `≥ 2` to `= 2`" isn't grounded. The Worked Sketch verifies discipline-conforming addresses but doesn't exhibit a counterfactual non-disciplined emission.

**Required**: Add a one-line counterexample address (e.g., `1.0.1.0.1.0.2.1.5`) that satisfies L1c but would land at `#E = 3`, to motivate why R0a-Cor2 is a substantive narrowing.

### Issue 8: SharedDepthOneAllocator lemma placement

**ASN-0086, Setup, "SharedDepthOneAllocator" lemma**: A multi-step structural T10a lemma is wedged into the Setup section alongside definitions.

**Problem**: Setup mixes hypotheses (s_C-resident, s_C ≠ s_L), definitions (zero-count depth, allocator-tree depth, →, ↦, ↝, Frame conditions, Substrate emission primitive, Extension, AddressUniverse, Partition, TypeCatalog), AND a derived lemma with proof. The reader cannot tell what is given vs. what is derived without re-reading.

**Required**: Promote SharedDepthOneAllocator to a separate section or to the Properties Introduced table; keep Setup limited to non-derived material.

## OUT_OF_SCOPE

### Topic 1: Multi-arity link nullification

The note restricts attention to standard-triple links throughout, with `L_K` defined only over arity-3 entries. Nullify's effect on `A_K^{(n)}` for higher arities is correctly deferred to Open Questions.

**Why out of scope**: Genuine future-ASN territory; not an error here.

### Topic 2: Cross-layer type catalog coordination

The Open Questions note "Can higher layers extend the type catalog T_cat dynamically without coordination, given L9 (TypeGhostPermission), and what happens when two layers independently choose colliding type addresses?"

**Why out of scope**: Multi-layer coordination is downstream of the relational-substrate definition. ASN-0086 correctly defers.

### Topic 3: Atomicity / consistency model

Whether Emit is atomic with respect to concurrent Observe is in Open Questions.

**Why out of scope**: Concurrency semantics are a separate concern.

VERDICT: REVISE
