# Review of ASN-0099

## REVISE

### Issue 1: Unconsumed parametric-conformance apparatus and dual-surface factoring
**ASN-0099, "Completeness"**: "The same conjunction-forces-equality contract transfers parametrically to every operation form, each with its own `result_*` function functional in its arguments and pinned to the corresponding abstract specification" … "When an implementation exposes both the V-side surface … and the I-side surface …, the factoring equation `result_V(R, d, Σ) = result(image(R, d, Σ), Σ)` follows by F2 ∧ F3 + F2★ ∧ F3★ (V form) + F12".

**Problem**: F2 ∧ F3 (the completeness/soundness obligation pinning `result = findlinks`) is the load-bearing conformance content. F2★ ∧ F3★ generalizes it to `result_filtered`, `result_scoped`, `result_V`, and then the dual-surface paragraph posits an implementation exposing two coordinated surfaces and proves they cohere. Nothing in the ASN consumes F2★ ∧ F3★ or the dual-surface equation — no theorem, no worked example (the examples exercise F1, F6, F9, F9-λ, F11, F12, F19). This is a derived guarantee stated without a consumer, plus speculative apparatus designed for a hypothetical multi-surface implementation architecture — accretion, not a system guarantee the spec needs.

**Required**: Reduce to a single line stating that each defined form carries the analogous F2 ∧ F3 obligation. Drop the `result_*` parametric block and the dual-surface factoring derivation unless a downstream obligation actually depends on them.

### Issue 2: Defensive parenthetical that does not advance the argument
**ASN-0099, "Completeness"**: "where `𝒮` is the Xanadu system state space (states of the form `Σ = (C, L, M, E, R, …)` from ASN-0036, ASN-0043, ASN-0047, ASN-0093; by SequentialTransitionAxiom of ASN-0093 each transition is atomic, so `Σ` is a well-defined single state at every query point)".

**Problem**: The clause "by SequentialTransitionAxiom … so `Σ` is a well-defined single state at every query point" justifies why a state symbol is well-formed — a defensive aside the precise reader must read past. The conformance statements F2/F3 are evaluated at a fixed `Σ`; nothing in them is at risk from non-atomicity, so the justification answers a question the surrounding claims never raise. This is the anti-bloat "explains why rather than what / imagines a concern the claim does not need" pattern.

**Required**: Cut the parenthetical down to naming `𝒮` as the state space; drop the atomicity justification.

## OUT_OF_SCOPE

### Topic 1: Bound on K.λ-to-visibility latency
The second Open Question ("Should the abstract specification require any bound on the time between K.λ commitment and the link's appearance in subsequent FINDLINKS results") is a future-ASN concern about timing/index semantics, correctly parked rather than answered here.

VERDICT: REVISE
