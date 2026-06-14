# Review of ASN-0133

This is a careful, mature note; I found no errors in the theorems themselves — Q0's view-rebuild, Q-EXT/Q5a's extinction bound, and Q6's three-obstruction case analysis all check out, and the two worked traces evaluate correctly. The findings below are a precision defect in the H-W treatment, one imprecise summary, and the meta-prose the anti-bloat classifier asks for.

## REVISE

### Issue 1: H-W collapses to perpetual quiescence, so its apparatus and "implies quiescence directly" are near-vacuous

**ASN-0133, Conditional termination (W/H-W, "The H-RF/H-W separation", Q5)**: "H-W implies quiescence directly: `|W(σ)| < ∞` bounds the trigger-true indices, so past the maximum such index `k*` no `(ρ, x, k)` is trigger-true ... every σ *reaches* quiescence (by `k*+1`) and *holds* it, with no fairness and no regime hypothesis. H-W is thus too strong to serve as Q6's hypothesis..."

**Problem**: The registry-level hypothesis H-W (`|W(σ)| < ∞` for *every* σ from Σ₀) is satisfiable only when no σ-reachable state is trigger-true — i.e., only at perpetual quiescence. Any reachable trigger-true state can be frozen into an infinite tail (an environment stutter `Σ → Σ`, valid because `→_sh*` is reflexive, or no-op fires), and the recurring `(ρ, x, k)` triples over that tail force `|W(σ)| = ∞`. Hence under H-W, `|W(σ)| = 0` for every σ and real fires `= 0`: "H-W implies quiescence directly" reduces to "perpetual quiescence implies quiescence," and Q5's bound (`real fires ≤ |W(σ)| = 0`) collapses to Q1's no-op consequence. The note half-sees this ("that starvation is essentially every registry that ever reaches a trigger-true argument") but still presents H-W as the graduated *top* of a hierarchy (H-W > bounded-growth > H-RF), with its own definition, a lemma (Q5), and a "separation" discussion, and frames `H-W ⟹ H-RF` and `H-W ⟹` quiescence as informative steps. They are not informative: the top of the hierarchy is degenerate, and the "separation" of H-RF from H-W is a comparison against a near-empty class.

**Required**: State the equivalence — registry-level H-W ⟺ every σ-reachable state is already quiescent — so H-W reads as the vacuous foil it is. Make explicit that the only meaningful content is the *per-σ* injection (finite `W(σ) ⟹` finite real fires, true of every σ and independent of H-W) and that the meaningful registry-level work bound is Q5a's distinct-argument count `|⋃_k [D_ρ]|`. Compress the H-W apparatus to match its foil-only role.

### Issue 2: The worked example's registry-side summary drops the bounded-direct-comment-traffic condition

**ASN-0133, Worked composition (*Quiescence*)**: "For this registry the *registry-side* guarantee — finitely many real fires, registry-inert past N — holds given a bounded flagged population under any weakly-fair scheduler."

**Problem**: `ρ_R`'s real fires are bounded by `|comments ever| = |ρ_P fires| + |direct environment cmt deposits|`. The note's own *Bound* paragraph conditions correctly on "that flagged population, *and any direct environment comment traffic*, [being] bounded," and explicitly admits direct deposits ("plus any the environment deposits directly"). If direct cmt traffic is unbounded while flags are bounded, `L_cmt` (= `[D_{ρ_R}]`) grows unbounded, `ρ_R` fires unboundedly, and "finitely many real fires" fails. A bounded flagged population *alone* is insufficient.

**Required**: Restore the direct-comment-traffic clause to the summary, or state that this registry assumes direct cmt deposits are absent/bounded.

### Issue 3: Meta-prose accretion (anti-bloat)

**ASN-0133, several sites**:
- Q0: "Purity makes every verdict observer-uniform — no agent reports, no consensus, no decision history." — editorial flourish on significance; does not advance the `quiescent_R ∈ PL` claim.
- Q6: "...is where the conclusion is genuinely weaker — *and not by a gap in the proof*." — defensive aside addressed to the reviewer, not content.
- Q6: "**(3)** — *the case the bounded-growth reader must not miss* —" — reader-instruction in a structural slot.
- Q6: the registry-side guarantee is stated at the section opening ("*Registry-side, unconditional.* ... is the registry's standing guarantee") and restated in substance at the proof's end ("What survives unconditionally is the registry-side half established at the outset: past N the registry never fires for real again...").

**Problem**: The note carries `review-mode.anti-bloat`; these are exactly the flourish / defensive-justification / reader-aside / duplicate-statement patterns that compound across cycles.

**Required**: Delete the flourish, the "not by a gap" aside, and the reader-instruction; drop or merge the closing registry-side restatement.

## OUT_OF_SCOPE

The note's "What this note doesn't cover" and "Open questions" already scope out the scheduler/serialization, the SF certificate (`pd_extinct`), cross-scope oscillation theory, and the environment model appropriately. No additional future-ASN topics surfaced.

VERDICT: REVISE
