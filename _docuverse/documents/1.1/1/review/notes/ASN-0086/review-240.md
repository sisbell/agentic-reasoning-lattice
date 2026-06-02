# Review of ASN-0086

## REVISE

### Issue 1: R-Scope self-emit branch mis-attributes the `=∅` claim to R0a "at Σ"

**ASN-0086, R-Scope (SingleTupleScope) proof**: "Within the pre-state, R0a's antichain at Σ gives `{a' ∈ dom(Σ.L) : a ≼ a'} = {a}` in the P1 case (where `a ∈ dom(Σ.L)`), and `= ∅` in the self-emit case (where `a ∉ dom(Σ.L)` — `a = b` is fresh — and no pre-existing link extends it, again by R0a)."

**Problem**: R0a at Σ is `(A a, a' ∈ dom(Σ.L) :: a ≼ a' ⟹ a = a')` — it only quantifies over pairs *both* in `dom(Σ.L)`. In the self-emit branch the proof has just stated `a ∉ dom(Σ.L)`, so R0a-at-Σ has no instance whose first argument is `a` and cannot, as written, yield `{a' ∈ dom(Σ.L) : a ≼ a'} = ∅`. The claim is *true*, but its justification is the antichain at **Σ'** — where `a ∈ dom(Σ'.L) = dom(Σ.L) ∪ {a}`, so for any `a' ∈ dom(Σ.L)`, `a ≼ a' ⟹ a = a'` contradicts `a ∉ dom(Σ.L)`, giving `¬(a ≼ a')`. The proof invokes "R0a at Σ'" two clauses later for `a ⊀ b`, but groups the self-emit `=∅` under "R0a's antichain at Σ," which is the wrong end of the transition for a fresh address.

**Required**: Attribute the self-emit `{a' ∈ dom(Σ.L) : a ≼ a'} = ∅` to R0a at **Σ'** (the only state in which `a` is a store member), not to the pre-state antichain. The identical mis-grouping should be checked in the wp Case 1 derivation, which restates the same branch.

### Issue 2: R0's Value-shape consequence forward-references Emit_K for an L3 discharge that is self-contained

**ASN-0086, R0 (TupleAddressFreshness), *Value-shape consequence*** and proof: "The standard triple `(F, G, K)` discharges K.λ's L3 precondition by its typed signature (Definition — Emit_K)" / "which satisfies K.λ's L3-discharge precondition by its typed signature (Value-shape consequence above; Definition — Emit_K)."

**Problem**: The L3 discharge (arity 3, both content slots in `Endset`, non-empty type slot) follows directly from R0's *own* hypotheses — `(F, G, K) ∈ Endset × Endset × T_admissible` — which are in scope at R0. The pointer to `Definition — Emit_K` (a later section) adds nothing to the local reasoning and inverts the dependency: Emit_K is *defined as* K.λ specialized, and its totality proof cites R0. A forward pointer from R0 into the operation built on R0 is exactly the forward-reference accretion the anti-bloat classifier flags — a citation that does not advance the claim and couples the proof to a downstream definition it does not need.

**Required**: Discharge L3 from R0's local typed hypotheses without the `Definition — Emit_K` pointer. If a cross-reference is wanted at all, it belongs in Emit_K (pointing back to R0), not in R0 pointing forward.

### Issue 3: Defensive rationale in the relational-layer definition

**ASN-0086, Definition — relational layer**: "Everything else is unconstrained: the substrate's document- and content-allocation steps `K.σ` and `K.α` (which the layer does not rename but does not exclude — documents and content must be allocatable for any `Emit_K` to have a home) and non-`R` `Emit_K` steps may be freely interleaved."

**Problem**: The parenthetical "which the layer does not rename but does not exclude — documents and content must be allocatable for any `Emit_K` to have a home" explains *why* K.σ/K.α are admitted rather than stating *what* the layer permits. The content ("K.σ, K.α, and non-`R` `Emit_K` may be freely interleaved") stands without it. This is rationale-for-the-rule meta-prose of the kind that compounds across cycles.

**Required**: Drop the justifying parenthetical; keep the structural statement of which steps the layer admits.

## OUT_OF_SCOPE

### Topic 1: Higher-arity typed relations `L_K^{(n)}`
The treatment of `|Σ.L(a)| > 3` links as elements of higher-arity relations (raised in Open Questions) is genuinely new structure, not a gap in this note's standard-triple development.

### Topic 2: Concurrency/atomicity of Emit vs Observe
The consistency model for concurrent observation of non-monotone `A_K` transitions is future territory; this note's SequentialAtomicTransitions foundation correctly defers it.

VERDICT: REVISE
