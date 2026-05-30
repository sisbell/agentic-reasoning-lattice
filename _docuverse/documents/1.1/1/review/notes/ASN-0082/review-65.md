# Review of ASN-0082

## REVISE

### Issue 1: Commutativity and associativity of ℕ addition are cited from T0, but no foundation axiom supplies them

**ASN-0082, "Span Width Preservation" (preamble) and Statement Registry ("ℕ comm/assoc")**: "Commutativity and associativity of ℕ addition are standard arithmetic facts about the carrier ℕ, cited from T0 (CarrierSetDefinition, ASN-0034) … we use, for all m, n, k ∈ ℕ, `m + n = n + m` (commutativity) and `(m + n) + k = m + (n + k)` (associativity)."

**Problem**: T0's axiom is purely the carrier/length/projection definition (`T` is finite sequences over ℕ with `#·` and `·ᵢ`); it states no arithmetic law. The foundation deliberately separates ℕ facts into named axioms — NAT-addcompat (order-compatibility + strict successor), NAT-closure (closure + additive identity), NAT-discrete, NAT-order, NAT-wellorder — and **none of these states commutativity or associativity of `+`**. The commutativity step is load-bearing in I3-S(a) ("n + ℓₘ = ℓₘ + n … by commutativity of ℕ addition") and the regrouping step in D-S(a) ("regrouping by commutativity and associativity"). Citing "T0's carrier ℕ" names a premise the cited dependency does not provide. The sentence "These are properties of the substrate carrier, not of system state, so they are cited as foundation facts rather than posited as a fresh universal axiom here" is defensive meta-prose that papers over the missing citation rather than discharging it.

**Required**: Cite the specific foundation axiom that supplies ℕ commutativity/associativity. If ASN-0034's NAT-* extraction does not include them (it does not, as listed), the dependency cannot be discharged as written — either the foundation must extract a NAT-comm / NAT-assoc axiom and the ASN cite it, or I3-S(a) and D-S(a) must route the identity through an available law (D-S(a) already demonstrates this is possible for subtraction via ReverseInverse + TA4; the addition-commutativity step in I3-S has no such fallback shown).

### Issue 2: D-SEP(b) Case 2 builds a superfluous D-CTG bracket argument for a fact D-SEQ supplies in one line

**ASN-0082, D-SEP proof of (b), Case 2**: "We establish r ∈ V_1(d) via D-CTG, using the last element of X as the lower bracket. First, X is non-empty … Fourth, applying D-CTG … D-CTG gives r ∈ V_1(d)."

**Problem**: The contraction operates under the precondition that D-SEQ holds on the pre-state, giving `V_1(d) = {[1, k] : 1 ≤ k ≤ N}`. `R ≠ ∅` directly supplies some `[1, k] ∈ V_1(d)` with `k ≥ p₂ + c`, hence `p₂ + c ≤ N`, hence `r = [1, p₂ + c] ∈ V_1(d)` immediately. The entire Case 1 / Case 2 split, the X-non-emptiness derivation, the "last element of X" construction, and the D-CTG invocation are unnecessary machinery for a one-step consequence of a precondition already in force. This is the over-engineered-proof pattern the active anti-bloat classifier asks to surface: a multi-paragraph case argument standing in for a direct appeal.

**Required**: Replace the Case 1/Case 2 D-CTG argument with the direct D-SEQ derivation of `r ∈ V_1(d)` from `R ≠ ∅` and the containment precondition.

### Issue 3: I3-VP wp conjunct 2 over-cites NAT-addcompat for a left-monotone step it does not license

**ASN-0082, "Weakest-precondition analysis (I3-VP …)", conjunct 2**: "Since `n ≥ 1` … and `vₘ ≥ 1` …, `vₘ + n ≥ 1 + 1 = 2 > 0` by NAT-addcompat (ASN-0034)."

**Problem**: NAT-addcompat's order-compatibility is `n ≥ p ⟹ m + n ≥ m + p` — monotonicity in the **right** operand with the left fixed. Deriving `vₘ + n ≥ 1 + 1` requires varying the **left** operand (`vₘ` vs `1`), which needs either commutativity (see Issue 1) or a left-monotonicity law, neither available. The obligation `vₘ + n > 0` is trivially met (`n ≥ 1`, closure), so the inflated `≥ 1 + 1 = 2` chain both over-claims and silently reuses the missing commutativity.

**Required**: Discharge `vₘ + n > 0` from `n ≥ 1` and closure/identity alone, or supply the law that licenses the left-operand comparison.

## OUT_OF_SCOPE

### Topic 1: Generalization of contraction to ordinal depth > 1
**Why out of scope**: The depth scoping axiom `#p = 2` confines contraction to single-component ordinals, and the Open Questions already record the TA4-vs-S8a collision at intermediate components. The deeper-ordinal gap-closure law is genuinely new territory, not a defect of this ASN.

### Topic 2: The content-placement sub-operation of INSERT
**Why out of scope**: I3 is explicitly the shift sub-operation only; allocation and placement of the inserted bytes (and the re-validation of D-CTG/D-MIN/D-SEQ once content fills the gap) belong to a separate operation ASN.

VERDICT: REVISE
