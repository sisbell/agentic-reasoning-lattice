# Review of ASN-0094

## REVISE

### Issue 1: Sh1, Sh2, Sh3 proofs use "by similar reasoning" instead of explicit case enumeration

**ASN-0094, Sh1 proof**: "*Proof.* By induction on `↦*`. Case A by case-equation. Case B: Sh-conf clauses (b) and (c) discharge canonical-slot form and cardinality match on the new tuple. ∎"

**Sh3 proof**: "*Proof.* Mirrors Sh2 with F → G, clauses (b) and (d). ∎"

**Problem**: Sh0's proof enumerates four sub-classes of ↦-steps preserving the case-equation in Case A (K.σ/K.α, K.λ at K'≁K with two sub-regimes, arrangement-modifying). Sh1/Sh2/Sh3 contract this to one-liners. "Case A by case-equation" hand-waves over the question of *which* ↦-steps satisfy the equation. A Dijkstra-style proof either spells out the same enumeration or factors the shared inductive step into a named lemma. The current text does neither.

**Required**: Either restate Case A's sub-class enumeration in each of Sh1/Sh2/Sh3, or extract the shared "case-equation preserving step" as a separately stated lemma that all four invoke.

### Issue 2: Lemma — RetractionSelfFreshness omitted from Properties Introduced table

**ASN-0094, Properties Introduced**: The "Load-bearing claims" table lists Sh-conf, Sh0–Sh4, SlotAccessorTotality, AllocatedAddressAntichain, LinkAddressNotPrefixOfEmit, EffectiveWpSimplification, NullifyActiveSubsetCompatibility, and three contracts.

