# Review of ASN-0047

I've carefully reviewed the transition model ASN. The technical content is substantive and the proofs check out on close inspection. The K.μ⁻ exhaustiveness lemma, K.μ~ link-subspace fixity proof, P4★ derivation, and ExtendedReachableStateInvariants induction all appear sound. The worked examples (entity hierarchy, fork-with-insertion, interior content replacement, ghost-base versioning, link allocation) verify boundary cases against the formal contracts.

The issues below are primarily meta-prose accretion patterns rather than proof flaws.

## REVISE

### Issue 1: Methodological commentary as paragraph-length material

**ASN-0047, *Elementary transitions* opening**: "We use the standard operational-semantics convention: a transition with unsatisfied preconditions does not enter the transition set... Counterfactual analyses below appeal to this convention to show that an attempted operation falls outside the transition set rather than producing an invalid post-state."

**Problem**: The "Rejection model" paragraph is methodological commentary about how the document treats preconditions, and the closing sentence is forward-looking meta-commentary about subsequent counterfactual analyses. Pattern match: methodological prose that explains the document's convention rather than advancing claims.

**Required**: Reduce to a one-sentence convention statement (e.g., "Convention: a transition with unsatisfied preconditions does not fire"). Remove the forward-looking sentence.

### Issue 2: Defensive justification of quantifier-excluded case

**ASN-0047, *The state model***: "Bootstrap genesis vs. K.δ allocation. The bootstrap node n₀ is established in E₀ by system genesis, not by a K.δ event. NodeUniqueAllocation's discharge — both the freshness clause `e ∉ E` and the bootstrap-lineage clause `n₀ ≼ e` — applies only to subsequent K.δ node-allocation events; n₀ itself satisfies `n₀ ≼ n₀` by reflexivity and falls outside the scope of any allocation-event freshness obligation. Likewise, the S4 invariant... quantifies over allocation events; n₀'s presence at Σ₀ as a genesis seed is outside that quantifier."

**Problem**: This paragraph imagines a case (does n₀ need to satisfy K.δ preconditions or S4?) that the quantifier already excludes. NodeUniqueAllocation quantifies over K.δ events; n₀ is established by genesis, not a K.δ event, so it's structurally outside scope without further argument. Pattern match: "a paragraph imagines a case the claim's carrier or precondition already excludes."

**Required**: Delete the paragraph. The state-model definition saying "E₀ = {n₀}" together with the K.δ definition quantifying over allocation events already makes the scope boundary self-evident.

### Issue 3: Named placeholder with explicitly no formal content

**ASN-0047, NodeAllocationRegistry section**: "This narrative carries no formal content of its own; it names what NodeUniqueAllocation abstracts over. The realisation (issuing protocol, persistence model, concurrency discipline) lies outside this ASN's discharge layer."

**Properties Introduced table**: "NodeAllocationRegistry | Discussion (not a formal item): the narrative name for the abstract obligation discharged formally by NodeUniqueAllocation alone..."

**Problem**: The ASN names a "Discussion" item that the body text explicitly states carries no formal content. Listing a placeholder in Properties Introduced is internally inconsistent with what that table is for. Pattern match: "a definition's introduction enumerates downstream consumers" and naming without formal content.

**Required**: Delete the NodeAllocationRegistry discussion paragraph; eliminate its Properties Introduced entry. NodeUniqueAllocation already carries the full formal content. If context about implementation is wanted, fold one sentence into NodeUniqueAllocation's prose.

### Issue 4: Axiom-necessity defense mixed with formal content

**ASN-0047, *Allocator hierarchy under documents***: "*Activation outside T10a's standard T2 spawning step.* SubAllocatorAxiom activates `A_C(d)` and `A_L(d)` at the K.δ event placing `d` into E_doc, but the activation does *not* follow T10a's T2 spawning premise. T10a's T2 step requires the new allocator's spawning point to inhabit its parent allocator's tracked domain... and the anchors `b_C(d), b_L(d)` are not elements of any predecessor allocator's tracked domain... The activation is therefore axiomatic at this layer rather than derivable from T10a's standard discipline. The bypass does not violate T10a.6..."

