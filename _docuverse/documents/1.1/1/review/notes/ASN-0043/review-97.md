# Review of ASN-0043

This note carries the `review-mode.anti-bloat` classifier, so I focus the review on meta-prose and duplication accreted around the forward-reference machinery, in addition to the standard correctness pass. The mathematics is sound: I traced the L1c producibility chains (including the L9 ghost construction and the L11b sibling-stream argument), the CPP/FSP discharge of state-local invariants, the worked-example transitions, and the T4-validity inductions, and found no correctness gaps. The findings below are all anti-bloat.

## REVISE

### Issue 1: "Home and Ownership" opening duplicates L11a
**ASN-0043, "Home and Ownership"**: "By GlobalUniqueness (ASN-0034), no two allocation events produce the same address. Link addresses are produced by allocation events conforming to T10a (L1c). Therefore each link receives a globally unique address."
**Problem**: This is L11a (LinkUniqueness) restated in different words. L11a says verbatim: "Distinct T10a-conforming allocation events produce distinct link addresses... This is GlobalUniqueness (ASN-0034) instantiated at link addresses: its sole precondition is T10a-conformance... and L1c... discharges precisely that." The reader who has read this paragraph reads it again as L11a; the reader who reaches L11a first reads it again here. This is the "two paragraphs in the same document say the same thing in different words" pattern. The same section also re-derives the cross-document `home(a₁) ≠ home(a₂)` result that the L11a/S7-analog material already carries.
**Required**: Collapse the prose into a single statement and point the GlobalUniqueness/uniqueness content to L11a (or vice versa). Keep only the part that advances the *ownership* argument (that `home(a)` fixes the owner), which is what the section is for.

### Issue 2: "Named accessor" carries well-definedness and interchangeability meta-prose
**ASN-0043, Convention — StandardTriple, *Named accessor***: "The side condition `|Σ.L(a)| ≥ 3` that makes the abbreviation well-defined is discharged for every conforming link by L3. The two forms are interchangeable in all formal statements."
**Problem**: An abbreviation definition does not need a sentence asserting its own well-definedness with a forward pointer to L3, nor a sentence declaring the two notations "interchangeable in all formal statements." This is essay content in a definitional slot — it explains *that the notation is safe to use* rather than advancing the definition's meaning. L8 then repeats the reminder ("the named accessor introduced above," "`.type` is slot 3, well-defined by L3").
**Required**: Reduce to the abbreviation itself (`Σ.L(a).type ≡ Σ.L(a).e₃`, conditional on arity ≥ 3). Drop the well-definedness and interchangeability sentences; L3 already establishes arity ≥ 3.

### Issue 3: FSP carries forward-pointer parentheticals and a "places no constraint" meta-sentence
**ASN-0043, FSP — FreshSiblingConformance**: "(L11a is discharged as a per-event distinctness obligation: the address `a` added by `Σ → Σ'` is distinct from every link address allocated in `Σ`, as the L11a bullet below shows.)" and "FSP places no constraint on the endset *targets* of `ℓ`; in particular `coverage(ℓ.type)` is unconstrained."
**Problem**: The first parenthetical forward-points to a bullet that appears a few lines later in the same proof ("as the L11a bullet below shows") — the reader must hold a promise that is immediately redeemed, which is pure navigation noise. The second sentence is meta-commentary about what the lemma *does not* assume; its only load-bearing use is at the L9/L11b call sites, where it can be stated where it matters.
**Required**: Delete the L11a forward-pointer parenthetical (the bullet stands on its own). Move the "unconstrained type targets" observation to L9, where the freedom is actually exercised, or drop it as derivable from the payload hypothesis.

### Issue 4: L1c's post-statement paragraph restates the formal predicate in prose
**ASN-0043, L1c**: "Each step is locally T10a-admissible: `kᵢ ∈ {0, 1, 2}` (the allowed T10a step types — `0` for sibling advance, `1` or `2` for child-spawn), and TA5a's side condition (ASN-0034) is discharged whenever `kᵢ = 2` by the explicit `zeros(tᵢ₋₁) ≤ 2` clause; for `kᵢ ∈ {0, 1}` TA5a is unconditional."
**Problem**: The formal *Chain* predicate already states `kᵢ ∈ {0, 1, 2}` and `(kᵢ = 2 ⟹ zeros(tᵢ₋₁) ≤ 2)`. This paragraph re-narrates those same two facts in prose and glosses the step types — explaining *what the predicate says* rather than advancing it. The genuinely new content here is only the half-sentence "The first step seats the field-separating zero at position `#s + 1`," which is concrete and should be kept.
**Required**: Trim to the seating observation; drop the restatement of the admissibility clauses already present in the formal predicate.

## OUT_OF_SCOPE

None. The Open Questions list correctly defers operations, transclusion consistency, compound-link well-formedness, and coverage-equivalence to future ASNs without making claims about them.

VERDICT: REVISE
