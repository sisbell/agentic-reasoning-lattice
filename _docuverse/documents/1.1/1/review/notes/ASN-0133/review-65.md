# Review of ASN-0133

I checked the proofs in this note closely — Q0's fixed-view-base rewrite (including the worked `R'` example, whose arithmetic I verified: correct value ⊤, both naive merges ⊥), Q3's idem=⊤ dedup-hit exclusion via the audit-slice spelling, Q5's per-σ injection, Q-EXT's at-most-once-per-argument, the regime form of H-SFAIR, all three branches of Q6 with both counterexamples, and the worked `cmt`/`res` trace `Σ₀→Σ₁→Σ₂`. The technical content holds up: I found no errors in the termination logic or the worked verification.

The findings below are prose defects — non-advancing statements of the kind the anti-bloat classifier targets.

## REVISE

### Issue 1: H-RF is stated as a tautology
**ASN-0133, Conditional termination, H-RF (FiniteRealFires)**: "A fire sequence from Σ₀ has *finitely many real fires* iff its real (non-no-op) fires are finite in number."

**Problem**: The biconditional relates a phrase to its own paraphrase. "has finitely many real fires" and "its real fires are finite in number" are the same proposition; the only content the right side adds is the parenthetical gloss that "real" means "non-no-op." The hypothesis is framed as *X iff X*. This is conspicuous against the note's own neighbors: H-FIN states a genuine equivalence (emission-set finiteness ⟺ step-run termination), and H-W is a flat condition (`|W(σ)| < ∞`).

**Required**: State H-RF as the condition it is — "σ has finitely many real (non-no-op) fires" — and drop the vacuous biconditional.

### Issue 2: H-FAIR's closing sentence advances no claim
**ASN-0133, Conditional termination, H-FAIR, final sentence**: "Fairness is a scheduler property; any discipline satisfying the statement discharges it, the removal and falsification escapes absorbing exactly the environmental interference a fire-only scheduler cannot forestall."

**Problem**: "any discipline satisfying the statement discharges it" is tautological — a discipline satisfies H-FAIR's statement exactly when it is fair, so "satisfies the statement ⟹ discharges [fairness]" is *X⟹X*. The trailing clause then restates a point already made earlier in the same paragraph ("a scheduler controls only its *fires*, so it cannot prevent the environment from falsifying x first"; "the scheduler owes nothing to absent or already-falsified arguments"). The sentence is a closing flourish that the reader must skip past to reach Q6.

**Required**: Cut the sentence. If "fairness is a scheduler property" is worth keeping, keep only that clause and drop the tautology and the restatement.

## OUT_OF_SCOPE

### Topic 1: Well-formedness of pdef-triggers
The note admits a trigger given as a `pdef` address (evaluated by reference) but does not state the well-formedness condition such an address must meet to *be* a trigger — that `sig(a)` carry Boolean result sort and a parameter matching `D_ρ`'s element sort. This is implied by RG's definition (`T_ρ : D_ρ → Bool`) and is fine to leave to the activation-binding layer the note already defers; a future ASN giving the pdef-trigger calling convention would pin it down.

VERDICT: REVISE
