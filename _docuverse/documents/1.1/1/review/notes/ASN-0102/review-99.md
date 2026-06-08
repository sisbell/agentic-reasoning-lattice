# Review of ASN-0102

## REVISE

### Issue 1: P4a discharge mischaracterizes the witnessing trace

**ASN-0102, X17 (P4a TraceWitnessing)**: "Read the standalone COPY as the trace `Σ_0 →* Σ'`, whose trace states are `{Σ_0, Σ'}`. A pair already in `R_{Σ_0}` is witnessed by `Σ_0`'s own P4a — its witnessing trace state lies in the history up to `Σ_0`, a prefix of this trace."

**Problem**: The two sentences are mutually inconsistent. P4a (ASN-0047) requires the witnessing state `Σ_k` to lie **among the trace's own states**. If the trace is declared to be the two-element `{Σ_0, Σ'}`, then a pair `(a,d) ∈ R_Σ` recorded long ago — and possibly contracted out of `d`'s content range by an intervening K.μ⁻ before `Σ` — is resident at *neither* `Σ_0` nor `Σ'`, so the two-element trace fails to witness it. The escape hatch "its witnessing trace state lies in the history up to `Σ_0`, a prefix of this trace" is false: a trace that *starts* at `Σ_0` does not contain states preceding `Σ_0`, so the history up to `Σ_0` is not a prefix of it. The argument silently sources a witness from outside the set it just defined.

**Required**: Discharge P4a by preservation, not by a two-state trace. Use P4a at `Σ` as the inductive hypothesis (it holds because `Σ` is a composite boundary); observe that any valid trace to `Σ'` factors as (a valid trace reaching `Σ`) followed by this COPY composite, so its trace states are `{Σ₀^init, …, Σ, Σ'}`; old pairs are then witnessed *within the reaching prefix* (which genuinely is part of this full trace) and the COPY-recorded pairs (X14, RR) are witnessed at `Σ'`. The phrase "whose trace states are `{Σ_0, Σ'}`" must be removed — it is the source of the slip.

### Issue 2: X14 / X17 state the unconditional-write fact twice, and X14 carries coupling-discharge prose belonging to X17

**ASN-0102, X14**: "At the instant COPY acts it thus both records `(a, d)` and makes `a` content-subspace-resident. COPY's only coupling-relevant contribution is (SL); J0 is vacuous by X1 (no allocation)."
**ASN-0102, X17**: "COPY's provenance write is *unconditional*: it records `(a, d)` for every `a ∈ A`, whether or not `a` was already content-subspace-range-resident in `d`."

**Problem**: X14's job is ContainmentRecording; X17's job is the coupling/invariant discharge. X14 first states (SL) cleanly, then re-states it in different words ("At the instant COPY acts it thus both records…"), then previews X17's coupling argument ("COPY's only coupling-relevant contribution is (SL); J0 is vacuous"). X17 then re-states (SL) a third time as "unconditional." This is forward-reference scaffolding parked in the carrier of a different claim, plus same-fact-twice duplication — exactly the accretion pattern.

**Required**: State (SL) once in X14 as the named fact, drop X14's self-restating sentence and the J0/"only coupling-relevant contribution" preview (those belong solely to X17's coupling discharge), and have X17 cite (SL) rather than re-assert it.

### Issue 3: The resolution preamble pre-stages X8's per-reference run analysis

**ASN-0102, "The source designation and its resolution"**: "each `k_i` is the maximal-run count of reference `r_i` taken in isolation (C1a, M12 applied per reference): each `k_i` counts the blocks of `r_i` that are maximal under M7's joint V- and I-adjacency merge condition *within that reference*."

**Problem**: Defining `k = (+ i : k_i)` is legitimate setup, but the elaboration of *what `k_i` counts* (maximality under M7 within a reference) is the substance of X8 (RunFragmentation), which re-derives it ("Within a single reference, no two blocks coalesce… Maximal-merge then forbids any source-V-adjacent pair from also being I-adjacent"). The preamble enumerates downstream machinery before the claim that carries it.

**Required**: Keep the notation `k = (+ i : k_i)` in the preamble; move the M7-maximality characterization of `k_i` into X8, where the within-reference no-coalescence argument lives.

## OUT_OF_SCOPE

### Topic 1: The four Open Questions (later displacement and discoverability, transitive containment, time-varying views, identity after the allocating document is unreachable)
**Why out of scope**: Each concerns operations or reachability conditions beyond a single COPY transition; they are correctly posed as future-ASN questions, not gaps in this note.

VERDICT: REVISE
