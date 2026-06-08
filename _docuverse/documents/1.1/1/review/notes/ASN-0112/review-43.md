# Review of ASN-0112

I worked through the span construction, both covering cases, the V-ReachTight biconditional, and the worked examples; the mathematics is sound (D0/D1 round-trip, the k=1 overshoot computation, the single- vs. cross-subspace split, and the wp derivations all check out). My findings are confined to the accretion the `review-mode.anti-bloat` classifier flags: the reach-tightness fact is re-derived rather than cited.

## REVISE

### Issue 1: wp Tight re-derives V-ReachTight instead of citing it
**ASN-0112, Preconditions and well-definedness**: "if `O(d) ≠ ∅` and `#origin_d ≤ #reach_d`, then D1 closes the round-trip and `reach(σ_d) = r⋆ = reach_d`, giving `Tight` (forward); conversely if `#origin_d > #reach_d`, then D0 makes the round-trip fail and `reach(σ_d) = r⋆ > reach_d`, giving `¬Tight`."
**Problem**: This is V-ReachTight (`reach(σ_d) = reach_d ⟺ #origin_d ≤ #reach_d`) re-proved verbatim via the same D1/D0 argument. The asymmetry is self-evident: the *companion* wp in the same section — `wp(op, Exact) = (single subspace)` — is derived correctly by *citing* V5 and V6, not by re-running their proofs. The Tight half should follow the same pattern.
**Required**: Replace the Tight derivation with a one-line appeal: `wp(op, Tight) = (O(d) = ∅ ∨ #origin_d ≤ #reach_d)` is immediate from V-ReachTight (with the empty-result disjunct handling vacuity). Drop the repeated D1/D0 walk.

### Issue 2: the `#origin_d > #reach_d` overshoot is established at five separate sites
**ASN-0112, multiple sections**: the fact that origin deeper than reach forces `r⋆ > reach_d` (round-trip failure) appears in (1) V2's second covering case (explicit TumblerAdd, k=1), (2) V-ReachTight's summary (D0), (3) the worked depth-divergent variant, (4) the implementation reach-tightness remark, and (5) the wp Tight derivation (Issue 1).
**Problem**: One proven fact, restated five ways. V2 case 2 already computes `reach_d < r⋆`; V-ReachTight then re-invokes D0 to conclude `r⋆ ≠ reach_d` when it could simply cite V2's strict inequality. This is the "two paragraphs say the same thing in different words" accretion pattern compounding across the note.
**Required**: Designate one site as the proof (V2 case 2 is the natural home, since it does the explicit computation) and have V-ReachTight and the worked variant cite it rather than re-deriving. Consolidate to a single canonical derivation.

### Issue 3: implementation remark offers "evidence" for an already-proven theorem
**ASN-0112, Implementation evidence**: "the root width is recomputed as a maximum-minus-minimum reach and remains non-negative ... concrete evidence for V2's positivity."
**Problem**: V2's positivity (`Pos(extent_d)`) is discharged abstractly by D0 — it is a theorem of the span algebra, not a contingent fact that implementation behavior could confirm or refute. Presenting empirical "evidence" for a proven invariant is the defensive-justification pattern: the prose does not advance the argument, since the proof already closes it. (Contrast the Q12–Q20 and Q14 remarks, which legitimately ground *design choices* like "the grasp is always occupied.")
**Required**: Either drop the non-negativity remark or reframe it as confirming the implementation *conforms to* the proven invariant, not as evidence *for* it.

## OUT_OF_SCOPE

(none — the note correctly defers per-subspace extent, version comparison, link counting, and content delivery to their own ASNs via Open Questions and the scope note.)

VERDICT: REVISE
