# Review of ASN-0134

This is an unusually careful note. The conflict analysis (H0–H2), the per-home-vs-global liberation (G1), the operation-level order-dependence families (§4), and the multi-read verdict theory (V0–V2) are all rigorous, and the author has plainly chased down the hard cases — the first-emission boundary in H2, the nesting-homes pathology in H1 (which correctly forces the origin argument over anchor incomparability), the `m=0/1` degenerate batches in A5, the literal-vs-operative reading of I1a in §4, and the strict-implication chain in V2 with its short-circuit converse-witness. I verified the §7 addresses and the §8 quiescence trace; both check out. I found one genuine gap.

## REVISE

### Issue 1: W5's out-of-order nullify dichotomy is non-exhaustive

**ASN-0134, §5 (W5, ActiveSliceStepLocal)**: "A nullify ordered before its target exists, where the target is *another* home's not-yet-emitted address, is *rejected*: at that state `a ∉ A_rel` and `a ≠ a_emit(Σ, d_retr)` (the slot lies on the other home's chain, not the retractor's)... Either way no retraction is left targeting an absent address — the cross-home pre-target case by declining, the self-emit case by pre-nullifying its own slot."

**Problem**: W5 makes a soundness claim ("no interleaving can yield an incoherent slice"), and its supporting case-analysis partitions out-of-order nullifies into exactly two cases via "Either way": (cross-home pre-target → decline) and (self-emit own frontier → pre-nullify). But there is a third case the dichotomy omits. Let `d_retr`'s link frontier be `f := f_{d_retr}^Σ`. The emitted slots of `d_retr`'s own chain are indices `0 … f−1`, the frontier slot is index `f` (`= a_emit(Σ, d_retr)`), and the slots at index `> f` are `d_retr`'s *own* not-yet-emitted *non-frontier* addresses. A `Nullify_Binary(Σ, d_retr, a)` with `a = chain_{d_retr}(j)`, `j > f`, has `a ∉ A_rel^Σ` (not emitted) and `a ≠ a_emit(Σ, d_retr) = chain_{d_retr}(f)` (chain injective, `j ≠ f`), so P-tgt fails and the call **declines** — but it is *not* cross-home: the slot lies on the retractor's own chain, so the note's rejection justification "(the slot lies on the other home's chain, not the retractor's)" does not apply to it. The soundness *conclusion* survives (a declined call deposits nothing, hence no dangling retraction), but the stated case-partition is not exhaustive, and the rejection criterion is mischaracterized as cross-home-specific when it is in fact P-tgt-general.

**Required**: Generalize the rejection arm from "cross-home pre-target" to "any P-tgt-failing target (`a ∉ A_rel^Σ ∧ a ≠ a_emit(Σ, d_retr)`) by declining," which subsumes both another home's not-yet-emitted addresses *and* the retractor's own not-yet-emitted non-frontier slots. The complete trichotomy is then: `a ∈ A_rel^Σ` → normal nullify; `a = a_emit(Σ, d_retr)` → self-emit, self-nullify; otherwise → decline (no step, no deposit). The "Either way no retraction is left targeting an absent address" conclusion then rests on a partition that actually exhausts the inputs Nullify_Binary admits (the to-span `(a, δ(1,#a))` is T12-well-formed for *any* tumbler `a`, so the pathological own-future target is a legal argument).

## OUT_OF_SCOPE

None to add. The note's own "What this note does not cover" section and Open Questions correctly defer scheduler/fairness, agent activation, inter-server/BEBE, concrete mechanisms, and predicate-evaluation cost — and it defines no claims that intrude on those, so there is nothing miscategorized to flag.

The ASN is a consistency/isolation model — it characterizes the guarantees (serializability, snapshot reads, per-home conflict locality, the invariant partition, the snapshot-predicate semantics of quiescence) and states MIC as mechanism-free obligations any faithful realization must meet. That is system-guarantee territory, stated abstractly enough that an alternative implementation (per-home scheduler, optimistic frontier-CAS, etc.) would have to satisfy it. It has not drifted into implementation mechanics.

VERDICT: REVISE
