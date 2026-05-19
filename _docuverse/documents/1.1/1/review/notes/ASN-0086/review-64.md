# Review of ASN-0086

## REVISE

### Issue 1: R5's from-set case not explicitly demonstrated

**ASN-0086, R5 (TupleSelfTargeting) proof**: The claim states "the unit-depth span `(a, δ(1, #a))` is well-formed and may appear in the from-set or to-set of an emitted tuple".

**Problem**: Step 3 of the proof exhibits a self-targeting *to-set* emission via the triple `(∅, G_self, K)` (G_self in slot 2). The from-set case is not walked through. The "Generalization to arbitrary endset contents" paragraph licenses any L3-conforming triple, which implicitly covers `(G_self, ∅, K)` or `(G_self, F, K)` for the from-set case — but this remains implicit. The proof's explicit conclusion "a ∈ coverage(Σ'.L(a').e₂)" addresses only slot 2.

**Required**: After Step 4, explicitly note that the generalization licenses placing `G_self` in slot 1 (e.g., the triple `(G_self, ∅, K)` is L3-conforming and admits the same R0 verification), establishing `a ∈ coverage(Σ'.L(a').e₁)` for the from-set case. Alternatively, exhibit a second concrete emission for the from-set case in parallel with Step 3.

### Issue 2: Relational layer's "Nullify-is-sole-producer" discipline not explicit in Definition

**ASN-0086, Definition — relational layer**: "The relational layer's operations are {Emit_K, Observe_K, Nullify}..."

**ASN-0086, WP Case 2, Relational-layer discharge**: "Under the relational layer's committed operations (Emit_K, Observe_K, Nullify), regime (ii) is structurally impossible: every L_R^Σ tuple arises from a Nullify call..."

**Problem**: The Definition admits Emit_K for arbitrary K ∈ T_admissible. Since R ∈ T_admissible, a caller can directly invoke Emit_R(Σ, d_retr, F, G) with arbitrary endsets — including non-unit-depth to-spans like `{(d, δ(1, #d))}` — bypassing Nullify entirely. Such a call would deposit an L_R^Σ tuple that did *not* arise from Nullify, contradicting WP Case 2's strong claim. The discipline "every L_R^Σ tuple arises from a Nullify call" appears in Implementation Notes (as the "unit-depth retraction discipline"), but the formal Definition of the layer does not enforce it via the operation set.

**Required**: Either (a) the Definition should explicitly state that callers commit to invoking Emit_K only with K ≁ R (forcing R-typed emissions through Nullify), (b) the operation set should restrict Emit_K's domain to T_admissible \ [R], or (c) WP Case 2's "structurally impossible" claim should be weakened to "structurally impossible *under the additional caller-level discipline that R-typed emissions are routed through Nullify*" with the discipline lifted from Implementation Notes into the Definition.

### Issue 3: WP Case 2's `NoCraftedSpanReachesD` lacks a formal definition

**ASN-0086, WP Case 2**: "where *NoCraftedSpanReachesD* — no `(b, F', G') ∈ L_R^Σ` has a to-span coverage that contains the fresh sibling-frontier address Emit_K is about to deposit under `d`."

**Problem**: The predicate is described informally but never given a formal definition. The note uses `a_K(Σ, d)` (implicitly) for "the address K.λ would deposit at home d in state Σ" but doesn't introduce this auxiliary function. A reviewer reading the wp computation literally has to reconstruct both the predicate and the auxiliary function.

**Required**: Either define `a_K(Σ, d)` explicitly (per ASN-0093 K.λ's first/subsequent emission rule) and write `NoCraftedSpanReachesD(Σ, d) ≡ (A (b, F', G') ∈ L_R^Σ :: a_K(Σ, d) ∉ coverage(G'))`, or restructure the wp computation to avoid the unnamed predicate.

### Issue 4: R6c base case verification too compressed

**ASN-0086, R6c proof**: "*Base* (`n = 0`): immediate."

**Problem**: Even granting that the IH at n=0 is the precondition, the proof should state how the conclusion `(a, F, G) ∉ A_K^{Σ_0}` follows — namely, by Definition of A_K applied to `(a, F, G) ∈ L_K^Σ` and `a ∈ nullified(Σ)`. "Immediate" leaves the reader to reconstruct that the IH carries through to the conclusion at every chain position via Definition of A_K, including n=0.

**Required**: Replace "immediate" with one sentence — e.g., "Base (n=0): IH at Σ_0 = Σ is the precondition; by Definition of A_K, `a ∈ nullified(Σ)` and `(a, F, G) ∈ L_K^Σ` jointly give `(a, F, G) ∉ A_K^Σ`."

## OUT_OF_SCOPE

### Topic 1: Multi-arity typed relations `L_K^{(n)}`

**Why out of scope**: The note restricts to standard-triple (arity-3) links throughout, with the higher-arity case explicitly deferred to open question #2. The Definition of L_K^Σ requires `|Σ.L(a)| = 3`, so higher-arity links are not members of any L_K. Extending the active-subset machinery to multi-arity relations is genuinely new territory.

### Topic 2: Concurrency / atomicity of Emit vs Observe

**Why out of scope**: Open question #5 acknowledges this. The current development is sequential (per ASN-0093's SequentialTransitionAxiom).

### Topic 3: Coverage-class collisions between independently-chosen types

**Why out of scope**: Open question #9 names this. The model is well-defined under coverage-class equivalence; the design question of how layers coordinate type-catalog choices is layered above this ASN.

### Topic 4: Tightening L1b in ASN-0043 from `#E ≥ 2` to `#E = 2`

**Why out of scope**: R0a-Cor2 establishes `#E = 2` strictly within this substrate via ASN-0093's K.λ contract. Whether to amend ASN-0043's L1b admission is an upstream concern (open question #7).

### Topic 5: Observe result ordering and cardinality bounds

**Why out of scope**: Open questions #4 and #6.

### Topic 6: Substrate-level enforcement of unit-depth retraction shape

**Why out of scope**: Open question #8 names this — whether to introduce a dedicated K-operation for retraction is a substrate-level redesign question outside this note's scope.

VERDICT: REVISE
