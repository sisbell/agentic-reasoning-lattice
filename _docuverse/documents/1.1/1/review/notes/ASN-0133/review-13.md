# Review of ASN-0133

This is a careful, self-aware note. The core termination story — Q-EXT (at-most-once from SF + extinction), Q5a (bounded-domain-growth ⟹ H-RF), Q6 (registry-inert past N, grow-only reaches-and-holds, non-grow-only defers to regime (i) / H-SFAIR) — checks out, and the Q-FLIP falsifier accounting, the idem=⊤ dedup-vs-audit argument in Q3, and the closed/open collapse are all correct as written. The two issues below are both localized to H-SFAIR, the recently-revised hypothesis.

## REVISE

### Issue 1: H-SFAIR's satisfiability is asserted as environment-robust ("Like H-FAIR"), but it is not

**ASN-0133, H-SFAIR (StrongFairnessHypothesis)**: "Like H-FAIR it binds only the registry's scheduling — the environment may still present, withdraw, and falsify arguments at will — and is satisfiable by standard disciplines (priority with aging across recurrences)."

**Problem**: The "Like H-FAIR" parallel is false in exactly the dimension that matters. The note correctly explains *why* H-FAIR is satisfiable against an arbitrary environment: its removal/falsification escapes "absorb… exactly the environmental interference a fire-only scheduler cannot forestall." H-SFAIR deliberately *removes* the removal escape for infinitely-recurring arguments (it demands GF-taken — real-firing). That removal makes its satisfiability environment-conditional in a way H-FAIR's is not.

Concretely, take case (3)'s own mechanism to the limit. The interleaving model admits consecutive environment steps (σ is "an interleaving" of fires and arbitrary non-registry `→_sh` transitions, with no stated turn-fairness). So an admissible environment can, around each scheduler turn, *add* `xᵢ` then *remove* it:

```
Σ₀ (xᵢ absent) →env add→ Σ₁ (xᵢ trigger-true) →env remove→ Σ₂ (absent) →sched (pre-state Σ₂: can't fire xᵢ)→ Σ₃ →env add→ Σ₄ (trigger-true) → …
```

`xᵢ` is trigger-true at `Σ₁, Σ₄, …` (infinitely-recurring) yet absent at every scheduler pre-state, so *no* discipline — priority-with-aging included, since aging only orders *in-domain* arguments — ever real-fires it. Then no σ in this environment satisfies H-SFAIR, so it is **unsatisfiable by any scheduler here**, not merely undischarged by a standard one. "Satisfiable by standard disciplines… environment at will" is therefore wrong: H-SFAIR's satisfiability presupposes an interleaving/serialization fairness (the scheduler eventually gets to fire each recurrently-presented argument) that the note neither states nor derives.

This also undercuts the framing of H-SFAIR as an *independent* alternative to regime (i). Q6 offers "the environment eventually leaves each argument in-domain and trigger-true until fired (regime (i) for the rule), **or** strong fairness (H-SFAIR)." But because an all-SF fired argument settles permanently, H-SFAIR-satisfiability *requires* the environment to eventually leave each recurring argument in-domain-trigger-true at some scheduler turn — essentially the per-rule regime (i) condition. The "or" is closer to a restatement than a genuine second route.

**Required**: Drop or qualify the "Like H-FAIR" satisfiability parallel. State that H-SFAIR, lacking H-FAIR's removal escape, is satisfiable only under an interleaving/turn-fairness in which the scheduler can eventually fire any persistently- or recurrently-presented argument — a condition an admissible withdraw-before-every-fire environment violates — and reconcile this with the per-rule regime (i) it nearly coincides with. (The full turn/serialization model is properly deferred to the scheduler layer; only the unqualified satisfiability *claim* must be repaired here.)

### Issue 2: "H-SFAIR ⟹ H-FAIR" is stated unconditionally but holds only for infinite σ

**ASN-0133, H-SFAIR**: "It is genuinely stronger — `H-SFAIR ⟹ H-FAIR` (the per-occurrence H-FAIR above)… an argument trigger-true only *finitely* often is, past its last true index `K_last`, permanently not-trigger-true, so each of its finitely many occurrences (all `≤ K_last`) is discharged by the removal-or-falsification holding at every index past `K_last`".

**Problem**: The finitely-recurring case discharges each occurrence using "the removal-or-falsification holding at every index past `K_last`" — which requires σ to *have* an index past `K_last`. For an infinite σ this is fine. But the note itself admits finite σ and gives them teeth: "a fair finite sequence cannot end at a non-quiescent state." Consider a finite σ whose final state is trigger-true for some `(ρ, x)` (so `K_last` = the final index). That occurrence has no later index, so H-FAIR fails — yet H-SFAIR holds **vacuously**, since no argument is trigger-true at infinitely many indices in a finite sequence. Hence H-SFAIR ⊉ H-FAIR precisely on the finite-σ case the note's own finite-σ argument relies on. The proof's `K_last + 1` step tacitly assumes infinite σ.

**Required**: Scope the implication to infinite σ, or state that finite σ are governed by H-FAIR's separate end-of-sequence obligation and are not within H-SFAIR's (vacuous) reach. Since H-SFAIR is "invoked in exactly one role" on infinite oscillating sequences, scoping the claim costs nothing downstream.

## OUT_OF_SCOPE

### Topic 1: A formal interleaving / turn-fairness model
**Why out of scope**: Pinning down who orders fires against environment steps — and the turn-fairness under which H-SFAIR becomes achievable — is scheduler/serialization machinery the note rightly defers ("What this note doesn't cover: A scheduler"). It is the missing piece behind Issue 1, but constructing it belongs to a future scheduler ASN; Issue 1 only asks that the satisfiability *claim* not outrun what this layer establishes.

### Topic 2: pd_extinct (SF certification) as a designated class
**Why out of scope**: Open Question 1 already identifies this as the natural next class (the SF half being the load-bearing *uncertified* check). It is correctly posed as future catalog growth, not a gap in this note.

VERDICT: REVISE
