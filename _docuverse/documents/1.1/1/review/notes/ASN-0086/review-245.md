# Review of ASN-0086

I checked the six properties (R0–R6), the three operations, the wp analysis, and the worked sketch against the foundation contracts. The technical core is sound: R0a's two-case antichain argument, R-Scope's P1/self-emit split, CoverageEqualityDecidable's cell partition, and both wp derivations all hold up, and the worked sketch correctly exercises the first-emission branch (Step 0), retraction (Step 1), R6c restoration (Step 2), R6b non-fixpoint (Step 3), and the wp Case 2 false branch (Step 4). I found no correctness gap, no missing invariant conjunct, and no non-foundation cross-ASN reference.

The note carries the anti-bloat classifier. The findings below are at-source meta-prose accretions — restatements the reader must skip past to follow the argument.

## REVISE

### Issue 1: Emit_K restates R0's Value-shape consequence
**ASN-0086, Definition — Emit_K**: "Emit_K specializes to N = 3 and e₃ = K, which discharges K.λ's L3 precondition (R0's Value-shape consequence) — so K.λ's contract carries over with no separate value requirement on the caller."

**Problem**: This is the same discharge already stated verbatim in R0's *Value-shape consequence* ("The standard triple `(F, G, K)` discharges K.λ's L3 precondition directly from R0's typed hypotheses ... so the caller discharges no separate value requirement"). The Emit_K paragraph re-derives it (N=3, e₃=K, L3) and then defers to the very note it is restating. The "Emit_K is operationally K.λ ... restricted to the standard-triple link value" half is a genuine statement of what the operation is and should stay; the L3 re-derivation is duplication.

**Required**: Drop the L3 re-derivation, keeping only the operational identification ("Emit_K is K.λ specialized to value `(F, G, K)`") and the parenthetical pointer to R0.

### Issue 2: R5 proof restates its own home-precondition discharge
**ASN-0086, R5 proof, opening paragraph**: "(Equivalently, "may appear in the from-set or to-set of an emitted tuple" presupposes a state with at least one document allocated, which `a ∈ A_rel^Σ` itself supplies.)"

**Problem**: The preceding two sentences already establish exactly this — "`home(a) ∈ dom(Σ.M)`, so `dom(Σ.M) ≠ ∅` — R0's home precondition can be discharged." The parenthetical says the same thing in different words within the same paragraph.

**Required**: Delete the parenthetical.

### Issue 3: Worked Sketch T4-validity note carries defensive elaboration
**ASN-0086, Worked Sketch / Setup**: "*T4-validity note.* Type-endset ghost addresses (per L9 ...) need not satisfy T4 ... We choose single-component tumblers here to keep the worked sketch's ghosts T4-valid by inspection, but deeper non-T4 tumblers (e.g., `3.0.0.0.1`) would also be admissible."

**Problem**: The clause justifying the example choice ("single-component tumblers ... T4-valid by inspection") is fine as explanatory prose, but the trailing "deeper non-T4 tumblers would also be admissible" is a defensive elaboration about cases the sketch deliberately does not use — it advances no claim in the example and only rehearses L9's permission already cited.

**Required**: Trim to the choice itself ("we use single-component ghost addresses for legibility"); drop the non-T4-admissibility aside.

## OUT_OF_SCOPE

### Topic 1: higher-arity link projections into typed relations
The note restricts `L_K` to standard triples (`|Σ.L(a)| = 3`) and leaves higher-arity links unindexed. The relational treatment of `|Σ.L(a)| > 3` is correctly deferred to Open Question 2, not an error here.

VERDICT: REVISE
