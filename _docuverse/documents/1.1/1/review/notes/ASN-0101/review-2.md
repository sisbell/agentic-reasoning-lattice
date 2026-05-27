# Review of ASN-0101

## REVISE

### Issue 1: σ_d formula yields the wrong result for depths m_S ≥ 3

**ASN-0101, D0 Effect**: "The shift function `σ_d(v) := vpos(S, ord(v) ⊖ δ(n, m_S)_{ord})` — equivalently, `σ_d(v)` decrements `v`'s last component by `n` while leaving earlier components unchanged"

**Problem**: The "equivalently" claim is false for m_S ≥ 3. By TumblerSub (ASN-0034), `a ⊖ w` uses `k = zpd(a, w)`: `r_i = 0` for `i < k`, `r_k = a_k − w_k`, `r_i = a_i` for `i > k`. For `v ∈ R` with form `[S, 1, ..., 1, k]` at depth m_S = 3:
- `ord(v) = [1, k]` (length 2)
- `δ(n, m_S)_{ord} = [0, n]` (length 2)
- `zpd([1, k], [0, n]) = 1` because position 1 differs (1 ≠ 0)
- Therefore `[1, k] ⊖ [0, n] = [1 − 0, k] = [1, k]` (position 2 copies from `a`, not subtracted)
- So `σ_d(v) = vpos(S, [1, k]) = [S, 1, k] = v` — **σ_d acts as the identity**.

This generalises: at any m_S ≥ 3, `ord(v)` begins with `1` while `δ(n, m_S)_{ord}` begins with `0`, forcing `zpd = 1` and leaving the last component untouched. The formula only works at the depth m_S = 2 inherited from ASN-0082.

**Required**: Replace the σ_d definition with one that correctly decrements the last component. Direct definition `σ_d([S, c_2, ..., c_{m_S-1}, k]) = [S, c_2, ..., c_{m_S-1}, k − n]` works. An implicit definition via TumblerAdd — `σ_d(v)` is the unique tumbler `a` such that `a ⊕ δ(n, m_S) = v`, well-defined under D-SEQ★ form by right-cancellation on equal-length operands — also works. The current formula does not.

### Issue 2: Worked example computation is wrong

**ASN-0101, "A worked example"**: "`[1, 4] ⊖ [0, 2] = [1, 2]    (the zero-prefix-up-to-divergence rule of TumblerSub)`"

**Problem**: By TumblerSub, `[1, 4] ⊖ [0, 2] = [1, 4]`, not `[1, 2]`. `zpd([1, 4], [0, 2]) = 1` because `1 ≠ 0` at position 1; then `r_1 = 1 − 0 = 1` and `r_2 = a_2 = 4`. The author asserts the intended result `[1, 2]` but cites a derivation that does not produce it. The "zero-prefix-up-to-divergence" phrase mis-describes TumblerSub: the prefix is zeroed only at positions *strictly before* `zpd`, and `zpd` is the *first* divergence — which here is position 1, not position 2.

**Required**: Either fix the formula (Issue 1) so the computation goes through, or replace the example with a depth-2 case (m_S = 2) where the existing formula succeeds.

### Issue 3: D1 "post-state characterisation" is asserted, not derived

**ASN-0101, D1 Justification**: "each σ_d(v') with v' = [S, 1, ..., 1, k'] and p + n ≤ k' ≤ n_S maps to [S, 1, ..., 1, k' − n] with p ≤ k' − n ≤ n_S − n."

**Problem**: This is the load-bearing step of D1 — the claim that σ_d closes the gap by mapping `R` onto `{[S, 1, ..., 1, j] : p ≤ j ≤ n_S − n}`. It is asserted without showing the TumblerSub computation. The computation does not produce the claimed result (Issue 1). The order-preservation paragraph that precedes this step only proves σ_d(v_1) < σ_d(v_2), not the structural form of σ_d(v). Order preservation alone is consistent with σ_d being the identity, which is what the formula in fact yields.

**Required**: Once the formula is corrected (Issue 1), derive the structural form explicitly — naming each component of σ_d(v) and showing why earlier components remain `1` and the last decrements by n.

### Issue 4: D8's D-CTG★ preservation fails under the current formula

**ASN-0101, D8, Group (i) Justification**: "By D1, V_S(M'(d)) has the stated form, so D-CTG★, D-MIN★, D-SEQ★ hold..."

**Problem**: Under the formula as written, the post-state `V_S(M'(d)) = L ∪ R` (since σ_d is identity at m_S ≥ 3), which is the contiguous prefix `{[S, 1, ..., 1, k] : 1 ≤ k ≤ p − 1}` together with the suffix `{[S, 1, ..., 1, k] : p + n ≤ k ≤ n_S}` — with a gap at positions `p, p+1, ..., p+n−1`. D-CTG★ fails on this gap, D-MIN★ holds (min is still `[S, 1, ..., 1]` when L ≠ ∅), and D-SEQ★ fails (the set is not `{[S, 1, ..., 1, k] : 1 ≤ k ≤ n_S − n}`). So D8 itself fails on subspace S whenever m_S ≥ 3.

**Required**: D8 holds correctly only once σ_d is correctly defined.

### Issue 5: "What shifts" narrative repeats the computation error

**ASN-0101, "What shifts: closing the gap"**: "The subtraction `ord(v) ⊖ δ(n, m_S)_{ord}` zeros the components where `ord(v)` and the displacement agree, reverses at the divergence (the last component), and gives `[1, ..., 1, k − n]`."

