# Review of ASN-0087

## REVISE

### Issue 1: Notational overloading of ⊕ in composite expression
**ASN-0087, M-Comp and "Decomposition"**: "MAKELINK is the composite `K.λ ⊕ K.μ⁺_L`, in that order, applied to the same home document `d`."
**Problem**: `⊕` is the tumbler addition operator throughout ASN-0034 and used in spans/displacement contexts in ASN-0053, ASN-0058, ASN-0098. Reusing it for operation sequencing introduces an avoidable ambiguity in a specification that prizes notational precision.
**Required**: Use distinct notation — `K.λ ; K.μ⁺_L`, "K.λ then K.μ⁺_L", or "the 2-step composite of K.λ followed by K.μ⁺_L". Update M-Comp accordingly.

### Issue 2: M-Inv omits P4a, P7a, P3, M0, M1
**ASN-0087, M-Inv claim and "Invariant Preservation" section**: lists L0–L14, S2–S8★, CL-OWN, CL-UNIQ, D-CTG★/D-MIN★/D-SEQ★, S4–S7d, C-fin, P0–P2, P4★, P6, P7, P8, NodeLineage.
**Problem**: ExtendedReachableStateInvariants (ASN-0047) lists P4a and P7a alongside P4★ as Class (b) composite-boundary properties; M-Inv addresses P4★ but never mentions P4a (HistoricalFidelity) or P7a (ProvenanceCoverage). ExtendedTransitionInvariants requires P3 (the conjunction P0∧P1∧P2∧L12). ASN-0093 foundational invariants M0 (DocumentTumblerWellFormed) and M1 (ArrangementMonotonicity) are not listed either. All five are trivially preserved (R unchanged, dom(C) unchanged, dom(M) unchanged), but the ASN's claim of comprehensive invariant verification has gaps.
**Required**: Add explicit verification (even one-line "trivial — R unchanged" style) for P4a, P7a, P3, M0, M1. Also note S9 (TwoStreamSeparation) follows from P0.

