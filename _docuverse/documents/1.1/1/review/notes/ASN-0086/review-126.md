# Review of ASN-0086

This note has clearly converged on its mathematical core — R0/R0a/R0a-Cor1/Cor2, R7a, and the WP analysis are sound, and the prior-declined SFD/Σ_D findings are correctly retired. My findings are concentrated where the `review-mode.anti-bloat` classifier directs: meta-prose and forward-reference accretion that the precise reader must skip past. One genuine logical-grounding nit is included.

## REVISE

### Issue 1: Repeated scope-refrain accretion throughout R0's proof
**ASN-0086, R0 proof**: "so that the argument carries over to every state-local-conforming state in the operations' domain (Definition — state-local-conforming state), not merely the `→*`-reachable ones"
**Problem**: The phrase "at every state in the operations' domain" and the "not merely the `→*`-reachable ones" disclaimer recur five-plus times across the first-emission bullets, subsequent-emission bullets, and the L-invariant-preservation paragraph. Each restates the same scope fact. This is the compounding forward-reference pattern: the same defensive justification re-asserted at every sub-step rather than once.
**Required**: State the scope claim once (R0 is proved over the state-local-conforming domain by avoiding ASN-0093's reachability-restricted lemmas) and delete the per-bullet repetitions.

### Issue 2: Defensive use-site inventory after R0's statement
**ASN-0086, R0**: "The conformance hypothesis is load-bearing — the freshness discharges below consume the state-local invariants L0, L1c, and L-fin."
**Problem**: This sentence inventories which invariants the downstream proof consumes before the proof runs. It does not advance the claim; the proof itself shows what it uses. This is the "definition's introduction enumerates downstream consumers" pattern.
**Required**: Delete. The proof's own citations make the dependency visible at the point of use.

### Issue 3: Cross-subspace freshness paragraph duplicated verbatim across R0's two branches
**ASN-0086, R0 proof**: the *Freshness against `dom(Σ.C)`* (first branch) and *Cross-subspace freshness* (subsequent branch) bullets are word-for-word identical ("`E(b)₁ = s_C` (L0) … `s_L ≠ s_C` (SC-NEQ) … T7 (SubspaceDisjointness) gives `a ≠ b`").
**Problem**: The two branches differ in their *home/within-home* arguments but the cross-subspace argument is independent of which branch fired. Repeating it verbatim is the "two paragraphs say the same thing" pattern.
**Required**: Factor the cross-subspace exclusion into a single sentence shared by both branches.

### Issue 4: Mutual deferral between Nullify's Definition and WP Case 1
**ASN-0086, Definition — Nullify** ("Single-tuple scope under R0a") and **WP Case 1** each prove/defer single-tuple scope, and the Properties table entry for Nullify points to "WP Case 1," while WP Case 1 points back to "the result proved under R0a in the Definition of Nullify."
**Problem**: This is the "multiple paragraphs defer to the same downstream location" pattern, here closed into a citation loop. A reader following either entry is bounced to the other.
**Required**: Prove single-tuple scope in exactly one location and have the other cite it one-directionally.

### Issue 5: Notation-justification prose
**ASN-0086, Definition — Reachability**: "We use `→*` and never `⊑`/`⊒` for it, to avoid colliding with ASN-0043's notation."
**Problem**: Prose justifying a notation choice rather than advancing reasoning. The `↝`/`→`/`→*`/`↝*` four-relation apparatus carries several such defensive distinctions ("distinct from ASN-0043's store-extension relation `⊒`," etc.).
**Required**: Pick the symbols and use them; drop the justification sentences. A one-line notation table at most.

### Issue 6: `→`-completeness derived from the wrong direction
**ASN-0086, State transition relation / Arrangement modification**: "Under M2 every document's arrangement is empty at every reachable state, so the substrate admits no arrangement-modifying transition — `→` is the complete dom-extending vocabulary."
**Problem**: This infers "no arrangement-modifying transition exists" *from* the invariant M2 (arrangements always empty). The dependency runs the other way: M2 holds *because* ASN-0093's transition vocabulary contains no arrangement-modifying operation (plus empty init). As written, the premise needed for completeness is being read off the conclusion it is supposed to support.
**Required**: Ground `→`-completeness directly in ASN-0093's transition vocabulary (K.σ/K.α/K.λ are the only operations, none touches `M(d)` beyond K.σ's empty-init), and cite M2 only as the resulting invariant.

## OUT_OF_SCOPE

### Topic 1: Concurrency/atomicity model for Emit vs Observe
**Why out of scope**: The Open Questions correctly defer the consistency model under concurrent Emit/Observe; this note's transitions are sequential-atomic by ASN-0093's SequentialTransitionAxiom, and a concurrency layer is genuinely future territory.

### Topic 2: Higher-arity typed relations `L_K^{(n)}`
**Why out of scope**: The note explicitly restricts to standard triples; multi-arity projection is a future ASN, not a defect here.

VERDICT: REVISE
