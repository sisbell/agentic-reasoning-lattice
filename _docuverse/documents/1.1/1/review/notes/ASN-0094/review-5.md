# Review of ASN-0094

## REVISE

### Issue 1: Catalog internally inconsistent with Sh5's organizing claim

**ASN-0094, The Canonical Shape Catalog**: Coverage and Comment both register at shape `(1, 1, A_doc, A_doc, ⊥)`, yet the catalog lists divergent template families (`latest_K_for_addr(d)` for Coverage; `unresolved_K_comments_via(K_res, d)`, `all_K_resolved_via(K_res, d)` for Comment).

**Problem**: Sh5 META commits to "templates depend only on (i) the shape components, (ii) K's name, and (iii) explicitly named layer-supplied accessors — never on per-K design freedom beyond those." Two rows with identical `(c_F, c_G, t_F, t_G, idem)` tuples must therefore share base template family. The catalog as presented shows identical shape tuples generating different templates, with per-K commitments (SingleHomeCoverageDiscipline; K_res parametricity) hidden as parenthetical caveats rather than load-bearing distinctions. The Open Questions section acknowledges this tension but the catalog still reads as if shape uniquely determines templates.

**Required**: Either (a) restructure each catalog row to separate *base templates* (forced by shape: `pair_K`, `from_K`, `to_K`, `from_addrs_K`, `to_addrs_K` for any `(1, 1, A_doc, A_doc, _)` shape) from *opt-in extensions* (forced by per-K discipline), mirroring how FunctionalDependencyDiscipline already factors out `K_target_of` from DirectedPair's base; or (b) promote per-K commitments to a shape-tuple component so `(1, 1, A_doc, A_doc, ⊥, SingleHome)` and `(1, 1, A_doc, A_doc, ⊥, ResolverParametric)` become structurally distinct rows. The present arrangement makes Sh5's claim unfalsifiable: any catalog divergence can be hand-waved as "different (iii)".

### Issue 2: FunctionalDependencyDiscipline preservation proof omitted

**ASN-0094, FunctionalDependencyDiscipline**: "Preservation under the discipline follows the same inductive argument as Sh4's layer-discipline contract, with the candidate set widened to all from-slot matches; the simultaneous-addition-and-contraction case (Sh4 Case D) carries over verbatim when K is itself the retraction relation. We omit the proof; the structure is identical to Sh4's."

**Problem**: The structure is *not* identical. FDD's shape constraint forces K to be DirectedPair `(1, 1, A_doc, A_doc, ⊤)`; Retraction has shape `(*, 1, A, A_rel, ⊤)`. So K ≁ R for any FDD-registered K, and Sh4's Case D (simultaneous addition+contraction at K ~ R) cannot fire for FDD. The proof has Cases A, B, C only — strictly simpler than Sh4's. Additionally, "widened to all from-slot matches" is the wrong direction: `C_fd ⊇ C` makes FDD a *stricter* gate than Sh4, not a relaxation; the phrasing suggests the opposite.

**Required**: State explicitly: "FDD's preservation argument runs Cases A, B, C identically to Sh4's; Case D does not arise because FDD's shape constraint precludes K ~ R, so no `Emit_K` step can simultaneously add to A_K and nullify K-tuples." Replace "widened" with "broadened" or "loosened in scope but strictened as a gate".

### Issue 3: AllocatedAddressAntichain — E(x) ≼ E(a) step elided

**ASN-0094, AllocatedAddressAntichain proof, Case 3**: "prefix `x ≼ a` with both element-level forces T4b's E-projection to satisfy `E(x) ≼ E(a)`, hence `E(x).1 = E(a).1`."

