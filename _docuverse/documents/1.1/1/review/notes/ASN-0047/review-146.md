# Review of ASN-0047

## REVISE

### Issue 1: LinkVPositionDepthAxiom fixes `m_L = 2` by axiom on implementation evidence alone
**ASN-0047, Link-subspace extension**: "**LinkVPositionDepthAxiom (Axiom, FixedLinkVPositionDepth).** `(A d ∈ E_doc :: m_L = 2)` ... Pins the link-subspace V-position depth to the value used by Nelson (LM 4/31) and reproduced in udanax-green (do2.c:151–167)."
**Problem**: The genuine underdetermination this axiom resolves is the *first* link-subspace V-position's depth (S8-depth is vacuous on an empty subspace). But fixing it to the specific value `2` — justified solely by implementation evidence — is an abstract over-specification: an alternative implementation satisfying the same state guarantees could use a different fixed link depth. The abstract model needs either a derivation of why `2` is forced, or an axiom of the form "link-subspace V-positions share a common depth `m_L ≥ 2` fixed at first insertion."
**Required**: Replace the concrete-value axiom with the depth-determinacy guarantee actually required (a fixed `m_L ≥ 2` per document), or derive `m_L = 2` from a stated abstract property rather than from `do2.c`.

### Issue 2: Axiom prose inventories downstream use-sites and explains why-needed rather than stating the axiom
**ASN-0047, NodeUniqueAllocation**: "clause (c) is the registry-side closure that downstream T2-spawn discharge invokes — specifically at K.δ case (ii) k = 2 sub-case B, where the spawnPt premise must be discharged against the external registry... details of the registry mechanism (issuing protocol, persistence model, concurrency discipline) lie outside this ASN's discharge layer." Similarly NodeRegistryBootstrap's Properties-table entry: "Initial-state commitment grounding the T2-style spawnPt discharge in K.δ case (ii) k = 2 with operand t = n₀..."
**Problem**: This is exactly the flagged pattern — an axiom whose introduction enumerates its consumers and explains *why it is needed* (scope, discharge-layer placement) rather than *what it states*. The use-site ("at K.δ case (ii) k = 2 sub-case B") belongs at the use-site, where it already appears.
**Required**: Reduce each axiom to its three conditions. Move the "which K.δ sub-case invokes clause (c)" pointer into sub-case B (where it is already stated) and delete the scope/discharge-layer commentary.

### Issue 3: Document-ordering justification prose in the state model
**ASN-0047, The state model**: "The link store L is named in the state tuple here so the initial state Σ₀ and its invariant verification — both stated next — can be given once in their final five-component form, rather than restated after L is introduced. The four-component preamble preceding the link store's introduction reads Σ with `L = ∅`..."
**Problem**: This justifies the document's presentation order rather than advancing any claim — the flagged "prose justifies document ordering" pattern. The reader does not need to be told why the tuple is five-component before L is defined.
**Required**: Delete the justification. State the five-component tuple; the `L = ∅` reading of earlier sections is self-evident once L₀ = ∅ is given.

### Issue 4: K.μ~ dependency-chain prose argues non-circularity repeatedly
**ASN-0047, Decomposition of K.μ~**: "Step (B)'s mechanical realisation produces what admissibility (i) stipulates without circular dependence on the downstream fixity arguments." And: "The argument consumes Step (A)'s subspace preservation (specifically the content-side restriction at B.2) but does not consume link-subspace fixity (Steps (C)/(D)) or CL-UNIQ."
**Problem**: These sentences exist to reassure the reader that the (A)→(E) ordering is non-circular — the flagged "prose justifies document ordering / non-circularity" pattern. The dependency is already visible from each step's cited premises; asserting "X does not consume Y" in prose adds no content and must be re-verified against the steps anyway.
**Required**: Remove the standalone non-circularity assertions. If a step's premises need to be explicit, list them in that step; do not narrate what later steps do or do not consume.

### Issue 5: Triple statement of the "K.α has no local amendment" point
**ASN-0047**: The same claim appears in three slots — (a) *Elementary transitions*, K.α: "The content-subspace restriction `E(a)₁ = s_C` ... is part of ASN-0093's K.α precondition directly; no separate local amendment of K.α is needed"; (b) *Amendments to existing transitions*: "**K.α (no local amendment in extended state).** ... No locally-introduced amendment of K.α is required"; (c) Properties table: "K.α's `E(a)₁ = s_C` precondition (inherited) — Inherited from ASN-0093's K.α directly — not a local amendment."
**Problem**: Two prose paragraphs plus a table row say the same thing in different words — the flagged "two paragraphs say the same thing" pattern.
**Required**: State it once (the Amendments-section paragraph is the natural home) and let the table row point to it without re-arguing.

### Issue 6: K.δ k=1 provenance case-split and "operational uniformity" explained redundantly
**ASN-0047**: The (a')/(b') case-split on which allocator hosts `A_v(d)`'s parent is given in *Sub-allocator names*, restated in *K.δ case (ii) discharge* (k=1), and exercised again in the fork worked example. The "operational uniformity" point appears twice as standalone meta-paragraphs: K.δ definition's "*Operational uniformity across operand provenance*" and *Allocator hierarchy*'s "*Operational uniformity of K.δ k = 0 reconciled with allocator-tree provenance*." The *K.δ case (ii) discharge* additionally embeds a "*Multi-version invariant chain*" worked elaboration.
**Problem**: Use-site inventory plus essay content in structural slots, and the same provenance dispatch explained three times. The "*Multi-version invariant chain*" paragraph is worked-example material relocated into a discharge section that the fork example already covers.
**Required**: State the (a')/(b') dispatch once (in *Sub-allocator names*) and cite it. Fold the "operational uniformity" observation into a single sentence at the K.δ k=1 precondition. Move or delete the multi-version elaboration — the worked example carries it.

### Issue 7: FrontierEquivalence "Significance" and "Counterexample" meta-prose
**ASN-0047, FrontierEquivalence**: "*Significance.* The direct freshness predicate `inc(t, 0) ∉ E` sidesteps allocator-structural identification entirely: its operational truth at the K.δ event is what selects `t`..."; and the "*Counterexample to T4b-based identification*" paragraph arguing at length why an approach the ASN does not take would fail.
**Problem**: The "Significance" block is essay content restating the lemma's payoff. The counterexample defends against an alternative formulation (T4b-based maximality) that no carrier in the ASN uses — the flagged "imagines a case the precondition already excludes / defensive justification" pattern.
**Required**: Delete "Significance." Reduce the counterexample to at most one sentence noting that T4b stratification does not identify the frontier, if any consumer actually relies on that fact; otherwise remove it.

## OUT_OF_SCOPE

### Topic 1: A link-withdrawal mechanism (status flag / tombstone / retraction link) reconciling LM 4/9 with D-CTG★
The ASN's suffix-only contraction forces withdrawing every link after an interior one. The mechanism for interior withdrawal is correctly deferred (already an Open Question); it is new territory, not an error here.

### Topic 2: Link inheritance under forking
J4 starts the forked document's link subspace empty. Whether forks should propagate home links via K.μ⁺_L steps is a future operations concern, properly left open.

META: not applicable — the ASN defines abstract state, transitions, and invariants; the concerns above are localized prose accretion and one over-specified axiom, not wholesale implementation drift.

VERDICT: REVISE
