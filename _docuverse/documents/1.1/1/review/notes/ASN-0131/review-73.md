# Review of ASN-0131

I checked the core definition, the worked example, the addressability machinery (RE-ADDR), the algebraic laws (RE-UDIST / RE-UDIST-∩), and the stability results (RE-EDIT, RE-RET, RE-CWP). The substantive logic is sound: RE-DEF is a clean set-builder, soundness/completeness fall out of it directly, the worked instance correctly exercises every distinctive postcondition (including the `θ`-disjointness field argument), the two intersection counterexamples (non-injective and injective) genuinely refute `⊇`, and RE-ADDR / R-Scope / RE-CWP all hold under the stated hypotheses. The issues below are a factual error, a mis-framed caveat, and an accreted recap.

## REVISE

### Issue 1: `addressable` is wrongly said to depend on the arrangement
**ASN-0131, "The unit of the answer: anchoring without names"**: "ASN-0086's `nullified(Σ)` — the set of withdrawn addresses — is a function of the link store `Σ.L` alone. So `addressable` depends on `Σ.L` and the present arrangement, never on *how* a retraction was performed."

**Problem**: The "So" presents the second sentence as a consequence of the first, but it contradicts it. `addressable(Σ) = dom(Σ.L) ∖ nullified(Σ)`; the note has just said (correctly) `nullified(Σ)` is a function of `Σ.L` alone, and `dom(Σ.L)` is too. So `addressable` is a function of `Σ.L` alone and does **not** depend on the arrangement. The note relies on exactly this elsewhere — the stability section states "`addressable(Σ)` and the region-independent pool `Avail(Σ)` are functions of `Σ.L` (through `nullified`) alone," and union-distributivity uses `Avail(Σ)` as "a function of `(Σ.L, nullified(Σ))` ... does not depend on the region." The "and the present arrangement" clause is false and self-inconsistent.

**Required**: Drop "and the present arrangement" — `addressable` depends on `Σ.L` alone. If the intended point was that *RE* reads both the arrangement and `Σ.L`, that is RE-LOC and belongs there, not attributed to `addressable`.

### Issue 2: RE-EDIT mis-frames the depth-2 caveat as a scope on delete-stability
**ASN-0131, "Stability ... Under editing of the queried document"**: "So delete-stability is scoped to text depth `#p = 2` and insert-stability to every `#p ≥ 2` — an asymmetry in which displacement primitives ASN-0082 supplies. ... Under that assumption the lifted edit acts exactly as every ASN-0047 atomic mover above does, at any content depth."

**Problem**: These two statements sit in apparent contradiction, and the reader must reconcile them within one paragraph. The first scopes "delete-stability" to `#p = 2`; the second says the lifted edit is stable "at any content depth." The load-bearing conclusion is the second: the stability argument needs only M-only confinement and holds at any depth for any M-only edit. The depth-2 limit is solely about whether ASN-0082 *defines a delete primitive* there — it does not constrain RE's stability result. So "delete-stability is scoped to `#p = 2`" mis-states the scope of the result, and the reader works through a caveat the next sentences render moot — the reviser-drift pattern the anti-bloat pass targets.

**Required**: State once that RE-stability holds for any M-only arrangement edit at any depth, then note separately (not as a scope on the stability result) that ASN-0082 supplies a concrete insert at `#p ≥ 2` and a concrete delete only at `#p = 2`. Do not present primitive-availability depths as a scope on delete-stability.

### Issue 3: redundant recap sentence in the Σ.L-evolution bridge
**ASN-0131, "Fresh emissions and the addressable population"**: "The unit-depth discipline is imported at a *stronger* reachability: ASN-0086 discharges it only for *layer*-reachable states, and the replayed `K.λ` sequence is layer-reachable precisely because the standing discipline commitment holds along it... So importing unit-depth is licensed by the standing assumption, not by the bare `→*` inclusion that carries the note's other ASN-0086 `Σ.L`-lemmas."

**Problem**: The closing sentence restates the distinction the preceding sentence already established (unit-depth needs layer-reachability via the standing commitment; the other lemmas ride the bare `→*` inclusion). It is meta-commentary on the proof's licensing structure rather than an advance of the argument — accreted recap, skippable without loss.

**Required**: Cut the closing recap; the preceding sentence already makes the layer-reachability point.

## OUT_OF_SCOPE

(none — the seven Open Questions appropriately defer genuinely-future territory: whole-vs-touching-spans, multiplicity, rendered answers, the structural intersection condition, non-co-resident stores, type-slot/content matches, and link-subspace regions. None should be pulled into this note.)

VERDICT: REVISE
