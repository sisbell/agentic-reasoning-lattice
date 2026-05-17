# Review of ASN-0047

## REVISE

### Issue 1: K.δ ghost-base versioning relationship to S7d unclear
**ASN-0047, Elementary transitions, K.δ table**: The k=1 ghost-base row admits operands `t ∉ E_doc` with freshness discharged via Path 2 (K.δ precondition + TA5 determinism), explicitly noting "T10a's GlobalUniqueness at the entity-allocator layer is unavailable."
**Problem**: S7d (ASN-0036, restated) requires every document tumbler to be "the result of an allocation event under T10a." Ghost-base K.δ bypasses T10a's standard tracking discipline (no allocator activation; T2 spawnPt premise fails). The ExtendedReachableStateInvariants theorem lists S7d as a per-state conjunct, but the proof does not address how ghost-base K.δ preserves it.
**Required**: Either justify how ghost-base K.δ events satisfy S7d's T10a-conformance clause, or explicitly weaken/restrict S7d in the extended state's invariant list.

### Issue 2: K.μ⁻ "derived precondition" annotation is confusing
**ASN-0047, Elementary transitions, K.μ⁻**: "(*Derived* — recorded for cross-reference, follows from the effect clause's satisfiability) `dom(M(d)) ≠ ∅`"
**Problem**: A precondition is either required (must hold for the transition) or a consequence (follows from other facts). Listing a "derived precondition" with the explanation that it's actually a consequence of the effect clause is stylistically muddled and obscures the contract.
**Required**: Either move this to a "Consequences" section, drop it entirely (since the effect clause carries the constraint), or commit to it as a real precondition.

### Issue 3: K.μ⁻ admissibility precondition contains redundancy
**ASN-0047, K.μ⁻ precondition**: The precondition lists both per-subspace removal patterns (case-(a) restriction) AND "At least one subspace contracts strictly." 
**Problem**: The strict-contraction clause is necessary for the effect-clause satisfiability (`dom(M'(d)) ⊂ dom(M(d))`). The per-subspace pattern enforcement plus the effect clause together already determine admissibility. Listing both creates overlapping constraints.
**Required**: Reduce to a single precondition statement, or clearly separate "structural shape of removal" from "non-triviality requirement."

### Issue 4: K.μ~ admissibility constraints reference post-state properties
**ASN-0047, K.μ~ contract, Admissibility constraints**: "the resulting arrangement M'(d) satisfies S8-depth, D-CTG★, D-MIN★, and S3★ at the post-state."
**Problem**: Listing post-state properties as admissibility constraints conflates "what is required to invoke" with "what holds after invocation." This is unusual and makes the contract opaque — admissibility cannot be evaluated without first computing the post-state.
**Required**: Distinguish between pre-state preconditions (admissibility) and post-state postconditions (what the contract guarantees). If π must produce a result satisfying these invariants, that's a constraint on π selection, not on the operation's admissibility per se.

### Issue 5: Defensive meta-prose accretion in Cross-document disjointness lemma
**ASN-0047, Allocator hierarchy under documents, Cross-document disjointness chain lemma**: 
- "The case-split is purely structural — it does not appeal to S7d or to any allocator-tracking property... (S7d and the T10a allocator structure are invoked below, *within* Case B, only to motivate the typical dispatch..."
- "**Coverage of Case B (motivational; structural lifting is load-bearing).** The proof of Case B does *not* depend on the sub-case enumeration..."
**Problem**: These are defensive justifications about what the proof does or doesn't depend on, not advancement of the proof itself. The "motivational; structural lifting is load-bearing" classifier is meta-prose. Per the anti-bloat classifier, this is "essay content in structural slots."
**Required**: Remove the parenthetical defenses; let the proof structure speak for itself.

### Issue 6: Defensive "Shift-lemma applicability" paragraph in K.μ⁺_L
**ASN-0047, K.μ⁺_L precondition**: "Shift-lemma applicability for link-subspace v_ℓ. The shift expression `shift(max(V_{s_L}(d)), 1)` invokes ASN-0036's V-position shift lemmas at a link-subspace V-position; we record the subspace-independence of those lemmas here for completeness."
**Problem**: This is a defensive paragraph justifying that subspace-independent lemmas apply to link-subspace V-positions. If the lemmas are subspace-independent, no justification is needed. Per anti-bloat: "new prose around an axiom explains why the axiom is needed rather than what it says."
**Required**: Remove or compress to a single citation.

### Issue 7: Reviser drift in J4 V-position preservation rationale
**ASN-0047, Definition (Fork), V-position preservation rationale**: "The earlier formulation `ran(M'(d_new)) ⊆ ran(M(d_src))` constrained only the I-address range and admitted forks where d_new's V-positions had different depth or different terminal indices from d_src's — admissible under D-CTG★, D-MIN★, and S8-depth but inconsistent with the design intent..."
**Problem**: This is reviser drift — content explaining why a *prior formulation* was insufficient. Per anti-bloat: "a paragraph looks like a prior finding's content relocated rather than removed." The current formulation is what matters; the rejected earlier version should not be preserved as commentary.
**Required**: Remove the prior-formulation discussion; state the current correspondence clause and its rationale directly.

