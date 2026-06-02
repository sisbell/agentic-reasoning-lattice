# Review of ASN-0086

## REVISE

### Issue 1: The Nullify *definition* slot contains a full two-branch correctness proof, duplicated in wp Case 1
**ASN-0086, Definition — Nullify**: "P1 in particular is not required for the operation to run and nullify its target — the self-emit branch (`a = a_emit(Σ, d_retr)`) runs Nullify with P1 false, as established directly below." … "On the self-emit path … P1 fails, yet the emitter address `b` coincides with `a`, so `a = b ∈ dom(Σ'.L) = A_rel^{Σ'}` directly; `coverage({(a, δ(1, #a))}) ∋ a` then gives `a ∈ nullified(Σ')` by Definition of `nullified`, with R6a again carrying it forward."

**Problem**: A Definition slot should state the operation, its precondition (P0), and its effect. Here it instead carries a multi-branch correctness argument (the P1 path *and* the self-emit path), proving `a ∈ nullified(Σ')` inline. That same self-emit nullification argument is then re-proved in **wp Case 1 → Self-emit branch** ("The internal `Emit_R` deposits `(∅, {(a, δ(1, #a))}, R)` at `e = a`, so `a ∈ A_rel^{Σ'}`; R0a's antichain at Σ' then gives … even though `a ∉ A_rel^Σ` and P1 is false"). The reader must wade through a proof to extract the one-line operation `Nullify ≡ Emit_R(Σ, d_retr, ∅, {(a, δ(1, #a))})`. This is essay/proof content in a structural slot.

**Required**: Reduce Definition — Nullify to the operation, its P0 precondition, and effect. Keep the P0/P1/PC labels (the wp analysis references them by name), but move the self-emit-branch correctness argument out of the definition body — R-Scope and wp Case 1 already own it. State the nullification effect by citing those results, not by re-deriving both branches in situ.

### Issue 2: Forward-deferral accretion around emission/home machinery
**ASN-0086, R5 proof**: "The self-targeting emission may be homed at *any* allocated document, not only at `home(a)`; Step 3 introduces the home `d` accordingly."
**ASN-0086, Definition — Nullify**: "as established directly below."
**ASN-0086, R0, Value-shape consequence**: the "L3-conformance check" is established once, then re-cited as a deferral target at R5 Step 3, R5 Step 4, Definition — Emit_K, and Definition — Nullify.

**Problem**: These are the flagged forward-reference patterns — prose that narrates document ordering ("Step 3 introduces the home `d` accordingly," "as established directly below") and a single sub-result that multiple later sites defer back to. The narration advances no reasoning; it tells the reader where the argument was parked. Per the anti-bloat note, these compound across cycles.

**Required**: Drop the document-ordering narration ("Step 3 introduces the home `d` accordingly," "as established directly below"). Where the L3-conformance check is reused, cite it by name once per use without re-explaining what it discharges.

## OUT_OF_SCOPE

### Topic 1: Cardinality / structural bound on `nullified(Σ)` relative to `dom(Σ.L)`
The Open Questions already raise whether unbounded retraction is permitted. This is genuinely future territory — the present note's invariants neither bound nor need to bound the retraction ratio — so it correctly sits as an open question, not a gap in this ASN.

### Topic 2: Atomicity of Emit relative to concurrent Observe
The `A_K` non-monotonicity consequence flags that observation views must treat `A_K` evolution as non-monotone, but the consistency model under concurrency is left to a future layer. Appropriately deferred.

VERDICT: REVISE
