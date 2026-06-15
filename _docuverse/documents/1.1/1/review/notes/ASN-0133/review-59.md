# Review of ASN-0133

This is a strong, carefully-argued note. I checked the load-bearing proofs — Q0's view rewrite (including the worked heterogeneous merge at `Σ*`), Q-EXT's SF/extinction composition, Q5's per-σ injection, Q5a's domain-union bound and its closed-case `⟺` reversal, and the full Q6 case split (regime (i) constancy, regime (ii) grow-only under weak fairness, the holding/reaching counterexamples, and the H-SFAIR regime form) — and they hold up. The worked `cmt`/`res` trace computes correctly end to end. The findings below are a missing hypothesis, a mis-aimed internal reference, and anti-bloat residue; none touches the mathematical core.

## REVISE

### Issue 1: Fire dischargeability rests on an unnamed registered-home hypothesis
**ASN-0133, The rule model (RG) and Worked composition (trace)**: RG restricts a fire's calls to "the operation surface `{Emit_K, Nullify_Binary}` (ASN-0128; `Observe_K` reads, and reads are not emissions)" and defines a fire as "the application of some emission set satisfying `Post_ρ(x, Σ, ·)` — a finite sequence of `→_sh` steps through the surface."

**Problem**: Both surface emitters run through `K.λ_sh`, whose gate requires a registered home `d ∈ dom(Σ.M)` (ASN-0126/0128). The surface excludes `K.σ` and `K.α`, so a fire **cannot create its own home or content** — the home must pre-exist, supplied by the environment or by `Σ₀`. Yet RG writes "*some* emission set satisfying `Post_ρ` … a finite sequence of `→_sh` steps," presupposing a realizable sequence exists. The note's own thesis is "termination as a conditional theorem with every hypothesis named," and this dischargeability precondition is exactly such an unnamed hypothesis. The worked trace makes the gap concrete: `Σ₀` is given as "`t ∈ M_tgt` with `is_attn(t) = ⊤` … and `L_cmt = L_res = ∅`" — nothing in `dom(Σ.M)` — yet the first fire is "one `Emit_cmt` depositing `c` covering `t` — a single `→_sh` step," a step whose gate is never discharged because no home is exhibited.

**Required**: Name the precondition — either that each rule's `Post_ρ` emits into a registered home (so `Post_ρ`-satisfiability presupposes one) or that a valid home is a standing hypothesis on the environment — and populate `dom(Σ.M)` in the trace so the "single `→_sh` step" gate is actually established (registered home, plus `Sh-conf` for the Binary `cmt`: `|F| = 1`, `|G| = 1`).

### Issue 2: Cross-rule re-arm is asserted, deferred to a mismatched Open Question, and uses undefined terminology
**ASN-0133, Worked composition / Q4 / Open questions**: The worked composition closes with "the general cross-rule coupling discipline, where a non-SF lower rule makes re-arm a live route, is left to Open Question 4," invoking "Q4's warning that locally disciplined rules can re-arm each other."

**Problem**: Three distinct defects converge here.
- (a) **Mis-aimed pointer.** OQ4 is "Cross-scope oscillation … an outer-scope fire can repeatedly un-quiesce an inner scope" — a *scope*-hierarchy phenomenon (Q8). The Open Question that actually names cross-*rule* re-arm is OQ2: "catch the common divergence patterns (mutual re-arm cycles)." A reader following "left to Open Question 4" lands on the wrong topic.
- (b) **Undefined "lower rule."** No rule ordering is defined in the note; the coupling is described only informally ("acyclic," "forward (`ρ_P → ρ_R`)," "one way only"). "Lower" presupposes a partial order on rules that never appears.
- (c) **Never witnessed.** Q4's claim "locally disciplined rules can re-arm each other without bound" is the load-bearing motivation for the whole SF design (locality is insufficient), but the note's only worked registry is *deliberately acyclic*, so the mutual re-arm is asserted and deferred but never exhibited.

**Required**: Re-point the deferral to the Open Question that covers cross-rule mutual re-arm (OQ2, or broaden OQ4 to name it explicitly); define or drop "lower rule"; and either exhibit a minimal two-rule mutual-re-arm pair (two non-SF active-view triggers, each fire flipping the other `⊥→⊤`) or mark Q4's insufficiency claim as explicitly deferred rather than stated as established.

### Issue 3: Anti-bloat residue
**ASN-0133, Q6 proof and the view-rewrite prose** (note carries `review-mode.anti-bloat`):
- (a) **Excluded-case parenthetical.** Q6's "(A third conceivable obstruction, an environment alternating ever-fresh trigger-true arguments, would need unboundedly many distinct arguments and so is excluded outright by bounded growth (Q5a) — the regime's own standing hypothesis — and is not examined.)" raises a case the regime's *standing hypothesis* already forbids, only to dismiss it. This is the reviser-drift pattern — a paragraph imagining a case the precondition excludes. Drop it; "two counterexamples … establish that the extra hypothesis is necessary" stands on its own.
- (b) **Duplicated chain/audit remark.** The fact that an unfiltered walk forces top-level audit is stated in Q0 ("Top-level default is by contrast unsafe whenever a trigger consumes a walk-sequence atom unfiltered … the full walk is unrecoverable (C-reach)") and restated in the heterogeneous example ("Were a trigger to quantify over `chain`'s full walk, default would be unsafe … top-level audit would be forced (Q0)"). Two statements of one fact; keep the general one, drop the restatement.

## OUT_OF_SCOPE

### Topic 1: Concrete scheduler / fairness realization
**Why out of scope**: H-FAIR, H-SFAIR, and H-ATOM are stated as hypotheses; the scheduling disciplines that satisfy them and the serialization of multi-step fires are correctly deferred ("What this note doesn't cover"). This is future operational territory, not a defect.

### Topic 2: Cross-rule coupling discipline for non-SF triggers
**Why out of scope**: The *discipline* that bounds mutual re-arm among non-SF rules is genuinely a future ASN — only the broken *reference* to it (Issue 2) is an error in this note, not the deferral itself.

VERDICT: REVISE
