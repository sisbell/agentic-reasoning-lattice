# Review of ASN-0047

## REVISE

### Issue 1: K.δ k=2 implicit constraint on operand level not stated

**ASN-0047, K.δ definition, Case (ii) k=2 sub-case**: The sub-case states `t ∈ E ∧ parent(e) = t` with structural identity `zeros(e) = zeros(t) + 1`.

**Problem**: Combined with the K.δ precondition `¬IsElement(e)` (zeros(e) ≤ 2), this implicitly forces zeros(t) ≤ 1 — i.e., t must be a node or account, never a document. A careless reader could think K.δ k=2 with t = document is valid (it produces an element, violating the precondition). The worked example mentions this consequence at the end ("a hypothetical fourth k = 2 descent would produce zeros = 3"), but the K.δ definition itself does not state the constraint.

**Required**: Add to the k=2 sub-case bullet an explicit constraint like "zeros(t) ≤ 1 (equivalently, IsNode(t) ∨ IsAccount(t))", so the per-sub-case constraint is visible at the definition site rather than left as a derivation from the case-level precondition.

### Issue 2: "Ghost-base versioning (k = 1)" paragraph is a pure pointer

**ASN-0047, K.δ definition**: "*Ghost-base versioning (k = 1).* The k = 1 sub-case admits an inc operand `t ∉ E_doc`; the structural-only check on `t` and the chain-wide ghost-routing of freshness discharge are catalogued in K.δ's precondition list and *Freshness discharge* paragraph above."

**Problem**: This paragraph adds no content — it merely points back to the precondition list and the *Freshness discharge* paragraph that precede it within the same K.δ definition. Both pieces of information are already where the paragraph points. This is the forward-reference accretion pattern the reviser explicitly flagged ("a paragraph looks like a prior finding's content relocated rather than removed").

**Required**: Remove the paragraph. If a section heading is needed for navigability, retain only the heading.

### Issue 3: "Frame extension (existing transitions)" paragraph adds little

**ASN-0047, Amendments to existing transitions**: "Each of K.α, K.δ, K.μ⁺, K.μ⁻, K.μ~, K.ρ holds `L' = L` in its extended-state frame; only K.λ extends L. L12 (LinkImmutability) follows trivially..."

**Problem**: This paragraph states the obvious fact that pre-existing transitions don't touch the newly-introduced L component, and notes that L12 follows trivially. It's filler explaining a structural extension rather than advancing reasoning. The same observation could be embedded as a single clause in the *Extended system state* paragraph at the head of the section, or in K.λ's definition itself.

**Required**: Absorb the content into the extended-state introduction or K.λ's frame statement, removing the standalone paragraph.

### Issue 4: P3★ naming inconsistency — no P3 predecessor in this ASN

**ASN-0047, Extended monotonicity invariants and Properties Introduced table**: The "★" notation is used consistently for "extended-state form of a four-component predicate". P0 has no star (unchanged), J1 → J1★, P4 → P4★, etc. But the ASN introduces P3★ as a fresh synthesis with no P3 in the body.

**Problem**: The Properties table entry says "P3★ (ArrangementMutabilityOnly, extended). Synthesises this ASN's P0..." — but P0/P1/P2 already exist unstarred, and there is no P3 elsewhere to amend. The "★" creates an expectation of a predecessor that doesn't exist.

**Required**: Either (a) rename to P3 (a fresh synthesis, no star), or (b) introduce a four-component P3 (e.g., as the qualitative summary of P0+P1+P2 in the Permanence section) so that P3★ is genuinely an extension.

### Issue 5: K.λ precondition collapses two discharge cases into one bullet

**ASN-0047, K.λ definition**: One bullet reads: "ℓ is produced by d's link sub-allocator: `ℓ = [d.0.s_L.1]` on the first emission (pinned by SubAllocatorAxiom.FirstEmission, which alone commits the first emission outside `dom(L) ∪ dom(C)`), and `ℓ = inc(max{ℓ' ∈ dom(L) : origin(ℓ') = d}, 0)` (TA5(c)) on every subsequent emission (T10a GlobalUniqueness on the A_L(d) inc chain gives `ℓ ∉ dom(L)`; SC-NEQ + T7 give `ℓ ∉ dom(C)`)."

