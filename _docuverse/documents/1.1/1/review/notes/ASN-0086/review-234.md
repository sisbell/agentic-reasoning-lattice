# Review of ASN-0086

## REVISE

### Issue 1: Two sections defer to "Worked Sketch Step 4" for the self-emit branch
**ASN-0086, Definition — Nullify** and **WP Case 1**:
- Nullify def: "P1 in particular is not required for the operation to run and nullify its target — Worked Sketch Step 4 invokes Nullify with P1 false (the self-emit branch)."
- WP Case 1: "The disjunct `a = a_emit(Σ, d_retr)` is the *self-emit branch* ... (the case Worked Sketch Step 4 exercises)."

**Problem**: The self-emit branch is established intrinsically at both sites — the Nullify definition already proves it directly ("yet the emitter address `b` coincides with `a`, so `a = b ∈ dom(Σ'.L)`..."), and WP Case 1 derives it from `A_rel^{Σ'} = A_rel^Σ ∪ {e}`. The two forward pointers to a downstream worked example add nothing to the reasoning; they are the "multiple paragraphs in different sections defer to the same downstream location" accretion pattern named in the classifier. A reader following the argument must skip past them.

**Required**: Remove both forward references to Worked Sketch Step 4. The realizability of the self-emit branch (`a = a_emit(Σ, d_retr)`, P1 false) is a property of the definition, not contingent on the example illustrating it.

### Issue 2: R5 proof reuses `d` with two distinct bindings
**ASN-0086, R5 (TupleSelfTargeting) proof**: opening — "taking `d = home(a)` discharges R0's home precondition `d ∈ dom(Σ.M)`"; Step 3 — "Pick any `d ∈ dom(Σ.M)` and any `K ∈ T_admissible`."

**Problem**: The symbol `d` is first bound to `home(a)`, then silently re-bound to "any `d`." The opening's specific binding is used only to establish `dom(Σ.M) ≠ ∅`, after which Step 3 discards it. A precise reader cannot tell whether the self-targeting emission must be homed at `home(a)` or at any document — the prose says both. The actual claim is the latter (any allocated home suffices).

**Required**: State the opening as "`a ∈ A_rel^Σ` with L1a gives `home(a) ∈ dom(Σ.M)`, so `dom(Σ.M) ≠ ∅`" without binding `d`, and let Step 3 introduce `d` once. Or keep `d = home(a)` throughout and drop "pick any d."

## OUT_OF_SCOPE

### Topic 1: Multi-arity typed relations and projections
The note restricts `L_K` to standard triples (`|Σ.L(a)| = 3`) and notes higher-arity links inhabit `A_rel` but index no tuple. The Open Questions correctly defer `L_K^{(n)}` and binary projections of `n`-ary links to future work. Not an error here.

### Topic 2: Concurrency/atomicity of Emit vs Observe
Observe-during-Emit consistency and the `A_K` observation model are raised in Open Questions and belong in a later ASN; the present note's single-authority/sequential-transition framing (ASN-0093 SequentialTransitionAxiom) is sufficient for the claims made.

VERDICT: REVISE
