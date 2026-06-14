# Review of ASN-0134

This is a careful, deeply-worked note. The conflict theory (H0–H3), the invariant partition (W0–W6), and the two operation-level non-confluence families of §4 are correct and, in several places, sharper than the foundations they rest on (H1's origin route genuinely covers the cross-document/cross-subspace case `CrossDocumentDisjointness` leaves unnamed; the I1a literal-vs-operative reading is a real and subtle observation). The worked traces in §7 and §8 check out arithmetically. I have two completeness gaps, both in otherwise-correct proofs, and neither a correctness error.

## REVISE

### Issue 1: G1's validity argument proves only the frontier precondition, then claims all preconditions

**ASN-0134, §4, G1 proof part (i)**: "per-home comparability totally orders `(d, S)`'s allocations, so by H0 each reads the frontier its predecessor left and lands at the next slot — gapless, collision-free — and by H1 no cross-`(d, S)` step disturbs that frontier wherever the linearization places it. **Each step's precondition is thus met at its position, so the linearization is a valid execution.**"

**Problem**: The argument establishes that *frontier-freshness* is met under any linearization, then concludes that *each step's precondition* is met. But a `K.λ_sh` step also carries the gate preconditions (K registered, `Sh-conf(K, F, G)`, arity 3) and both `K.α`/`K.λ_sh` require `d ∈ dom(M)`. "The linearization is a valid execution" requires *all* of these at each step's (reordered) position, not only the frontier one. The proof never argues the non-frontier preconditions survive reordering. They do — but that is precisely the kind of multi-premise step a Dijkstra-style proof must not leave implicit, especially in the note's central theorem. The lifted version (the `H3` paragraph) repairs the `d_new ∈ dom(M)` part for `K.σ`/allocation via register-before-allocate, but the **gate** is unargued in both the base and lifted proofs.

**Required**: Add one sentence to G1(i) (carrying to the lift): the gate is reordering-invariant — `Sh-conf` by ASN-0128 P4 (ShConfStateIndependence), arity and registration-status by registry immutability (W6 / ASN-0128 R1) — and `d ∈ dom(M)` persists by G-PO's pre-registration plus ASN-0093's M1 monotonicity (already named in A6's transition clause). Hence frontier-freshness is the *sole* reordering-sensitive precondition, which is what the per-home argument must (and does) secure. This converts "each step's precondition is thus met" from an overstated conclusion into a discharged one.

### Issue 2: V2's second strict implication is asserted but never witnessed, breaking parity with the first

**ASN-0134, §8, V2**: "`[all p reads at one index] ⟹ [no Q-affecting step linearizes between the first and last read] ⟹ [the verdict is sound about a single state]`. The middle condition ... is the weakest *sufficient* condition this note establishes, **not** a necessary one: the implication to soundness is genuinely *strict*, since a verdict may come out sound by other routes — g insensitive to the disturbed constituent ... — even when a Q-affecting step does fall between the reads (the banking argument above proves only the sufficient direction ... and offers nothing converse)."

**Problem**: The *first* implication's strictness is concretely exhibited — the §8 trace's non-`Q`-affecting `K₁`-emit moves the index while preserving soundness. The *second* implication's strictness (soundness possible *with* a `Q`-affecting step between the reads) is only asserted with a one-line plausibility route; the §8 trace shows the opposite for its `g` (the `Q`-affecting `T₂`-nullify produces an *unsound* verdict). The note honors the "concrete example" standard everywhere else (§7, §8); this strictness claim alone stands on a reason without a witness, leaving the "strict, not iff" framing partly undischarged.

**Required**: Either exhibit a short witness — e.g. short-circuit `g(v₁, v₂) = (v₁ = ⊤) ? ⊤ : v₂`, read `v₁ = ⊤` at `r₁` (so `Q(Σ_{r₁}) = ⊤`), then a `Q`-affecting step flips the not-yet-read but `g`-ignored `v₂`, and the verdict is still `⊤ = Q(Σ_{r₁})` — or soften the framing to "we establish sufficiency; necessity is not claimed," dropping the "strict implications" assertion to what is actually derived.

## OUT_OF_SCOPE

### Topic 1: A reader-facing batch-atomicity contract (OQ4/OQ5)
The note correctly proves (A5) that the substrate provides no all-or-nothing visibility for `m ≥ 2` batches, shows W4 supplies only the *writer-side* (contiguity) half, and defers the reader-side closure. That deferral is sound — a "batch isolation" layer is genuinely new territory, not a gap in this note's per-step model. No flag; affirming the scoping.

### Topic 2: Cross-server composition of per-home orders (OQ7)
G1's per-home independence is the natural seam for inter-server progress, but the multi-server consistency model (BEBE) is correctly left to a separate note. Appropriately scoped out.

VERDICT: REVISE
