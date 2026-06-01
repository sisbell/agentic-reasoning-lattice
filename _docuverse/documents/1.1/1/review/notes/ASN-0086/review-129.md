# Review of ASN-0086

I checked the R0–R7a proofs, the three operations, both wp cases, and the worked sketch against the foundation contracts. The relational reductions (R1–R4, R6a–R6c) and the freshness/conformance machinery (R0, R0a, R0a-Cor1/Cor2, R7a) are logically sound — I verified the Δ-enumeration/replay argument in R7a, the chain-index discharge (4)(Case A/B1/B2), and the Worked Sketch tumbler arithmetic, and they hold. The findings below are prose/scope, consistent with the `review-mode.anti-bloat` classifier.

## REVISE

### Issue 1: wp Case 2 retained for an actor outside the note's operation set, wrapped in justification prose
**ASN-0086, Weakest-Precondition Analysis, Case 2**: "The wp below is a foundation-level observation about K.λ, retained here only for contrast with the relational-layer specialization that follows... This note's own operation set `{Emit_K, Observe_K, Nullify}` is substrate-conforming and unit-depth-disciplined by construction and so never reaches regimes (ii)/(iii); they are stated tersely."

**Problem**: This is meta-prose explaining *why* the analysis is present rather than advancing it. The note's own operations only ever reach regime (i); regimes (ii) (crafted-span) and (iii) (self-nullifying R-typed) are reachable only by a *direct K.λ caller* that bypasses the relational layer entirely. The full four-conjunct wp, its necessity argument, and the regime taxonomy are therefore precondition analysis for an actor that is not in this note's vocabulary. The closing sentence ("The full four-conjunct form above remains the honest precondition for direct K.λ callers, which the substrate does not preclude") confirms the analysis is aimed outside the note. The relevant result for this note is the one-line specialization `d ∈ dom(Σ.M) ∧ K ∈ T_admissible`.

**Required**: Either (a) state the relational-layer wp (`d ∈ dom(Σ.M) ∧ K ∈ T_admissible`) as the primary result and demote the direct-caller regimes to a single sentence noting they exist for callers the substrate does not preclude, or (b) drop the direct-caller regimes as out-of-note-scope. Remove the "retained only for contrast" / "stated tersely" framing either way — the apology is the bloat.

### Issue 2: R0 proof carries a scope disclaimer that restates its own generality
**ASN-0086, R0 proof**: "Throughout this proof — both the freshness discharge here and the post-state invariant discharge below — we use per-address chain facts only... The argument therefore carries over to every state-local-conforming state... we do not restate this scope below."

**Problem**: This is a paragraph about the proof's reach rather than a step of the proof. The per-address character of each cited chain fact (FirstEmission, TA5-SigValid, the L1c chain reconstruction) is already evident at each use; the "we do not restate this scope below" promise is meta-commentary. The R0a-Cor1 proof carries the same self-justifying parenthetical ("Because the argument rests on clause (b) alone and never on ASN-0093's →-scoped ChainMembershipForOrigin, the conclusion holds at every substrate-conforming Σ — →*-reachable or ↝-reachable conforming-layer post-state alike").

**Required**: Drop both scope disclaimers. If generality over state-local-conforming states is load-bearing, it is established by the quantifier in R0's statement plus the per-step citations; it does not need a separate prose paragraph.

### Issue 3: the at-most-one-key-per-home discipline is elaborated in two definitions plus re-elaborated at each use
**ASN-0086, Definition — substrate-conforming state** ("Concretely, clause (b) rests on the at-most-one-key-per-home discipline: every transition in this note's vocabulary deposits at most one fresh link key per home per step — each K.λ primitive emits a single key at the sibling frontier, and a composite `↝`-step may touch several homes but contributes at most one fresh key to any single home. Under this discipline, if a step adds a fresh key at home `d`...") and **Definition — substrate-conforming layer** ("(including the at-most-one-key-per-home discipline)").

**Problem**: The discipline's content — "at most one fresh key per home per step, landing at the next contiguous chain index" — is stated in full in the state definition, lifted again in the layer definition, then re-narrated at R0a-Cor1's step and again at R7a discharge (4)(iii). The state-definition sentence already fixes the index-contiguity consequence; the downstream re-narrations duplicate it.

**Required**: State the discipline and its index-contiguity consequence once (in Definition — substrate-conforming state), and have R0a-Cor1 and R7a cite it by name without re-deriving "the next index past the frontier."

## OUT_OF_SCOPE

### Topic 1: Atomicity of Emit relative to concurrent Observe, and the observation-ordering guarantee
The note proves single-threaded structural properties; concurrency consistency (Emit/Observe atomicity, the consistency model under which `A_K` transitions are observed, ordering on Observe results) is correctly deferred to the Open Questions and would be a separate ASN, not a defect here.

### Topic 2: Attributed retraction
Nullify hardcodes `F = ∅`, so attribution-bearing retraction (Convention RetractionDirectionality's "from-set reserved for attribution") is expressible only via direct Emit_R. Whether the relational layer should offer an attributed-Nullify variant is new territory, not an error in the present operation set.

VERDICT: REVISE
