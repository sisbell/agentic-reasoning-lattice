# Review of ASN-0133

This is a careful note whose explicit thesis is hypothesis-honesty — "every hypothesis named… stated as named hypotheses rather than smuggled." I checked the proofs against that standard. Q0, Q1, Q5, and Q6 hold up (Q5's index-injection bound is clean; Q6's last-real-fire argument is correct under H-RF + H-FAIR). The failures are concentrated in the SF/extinction machinery and the H-W route, and in two of three cases the note's own text supplies the refutation.

## REVISE

### Issue 1: Q5a drops extinction discipline — its bound is false for an all-SF-but-non-falsifying registry

**ASN-0133, Q5a (and its restatements):** "For an all-SF registry (every trigger an SF spelling), the finite-real-fire conclusion follows from bounded domain growth directly… each argument fires each rule at most once (Q-EXT)." Echoed in the commits bullet ("by bounded domain growth **alone** for an all-SF registry"), in Q6 ("under all-SF + bounded domain growth + H-FAIR"), and in Q-FLIP ("at-most-once-per-argument is a registration-time fact about the SF spelling (Q-EXT)").

**Problem**: Q5a's own parenthetical defines "all-SF" as "**every trigger** an SF spelling" — a property of triggers only. But "each argument fires each rule at most once" is **Q-EXT's** conclusion, and Q-EXT has two antecedents, not one: "If `T_ρ` is an SF spelling…, **extinction discipline** strengthens to at-most-once… the **disciplined fire** makes `T_ρ(x, ·)` false, and SF makes false permanent." SF supplies only "false stays false"; it never supplies "true becomes false." That second half is extinction discipline, and it is a separate hypothesis that Q5a's "all-SF" gloss omits.

The omission is not cosmetic — the bound is false without it. Take `R = {ρ}`, `D_ρ = {a}` (a singleton, trivially grow-only and bounded), `T_ρ(a) ≡ ¬(∃ c ∈ L_K :: a ∈ coverage_G(c))` with `L_K` initially empty. `T_ρ` is a negated existential over a grow-only audit slice, hence SF (so all-SF holds), and the domain never grows. Give ρ the weak contract `Post_ρ ≡ ⊤` that Q3 itself names, discharged by the empty emission set. A fire of `(ρ, a)` at the initial state is trigger-true, so by RG it is the "otherwise" branch — a **real fire** (Q6 is explicit: "a trigger-true fire *is* a real fire"), even though `Σ' = Σ`. Nothing was added to `L_K`, so `T_ρ(a)` is still ⊤; fire again; again — unboundedly many real fires on one bounded-domain argument. Q5a's bound `Σ_ρ|⋃_k[D_ρ]| = 1` is violated. Q5 forbids exactly this spin via H-W ("H-W already forbids spinning"); Q5a has no H-W and must forbid it via Q-EXT — which it cannot, because Q-EXT needs the extinction discipline Q5a did not assume.

The worked example tacitly admits this: it establishes extinction *separately* — "Post_P requires an emitted `cmt` covering t… each strong enough (Q3): the emission makes the trigger's existential true, hence the trigger false" — **before** invoking Q-EXT. That is the hypothesis Q5a's statement leaves out.

**Required**: State Q5a's hypothesis as an *extinction-disciplined* all-SF registry (each rule both SF-triggered **and** extinction-disciplined, the latter checkable via Q3). Correct the commits bullet ("bounded domain growth **alone**" is wrong — extinction discipline is also load-bearing), Q6's "all-SF + bounded domain growth + H-FAIR," and Q-FLIP's "a registration-time fact about the SF spelling" (it is a fact about the SF spelling **plus** the Q3 extinction check).

### Issue 2: the worked example's stratification repair is vacuous for the SF producer, and so fails to exclude the very divergence it diagnoses

**ASN-0133, Worked composition:** "Stratification states the repair: ρ_P at stratum 0, ρ_R at stratum 1, legal iff **resolver emissions never re-arm the producer**." The diagnosed divergence one sentence earlier is: "let the resolver's emissions also make fresh targets need attention (… enlarging `⋃_k [D_{ρ_P}]_{Σ_k}`)."

