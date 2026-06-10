# Review of ASN-0126

## REVISE

### Issue 1: The projected-path R6c transfer is proven twice, and the earlier occurrence cites the later one as its license
**ASN-0126, Retraction as an attributed Binary (Nullify_Binary, *Postconditions — Persistence*)**: "…by R6c (RestorationByReemission, ASN-0086), whose conclusion is path-quantified over `→*`-successors, the category B2 excludes, so it travels instead by the projected-path license of Corollary RangeSterilization (i) (Range sterilization): ProjectionBridge maps the `→_sh*`-derivation onto `π(Σ') →* π(Θ)`, R6c's hypotheses hold at `π(Σ')` (pure L-reads, B1), and B1 carries its conclusion … back."

**Problem**: This is, modulo renaming of states, the identical argument spelled out inside Corollary RangeSterilization (i): "R6c's conclusion is path-quantified over `→*`-successors — the category B2 excludes … so it needs a path-level license: ProjectionBridge's step-mapping clause gives, by induction on the derivation, `π(Θ) →* π(Θ')`; R6c's hypotheses hold at `π(Θ)` (pure L-reads, shared by B1) … and B1 carries its conclusion … back." The same multi-step transfer device — a bridge-level fact, since it uses only ProjectionBridge and B1 — is derived inline in two sections, and the persistence clause cites a corollary that appears only *later* in the document as the source of the device it then re-derives anyway. Duplicated inline derivations of one device are exactly the divergence risk the anti-bloat classifier targets, and the backward dependency (an operation contract leaning on a forward corollary for a proof technique) misplaces the fact: it belongs beside B2, which is where its exclusion is announced.

**Required**: State the path-transfer license once, as a named clause of the projection bridge (e.g., **B3**: any ASN-0086 result whose hypotheses are single-state C/M/L-reads and whose conclusion is quantified over `→*`-successors transfers along `π` of any `→_sh*`-derivation, by ProjectionBridge's step mapping plus B1 at both ends), prove it there, and cite B3 from both the Nullify_Binary persistence clause and Corollary RangeSterilization (i).

### Issue 2: Forward-deferral accretion onto Range sterilization, plus contract-internal meta-prose
**ASN-0126, multiple sections**: (a) The shape-gated emit: "The inherited contract guarantees that key *fresh*, not where it lands; that every deposit in fact lands at the pinned address `a_emit(Σ, d)` is derived from L-ContiguousPrefix once the bridge is available (frontier-landing, Range sterilization)." (b) Retraction as an attributed Binary: "And the first gap's cost extends to unfilled chain slots — Corollary RangeSterilization (Range sterilization)." (c) Nullify_Binary, *Coverage nullification*: "…and the unfilled chain slots that coverage reaches are sterilized (Corollary RangeSterilization, Range sterilization)." (d) Nullify_Binary, *Persistence*: "and under `→_sh` neither half of the permanence is free, so the contract supplies both transfers rather than leave the app to reassemble them."

**Problem**: Together with Issue 1's citation, four paragraphs in three sections defer to the same downstream section — the flagged accretion pattern. Instance (a) defends a question the gate section's own content never raises: nothing in that section consumes the pinning claim (P5 obtains it from `Emit_K`'s contract, not from frontier-landing; frontier-landing's only consumer is Range sterilization itself). Instance (c) imports a forward corollary by name into a postcondition list and uses "sterilized" before the term has been defined; the clause is not a property of Σ' but a claim about future emissions, proven two sections later. Instance (d) explains why the contract includes the persistence clause — author-to-reviewer justification — rather than stating anything the clause guarantees.

**Required**: Keep one forward pointer, at the point where the gap is first established (end of the two-gaps paragraph in Retraction as an attributed Binary, instance (b)). In (a), either delete the sentence or keep only the freshness-vs-landing distinction without the deferral. In (c), restrict the postcondition to what holds at Σ' (the `⊆ nullified(Σ')` statement already carries it) and let Range sterilization, which instantiates the wrapper case anyway, state the unfilled-slot consequence. Delete sentence (d).

### Issue 3: P6's inductive step establishes the fresh tuple's conjuncts at the wrong state
**ASN-0126, Reachable conformance**: "For the tuple a step newly deposits, P3 supplies all three conjuncts — the standard-triple shape from precondition (0) of `K.λ_sh`, registration from (i), conformance from (ii)."

**Problem**: Preconditions (i) and (ii) are evaluated at the pre-state Σ of the firing step; P6's claim is about the post-state Σ' (and P3, stated before P1 and P4 exist in the document, carries the same unindexed "is registered … Sh-conf holds" phrasing, so it cannot supply the post-state versions by itself). The proof is careful about exactly this transfer for tuples *already present* — citing L12, P1, and P4 in turn — but is silent about it for the tuple the step deposits. As written, the step case proves registration and conformance of the new tuple at Σ, not at Σ', leaving a half-step gap in the induction.

**Required**: Add the transfer for the fresh tuple: registration at Σ' by P1 (or directly by the step's own registry frame condition), and the Sh-conf verdict at Σ' by P4. Alternatively, state once that both conjuncts are state-independent over reachable states and apply that observation uniformly to fresh and persisting tuples.

### Issue 4: The "strictly stronger" wp claim is unscoped and contradicted per-substrate by the note's own configuration sweep
**ASN-0126, Weakest precondition of the shape-gated emit**: "This weakest precondition is *strictly stronger* than `K.λ_sh`'s own precondition: … **Both** can fail for a gate-clearing emit."

**Problem**: Strictness depends on the registry, and Range sterilization proves it. Under "[R] unregistered" the note itself states "C2 and C3 holding at every emit", and under "[R] registered Unary" every `L_R` tuple has `coverage(G') = ∅`, so C2 and C3 again hold at every gate-clearing emit over every reachable state. In both configurations the wp coincides with the operation's precondition as predicates over that substrate's reachable states — it is not strictly stronger there. Both offered witnesses (the Binary self-emit; a pre-existing covering `L_R` tuple) presuppose [R] registered Binary or Multi. A note that is elsewhere exact about its quantification domains ("over `→_sh*`-reachable Σ") leaves this claim ambiguous between a per-substrate statement (false for two of the four configurations) and a class-of-substrates statement (true, witnessed only by Binary/Multi registries).

**Required**: Scope the claim — e.g., "strictly stronger whenever [R] is registered Binary or Multi; under the unregistered and Unary configurations C2 and C3 hold at every gate-clearing emit (Range sterilization) and the wp coincides with the precondition" — or state explicitly that strictness is quantified over the class of admissible registries and name the witnessing configuration.

## OUT_OF_SCOPE

### Topic 1: Multi-app composition of `Σ_init.registry`
The note's registration story is single-app ("An app *declares* a type by placing its `[K_j] ↦ shape` entry in `Σ_init.registry`"), and C0 forbids `~`-equal keys, but nothing governs how several apps sharing one substrate merge their declarations or what resolves a coverage-class collision — two apps declaring the same `[K]` with different shapes.

**Why out of scope**: The construction protocol for `Σ_init` is new territory adjacent to Open Question 4 (standard registrations), not an error in this framework's state, transition, or invariant content; C0 is the correct boundary for this note.

VERDICT: REVISE