**Problem**: Lemma — RetractionSelfFreshness is load-bearing (it's invoked in Sh4's Case D analysis to dispatch the K ~ R simultaneous addition-and-contraction case, and in NullifyActiveSubsetCompatibility's Case A to discharge `addr(τ_new) ∉ nullified(Σ')`). The omission is inconsistent with the table's stated purpose.

**Required**: Add RetractionSelfFreshness to the load-bearing claims table.

### Issue 3: K = comment walkthrough doesn't exercise NonIdempotentDirectedPair's defining feature

**ASN-0094, Worked Example: K = comment**: Emissions 1 and 2 have F₁={d_1}, G₁={d_2} and F₂={d_2}, G₂={d_2} — *different* slot-pairs.

**Problem**: The defining feature of NonIdempotentDirectedPair vs DirectedPair is that two emissions with *identical* slot-pairs both produce distinct active tuples (no Sh4 suppression at idem = ⊥). The walkthrough's two emissions have distinct slot-pairs, so they'd be admitted by DirectedPair too. The walkthrough doesn't distinguish the shape from its idempotent sibling.

**Required**: Add an emission with the same slot-pair as Emission 1 (F = {d_1}, G = {d_2}), demonstrating that a distinct τ_1' is admitted at a fresh address with `addr(τ_1') ≠ addr(τ_1)` despite identical slot content. Show the resulting template evaluations include both τ_1 and τ_1' in `from_K(d_1)` and `to_K(d_2)`.

### Issue 4: CallerSideClassification numbering inconsistency with Gate Ordering

**ASN-0094, Definition — CallerSideClassification**: "the following six side-effect-free checks in order, halting at the first failure to identify the rejecting gate (numbering mirrors the *Gate Ordering (consolidated)* below)"

**Problem**: CallerSideClassification has 6 numbered checks (1. Registry, 2. Single-home, 3. Canonical-form, 4. Discipline-suppression, 5. Cardinality, 6. Target-domain). The "Gate Ordering (consolidated)" has 5 numbered gates (1. Single-home, 2. Canonical-form, 3. Per-K, 4. Cardinality/target-domain, 5. K.λ). Registry isn't a separate gate in the consolidated ordering, and the consolidated version bundles cardinality+target-domain as one gate. The "numbering mirrors" claim doesn't hold.

**Required**: Either renumber so the two enumerations literally align, or remove the "numbering mirrors" claim and explain how the two enumerations differ.

### Issue 5: Lemma — RetractionSelfFreshness placement disrupts Sh4 proof structure

**ASN-0094, Sh4 section**: The Lemma — RetractionSelfFreshness block is inserted between "Preservation under the contract" (the proof's setup paragraph) and "*Base.*" (the proof's actual base case).

**Problem**: Embedding a substantial named lemma mid-proof makes the inductive structure harder to follow. The lemma is used downstream in Sh4's Case D and in NullifyActiveSubsetCompatibility — it should be stated as a top-level lemma before Sh4's proof setup, then cited at each use site.

**Required**: Hoist Lemma — RetractionSelfFreshness to a separate top-level section (analogous to AllocatedAddressAntichain's placement), then have Sh4 Case D and the Nullify Compatibility section cite it.

### Issue 6: AllocatedAddressAntichain Lemma's usage points not explicitly cited

**ASN-0094, AllocatedAddressAntichain Lemma**: "The lemma underwrites the syntactic-to-semantic bridge: a canonical-slot endset at an allocated address `x` denotes exactly `{x}` among allocated addresses..."

**Problem**: The Lemma is described in prose as foundational but isn't cited at any specific proof step in Sh0–Sh4, the contracts, or the slot accessor definitions. FDD's contract correctness paragraph says "By the same AllocatedAddressAntichain argument used in Sh4's contract" — but Sh4's contract correctness paragraph itself does not cite AllocatedAddressAntichain directly; it relies on the explicit post-filter mechanism. Either the Lemma is load-bearing somewhere and its citation is missing, or it's documentation that should be relocated to a Notes section.

**Required**: Either pin AllocatedAddressAntichain's citations to the specific proof steps that require it (most likely: the slot-accessor totality argument and the contract over-approximation tightening), or restate the Lemma's role as informative rather than load-bearing.

### Issue 7: Decidability of coverage-equality on finite span sets — procedure without rigorous derivation

**ASN-0094, TypedRelationCatalog Definition, *Decidability of coverage-equality on finite span sets***: "(1) compute both endpoint sets (T1, TumblerAdd); (2) sort their union under T1 (T2) into intervals delimited by consecutive endpoints; (3) test each delimited interval for membership in each coverage via a representative point (T1/T2); (4) equality holds iff every delimited interval has matching outcomes. The procedure is polynomial in `n + n'`..."

**Problem**: The procedure correctness depends on coverage being a finite union of half-open intervals under T1, but `coverage({(x, δ(1, #x))}) = {t : x ≼ t}` is *unbounded above* (no top element in T). The procedure's "intervals delimited by consecutive endpoints" doesn't obviously handle unbounded intervals. The polynomial complexity claim has no supporting argument. This is the load-bearing decidability that makes `K ∈ T_cat` testable.

**Required**: Either show explicitly how the procedure handles unbounded subtree intervals (covering "from start to next sibling/parent boundary"), or cite a foundation lemma that establishes the decidability with proof.

### Issue 8: Common rejection patterns preamble doesn't reference where pattern 6 is derived

**ASN-0094, Per-Shape Template Walkthroughs preamble**: "Walkthroughs cite these patterns by number; the Comment walkthrough below derives patterns 1–4 in full as canonical references, with pattern 5 derived first at Classifier."

**Problem**: Pattern 6 (per-K-discipline-suppression rejection) is exercised in the BundledDirectedPair walkthrough ("Sh4 suppression on a duplicate empty-G attempt"), but this preamble doesn't mention it. A reader scanning for canonical pattern derivations may miss pattern 6's location.

**Required**: Extend the preamble to mention pattern 6's derivation in BundledDirectedPair.

### Issue 9: Sh-conf's "regardless of clause (d)" argument lacks structural support

**ASN-0094, Sh4 idempotency contract, *Contract correctness***: "`C(F, G, Σ)` equals the specified set regardless of Sh-conf clause (d): the post-filter (i.b) tests exact slot-address-set equality, and any τ in the specified set passes both (i.a)'s Observe (by Prefix reflexivity on each pattern address) and (i.b)'s filter."

**Problem**: The phrase "regardless of clause (d)" elides that the contract fires at gate 3, *before* gate 4 (cardinality/target-domain). The argument needs to show that the post-filter (i.b) handles the case where slot_addrs(F) contains addresses not in t_F^Σ — which can occur because clause (d) hasn't fired yet. The current text gives one sentence; the AllocatedAddressAntichain Lemma is what closes the over-approximation gap when clause (d) holds, but the contract is supposed to be correct *without* clause (d). The explicit argument for that case is sparse.

**Required**: Show explicitly the contract's correctness when Sh-conf clause (d) fails (i.e., when some slot address is unallocated): the Observe over-approximates more broadly, but the post-filter (i.b) still produces `C(F, G, Σ)` exactly. Walk through a concrete unallocated-pattern scenario.

### Issue 10: BundledDirectedPair walkthrough's "alternative continuation" notation conflates state-tree positions

**ASN-0094, BundledDirectedPair worked example**: "consider the parallel branch from the same `Σ_0` that the main timeline started from: fire `Emit_K(Σ_0, home_cite, F_BDP0, G_BDP0)`... Result Σ_0a..."

**Problem**: Σ_0a is a *successor* of Σ_0 (reached by emitting BDP0 from Σ_0), but the subscript "0a" suggests it's a sibling of Σ_0 at the initial level. The "parallel branch" language describes a parallel exploration in the proof author's reasoning, not parallel reachability in the state graph (which is sequential under ↦). This conflates state-tree position with proof-narrative branching.

**Required**: Either rename Σ_0a to Σ_1' (or similar) to make the successor relationship explicit, or rewrite the prose to clarify that "parallel" refers to the proof's narrative choice, not the state structure.

### Issue 11: The Sh-conf "Initial-State Baseline" section conflates Σ_0 and Σ_init in proof text

**ASN-0094, Initial-State Baseline**: "Sh0–Sh4 presuppose `L_K^{Σ_init} = ∅` for every `K ∈ T_cat`. References to `Σ_0` in proofs denote this `Σ_init`."

But the worked example: "The walkthrough's `Σ_0` is reached from `Σ_init` by a finite sequence of K.σ/K.α steps (no K.λ-steps), so `dom(Σ_0.L) = ∅`."

**Problem**: The framework uses Σ_0 in two distinct senses — as Σ_init in preservation proofs and as a pre-emission post-K.σ/K.α state in worked examples. The conflation is documented but creates cognitive load. A reader stepping through Sh0's proof "At `Σ_0 = Σ_init`..." then reading the comment walkthrough "From Σ_0..." has to dispatch on context.

**Required**: Use Σ_init in preservation-proof text and reserve Σ_0 for worked-example pre-emission states. Or introduce distinguishing notation (Σ_init for the framework baseline, Σ_0 for walkthrough setup).

## OUT_OF_SCOPE

### Topic 1: Multi-process atomicity for the contracts
**Why out of scope**: Already flagged in Open Questions as a scope boundary. The framework's commitment to single-process substrates is explicit. Extending to multi-process would be a new layer atop this one.

### Topic 2: Ghost-targeting slot semantics
**Why out of scope**: Already in Open Questions. Whether future shapes admit slot addresses outside A^Σ at emission time is a separate design decision.

### Topic 3: Document-container target symbol A_M
**Why out of scope**: Already in Open Questions. Adding A_M to the target-domain vocabulary would re-enable metalink-style targeting; it's a registry extension, not a flaw in the current framework.

VERDICT: REVISE
