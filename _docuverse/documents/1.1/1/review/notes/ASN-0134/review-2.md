# Review of ASN-0134

This note is unusually thorough — it carries a worked example (§7), genuine wp analyses (§7, §9), and an explicit invariant partition with derived consequences. The depth standards are met. My findings are about cases the conflict analysis skips, not about missing scaffolding.

## REVISE

### Issue 1: K.σ (document registration) is in the step vocabulary but absent from the conflict analysis, the confluence result, and the contract

**ASN-0134, §1 / H1 / H2 / G-PO / MIC clause 2 / M1(c)**: §1 fixes the step vocabulary as `K = {K.σ, K.α, K.λ_sh}` and A1 counts *every* state-changing operation (K.σ included) as "exactly one atomic step." H0's proof reasons about K.σ explicitly ("a `K.σ`, which registers a document and frames both stores"). But the moment the note turns to *conflict*, K.σ silently vanishes:

- H1/H2 are stated for "two **allocation** steps" only.
- G-PO defines a schedule as "a finite set `O` of **allocation steps (K.α, K.λ_sh)** into homes **registered at Σ**" — registration is pushed entirely before the schedule.
- W1/W2 classify uniqueness of *allocated* addresses; document addresses are not "allocated in a home" — they *are* homes — so neither clause covers them.
- MIC clause 2 is "Per-home **allocation** serialization"; M1(c) claims "no writer collides with a concurrent writer's **allocation**."

**Problem**: K.σ has a real conflict structure that the note neither analyzes nor scopes out. In this note's chosen stack (ASN-0093, which the note deliberately keeps *instead of* ASN-0047's entity steps), `K.σ`'s precondition is `d ∉ dom(M)` with `d` **caller-supplied** — there is no document sub-allocator. So two agents proposing the *same* fresh `d` against a common pre-state both pass `d ∉ dom(M)`, and the first-to-commit forces the second's precondition to fail. That is a same-address collision structurally identical to H2, with no MIC clause governing it. There is also a register-before-allocate *dependency* (an allocation into `d` requires `d ∈ dom(M)`) that G-PO assumes away by requiring all homes pre-registered. Consequently MIC's minimality boast — "removing any clause admits a counterexample" — and M1(c)'s "no writer collides" are overstated: there is a collision mode (concurrent same-address registration) for which the contract has no clause and the safety theorem makes no claim.

This is an internal inconsistency, not merely an omission: the note reasons about K.σ in A1/A2/A6/H0 but drops it from exactly the deliverable (conflict → contract) it sets out to produce.

**Required**: Either (a) bring K.σ into the conflict analysis — state whether two K.σ commute (different `d`) or collide (same `d`), state the register-before-allocate dependency, and add the corresponding MIC clause and M1(c) case; or (b) explicitly and consistently scope document registration out, removing it from the steps that the conflict/confluence/contract claims quantify over and noting that document-address freshness is an assumed precondition supplied by the (excluded) entity-allocation layer. The current half-in/half-out treatment must be resolved.

### Issue 2: G1(ii)'s confluence is proven for a fixed step-schedule, but §4 applies it to runtime *operation* interleavings — where idem=⊤ dedup makes the committed survivor order-dependent

**ASN-0134, G1(ii) and §4 final paragraph**: G1(ii) reads "all linearizations are confluent — they reach one and the same final state, **with the same address at every chain slot of every home** … no committed address depends on how a linearization resolves it." §4 then applies this to agents: "leaving agents in different homes ≺-incomparable and so free to proceed with no coordination whatsoever; … by G1(ii) **they all reach the same committed state — observationally indistinguishable** … from the global order."

