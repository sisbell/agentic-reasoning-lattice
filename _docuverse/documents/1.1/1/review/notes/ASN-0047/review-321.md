# Review of ASN-0047

I checked the transition model against its own claims: the five-component state, the elementary transitions K.α/K.δ/K.λ/K.μ⁺/K.μ⁺_L/K.μ⁻/K.ρ, the named composite K.μ~, the coupling constraints, and the per-state / composite-boundary invariant partition. The arithmetic in the worked examples is sound (anchor construction `b_C(d)=inc(d,2)=[d.0.1]`, version chains, fork addresses all check out), the J1★ range-vs-domain distinction is correctly applied, and the P4★/P7 content-subspace scoping is a genuine, well-motivated design choice rather than a bug. I found no correctness defect. The note carries `review-mode.anti-bloat`, and the findings below are the meta-prose accretions that finding mode targets.

## REVISE

### Issue 1: The "clause (i) is the shape package, S3★/S8★ are separate" distinction is restated 3–4 times
**ASN-0047, *Decomposition of K.μ~* and Class (a) matrix prose**: The point that admissibility clause (i) constrains only V-position *domains* (S8a, S8-depth, S8-fin, D-CTG★, D-MIN★) and that S3★/S8★ are discharged separately is asserted at least four times:
- clause (iv) discussion — "(i) is a constraint on V-position *domains*, not on which I-address each carries";
- sufficiency clause (i) — "(Recall S3★ is *not* a clause-(i) constraint — clause (i) is the arrangement-*shape* package only — so it is discharged separately, immediately below.)";
- Step (B) — "*the realisation establishes `S3★(Σ')`*" (result K.μ~-S3★);
- matrix prose — "S8★ is *not* an admissibility-(i) precondition (clause (i)'s package, per the Decomposition section, does not list it)".

**Problem**: Each occurrence re-establishes the same shape-vs-referential-integrity boundary, forcing the reader to re-confirm a distinction already settled. This is the "two paragraphs say the same thing in different words" pattern the anti-bloat pass targets.

**Required**: State the clause-(i) scope (shape package only; S3★ via Step (B), S8★ via the decomposition) once, at the admissibility definition, and replace the later restatements with a bare pointer.

### Issue 2: The temporal-scope (per-state vs composite-boundary) distinction is narrated in three locations
**ASN-0047, *Extended reachable-state invariants* preamble, P4a definition box, Class (b) P4a discharge**: The preamble defines the per-state / composite-boundary split and the rule that composite-boundary properties "may transiently fail at intermediate states." The P4a box then re-narrates it ("a composite-boundary property whose witness need not inhabit the current arrangement"), and the Class (b) discharge narrates it a third time ("discharged by induction along the witnessing trace, not by a per-state check ... It forbids a composite that both places `a` (K.μ⁺) and removes it (K.μ⁻) before its endpoint").

**Problem**: The same classification machinery and the same "ValidComposite★ restores at the boundary" argument are re-run in three slots. A reader following the P4a discharge must re-absorb framework prose already given in the preamble.

**Required**: Keep the temporal-scope framework in the preamble only; in the P4a box and Class (b) discharge, cite it and state only what is new to P4a (the witnessing-trace induction).

## OUT_OF_SCOPE

### Topic 1: Renumbering-aware interior contraction of the link subspace
The ASN restricts K.μ⁻ to suffix removal and flags interior `DELETEVSPAN`-style compaction as an open question. This is correctly deferred — modeling renumber-on-delete is new territory, not an error here.

### Topic 2: Concurrency / serialization of same-document link allocation
The SequentialTransitionAxiom assumes totally-ordered atomic transitions; concurrent allocation discipline is appropriately listed as an open question rather than specified.

VERDICT: REVISE
