# Review of ASN-0116

I checked this as a proof manuscript: every clause of the valid-composite construction against the precondition each atomic step acts on, every boundary of the insertion point, every conjunct of the four named invariants, and the two non-trivial derivations (IP4's witness algebra and IP6's weakest precondition). It holds up.

## What I verified

**The valid-composite reduction is the load-bearing claim, and it is discharged honestly.** INSERT does not invoke ASN-0082's I3 family as a transition — the note correctly observes I3 is a postcondition spec — and instead exhibits the explicit sequence `K.α(×n) → K.μ⁻ → K.μ⁺ → K.ρ(×n)`, discharging each step's elementary precondition at the intermediate state it acts on. I confirmed:
- The freshness split across the `n` K.α steps is per-step correct: `k=0` is FirstEmissionFreshness or SubsequentEmissionFreshness depending on whether the content region is empty, and every `k ≥ 1` acts on a store the prior in-insert allocation has already made non-empty. The ordering `K.α` before `K.μ⁺` is necessary (K.μ⁺ needs `A_new ⊆ dom(C)` as targets), and the note says so.
- The `K.μ⁻`-before-`K.μ⁺` ordering is necessary, not merely chosen: were K.μ⁺ to install the shifted suffix `{q_{J+n},…,q_{N+n}}` while the old suffix `{q_J,…,q_N}` were still present, the overlap `{q_{J+n},…,q_N}` would force a new value onto an existing position, violating prior-domain agreement. After K.μ⁻ vacates, K.μ⁺ adds an all-fresh domain. Verified.
- The strict-contraction precondition `n'_{s_C} = J−1 < N` holds down to `J=1` (front insertion, `n'_{s_C}=0`), and K.μ⁻ is correctly dropped in the append/empty cases where `J−1 = N`.
- Clause-2 couplings (J0, J1★, J1'★) are driven entirely by RAN's range identity: the content-subspace range-new addresses are exactly `A_new`, the shifted-suffix addresses being range-*old* (re-slotted, same I-address). The J1'★ subtlety — that shifted-suffix addresses induce no new provenance because provenance keys on (I-address, document) and these are already in `R` by P4★ at the pre-state boundary — is correctly handled.

**Boundary coverage is complete.** Front (`J=1`, the only `n'_{s_C}=0` branch), append (`J=N+1`, K.μ⁻ dropped), empty subspace with *both* sub-cases distinguished — fresh document (first emission) versus re-insertion after full contraction (subsequent emission off a non-empty content region while the arrangement restarts at `q_1`). The independence of the K.α start address from the empty *arrangement* (it tracks the content region, not `V_S(d)`) is exactly the kind of distinction that is usually skipped, and it is drawn explicitly.

**IP1's maximal-run analysis is right in both directions.** The backward I-merge (when `q_{J-1}` holds the greatest origin-`d` address, so `a = inc(a_prev,0)` is I-adjacent) is correctly admitted, and the forward non-merge is proven by the frontier argument: `shift(a,n) ∉ dom(C')` (beyond the post-allocation frontier) while the shifted-suffix head `M(d)(q_J) ∈ dom(C)` by S3★, so they cannot coincide — for *any* origin of `M(d)(q_J)`, including transclusion.

**IP4 and IP6 are genuine derived consequences, not restated postconditions.** IP4's four-part witness decomposition is exhaustive and disjoint, the bijection onto (left ∪ shifted-suffix ∪ cross-subspace) is verified, and the non-comparability of the V-position witness sets (`project(Σ') ⊄ project(Σ)` when a suffix witness is present, via the greatest-shifted-witness argument; `project(Σ) ⊆ project(Σ')` may fail because vacated slots are re-populated) is correctly established — this prevents the false belief that prior link witnesses survive as the same V-positions. IP6's wp computes to a *containment* `Added ⊆ D(d,Σ)`, not an emptiness, and the note correctly identifies the ghost-plus-live-span pre-state that the (strictly stronger) sufficient emptiness form over-rejects. This is the non-trivial wp the standard demands.

## OUT_OF_SCOPE

### Topic 1: Insertion at a transclusion-shared position; concurrent-insertion freshness; transclusion provenance; post-edit fragmentation
**Why out of scope**: These are correctly confined to the note's own Open Questions. Each requires machinery this operation does not introduce (COPY/ASN-0118, an inter-authority serialization model, derivation-vs-allocation provenance). The note touches transclusion only where it must — IP5's isolation and IP1's forward-non-merge are stated to hold whatever the origin of a suffix address — without over-claiming.

### Topic 2: Link creation and link discovery
**Why out of scope**: IP4/IP6 govern how *existing* links fare under INSERT (coverage invariance, witness tracking, discoverability wp) using foundation `discoverable_from`/`coverage`; they neither create links (MAKELINK/K.λ, explicitly noted as a distinct operation) nor define a discovery operation (FINDLINKS). The boundary is drawn in the right place.

VERDICT: CONVERGED