**Problem**: `T_P` is an SF spelling (the note establishes this in the same example), and the note's own falsifier accounting makes SF triggers *immune to re-arming*: "⊥-stability (PD0) makes a falsified SF trigger permanent against every item above, deposits included." So "resolver emissions never re-arm the producer" is satisfied **vacuously** — no emission can ever re-arm an SF trigger — and therefore excludes nothing. In particular it does not exclude the diagnosed divergence, which is not a re-arm at all: a `res` emission lands in `L_res`, which `T_P` (reading `L_cmt`) never consults, so it cannot flip `T_P` on any existing target; it only adds **new** targets to `D_{ρ_P}`. A reader who applies the stated condition literally certifies the divergent registry as "legal." The note is elsewhere scrupulous about precisely this distinction — at-most-once *per argument* (re-arm impossible under SF) versus *new arguments* (domain growth, Q5a) — so importing the general-stratification word "re-arm" here contradicts the note's own usage.

**Required**: State the condition in terms of the diagnosed mechanism: "legal iff resolver emissions never **enlarge the producer's domain** (never make a fresh target need attention)." The general phrasing "no rule's emissions re-arming a strictly lower stratum" is fine for *non-SF* lower strata but must be specialized to domain-growth for the all-SF producer.

### Issue 3: H-W is listed as a route to H-RF, but the note's own starvation argument proves H-W unsatisfiable for any working registry — the worked example included

**ASN-0133, commits bullet / H-RF:** "supplied two ways — by the bounded-work hypothesis (H-W) for any registry (Q5), or by bounded domain growth alone for an all-SF registry (Q5a)"; "Two routes therefore supply H-RF: H-W supplies it for any registry (Q5…)."

**Problem**: H-W is defined over **every** σ — "iff `|W(σ)| < ∞` for every σ from Σ₀ … unfair schedulers included." The note then proves "an unfair scheduler that starves a persistently-true trigger drives `|W(σ)| = ∞` whatever the registry's structure." Because H-W quantifies over those unfair σ, this *is* a proof that **H-W is false** for any registry that can reach a state holding one trigger-true argument alongside one trigger-false in-domain argument: freeze the state by no-op-spamming the false argument forever, and the true argument's triple `(ρ, x, k)` recurs at every step, so `|W(σ)| = ∞`. That is essentially every registry that does concurrent work — including this note's **own worked example**: a single commented-but-still-`needs_attention` target (in-domain, trigger-false) beside one uncommented target (trigger-true) yields the starving σ, so the worked example does *not* satisfy H-W (it terminates via Q5a, not H-W). H-W and Q5a are therefore not co-equal routes — one is vacuous for every working registry. Listing a hypothesis the note has just proven unsatisfiable as "one of two ways to supply H-RF" is precisely the kind of un-named/un-flagged hypothesis the note's thesis disclaims. (This is sharper than "H-W is meta-level," which the note does say: meta-level means *unverifiable*; the starvation argument shows H-W is *false*.)

**Required**: Either (a) define H-W over **fair** σ only — which restores satisfiability (no starvation under fairness, finite if no infinite re-arm) and still suffices for Q6, whose σ is fair by H-FAIR; or (b) demote H-W from "route" to foil: state plainly, as a corollary of the note's own starvation observation, that H-W is unsatisfiable for any registry with concurrent pending/completed work, so Q5a (or directly assuming H-RF) is the only structural route, with H-W serving solely to locate H-RF as the strictly weaker, attainable hypothesis.

## OUT_OF_SCOPE

### Topic 1: Discharging the meta-level hypotheses (`pd_extinct` certificate, a PL surrogate for H-W, bounded-domain-growth checking)
**Why out of scope**: The note correctly names these as un-discharged (H-W and bounded domain growth are reachability-quantified; the SF certificate is deferred to a designated-class question) and routes them to its own Open Questions 1–2. Building the SF/`pd_extinct` certificate and a runtime divergence detector is genuinely new territory, not a defect here.

### Topic 2: A scheduler discharging H-FAIR, and cross-scope oscillation bounds (Q8 re-entry)
**Why out of scope**: H-FAIR is explicitly stated-not-constructed, and bounding re-entry across scopes is flagged as Open Question 4 for a future cascade/re-opening theory. Deferring both is the right call.

VERDICT: REVISE