### Issue 3: Freshness argument cites only ChainEnumerationInjectivity
**ASN-0087, "Freshness of the Allocation," within-d link chain**: "By ChainEnumerationInjectivity (ASN-0093), the chain `A_L(d) = (t_1, t_2, ...)` is strictly monotone under T1. Each K.λ event on `A_L(d)` consumes the next index in the chain..."
**Problem**: Strict monotonicity alone doesn't establish that K.λ produces an element outside `dom(L)`. The actual argument requires ChainMembershipForOrigin (ASN-0093) to establish that `dom(L) ∩ {ℓ' : origin(ℓ') = d}` is a contiguous initial segment `{s_1, ..., s_{n_d}}`, so `max{ℓ' ∈ dom(L) : origin(ℓ') = d} = s_{n_d}` and `inc(s_{n_d}, 0) = s_{n_d+1} ∉ dom(L)`. Without ChainMembershipForOrigin, the freshness conclusion does not follow.
**Required**: Cite ChainMembershipForOrigin alongside ChainEnumerationInjectivity. Make the contiguous-initial-segment step explicit.

### Issue 4: L1c chain T4-validity preservation lacks explicit zero-count tracking
**ASN-0087, "Invariant Preservation," L1c chain construction**: each step says "T4-validity preserved by TA5a" without tracking zero counts.
**Problem**: TA5a's preservation condition for `k=2` requires `zeros(t) ≤ 2`; for `k=1` requires `zeros(t) ≤ 3`. The proof needs explicit verification that these bounds hold at each step. The values are:
- `zeros(t₀) = zeros(d) = 2` ✓ (satisfies `k₁ = 2` bound)
- `zeros(t₁) = zeros(b_C(d)) = 3` (one new zero from separator)
- `zeros(t₂) = zeros(b_L(d)) = 3` (k=0 preserves)
- `zeros(t₃)` ≤ 3 must be checked before applying step k=1
This tracking is absent.
**Required**: Add a one-line zero-count column to the chain table, or insert a single sentence verifying that the `k=1` bound at step 3 is met (`zeros(b_L(d)) = 3 ≤ 3`).

### Issue 5: M-Disc claim is a restatement of LP12 without MAKELINK-specific content
**ASN-0087, M-Disc claim**: "After MAKELINK: `discoverable_from(ℓ, d_target, Σ') ⟺ (E i : coverage(Σ'.L(ℓ).eᵢ) ∩ ran(Σ'.M(d_target)) ≠ ∅)`, by LP12."
**Problem**: This is LP12 at any state — substituting `Σ'`. It introduces no claim that's not already a theorem at every reachable state. M-WP is the substantive contribution; M-Disc duplicates LP12 without adding MAKELINK-specific content. Either it should be reframed to assert what MAKELINK *establishes* (e.g., for the fresh `ℓ`, the post-state's `ran(Σ'.M(d_target))` is computable from the pre-state's `ran(Σ.M(d_target))` plus the placement effect), or removed in favor of M-WP.
**Required**: Either delete M-Disc as redundant, or strengthen it to a MAKELINK-specific consequence not already implied by LP12 alone.

### Issue 6: M-Inv conflates per-state and transition invariants
**ASN-0087, M-Inv**: groups L-invariants, S-invariants, and "unchanged-component invariants (S4, S7a, S7b, S7c, S7d, C-fin, P0, P1, P2, P4★, P6, P7, P8, NodeLineage)" together.
**Problem**: P0, P1, P2 are transition invariants (state-pair predicates), while S4, S7a, etc., are per-state invariants. ASN-0047 cleanly distinguishes ExtendedReachableStateInvariants from ExtendedTransitionInvariants. Mixing them obscures what is being claimed about Σ' alone vs. the transition Σ → Σ'.
**Required**: Split M-Inv into two claims (or two clauses): per-state invariants at Σ', and transition invariants for Σ → Σ' (which discharges P3 explicitly).

### Issue 7: K.μ⁺_L precondition `subspace(v_ℓ) = s_L` not explicitly discharged
**ASN-0087, "Preconditions"**: Derives `ℓ ∉ ran(Σ.M(d))` via S3★ chain but doesn't verify `subspace(v_ℓ) = s_L`.
**Problem**: K.μ⁺_L's precondition (ASN-0047) explicitly requires `subspace(v_ℓ) = s_L`. The ASN constructs `v_ℓ = [s_L, k]` so this holds by inspection, but the verification chain should be explicit. Similarly `#v_ℓ = m_L = 2` should be discharged from LinkVPositionDepthAxiom.
**Required**: Add a one-sentence discharge: `subspace(v_ℓ) = (v_ℓ)₁ = s_L` by construction; `#v_ℓ = 2 = m_L` by LinkVPositionDepthAxiom.

## OUT_OF_SCOPE

### Topic 1: Linking permission enforcement
**Why out of scope**: The ASN correctly notes that MAKELINK does not verify ownership of referenced documents per Nelson's publication contract. Permission models belong to a future protocol-layer ASN, not to the substrate's link-creation operation.

### Topic 2: Protocol-level atomicity mechanism
**Why out of scope**: The ASN punts composite-level atomicity to the protocol layer above the substrate. The specific mechanism (transactional wrapping, request-response coupling, etc.) is correctly noted as not the substrate's responsibility.

### Topic 3: Index maintenance specifics (spanfilade)
**Why out of scope**: M-NoIndexState correctly establishes that the abstract specification requires no separate index state. Implementation-specific indices for performance are a layer below the abstract spec.

### Topic 4: Multi-invocation MAKELINK sequencing semantics
**Why out of scope**: How sessions of MAKELINK calls compose, ordering across concurrent callers, etc., are protocol concerns beyond a single operation's specification.

VERDICT: REVISE
