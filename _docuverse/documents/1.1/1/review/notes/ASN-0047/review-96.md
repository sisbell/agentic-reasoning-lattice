# Review of ASN-0047

## REVISE

### Issue 1: Reference error in S4 cross-document distinctness
**ASN-0047, ExtendedReachableStateInvariants proof, S4 bullet (K.λ — Cross-document distinctness):** "the *Cross-document disjointness chain* lemma (T10a.{2,5} → T10) — derived in the Orphan links and coupling flexibility section — gives `ℓ₁ ≠ ℓ₂`"
**Problem:** The lemma is actually stated and proved in the "Allocator hierarchy under documents" section. The "Orphan links and coupling flexibility" section discusses orphan link semantics and contains no derivation of this lemma. A reader following the pointer will not find what is claimed.
**Required:** Update the cross-reference to "the Allocator hierarchy under documents section" where the lemma actually lives.

### Issue 2: NodeAllocationRegistry minimal requirement is incomplete
**ASN-0047, NodeAllocationRegistry (Definition) and NodeUniqueAllocation (Axiom):** The Registry "issues node addresses" with "minimal requirement... the single uniqueness condition stated below as NodeUniqueAllocation."
**Problem:** K.δ case (i) requires both `e ∉ E` AND `n₀ ≼ e`. NodeUniqueAllocation discharges only the freshness conjunct. The structural conjunct `n₀ ≼ e` (the constraint that issued node addresses extend the bootstrap [1]) is load-bearing for the NodeLineage invariant but is not stated as a registry obligation anywhere — it appears only as a K.δ precondition that the registry must somehow satisfy. As written, a registry could comply with NodeUniqueAllocation while issuing arbitrary node addresses, making K.δ case (i) unsatisfiable.
**Required:** Either extend NodeUniqueAllocation to a second axiom clause covering `n₀ ≼ e`, or rewrite the Registry definition's "minimal requirement" to include the structural-lineage condition explicitly.

### Issue 3: "Why SubAllocatorAxiom anyway" is essay content in a structural slot
**ASN-0047, Allocator hierarchy under documents section:** Two paragraphs labelled "*The multi-step T10a chain reaching `[d.0.s_X.1]`*" and "*Why SubAllocatorAxiom anyway*" follow the SubAllocatorAxiom statement.
**Problem:** These paragraphs explain *why* the axiom is included rather than *what* it says — exactly the anti-bloat pattern "new prose around an axiom explains why the axiom is needed rather than what it says." The "Why SubAllocatorAxiom anyway" paragraph defensively argues that "the axiom is not a closure of a gap T10a leaves; it is an *abstraction*..." and inventories what the collapse "buys downstream" — both rationale, not specification. The detailed walkthrough of the underlying T10a chain similarly belongs in a design note.
**Required:** Remove the two rationale paragraphs. If the underlying T10a-reachability of `[d.0.s_X.1]` is load-bearing for some downstream proof, encode that fact directly at the use site or as a numbered lemma; otherwise it carries no specification weight.

### Issue 4: Bootstrap n₀ = [1] design-rationale prose
**ASN-0047, State model section, "Structural form of n₀" paragraph (second paragraph):** "The value `[1]` is not arbitrary: Nelson's design requires the bootstrap to be `[1]` specifically... A different choice — `[2]`, `[42]` — would either fragment the root..."
**Problem:** Same anti-bloat pattern as Issue 3 — defending why a specific value was chosen, with citations to LM 4/17, LM 4/28, LM 4/38 and counterfactual analysis of `[2]` or `[42]`. The first paragraph already states the structural commitments needed by downstream proofs (single-component, zeros = 0, NodeLineage extension). The second paragraph is essay justifying the choice; it belongs in a rationale or design-notes file, not in the ASN body.
**Required:** Delete the second paragraph. Keep the structural form, drop the design-history argument.

### Issue 5: NodeLineage consequence to non-node entities not derived
**ASN-0047, Permanence section (NodeLineage) and Cross-layer bridges section (P6/P8):** NodeLineage states `(A e ∈ E : IsNode(e) : n₀ ≼ e)` — but only for nodes.
**Problem:** The full consequence — that every entity, every content address, and every link address descends from `n₀` (i.e., `n₀ ≼ e` for *every* `e ∈ E ∪ dom(C) ∪ dom(L)`) — follows from NodeLineage + P8 + transitivity of ≼ + (for content) P6 + S7a. This consequence is non-trivial (it establishes that the docuverse forms a single rooted tree rather than a forest) and is what the bootstrap discussion of `[1]` is really after. But the ASN proves only the IsNode-restricted form and leaves the propagation implicit. A reader cannot cite "every address descends from `n₀`" because that statement is nowhere proved.
**Required:** Add a named derived corollary — e.g., **GlobalLineage**: `(A x ∈ E ∪ dom(C) ∪ dom(L) :: n₀ ≼ x)` — with the propagation proof.

### Issue 6: P5 proof refers to "five elementary transitions" but the system has more
**ASN-0047, Destruction confinement section (P5 proof):** "*Proof.* By case analysis on the five elementary transitions. K.α extends dom(C) preserving existing entries, with E and R in its frame..."
**Problem:** P5 is stated in the four-component pre-extension state (before K.λ and K.μ⁺_L are introduced), where the elementary count is genuinely five. P3 then supersedes P5 in the extended state. But the prose enumerates "K.α, K.δ, K.μ⁺, K.μ⁻, K.ρ" and adds "K.μ~ decomposes into K.μ⁻ followed by K.μ⁺" — a reader reaching P5 from a forward reference (P3 says "P3 supersedes P5") will look back at a proof that ignores K.λ and K.μ⁺_L entirely, with no signpost that this is intentional.
**Required:** Either add a sentence at the start of P5's proof clarifying that P5 is stated and proved at the pre-extension state context (with the L-clause picked up by P3 later), or restate P5 once more after the extended state introduction and discharge the L clause directly.

### Issue 7: K.δ k = 0 sub-case implicit constraint on operand
**ASN-0047, K.δ definition, Per-sub-case additional requirements:** "*k = 0 (sibling):* `t ∈ E ∧ parent(t) = parent(e) ∧ zeros(t) = zeros(e)`."
**Problem:** `parent(t)` is undefined when `IsNode(t)` (per T4b — parent is defined only for non-node entities). The k = 0 precondition silently requires `¬IsNode(t)` through the partiality of `parent(t)`, but never states this. The reader must derive the implicit exclusion from the structural identity `zeros(e) = zeros(t)` together with the case-level `¬IsNode(e)`. Making `¬IsNode(t)` an implicit consequence of partial-function evaluation is the kind of subtlety that breaks under translation to a different logic.
**Required:** Add `¬IsNode(t)` (equivalently `zeros(t) ≥ 1`) explicitly to the k = 0 sub-case requirements, with a brief note that this follows from the structural identity but is stated for clarity.

## OUT_OF_SCOPE

The ASN's own *Open Questions* and *Scope* sections enumerate the deferred topics correctly. The deferred items — operation specifications, concurrency discipline beyond SequentialTransitionAxiom, registry protocol details, withdrawal mechanism, account-level k = 1 admissibility, transitive-transclusion provenance — are properly future-ASN territory and not flaggable against this draft.

VERDICT: REVISE
