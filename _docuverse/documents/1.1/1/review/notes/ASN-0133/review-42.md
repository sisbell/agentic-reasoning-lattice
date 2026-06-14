# Review of ASN-0133

This is a mature note and the core technical content holds up under scrutiny. I traced Q0's view-rebuild against every view-sensitive atom (the four PC3-parameterized atoms plus the six UV-rewritten collections, with `chain` reduced through `elems`/`is_in_chain`) and it is genuinely exhaustive; Q5's index-injection argument is correct and correctly notes extinction is unneeded; Q5a's at-most-once bound and the Q6 case split (1)/(2)/(3) over non-grow-only domains, including the H-SFAIR regime-form closure of case (3), all check out. The two findings below are a precision overstatement and accreted meta-prose around an axiom.

## REVISE

### Issue 1: "cannot in fact diverge" overstates a result the same paragraph makes hypothesis-conditional

**ASN-0133, Worked composition (Bound / Quiescence discussion)**: "so the registry's real fires are finite, its *work* terminates, *if* that flagged population … is bounded — a *sufficient* condition … the registry's one honest hypothesis on its environment." … "This registry cannot in fact diverge, and the reason is structural: … Both divergence routes — re-arm and producer-domain growth — are closed here by the registry's own types."

**Problem**: These two claims are in tension, and the second is overstated. Work-termination is established only under the bounded-input hypothesis the note itself names as "the registry's one honest hypothesis on its environment" — and the note even confirms divergence is reachable, since an environment that flags unboundedly many targets while the scheduler fires each before retraction produces unboundedly many real `ρ_P` fires. So "cannot in fact diverge" (unqualified) is false. The structural argument supports only "no *internal* divergence amplification." Worse, "producer-domain growth … closed here by the registry's own types" is accurate only for the *internal*, `ρ_R`-mediated route: `[D_{ρ_P}] = {t ∈ M_tgt : is_attn(t)}` grows precisely by *environment* deposits of `tgt`/`attn`, which the types do not close — that growth *is* the unbounded route the hypothesis must exclude. Listing "producer-domain growth" as a closed route reads as discharging the very hypothesis the note insists is real, undercutting the note's own open-model honesty thesis.

**Required**: Qualify the conclusion to what is proved — e.g. "This registry has no *internal* divergence route" / "cannot diverge of its own accord." Make explicit that "producer-domain growth is closed" means closed against `ρ_R`'s emissions only, with environment-driven growth of `[D_{ρ_P}]` remaining as exactly the bounded-input hypothesis stated one sentence earlier.

### Issue 2: H-FAIR's definition is padded with a forward-pointer and a twice-stated principle (anti-bloat)

**ASN-0133, H-FAIR**: the axiom's actual content (per-occurrence discharge by real-fire / removal / in-domain falsification) is interleaved with meta-prose:
- Forward pointer: "Q6 reads the discharge at this strength." — tells the reader a downstream consumer; advances nothing in the definition of H-FAIR.
- The principle "the scheduler controls only its fires, not the environment" is stated twice within H-FAIR: once mid-definition ("a scheduler controls only its *fires*, so it cannot prevent the environment from falsifying x first") and again at the close ("Fairness binds only the registry's scheduling of its fires; it places no obligation on the environment, which may create, remove, and falsify trigger-true arguments as it likes") — then echoed a third time at H-SFAIR ("Like H-FAIR, it constrains only the *registry's* scheduling, not the environment").
- Why-the-clause-is-needed rationale: "Without this escape, no scheduler could meet H-FAIR against an environment that falsifies a trigger the scheduler did not itself fire" restates the necessity already conveyed by the preceding "cannot prevent the environment from falsifying x first."

**Problem**: This is the forward-reference/rationale accretion the `review-mode.anti-bloat` classifier targets. A reader extracting "what is H-FAIR" must skip past a Q6 forward-pointer, a thrice-stated registry-vs-environment principle, and a why-needed restatement. (The scheduler-discipline list "round-robin, queue-fair, priority with aging" is a concrete example and should stay.)

**Required**: State the registry-not-environment principle once (the H-SFAIR "Like H-FAIR" reminder may stay as it is explicitly a back-reference); drop the "Q6 reads the discharge at this strength" forward-pointer and the redundant "Without this escape…" restatement, keeping the single definitional sentence that introduces in-domain falsification as the third discharge.

## OUT_OF_SCOPE

### Topic 1: Atomicity mechanism for multi-step fires
The note cites "atomic by H-ATOM via I4" for single-step fires in the worked example. H-ATOM is the multi-step atomicity hypothesis and is vacuous for a single `→_sh` step; how a genuinely multi-step fire is serialized against environment interleaving is correctly deferred to the scheduler ("What this note doesn't cover"). No action needed here — flagging only that the single-step citation is decorative, not load-bearing.

### Topic 2: SF certification, PL surrogate for H-W, cross-scope oscillation bound
**Why out of scope**: These are correctly carried as the note's own Open Questions 1, 2, and 4. They are new territory (a `pd_extinct` certificate class, a per-state divergence-warning predicate, a cascade/re-opening theory), not defects in this ASN.

VERDICT: REVISE
