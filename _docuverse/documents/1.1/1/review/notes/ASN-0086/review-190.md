# Review of ASN-0086

## REVISE

### Issue 1: CoverageEqualityDecidable — gap-nonemptiness discharge is invalid for tight successor gaps

**ASN-0086, Lemma CoverageEqualityDecidable**: "We discharge non-emptiness: for every consecutive pair `c_k < c_{k+1}`, the zero-extension `c_k.0` witnesses `c_k < c_k.0 < c_{k+1}`. ... or a zero component, so `c_k.0 ≼ c_{k+1}` with `c_k.0 ≠ c_{k+1}` (the endpoints are distinct), giving `c_k.0 < c_{k+1}` by case (ii)."

**Problem**: The step "`c_k.0 ≠ c_{k+1}` (the endpoints are distinct)" is a non-sequitur. Endpoint distinctness gives `c_k ≠ c_{k+1}`, **not** `c_k.0 ≠ c_{k+1}`. The zero-extension `c_k.0` is the *immediate T1-successor* of `c_k` (ASN-0034 TA5 note: "The true immediate successor in the total order is `t.0` — the zero-extension"). Therefore the gap `(c_k, c_{k+1})` is empty **exactly when** `c_{k+1} = c_k.0`, and in that case `c_k.0 = c_{k+1} ∉ (c_k, c_{k+1})` — the proposed witness lies on the boundary, not the interior.

Such pairs are reachable. Take `e = {([1],[1])}` (endpoints `[1]`, `[2]`) and a second span starting at `[2,0]` (endpoints `[2,0]`, `[2,1]`). Sorted: `[1] < [2] < [2,0] < [2,1]`. The consecutive pair `[2], [2,0]` has `[2,0] = [2].0`, so its gap is empty.

This is precisely the soundness hazard the proof itself names ("were some gap empty, both coverages would restrict to `∅` there regardless, yet their boolean gap-indicators could differ, falsely reporting equal coverage sets as unequal"). The discharge meant to exclude that hazard does not exclude it: the algorithm compares indicator vectors over *all* cells including empty gaps, where equal-coverage endsets may yield differing arithmetic indicators (`s ≤ c_k ∧ c_{k+1} ≤ s ⊕ ℓ` is a constraint on endpoints, not on actual membership of a now-vacuous interval), producing a false "unequal."

**Required**: Identify the empty gaps explicitly — `(c_k, c_{k+1})` is empty iff `c_{k+1} = c_k.0` — and exclude them from the indicator comparison (an empty cell contributes `∅` to both coverages and must not be compared), or otherwise prove the gap-covering test agrees on empty gaps for equal-coverage endsets. The current "every gap contains `c_k.0`" claim is false.

### Issue 2: Nullify's execution precondition is overstated; the wp Case 1 parenthetical mislabels a P0-satisfied failure as "dropping P0"

**ASN-0086, Definition — Nullify**: "Nullify has a single *execution precondition* — **P0**: `d_retr ∈ dom(Σ.M)` ... Whenever P0 holds, Nullify executes and produces a post-state Σ'." And **wp Case 1**: "(Without such a `d_retr`, e.g. if `dom(Σ.M) = {d}`, the off-chain `inc(ℓ_prev, 0)` at `d`'s nested frontier leaves `Emit_R` undefined and no Σ' is produced — the 'dropping P0' mode rather than a postcondition failure.)"

**Problem**: These contradict each other. By Definition — Emit_K, `Emit_K(Σ, d, ·)` "can be undefined because the chain frontier may be ill-formed" even when `d ∈ dom(Σ.M)`. Since `Nullify ≡ Emit_R(Σ, d_retr, ∅, …)`, Nullify inherits this partiality: over the state-local-conforming domain (which the note explicitly invokes for the wp analysis), `d_retr ∈ dom(Σ.M)` does **not** guarantee execution — `d_retr`'s own link frontier must also be well-formed. In the cited parenthetical, `dom(Σ.M) = {d}` and the retraction is attempted at `d_retr = d`, so P0 (`d ∈ dom(Σ.M)`) **holds**, yet no Σ' is produced. Calling this "the 'dropping P0' mode" is wrong — P0 is satisfied. The case demonstrates that P0 is not the sole execution gate, directly refuting "Whenever P0 holds, Nullify executes."

**Required**: Either restrict Nullify's domain to substrate-conforming Σ (where every home's frontier is well-formed, so P0 does suffice), or add the missing execution condition — `d_retr`'s homed-set is a contiguous chain prefix (well-formed frontier) — to the execution gate. Correct the wp Case 1 parenthetical: this is a P0-satisfied non-execution, not a "dropping P0" case.

### Issue 3: Forward-reference ordering justification (anti-bloat)

**ASN-0086, The Active Subset (closing sentence)**: "R6d (RetractionStabilityUnderConformingLayer) lifts R6a and R6c from `→`/`→*` to the `↝`-steps of a substrate-conforming layer; it is stated after its dependencies R7a and *Definition — substrate-conforming layer* (Three Operations)."

**Problem**: This sentence justifies *document ordering* ("it is stated after its dependencies …") rather than advancing any claim — one of the explicitly flagged accretion patterns. R6d's actual statement and dependency list already appear at its definition site; the placement rationale is meta-prose the reader must skip. R6d's own opening ("R6a and R6c are proved against `→` and `→*` … but the substrate's operational evolution is `↝`") repeats the same framing a second time.

**Required**: Delete the placement-justification clause; let R6d stand at its site with its dependency citations. Collapse R6d's opening framing into the lemma statement.

## OUT_OF_SCOPE

### Topic 1: Concurrency/atomicity model for Observe vs. Emit
The interaction of `Observe_K` reads with concurrent `Emit_K` transitions, and the consistency model under which `A_K` transitions are observed, is genuinely new territory (already listed in Open Questions). It is not an error in this note, which fixes a sequential, atomic transition model (ASN-0093 SequentialTransitionAxiom).

META: not applicable — the note defines state-derived sets, operations, and invariants abstractly (active/audit distinction, retraction semantics), squarely within specification territory.

VERDICT: REVISE
