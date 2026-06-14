# Review of ASN-0133

## REVISE

### Issue 1: "regime (i)" is defined three non-equivalent ways, and the proof establishes only the strongest

**ASN-0133, Q6 ("Reaching and holding, by hypothesis package") vs. Q6 Proof "(i)" vs. H-SFAIR "Satisfiability is environment-conditional"**:

- Package list: "**+ regime (i)** (the environment eventually stops presenting trigger-true work — idles): reached and held, for *any* registry."
- Proof: "**(i) Environment eventually idle** (finitely many environment steps): past both N and the last environment step the state is constant... contradicting H-FAIR — so the tail is quiescent and absorbing."
- H-SFAIR passage: "reaches-and-holds even against an environment that never idles — e.g. endless dom(Σ.C) deposits, which no `[D_ρ]` or `T_ρ` reads."
- Non-grow-only paragraph: "the environment eventually leave each argument in-domain and trigger-true until fired (regime (i) for the rule)."

**Problem**: These are three different conditions, and an environment that performs **endless K.α (content) deposits and nothing else** sits in the gap between them. Such an environment *stops presenting trigger-true work* (K.α touches only `dom(Σ.C)`, which no trigger reads — V-DOC/QD-audit), so the **package list classifies it as regime (i)** ("reached and held, for any registry"). But it has **infinitely many environment steps**, so the **proof's argument does not apply** — there is no "last environment step," the full state is *not* constant, and the constant-tail contradiction never starts. And the **H-SFAIR passage explicitly classifies it as "never idles,"** presenting it as the case H-SFAIR uniquely handles — which directly contradicts the package list's classification of the same environment as regime (i).

So either the package-list claim is unproved (the proof's regime (i) covers only finitely-many-steps, not "stops presenting trigger-true work"), or the H-SFAIR distinguishing example is wrong (regime (i) already covers endless-K.α). Both cannot stand.

**Required**: Give regime (i) a single precise definition. The definition that makes the constant-tail argument work *and* covers endless-K.α is "the footprint-relevant state — the `dom(Σ.M)`/`Σ.L` portions every `[D_ρ]` and `T_ρ` reads (FP) — is eventually constant." Then (a) rewrite the proof to reason about the footprint-relevant state being constant past N rather than "the state is constant"; (b) since regime (i) so defined covers endless-K.α, replace the H-SFAIR distinguishing example with an environment that perturbs the footprint *forever* yet is turn-fair (each recurrently-presented argument eventually fired) — that is the case genuinely outside regime (i); and (c) reconcile "regime (i) for the rule" (the cooperative "leave each argument fireable" reading) with whichever definition you adopt, since that fourth gloss is a cooperation condition, not an idleness one.

### Issue 2: Q3 carries a scope-justifying aside about the *other* half of at-most-once

**ASN-0133, Q3 ("Not effective in general")**: "The companion SF-spelling half of at-most-once is, by contrast, genuinely decidable wherever invoked — PD0's ST/SF rules are syntax-directed, like WT, the very rules ASN-0130's `certify_pd_stable` runs — so it is the extinction half alone this note must scope."

**Problem**: Q3 is about the static checkability of the *extinction* contract. This sentence is about the *SF-spelling* half (a different obligation, established by Q-EXT/PD0), and its payload is a scope declaration — "it is the extinction half alone this note must scope." That is reviser drift: prose explaining *which half the note addresses* rather than advancing Q3's claim, with a tangential pointer to `certify_pd_stable`'s implementation. The reader must skip it to follow Q3.

**Required**: Delete the aside. If the split of labor between the SF half and the extinction half needs stating, it belongs once, at Q-EXT, not inside Q3's effectiveness argument.

### Issue 3: "Worked composition" states the internal/external divergence split three times

**ASN-0133, "Worked composition" (Quiescence/divergence paragraph)**:
1. "This registry cannot diverge *of its own accord* — it has no *internal* divergence route — and the reason is structural: ... the two rules' domains and emissions are *type-isolated*."
2. "Both internal divergence routes — re-arm and producer-domain growth via `ρ_R`'s emissions — are closed here by the registry's own types; what they do not close is the crux's environment-driven growth of `[D_{ρ_P}]`..."
3. "Divergence thus remains reachable — an unboundedly-flagging environment whose flags outrun retraction drives unboundedly many real `ρ_P` fires — just never of the registry's own making."

**Problem**: All three sentences assert the same proposition — internal divergence is closed by type isolation, external divergence (unbounded flagging) remains. This is the same-thing-in-different-words pattern; sentence (2)'s "Both internal divergence routes... closed... what they do not close" and (3)'s "remains reachable... never of the registry's own making" add nothing over (1) plus the already-stated bounded-flagged-population hypothesis.

**Required**: Keep one statement (the type-isolation argument, sentence 1, which carries the actual content) and the single sentence noting external divergence survives; cut the restatements.

### Issue 4: the H-W dismissal digresses into stutter-unavailability

**ASN-0133, W (Work)**: "A literal stutter `Σ →_sh* Σ` is *not* available — every `→_sh` step strictly grows one of `dom(Σ.M)`, `dom(Σ.C)`, `dom(Σ.L)` ... and the one other way to hold the state fixed, a no-op fire, needs an available trigger-*false* `(ρ', x')` (RG), which a non-quiescent state need not offer. The `K.α` tail sidesteps both..."

**Problem**: The point being made — H-W (`|W(σ)| < ∞` for *every* σ) is equivalent to "every reachable state is quiescent," hence useless, hence Q5 uses per-σ `|W(σ)|` — is correct and worth one sentence. The detour establishing *why the K.α tail rather than a stutter* is the construction (no-stutter, no-op-fire-needs-a-trigger-false-argument) is justification a precise reader skips to reach the conclusion.

**Required**: Compress to the core: "H-W is equivalent to every reachable state being quiescent — extend any non-quiescent state by content (K.α) deposits, invisible to every trigger (V-DOC), for an infinite-`W` σ — so the per-σ count, not H-W, is load-bearing."

## OUT_OF_SCOPE

### Topic 1: the turn-fairness condition H-SFAIR's satisfiability requires
The note correctly identifies (and defers to the implementation layer) the joint scheduler/environment turn-fairness under which H-SFAIR's regime form is satisfiable. As a *conditional* result ("H-SFAIR ⟹ reach-and-hold"), the theorem stands without it; constructing the turn-fairness discipline is genuinely a future/protocol concern, not a defect here. (Once Issue 1 is fixed, ensure the discussion of this condition is the *only* place the H-SFAIR-vs-regime-(i) distinction is argued.)

META: (none — the note defines a state predicate, its absorption, and conditional termination guarantees at a level any implementation would have to meet; it has not drifted into implementation mechanics.)

VERDICT: REVISE