**Problem**: The first-emission case (closed by SubAllocatorAxiom.FirstEmission) and the subsequent-emission case (closed by T10a GlobalUniqueness) have structurally different discharge routes and produce different forms of ℓ. Combining them in one prose-heavy bullet makes the precondition hard to parse. The discharge summary table already separates them; the precondition should too.

**Required**: Split the bullet into two — one for the first-emission case (predicate `{ℓ' ∈ dom(L) : origin(ℓ') = d} = ∅`, with ℓ = [d.0.s_L.1] discharged by SubAllocatorAxiom.FirstEmission) and one for subsequent emissions (predicate `{ℓ' ∈ dom(L) : origin(ℓ') = d} ≠ ∅`, with ℓ = inc(max{...}, 0) discharged by T10a GlobalUniqueness).

### Issue 6: K.μ~ "full content-subspace clearance" presented as the decomposition rather than one decomposition

**ASN-0047, Decomposition of K.μ~**: "When π ≠ id (which requires `dom_C(M(d)) ≠ ∅`), K.μ~ expands as *full content-subspace clearance and rebuild*: K.μ⁻ removes V_{s_C}(d) entirely..."

**Problem**: This presents full clearance as the unique decomposition. But K.μ⁻'s admissibility only requires per-subspace suffix removal — for a permutation π that fixes positions [1,1..k₀-1] and only permutes [1,k₀..n], partial suffix clearance (removing [1,k₀..n] and rebuilding that suffix) would also be admissible. The interior content replacement worked example uses partial-suffix decomposition for a different (non-K.μ~) composite, demonstrating the pattern is otherwise admissible. The ASN should either justify why K.μ~ specifically requires full clearance, or acknowledge that other decompositions exist and full clearance is one valid choice.

**Required**: Clarify that the full-clearance decomposition is *one* valid expansion (chosen for uniformity), with partial-suffix decompositions also admissible for permutations that fix a contiguous prefix. Alternatively, justify the structural necessity of full clearance.

### Issue 7: Bootstrap node value [1] presented as fixed without marking the conventional nature

**ASN-0047, State model**: "*Structural form of n₀.* The bootstrap node is fixed as `[1]` — a one-element tumbler with `zeros(n₀) = 0`..."

**Problem**: NodeLineage requires `n₀ ≼ e` for all nodes — but the constraint is satisfied by any single-component positive tumbler ([1], [2], [42]). The choice of [1] specifically is conventional, not derived. The ASN states it as fixed but doesn't mark the convention or explain why [1] is privileged. This matters because s_C = 1 (per SubspaceConventionAxiom) coincides numerically with n₀'s only component, which could confuse readers tracing tumbler structure in worked examples.

