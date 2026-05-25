# Review of ASN-0069

## REVISE

### Issue 1: `d²_new` symbol overloaded across V10, V11, and the worked example

**ASN-0069, V10**: "let `Σ¹ →* Σ²` be a later fork of the same `d_src` ... producing `d²_new`" — here `d²_new` is a *sibling* of `d¹_new`, both being forks of `d_src`.

**ASN-0069, V11**: "`d_src → d¹_new → d²_new → ... → d^k_new` where each step `dⁱ⁻¹_new → dⁱ_new` is a fork composite" — here `d²_new` is a *fork of `d¹_new`*, not of `d_src`.

**ASN-0069, Worked Example — Further forking**: "produces `d²_new = inc(d_new, 1)`" — chained fork (V11 sense).

**ASN-0069, Worked Example — Subsequent fork of d_src**: "the new fork is `d²_new = inc(d_new, 0)`" — sibling fork (V10 sense).

**Problem**: The same symbol denotes structurally distinct tumblers (different lengths, different parents in the allocator tree) depending on context. A reader cannot resolve `d²_new` without inferring intent.

**Required**: Introduce disambiguated notation — e.g., `dᵢ_chain` and `dᵢ_sib`, or `dⁱ_new` reserved exclusively for V11's chain and `d_new¹, d_new²` for V10's siblings.

### Issue 2: V7's empty-case composite lacks explicit ValidComposite★ verification

**ASN-0069, "The Fork Composite" verification section**: The verification walks through K.δ + K.μ⁺ + K.ρ × n for the non-empty case and concludes "The composite is a valid composite under ValidComposite★. ∎" The empty case (V7: K.δ alone) is described informally in V7's body but never has its ValidComposite★ status verified.

**Problem**: V7 asserts "the operation succeeds," which presupposes ValidComposite★. The K.δ precondition is the same as the non-empty case (covered), but the coupling constraints J0, J1★, J1'★ need to be verified for the K.δ-alone composite — they hold vacuously (ran(M'(d_new)) = ∅ makes J1★'s antecedent unsatisfiable, R' = R makes J1'★'s antecedent empty, dom(C') = dom(C) makes J0's antecedent empty), but the ASN does not state this.

**Required**: Add an explicit "K.δ-alone ValidComposite★ verification" paragraph parallel to the non-empty case, discharging the three coupling constraints vacuously.

### Issue 3: V8b's re-installation example glosses over I-address choice for intermediate positions

**ASN-0069, V8b**: "if K.μ⁻ on `d_src` retains only `{[s_C, 1, ..., 1, k] : 1 ≤ k ≤ 3}` and the operator wishes to restore the previously-removed position `[s_C, 1, ..., 1, 7]`, that restoration requires intermediate K.μ⁺ steps that first fill positions 4, 5, 6 — each step admissible only when its added position is the next contiguous one. Throughout these steps, the I-address `a ∈ dom(C)` remains permanently available by P0..."

**Problem**: The example focuses on the I-address at position 7 remaining available, but K.μ⁺ requires each new V-position to map to *some* I-address in `dom(C)` (by S3★). The example is silent on what I-addresses positions 4, 5, 6 must map to during the intermediate steps. The text says "the I-address `a`" as if there is one, but for positions 4, 5, 6 a different I-address (or several) must be supplied. Also, K.μ⁺ can add multiple positions in a single step, so "each step admissible only when its added position is the next contiguous one" describes one admissible discipline, not the only one.

**Required**: Clarify that intermediate restoration requires *some* valid I-address (possibly a different one than was previously at that position) for each filled V-position, and note that the per-step single-position framing is one of several admissible disciplines under K.μ⁺.

### Issue 4: V11a transitivity argument is single-step, but conclusion is over a chain

**ASN-0069, V11a**: The derivation establishes transitivity of `≼` for a single triple `(a, b, c)`, then concludes "the chain `d_src ≼ d¹_new ≼ ... ≼ d^k_new` follows by repeated application of transitivity."

**Problem**: "Repeated application" is an implicit induction on chain length `k`. For a single-triple transitivity to chain into an arbitrary-length chain requires a separate induction.

**Required**: State the chain conclusion as an induction on `k`: base `k = 1` is V2 directly; step `k → k+1` applies the single-triple transitivity to `d_src ≼ d^k_new` (IH) and `d^k_new ≼ d^{k+1}_new` (V2 at step k+1).

## OUT_OF_SCOPE

None.

VERDICT: REVISE
