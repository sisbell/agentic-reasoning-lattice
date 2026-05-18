# Review of ASN-0086

## REVISE

### Issue 1: R7a proof doesn't handle multi-emission composites in `↝`

**ASN-0086, R7a proof**: "Setting `(F, G, K) := Σ'.L(a)` for the fresh `a ∈ dom(Σ'.L) \ dom(Σ.L)`, the class-(iii) step `Σ → Σ_iii` emitting `(F, G, K)` at `a` yields `Σ_iii.L = Σ'.L`."

**Problem**: The claim quantifies over `↝` (categorical, ranging over any-layer operations), but the proof uses "the fresh `a`" (singular). For a multi-emission composite operation in some higher layer producing `Σ'.L = Σ.L ∪ {a₁ ↦ v₁, a₂ ↦ v₂}` with two fresh keys, no single class-(iii) step matches. The earlier prose "its `Σ.L`-affecting sub-effect decomposes into one" is ambiguous — "one" reads as singular and the technical existence claim "there exists a class-(iii) `→`-step `Σ → Σ_iii` with `Σ_iii.L = Σ'.L`" only fires for single-key extensions. Note: the proof's earlier sentence "any `Σ ↝ Σ'` with `Σ.L ≠ Σ'.L` must extend `dom(Σ.L)` by at least one fresh address" explicitly admits multi-key extensions.

**Required**: Either restrict R7a's domain to single-emission `↝`-transitions (single fresh key in `dom(Σ'.L) \ dom(Σ.L)`), or generalize the conclusion to "there exists a finite sequence of class-(iii) `→`-steps `Σ = Σ_0 → Σ_1 → ... → Σ_n` with `Σ_n.L = Σ'.L`" with the proof adapted accordingly.

### Issue 2: R0 Step 4 bundles invariants with incorrect justification

**ASN-0086, R0 Step 4**: "*L-invariants preserved by the class-(iii) Frame.* `Σ'.C = Σ.C` and `Σ'.M = Σ.M` substitute through every predicate whose free variables draw only from `(Σ.C, Σ.M)`: L12, L12a, L12b, L-fin, and every ASN-0036 S-invariant hold by input-substitution."

**Problem**: L12, L12a, L12b, and L-fin have free variables in `Σ.L` or `Σ'.L`, not just `(Σ.C, Σ.M)`:
- L12 (LinkImmutability): quantifies over `dom(Σ.L)` with conclusion on `Σ'.L(a)`
- L12a (LinkStoreMonotonicity): `dom(Σ.L) ⊆ dom(Σ'.L)`
- L12b (HomeDocumentPersistence): `{home(a) : a ∈ dom(Σ.L)} ⊆ dom(Σ'.M)` — `home` reads `Σ.L`
- L-fin (LinkStoreFiniteness): `|dom(Σ.L)| < ∞`

The justification "by input-substitution on (Σ.C, Σ.M)" doesn't apply to these. The actual preservation mechanism is the class-(iii) Frame's value-preservation clause (`Σ'.L = Σ.L ⊕ {a ↦ (F, G, K)}` — preserving existing keys) and single-key extension structure, not substitution through `(Σ.C, Σ.M)`. The conclusion holds, but the cited justification is wrong.

