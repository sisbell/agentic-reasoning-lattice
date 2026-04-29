# Proof Verification: TumblerSub

Looking at the TumblerSub property section, I need to verify the definition and its three verification subsections (TA1/TA1-strict, TA3/TA3-strict, TA4).

**Definition of TumblerSub**: Correct, well-formed, formal contract matches narrative.

**TA1/TA1-strict verification**: Three cases on `k` vs `j = divergence(a,b)` are exhaustive (prefix divergence forces `k < j` since `k ≤ min(#a,#b) < j`). Each case correctly applies TumblerAdd's constructive definition and T1. The strict conclusion (Cases 2 and 3 iff `k ≥ j`) is sound.

**TA3 verification**: The inline derivation (†) — every zero tumbler is strictly less than every positive tumbler — is correct from T1 alone. Case 0 (proper prefix) with three sub-cases, Case 0a (component divergence + zero-padded equality), and Cases 1–3 (partitioned by `dₐ` vs `d_b`) are exhaustive. Case 2 impossibility argument is valid (`a ≥ w` contradicts `a_{dₐ} < w_{dₐ}`). The implicit claim that `d_b` is well-defined when `a` is not zero-padded-equal to `w` holds: if `b` were zero-padded-equal to `w`, then `a > w ≈ b` would force `a > b`, contradicting `a < b`.

**TA3-strict verification**: Correct — `#a = #b` eliminates Case 0 (proper prefix requires distinct lengths), and all remaining cases produce strict inequality.

**TA4 verification**: Both sub-cases (`aₖ > 0` and `aₖ = 0`) correctly reconstruct `a`. The "result-length identity" `#r = #w` follows directly from TumblerAdd's constructive definition when `k = #a = #w`.

**The problem is the formal contract.**

```
RESULT: FOUND

**Problem**: The formal contract placed after TA3-strict's proof does not capture TA3-strict. The contract states:

  *Preconditions:* a ∈ T, b ∈ T, w ∈ T, a < b, a ≥ w, b ≥ w
  *Postconditions:* a ⊖ w ≤ b ⊖ w

TA3-strict (a separately labeled **Claim** with its own proof) establishes `a ⊖ w < b ⊖ w` (strict) under the additional precondition `#a = #b`. The formal contract omits `#a = #b` from preconditions and uses `≤` instead of `<` in postconditions. Whether the contract is intended for TA3 (weak) or TA3-strict, there is a mismatch: if for TA3-strict, both the precondition and postcondition are wrong; if for TA3 (weak), then TA3-strict lacks its own formal contract entirely.

**Required**: Either (a) add a separate formal contract for TA3-strict:

  *Formal Contract:*
  - *Preconditions:* a ∈ T, b ∈ T, w ∈ T, a < b, a ≥ w, b ≥ w, #a = #b
  - *Postconditions:* a ⊖ w < b ⊖ w

or (b) reposition the existing contract immediately after TA3 (weak)'s proof and append TA3-strict's contract after TA3-strict's proof.
```
