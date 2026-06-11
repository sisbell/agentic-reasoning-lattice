# Review of ASN-0116

## REVISE

(none)

This ASN withstands the checks that usually break operation specifications. The verification record, so the convergence claim is auditable:

**Composite validity (clause 1).** Each step's precondition was checked against the state its predecessors leave. K.α iteration: the `k = 0` branch correctly splits on the *content region* `{a' ∈ dom(C) : origin(a') = d}`, not the arrangement — and the ASN proves it matters with the re-insertion-after-full-contraction sub-case (b), where `V_S(d) = ∅` yet the start is a subsequent emission `[d.0.s_C.7]`. For `k ≥ 1`, the induction maintaining `shift(a, k−1)` as the region maximum is implicit but sound (ChainEnumerationInjectivity gives strict advance past all prior chain elements). K.μ⁻: strict contraction `n'_{s_C} = J−1 < N` holds down to `J = 1`, and the front-insertion boundary case exercises `n'_{s_C} = 0` explicitly — the one branch where "retain nothing" must still fire rather than degenerate. The intermediate-state D-SEQ★ needed to phrase the retention is discharged by the observation that no K.α step touches `M`. K.μ⁺: all five obligations (targets in `dom(C)`, S8a of added positions, dense-run D-CTG★/D-MIN★/S8-depth, `s_C`-restriction, strict-but-finite growth) are discharged individually, including prior-domain agreement — the reason the contraction must precede the extension at all, which the ASN correctly identifies as why no single K-atomic can realise the shift. K.ρ: preconditions hold post-K.μ⁺.

**Composite validity (clause 2).** J0/J1★/J1'★ all reduce to the range identity RAN, which I verified from the clauses: left images verbatim, suffix images re-slotted (range-old), block images exactly `A_new` (range-new by freshness against `dom(C) ∪ dom(L)`). The shifted-suffix subtlety — addresses at new V-positions inducing *no* provenance entries because J1★/J1'★ are range-based — is traced concretely in the worked example with `a_3, a_4, a_5`, including the P4★ appeal for their pre-existing records.

**IP1's maximality analysis.** The backward-merge possibility and forward-merge impossibility are both proved, not asserted. The forward-merge argument is correct under adversarial reading: `shift(a, n) ∉ dom(C')` by contiguous-initial-segment membership (ChainMembershipForOrigin) plus cross-chain disjointness, while the suffix head `M(d)(q_J) ∈ dom(C)` by S3★ — and the argument explicitly survives the transclusion regime where the suffix head's origin and ordering against `a` are unconstrained.

**IP4.** The four-part decomposition is exhaustive and pairwise disjoint (index intervals plus subspace split). The non-containment claim for the suffix-witness case is sound: `shift(v_max, n)` cannot be a prior witness in any of the three prior classes. The deliberate refusal to claim a fixed inclusion direction — with the vacated-slot re-coverage configuration showing why — is the correct strength.

**IP6.** The wp is genuinely weakest: the derivation `D(d, Σ') = D(d, Σ) ∪ Added` is licensed per-link by LP12 + RAN + LP3★/LP13, lifted to sets by F-LINK (`dom(Σ'.L) = dom(Σ.L)`), and the containment form `Added ⊆ D(d, Σ)` is correctly distinguished from the over-rejecting emptiness form. The worked example realises both sides of the separation: `ℓ ∈ Added ∩ D(d, Σ)` (harmless) and the orphaned `ℓ' ∈ Added ∖ D(d, Σ)` (a genuine LP18 resurrection breaking preservation). The coverage computations behind it are careful — the LP-Fin reduction of infinite prefix-subtrees to start-membership is fully discharged, including `#E = 2` for all store entries via chain form rather than the weaker C1b bound.

**Boundary cases.** Front insertion (`J = 1`), append (`J = N+1`), empty subspace with both content-region sub-cases, and occupied-slot rebinding (IP3) are all worked with concrete addresses. `n ≥ 1` excludes the zero-width insert by precondition.

**Notation discipline.** All cross-references are to foundation ASNs; no foundation concept is re-derived under new notation (`shift(t, 0) := t` follows the established convention; `inc(·, 0) = shift(·, 1)` is justified via TA5-SigValid/TA5(c) rather than assumed).

**Anti-bloat scan.** The paragraph justifying the K.μ⁻/K.μ⁺ decomposition is load-bearing (it proves no single atomic can realise the shift), not defensive meta-prose. The gapped/filled bridge is stated once and referenced thereafter. The ghost-reference configuration recurs across IP4, IP6, and the worked example, but each occurrence does distinct work (introduction, wp separation, instantiation). No relocated-finding residue or duplicate paragraphs found.

## OUT_OF_SCOPE

### Topic 1: Transclusion interactions (insertion point shared with another document's arrangement; provenance of transcluded placement)
**Why out of scope**: Both are correctly parked as Open Questions; placement-by-reference is COPY territory (ASN-0118 reframe), not fresh allocation.

### Topic 2: Concurrent insertions without a serializing authority
**Why out of scope**: The substrate's SequentialTransitionAxiom makes this a future relaxation of the transition model, not a gap in this operation's specification.

### Topic 3: Post-edit fragmentation obligations on the inserted run
**Why out of scope**: IP1 correctly stops at "a run, not necessarily maximal"; what later DELETE/REARRANGE owe the run's contiguity belongs to those operations' ASNs.

VERDICT: CONVERGED
