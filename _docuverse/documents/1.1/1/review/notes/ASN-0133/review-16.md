# Review of ASN-0133

This is a scrupulous note — it names its hypotheses, distinguishes static from effective, open from closed, weak from strong fairness, and anticipates most objections. The main termination results (Q0/Q1 unconditional; Q-EXT; Q5/Q5a; Q6 across its three obstructions) hold up under checking, including the delicate H-SFAIR⟹H-FAIR scoping and the H-W foil argument. The findings below are real but mostly off the critical path of the termination theorem; one is a recurring overstatement, one is a smuggled assumption against the note's own discipline.

## REVISE

### Issue 1: "Heterogeneous-view ⟹ not one PL term" ignores the cross-view rebuild the note's own foundation provides

**ASN-0133, Q0 (Recognizability)**: "For a heterogeneous-view registry the merge is blocked and `quiescent_R` is a finite metalevel conjunction of separately-viewed PL predicates, not one PL term."

**Problem**: The note establishes "not one PL term" only against the *naive* PC0 conjunction that keeps each view-parameterized atom at its native view. But PC3 — which Q0 cites for the same-view requirement — also makes `A_K` and `L_K` *fixed-view bases* denoting the active and audit slices "at every term view," and gives cross-view rebuilds through them (`members(K, audit) = ⋃(L_K, addrs_F)` inside an active-view term). By the same device an active read rebuilds inside an audit (or any) term — `members(K, active) = ⋃(A_K, addrs_F)` — and a default-view collection read rebuilds as `{x ∈ ⋃(A_K, addrs_F) : ¬(∃ J :: is_filtered_J(x))}` over the fixed-view bases; verdict/Boolean atoms (`is_K`, `is_in_chain`, `age`, `tip`) are never UV-rewritten, so they already read one fixed slice. Since `quiescent_R` conjoins only *Boolean* triggers, every view-parameterized constituent is rewritable at one chosen term-view, unifying the views into a single PC0 term. So "not one PL term" is unjustified and appears false: `quiescent_R ∈ PL` even when triggers natively differ in view. The single-view-vs-heterogeneous distinction is repeated as a structural fact in Q0, Q7, and the abstract, so the overstatement recurs.

**Required**: Either exhibit a genuinely non-unifiable Boolean trigger (a view-parameterized read with no fixed-view-base rewrite) to justify "not one PL term," or retract it — stating that only the naive same-view merge is blocked, while the fixed-view-base rewrite makes `quiescent_R ∈ PL` for any registry. The latter would *strengthen* Q0 and collapse the single-view caveat in Q0/Q7 rather than weaken anything.

### Issue 2: Fire atomicity is smuggled into the σ model, against the note's stated discipline

**ASN-0133, RG / H-FAIR**: "Between two fires a rule domain `[D_ρ]` may grow or shrink under an environment step." / "σ = (Σ₀, s₁, Σ₁, s₂, …) interleaves, from Σ₀, two kinds of step: a fire of some `(ρ, x)`… and an environment step — any non-registry `→_sh*` transition."

**Problem**: A fire is "a finite sequence of `→_sh` steps… `Σ →_sh* Σ'`," and an environment step is *also* a `→_sh*` transition — yet σ interleaves the two only at the macro-step boundary: environment steps fall "between two fires," never inside one. This makes each multi-step fire *atomic* against environment interleaving. On the shared substrate the note repeatedly emphasizes, nothing in the cited semantics serializes a contiguous run of `→_sh` steps — ASN-0128's I4 serializes *individual* `→_sh` steps, not runs of them. The atomicity is load-bearing: X-DEF reads "every fire yields Σ' with `T_ρ(x, Σ') = ⊥`" off the fire's *own* post-state, which an interleaved environment step would perturb for any non-monotone trigger. The note commits to "named hypotheses rather than smuggled," and this one is smuggled into the σ construction, gestured at only by the deferred "concurrency reconciliation."

**Required**: Name the serialization/atomicity assumption and locate it — as a property the deferred scheduler supplies, or by restricting a fire to a single surface call. The honest observation is available for free: the marker-pattern fires that carry Q5a/Q6 emit one tuple, so they are single-step and atomic by I4; the restriction costs the load-bearing results nothing. State that, rather than leaving multi-step atomicity implicit in the general model.

### Issue 3: The fixed `addr` projection cannot express the "per-target" tier the note advertises for tuple-domained rules

**ASN-0133, SC / Q7**: "`π_ρ` is the identity on an address-valued `D_ρ`… and V-TUP's address projection `addr : Tup → T` on a tuple-valued `D_ρ` (filter body `S(addr(x))`, scoping each tuple by its own address)." / "Canonical tiers (per-target, per-collection, system-wide) are application vocabulary over this machinery."

**Problem**: `π_ρ` is *fixed* to `addr` for tuple-valued domains, so the worked example's resolver (domain `L_cmt`) is scoped only by a comment's own tuple-address — never by the comment's target (`coverage_G`). A comment is homed on its finding's chain, so `addr(c)` is not in its target's region; `S(addr(c))` cannot express "comments about target T." The "per-target" tier, cited as expressible "over this machinery," is therefore unrealizable for tuple-domained rules: per-target resolver quiescence under `addr`-scoping is vacuous (no comment's address lies in the target region), so it does not capture "every comment about T resolved." The machinery under-delivers on a tier the note names.

**Required**: Either generalize `π_ρ` to a rule-chosen projection (so a tuple rule may scope by `coverage_G`/`coverage_F`, not only `addr`), or scope the claim — say that `addr`-projection realizes per-target scoping only for address-domained rules, and state what "per-target" means for a tuple-domained rule.

### Issue 4: No concrete fire-sequence trace exercises Q0 and Q6's reaching-claim

**ASN-0133, Worked composition**: structural verification only.

**Problem**: The worked composition verifies SF spelling, the extinction contracts, the Q5a bound, and single-view-ness for the cmt/res registry — genuine concrete checks — but never traces a fire sequence. Q0's central construct (the nested-quantifier `quiescent_R`) and Q6's reaching-claim are *applied* to the registry abstractly; neither is exercised on a specific `Σ₀ → … → Σ_terminal`. The depth standard asks the key postconditions be checked against one concrete scenario, and the note's title is precisely about reaching the terminal state.

**Required**: Add a short trace — e.g., `Σ₀` with target `t` flagged and uncommented; `ρ_P` fires, emitting `cmt c`, driving `T_P(t) → ⊥`; `ρ_R` fires, emitting `res`, driving `T_R(c) → ⊥` — then *evaluate* `quiescent_R` at the terminal state and confirm it returns ⊤ (checking that the nested quantifier actually computes "every flagged target commented, every comment resolved"), and that this is the finite, reached-and-held sequence Q6 promises for the grow-only resolver.

## OUT_OF_SCOPE

### Topic 1: The note's own deferrals are correctly future work
The scheduler (H-FAIR construction), the environment model, the `pd_extinct` SF certificate, a PL surrogate for H-W, per-scope-vs-global settling, and bounded cross-scope re-entry are all listed under "What this note doesn't cover" / "Open questions." Each is genuinely a layer above or a future ASN, not a gap in this one — the note draws those lines correctly.

### Topic 2: Convergence rate and liveness-while-non-quiescent
Q6 establishes *that* quiescence is reached under its hypotheses but says nothing about *how fast*, nor what progress is guaranteed while a system is still non-quiescent (e.g., monotone shrinkage of the trigger-true frontier). A quantitative/liveness companion is reasonable future territory, not an omission here.

VERDICT: REVISE
