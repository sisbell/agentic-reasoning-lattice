# Review of ASN-0115

## REVISE

### Issue 1: Subspace-confinement step omits T5 and misstates the interval

**ASN-0115, "What a spec-set is"**: "this forces `actionPoint(ℓ) ≥ 2`, so `s ⊕ ℓ` agrees with `s` on position 1 and the span's interval cannot cross the subspace boundary."
**ASN-0115, R10 parenthetical**: "`s ⊕ ℓ` agrees with `s` on position 1 = `s_C`, hence every `t < s ⊕ ℓ` has first component `s_C`."

**Problem**: The inference from "the two *endpoints* `s` and `s ⊕ ℓ` share position 1" to "*every interior* `t` shares position 1" is exactly ContiguousSubtrees (T5, ASN-0034) applied with prefix `p = [s₁]`: `p ≼ s`, `p ≼ s ⊕ ℓ`, and `s ≤ t ≤ s ⊕ ℓ` give `p ≼ t`. T5 is the load-bearing step that confines the denotation to one subspace and justifies the entire scope restriction, yet it is never named. Separately, "every `t < s ⊕ ℓ`" is literally false without the lower bound (any `t` below `s` is also `< s ⊕ ℓ`); the claim holds only for `t ∈ ⟦σ⟧`, i.e. `s ≤ t < s ⊕ ℓ`.

**Required**: Cite T5 explicitly for the endpoint-to-interior step, and restate the conclusion as "every `t ∈ ⟦σ⟧` has first component `s₁`."

### Issue 2: `#s ≥ 2` rests on S8a, which constrains only bound positions; "V-position of d" is undefined

**ASN-0115, "What a spec-set is"**: "Combined with level-uniformity (`#ℓ = #s`) and the V-position depth `#s ≥ 2` (ASN-0036, S8a) ... `σ = (s, ℓ)` whose start is a V-position of `d`."

**Problem**: The ordinal-level confinement needs `actionPoint(ℓ) = #ℓ = #s ≥ 2`; if `#s = 1` the action point is 1 and the interval crosses subspaces. The justification for `#s ≥ 2` is cited to S8a, but S8a (VPositionWellFormedness) is an invariant over *bound* positions `v ∈ dom(Σ.M(d))`. A span start need not be bound — R6 itself contemplates named positions absent from the arrangement. So whether the citation is valid depends on the undefined phrase "a V-position of `d`": if it means `s ∈ dom(Σ.M(d))` (active), S8a applies but then the start can never be one of R6's gaps, and that should be stated; if it means a well-formed V-position by shape, then `#s ≥ 2` follows from the V-position well-formedness shape requirement, not from S8a.

**Required**: Define "V-position of `d`" precisely. Either require the start to be active (and note the start is therefore never a silent gap), or derive `#s ≥ 2` from the V-position shape constraint (`zeros(s) = 0`, `#s ≥ 2`, positive components) rather than the domain-restricted S8a.

### Issue 3: R7's WLOG assumes comparability the theorem statement does not guarantee

**ASN-0115, R7**: "Let `Σ`, `Σ'` be any two states for which the consulted arrangement restrictions agree ... The states of a single docuverse are totally ordered (ASN-0047, SequentialTransitionAxiom), so without loss of generality `Σ` precedes `Σ'`."

**Problem**: SequentialTransitionAxiom totally orders the transitions of a *single execution*, making states *on that execution* comparable. The theorem quantifies over "any two states," which need not lie on a common trace; for such states the WLOG "`Σ` precedes `Σ'`" — and hence the appeal to S0/L12 over "intervening transitions" — is not licensed. The intended reading is two states of one evolving docuverse (the later being "asking again"), under which the proof is correct.

**Required**: Scope the hypothesis to states reachable from a common initial state along the sequential transition order, so the WLOG is discharged by the axiom rather than assumed.

## OUT_OF_SCOPE

### Topic 1: Inline provenance of delivered fragments
R9 deliberately asserts only resolution-traceability of origin, deferring whether origin travels inside the delivered material. This is correctly listed in Open Questions; no action needed in this ASN.

### Topic 2: Single-span subspace straddling
The behavior of a span whose denotation itself crosses `s_C`/`s_L` is excluded by the ordinal-level restriction and deferred. Appropriate scoping.

VERDICT: REVISE