**Problem**: The first half explains *why* SubAllocatorAxiom must be axiomatic rather than derivable. The second half supplies the T10a.6 non-violation argument (formal content). Pattern match: "new prose around an axiom explains why the axiom is needed rather than what it says."

**Required**: Tighten the necessity defense to one sentence ("The activation cannot be derived from T10a's T2 spawning rule because b_C(d), b_L(d) inhabit no predecessor's tracked domain.") Keep the T10a.6 non-violation argument as it provides actual disjointness justification.

### Issue 5: Closing-paragraph regime commentary

**ASN-0047, *Freshness-discharge summary* closing**: "The asymmetric stratification — node allocation external to T10a (NodeUniqueAllocation), document/account allocation within T10a (GlobalUniqueness), and content/link sub-allocators activated by SubAllocatorAxiom — reflects three distinct allocation regimes."

**Problem**: Single-sentence meta-observation about the structure of the table just presented. Adds no formal content; restates structure already visible in the table. Pattern match: meta-commentary on regime structure.

**Required**: Delete the sentence. The table is self-explanatory.

### Issue 6: Missing primitive transitions in Properties Introduced

**ASN-0047, Properties Introduced table (first table)**: K.μ⁻ and K.μ~ are not listed as new properties, despite being introduced as elementary transitions in *Elementary transitions* and *Decomposition of K.μ~*. K.μ⁻ appears only in the second table under "K.μ⁻ (per-subspace scope)" — which is a strengthening of postconditions, not the transition's introduction. K.μ~ appears only via its derived sub-property K.μ~-FIX.

**Problem**: K.μ⁻ and K.μ~ are introduced in this ASN (not foundation properties), so they belong in the first table. The current placement is inconsistent with how the other transitions (K.α, K.δ, K.μ⁺, K.μ⁺_L, K.λ, K.ρ) are catalogued.

**Required**: Add explicit K.μ⁻ and K.μ~ rows to the first "New properties introduced" table.

### Issue 7: SequentialTransitionAxiom omitted from Properties Introduced

**ASN-0047, *The state model***: SequentialTransitionAxiom is defined as an axiom in the state-model section but does not appear in either the first or second Properties Introduced table.

**Problem**: The axiom is referenced multiple times downstream (e.g., in K.δ's freshness discharge, in S4's discharge), but readers consulting the Properties Introduced table will not find it catalogued.

**Required**: Add SequentialTransitionAxiom to the first Properties Introduced table.

## OUT_OF_SCOPE

### Topic 1: Concurrency discipline for ghost-base K.δ events

**Why out of scope**: The ASN admits ghost-base versioning (K.δ k = 1 with t ∉ E_doc) with freshness discharged by direct E-inspection under SequentialTransitionAxiom's atomic inspection-commit semantics. Multi-protocol concurrency concerns (per-allocator serialization, transactional commit, global pre-commit uniqueness) are explicitly recorded in Open Questions. Future work, not a defect of this ASN.

### Topic 2: Authority/authorization for cross-account namespace allocation

**Why out of scope**: The ghost-base versioning case admits any T4-valid IsDocument tumbler as operand, which could in principle allow allocation under a parent account owned by a different principal. Ownership and access-control checks are explicitly listed in the ASN's Scope section as out of scope. Belongs in a future authorization ASN.

### Topic 3: Mechanism reconciling Nelson's tombstoning with D-CTG★/D-MIN★

**Why out of scope**: The ASN frankly acknowledges the link-withdrawal gap created by uniform contiguity (interior link withdrawal forces suffix truncation). Reconciliation requires a separate withdrawal mechanism (status flag, tombstone marker, or retraction link) outside K.μ⁻'s presentational-removal contract. Recorded in Open Questions.

VERDICT: REVISE
