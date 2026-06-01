# Review of ASN-0086

The note is mathematically sound across its load-bearing proofs — R0, R0a, L-ContiguousPrefix, R7a, R6d, and the two wp cases all check out under careful reading, including the boundary branches (first-emission vs. subsequent-emission, empty homed-set, self-nullification). The worked sketch's concrete tumblers (`a₁ = 1.0.1.0.1.0.2.1` etc.) recompute correctly against the K.λ chain. The findings below are accreted meta-prose around forward references (the classifier this note carries) plus one under-specified load-bearingness counterexample.

## REVISE

### Issue 1: PC-dropping counterexample (wp Case 1) presupposes a Σ' the witness does not guarantee
**ASN-0086, Weakest-Precondition Analysis, Case 1**: "Dropping PC admits the non-conforming nested link pair `a ≼ a''` ... Then P0 ∧ P1 holds, yet after Nullify `a''` persists by L12a and `{t : a ≼ t} ∩ A_rel^{Σ'} ⊇ {a, a''} ≠ {a}`."

**Problem**: The phrase "after Nullify" presupposes the operation produces a Σ'. `Nullify(Σ, d_retr, a)` runs only if its internal `Emit_R` is defined at `(Σ, d_retr)` — i.e., `d_retr`'s chain frontier is well-formed. In the NestedLinkWitness state the nesting sits at home `d` (the home of `a` and `a''`), whose apparent `ℓ_prev = a''` makes `inc(ℓ_prev, 0)` off-chain, so `Emit_R` at `d` is *undefined* (exactly the partiality the Emit_K Definition describes). If `dom(Σ.M) = {d}`, no admissible `d_retr` exists, no Σ' is produced, and the counterexample is vacuous rather than a postcondition failure. The argument silently needs a witness Σ carrying both the nested pair *and* a clean home for `d_retr`.

**Required**: State that the PC-dropping witness exhibits a Σ with the nested pair at home `d` together with a distinct clean document `d_retr ∈ dom(Σ.M)` at which `Emit_R` is defined; then the produced Σ' contains both `a` and the persisting `a''`, and the postcondition fails as claimed.

### Issue 2: Reduction-to-Emit_K corollary imagines composites the layer's own Definition excludes
**ASN-0086, Corollary (reduction to Emit_K), proof paragraph 2**: "R7a additionally covers composite extensions of the layer, whose `Σ.L`-effects decompose into K-steps for arbitrary `m`."

**Problem**: The relational layer's Definition states it "admits no composites that touch `Σ.L` indirectly." The corollary's subject is *this* layer's operations (`{Emit_K, Observe_K, Nullify}`), which by paragraph 1 reduce trivially at `m = 1`. Paragraph 2 then reasons about "composite extensions of the layer" — a case the layer's own definition rules out. This is essay content justifying R7a's generality lodged in a corollary whose claim does not depend on it; it advances no part of the reduction being proved.

**Required**: Delete paragraph 2, or relocate the "R7a is general for arbitrary `m`" observation to R7a itself. The corollary needs only paragraph 1.

### Issue 3: R7a Remark is a non-reliance disclaimer wrapping implementation trivia
**ASN-0086, Remark after R7a**: "*Remark (illustration only — not relied on by R7a or its consumers).* R7a is proved for arbitrary `m ≥ 1`, and R6d consumes the decomposition only as a finite K-step chain; neither uses any particular value of `m`."

**Problem**: The opening clause is a self-described non-reliance disclaimer ("illustration only — not relied on by R7a or its consumers"), and the body defends the lemma's `m`-genericity against an objection no one raised before reaching the udanax-green observation. This is the use-site/non-reliance framing pattern the anti-bloat directive flags. The implementation evidence (CREATELINK writes one link key, `m = 1`) is legitimate; the meta-framing around it is not.

**Required**: Keep the udanax-green observation as a plain implementation note; drop the "not relied on by R7a or its consumers" / "neither uses any particular value of `m`" defensive scaffolding.

## OUT_OF_SCOPE

### Topic 1: cardinality bound of `nullified(Σ)` relative to `dom(Σ.L)`
**Why out of scope**: Whether unbounded retraction is permitted or a structural ratio must hold (Open Question 6) is a new invariant question, not a defect in this note's active/audit construction.

### Topic 2: tightening L1b's `#E ≥ 2` to `#E = 2` at the substrate source
**Why out of scope**: L-ContiguousPrefix-Cor1 already derives `#E(a) = 2` for substrate-conforming states; whether to push the constraint into ASN-0043's admission rule (Open Question 7) is a foundation-level change, not a fix here.

VERDICT: REVISE
