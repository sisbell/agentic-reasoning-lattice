# Review of ASN-0131

I worked through every introduced claim against the foundation contracts. The mathematics is sound throughout — RE-DEF, RE-SND/RE-CMP (immediate reads of the biconditional), RE-UDIST, the two-obstruction intersection argument (RE-UDIST-∩), RE-SEL, RE-CWP, and the RE-ADDR/RE-RET addressability chain all check out, including the worked instance (I verified `a₄ = a₂ ⊕ δ(2,#a₂)` is the exclusive bound via TS3, the `coverage(e₃) ∩ dom(Σ.C) = ∅` field-agreement argument, and the contraction-WP derivation). The note satisfies the depth requirements: a non-trivial wp (RE-CWP), a concrete worked example exercising every postcondition, and derived consequences throughout.

The findings below are anti-bloat: this note carries the `review-mode.anti-bloat` classifier, and the prose around its cross-ASN imports has accreted past what the claims need.

## REVISE

### Issue 1: ASN-0082 insert/delete machinery is cited and then declared irrelevant

**ASN-0131, "Stability... Under editing of the queried document"**: "The foundation realises them as displacements (I3 PostInsertionShift, D-SHIFT, ASN-0082): an insertion at `p` of width `n` carries the content at every position `v ≥ p` up to `shift(v, n)` (I3, established there at every text depth `#p ≥ 2`), and a deletion carries the content lying above the removed span back down (D-SHIFT, established there at text depth `#p = 2`; the foundation supplies no gap-closing interior-span delete at greater content depths `m_{s_C} > 2` ...). That difference is one of *primitive availability* ... — not a scope on RE's stability."

Followed by: "What that argument requires of either is not the displacement's specifics but only that it is an arrangement edit confined to `Σ.M(d)` — an **M-only edit**."

**Problem**: The paragraph imports I3/D-SHIFT, the insert-vs-delete depth asymmetry, the "no gap-closing interior-span delete at `m_{s_C} > 2`" caveat, and the I3-V un-backfilled-vacancy intermediate — then states outright that none of these specifics bear on RE's stability ("not a scope on RE's stability," "not the displacement's specifics but only ... M-only"). This is machinery cited only to be set aside. A precise reader must read and discard the depth-asymmetry and gap-closure digression to reach the single load-bearing fact (mid-document shift is an M-only arrangement edit, conservatively lifted).

**Required**: Reduce to the M-only point: mid-document insert/delete are arrangement edits confined to `Σ.M(d)` (a conservative lift of ASN-0082's shift primitives, which model only `(C,M)`), so RE tracks them by image membership exactly as it tracks the atomic movers, at any content depth. Drop the I3/D-SHIFT depth-asymmetry, the interior-span-delete caveat, and the I3-V intermediate — the note itself certifies they don't matter.

### Issue 2: The addressability section re-narrates ASN-0086's provenance and over-justifies the import

**ASN-0131, "Fresh emissions and the addressable population"**: "Its **to-set consequence**, ASN-0086's *unit-depth retraction discipline* ... follows by induction over layer-reachable states (ASN-0086). Since `nullified(Σ)` is an existential over `L_Θ^Σ` alone (ASN-0086), this `L_Θ`-scoped unit-depth fact is exactly what addressability consults." And later: "The unit-depth discipline is imported at a *stronger* reachability: ASN-0086 discharges it only for *layer*-reachable states, and the replayed `K.λ` sequence is layer-reachable precisely because the standing discipline commitment holds along it..."

**Problem**: The `Σ.L`-evolution bridge is load-bearing — RE-ADDR and RE-RET genuinely need ASN-0086's R0a/R-Scope/unit-depth lemmas transferred into ASN-0047's reachability, and that transfer must be justified. But the prose re-narrates *how* ASN-0086 derives the discipline ("follows by induction over layer-reachable states") and appends relevance-justifications ("is exactly what addressability consults"), rather than stating the imported fact and citing it. This is the "re-derives provenance" / "explains why the imported result is needed rather than what it says" pattern.

**Required**: State the imported facts (unit-depth to-set on `L_Θ`; flat antichain R0a; single-tuple scope R-Scope) with bare ASN-0086 citations, keep the one-sentence reachability-bridge inclusion that licenses the transfer, and cut the re-narration of ASN-0086's own induction and the use-site justifications.

### Issue 3: The intersection characterization is stated twice in consecutive sentences

**ASN-0131, "Composing regions"**: "Because the `⊆` half is unconditional, `⊇` — and hence equality — holds *exactly* when `(∀ (i, e) ∈ Avail(Σ) : touch_{W₁}(e) ∧ touch_{W₂}(e) ⟹ touch_{W₁ ∩ W₂}(e))` ... With the `⊆` half unconditional and the pool `Avail(Σ)` region-independent, this touch-implication is the *exact* — necessary and sufficient — characterisation of intersection-equality."

**Problem**: The second sentence restates the first — "holds *exactly* when [formula]" and "this touch-implication is the *exact* — necessary and sufficient — characterisation" are the same assertion, and "With the `⊆` half unconditional" repeats the "Because the `⊆` half is unconditional" justification already given. Two sentences in the same paragraph saying the same thing.

**Required**: Merge into one statement of the necessary-and-sufficient condition, then proceed directly to the genuinely new "What it is not is *structural*" point.

## OUT_OF_SCOPE

### Topic 1: Whole-endset vs touching-spans, multiplicity, rendered answers, the structural intersection condition, cross-store completeness, type-slot-against-content, and link-subspace regions

**Why out of scope**: These are correctly captured by Open Questions 1–7. The note holds RE-WHOLE provisional pending OQ1 and confines itself to `W ⊆ s_C` with the type-disjointness hypothesis flagged (OQ6) — each is new territory for a successor operation/note, not a gap in this one. RE-CLIP is correctly established as universal across both readings, so deferring RE-WHOLE's resolution does not undermine the no-clipping guarantee. No action needed; the deferrals are appropriately scoped.

VERDICT: REVISE
