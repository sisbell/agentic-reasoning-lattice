# Review of ASN-0047

## REVISE

### Issue 1: K.μ~-FIX jumps from per-subspace cardinality equality to set equality without establishing depth preservation

**ASN-0047, *Decomposition of K.μ~*, K.μ~-FIX (Domain fixity)**: "D-SEQ★ at the pre- and post-states gives `V_S(d) = {[S, 1, ..., 1, k] : 1 ≤ k ≤ n_S}` and `V_S(d') = {[S, 1, ..., 1, k] : 1 ≤ k ≤ n'_S}` for each subspace S; since π is a bijection and (by subspace preservation) bijects V_S(d) onto V_S(d'), `n'_S = n_S` and `V_S(d') = V_S(d)`."

**Problem**: The bijection plus subspace preservation establishes `n'_S = n_S` (equal cardinality per subspace), but the leap to `V_S(d') = V_S(d)` requires the two canonical sequences to share the same depth `m_S`. Subspace preservation, derived in Step (A), fixes only the **first component** (`subspace(π(v)) = v₁`); it says nothing about `#π(v)`. Nothing in K.μ~'s admissibility filter constrains π to preserve V-position length. Concretely, take `V_{s_C}(d) = {[1,1], [1,2]}` (depth 2) and the bijection π([1,1]) = [1,1,1], π([1,2]) = [1,1,2] (depth 3). The induced `M'(d)` has `V_{s_C}(d') = {[1,1,1], [1,1,2]}`, which satisfies D-CTG★ (contiguous), D-MIN★ (`min = [s_C,1,1]`), D-SEQ★ (`{[s_C,1,k]:1≤k≤2}`), S8-depth (uniform depth 3), S8a, and S3★ — so admissibility (i) holds — and clause (ii) holds because `dom(M'(d)) ≠ dom(M(d))`. Yet `dom(M'(d)) = {[1,1,1],[1,1,2]} ≠ {[1,1],[1,2]} = dom(M(d))`, falsifying K.μ~-FIX. The full-clearance realization can produce exactly this: K.μ⁻ empties the content subspace, then K.μ⁺ first-insertion re-pins the depth at any `m ≥ 2` (per the K.μ⁺ "first content insertion" rule). So the named composite genuinely admits depth-changing π.

This cascades: the necessity proof cites "K.μ~-FIX (`dom(M'(d)) = dom(M(d))`)" to assert "π is a bijection of a fixed domain," and Step (1) of the link-subspace fixity proof derives `dom_L(M'(d)) = dom_L(M(d))` from "K.μ~-FIX's per-subspace decomposition (`n'_S = n_S`)" — both inherit the unsound set-equality step. The abstract admissibility filter is strictly broader than what the K.μ⁻ + K.μ⁺ realization can achieve, and K.μ~-FIX papers over the gap.

**Required**: Add a depth-preservation conjunct to K.μ~'s admissibility — e.g., require `#π(v) = #v` for every `v ∈ dom(M(d))` (equivalently, restrict the bijection equation to length-preserving π) — and derive it where it is currently assumed, or prove depth preservation from an additional constraint. Then `V_S(d') = V_S(d)` follows from `n'_S = n_S` plus equal depth. Repair the necessity proof and link-fixity Step (1), which both rest on the fixed-domain claim.

### Issue 2: Reviser-drift — the "caller-checked guard / GlobalUniqueness preserves, does not supply" clarification is restated in four locations

**ASN-0047**, appears in (a) *K.δ case (ii) discharge*: "it is a caller-checked guard, a precondition observed before the event fires, not a conclusion derived afterward. Once the guard has been applied, GlobalUniqueness (ASN-0034) preserves the distinctness invariant that always applying it maintains — GlobalUniqueness preserves distinctness, it does not supply the guard."; (b) *Class (a) verification, S7d* prose; (c) the *ExtendedReachableStateInvariants* S7d note; (d) the *Entity distinctness* corollary.

**Problem**: The same epistemic clarification — "freshness `e ∉ E` is a precondition checked by the caller, and GlobalUniqueness preserves the resulting distinctness rather than supplying the guard" — is reproduced in different words across four separated sections. This is the "two paragraphs in different sections say the same thing" / reviser-drift pattern: the clarification advances nothing on re-statement, and a reader following the S7d discharge must skip past prose already absorbed at the K.δ catalogue. It compounds the document length without adding argument.

**Required**: State the guard-vs-preservation distinction once at the K.δ case (ii) discharge and have S7d, the ExtendedReachableStateInvariants note, and the Entity-distinctness corollary cite it by reference rather than re-prosecute it.

### Issue 3: J1'★ derivation contains a defensive "what does not close the gap" essay before stating what does

**ASN-0047, *Scoped coupling constraints*, J1'★ derivation**: "What closes that gap is neither the step-local calculus nor J0 + P2. Consider a *record-then-strip* composite ... Every elementary precondition holds at each intermediate state ... J0 does *not* forbid this ... What renders this composite invalid is **J1'★ itself** ... J0 closes only the *freshly-allocated* sub-case ... the general record-then-strip case is excluded by J1'★ as a boundary constraint, not by the step-local calculus."

**Problem**: The substantive content — that J1'★'s Σ'-witness form is a boundary validity condition excluding the record-then-strip composite — is one sentence. It is wrapped in a multi-sentence defensive narration of what does *not* close the gap (step-local calculus, J0, P2), restating the same exclusion three times in different framings. The concrete record-then-strip composite is legitimate to keep; the surrounding "neither X nor Y, but Z, and to be clear not X" scaffolding is meta-prose in a derivation slot.

**Required**: Keep the record-then-strip example and the single sentence identifying J1'★'s boundary form as the closer; delete the repeated negative framing ("neither the step-local calculus nor J0 + P2," "J0 does not forbid," "not by the step-local calculus").

## OUT_OF_SCOPE

None. The Open Questions section already routes future topics (link inheritance under forking, concurrency/serialization of allocation, tombstoning mechanisms, account-level versioning) to later ASNs appropriately.

VERDICT: REVISE