**Problem**: The step requires two sub-arguments not shown. Given x ≼ a with `zeros(x) = zeros(a) = 3`:
- The three zeros of x (at positions n_1 < n_2 < n_3 ≤ #x) are *the only* zeros of a — because any additional zero in a at position > #x would push `zeros(a) ≥ 4`, contradicting `zeros(a) = 3`.
- E-field of x starts at n_3 + 1 and ends at #x; E-field of a starts at n_3 + 1 and ends at #a. By x ≼ a, components agree on positions 1..#x, hence E(x) agrees with E(a) on the first #x − n_3 = #E(x) positions.

Neither sub-step is named. A Dijkstra-rigor proof should expose both, because the load-bearing fact is that the *zero-positions* of x and a coincide, not just that some E-field prefix relation holds abstractly.

**Required**: Make the derivation explicit: from `zeros(x) = zeros(a) = 3 ∧ x ≼ a` derive that x's three zero positions are also a's three zero positions (the only ones), then conclude E(x) ≼ E(a) from componentwise agreement on positions ≤ #x.

### Issue 4: "depth-2 span" terminology misuses δ's parameters

**ASN-0094, Worked Example, Rejection case 1**: "`F_3 = {(d_1, δ(2, #d_1))}` — a depth-2 span violating canonical-slot form, which requires unit-depth displacements `δ(1, #x)`."

**Problem**: By OrdinalDisplacement (ASN-0034), `δ(n, m) = [0, ..., 0, n]` of length m. The parameter m is the depth (length / nesting); n is the increment / width at the last component. `δ(2, #d_1)` is a *width-2* displacement, not depth-2 — both `δ(1, #d_1)` and `δ(2, #d_1)` have the same depth (#d_1); they differ in the last-component value. The coverage `{t : d_1 ≤ t < d_1 ⊕ δ(2, #d_1)}` is two adjacent unit-depth subtrees, not a single subtree "at depth 2".

The framework's "unit-depth" naming for δ(1, #x) compounds the confusion: "unit-depth" reads as "depth 1" but actually means "increment 1 at the action point of depth #x".

**Required**: Rename "depth-2 span" to "width-2 displacement" or "increment-2 displacement". Optionally reconsider the "unit-depth" naming — perhaps "unit-increment span" or "atomic span" — though that ripples through ASN-0086 references and may be out of scope.

### Issue 5: "three structural gates" inconsistent with Sh-conf's four clauses

**ASN-0094, Worked Example, Rejection case 3**: "Cardinality is the second of Sh-conf's three independently-checked structural gates (canonical form, cardinality, target domain)".

**Problem**: Sh-conf is defined with four clauses (a, b, c, d). Clauses (a) and (b) check canonical form for F and G separately — the text collapses them into a single "canonical form" gate without prior consolidation. A reader counting clauses sees four; a reader tracking gates sees three. Failure modes also differ: F-only canonical failure vs. G-only canonical failure are distinguishable at the clause level, blurred at the gate level.

**Required**: Either fold the consolidation explicitly into Sh-conf's definition ("clauses (a) and (b) jointly form the canonical-form gate; (c) the cardinality gate; (d) the target-domain gate") or count consistently as four throughout the worked examples.

### Issue 6: SingleHomeCoverageDiscipline emission_order well-definedness depends on shared-chain reasoning that isn't tight

**ASN-0094, Coverage walkthrough**: "emission_order(τ) := the chain-index of addr(τ) within the link sub-allocator chain at d_K".

**Problem**: When d_K hosts emissions of multiple distinct types (Coverage K plus other relations also homed at d_K), the link sub-allocator chain at d_K interleaves K-tuples and non-K-tuples. The chain-index of K-tuples is then *not contiguous* — chain indices 0, 2, 5 might be K while 1, 3, 4 are other relations. The ASN's argument for (ii) injectivity and (iii) chain-index-equals-T1-order holds on the full chain, hence holds on the K-subset, so `argmax` is still well-defined; but the text doesn't address this case at all — it argues only about d_K's full chain enumeration, leaving readers to verify that subset behavior preserves the argmax.

**Required**: Add one sentence: "Under SingleHomeCoverageDiscipline, K's tuples form a (possibly non-contiguous) subset of the chain enumeration at d_K; chain-index injectivity and T1-monotonicity transfer to any subset, so argmax over `S_d ⊆ K-tuples` remains well-defined." Otherwise a reader reasonably asks whether d_K must host *only* K (which would be a much stronger commitment than what's actually needed).

### Issue 7: Sh4 contract's atomicity scope justification missing for cross-class retraction

**ASN-0094, Sh4 — layer-discipline contract**: "The layer commits to executing clauses (i)–(iii) atomically with respect to other Sh4-emitters at the same `~`-equivalence class of K".

**Problem**: The scope `~`-class is justified intuitively but not argued. Concurrent `Emit_R` (when R ≁ K) can transition some τ ∈ A_K^Σ out of A_K, racing with Emit_K's Observe-then-commit. The proof of Sh4 preservation should either argue that this race is benign (because Sh4 only constrains pairs within A_K, and removing τ from A_K never *creates* a Sh4 violation) or expand the atomicity scope. The text takes the first position implicitly without stating it.

**Required**: Add one sentence in Sh4's contract discussion: "Cross-`~`-class concurrency (e.g., concurrent Emit_R retracting K-tuples while Emit_K is in flight) does not require serialization, because the only mutation Emit_R applies to A_K is removal — removing a tuple from A_K cannot violate the pairwise-slot-pair-distinctness condition, only restore it."

## OUT_OF_SCOPE

### Topic 1: Tuple-DirectedPair and other bipartite catalog rows
**Why out of scope**: The catalog enumerates current needs; bipartite mirrors (Tuple-DirectedPair, non-idempotent Resolution, etc.) are extension territory acknowledged in the Open Questions. Not errors in this ASN.

### Topic 2: Ghost slot addresses
**Why out of scope**: Sh-conf forbids ghosts in slots by design; relaxation is a deliberate future-shape question acknowledged in Open Questions.

### Topic 3: T_cat evolvability over substrate lifetime
**Why out of scope**: Lifetime constancy is a stated commitment; evolution semantics belong to a substrate-lifecycle ASN.

### Topic 4: (0, 0) shapes, c_F = 0|1, composite shapes
**Why out of scope**: All listed in Open Questions as future shape-family extensions.

VERDICT: REVISE