**Problem**: G1(ii) is proven for a **fixed** `(O, ≺)` of raw `→_sh` steps (G-PO), and at the raw level it is correct — `K.λ_sh` does no dedup, so two same-value deposits into distinct homes both commit and commute. But §4 applies G1(ii) to "every interleaving the runtime then produces," i.e. to interleavings of *operations*, and A1 itself says an idem=⊤ `Emit_K` **hit is zero steps**. The operation→step realization is therefore order-dependent: two agents in homes `d ≠ d'` both calling `Emit_K(F, G, K)` with `idem(K)=⊤` and coverage-equal `(F,G)` (dedup is over the *global* `A_K`, not per-home) realize as *different step sets* depending on order — in `X;Y`, X deposits at `a_emit(Σ,d)` and Y is a hit; in `Y;X`, Y deposits at `a_emit(Σ,d')` and X is a hit. The surviving tuple sits at the winner's home/address (this is precisely ASN-0128 I4's first-to-commit), so a *different* chain slot of a *different* home is filled depending on the race. That is observable: `Observe_K` returns the surviving tuple's address (`a` vs `a'`), and home-relative behaviors (BH4 `age`, denominated in the home's own traffic) differ. Per-home serialization gives no help here — the two emissions are cross-home, hence `≺`-incomparable, hence free-running.

So "no committed address depends on how a linearization resolves it" and "observationally indistinguishable" are false at the operation level for the very scenario the note's motivation invokes ("two simultaneous creators," concurrent assertion of the same fact). The note never reconciles G1's step-level confluence with ASN-0128 I4's first-to-commit order-dependence.

**Required**: Restrict the benignness claim to the raw step level (a fixed `O`), and state explicitly that the operation→schedule realization is order-stable only when no two concurrent operations are idem=⊤ with coverage-equal `(F,G)`. Add the carve-out: concurrent idem=⊤ coverage-equal emissions into distinct homes are operation-level **non-confluent** — first-to-commit (ASN-0128 I4) fixes the survivor's home and address, observable via `Observe` and home-relative behaviors — and per-home serialization does not make them confluent.

### Issue 3: A6 asserts the inductive step without a base case — Σ₀ is never anchored to a reachable/initial state

**ASN-0134, A6**: "*Every* state on `𝔼` is structurally canonical, **because each of these invariants is preserved by every single step**."

**Problem**: The justification is purely the inductive step. The foundation invariants it leans on (ASN-0093's store invariants, ASN-0126 P6/P1/P2, ASN-0128 R1/R2) are theorems about `→_sh*`-**reachable** states, i.e. states reachable from `Σ_init`. For A6 to follow, every `Σ_k` on `𝔼` must be reachable, which requires `Σ₀` to be reachable — yet §1 introduces `𝔼 : Σ₀ → Σ₁ → ⋯` without pinning `Σ₀ = Σ_init` (or otherwise reachable). "Preserved by every single step" is the step; the base ("`Σ₀` is canonical") is unstated. G-PO later requires a "reachable start state Σ," showing the intent exists elsewhere, but A6 — the claim the whole §5 partition and G1(i) rest on — is stated globally over `𝔼` without it.

**Required**: Anchor `Σ₀ = Σ_init` (or `Σ₀` `→_sh*`-reachable) where `𝔼` is introduced, so that A6 reads "every `Σ_k` is `→_sh*`-reachable, hence canonical by the foundations." One sentence; but without it the induction has no base.

## OUT_OF_SCOPE

### Topic 1: The concurrent document-minting discipline (account-level sub-allocators for document addresses)

**Why out of scope**: The *deeper* half of Issue 1 — how document addresses are made fresh under concurrency when several agents mint documents (e.g. via an account's `A_doc` sub-allocator, where same-account minting would be a same-allocator conflict and cross-account commutes) — belongs to the entity-allocation foundation the note deliberately excludes. Issue 1 above is the REVISE part (K.σ is in *this* note's vocabulary and step-counting but absent from its own conflict/contract claims); the full per-allocator treatment of document minting is legitimately a separate note. (Cross-server composition of per-home orders, Open Question 5, is likewise correctly deferred and already harness-scoped-out — not flagged.)

VERDICT: REVISE
