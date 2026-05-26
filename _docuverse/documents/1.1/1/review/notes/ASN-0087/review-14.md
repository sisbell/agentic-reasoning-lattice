# Review of ASN-0087

The ASN specifies MAKELINK as the composite `K.λ ; K.μ⁺_L`. I verified: the precondition discharge via S3★+S3★-aux+L14 chain (intermediate Σ_mid conditions reduced to original-state conditions); freshness across three layers (within-chain via ChainEnumerationInjectivity, cross-subspace via DisjointSubAllocatorChains, cross-document via T10); the L1c structural inc-chain `d → b_C(d) → b_L(d) → t_1^L(d) → ... → ℓ` with each TA5a admissibility bound (zeros(d)=2≤2 at k=2; zeros(b_L(d))=3≤3 at k=1) verified at saturation; per-state invariants discharged at Σ' (link entry: L0/L1/L1a/L1b/L1c/L3/L12/L14/L-fin; V-arrangement: S2/S3★/S8a/S8-depth/S8-fin/S8★/CL-OWN/CL-UNIQ/D-MIN★/D-CTG★/D-SEQ★; vacuous-by-frame: M0/S4/L11a/S7a-d/C-fin/P6/P7/P8/NodeLineage); composite-boundary properties (P4★/P4a/P7a) with J0/J1★/J1'★ separately discharged (J0 by `dom(C')∖dom(C)=∅`, J1★ structurally by `subspace(v_ℓ)=s_L≠s_C`, J1'★ by `R'∖R=∅`); transition invariants (M1 with equality, L12/P0/P1/P2/P3/S9). I checked the atomicity treatment of Σ_mid via three classes (α/β/γ), the side-effect biconditional via L12+LP3★+LP12 with temporal-direction via Store Monotonicity★, the wp analysis with home/non-home case split and standard-authoring collapse, the reflexive endset handling, and the worked example with reflexive variant (verified a₁≼a₁ trivially, ℓ⋠a₁/a₂ at differing positions, ℓ≼ℓ trivially in reflexive case yielding project={v_ℓ}).

## REVISE

(none)

The proofs are explicit at every step. Boundary cases are addressed (empty endsets for slots ≠ 3, first link via V_{s_L}(d)=∅, reflexive endsets, N=3 minimum). Every invariant conjunct is checked. The concrete worked example exercises both the regular and reflexive routes. The wp analysis exposes a non-trivial structural collapse under standard authoring. Derived consequences (M-Reflexive, M-PriorLinkDisc, M-DiscSymmetry) are explicitly derived. All cross-references are to foundation ASNs.

## OUT_OF_SCOPE

### Topic 1: Substrate reconciliation between `dom(M)` and `E_doc`
**Why out of scope**: The ASN acknowledges this notational gap and defers to a future substrate-reconciliation ASN. Affects every operation on the combined substrate, not just MAKELINK.

### Topic 2: Protocol-level composite atomicity
**Why out of scope**: SequentialTransitionAxiom guarantees per-elementary-transition atomicity; composite-level external atomicity for MAKELINK belongs to protocol-layer specification.

### Topic 3: Cascade dynamics under extended MAKELINK sequences
**Why out of scope**: Invariant preservation under cascades is argued via LP9+LP13+L12; detailed cascade dynamics (equilibrium, convergence) belong to a future discovery-semantics ASN.

### Topic 4: Endset discipline enforcement (StandardAuthoring vs L4 forward-reaching endsets)
**Why out of scope**: StandardAuthoring is named but not enforced as precondition. The policy question of when to require it belongs to future operation ASNs.

### Topic 5: V-position movement under K.μ~ and discoverability preservation
**Why out of scope**: K.μ~ rebinding of v_ℓ is noted; formal characterization belongs to a future link arrangement dynamics ASN.

### Topic 6: LP18 (Resurrection) discoverability when transcluding documents appear later
**Why out of scope**: LP18 is referenced in side-effects discussion; full development of resurrection semantics across long transition sequences is future work.

VERDICT: CONVERGED
