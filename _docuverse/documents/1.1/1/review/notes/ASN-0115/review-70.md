# Review of ASN-0115

## REVISE

### Issue 1: Deep-case emptiness argument applies Confinement beyond its stated form
**ASN-0115, §What a spec-set is — `act` override paragraph (deep case)**: "S8-depth then pins `#v = m_S(d) < m = #s`, while Confinement's agreement of `v` with `s` on positions `1 ≤ j < m` covers all `#v` of `v`'s own positions — so `v` is a proper prefix of `s`"
**Problem**: Confinement's stated postcondition is "`tⱼ = sⱼ` for `1 ≤ j < m`", which presupposes positions `1..m−1` exist on `t`; what the proof actually establishes is `p ≼ t`, which carries the unstated length bound `#t ≥ m − 1`. In the deep case `#v = m_S(d)` can be any value in `[2, m)`. When `m_S(d) = m − 1` the quoted inference works (`v = p ≺ s`). When `m_S(d) < m − 1` the agreement clause is not applicable to `v` at all — `v` lacks positions `m_S(d)+1 .. m−1` — and the actual contradiction is with the length bound `#v ≥ m − 1` implicit in `p ≼ v`, not with the prefix order. The argument as written discharges only one of the two sub-cases of a load-bearing claim (that the override is inert in the deep case).
**Required**: Record the length consequence in Confinement's postcondition (conclude `p ≼ t`, hence `#t ≥ m − 1` and `tⱼ = sⱼ` for `1 ≤ j < m`), then split the deep case explicitly: `m_S(d) < m − 1` contradicts `#v ≥ m − 1` outright; `m_S(d) = m − 1` gives `v = p ≺ s`, so `v < s` (T1 case (ii)), contradicting `v ≥ s`.

### Issue 2: R7 proof defends its hypothesis against a case the carrier excludes
**ASN-0115, §Repeatability**: "the two states are comparable under the sequential transition order, not merely reachable from a shared ancestor — divergent branches of the reachability relation would not be comparable, and across them a freshly allocated address could carry different values, so comparability is required, not derived."
**Problem**: This sentence does not advance the proof; it justifies the hypothesis. The proof needs exactly one fact from it — "The hypothesis gives `Σ →* Σ'` directly" — after which S0 applies along the path. The remainder imagines divergent branches of reachability, a case R7's own carrier ("two states of one evolving docuverse" under the standing precondition's sequential transition order, where transitions are totally ordered) already excludes; and the closing verdict "required, not derived" sits oddly against that axiom, under which comparability of two states of the one evolving docuverse *is* derived. This is the defensive-justification pattern: prose explaining why the hypothesis is needed rather than using it.
**Required**: Delete everything after "The hypothesis gives `Σ →* Σ'` directly". If branching histories are genuinely intended in the model, that conflicts with the standing precondition and must be reconciled there, not argued inside R7's proof.

### Issue 3: R11 wp paragraph states the same discharge twice in adjacent sentences
**ASN-0115, §What governs the material — wp paragraph**: "There is no independent store-membership conjunct to add. The active position is a content position … so generalized referential integrity discharges store membership directly — `Σ.M(d)(v) = a ⟹ a ∈ dom(Σ.C)` (S3★) — the instant (i) holds; immutability (S0) then holds `Σ.C(a)` fixed for all time." followed immediately by "The two facts are not two necessary preconditions to be conjoined but a *decomposition* of the one condition: (i) is the live reference the caller must establish, and `a ∈ dom(Σ.C)` is its automatic, permanent consequence (S3★ supplying membership, S0 supplying immutability)."
**Problem**: The second sentence restates the first — store membership is a consequence of (i) via S3★, held fixed by S0 — in different words, citing the same two invariants for the same two roles. It adds no new premise, case, or consequence; it reads as relocated rather than removed prose from a prior cycle.
**Required**: Keep one formulation (the S3★/S0 discharge) and delete the other.

### Issue 4: R8's no-deduplication point is made twice in one paragraph
**ASN-0115, §What co-delivery does with transclusion, final paragraph before the worked instance**: "This is forced abstractly — two distinct V-positions are two distinct entries, and a delivery that dropped one would violate R3 (it would silently omit a named, bound position)." and, two sentences later, "An alternative implementation is *required* to deliver both, by R3 — the absence of deduplication is not an implementation accident but a consequence of exactness."
**Problem**: Both sentences make the identical point — R3 forces delivery of both items — flanking the Gregory evidence. The first, being abstract, already covers every implementation, so the second's "alternative implementation" framing adds nothing beyond rhetoric ("not an implementation accident").
**Required**: State the R3-forces-both point once; the Gregory sentence can stand between the abstract claim and the worked instance without a second restatement.

### Issue 5: R2 uses an undefined projection `.val`
**ASN-0115, §Faithfulness, R2 box**: "`item(v, ρ, Σ).val = Σ.C(Σ.M(d)(v))`"
**Problem**: `item` is defined as a tagged pair (`⟨content, Σ.C(a)⟩` or `⟨ref, a⟩`); no projection `.val` is ever defined. This is the only formal equality in the document that uses it, and the claims table itself avoids it ("every content item equals `Σ.C(Σ.M(d)(v))`"). An undefined accessor inside a formal contract is a gap once this is carried to formalization.
**Required**: Either define the value projection on content-tagged items, or restate R2 as `item(v, ρ, Σ) = ⟨content, Σ.C(Σ.M(d)(v))⟩` for content positions.

## OUT_OF_SCOPE

### Topic 1: Caller-side distinguishability of empty-delivery causes
A delivery can be empty for three distinct reasons — depth-incompatible override, a genuinely unbound named region, or an empty subspace — and the ASN deliberately signals all three identically (structurally, by absence). Whether a result shape should let a caller discriminate these cases is an interface-design question.
**Why out of scope**: The ASN's structural-signalling stance is internally consistent and grounded in Nelson's drop-the-unsatisfiable-part rule; a richer result shape would be a new operation contract, not a fix to this one. It belongs with the existing open question on permitted failure modes.

VERDICT: REVISE
