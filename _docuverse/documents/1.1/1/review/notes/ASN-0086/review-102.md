# Review of ASN-0086

## REVISE

### Issue 1: P1 mislabeled as an emission-gating precondition; contradicted by the WP analysis
**ASN-0086, Definition — Nullify**: "Nullify has two *executing preconditions* that gate the underlying Emit_R — (P0) `d_retr ∈ dom(Σ.M)` ... and (P1) `a ∈ A_rel^Σ` ..."

**Problem**: P1 does not gate emission. `Nullify(Σ, d_retr, a) ≡ Emit_R(Σ, d_retr, ∅, {(a, δ(1, #a))})`. The span `(a, δ(1, #a))` is T12-well-formed for *any* tumbler `a` (since `#a ≥ 1` by T0 and `actionPoint(δ(1, #a)) = #a ≤ #a`), regardless of whether `a ∈ dom(Σ.L)`. So the underlying Emit_R executes and produces a Σ' even when `a ∉ A_rel^Σ`. P1 is required for the *postcondition* (`a ∈ nullified(Σ')`), not to gate the operation — exactly like the scope condition P2.

The ASN contradicts itself: WP Case 1's necessity argument for P1 explicitly assumes emission proceeds — "dropping P1 admits `a ∉ A_rel^Σ`; the only new key at Σ' is the fresh emitter `b ≠ a`, so by L12a's pointwise agreement `a ∉ dom(Σ'.L)`..." This treats Σ' as existing and only the postcondition failing. By contrast, P0's necessity says "Nullify does not execute, no post-state Σ' is produced." The two are treated inconsistently while both are labeled "executing preconditions that gate the underlying Emit_R."

**Required**: Reclassify P1 as a postcondition-establishing condition (alongside P2), not an emission gate. Only P0 genuinely gates emission (K.λ's home precondition). Make the Definition consistent with WP Case 1's necessity treatment.

### Issue 2: Frame-condition prose and forward operation-inventory duplicated across sections
**ASN-0086, "State transition relation"**: "ASN-0093's frame conditions on each K-op ensure that the two non-affected stores are preserved pointwise, and that the affected store is extended by exactly one fresh key per step."
**ASN-0086, "Definition — Reachability"**: "By the frame conditions of (i)–(iii) — each primitive transition extends exactly one of `Σ.C`, `Σ.M`, `Σ.L` at a fresh key and leaves the other two components unchanged..."

**Problem**: Two paragraphs in adjacent sections state the same frame-condition fact in different words. Separately, the "State transition relation" paragraph carries a forward use-site inventory — "The operations defined later in this note (Observe, Nullify) either compose Emit_K ... or leave Σ unchanged (Observe)" — that is restated again in "Definition — relational layer." These are the anti-bloat patterns the classifier names (repeated content; downstream-consumer inventory in a structural slot).

**Required**: State the frame-condition fact once; delete the forward operation inventory from the transition-relation section (it belongs only where the operations are defined).

### Issue 3: Single-tuple scope proved twice
**ASN-0086, Definition — Nullify ("Single-tuple scope, absolute under R0a")** and **WP Case 1**: both establish `{t : a ≼ t} ∩ A_rel^{Σ'} = {a}` via R0a's antichain on `dom(Σ'.L)`.

**Problem**: The same conclusion with the same R0a-antichain derivation appears in both places. The WP version adds only necessity/sufficiency framing around an identical core argument.

**Required**: Prove the scope result once and have the other site cite it, rather than re-deriving the antichain argument.

## OUT_OF_SCOPE

### Topic 1: Concurrency/atomicity of Emit vs. Observe, ordering of Observe results, cardinality bounds on nullified(Σ)
**Why out of scope**: These are raised in Open Questions and concern a consistency model and resource bounds not yet defined; they are future-ASN territory, not defects here.

### Topic 2: Whether L1b should be tightened to `#E = 2` at the substrate
**Why out of scope**: R0a-Cor2 establishes `#E = 2` within this note's scope; whether ASN-0043's L1b should be amended is a foundation-level design question for a different ASN.

VERDICT: REVISE
