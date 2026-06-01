# Review of ASN-0086

This note has clearly been hardened over many cycles; the core proofs (R0, R0a, R7a, the WP analyses) are internally careful and the active/audit distinction is genuine new content, not a re-skin. My findings are concentrated where the `review-mode.anti-bloat` classifier points: prose that restates the same scope point in two places, forcing the reader to confirm twice that nothing new is being said.

## REVISE

### Issue 1: WP Case 1 justifies retaining PC twice in identical terms
**ASN-0086, Weakest-Precondition Analysis, Case 1**: the sufficiency framing says *"We state the stronger PC because it is exactly what the relational layer's usage discipline supplies — full substrate-conformance, not merely a local antichain on a's subtree."* The *Non-weakestness* paragraph closes with *"We retain PC in the stated precondition because it is the condition the relational layer establishes."*
**Problem**: These are the same claim — "PC over-constrains but we keep it because the layer supplies it" — made twice, separated by the load-bearingness and non-weakestness derivations. The *Domain of quantification* paragraph (*"For layer-initiated calls PC holds for free and the effective precondition collapses to P0 ∧ P1"*) makes it a third time. A reader tracking the argument has to verify each restatement adds nothing.
**Required**: State the "PC is layer-supplied, hence retained though non-weakest" point once (it belongs with *Non-weakestness*, where the weaker local condition is exhibited) and drop the other two occurrences.

### Issue 2: R0 proof states its per-address scope caveat twice, with a defensive non-use inventory
**ASN-0086, R0 proof**: the freshness discharge opens with *"we use only ASN-0093's per-address chain facts ... and never its store-wide, reachability-restricted lemmas (FirstEmissionFreshness, ChainMembershipForOrigin, SubsequentEmissionFreshness, R0a-Cor1) ... The argument therefore carries over to every state-local-conforming state."* The L-invariant-preservation phase then repeats it: *"under the same per-address scope fixed there — using only state-independent, single-address chain facts."*
**Problem**: The scope justification is legitimate (R0 must apply at non-`→*`-reachable states), but it is asserted in two phases of one proof, and the parenthetical enumeration of four lemmas the proof does *not* use is a defensive inventory rather than a step in the argument. This is exactly the "non-use inventory" pattern the anti-bloat note flags.
**Required**: Fix the per-address scope once at the top of the proof (covering both the freshness and L-invariant phases) and drop the second restatement; replace the four-lemma non-use list with the single positive statement "per-address chain facts only."

### Issue 3: "Arrangement modification is out of scope" paragraph re-establishes → completeness already stated
**ASN-0086, State transition relation**: the main paragraph already commits *"Every dom-extending transition in → is one of the three K-ops; the substrate exposes no removal, replacement, or in-place mutation transition..."* The immediately following *"Arrangement modification is out of scope"* paragraph re-asserts *"→ ≡ K.σ ∪ K.α ∪ K.λ is the complete dom-extending vocabulary."*
**Problem**: The completeness of → is stated in both paragraphs. The second paragraph does carry one piece of new content (deriving M2 / no arrangement-modifying op, needed for R6c), but it re-derives the completeness claim verbatim around that content.
**Required**: Keep only the M2-derivation content in the second paragraph and remove the duplicated "→ is the complete dom-extending vocabulary" restatement, which the preceding paragraph already owns.

### Issue 4: Properties-Introduced table embeds full derivation chains, duplicating the proofs
**ASN-0086, Properties Introduced table**: entries carry derivation annotations such as `R6a | ... (= R3 + R2 + purity of coverage)`, `R0a | ... Case 1 cross-home via L1 + L1a; Case 2 same-home via R0a-Cor1 ... equivalently via T10a.2`, and `Nullify | ... (= R5 + R0 + R0a + R6a + L12)`.
**Problem**: A summary table should index claims, not re-state their proof skeletons. These derivation chains reproduce the proof structure already given in the body, so the table is a second copy of the dependency graph that must be kept in sync as proofs change — and several entries (e.g., R0a's "Case 1 ... Case 2 ... equivalently via T10a.2") are essay-length restatements of the proof in a structural slot.
**Required**: Reduce table entries to the statement plus at most the headline dependency; move the case-by-case derivation prose out of the table (it already lives in the proofs).

## OUT_OF_SCOPE

### Topic 1: Concurrency / atomicity model for Emit vs Observe
The Open Questions already defer the consistency model under which `A_K` transitions are observed and whether Emit must be atomic against concurrent Observe. This is correctly future territory — the present note proves only single-authority, sequential properties (SequentialTransitionAxiom is inherited from ASN-0093).

### Topic 2: Higher-arity typed relations
`L^Σ` is explicitly restricted to standard-triple links, with `|Σ.L(a)| > 3` set aside. Extending the relational vocabulary to `L_K^{(n)} ⊆ A_rel × ℘(A)^n` is a distinct construction and belongs in a future ASN, as the Open Questions note.

VERDICT: REVISE
