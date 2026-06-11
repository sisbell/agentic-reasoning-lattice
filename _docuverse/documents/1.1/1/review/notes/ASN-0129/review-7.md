# Review of ASN-0129

I verified the load-bearing arguments rather than summarizing them; the checks that mattered are recorded below so the convergence claim is auditable.

**Checks performed.**
- **V-IDX vacuity**: recomputed against the designated entries' fixed records (S1–S3) — BH1 fails at the two Binary designates (`supersedes`, `R`), BH2/BH3 fail at the Unary `retired`, BH4 fails at all three (`idem=⊤` throughout). Universal attachment of any behavior family is foreclosed twice over (fixed records and R-C0 compatibility), so the instance-wise exclusion is genuinely vacuous at every constructible registry, as claimed.
- **The trace**: recomputed all three transitions. Gates pass (`|F|=|G|=1` against Binary at each emit); the Σ₁ dedup for `Emit_res` correctly misses against `A_res^{Σ₁} = ∅`; at Σ₃ the nullified set is exactly `{a₂}` — `a₁` and `a₃` are chain *siblings* of `a₂` (equal length, distinct, hence prefix-incomparable by T10a.2's argument), so single-tuple scope holds and `M_cmt` survives. The value sequences ⊥,⊤,⊥ for `quiescent(t)` and ⊥,⊤,⊤ for `ever_res` are both correct.
- **PD0 soundness**: the witness-persistence ground checks for every rule — grow-only bases by the step effects, filters by membership-plus-ST-body persistence, existential witnesses by L12a/L12 across extended-record steps, count polarities (`count ≤ c` in SF only; equality in neither class — falsifiable upward from below, dead once overshot) are all right. The implication rule (`P ∈ SF, Q ∈ ST ⊢ P⇒Q ∈ ST`) checks by case split.
- **QD-fin**: the induction is complete (only three step kinds exist under `→_sh`, each adjoining at most one key), and the self-contained re-derivation of link-store finiteness honestly spares the B2/RP-b transfer chain a bare L-fin citation. H-init is correctly identified as a hypothesis no foundation claim supplies — naming it rather than citing it is the right move.
- **PC6**: the converse's one substantive leaf — `Observe_K` as a finite per-tuple conjunction over V-TUP coverage tests — checks (pattern sets are finite query data; `S_view ∈ {L_K, A_K}` are QD domains). The registry-lookup discharge by constant-folding is sound given R1. The entailment polarity between the unrestricted ceiling and C-reach is stated correctly (ceiling ⟹ ¬C-reach via the feedback loop; conjecture of C-reach is implicitly conjecture of ceiling failure; ¬C-reach would not restore the ceiling, hedged by the parity example).
- **C-reach downgrade**: the three reasons the naive FO argument fails are each correct — on out-degree-≤1 graphs `is_in_chain` *is* `reach` at arbitrary distance (the walk visits the entire reachable set before sink or revisit), PC2a's counting exceeds plain FO, and V-PRIM's built-in total orders degrade locality-based lower bounds. Downgrading to conjecture with the proof obligation recorded is the rigorous outcome.
- **UV/FP/PD2 coherence**: the `is_in_chain` Boolean clause (active-walk verdict, deliberately divergent from `target ∈ elems(chain(addr))` at default view) is acknowledged at both sites; `targets_keyed`'s cross-type footprint and BH4's home-wide footprint are carried into PD2's exception list explicitly. Boundary cases (empty domains in PC1, `max_{T1}` at ∅, the impossible empty registry under R-C1) are handled.

## REVISE

(none)

## OUT_OF_SCOPE

### Topic 1: Protocol-layer convergence theory over PD0–PD2
**Why out of scope**: The note supplies the language, evaluation guarantees, and stability classes, and explicitly fences trigger/termination constructions. A successor owes the actual theorems — soundness of fire-until-stable loops under PD0 hypotheses, re-opening rules when PD1 falsifiers are admitted, scheduler fairness and fire atomicity. That is new machinery written *in* PL, not a gap in PL's foundation.

### Topic 2: The C-reach invariance argument (the note's Open Question 6)
**Why out of scope**: Proving reach-inexpressibility requires exhibiting branchy, cardinality-balanced state families invariant under every atom, aggregate, and order-sensitive composite — an argument in a counting-plus-order regime where nearby questions are open. The note correctly holds it as a conjecture; discharging it is future work, not a defect here.

### Topic 3: Mechanical certification of the dynamics classes (Open Question 5)
**Why out of scope**: PD0's enumerated forms are sound but deliberately incomplete — e.g., the audit-view atom spelling `c ∈ M_K` is uncertified while its equivalent `(∃ x ∈ M_K :: x = c)` is in ST. A checker that normalizes spellings before classifying, and its decidability, belongs to a successor; the note flags the incompleteness itself.

### Topic 4: Paired extensions of base and vocabulary
**Why out of scope**: The relativization-cost paragraph prices the deliberate omissions — accumulating Σ-folds, ℕ-multiplication, exposed address arithmetic — and observes that admitting any requires moving both sides of PC6's equality at once (V-PRIM and the base together). The bounded least-fixed-point successor (Open Question 4) is the largest instance. These are conscious ceiling-raises for future notes, not errors in this one.

VERDICT: CONVERGED
