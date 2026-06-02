# Review of ASN-0086

## REVISE

### Issue 1: WP Case 1 presents a sufficient — not weakest — precondition, silently omitting the self-emit branch

**ASN-0086, Weakest-Precondition Analysis, Case 1**: "the conjunction `P0(Σ, d_retr) ∧ P1(Σ, a)` … is a *sufficient* precondition for the postcondition, with each conjunct load-bearing. … For P1, choose `a ∉ A_rel^Σ` distinct from the fresh emitter `a_emit(Σ, d_retr)` …"

**Problem**: The section is titled *Weakest-Precondition Analysis*, and Case 2 computes an actual weakest precondition, but Case 1 computes only a *sufficient* one and never identifies the weakest. There is a concrete, unacknowledged case where the scope postcondition `{t : a ≼ t} ∩ A_rel^{Σ'} = {a}` holds despite `¬P1`:

Take `a := a_emit(Σ, d_retr)`. This `a` is fresh by construction (`a_emit` always returns an address `∉ dom(Σ.L)`), so `a ∉ A_rel^Σ` — `P1` fails. But `Nullify` executes under `P0` alone (the note states "P0 governs execution; P1 and PC condition the … postcondition"), so the internal `Emit_R` deposits its retractor at `a_emit(Σ, d_retr) = a` itself, giving `Σ'.L(a) = (∅, {(a, δ(1,#a))}, R)`. Then `A_rel^{Σ'} = dom(Σ.L) ∪ {a}`, and R0a's antichain at Σ' gives `{a' ∈ dom(Σ'.L) : a ≼ a'} = {a}` — the postcondition holds with `P1` false.

The load-bearingness counterexample tacitly avoids exactly this case ("distinct from the fresh emitter `a_emit(Σ, d_retr)`"), which is the tell: the authors know `a = a_emit` is special but never connect it to weakestness. This is the same self-emit configuration the document itself constructs and analyzes in Worked Sketch Step 4 (`a₃ = a_emit(Σ_3, d)`), so the machinery to recognize it is present elsewhere. The true weakest precondition is strictly weaker than `P0 ∧ P1`, roughly `P0 ∧ (a ∈ A_rel^Σ ∨ a = a_emit(Σ, d_retr))`.

**Required**: Either (a) compute the actual weakest precondition for Case 1, including the `a = a_emit(Σ, d_retr)` branch under which scope holds via R0a directly (R-Scope's `P1` domain does not cover it, but the conclusion does); or (b) state explicitly that Case 1 deliberately offers only a sufficient, non-redundant precondition rather than the weakest, and say why the self-emit branch is excluded — making clear that "load-bearing" here means "non-redundant," not "necessary."

## OUT_OF_SCOPE

### Topic 1: Atomicity/consistency of `A_K` transitions under concurrent `Observe`

The Open Questions already defer concurrency and observation-consistency to future work; the active/audit distinction is specified state-locally, and a concurrency model is genuinely new territory.

VERDICT: REVISE
