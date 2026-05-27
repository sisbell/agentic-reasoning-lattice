# Review of ASN-0076

## REVISE

### Issue 1: Notational collision around `Σ_0` in E5's proof

**ASN-0076, E5 (DivergentSuccessors) proof**: The base case states "`Σ_0 = Σ` realizes the required structure with the empty set of supersession links" — using `Σ_0` as the induction-indexed state at k=0. The next paragraph then writes "Since `Σ` is reachable from `Σ_0`, `Σ_{k-1}` is itself reachable from `Σ_0` — the concatenation of the path `Σ_0 →* Σ` with the `k-1` EDITLINK composites is a finite sequence of valid composite transitions" — here `Σ_0` denotes the system's initial state from ASN-0047 (`Σ₀ = (C₀, L₀, E₀, M₀, R₀)`).

**Problem**: The same symbol `Σ_0` is used within consecutive paragraphs for two different states: (a) the induction-indexed state at k=0 (equal to `Σ`), and (b) the system's initial state from which `Σ` is reachable. A reader following the proof must silently disambiguate which `Σ_0` is meant at each occurrence.

**Required**: Use distinct notation. Either rename the system's initial state in the inductive step (e.g., `Σ_init`, or just write "the system's initial state"), or index the induction sequence starting from 1 (so the induction-indexed states are `Σ_1, ..., Σ_k` and `Σ` itself is not relabeled).

### Issue 2: Worked example does not verify E0's induction base for arity-2 element field

**ASN-0076, Worked Example, E0 verification**: The verification cites SubAllocatorAxiom.FirstEmission for the first emission and TA5(c)+TA5(b)+TA5-SigValid+T0 for subsequent emissions, but the example itself only exercises the first-emission rule (Bob's `A_L(d_bob)` has emitted no prior links at `Σ`, so Step 1 hits sub-case (a)). The non-trivial chain — `#E(ℓ_sup) ≥ 2` inherited from `#E(ℓ_new) = 2` through `inc(·, 0)` — is exercised at Step 2 but the example does not name the four-fact discharge (TA5(c), TA5(b), TA5-SigValid, T4 field-segment) explicitly at the calculation step. The reader who checks `ℓ_sup = [4.0.2.0.3.0.2.2]` against the formal discharge has to reconstruct the entire chain.

**Problem**: A concrete example should verify the non-trivial postconditions against the calculation. The element-field depth bound `#E(ℓ_sup) = 2` is asserted but the structural reason (sig at terminal, modification doesn't cross a zero, field decomposition preserved) is not exhibited at this concrete value.

**Required**: Add one or two sentences at the `ℓ_sup` calculation step naming the key facts: `sig(ℓ_new) = #ℓ_new = 8` (T4-valid + TA5-SigValid), so `inc(ℓ_new, 0)` modifies position 8 only; `ℓ_new[8] = 1 ≠ 0`, so `ℓ_sup[8] = 2 ≠ 0`; `zeros(ℓ_sup) = zeros(ℓ_new) = 3`; the third zero remains at position 6; `#E(ℓ_sup) = 8 - 6 = 2`. The current trace asserts `ℓ_sup = [4.0.2.0.3.0.2.2]` and moves on.

### Issue 3: E4's "no further atomic transitions intervene" argument under-discharges the cited axiom

**ASN-0076, E4 (SupersessionLink) proof**: "EDITLINK's composite consists of exactly two K.λ steps and no further atomic transitions intervene (by SequentialTransitionAxiom, ASN-0047, together with the composite definition), so `Σ' = Σ_2`..."

**Problem**: SequentialTransitionAxiom only asserts that transitions are atomic and totally ordered; it does not assert that named composites consist of adjacent transitions. The adjacency is supplied entirely by the composite definition (which uses "Step 1; Step 2" notation and is reinforced by the paragraph at the end of E0: "If the user wishes to allocate further links under `d_new` between the successor and supersession steps, those allocations belong to a different composite, not to this one"). The citation to SequentialTransitionAxiom is doing no real work here — only the composite definition is.

**Required**: Either drop the SequentialTransitionAxiom citation in E4 (since it isn't load-bearing — only the composite definition establishes adjacency), or strengthen the composite definition to state the adjacency requirement explicitly (e.g., "Step 2 fires immediately after Step 1 with no atomic transition between them") so that the E4 argument has something formal to cite beyond the informal note at the end of E0.

## OUT_OF_SCOPE

No additions beyond what the ASN's Open Questions already enumerate (supersession cycles, retraction semantics, multi-link supersession, discovery operation interaction, authorization model for `d_new` selection, τ_sup recognition convention, edit propagation through content). The Open Questions cover the natural deferrals well.

VERDICT: REVISE
