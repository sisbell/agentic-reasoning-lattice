# Review of ASN-0115

## REVISE

### Issue 1: V-spec definition admits subspace-straddling spans, contradicting R10
**ASN-0115, "What a spec-set is" / R10**: The V-spec definition requires only "a well-formed level-uniform span `σ`," while R10 asserts delivery "works with" only "the ordinal, deepest-action-point spans" and concludes "a text-rooted span cannot reach link positions, since `s ⊕ ℓ` agrees with `s` on position 1."

**Problem**: Level-uniform (ASN-0053 S6) means only `#s = #ℓ`; well-formed (T12) means only `actionPoint(ℓ) ≤ #s`. Neither forces `actionPoint(ℓ) = #ℓ` (the ordinal/deepest-action-point condition, ASN-0082 OrdinalLevel). A level-uniform well-formed span with `actionPoint(ℓ) = 1` does **not** preserve position 1. Concretely, `s = [1,5]` (subspace `s_C`), `ℓ = [2,0]` (Pos, actionPoint = 1, `#ℓ = #s = 2`): `s ⊕ ℓ = [3,0]`, so `⟦σ⟧ = {t : [1,5] ≤ t < [3,0]}` contains `[2,3]`, a depth-2 position with `subspace = s_L`. A single V-spec span therefore *can* straddle from the text subspace into the link subspace — exactly the case R10's parenthetical claims is excluded and which the ASN explicitly defers to Open Questions. R10's justification ("`s ⊕ ℓ` agrees with `s` on position 1") holds only when `actionPoint(ℓ) ≥ 2`, which the definition does not guarantee.

**Required**: Tighten the V-spec definition to require ordinal-level spans (`actionPoint(ℓ) = #ℓ`, per ASN-0082 OrdinalLevel), so that R10's reasoning is sound and single-span straddling is genuinely outside this ASN; or, if general level-uniform spans are intended, withdraw R10's exclusion claim and confront the straddling case here rather than deferring it.

### Issue 2: R7 proof invokes store monotonicity for two states it treats as unordered
**ASN-0115, R7 (Repeatability)**: "Let `Σ`, `Σ'` be any two states for which the consulted arrangement restrictions agree … The stores can only *grow* and never alter an existing entry (S0 for content, L12 for links), so for every resolved address the delivered value or reference is the same at both states."

**Problem**: S0/S1 and L12 are *per-transition* monotonicity/immutability invariants — they license `dom(Σ.C) ⊆ dom(Σ'.C)` and value-equality only when `Σ` precedes `Σ'`. R7 quantifies symmetrically over "any two states," yet the proof asserts "the stores can only grow" without establishing a direction between `Σ` and `Σ'`. For two states not known to be reachability-ordered, "grow" is undefined, and the step that resolved address `a` has `Σ.C(a) = Σ'.C(a)` is not discharged.

**Required**: Either invoke the total ordering of states (ASN-0047 SequentialTransitionAxiom) to pick a direction WLOG, then apply S0/S1/L12; or argue from global content immutability directly (any `a` in both `dom(Σ.C)` and `dom(Σ'.C)` carries one fixed value), citing that `a ∈ dom(Σ.C)` and `a ∈ dom(Σ'.C)` follow from S3★ at each state. As written the monotonicity appeal does not cover the symmetric statement.

## OUT_OF_SCOPE

### Topic 1: Reading a delivered link's endset structure
**Why out of scope**: R10 delivers a link position as a reference to the link address, explicitly not the endset structure; reading link structure by address is READLINK/FOLLOWLINK (ASN-0111/0114), correctly deferred.

### Topic 2: Single-span subspace straddling and inline provenance
**Why out of scope**: Both are listed in Open Questions and are genuinely new territory beyond resolve-then-deliver. (Note this is contingent on Issue 1 being fixed by restricting to ordinal spans; otherwise straddling is in scope for *this* ASN's spans.)

VERDICT: REVISE
