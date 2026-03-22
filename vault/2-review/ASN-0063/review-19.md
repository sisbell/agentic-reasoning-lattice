# Review of ASN-0063

## REVISE

### Issue 1: J4 (Fork) compatibility with D-CTG/D-MIN amendment is not verified

**ASN-0063, Extending the Transition Framework**: "We verify that J4 remains a valid composite under the amended coupling constraints."

**Problem**: The verification covers J1★ and J1'★ but omits the D-CTG/D-MIN postcondition added to K.μ⁺ by the amendment. J4's K.μ⁺ step must produce M'(d\_new) satisfying D-CTG and D-MIN for each subspace. The claim "J4 remains a valid composite" is incomplete without this.

**Required**: State that J4's K.μ⁺ step operates on a freshly created document (M(d\_new) = ∅ after K.δ), so the K.μ⁺ step constructs the entire content-subspace arrangement. By choosing V-positions contiguously from the minimum [s\_C, 1, ..., 1], D-CTG and D-MIN are satisfied. The link subspace of d\_new is empty (J4's K.μ⁺ is content-subspace-only by the amendment), so D-CTG and D-MIN hold vacuously for it. This is a one-sentence addition to the J4 paragraph.

### Issue 2: K.μ~ decomposition validity under D-CTG/D-MIN amendment is not established

**ASN-0063, ExtendedReachableStateInvariants proof, K.μ~ case**: "D-CTG and D-MIN hold for M'(d): K.μ⁺ (amended) requires M'(d) to satisfy D-CTG and D-MIN as a postcondition — these hold directly, not derived from D-SEQ."

**Problem**: This addresses the output state only. K.μ~ is a distinguished composite K.μ⁻ + K.μ⁺. The K.μ⁻ step must produce an intermediate state satisfying D-CTG and D-MIN (by the K.μ⁻ amendment introduced in this ASN). The proof does not verify this intermediate state, nor does it show that a valid decomposition exists for every K.μ~.

The fixity analysis proves that link-subspace positions are unchanged at the output (r = 0). This implies K.μ⁻ removes only content-subspace positions. But the fixity derivation uses S3★ at the output — it does not directly constrain the K.μ⁻ step. The gap is: the proof must show that the K.μ⁻ step within K.μ~ can always be chosen to satisfy the D-CTG/D-MIN amendment.

**Required**: Add an explicit existence argument. Since link-subspace fixity shows r = 0, K.μ⁻ within K.μ~ removes only content-subspace positions. By D-SEQ at the input, content-subspace positions form {[s\_C, 1, ..., 1, k] : 1 ≤ k ≤ n}. K.μ⁻ can remove a suffix of this range (or all positions), leaving {[s\_C, 1, ..., 1, k] : 1 ≤ k ≤ n'} for some 0 ≤ n' ≤ n, which satisfies D-CTG and D-MIN. The link subspace at the intermediate state equals the input (r = 0), preserving D-CTG/D-MIN. K.μ⁺ then rebuilds the content subspace from n' + 1 to n with new mappings, satisfying D-CTG/D-MIN at the output. For any bijection π, the decomposition with n' = 0 (remove all content-subspace positions, then re-add with new mappings) is always valid.

## OUT_OF_SCOPE

### Topic 1: ASN-0036 S8a commentary inconsistency with s\_L > 0
**Why out of scope**: ASN-0036 S8a's commentary states "The range guard v₁ ≥ 1 excludes link-subspace V-positions (where v₁ = 0)." This ASN correctly derives s\_L > 0 from L1 + T4, meaning link-subspace V-positions have v₁ = s\_L ≥ 1 and fall within S8a's quantifier scope. The formal statement of S8a is correct and this ASN handles it correctly — the commentary inaccuracy is in ASN-0036, not here.

### Topic 2: Link withdrawal mechanism
**Why out of scope**: The ASN identifies the tension between D-CTG (preventing interior removal) and link-subspace fixity under K.μ~ (preventing gap closure via reordering), and correctly defers the withdrawal mechanism to the open questions. The analysis of which K.μ⁻ applications are valid for the link subspace (maximum-end removal only, or total removal) is sufficient for this ASN's scope.

### Topic 3: Ownership-gated transitions
**Why out of scope**: The ASN notes that "owner-only modification" is design intent not yet formalized in the transition framework. This is future work — K.α, K.μ⁺, and other transitions constrain structural validity but do not gate on ownership. The formal guarantees in this ASN (CL4, CL5, CL6) do not depend on ownership formalization.

VERDICT: REVISE
