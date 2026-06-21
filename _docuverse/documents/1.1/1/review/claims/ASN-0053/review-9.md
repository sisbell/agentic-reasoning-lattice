## Audit

I trace each claim in dependency order: S0, WF, S6, S2, S11.

**S0 (Convexity).** The proof reduces to two applications of mixed-order transitivity: `start(σ) ≤ p ≤ q` yields `start(σ) ≤ q`, and `q ≤ r < reach(σ)` yields `q < reach(σ)`, both licensed by T1's `≤`-abbreviation and `<`-transitivity. Sound.

**WF (WellFormedSpanFromEndpoints).** The critical precondition chain for D1 is the elimination of T1 case (ii) via `#s = #r`: case (ii) would give `#s + 1 ≤ #s`, impossible by strict-successor; T1 case (i) then identifies `k = divergence(s, r) ≤ #s`, discharging D1's fifth precondition. TumblerSub's padded projections collapse to native components under `#r = #s`, so `Pos(r ⊖ s)`, `actionPoint(r ⊖ s) = j ≤ #(r ⊖ s) = #s`, and level-uniformity `#width(γ) = max(#r, #s) = #s = #start(γ)` all follow cleanly. Sound.

**S6 (LevelConstraint).** Single application of TumblerAdd's result-length identity `#(s ⊕ ℓ) = #ℓ` under the span's own well-formedness hypotheses, composed with `#ℓ = #s` from level-uniformity. Sound.

**S2 (EmptyDistinction).** The proof itself is valid: T12's postcondition (b) gives `s ∈ span(s, ℓ) = ⟦s, ℓ⟧`, so the denotation is non-empty. The proof step is clean. However, the formal contract is flawed — see finding below.

**S11 (DifferenceBound).** Boundary derivation: `start(β) ∈ ⟦β⟧ ⊆ ⟦α⟧` (S2 applied to β) gives `start(α) ≤ start(β) < reach(α)`; the contradiction argument (reach(β) > reach(α) would put `reach(α) ∈ ⟦β⟧ ⊆ ⟦α⟧`, yielding `reach(α) < reach(α)`) gives `reach(β) ≤ reach(α)`. The three sub-ranges (L)/(M)/(R) partition `⟦α⟧` by T1 totality; `⟦λ⟧ = (L)` and `⟦ρ⟧ = (R)` follow from reach(λ) = start(β) and start(ρ) = reach(β). WF's preconditions for λ discharge immediately; for ρ, `reach(β), reach(α) ∈ T` come from TumblerAdd's carrier postcondition, and `#reach(β) = #reach(α)` comes from S6 plus level_compat. Tightness: pick `t ∈ ⟦β⟧` (non-empty by S2); `start(α) ≤ t` and `t ≤ reach(β)` with both endpoints in `⟦γ⟧` lets S0 force `t ∈ ⟦γ⟧`, contradicting `t ∉ ⟦λ⟧ ∪ ⟦ρ⟧`. Sound.

---

### S2 formal Preconditions omit `s ∈ T`
**Class**: REVISE
**Foundation**: T12 (SpanWellDefinedness) — preconditions `s ∈ T, ℓ ∈ T, Pos(ℓ), actionPoint(ℓ) ≤ #s`
**ASN**: S2 (EmptyDistinction), Formal Contract Preconditions — "the preconditions of Definition (Span), equivalently the preconditions of T12: ℓ ∈ T, Pos(ℓ) (i.e. ℓ > 0), and actionPoint(ℓ) ≤ #s"
**Issue**: The Preconditions section explicitly claims to enumerate T12's preconditions but lists only three of the four. T12 requires `s ∈ T` as a distinct precondition; S2's list drops it. The Depends section compounds this: "Pos(ℓ) (i.e. ℓ > 0) and actionPoint(ℓ) ≤ #s are S2's own hypotheses, the preconditions of Definition (Span) that T12 likewise assumes" — again omitting both `s ∈ T` and, in that tighter list, `ℓ ∈ T`. A downstream consumer reading S2's formal contract would see an incomplete precondition set and would not know to supply `s ∈ T` when invoking S2 to discharge a non-emptiness obligation.
**What needs resolving**: The Preconditions section must include `s ∈ T` in its enumeration of T12's preconditions. The Depends section's characterization of "S2's own hypotheses" must likewise include `s ∈ T` (and `ℓ ∈ T`, which it currently omits from that sub-list while including it in the Preconditions).

---

VERDICT: REVISE