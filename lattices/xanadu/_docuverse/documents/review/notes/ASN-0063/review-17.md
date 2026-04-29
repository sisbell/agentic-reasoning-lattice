# Review of ASN-0063

## REVISE

### Issue 1: K.μ⁻ amendment not formalized
**ASN-0063, Extending the Transition Framework**: "K.μ⁻ (ASN-0047), when applied in the extended state, must likewise produce M'(d) satisfying D-CTG and D-MIN"
**Problem**: K.μ⁺ receives an explicit, clearly delineated amendment (content-subspace restriction + D-CTG/D-MIN postcondition), recorded in the Properties table as "K.μ⁺ amendment." K.μ⁻ receives only this single sentence — not structured as a formal amendment, not entered in the Properties table, and not restated at the point of use. Yet the ExtendedReachableStateInvariants proof later says "D-CTG, D-MIN preserved by the postcondition requirement" for K.μ⁻, citing a requirement that was never formally established. K.μ⁻ from ASN-0047 permits arbitrary contraction of dom(M(d)) — removing an interior V-position breaks D-CTG, and removing the minimum breaks D-MIN. Without an explicit postcondition amendment, K.μ⁻ does not preserve D-CTG or D-MIN, and the inductive step of ExtendedReachableStateInvariants fails for the K.μ⁻ case.
**Required**: State the K.μ⁻ amendment with the same precision as K.μ⁺'s. Add it to the Properties table. The amendment restricts K.μ⁻'s effect: M'(d) must satisfy D-CTG and D-MIN for each subspace. State the consequence — by D-SEQ at the *input* state, this constrains contraction to removal from the maximum end of V_S(d) or removal of all positions in V_S(d).

### Issue 2: K.μ~ D-CTG/D-MIN argument is circular
**ASN-0063, ExtendedReachableStateInvariants proof**: "D-SEQ at equal cardinality yields V_S(d') = V_S(d), so D-CTG and D-MIN hold"
**Problem**: D-SEQ is derived from D-CTG ∧ D-MIN ∧ S8-fin ∧ S8-depth (ASN-0036). Applying D-SEQ at the output state Σ' presupposes D-CTG and D-MIN hold there — which is the conclusion being established. The argument is circular. The bijection π and equal cardinality are insufficient without independently establishing D-CTG and D-MIN for M'(d). Consider: π could map V_{s_C}(d) = {[s_C, 1], [s_C, 2], [s_C, 3]} to {[s_C, 2], [s_C, 3], [s_C, 4]} — satisfying S8a, S8-depth, and S8-fin, but violating D-MIN. Without D-CTG/D-MIN established at the output, D-SEQ does not apply.
**Required**: Replace the circular argument with: K.μ~ decomposes into K.μ⁻ + K.μ⁺. K.μ⁺ (amended) requires M'(d) to satisfy D-CTG and D-MIN as a postcondition. Therefore D-CTG and D-MIN hold for M'(d). D-SEQ then applies at the output state. Combined with equal cardinality (from the bijection and link-subspace fixity), V_S(d') = V_S(d). The same fix applies to the claim "S8 follows similarly" — state that S8 is derived from the now-established S8-fin, S8a, S2, S8-depth, D-CTG, D-MIN via the same derivation chain as ASN-0036.

### Issue 3: S3★-aux missing from ExtendedReachableStateInvariants
**ASN-0063, ExtendedReachableStateInvariants theorem**: the conjunction lists S3★ but not S3★-aux
**Problem**: S3★-aux — `(A d, v : v ∈ dom(M(d)) : subspace(v) = s_C ∨ subspace(v) = s_L)` — is proved by its own induction, listed in the Properties table, and used critically in the K.μ~ link-subspace fixity argument. The fixity proof eliminates the case `subspace(π(v)) = s_C` for a link-subspace position by showing it violates S3★'s content clause (since `M'(d)(π(v)) ∈ dom(L)` and `dom(L) ∩ dom(C) = ∅`). But this elimination requires knowing `subspace(π(v)) ∈ {s_C, s_L}` — which is S3★-aux. S3★ alone does not exclude a hypothetical third subspace value `s_X` for which S3★'s conditionals are vacuously true. The theorem's invariant conjunction is therefore incomplete: the inductive step (K.μ~ case) requires a property not listed in the inductive hypothesis.
**Required**: Add S3★-aux to the ExtendedReachableStateInvariants conjunction. Alternatively, strengthen S3★ to: `(A d, v : v ∈ dom(M(d)) : (subspace(v) = s_C ∧ M(d)(v) ∈ dom(C)) ∨ (subspace(v) = s_L ∧ M(d)(v) ∈ dom(L)))` — a disjunctive form that subsumes both S3★ and S3★-aux, eliminating the gap.

## OUT_OF_SCOPE

### Topic 1: K.μ⁺_L origin restriction
K.μ⁺_L requires `ℓ ∈ dom(L)` and `d ∈ E_doc` but does not require `origin(ℓ) = d`. This permits placing a link originated by document X into document Y's arrangement — blurring Nelson's ownership model ("a document consists of its contents and its out-links"). The generality is likely intentional: the ASN notes that "A mechanism for link inheritance under forking, if desired, would require K.μ⁺_L steps in the fork composite," implying the transition is designed to be composed into future operations. Whether to restrict K.μ⁺_L to home-document links or to leave it general (with link inheritance as the explicit use case) is a design question for a future ASN on link lifecycle or version semantics.
**Why out of scope**: This is an architectural design choice about the ownership model under composition, not an error in this ASN's definitions or proofs. CREATELINK always produces `origin(ℓ) = d`, so the unrestricted case never arises within this ASN's composite.

VERDICT: REVISE