**Required**: Separate the justification. L12 and L12a follow from the Frame's single-key value-preserving extension definition. L12b follows from `dom(Σ'.M) = dom(Σ.M)` (frame) plus L12b at Σ. L-fin follows from finiteness closure under single-element union. Only the ASN-0036 S-invariants (which have free variables purely in `(Σ.C, Σ.M)`) follow by genuine input-substitution.

### Issue 3: Meta-prose accumulation around forward references

**ASN-0086, multiple locations**: The note has the `review-mode.anti-bloat` classifier, and several paragraphs match the flagged patterns.

**Problem**: Specific forward-reference instances:

(a) Frame conditions paragraph, final sentence: "R0's role below is to discharge the existential of a `→` step satisfying L0/L1/L1a/L1b/L1c/L3, not to derive the frame conditions on `Σ.C` and `Σ.M`, which are part of (iii)'s definition; R0 Step 4 invokes the frame definitionally when setting `Σ'.C := Σ.C` and `Σ'.M := Σ.M`." — describes R0 before R0 is stated.

(b) Sibling-frontier discipline definition, final sentence: "R0a introduces the discipline-restricted reachability relation `→_D` (transitions whose class-(iii) steps respect the discipline) as the quantifier range of its sibling-stream invariant." — forward-references R0a's mechanism within the discipline definition.

(c) Setup "Discipline-conditional claims" paragraph: enumerates which claims depend on which hypothesis. The same information appears tagged in each claim's own statement and in the Properties Introduced table — three locations for the same tracking.

(d) R0a preamble: "R0a is Setup-free in its dependence on the foundation ASNs but discipline-conditional on the implementation's emission policy; the conditionality propagates to Nullify's single-tuple-scope guarantee." — restates per-claim tags in introductory framing.

The same "the substrate primitive in isolation admits broader X" framing appears in the sibling-frontier discipline definition, in R0a's claim text, in Nullify's "Crafted-span retractions" note, and in Emit_K's "A_K^{Σ'} membership" note.

**Required**: Remove the forward references (a), (b). Condense (c) or remove it (per-claim tags suffice). Trim (d) to the substantive content (Setup-free vs. discipline-conditional split). Consolidate the repeated "substrate primitive admits broader" framing to one canonical location.

### Issue 4: R0a Stage 1's "covered by the same argument with roles swapped"

**ASN-0086, R0a Stage 1**: "The reverse direction `a' ⊀ a` (under `d ≠ d'`) is covered by the same argument with roles swapped: instantiating the derivation at `(a', a)` yields the symmetric contradiction."

**Problem**: This is right at the boundary of "no proof by similarly." The argument *is* genuinely symmetric in `(a, a', d, d')`, but the symmetry claim is asserted rather than demonstrated. Given that the cross-home sub-argument is load-bearing for the unconditional half of R0a, the reverse direction deserves at least one explicit sentence naming the symmetry (e.g., "by the symmetry of the derivation in `(a, a', d, d')` — every step's conclusion is symmetric under swap, no step relies on which side is named `a`").

**Required**: Either expand the reverse-direction discharge to one sentence naming the symmetry explicitly, or fold both directions into a single derivation parameterized symmetrically from the start.

### Issue 5: R0a-Cor1 induction step doesn't handle the new-document class-(i) case explicitly

**ASN-0086, R0a-Cor1 induction step**: "Classes (i) and (ii) leave `dom(Σ.L)` unchanged (Frame), preserving the invariant."

**Problem**: Class-(i) transitions extend `dom(Σ.M)` with a fresh document `d_new`. For this new `d_new`, the invariant must hold at Σ' even though no prior `J_{d_new}^Σ` was defined. The argument is straightforward (the homed set under `d_new` is empty at Σ', so `J_{d_new}^{Σ'} = -1`), but the proof glosses this rather than handling it. The "the invariant" being preserved should be quantified explicitly over `d ∈ dom(Σ'.M)`, which is a superset of `dom(Σ.M)`.

**Required**: One sentence in the class-(i) sub-case: "for any fresh `d_new ∈ dom(Σ'.M) \ dom(Σ.M)`, the homed set `{a ∈ dom(Σ'.L) : home(a) = d_new} = ∅` (no link is homed at `d_new` yet), so set `J_{d_new}^{Σ'} = -1` and the invariant holds at `d_new` vacuously."

### Issue 6: Definition of `Emit_K` — case B seed-independence depends on R0a-Cor1, which is discipline-conditional

**ASN-0086, Emit_K Definition**: "Since `Emit_K` commits to R0 Step 2's construction by signature, every `Emit_K`-induced trace respects the sibling-frontier discipline, and R0a (otherwise conditional) applies unconditionally within `Emit_K`'s semantics."

**Problem**: The seed-independence argument in Case B's analysis uses R0a-Cor1 to conclude `j = J_d^Σ + 1`. R0a-Cor1 is itself discipline-conditional — its proof induction relies on each `→`-step being disciplined. The note argues circularly that "Emit_K commits to R0 Step 2's construction by signature... so R0a applies unconditionally within Emit_K's semantics." But R0a-Cor1's premise is that *every* class-(iii) step along the reachability chain reaching Σ is disciplined, not just the present Emit_K step. If `Σ` was reached via undisciplined emissions (some other layer or operation calling the broader substrate primitive), R0a-Cor1 doesn't hold at Σ, and Emit_K's seed-independence breaks at this Σ regardless of Emit_K's own discipline.

**Required**: Clarify that Emit_K's seed-independence (and hence its function-ness) requires the *entire trajectory* reaching Σ to be disciplined, not just Emit_K itself. Either state this as an additional precondition on Emit_K, or restrict Emit_K's domain to states `Σ` reachable by disciplined trajectories, or weaken to "Emit_K's output is a function of (Σ, d, F, G) on the disciplined-reachable sub-domain of Σ."

