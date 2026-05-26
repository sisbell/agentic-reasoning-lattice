# Review of ASN-0076

## REVISE

### Issue 1: E4's proof omits formal discharge of the membership conditions

**ASN-0076, §The Supersession Relationship, E4**: The claim asserts:

```
(ℓ_old, δ(1, #ℓ_old)) ∈ Σ'.L(ℓ_sup).e₁
(ℓ_new, δ(1, #ℓ_new)) ∈ Σ'.L(ℓ_sup).e₂
(τ_sup,  δ(1, #τ_sup))  ∈ Σ'.L(ℓ_sup).e₃
```

The proof text reads: "By L13, the spans ... are well-formed references to the link entities at those addresses. By L4, endset spans may target any tumblers — including link I-addresses. By PrefixSpanCoverage, the canonical unit-depth span at `x` has coverage `{t : x ≼ t}`..."

**Problem**: This discusses well-formedness and coverage properties of the spans but never establishes that `Σ'.L(ℓ_sup).e_i = E_X`. The three explicit membership claims are not derived. L13/L4/PrefixSpanCoverage tell us spans are *valid endset constituents*, but the claim is about *what is actually stored* at slot e_i in the post-state. That step requires K.λ's effect plus L12, neither of which the proof invokes. The omission propagates: E7's proof opens with "By the construction of `Σ.L(ℓ_sup).e_1 = E_from = {(ℓ_old, δ(1, #ℓ_old))}`" — relying on a derivation E4 should have furnished.

**Required**: Explicit chain: (i) by K.λ's effect at the supersession step, `Σ_2.L(ℓ_sup) = (E_from, E_to, E_type)` where `Σ_2` is the post-state of the second K.λ; (ii) since EDITLINK's composite is exactly two K.λ steps, `Σ_2 = Σ'`, so `Σ'.L(ℓ_sup) = (E_from, E_to, E_type)` (L12 carries the value through trivially, since no further transition follows); (iii) by L6 (slot accessor), `Σ'.L(ℓ_sup).e_1 = E_from = {(ℓ_old, δ(1, #ℓ_old))}`; (iv) hence `(ℓ_old, δ(1, #ℓ_old)) ∈ Σ'.L(ℓ_sup).e_1`. Repeat for e_2 and e_3. The L13/L4/PrefixSpanCoverage discussion is correct *interpretation* of why these memberships matter, but it is not the discharge.

### Issue 2: Notational inconsistency in E7's proof

**ASN-0076, §E7 (LineageDiscoverability), proof**: "By the construction of `Σ.L(ℓ_sup).e_1 = E_from = {(ℓ_old, δ(1, #ℓ_old))}` and PrefixSpanCoverage (ASN-0043), `coverage({(ℓ_old, δ(1, #ℓ_old))}) ⊇ {ℓ_old}`, so `ℓ_old ∈ coverage(Σ'.L(ℓ_sup).e_1)`."

**Problem**: `ℓ_sup` is created during EDITLINK and is not in `dom(Σ.L)` (pre-state). Writing `Σ.L(ℓ_sup).e_1` is incorrect — `Σ.L(ℓ_sup)` is undefined at the pre-state. The line then jumps to `Σ'.L(ℓ_sup).e_1` without explanation. The asymmetric primes across one sentence are jarring; either both should be Σ' (with the equality justified via Issue 1's chain), or the construction reference should explicitly name the intermediate `Σ_2`.

**Required**: Replace `Σ.L(ℓ_sup).e_1 = E_from` with `Σ'.L(ℓ_sup).e_1 = E_from`, and cite E4 (once Issue 1 is fixed) for the equality, rather than appealing to "the construction." Same fix on the symmetric clause for `e_2`.

### Issue 3: "Step order" argument conflates definition and necessity

**ASN-0076, §E0**: "We must observe two things about the order. First, the successor step must precede the supersession step: only after `ℓ_new ∈ dom(L)` is the canonical unit-depth span `(ℓ_new, δ(1, #ℓ_new))` in `E_to` a reference to an existing link entity."

**Problem**: The wording "must precede" suggests a precondition-level constraint, but K.λ's preconditions on the second step do *not* require `ℓ_new ∈ dom(L)` — L4 explicitly admits endset spans to any tumbler in T, including those not in `dom(L)`. The order is fixed by the composite's *definition* (the sequential ordering of the two K.λ invocations), not by K.λ's preconditions. The semantic remark about "reference to an existing link entity" is a consequence, not the reason for the ordering.

**Required**: Rephrase to "The composite definition fixes the successor step first; the second step's endset construction reads the value of `ℓ_new` produced by the first step." Then preserve the semantic remark as an observation about why this ordering yields a coherent reference, not as a justification of the ordering itself.

## OUT_OF_SCOPE

None. The Open Questions section appropriately defers chains of supersession, retraction semantics, type-endset registry conventions, multi-way supersessions, and discovery operation semantics to future work.

VERDICT: REVISE