### Issue 8: Multiple paragraphs defer to the same withdrawal-mechanism open question
**ASN-0047**: At least four locations defer to the deferred withdrawal mechanism:
- D-CTG★ amendment's "Consequence for link withdrawal" paragraph
- K.μ⁻ amendment discussion
- Worked example "link allocation and arrangement" Step 5 counterfactual
- Open Questions list
**Problem**: Per anti-bloat: "multiple paragraphs in different sections defer to the same downstream location." Each citation re-explains the tombstoning issue.
**Required**: Consolidate to one explanatory location and have other sites cite it briefly.

### Issue 9: Missing concrete worked example for K.δ case (ii) k=2 descent
**ASN-0047, Worked examples**: The worked examples exercise K.δ case (i) (node baptism), K.δ case (ii) k=0 (sibling in ghost-base example), K.δ case (ii) k=1 (live and ghost-base), but not K.δ case (ii) k=2 (account from node, or document from account). The "fork with subsequent insertion" example starts with `E₁ = {1, 1.0.1, 1.0.1.0.1}` — assuming these exist without showing how the account and document were allocated.
**Problem**: The k=2 descent case is the primary mechanism for account and document allocation in the system. The absence of a direct worked example leaves the most common K.δ pattern unverified against concrete preconditions.
**Required**: Add a worked example exercising K.δ case (ii) k=2 — e.g., allocating account `1.0.1` from node `1`, then document `1.0.1.0.1` from account `1.0.1`.

### Issue 10: SubAllocatorAxiom explanatory prose redundancy
**ASN-0047, Allocator hierarchy under documents**: The axiom has three labeled clauses, followed by explanatory paragraphs: "Past each sub-allocator's first emission, the frontier is a T10a-conforming `inc(·, 0)` chain whose subsequent emissions inherit T10a's GlobalUniqueness in full; SubAllocatorAxiom.Namespace underwrites only the bootstrap." Then the dispatch table re-explains the same content.
**Problem**: The relationship between SubAllocatorAxiom and T10a is explained in three forms (axiom prose, post-axiom paragraph, dispatch table). Per anti-bloat: "two paragraphs in the same document say the same thing in different words."
**Required**: Consolidate; let the dispatch table carry the operational distinction without restating it in prose.

### Issue 11: K.μ~ "all valid π yield the same post-state" derivation is over-explained
**ASN-0047, K.μ~ contract**: "Claim: all valid π for a given (M(d), M'(d)) yield the same post-state. The post-state M'(d) is a partial function — a set of (V-position, I-address) pairs..."
**Problem**: This derivation explains why witness selection doesn't change the observable post-state — but the contract already specifies M'(d) as the post-state. The fact that a witness is just a witness is immediate from "there exists π" framing. The detailed argument is essay content.
**Required**: Replace with a one-sentence note that π is existentially witnessed and witness choice does not affect the post-state.

### Issue 12: L1b derivation chain not tight
**ASN-0047, ExtendedReachableStateInvariants proof, Foundation invariants previously implicit, L1b**: The discharge for the first-link case appeals to SubAllocatorAxiom's structural construction ("`[d.0.s_L.1]` with element field `[s_L, 1]`, so `#E(ℓ) = 2` by construction"); the subsequent case appeals to TA5(c) length-preservation.
**Problem**: The derivation is correct but the structural-construction discharge for the first-link case could be made more rigorous — `#E([d.0.s_L.1]) = 2` requires knowing the parse splits the element field as `[s_L, 1]` (two components after the third zero), which depends on T4b's projection. A direct citation rather than "by construction" would tighten it.
**Required**: Explicitly cite T4b applied to the first-emission address to derive `#E(ℓ) = 2`.

## OUT_OF_SCOPE

### Topic 1: Concurrency and atomicity guarantees
**Why out of scope**: Listed in Open Questions; the present ASN assumes sequential single-event semantics. Concurrent operation handling, atomicity of composites under concurrency, and pre-commit uniqueness disciplines belong to a future concurrency-focused ASN.

### Topic 2: Link withdrawal mechanism
**Why out of scope**: Explicitly deferred in Open Questions. The D-CTG★ amendment forecloses interior link withdrawal via K.μ⁻; the tombstone/inactive-status mechanism Nelson describes requires a separate withdrawal-specific ASN.

### Topic 3: Account-level depth-1 extension (K.δ with k=1, IsAccount(t))
**Why out of scope**: Listed in Open Questions; the consultation evidence supports the current restriction to document-only versioning.

### Topic 4: Version lineage and ancestry beyond initial creation step
**Why out of scope**: Version-management ASN. The K.δ ghost-base discussion notes "richer version contract... is deferred to a subsequent version-management ASN."

### Topic 5: Link inheritance under forking
**Why out of scope**: Explicitly stated as outside this ASN's scope at the J4 fork discussion. Would require K.μ⁺_L steps in the fork composite.

### Topic 6: Multi-server / replication protocol (BEBE)
**Why out of scope**: Excluded by the stated scope list. The single-canonical-root constraint via NodeLineage is consistent with this exclusion.

### Topic 7: Operations layer (INSERT, DELETE, COPY, REARRANGE, MAKELINK, CREATENEWVERSION, DELETEVSPAN)
**Why out of scope**: Explicitly excluded by the stated scope list. The elementary transitions and named composite K.μ~ are the abstract layer; operation specifications belong to a downstream ASN.

VERDICT: REVISE
