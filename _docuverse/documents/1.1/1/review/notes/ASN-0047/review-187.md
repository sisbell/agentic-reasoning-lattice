# Review of ASN-0047

## REVISE

### Issue 1: P4a's "historical fidelity" framing overclaims relative to what the discharge establishes

**ASN-0047, P4a (Historical fidelity) and its Class (b) discharge**: P4a is stated as "every entry in R reflects an actual *past* content-subspace containment event," formally `(E Σ_k in the transition history : (E v ∈ dom(M_k(d)) : subspace(v) = s_C ∧ M_k(d)(v) = a))`. The discharge says: "for `(a, d) ∈ R' \ R`, J1'★ supplies `v ∈ dom(M'(d))` ... so Σ' itself witnesses."

**Problem**: ValidComposite★ does not constrain the order of K.ρ and the matching K.μ⁺. In the order `K.α → K.ρ → K.μ⁺` (which satisfies every elementary precondition — the ASN itself notes "orderings such as K.α → K.ρ → K.μ⁺ satisfy every elementary precondition"), K.μ⁺ is the last step, so at Σ' the witnessing mapping exists *only in the present state Σ'*; no strictly-earlier state ever carried it. The discharge therefore must admit Σ' (the present) as `Σ_k`, which it does. But then the property does not capture "past" containment at all — it is satisfiable by present containment alone. The word "past," and the name "Historical fidelity," assert more than the formal statement (∃ state in history, present included) and the discharge actually deliver.

**Required**: Either (a) rename/restate P4a to "every R-entry has a content-subspace witness at the composite boundary at which it was recorded" (dropping the "past"/"historical" framing), or (b) if genuine historical fidelity is intended, strengthen J1'★/ValidComposite★ to require the matching K.μ⁺ to precede the K.ρ, so a strictly-earlier witnessing state exists, and update the discharge to name that state rather than Σ'.

### Issue 2: Repeated "caller-checked guard, not a conclusion" justification restated across K.δ sub-cases and the discharge section

**ASN-0047, K.δ case (ii) and §*K.δ case (ii) discharge and parent-allocator activation***: The point that the freshness conjunct `e ∉ E` "is a *caller-checked guard*, observed before the event fires — it is a precondition, not a conclusion" is stated in the K.δ case-(ii) preamble, then re-stated for k=0 ("the operational frontier check"), for k=1 ("The caller-checked guard `e ∉ E` is the operational precondition here"), for k=2 ("The caller-checked guard `e ∉ E` is the operational precondition"), and again in the discharge section ("In each, `e ∉ E` is the caller-checked guard; GlobalUniqueness ... preserves the distinctness invariant that always applying the guard maintains, rather than supplying the guard itself").

**Problem**: This is the same meta-claim ("the guard is a precondition, distinctness is preserved by GlobalUniqueness thereafter") rendered four-plus times in different words. It does not advance the per-sub-case reasoning, which differs only in *which allocator* the step acts on and *which discipline clause* (direct per-`(t,k')` uniqueness vs. derived FrontierEquivalence) applies.

**Required**: State the guard-vs-conclusion distinction and the GlobalUniqueness-preserves-distinctness fact once (in the discharge-section preamble), and let each sub-case carry only its distinguishing content (operand, parent allocator, discipline clause).

### Issue 3: K.μ⁺'s definition enumerates a downstream consumer (K.μ~) inside its own body

**ASN-0047, K.μ⁺ (Arrangement extension)**: "The K.μ~ decomposition (replacement as K.μ⁻ then K.μ⁺) relies on this disjointness: the K.μ⁻ step empties the affected positions from dom, and the subsequent K.μ⁺ step adds mappings at positions that — having been removed — are now disjoint from the intermediate domain."

**Problem**: This sentence advances the meaning of K.μ~, not of K.μ⁺. A definition's body enumerating where its property is later consumed is accretion — the disjointness fact itself is the K.μ⁺ content; the K.μ~ relevance belongs at the K.μ~ decomposition, which already re-derives the disjointness it needs.

**Required**: Delete the K.μ~ use-site sentence from the K.μ⁺ definition; the disjointness consequence stands on its own.

### Issue 4: Empty forward-pointers conveying no content

**ASN-0047, end of *Amendments to existing transitions***: "The discharge of J4 (Fork) under the amended K.μ⁺ is given in *Coupling and isolation* below alongside J4's definition."

**Problem**: This sentence carries no claim — it only announces that content appears elsewhere. The same pattern recurs (e.g., K.δ's "§*K.δ case (ii) discharge ... below records, in one place, ...*; that analysis is not re-derived here"). A reader gains nothing at the pointer site; the deferral is bookkeeping.

**Required**: Remove standalone pointer sentences. Where a cross-reference genuinely aids navigation, fold it into the sentence that makes a claim (e.g., "J4 is discharged under the amended K.μ⁺ (§Coupling and isolation)") rather than as its own statement.

### Issue 5: K.μ⁻ "Three-case partition" includes an exhaustiveness clause discharging a precondition-excluded case

**ASN-0047, K.μ⁻ amendment, *Three-case partition by pre-state subspace populations***: "The K.μ⁻ precondition `dom(M(d)) ≠ ∅` excludes the fourth case (`V_{s_C}(d) = V_{s_L}(d) = ∅`); the remaining three cases each force the contraction at a determinate subspace".

**Problem**: The partition's substantive content (which subspace must shrink) is already determined by the constructive retention-count precondition plus the strict-contraction clause. The explicit naming-and-excluding of a fourth case the precondition already rules out is exhaustiveness bookkeeping that the constructive specification renders redundant.

**Required**: Drop the fourth-case exclusion clause; if the locus-of-contraction observation is worth keeping, state it as a one-line consequence of the strict-contraction clause rather than as a four-way case enumeration.

## OUT_OF_SCOPE

None — the Open Questions section already correctly defers link inheritance under forking, interior link withdrawal/tombstoning, concurrency/serialization, and address-space exhaustion to future ASNs.

VERDICT: REVISE