**Problem**: The divergence between `ord(v) = [1, ..., 1, k]` and `δ(n, m_S)_{ord} = [0, ..., 0, n]` is at the *first* position, not the last. TumblerSub does not "zero the components where they agree" — it zeros positions strictly before `zpd`, then computes `r_zpd = a_zpd − w_zpd`, then copies `a`. The narrative description does not match the TumblerSub specification.

**Required**: Rewrite the prose to match the corrected formula.

### Issue 6: D-MIN★ derivation in "Deletion at the start" boundary case is unjustified

**ASN-0101, "Boundary cases" / "Deletion at the start"**: "Computing σ_d(r): ord(r) = [1, ..., 1, n + 1], δ(n, m_S)_{ord} = [0, ..., 0, n], ord(r) ⊖ δ(n, m_S)_{ord} = [1, ..., 1, 1] (the divergence falls at the last position, yielding n + 1 − n = 1)"

**Problem**: For m_S ≥ 3, the divergence does *not* fall at the last position — it falls at position 1 (the leading `1` in `ord(r)` versus the leading `0` in `δ_ord`). TumblerSub gives `[1, ..., 1, n+1]`, not `[1, ..., 1, 1]`. The parenthetical "yielding n + 1 − n = 1" misidentifies which position is being subtracted. D-MIN★ preservation in this case rests on the same error as Issue 1.

**Required**: Same fix as Issue 1; then revise this boundary verification to follow correctly.

### Issue 7: Worked example's "Verification of D8" mis-states V_1(M'(d))

**ASN-0101, "A worked example"**: "Verification of D8. ... D-CTG★, D-MIN★, D-SEQ★ hold: the post-state is the contiguous prefix of depth-3 positions in subspace 1 starting at [1, 1, 1], with maximum [1, 1, 2]."

**Problem**: Under the formula as stated, the post-state `V_1(M'(d)) = L ∪ Q = {[1, 1, 1]} ∪ {[1, 1, 4]} = {[1, 1, 1], [1, 1, 4]}` — *not* `{[1, 1, 1], [1, 1, 2]}`. So D-CTG★ would fail. The worked example asserts the intended (correct) outcome but the cited operations do not produce it.

**Required**: Fix the formula (Issue 1) so the computation actually produces `{[1, 1, 1], [1, 1, 2]}`.

### Issue 8: Atomicity argument against K.μ⁻ ∘ K.μ~ is hand-waved

**ASN-0101, "The operation"**: "It is *not* a derived composite of `K.μ⁻` (suffix truncation) and `K.μ~` (reordering); composing those would either fail D5 (the reordering would have to be admissible under a stricter invariant) or require an intermediate state that violates S2 or D-CTG★."

**Problem**: "D5" appears here to refer to something other than the cross-document isolation D5 introduced later — there is no prior referent for "D5" at this point. The "fail D5" wording also makes no sense as written: K.μ⁻ acts on a single document, so cross-document isolation is trivially preserved. The intended argument is presumably that K.μ⁻ cannot remove an *interior* span (it only contracts a suffix per its formal contract in ASN-0047) and that K.μ~ on the truncated arrangement cannot fill the resulting hole without violating D-CTG★/D-SEQ★. State this argument directly.

**Required**: Replace the ambiguous "D5" reference with an explicit citation, and lay out which case (interior deletion vs. suffix) and which invariant each decomposition path violates.

### Issue 9: ValidComposite★ admissibility is asserted but not formally extended

**ASN-0101, "The operation"**: "DEL contributes a single elementary transition to any ValidComposite★ chain in which it appears..."

**Problem**: ASN-0047's ValidComposite★ enumerates the admissible elementary transitions as `{K.α, K.δ, K.λ, K.μ⁺, K.μ⁺_L, K.μ⁻, K.μ~, K.ρ}`. Adding DEL requires extending that enumeration — but the ASN gives no formal statement of the extension, only a prose claim. The vacuity of J0/J1★/J1'★ at a DEL step is argued informally; the actual structural statement "ValidComposite★ admits DEL as an elementary transition with coupling constraints J0, J1★, J1'★ holding vacuously" should be a named claim that downstream ASNs can cite.

**Required**: Add a named claim (e.g., D-CC) recording the extension of ValidComposite★ and the vacuity argument. Without it, downstream ASNs cannot cleanly invoke "DEL in a ValidComposite★ chain".

### Issue 10: Recoverability section makes an unsupported claim about versioning behavior

**ASN-0101, "A note on recoverability"**: "A version is, in the working framework, a separately addressed document — `inc(d, 1)`, in the K.δ vocabulary — whose arrangement is set up to match `d`'s arrangement at a particular point in time."

**Problem**: ASN-0047's K.δ case (ii) sub-case `k = 1` allocates `inc(t, k)` with `t = d_src` and `parent(e) ∈ E` — but the K.δ effect for IsDocument explicitly sets `M'(e) = ∅`, not `M'(e) = M(d_src)`. The "arrangement set up to match" claim is the responsibility of a separate composite (the J4 ForkComposite of ASN-0047), not K.δ alone. The current prose conflates them.

**Required**: Either cite J4 (ForkComposite) explicitly as the mechanism that populates the new version's arrangement, or rephrase to acknowledge that "versioning" in the broader sense is a multi-step composite outside DEL's scope.

## OUT_OF_SCOPE

(No additional out-of-scope topics beyond those already declared by the prompt — INSERT, COPY, REARRANGE, link semantics, version creation, BEBE.)

VERDICT: REVISE
