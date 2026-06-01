# Review of ASN-0086

This note is mathematically careful — the operation set (Emit_K, Observe, Nullify) is well-bounded, the wp analysis (both cases) is genuinely non-trivial with necessity arguments per conjunct, and the worked sketch exercises R0/R2/R3/R6a/R6b/R6c against concrete tumblers. The substantive content has converged. The note carries `review-mode.anti-bloat`, and the remaining findings are forward-reference accretion and a single trivial-but-unproven lift.

## REVISE

### Issue 1: Clause (b) of substrate-conforming layer enumerates consumers and argues its own necessity
**ASN-0086, Definition — substrate-conforming layer, clause (b)**: "This contiguity is the hypothesis R0a Case 2, R0a-Cor1, and R7a consume." … "Clause (b) is not implied by clause (a): the tumbler `a* = [d.0.s_L.1.1]` is T10a-conforming and L-invariant-admissible … yet lies off `A_L(d)`'s sibling-frontier chain … Clause (b)'s frontier condition is what excludes such off-frontier keys."

**Problem**: Two flagged patterns in one definition slot. The first sentence is a downstream-consumer inventory ("the hypothesis R0a Case 2, R0a-Cor1, and R7a consume"). The `a*` paragraph is a defensive necessity argument — it explains *why the clause is needed* (independence from clause (a)) rather than stating *what the clause requires*. A definition should state the frontier-emission obligation and stop.

**Required**: Reduce clause (b) to its content — "the homed-set `{a ∈ dom(Σ.L) : home(a) = d}` is a contiguous initial segment of `A_L(d)`'s chain enumeration; a layer discharges this by emitting every fresh link key at its home's sibling frontier." Delete the consumer list and the `a*` independence essay.

### Issue 2: substrate-conforming state def carries a convoluted dual-state justification with forward reference
**ASN-0086, Definition — substrate-conforming state**: "Both every `→*`-reachable state — the K-op primitives K.σ/K.α/K.λ satisfy (a) and (b) by their ASN-0093 contracts — and every `↝`-reachable state produced by a substrate-conforming *layer* (Definition — substrate-conforming layer, below) — whose clauses (a)/(b) are exactly the two conditions named here — satisfy these clauses."

**Problem**: The sentence defends, with a nested forward reference, that two classes of states both satisfy clauses already stated immediately above. The em-dash insertions ("whose clauses (a)/(b) are exactly the two conditions named here") restate the definition's own content. The reader must unpack the parenthetical scaffolding to extract a claim the definition has already made.

**Required**: State the definition (clauses (a) and (b)) once. If the coincidence between this definition's clauses and the layer definition's clauses is load-bearing, assert it where the layer is defined, not as a forward-referencing aside here.

### Issue 3: R0a-Cor1 substantive-postcondition (b) and the #E=2 narrowing are each stated in multiple places
**ASN-0086, R0a-Cor1**: main statement says "with `J_d^Σ = -1` denoting the empty set when no link is homed at `d`"; then "Substantive postconditions" (b) repeats: "J_d^Σ = -1 absorbs the empty case. By convention `J_d^Σ = -1 ⟺` the homed-set is empty."

**Problem**: Postcondition (b) restates the convention already given in the main statement — "two paragraphs say the same thing in different words." Separately, the `#E ≥ 2 → #E = 2` narrowing of L1b appears three times: R0a-Cor2's parenthetical ("This narrows L1b's … to the tighter `#E = 2` strictly"), the Properties table R0a-Cor2 row ("tightens L1b's `#E ≥ 2` admission to depth-2 strictly"), and the Open Questions ("Should L1b's substrate-level admission `#E ≥ 2` … be tightened to `#E = 2`").

**Required**: Drop R0a-Cor1 postcondition (b) (it duplicates the main statement). For the L1b narrowing, keep the factual statement in one place (R0a-Cor2) and the design question in Open Questions; remove the duplicate framing from the table row, which should only label the lemma.

### Issue 4: R6c's "Consequence" attributes a transitive-closure claim to single-step R3 without the induction
**ASN-0086, Consequence after R6c**: "R3 (TypedSliceMonotonicity) makes the audit slice monotone — `Σ →* Σ' ⟹ L_K^Σ ⊆ L_K^{Σ'}`".

**Problem**: R3 is stated and proved for a single step (`Σ → Σ'`). The consequence asserts the `→*` (reflexive-transitive closure) version as if it were R3 directly. The lift is trivial, but it is an inductive lift, and the note elsewhere (R6c itself) performs exactly this induction explicitly — so the omission here is inconsistent.

**Required**: Either qualify as "R3 lifted along `→*` by the same induction as R6c," or state the `→*` monotonicity as a named one-line corollary. Don't present a closure claim as a direct consequence of a single-step lemma.

## OUT_OF_SCOPE

### Topic 1: Concurrency/atomicity of Emit vs Observe, and cardinality bounds on nullified(Σ)
**Why out of scope**: These are correctly deferred to the Open Questions. The substrate as specified is sequential (ASN-0093 SequentialAtomicTransitions), and a consistency model for concurrent observation is genuinely new territory, not a gap in this note's claims.

### Topic 2: Higher-arity links as `L_K^{(n)} ⊆ A_rel × ℘(A)^n`
**Why out of scope**: The note restricts to standard triples explicitly and flags the n-ary generalization as future work. Not an error here.

VERDICT: REVISE
