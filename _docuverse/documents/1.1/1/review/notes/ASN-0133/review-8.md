# Review of ASN-0133

This is an unusually disciplined note. The meta-level/registration-checkable line is drawn carefully and repeatedly (Q3's reachable-vs-schema split, the H-W-as-foil framing, the SF-spelling vs extinction-discipline decomposition), the falsifier accounting (Q-FLIP) correctly catches the `target_of` re-arm that the "no retraction ⟹ flip-once" folklore misses, and Q6's proof handles the no-real-fire, has-real-fire, and finite-σ cases separately rather than by "similarly." Most of what I checked holds. Two things do not.

## REVISE

### Issue 1: The fire-sequence model is closed, which trivializes Q5a's "route" and the worked example's conditionality

**ASN-0133, "The rule model" / "Conditional termination" (Q5a) / "Worked composition" (Bound)**: RG defines `σ = (Σ₀, fire₁, Σ₁, …)` where each fire is a registry rule's application, `Σ →_sh* Σ'`. Q5a then claims bounded domain growth is a substantive route to H-RF — "trading the cross-rule re-arm analysis for a domain-growth bound" — and the worked example concludes: "the registry terminates iff the population of targets that ever need attention is bounded, which is the registry's one honest hypothesis on its environment."

**Problem**: As written, `σ`'s only transitions are registry fires (each `Σ_{k+1}` is the result of `fire_k` on `Σ_k`; nothing else moves the state). Under that reading, by QD-fin (ASN-0129) every domain is finite at each state, and a domain acquires new elements *only through deposits, which come only from the registry's own real fires*. Work this through:

- In the worked registry `{ρ_P, ρ_R}`, no rule emits or retracts `attn` or `tgt` (`ρ_P` emits `cmt`, `ρ_R` emits `res`). So `A_attn` and `A_tgt` are constant along every `σ`, and the producer domain `[D_{ρ_P}] = {t ∈ M_tgt : is_attn(t)}` (active) is therefore *static* — equal to its `Σ₀` value `F₀`, finite by QD-fin.
- By Q-EXT, `ρ_P` real-fires at most once per `t`, so `ρ_P` real fires `≤ |F₀| < ∞`. Each emits ≤1 `cmt`, so `|⋃_k [D_{ρ_R}]_{Σ_k}| = |comments| ≤ |F₀|`, and `ρ_R` real fires `≤ |F₀|`. Total real fires `≤ 2|F₀| < ∞` **unconditionally** — H-RF holds with no extra hypothesis, and by Q6+H-FAIR the registry terminates under fairness with nothing assumed about an "environment."

So the "honest hypothesis on its environment" is `|F₀| < ∞`, which QD-fin already guarantees; the "iff" has a right side that is always true. The conditionality is real only in an *open* model where targets are flagged by something outside the registry's own fires — which RG does not formalize.

This is not confined to the example. For the whole class Q5a targets (closed, all-SF, extinction-disciplined): infinitely many distinct domain elements appearing across `σ` requires infinitely many deposits, hence infinitely many real fires; so `bounded-domain-growth ⟺ H-RF`. Q5a's hypothesis is then equivalent to its conclusion, and the advertised "trade" (prove a domain bound instead of analyzing re-arming) buys nothing — you have proven the conclusion. The machinery is evidently *designed* for an open model: SF's ⊥-stability (Q-EXT) gives at-most-once-per-argument against *any* `→_sh` step including external ones, and bounded *external input* is exactly what would make Q5a's domain bound an independent, attainable hypothesis. But that model is not the one RG writes down.

**Required**: Either (a) formalize the open setting the hypotheses presuppose — admit non-registry `→_sh` steps into the sequence (or as an explicit environment that grows slices between fires), and re-state Q5/Q6/Q5a so the domain-growth bound is a bound on that external input rather than on the registry's own fire-reachable states; or (b) keep the closed model and correct the claims accordingly: state that for closed all-SF+extinction registries `bounded-domain-growth ⟺ H-RF` (so Q5a is a restatement, not a route), and replace the worked example's "terminates iff bounded need-attention, an environment hypothesis" with the true closed-model fact (it terminates unconditionally under fairness, the producer domain being static-finite). The note cannot have it both ways — Q5a's "route" framing and the example's conditionality both require external domain growth that the current `σ` excludes.

### Issue 2: H-FIN is stated as an existential where the operative reading is universal

**ASN-0133, "The rule model" (RG)**: "a fire terminates exactly when the contract it discharges admits a finite emission set — H-FIN is the contract-level demand that it does."

**Problem**: The biconditional is wrong as a per-fire statement. A fire applies *some* emission set; whether it terminates depends on *that chosen set* being finite, not on the contract *admitting* (∃) a finite set. A contract admitting both a finite and an infinite emission set satisfies "admits a finite emission set," yet a body may choose the infinite one and not terminate — at which point the fire has no post-state `Σ'` and the sequence model is undefined. The very next sentence gives the correct reading — "a nondeterministic body terminates iff *every* `Post_ρ`-satisfying fire sequence it can produce does" (∀) — so the model genuinely needs the universal form, and H-FIN's `∃`-flavored spelling contradicts it.

**Required**: State H-FIN as the universal: *every* `Post_ρ`-satisfying emission set is finite (equivalently, every admissible fire sequence terminates). Then "a fire terminates iff its emission set is finite, and H-FIN demands all admissible sets are" is consistent with the universal-over-choices reading and soundly underwrites every fire having a post-state.

## OUT_OF_SCOPE

### Topic 1: Shipping the SF certificate class (`pd_extinct`)
**Why out of scope**: Open Question 1 correctly identifies that ASN-0130 ships only `pd_stable` (ST⁺) and no SF certificate, leaving SF membership the load-bearing *uncertified* (though decidable) registration check. Adding a `pd_extinct` designated class is a future extension of ASN-0130's catalog, not a defect to repair here.

### Topic 2: Scheduler construction, stochastic bodies, activation binding
**Why out of scope**: The note explicitly defers these to the protocol layer ("What this note doesn't cover"), and that deferral is appropriate — H-FAIR as a stated hypothesis with no shipped scheduler is the honest treatment for a substrate-level note, consistent with its thesis that fairness is named, not discharged.

VERDICT: REVISE