### Issue 7: SharedDepthOneAllocator lemma — naming `A_{d.0.1}` before subspace labels are pinned

**ASN-0086, SharedDepthOneAllocator step (d)**: "The depth-2 allocators `A_{d.0.s_C.1}` and `A_{d.0.s_L.1}` are opened by *distinct* spawn pairs `(d.0.s_C, 1) ≠ (d.0.s_L, 1)` (parent tumblers distinct by L0 + the subspace-distinctness hypothesis)..."

**Problem**: The naming convention `A_x` is "the allocator whose first emission is `x`" (per Setup), but the lemma uses `A_{d.0.s_C.1}` and `A_{d.0.s_L.1}` to name two distinct allocators whose first emissions differ by `s_C` vs. `s_L`. The lemma asserts these allocators *exist*, but the existence requires both `(d.0.s_C, 1)` and `(d.0.s_L, 1)` spawn pairs to have actually fired in some history. The lemma doesn't establish existence — it characterizes structure assuming they exist. This makes step (d)'s "independence" claim a conditional structural claim, not an existence assertion.

**Required**: Clarify that step (d) asserts conditional structure ("*If* both depth-2 subspace-specific allocators have been opened, they evolve independently") rather than unconditional existence. Or strengthen by noting that R0 Step 2 Case A's emission opens `A_{d.0.s_L.1}` whenever the first link is sited at `d`, and the symmetric content-side argument opens `A_{d.0.s_C.1}`.

### Issue 8: `Σ_0` in R0a's hypothesis — implicit assumption

**ASN-0086, R0a statement**: "Under the discipline (every class-(iii) `→`-transition along the reachability chain is `→_D`-admissible), `dom(Σ.L)` is a tumbler-prefix antichain at every reachable state: `(A Σ : (E Σ_0 : dom(Σ_0.L) = ∅ ∧ Σ_0 →_D* Σ) :: ...)`."

**Problem**: The quantifier requires the existence of *some* Σ_0 with `dom(Σ_0.L) = ∅` from which Σ is reachable. Is this guaranteed for every state of interest? The induction is on `→_D*`-chain length from Σ_0, so this is implicitly an initial-state assumption. The note doesn't establish that every reachable state has such an antecedent — and indeed, a "midstream" state (e.g., a state in which links were already present without an empty-link-store antecedent) wouldn't satisfy this premise.

**Required**: Either (a) make the initial-state assumption explicit (every reachable Σ has an empty-link-store ancestor in its reachability past), or (b) shift the induction's base case to a non-empty initial condition with a stated invariant that the discipline-restricted reachability respects.

## OUT_OF_SCOPE

### Topic 1: Multi-arity link relations

The note restricts attention to standard-triple links with `|Σ.L(a)| = 3`. L3 admits arity `≥ 3`. Extending `L_K^{(n)}` to higher arities, formalizing slot positions beyond the standard triple, and re-deriving R6a/R6b/R6c for multi-arity retractions is significant additional work.

**Why out of scope**: This is signaled as future work via the explicit scope-restriction note and an Open Question. The current note's content is complete on its restricted domain.

### Topic 2: Higher-layer concurrency semantics

The Open Questions raise atomicity (Emit vs. concurrent Observe) and consistency models. These are layered concerns above the substrate.

**Why out of scope**: The substrate model is sequential by construction (each `→`-step is atomic). Concurrency is a higher-layer concern.

### Topic 3: Substrate-level elevation of the sibling-frontier discipline

The Open Questions ask whether the discipline should be elevated to a substrate-level guarantee, making R0a unconditional and discharging Nullify's P3 automatically.

**Why out of scope**: Acknowledged as a design tradeoff and explicitly listed for future consideration.

### Topic 4: Relaxation to deeper-sited link addresses

The Open Questions raise the relaxation to admit `#E ≥ 3` (Nelson's foundational design).

**Why out of scope**: Acknowledged as a substantial structural rework requiring re-derivation of R0a, Nullify's scope guarantee, and related claims.

### Topic 5: L14's native scoped form without the Setup hypothesis

The Open Questions raise the slice-wise reformulation under L14's native scoped form.

**Why out of scope**: Setup commits to globally `s_C`-resident content, which simplifies R0, R4, R5; the slice-wise variant is a future generalization.

VERDICT: REVISE