**Required**: Mark [1] as a conventional choice (consistent with Nelson's single root authority), or relax the stipulation to "any single-component positive tumbler" with [1] as the canonical convention.

### Issue 8: SubAllocatorAxiom's necessity claim is incompletely justified

**ASN-0047, Allocator hierarchy under documents**: "T10a's discipline does not span the bootstrap step from a document address `d` to the sub-allocator's first emission `[d.0.s_X.1]` (the at-most-once spawning constraint blocks d from minting that address directly under T10a)."

**Problem**: The justification "blocks d from minting that address directly" is true for a single inc step, but T10a admits multi-step chains. Reconstruction: d's allocator can spawn a child at inc(d, 2) = [d.0.1]; that child can then spawn at inc([d.0.1], 0) = [d.0.2] (sibling chain emits [d.0.1], [d.0.2], ...); [d.0.1]'s allocator can also spawn a k=1 child at [d.0.1.1]. So [d.0.s_C.1] is reachable from d via a multi-step T10a chain. The ASN's choice to axiomatize first-emission is an abstraction over this chain, not a closure of a gap T10a leaves. The justification should reflect this — either explicate the multi-step chain and explain why the axiomatic abstraction is preferred, or strengthen the argument for why T10a cannot reach [d.0.s_C.1].

**Required**: Tighten the justification — either (a) show the multi-step T10a chain and frame SubAllocatorAxiom as an abstraction that simplifies downstream discharge, or (b) show concretely which T10a constraint blocks the chain (e.g., a per-(t,k') constraint that fails).

### Issue 9: Dual-phase (four-component → extended) structure produces cumulative amendment accretion

**ASN-0047, structure across multiple sections**: The ASN first builds the four-component state Σ = (C, E, M, R) with K.α, K.μ⁺, J1, J1', P4, etc., then introduces L and "amends" most definitions. The catalogue includes K.α amendment, K.μ⁺ amendment, K.μ⁻ per-subspace scope, J1★ replacing J1, J1'★ replacing J1', ValidComposite★ replacing ValidComposite, P4★ replacing P4, D-CTG★ / D-MIN★ / D-SEQ★ replacing their unstarred forms, S3★ replacing S3, S7d★ replacing S7d, S8★ replacing S8, P3★ as fresh synthesis.

**Problem**: Each amendment requires its own scope-clarifying prose ("in the extended state...", "supersedes...", "is the link-store extension contributed by..."). The cumulative meta-prose around supersession is significant. A reader has to mentally merge each amended form back into its base definition. The Issue 2 and Issue 3 paragraphs are symptoms of this broader structural choice. The original four-component K.μ⁺ / J1 forms appear in the document but are not the canonical statements — those are the starred versions.

**Required**: Consider restructuring to a single-phase presentation — introduce L as a state component from the beginning, give K.α and K.μ⁺ their final (content-subspace-scoped) forms directly, state J1 in its content-scoped form initially. The "amendment" paragraphs would disappear, replaced by direct definitions. If the four-component model is pedagogically valuable, present it as a *consequence* (states with empty L reduce to the four-component case) rather than as the primary mode followed by patches.

### Issue 10: J1 "derivation by wp" framing understates the design choice

**ASN-0047, Coupling and isolation**: "**J1 (Extension records provenance).** Arrangement extension K.μ⁺ must co-occur with provenance recording K.ρ... We derive this by wp. The invariant we need — Contains(Σ) ⊆ R — must hold after the composite transition."

**Problem**: The derivation is presented as mechanical wp computation, but the load-bearing premise — that Contains(Σ) ⊆ R is a required invariant — is itself a design choice (this is P4, which the ASN derives from J1). The presentation order suggests J1 follows from wp, but the actual logic is: (1) declare P4 as a design invariant; (2) compute wp(K.μ⁺, P4) and find K.μ⁺ alone doesn't preserve it; (3) introduce J1 as the coupling that makes P4 preservable; (4) prove P4 holds given J1.

**Required**: Reframe the J1 introduction to make the design-choice nature of P4 explicit. The wp computation reveals what coupling is needed to preserve P4 — not that J1 falls out of nowhere by mechanical derivation. A short statement like "to maintain Contains(Σ) ⊆ R across K.μ⁺ steps, K.ρ must co-occur" makes the design choice visible.

### Issue 11: K.δ structural identities could be presented as TA5-derived consequences

**ASN-0047, K.δ definition, Case (ii)**: After the per-sub-case bullets, the definition lists "Structural identities: `zeros(e) = zeros(t)` for k ∈ {0, 1}; `zeros(e) = zeros(t) + 1` for k = 2; `parent(e) = parent(t)` for k ∈ {0, 1}; `parent(e) = t` for k = 2."

**Problem**: These are framed as stipulations alongside the preconditions, but they are consequences of TA5 and parent's definition (T4b), not independent requirements. Listing them as structural identities mixes derived consequences with imposed preconditions, making it unclear what must be checked vs. what follows.

**Required**: Mark these as derived consequences (e.g., "Structural identities (consequences of TA5 + T4b's parent projection):..."), or remove them entirely since they follow from the inc-form e = inc(t, k) plus TA5's contract.

## OUT_OF_SCOPE

(No issues to flag — the ASN's Scope statement appropriately excludes operations, atomicity, replication, indexing, and related topics; open questions explicitly defer items that could belong in future ASNs.)

VERDICT: REVISE
