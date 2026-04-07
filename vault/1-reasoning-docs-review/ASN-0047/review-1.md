# Review of ASN-0047

## REVISE

### Issue 1: J0 claimed as derivation from S7a but is a new invariant
**ASN-0047, Coupling and isolation**: "Every freshly allocated I-address appears in some arrangement. This follows from S7a (ASN-0036): the address a bears the creating document's prefix, identifying a document d₀ ∈ E_doc whose arrangement must contain the new content."
**Problem**: S7a constrains address *structure* — the prefix of `a` identifies the creating document. It says nothing about the creating document's arrangement containing `a`. An address could be allocated into `dom(C)` with the correct prefix (satisfying S7a) while appearing in no arrangement whatsoever. The final clause — "whose arrangement must contain the new content" — does not follow from S7a. S7a tells you *which* document the address belongs to; it does not tell you *that* the address must appear in any `M(d)`.
**Required**: Present J0 as a new invariant with independent justification, not as a derivation from S7a. The justification can appeal to design intent (Nelson's description of content entering the docuverse), but the logical status must be honest: J0 is an axiom of the state transition model, not a theorem of ASN-0036.

### Issue 2: K.μ⁺ and K.μ⁻ do not state value preservation for unaffected mappings
**ASN-0047, Elementary transitions (K.μ⁺)**: "New V→I mappings are added to some d ∈ E_doc: dom(M'(d)) ⊃ dom(M(d))"
**ASN-0047, Elementary transitions (K.μ⁻)**: "Existing V→I mappings are removed from some d ∈ E_doc: dom(M'(d)) ⊂ dom(M(d))"
**Problem**: Both transitions specify only a domain change. Neither states that values at surviving positions are preserved:
- K.μ⁺ should state: `(A v : v ∈ dom(M(d)) : M'(d)(v) = M(d)(v))` — existing mappings unchanged.
- K.μ⁻ should state: `(A v : v ∈ dom(M'(d)) : M'(d)(v) = M(d)(v))` — remaining mappings unchanged.

Without these, K.μ⁺ could silently replace values at existing positions (conflating extension with replacement), and K.μ⁻ could modify values at surviving positions (conflating contraction with rewriting). This undermines the completeness argument: the claim that replacement decomposes into K.μ⁻ + K.μ⁺ depends on each being a *pure* operation (add-only, remove-only). If K.μ⁺ can also modify, then replacement doesn't need K.μ⁻, and the six-transition taxonomy is redundant rather than minimal.
**Required**: Add the value-preservation constraint to each transition's formal specification.

### Issue 3: Entity set partition is not exhaustive without element-level exclusion
**ASN-0047, The state model**: "The level predicates of ASN-0045 partition E into three strata"
**Problem**: ASN-0045 defines *four* level predicates: IsNode (zeros = 0), IsAccount (zeros = 1), IsDocument (zeros = 2), IsElement (zeros = 3). These four are mutually exclusive and exhaustive over ValidAddress tumblers. The claimed three-stratum partition E = E_node ∪ E_account ∪ E_doc holds only if no element-level address is in E. The ASN assumes this — elements live in `dom(C)`, not E — but never states it. Without the exclusion, a fourth stratum E_elem exists, P1's "uniformly across levels" is incomplete, and the temporal decomposition table is wrong.
**Required**: State explicitly: `(A e ∈ E :: ¬IsElement(e))`, or equivalently `E ⊆ {t : ValidAddress(t) ∧ zeros(t) ≤ 2}`. Then the three-stratum partition follows.

### Issue 4: P4 lacks base case and systematic verification
**ASN-0047, Coupling and isolation (P4)**: "In any reachable state where J1 has been satisfied for all prior transitions: Contains(Σ) ⊆ R"
**Problem**: P4 is an inductive claim. J1 is the inductive step (new pairs in Contains require corresponding R entries). Two gaps:

(a) No base case. The claim holds over "reachable states" but no initial state Σ₀ is defined. If Σ₀ = (∅, ∅, λd.⊥, ∅), then Contains(Σ₀) = ∅ ⊆ ∅ = R₀, and the base case is trivial — but it must be stated.

(b) No case analysis across transitions. The ASN derives J1 by wp for K.μ⁺ but doesn't verify that other transitions preserve Contains(Σ) ⊆ R. The cases are straightforward (K.μ⁻ can only shrink Contains; K.μ~ preserves ran(M(d)); K.α, K.δ, K.ρ don't touch M or only grow R) but "straightforward" is not "shown."
**Required**: State the base case. Show each elementary transition preserves P4, citing the relevant property (J1 for K.μ⁺, monotonicity for K.μ⁻, ran-preservation for K.μ~, frame conditions for the rest).

### Issue 5: Frame conditions and coupling constraints use incompatible scopes without clarification
**ASN-0047, Elementary transitions and Coupling**: K.μ⁺ frame states "R' = R", but J1 requires K.ρ to co-occur with K.μ⁺, which changes R. K.α frame states "M'(d) = M(d) for all d", but J0 requires K.μ⁺ to co-occur, which changes some M(d).
**Problem**: Two readings are possible:

(A) Frames describe individual transition effects; coupling describes required composition. Composite effects are the union. No contradiction.

(B) Frames describe the net effect of the transition (including coupled partners). Then K.μ⁺'s frame R' = R contradicts J1.

The ASN uses reading (A) but never says so. The same ambiguity affects composition ordering: J4 says fork compounds K.δ + K.μ⁺ + K.ρ, but K.μ⁺ requires `d ∈ E_doc`, which K.δ establishes — so K.δ must precede K.μ⁺. Similarly, J0 couples K.α with K.μ⁺, and S3 requires the I-address to exist before the V→I mapping is created, implying K.α precedes K.μ⁺. The ASN doesn't specify ordering.
**Required**: State that frames describe individual elementary transitions; coupling constraints describe required co-occurrence in composite transitions; and composite transitions are ordered sequences whose intermediate states need not satisfy all invariants, but whose final state must.

## OUT_OF_SCOPE

### Topic 1: Systematic preservation of ASN-0036 V-position invariants
The elementary transitions K.μ⁺ and K.μ~ introduce or rearrange V-positions but the ASN does not verify they preserve S8a (VPositionWellFormed) or S8-depth (FixedDepthPositions) from ASN-0036. The ASN selectively invokes S3 for K.μ⁺ but omits the structural V-position invariants.
**Why out of scope**: V-position structure constraints are tied to the mechanics of how V-positions are constructed, which depends on operation definitions (INSERT, COPY, REARRANGE) — all explicitly excluded from this ASN's scope. A future ASN defining those operations should verify S8a and S8-depth preservation.

### Topic 2: Initial state and system initialization semantics
The ASN defines transitions but not the starting state Σ₀. A minimal base case suffices for P4 (noted in REVISE Issue 4), but the full initialization semantics — how the first node, first account, and first document come into existence — is a separate topic.
**Why out of scope**: Initialization is about bootstrapping the entity hierarchy, not about the transition taxonomy this ASN establishes.

VERDICT: REVISE
